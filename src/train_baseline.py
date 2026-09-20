"""
train_baseline.py - Huấn luyện mô hình cơ sở TF-IDF + Logistic Regression
Mục đích: Thiết lập mốc chuẩn (Baseline) tối thiểu theo đúng tinh thần AI Project Cycle:
"Start from simple to more complex models because our solutions need to be as compact as possible."
"""

import os
import sys
import time
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

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
    BASELINE_MODEL_PATH,
    BASELINE_VAL_METRICS_PATH,
    BASELINE_VAL_CM_PATH,
    FIGURES_DIR,
    RANDOM_SEED
)
from src.data import load_and_validate_data, get_train_val_split

def train_and_evaluate_baseline():
    print("="*60)
    print("BẮT ĐẦU HUẤN LUYỆN MÔ HÌNH BASELINE: TF-IDF + LOGISTIC REGRESSION")
    print("="*60)
    
    # 1. Nạp và phân chia dữ liệu (Tập Test được niêm phong hoàn toàn)
    df = load_and_validate_data()
    train_df, val_df = get_train_val_split(df, random_state=RANDOM_SEED)
    print(f"[*] Phạm vi huấn luyện: Train set ({len(train_df)} mẫu)")
    print(f"[*] Phạm vi đánh giá phát triển (Development Evaluation): Validation set ({len(val_df)} mẫu)")
    print("[*] NGUYÊN TẮC BẢO VỆ TEST SET: Tập Test không được nạp, dự đoán hay đánh giá trong giai đoạn này.")
    
    # 2. Xây dựng Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True,
            strip_accents='unicode'
        )),
        ('clf', LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=RANDOM_SEED,
            solver='lbfgs'
        ))
    ])
    
    # 3. Huấn luyện mô hình trên Train Set
    print("\n[*] Đang huấn luyện mô hình trên Train Set...")
    start_time = time.time()
    pipeline.fit(train_df["text"], train_df["label"])
    training_time = time.time() - start_time
    print(f"[+] Huấn luyện hoàn tất trong {training_time:.2f} giây.")
    
    # 4. Đánh giá phát triển trên Validation Set (KHÔNG chạm vào Test Set)
    print("\n[*] Đang đánh giá hiệu năng phát triển trên Validation Set...")
    eval_start_time = time.time()
    val_preds = pipeline.predict(val_df["text"])
    val_probs = pipeline.predict_proba(val_df["text"])[:, 1]
    inference_time = time.time() - eval_start_time
    
    acc = accuracy_score(val_df["label"], val_preds)
    prec_macro = precision_score(val_df["label"], val_preds, average='macro')
    rec_macro = recall_score(val_df["label"], val_preds, average='macro')
    f1_macro = f1_score(val_df["label"], val_preds, average='macro')
    f1_weighted = f1_score(val_df["label"], val_preds, average='weighted')
    
    prec_per_class = precision_score(val_df["label"], val_preds, average=None)
    rec_per_class = recall_score(val_df["label"], val_preds, average=None)
    f1_per_class = f1_score(val_df["label"], val_preds, average=None)
    
    print("\n" + "="*50)
    print("KẾT QUẢ ĐÁNH GIÁ TRÊN VALIDATION SET (TF-IDF + LOGISTIC REGRESSION):")
    print(f"Validation Accuracy:        {acc*100:.2f}%")
    print(f"Validation Macro Precision: {prec_macro:.4f}")
    print(f"Validation Macro Recall:    {rec_macro:.4f}")
    print(f"Validation Macro F1-score:  {f1_macro:.4f}")
    print(f"Validation Weighted F1:     {f1_weighted:.4f}")
    print(f"Inference Time:             {inference_time:.3f}s ({len(val_df)/inference_time:.1f} samples/s)")
    print("\nChi tiết Classification Report (Validation):")
    print(classification_report(val_df["label"], val_preds, target_names=["Negative (0)", "Positive (1)"], digits=4))
    print("="*50)
    
    # 5. Lưu kết quả validation metrics
    os.makedirs(os.path.dirname(BASELINE_VAL_METRICS_PATH), exist_ok=True)
    cm = confusion_matrix(val_df["label"], val_preds)
    
    metrics_data = {
        "model_name": "TF-IDF + Logistic Regression",
        "evaluation_split": "validation",
        "accuracy": float(acc),
        "macro_precision": float(prec_macro),
        "macro_recall": float(rec_macro),
        "macro_f1": float(f1_macro),
        "weighted_f1": float(f1_weighted),
        "class_0_precision": float(prec_per_class[0]),
        "class_0_recall": float(rec_per_class[0]),
        "class_0_f1": float(f1_per_class[0]),
        "class_1_precision": float(prec_per_class[1]),
        "class_1_recall": float(rec_per_class[1]),
        "class_1_f1": float(f1_per_class[1]),
        "training_time_seconds": float(training_time),
        "inference_time_seconds": float(inference_time),
        "validation_sample_count": len(val_df),
        "confusion_matrix": cm.tolist()
    }
    
    with open(BASELINE_VAL_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu validation metrics tại: {BASELINE_VAL_METRICS_PATH}")
    
    # 6. Vẽ và lưu Validation Confusion Matrix
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Negative (0)", "Positive (1)"],
                yticklabels=["Negative (0)", "Positive (1)"],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title("Baseline Validation Confusion Matrix (TF-IDF + LogReg)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.tight_layout()
    plt.savefig(BASELINE_VAL_CM_PATH, dpi=300)
    plt.close()
    print(f"[+] Đã lưu biểu đồ validation confusion matrix tại: {BASELINE_VAL_CM_PATH}")
    
    # 7. Lưu mô hình đã huấn luyện
    os.makedirs(os.path.dirname(BASELINE_MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, BASELINE_MODEL_PATH)
    print(f"[+] Đã lưu mô hình baseline tại: {BASELINE_MODEL_PATH}")
    
    return metrics_data

if __name__ == "__main__":
    train_and_evaluate_baseline()
