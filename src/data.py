"""
data.py - Module nạp, kiểm tra tính toàn vẹn (Data Audit), xử lý rò rỉ dữ liệu và phân chia Train/Val/Test.
Triển khai độc lập từ đầu (independent implementation from scratch; reference code was not reused) & Chống Data Leakage:
1. Validate schema và miền giá trị nhãn {0, 1}.
2. Kiểm tra missing values và chuỗi rỗng.
3. Phân tích và loại bỏ trùng lặp tuyệt đối (Exact Duplicates) trước khi split.
4. Phát hiện và xử lý trùng lặp xung đột nhãn (Conflicting Labels).
5. Phân chia Stratified Split và xác nhận không có bất kỳ văn bản nào xuất hiện đồng thời ở Train và Test.
6. Đo lường độ dài token bằng chính BERT Tokenizer thực tế thay vì đếm từ giả định.
"""

import os
import sys
import re
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.pyplot as plt
import seaborn as sns

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Đảm bảo repository root luôn có trong sys.path khi chạy trực tiếp hoặc dạng module
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Import cấu hình tập trung
from src.config import (
    DEFAULT_DATA_PATH,
    FALLBACK_DATA_PATH,
    FIGURES_DIR,
    METRICS_DIR,
    TOKEN_STATS_PATH,
    RANDOM_SEED,
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
    MODEL_NAME,
    MAX_LENGTH
)

