"""
evaluate.py - Đánh giá so sánh đối đầu (Comparative Evaluation) giữa Baseline và BERT trên tập kiểm thử (Test Set).
Nguyên tắc bảo vệ tính toàn vẹn của Test Set:
1. Fail-fast guard: Bắt buộc cả mô hình Baseline (baseline_tfidf_lr.joblib) và mô hình BERT (bert_best_model/)
   đều phải tồn tại trước khi tiến hành đánh giá Test Set.
2. Cả hai mô hình được đánh giá trên cùng một tập Test Set độc lập (3,949 mẫu) trong cùng một lượt chạy.
3. Tách biệt rõ ràng artifacts:
   - artifacts/metrics/baseline_test_metrics.json & artifacts/figures/baseline_test_confusion_matrix.png
   - artifacts/metrics/bert_test_metrics.json & artifacts/figures/bert_test_confusion_matrix.png
   - artifacts/metrics/comparative_metrics.json (Bảng so sánh đối đầu tổng hợp)
   - artifacts/metrics/error_cases.json (20 ca lỗi đặc trưng của BERT)
"""

import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
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
    MAX_LENGTH,
    RANDOM_SEED,
    BASELINE_MODEL_PATH,
    BERT_BEST_MODEL_DIR,
    BASELINE_TEST_METRICS_PATH,
    BASELINE_TEST_CM_PATH,
    BERT_TEST_METRICS_PATH,
    BERT_TEST_CM_PATH,
    COMPARATIVE_METRICS_PATH,
    ERROR_CASES_PATH,
    FIGURES_DIR
)
from src.data import load_and_validate_data, split_data

def check_model_artifacts():
    """
    Fail-fast guard: Kiểm tra sự tồn tại của cả hai mô hình trước khi cho phép nạp Test Set.
    """
    missing = []
    if not os.path.exists(BASELINE_MODEL_PATH):
        missing.append(f"Baseline model not found at: {BASELINE_MODEL_PATH}")
    if not os.path.exists(BERT_BEST_MODEL_DIR):
        missing.append(f"BERT best model directory not found at: {BERT_BEST_MODEL_DIR}")

    if missing:
        raise RuntimeError(
            "FAIL-FAST GUARD: Không thể thực thi đánh giá trên Test Set vì thiếu artifact mô hình:\n"
            + "\n".join(f"  - {m}" for m in missing)
            + "\n\nYêu cầu: Hãy hoàn thành 'python -m src.train_baseline' và 'python -m src.train_bert' "
            "trước khi thực hiện đánh giá tập kiểm thử cuối cùng."
        )

