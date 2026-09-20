"""
data.py - Module nạp, kiểm tra tính toàn vẹn (Data Audit), xử lý rò rỉ dữ liệu và phân chia Train/Val/Test.
Tuân thủ nghiêm ngặt nguyên tắc Clean-Room & Chống Data Leakage:
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
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.pyplot as plt
import seaborn as sns

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Import cấu hình tập trung
from src.config import (
    DEFAULT_DATA_PATH,
    FALLBACK_DATA_PATH,
    FIGURES_DIR,
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

    # 2. Missing values & Minimal Cleaning
    null_text_count = df["text"].isnull().sum()
    null_label_count = df["label"].isnull().sum()
    
    df["text"] = df["text"].apply(clean_text_minimal)
    empty_text_count = (df["text"].str.len() == 0).sum()
    
    # Loại bỏ null và rỗng
    df = df[df["text"].str.len() > 0].copy()
    
    # 3. Validate Labels (phải thuộc {0, 1})
    try:
        df["label"] = df["label"].astype(int)
    except Exception as e:
        raise ValueError(f"Không thể ép kiểu cột 'label' về số nguyên: {e}")
        
    invalid_labels = set(df["label"].unique()) - {0, 1}
    if invalid_labels:
        raise ValueError(f"Phát hiện nhãn không hợp lệ ngoài miền {{0, 1}}: {invalid_labels}")

    # 4. Duplicate & Data Leakage Audit trước khi split
    # a. Kiểm tra văn bản trùng lặp nhưng xung đột nhãn (cùng text nhưng vừa gắn 0 vừa gắn 1)
    text_label_counts = df.groupby("text")["label"].nunique()
    conflicting_texts = text_label_counts[text_label_counts > 1].index
    conflicting_count = len(conflicting_texts)
    
    if conflicting_count > 0:
        print(f"[!] CẢNH BÁO: Phát hiện {conflicting_count} văn bản có nhãn xung đột (Conflicting Labels). Loại bỏ toàn bộ để tránh nhiễu.")
        df = df[~df["text"].isin(conflicting_texts)].copy()

    # b. Kiểm tra và loại bỏ exact duplicate text
    exact_duplicates_count = df.duplicated(subset=["text"]).sum()
    if exact_duplicates_count > 0:
        print(f"[!] Phát hiện {exact_duplicates_count} mẫu trùng lặp hoàn toàn (Exact Duplicates). Loại bỏ để chống rò rỉ dữ liệu qua Test Set.")
        df = df.drop_duplicates(subset=["text"], keep="first").copy()

    final_count = len(df)
    total_dropped = initial_count - final_count

    print("\n" + "="*50)
    print("BÁO CÁO TOÀN VẸN DỮ LIỆU (DATA AUDIT REPORT):")
    print(f"- Số mẫu ban đầu:              {initial_count}")
    print(f"- Mẫu bị thiếu / rỗng (Dropped): {empty_text_count + null_text_count + null_label_count}")
    print(f"- Mẫu xung đột nhãn (Dropped):   {conflicting_count}")
    print(f"- Mẫu trùng lặp text (Dropped):  {exact_duplicates_count}")
    print(f"- Tổng số mẫu bị loại bỏ:       {total_dropped}")
    print(f"- Số mẫu hợp lệ duy nhất:        {final_count}")
    print(f"- Phân bố nhãn sau làm sạch:     {df['label'].value_counts().to_dict()}")
    print("="*50 + "\n")

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
    print("[+] XÁC NHẬN: 100% không có rò rỉ dữ liệu (Zero Overlap giữa Train, Val và Test).")

    print(f"[*] Phân chia tập dữ liệu hoàn tất (seed={random_state}):")
    print(f"    - Train set: {len(train_df)} mẫu ({len(train_df)/len(df)*100:.1f}%) | Phân bố: {train_df['label'].value_counts().to_dict()}")
    print(f"    - Val set:   {len(val_df)} mẫu ({len(val_df)/len(df)*100:.1f}%) | Phân bố: {val_df['label'].value_counts().to_dict()}")
    print(f"    - Test set:  {len(test_df)} mẫu ({len(test_df)/len(df)*100:.1f}%) | Phân bố: {test_df['label'].value_counts().to_dict()}")

    return train_df, val_df, test_df

def analyze_and_plot_data(df: pd.DataFrame, output_dir: str = None):
    """
    Đo lường độ dài token thực tế bằng BERT Tokenizer và xuất các biểu đồ trực quan hóa.
    """
    if output_dir is None:
        output_dir = FIGURES_DIR
    os.makedirs(output_dir, exist_ok=True)

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
        
        # Tokenize không truncate để đo chiều dài thực
        token_lengths = [len(tokenizer.encode(t, truncation=False)) for t in df["text"]]
        df["token_length"] = token_lengths
        
        print("\n" + "="*50)
        print("THỐNG KÊ ĐỘ DÀI TOKEN THỰC TẾ (BERT TOKENIZER STATS):")
        stats = df["token_length"].describe(percentiles=[0.25, 0.5, 0.75, 0.90, 0.95, 0.99])
        print(stats)
        print("="*50 + "\n")
        
        # Vẽ biểu đồ phân bố độ dài token
        plt.figure(figsize=(9, 4.5))
        sns.histplot(data=df, x="token_length", hue="label", bins=50, kde=True, palette=["#e74c3c", "#2ecc71"], alpha=0.5)
        plt.axvline(x=128, color="#34495e", linestyle="--", linewidth=1.5, label="Cutoff 128")
        plt.axvline(x=256, color="#8e44ad", linestyle=":", linewidth=1.5, label="Cutoff 256")
        plt.title(f"BERT Token Length Distribution ({MODEL_NAME})", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Number of Tokens", fontsize=11)
        plt.ylabel("Frequency", fontsize=11)
        plt.legend(loc="upper right")
        plt.xlim(0, 400)
        plt.tight_layout()
        token_fig_path = os.path.join(output_dir, "token_length_distribution.png")
        plt.savefig(token_fig_path, dpi=300)
        plt.close()
        print(f"[+] Đã lưu biểu đồ phân bố độ dài token tại: {token_fig_path}")
        
    except Exception as e:
        print(f"[!] Không thể chạy BERT tokenizer để đo token length (có thể do môi trường offline): {e}")
        print("[!] Giữ trạng thái phân tích độ dài token là [PENDING EXPERIMENT].")

if __name__ == "__main__":
    df = load_and_validate_data()
    train_df, val_df, test_df = split_data(df)
