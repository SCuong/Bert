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

# Import cấu hình tập trung
from src.config import (
    BASELINE_MODEL_PATH,
    BASELINE_METRICS_PATH,
    FIGURES_DIR,
    RANDOM_SEED
)
from src.data import load_and_validate_data, split_data

def train_and_evaluate_baseline():
    print("="*60)
    print("BẮT ĐẦU HUẤN LUYỆN MÔ HÌNH BASELINE: TF-IDF + LOGISTIC REGRESSION")
    print("="*60)
    
    # 1. Nạp và phân chia dữ liệu
    df = load_and_validate_data()
    train_df, val_df, test_df = split_data(df, random_state=RANDOM_SEED)
    
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
    
    # 3. Huấn luyện mô hình
    print("\n[*] Đang huấn luyện mô hình...")
    start_time = time.time()
    pipeline.fit(train_df["text"], train_df["label"])
    training_time = time.time() - start_time
    print(f"[+] Huấn luyện hoàn tất trong {training_time:.2f} giây.")
    
    # 4. Đánh giá trên Validation set
    val_preds = pipeline.predict(val_df["text"])
    val_acc = accuracy_score(val_df["label"], val_preds)
    val_f1 = f1_score(val_df["label"], val_preds, average='macro')
    print(f"[*] Validation Accuracy: {val_acc*100:.2f}% | Val Macro F1: {val_f1:.4f}")
    
    # 5. Đánh giá duy nhất trên Test set
    print("\n[*] Đang đánh giá trên tập kiểm thử độc lập (Test Set)...")
    eval_start_time = time.time()
    test_preds = pipeline.predict(test_df["text"])
    test_probs = pipeline.predict_proba(test_df["text"])[:, 1]
    inference_time = time.time() - eval_start_time
    
    acc = accuracy_score(test_df["label"], test_preds)
    prec_macro = precision_score(test_df["label"], test_preds, average='macro')
    rec_macro = recall_score(test_df["label"], test_preds, average='macro')
    f1_macro = f1_score(test_df["label"], test_preds, average='macro')
    f1_weighted = f1_score(test_df["label"], test_preds, average='weighted')
    
    prec_per_class = precision_score(test_df["label"], test_preds, average=None)
    rec_per_class = recall_score(test_df["label"], test_preds, average=None)
    f1_per_class = f1_score(test_df["label"], test_preds, average=None)
    
    print("\n" + "="*50)
    print("KẾT QUẢ ĐÁNH GIÁ TRÊN TEST SET (TF-IDF + LOGISTIC REGRESSION):")
    print(f"Accuracy:        {acc*100:.2f}%")
    print(f"Macro Precision: {prec_macro:.4f}")
    print(f"Macro Recall:    {rec_macro:.4f}")
    print(f"Macro F1-score:  {f1_macro:.4f}")
    print(f"Weighted F1:     {f1_weighted:.4f}")
    print(f"Inference Time:  {inference_time:.3f}s ({len(test_df)/inference_time:.1f} samples/s)")
    print("\nChi tiết Classification Report:")
    print(classification_report(test_df["label"], test_preds, target_names=["Negative (0)", "Positive (1)"], digits=4))
    print("="*50)
    
    # 6. Lưu kết quả metrics
    os.makedirs(os.path.dirname(BASELINE_METRICS_PATH), exist_ok=True)
    cm = confusion_matrix(test_df["label"], test_preds)
    
    metrics_data = {
        "model_name": "TF-IDF + Logistic Regression",
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
        "test_sample_count": len(test_df),
        "confusion_matrix": cm.tolist()
    }
    
    with open(BASELINE_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu metrics tại: {BASELINE_METRICS_PATH}")
    
    # 7. Vẽ và lưu Confusion Matrix
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Negative (0)", "Positive (1)"],
                yticklabels=["Negative (0)", "Positive (1)"],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title("Baseline Confusion Matrix (TF-IDF + LogReg)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.tight_layout()
    cm_path = os.path.join(FIGURES_DIR, "baseline_confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[+] Đã lưu biểu đồ confusion matrix tại: {cm_path}")
    
    # 8. Lưu mô hình
    os.makedirs(os.path.dirname(BASELINE_MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, BASELINE_MODEL_PATH)
    print(f"[+] Đã lưu mô hình tại: {BASELINE_MODEL_PATH}")
    
    return metrics_data

if __name__ == "__main__":
    train_and_evaluate_baseline()
