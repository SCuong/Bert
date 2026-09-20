"""
data.py - Module nạp, tiền xử lý và phân chia dữ liệu cho đồ án BERT Hotel Reviews.
Tuân thủ tiêu chuẩn học thuật:
- Giữ nguyên văn bản tự nhiên cho BERT (không xóa stopwords, không lemmatize câu).
- Phân chia Stratified Train/Val/Test (70/10/20) với random seed = 42.
- Kiểm tra tính toàn vẹn dữ liệu, loại bỏ dữ liệu rỗng và phân tích phân bố độ dài.
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

# Đường dẫn ưu tiên dữ liệu nội bộ trong BERT_Project/data/
DEFAULT_RAW_DATA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "dts_20k_raw.csv")
)
FALLBACK_RAW_DATA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Bài giảng", "AI.Code", "NLP_Demo", "dts_20k_raw.csv")
)

def clean_text_minimal(text: str) -> str:
    """
    Tiền xử lý tối thiểu dành cho mô hình ngôn ngữ (BERT):
    - Xóa thẻ HTML (<br />, <p>, v.v.)
    - Chuẩn hóa khoảng trắng
    - Giữ nguyên dấu câu, chữ hoa/thường, từ phủ định để bảo tồn ngữ cảnh.
    """
    if not isinstance(text, str):
        return ""
    # Xóa HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # Chuẩn hóa khoảng trắng
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_and_clean_data(file_path: str = None) -> pd.DataFrame:
    """
    Nạp dữ liệu từ file CSV, làm sạch tối thiểu và loại bỏ các mẫu rỗng.
    """
    if file_path is None:
        if os.path.exists(DEFAULT_RAW_DATA_PATH):
            file_path = DEFAULT_RAW_DATA_PATH
        elif os.path.exists(FALLBACK_RAW_DATA_PATH):
            file_path = FALLBACK_RAW_DATA_PATH
        else:
            file_path = DEFAULT_RAW_DATA_PATH
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")
        
    print(f"[*] Đang nạp dữ liệu từ: {file_path}")
    df = pd.read_csv(file_path)
    
    # Kiểm tra cấu trúc cột
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError(f"Dữ liệu phải chứa cột 'text' và 'label'. Cột hiện có: {df.columns.tolist()}")
        
    initial_count = len(df)
    
    # Áp dụng clean_text_minimal
    df["text"] = df["text"].apply(clean_text_minimal)
    
    # Ép kiểu nhãn về int
    df["label"] = df["label"].astype(int)
    
    # Loại bỏ các dòng rỗng
    df = df[df["text"].str.strip().str.len() > 0].copy()
    cleaned_count = len(df)
    dropped_count = initial_count - cleaned_count
    
    print(f"[*] Tổng số mẫu ban đầu: {initial_count}")
    print(f"[*] Đã loại bỏ {dropped_count} mẫu rỗng.")
    print(f"[*] Tổng số mẫu hợp lệ: {cleaned_count}")
    print(f"[*] Phân bố nhãn:\n{df['label'].value_counts().to_dict()}")
    
    return df

def split_data(df: pd.DataFrame, train_ratio=0.7, val_ratio=0.1, test_ratio=0.2, random_state=42):
    """
    Phân chia dữ liệu thành Train, Validation và Test theo phương pháp Stratified Split.
    Cố định random_state=42 để đảm bảo tính tái lập.
    """
    assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5, "Tổng tỷ lệ phân chia phải bằng 1.0"
    
    # Bước 1: Tách Test set (20%)
    sss_test = StratifiedShuffleSplit(n_splits=1, test_size=test_ratio, random_state=random_state)
    for train_val_idx, test_idx in sss_test.split(df, df["label"]):
        train_val_df = df.iloc[train_val_idx].copy()
        test_df = df.iloc[test_idx].copy()
        
    # Bước 2: Tách Val set từ phần còn lại (10% của tổng số mẫu -> val_ratio / (train_ratio + val_ratio))
    val_rel_ratio = val_ratio / (train_ratio + val_ratio)
    sss_val = StratifiedShuffleSplit(n_splits=1, test_size=val_rel_ratio, random_state=random_state)
    for train_idx, val_idx in sss_val.split(train_val_df, train_val_df["label"]):
        train_df = train_val_df.iloc[train_idx].copy()
        val_df = train_val_df.iloc[val_idx].copy()
        
    print(f"[*] Phân chia tập dữ liệu hoàn tất (seed={random_state}):")
    print(f"    - Train set: {len(train_df)} mẫu ({len(train_df)/len(df)*100:.1f}%) | Phân bố: {train_df['label'].value_counts().to_dict()}")
    print(f"    - Val set:   {len(val_df)} mẫu ({len(val_df)/len(df)*100:.1f}%) | Phân bố: {val_df['label'].value_counts().to_dict()}")
    print(f"    - Test set:  {len(test_df)} mẫu ({len(test_df)/len(df)*100:.1f}%) | Phân bố: {test_df['label'].value_counts().to_dict()}")
    
    return train_df, val_df, test_df

def analyze_and_plot_data(df: pd.DataFrame, output_dir: str = None):
    """
    Phân tích thống kê độ dài từ và xuất các biểu đồ trực quan hóa sang artifacts/figures.
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts", "figures"))
    os.makedirs(output_dir, exist_ok=True)
    
    df["word_count"] = df["text"].apply(lambda x: len(x.split()))
    df["char_count"] = df["text"].apply(len)
    
    print("\n" + "="*50)
    print("THỐNG KÊ ĐỘ DÀI TỪ (WORD COUNT STATS):")
    print(df["word_count"].describe(percentiles=[0.25, 0.5, 0.75, 0.90, 0.95, 0.99]))
    print("="*50 + "\n")
    
    # 1. Vẽ biểu đồ phân bố nhãn
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
    
    # 2. Vẽ biểu đồ phân bố độ dài từ
    plt.figure(figsize=(9, 4.5))
    sns.histplot(data=df, x="word_count", hue="label", bins=50, kde=True, palette=["#e74c3c", "#2ecc71"], alpha=0.5)
    plt.axvline(x=128, color="#34495e", linestyle="--", linewidth=1.5, label="Max length = 128")
    plt.axvline(x=256, color="#8e44ad", linestyle=":", linewidth=1.5, label="Max length = 256")
    plt.title("Review Length Distribution by Class (Word Count)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Number of Words", fontsize=11)
    plt.ylabel("Frequency", fontsize=11)
    plt.legend(["Negative (0)", "Positive (1)", "Cutoff 128", "Cutoff 256"], loc="upper right")
    plt.xlim(0, 400)
    plt.tight_layout()
    length_fig_path = os.path.join(output_dir, "length_distribution.png")
    plt.savefig(length_fig_path, dpi=300)
    plt.close()
    print(f"[+] Đã lưu biểu đồ phân bố độ dài tại: {length_fig_path}")

if __name__ == "__main__":
    df = load_and_clean_data()
    analyze_and_plot_data(df)
    train_df, val_df, test_df = split_data(df)