def clean_text_minimal(text: str) -> str:
    """
    Tiền xử lý tối thiểu dành cho mô hình Transformer:
    - Xóa thẻ HTML (<br />, <p>, v.v.)
    - Chuẩn hóa khoảng trắng
    - Giữ nguyên dấu câu, chữ hoa/thường, từ phủ định để bảo tồn ngữ cảnh.
    """
    if not isinstance(text, str):
        return ""
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_and_validate_data(file_path: str = None) -> pd.DataFrame:
    """
    Nạp dữ liệu, thực hiện Data Audit toàn diện và loại bỏ duplicate/rò rỉ trước khi split.
    Xử lý rõ ràng và không double-count:
    1. Validate schema (phải có cột 'text' và 'label').
    2. Missing values: Kiểm tra và loại bỏ các dòng có text null hoặc label null.
    3. Empty text: Làm sạch tối thiểu và loại bỏ các dòng có text rỗng sau khi làm sạch.
    4. Validate nhãn: Ép kiểu về int và kiểm tra nghiêm ngặt nhãn chỉ thuộc {0, 1}.
    5. Conflicting labels: Phát hiện và loại bỏ các dòng có text trùng lặp nhưng nhãn khác nhau.
    6. Exact duplicates: Loại bỏ các dòng trùng lặp text hoàn toàn để chống rò rỉ qua Test Set.
    """
    if file_path is None:
        if os.path.exists(DEFAULT_DATA_PATH):
            file_path = DEFAULT_DATA_PATH
        elif os.path.exists(FALLBACK_DATA_PATH):
            file_path = FALLBACK_DATA_PATH
        else:
            file_path = DEFAULT_DATA_PATH

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")

    print(f"[*] Đang nạp dữ liệu từ: {file_path}")
    df = pd.read_csv(file_path)
    initial_count = len(df)

    # 1. Validate Schema
    required_cols = {"text", "label"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Dữ liệu thiếu cột bắt buộc. Yêu cầu: {required_cols}, Hiện có: {df.columns.tolist()}")

    # 2. Missing values handling (kiểm tra trước khi ép kiểu để tránh lỗi non-finite)
    null_text_mask = df["text"].isnull()
    null_label_mask = df["label"].isnull()
    missing_rows_mask = null_text_mask | null_label_mask

    null_text_count = int(null_text_mask.sum())
    null_label_count = int(null_label_mask.sum())
    missing_rows_count = int(missing_rows_mask.sum())

    # Loại bỏ các dòng có text null hoặc label null
    df = df[~missing_rows_mask].copy()

    # 3. Minimal text cleaning & Empty text check
    df["text"] = df["text"].apply(clean_text_minimal)
    empty_text_mask = (df["text"].str.len() == 0)
    empty_text_count = int(empty_text_mask.sum())
    df = df[~empty_text_mask].copy()

    # 4. Validate và chuyển đổi nhãn (sau khi đã loại bỏ toàn bộ missing labels)
    try:
        df["label"] = pd.to_numeric(df["label"], errors="raise").astype(int)
    except Exception as e:
        raise ValueError(f"Không thể ép kiểu cột 'label' về số nguyên: {e}")

    invalid_labels = set(df["label"].unique()) - {0, 1}
    if invalid_labels:
        raise ValueError(f"Phát hiện nhãn không hợp lệ ngoài miền {{0, 1}}: {invalid_labels}")

    # 5. Conflicting labels audit (cùng text nhưng vừa gắn 0 vừa gắn 1)
    text_label_counts = df.groupby("text")["label"].nunique()
    conflicting_texts = text_label_counts[text_label_counts > 1].index
    conflicting_rows_mask = df["text"].isin(conflicting_texts)
    conflicting_rows_count = int(conflicting_rows_mask.sum())
    conflicting_unique_texts = len(conflicting_texts)

    if conflicting_rows_count > 0:
        print(f"[!] CẢNH BÁO: Phát hiện {conflicting_unique_texts} văn bản ({conflicting_rows_count} dòng) có nhãn xung đột (Conflicting Labels). Loại bỏ toàn bộ để tránh nhiễu.")
        df = df[~conflicting_rows_mask].copy()

    # 6. Exact duplicates audit (loại bỏ trùng lặp text giữ lại mẫu đầu tiên)
    exact_duplicates_count = int(df.duplicated(subset=["text"]).sum())
    if exact_duplicates_count > 0:
        print(f"[!] Phát hiện {exact_duplicates_count} mẫu trùng lặp văn bản hoàn toàn (Exact Duplicates). Loại bỏ để chống rò rỉ dữ liệu qua Test Set.")
        df = df.drop_duplicates(subset=["text"], keep="first").copy()

    final_count = len(df)
    total_dropped = initial_count - final_count

    # Ràng buộc kiểm toán tính toàn vẹn: Không double-count số mẫu bị loại
    assert total_dropped == (missing_rows_count + empty_text_count + conflicting_rows_count + exact_duplicates_count), \
        f"Lệch kiểm toán mẫu: {total_dropped} != {missing_rows_count} + {empty_text_count} + {conflicting_rows_count} + {exact_duplicates_count}"

    print("\n" + "="*55)
    print("BÁO CÁO TOÀN VẸN DỮ LIỆU (DATA AUDIT REPORT):")
    print(f"- Số mẫu ban đầu:                {initial_count}")
    print(f"- Mẫu thiếu text / label:        {missing_rows_count} (null text: {null_text_count}, null label: {null_label_count})")
    print(f"- Mẫu rỗng sau khi làm sạch:     {empty_text_count}")
    print(f"- Mẫu có nhãn xung đột (Dropped):{conflicting_rows_count} ({conflicting_unique_texts} cụm text)")
    print(f"- Mẫu trùng lặp text (Dropped):  {exact_duplicates_count}")
    print(f"- Tổng số mẫu bị loại bỏ:        {total_dropped}")
    print(f"- Số mẫu hợp lệ duy nhất:        {final_count}")
    print(f"- Phân bố nhãn sau làm sạch:     {df['label'].value_counts().to_dict()}")
    print("="*55 + "\n")

    return df

def split_data(df: pd.DataFrame, train_ratio=TRAIN_RATIO, val_ratio=VAL_RATIO, test_ratio=TEST_RATIO, random_state=RANDOM_SEED):
    """
    Phân chia dữ liệu Stratified (Train/Val/Test) và kiểm tra triệt để không có rò rỉ dữ liệu.
    """
    assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5, "Tổng tỷ lệ phân chia phải bằng 1.0"

    # Tách Test Set độc lập
    sss_test = StratifiedShuffleSplit(n_splits=1, test_size=test_ratio, random_state=random_state)
    for train_val_idx, test_idx in sss_test.split(df, df["label"]):
        train_val_df = df.iloc[train_val_idx].copy()
        test_df = df.iloc[test_idx].copy()

    # Tách Val Set từ Train_Val
    val_rel_ratio = val_ratio / (train_ratio + val_ratio)
    sss_val = StratifiedShuffleSplit(n_splits=1, test_size=val_rel_ratio, random_state=random_state)
    for train_idx, val_idx in sss_val.split(train_val_df, train_val_df["label"]):
        train_df = train_val_df.iloc[train_idx].copy()
        val_df = train_val_df.iloc[val_idx].copy()

    # Xác thực chống Data Leakage (Không có giao thoa văn bản giữa các tập)
    train_texts = set(train_df["text"])
    val_texts = set(val_df["text"])
    test_texts = set(test_df["text"])

    leakage_train_test = train_texts.intersection(test_texts)
    leakage_val_test = val_texts.intersection(test_texts)
    leakage_train_val = train_texts.intersection(val_texts)

    if leakage_train_test or leakage_val_test or leakage_train_val:
        raise RuntimeError(
            f"Phát hiện rò rỉ dữ liệu (Data Leakage)! "
            f"Train-Test overlap: {len(leakage_train_test)}, "
            f"Val-Test overlap: {len(leakage_val_test)}, "
            f"Train-Val overlap: {len(leakage_train_val)}"
        )
    print("[+] XÁC NHẬN: Không có rò rỉ dữ liệu (Zero Overlap giữa Train, Val và Test).")

    print(f"[*] Phân chia tập dữ liệu hoàn tất (seed={random_state}):")
    print(f"    - Train set: {len(train_df)} mẫu ({len(train_df)/len(df)*100:.1f}%) | Phân bố: {train_df['label'].value_counts().to_dict()}")
    print(f"    - Val set:   {len(val_df)} mẫu ({len(val_df)/len(df)*100:.1f}%) | Phân bố: {val_df['label'].value_counts().to_dict()}")
    print(f"    - Test set:  {len(test_df)} mẫu ({len(test_df)/len(df)*100:.1f}%) | Phân bố: {test_df['label'].value_counts().to_dict()}")

    return train_df, val_df, test_df

def analyze_and_plot_data(df: pd.DataFrame, output_dir: str = None):
    """
    Đo lường độ dài token thực tế bằng BERT Tokenizer và xuất các biểu đồ trực quan hóa.
    Tính toán các phân vị: median, p90, p95, p99, tỷ lệ cắt cụt tại 128 và 256.
    KHÔNG huấn luyện bất kỳ mô hình nào tại bước này.
    """
    if output_dir is None:
        output_dir = FIGURES_DIR
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)

    # 1. Vẽ phân bố nhãn
    plt.figure(figsize=(6, 4))
    sns.set_theme(style="whitegrid")
    ax = sns.countplot(data=df, x="label", palette=["#e74c3c", "#2ecc71"])
    plt.title("Class Distribution (0: Negative, 1: Positive)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Sentiment Label", fontsize=11)
    plt.ylabel("Number of Samples", fontsize=11)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                    ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    plt.tight_layout()
    class_fig_path = os.path.join(output_dir, "class_distribution.png")
    plt.savefig(class_fig_path, dpi=300)
    plt.close()
    print(f"[+] Đã lưu biểu đồ phân bố nhãn tại: {class_fig_path}")

    # 2. Đo lường Token Length bằng BERT Tokenizer thực tế
    try:
        from transformers import AutoTokenizer
        print(f"[*] Đang tải tokenizer thực tế '{MODEL_NAME}' để đo lường phân bố độ dài token...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        token_lengths = [len(tokenizer.encode(t, truncation=False)) for t in df["text"]]
        token_lengths_arr = np.array(token_lengths)
        df_copy = df.copy()
        df_copy["token_length"] = token_lengths

        # Tính toán các chỉ số phân vị theo yêu cầu
        stats_dict = {
            "total_samples": int(len(token_lengths_arr)),
            "mean": float(np.mean(token_lengths_arr)),
            "std": float(np.std(token_lengths_arr)),
            "min": int(np.min(token_lengths_arr)),
            "median": float(np.median(token_lengths_arr)),
            "p90": float(np.percentile(token_lengths_arr, 90)),
            "p95": float(np.percentile(token_lengths_arr, 95)),
            "p99": float(np.percentile(token_lengths_arr, 99)),
            "max": int(np.max(token_lengths_arr)),
            "pct_truncated_at_128": float((token_lengths_arr > 128).mean() * 100),
            "pct_truncated_at_256": float((token_lengths_arr > 256).mean() * 100),
            "candidate_max_length": MAX_LENGTH
        }

        print("\n" + "="*55)
        print("THỐNG KÊ PHÂN VỊ ĐỘ DÀI TOKEN THỰC TẾ (BERT TOKENIZER):")
        print(f"- Tổng số mẫu kiểm tra:       {stats_dict['total_samples']:,}")
        print(f"- Giá trị trung bình (Mean):   {stats_dict['mean']:.2f} tokens")
        print(f"- Độ lệch chuẩn (Std):         {stats_dict['std']:.2f} tokens")
        print(f"- Giá trị nhỏ nhất (Min):      {stats_dict['min']} tokens")
        print(f"- Trung vị (Median / p50):     {stats_dict['median']:.1f} tokens")
        print(f"- Phân vị 90 (p90):            {stats_dict['p90']:.1f} tokens")
        print(f"- Phân vị 95 (p95):            {stats_dict['p95']:.1f} tokens")
        print(f"- Phân vị 99 (p99):            {stats_dict['p99']:.1f} tokens")
        print(f"- Giá trị lớn nhất (Max):      {stats_dict['max']} tokens")
        print(f"- Tỷ lệ cắt cụt nếu chọn 128:  {stats_dict['pct_truncated_at_128']:.2f}%")
        print(f"- Tỷ lệ cắt cụt nếu chọn 256:  {stats_dict['pct_truncated_at_256']:.2f}%")
        print(f"- Ngưỡng candidate hiện tại:   {MAX_LENGTH}")
        print("="*55 + "\n")

        with open(TOKEN_STATS_PATH, "w", encoding="utf-8") as f:
            json.dump(stats_dict, f, indent=4, ensure_ascii=False)
        print(f"[+] Đã lưu số liệu thống kê độ dài token tại: {TOKEN_STATS_PATH}")

        # Vẽ biểu đồ phân bố độ dài token
        plt.figure(figsize=(9, 4.5))
        sns.histplot(data=df_copy, x="token_length", hue="label", bins=50, kde=True, palette=["#e74c3c", "#2ecc71"], alpha=0.5)
        plt.axvline(x=128, color="#34495e", linestyle="--", linewidth=1.5, label=f"Cutoff 128 ({stats_dict['pct_truncated_at_128']:.1f}% truncated)")
        plt.axvline(x=256, color="#8e44ad", linestyle=":", linewidth=1.5, label=f"Cutoff 256 ({stats_dict['pct_truncated_at_256']:.1f}% truncated)")
        plt.title(f"BERT Token Length Distribution ({MODEL_NAME})", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Number of Tokens", fontsize=11)
        plt.ylabel("Frequency", fontsize=11)
        plt.legend(loc="upper right")
        plt.xlim(0, max(400, int(stats_dict['p99'] * 1.2)))
        plt.tight_layout()
        token_fig_path = os.path.join(output_dir, "token_length_distribution.png")
        plt.savefig(token_fig_path, dpi=300)
        plt.close()
        print(f"[+] Đã lưu biểu đồ phân bố độ dài token tại: {token_fig_path}")

    except Exception as e:
        print(f"[!] Không thể chạy BERT tokenizer để đo token length: {e}")
        print("[!] Giữ trạng thái phân tích độ dài token là [PENDING EXPERIMENT].")

if __name__ == "__main__":
    df = load_and_validate_data()
    train_df, val_df, test_df = split_data(df)
    analyze_and_plot_data(df)