def evaluate_baseline_on_test(test_df: pd.DataFrame):
    """
    Đánh giá mô hình Baseline (TF-IDF + Logistic Regression) trên tập Test Set độc lập.
    """
    print("\n" + "-"*60)
    print("1. ĐÁNH GIÁ BASELINE (TF-IDF + LOGISTIC REGRESSION) TRÊN TEST SET")
    print("-" * 60)

    print(f"[*] Nạp mô hình baseline từ: {BASELINE_MODEL_PATH}")
    pipeline = joblib.load(BASELINE_MODEL_PATH)

    eval_start = time.time()
    preds = pipeline.predict(test_df["text"])
    eval_time = time.time() - eval_start

    true_labels = test_df["label"].values
    acc = accuracy_score(true_labels, preds)
    prec_macro = precision_score(true_labels, preds, average="macro")
    rec_macro = recall_score(true_labels, preds, average="macro")
    f1_macro = f1_score(true_labels, preds, average="macro")
    f1_weighted = f1_score(true_labels, preds, average="weighted")

    prec_per_class = precision_score(true_labels, preds, average=None)
    rec_per_class = recall_score(true_labels, preds, average=None)
    f1_per_class = f1_score(true_labels, preds, average=None)
    cm = confusion_matrix(true_labels, preds)

    print(f"Baseline Test Accuracy:        {acc*100:.2f}%")
    print(f"Baseline Test Macro Precision: {prec_macro:.4f}")
    print(f"Baseline Test Macro Recall:    {rec_macro:.4f}")
    print(f"Baseline Test Macro F1:        {f1_macro:.4f}")
    print(f"Baseline Test Weighted F1:     {f1_weighted:.4f}")
    print(f"Baseline Inference Time:       {eval_time:.3f}s ({len(test_df)/eval_time:.1f} samples/s)")

    # Lưu metrics
    os.makedirs(os.path.dirname(BASELINE_TEST_METRICS_PATH), exist_ok=True)
    baseline_metrics = {
        "model_name": "TF-IDF + Logistic Regression",
        "evaluation_split": "test",
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
        "inference_time_seconds": float(eval_time),
        "test_sample_count": len(test_df),
        "confusion_matrix": cm.tolist()
    }
    with open(BASELINE_TEST_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(baseline_metrics, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu baseline test metrics tại: {BASELINE_TEST_METRICS_PATH}")

    # Lưu confusion matrix
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Negative (0)", "Positive (1)"],
                yticklabels=["Negative (0)", "Positive (1)"],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title("Baseline Test Confusion Matrix (TF-IDF + LogReg)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.tight_layout()
    plt.savefig(BASELINE_TEST_CM_PATH, dpi=300)
    plt.close()
    print(f"[+] Đã lưu baseline test confusion matrix tại: {BASELINE_TEST_CM_PATH}")

    return baseline_metrics

def evaluate_bert_on_test(test_df: pd.DataFrame):
    """
    Đánh giá mô hình Fine-Tuned BERT trên cùng tập Test Set độc lập.
    """
    print("\n" + "-"*60)
    print("2. ĐÁNH GIÁ FINE-TUNED BERT TRÊN TEST SET")
    print("-" * 60)

    print(f"[*] Nạp mô hình BERT từ: {BERT_BEST_MODEL_DIR}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[*] Thiết bị kiểm thử: {device}")

    tokenizer = AutoTokenizer.from_pretrained(BERT_BEST_MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(BERT_BEST_MODEL_DIR)
    model.to(device)
    model.eval()

    batch_size = 32
    texts = test_df["text"].tolist()
    true_labels = test_df["label"].tolist()

    all_preds = []
    all_probs = []

    print("[*] Đang thực hiện suy luận theo batch...")
    start_eval = time.time()

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()
            preds = np.argmax(probs, axis=1)

        all_probs.extend(probs)
        all_preds.extend(preds)

    eval_time = time.time() - start_eval
    all_probs = np.array(all_probs)
    all_preds = np.array(all_preds)

    acc = accuracy_score(true_labels, all_preds)
    prec_macro = precision_score(true_labels, all_preds, average="macro")
    rec_macro = recall_score(true_labels, all_preds, average="macro")
    f1_macro = f1_score(true_labels, all_preds, average="macro")
    f1_weighted = f1_score(true_labels, all_preds, average="weighted")

    prec_per_class = precision_score(true_labels, all_preds, average=None)
    rec_per_class = recall_score(true_labels, all_preds, average=None)
    f1_per_class = f1_score(true_labels, all_preds, average=None)
    cm = confusion_matrix(true_labels, all_preds)

    print(f"BERT Test Accuracy:        {acc*100:.2f}%")
    print(f"BERT Test Macro Precision: {prec_macro:.4f}")
    print(f"BERT Test Macro Recall:    {rec_macro:.4f}")
    print(f"BERT Test Macro F1:        {f1_macro:.4f}")
    print(f"BERT Test Weighted F1:     {f1_weighted:.4f}")
    print(f"BERT Inference Time:       {eval_time:.2f}s ({len(test_df)/eval_time:.1f} samples/s)")

    # Lưu metrics
    os.makedirs(os.path.dirname(BERT_TEST_METRICS_PATH), exist_ok=True)
    bert_metrics = {
        "model_name": "Fine-Tuned BERT",
        "evaluation_split": "test",
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
        "inference_time_seconds": float(eval_time),
        "test_sample_count": len(test_df),
        "confusion_matrix": cm.tolist()
    }
    with open(BERT_TEST_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(bert_metrics, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu BERT test metrics tại: {BERT_TEST_METRICS_PATH}")

    # Lưu confusion matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Negative (0)", "Positive (1)"],
                yticklabels=["Negative (0)", "Positive (1)"],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title("BERT Test Confusion Matrix", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.tight_layout()
    plt.savefig(BERT_TEST_CM_PATH, dpi=300)
    plt.close()
    print(f"[+] Đã lưu BERT test confusion matrix tại: {BERT_TEST_CM_PATH}")

    # Trích xuất 20 ca lỗi
    test_df_eval = test_df.copy()
    test_df_eval["pred"] = all_preds
    test_df_eval["prob_0"] = all_probs[:, 0]
    test_df_eval["prob_1"] = all_probs[:, 1]
    test_df_eval["confidence"] = np.max(all_probs, axis=1)

    errors = test_df_eval[test_df_eval["label"] != test_df_eval["pred"]].copy()
    fps = errors[errors["label"] == 0].sort_values("confidence", ascending=False).head(10)
    fns = errors[errors["label"] == 1].sort_values("confidence", ascending=False).head(10)
    selected_errors = pd.concat([fps, fns]).to_dict(orient="records")

    with open(ERROR_CASES_PATH, "w", encoding="utf-8") as f:
        json.dump(selected_errors, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã trích xuất 20 ca lỗi đặc trưng tại: {ERROR_CASES_PATH}")

    return bert_metrics

def compare_and_report(baseline_metrics: dict, bert_metrics: dict, test_sample_count: int):
    """
    Tổng hợp và lưu bảng so sánh đối đầu giữa Baseline và BERT.
    """
    print("\n" + "="*65)
    print("BẢNG SO SÁNH ĐỐI ĐẦU CHÍNH THỨC TRÊN TEST SET (HELD-OUT EVALUATION)")
    print("="*65)

    comp_payload = {
        "evaluation_split": "test",
        "test_sample_count": test_sample_count,
        "baseline": {
            "model_name": baseline_metrics["model_name"],
            "accuracy": baseline_metrics["accuracy"],
            "macro_precision": baseline_metrics["macro_precision"],
            "macro_recall": baseline_metrics["macro_recall"],
            "macro_f1": baseline_metrics["macro_f1"],
            "weighted_f1": baseline_metrics["weighted_f1"],
            "inference_time_seconds": baseline_metrics["inference_time_seconds"]
        },
        "bert": {
            "model_name": bert_metrics["model_name"],
            "accuracy": bert_metrics["accuracy"],
            "macro_precision": bert_metrics["macro_precision"],
            "macro_recall": bert_metrics["macro_recall"],
            "macro_f1": bert_metrics["macro_f1"],
            "weighted_f1": bert_metrics["weighted_f1"],
            "inference_time_seconds": bert_metrics["inference_time_seconds"]
        },
        "delta_bert_vs_baseline": {
            "accuracy": round(bert_metrics["accuracy"] - baseline_metrics["accuracy"], 4),
            "macro_f1": round(bert_metrics["macro_f1"] - baseline_metrics["macro_f1"], 4)
        }
    }

    with open(COMPARATIVE_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(comp_payload, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu comparative metrics tại: {COMPARATIVE_METRICS_PATH}")

    print(f"{'Chỉ số (Metric)':<22} | {'Baseline (TF-IDF + LR)':<22} | {'Fine-Tuned BERT':<20} | {'Chênh lệch (Delta)':<15}")
    print("-" * 88)
    print(f"{'Accuracy':<22} | {baseline_metrics['accuracy']*100:>20.2f}% | {bert_metrics['accuracy']*100:>18.2f}% | {comp_payload['delta_bert_vs_baseline']['accuracy']*100:>+13.2f}%")
    print(f"{'Macro Precision':<22} | {baseline_metrics['macro_precision']:>21.4f} | {bert_metrics['macro_precision']:>19.4f} | {bert_metrics['macro_precision'] - baseline_metrics['macro_precision']:>+14.4f}")
    print(f"{'Macro Recall':<22} | {baseline_metrics['macro_recall']:>21.4f} | {bert_metrics['macro_recall']:>19.4f} | {bert_metrics['macro_recall'] - baseline_metrics['macro_recall']:>+14.4f}")
    print(f"{'Macro F1-Score':<22} | {baseline_metrics['macro_f1']:>21.4f} | {bert_metrics['macro_f1']:>19.4f} | {comp_payload['delta_bert_vs_baseline']['macro_f1']:>+14.4f}")
    print(f"{'Weighted F1-Score':<22} | {baseline_metrics['weighted_f1']:>21.4f} | {bert_metrics['weighted_f1']:>19.4f} | {bert_metrics['weighted_f1'] - baseline_metrics['weighted_f1']:>+14.4f}")
    print(f"{'Inference Time':<22} | {baseline_metrics['inference_time_seconds']:>20.3f}s | {bert_metrics['inference_time_seconds']:>18.3f}s | {'-':>14}")
    print("="*65 + "\n")

    return comp_payload

def run_evaluation():
    print("="*65)
    print("KHỞI CHẠY ĐÁNH GIÁ SO SÁNH ĐỐI ĐẦU TRÊN TẬP KIỂM THỬ (TEST SET)")
    print("="*65)

    # 1. Fail-fast guard: Kiểm tra sự tồn tại của cả hai mô hình
    check_model_artifacts()

    # 2. Nạp dữ liệu và tách Test Set độc lập
    df = load_and_validate_data()
    _, _, test_df = split_data(df, random_state=RANDOM_SEED, verbose_test=True)
    print(f"[*] Tập Test gồm {len(test_df)} mẫu. Phân bố nhãn: {test_df['label'].value_counts().to_dict()}")

    # 3. Đánh giá Baseline trên Test Set
    baseline_metrics = evaluate_baseline_on_test(test_df)

    # 4. Đánh giá BERT trên Test Set
    bert_metrics = evaluate_bert_on_test(test_df)

    # 5. So sánh đối đầu và báo cáo
    compare_and_report(baseline_metrics, bert_metrics, len(test_df))

if __name__ == "__main__":
    run_evaluation()
