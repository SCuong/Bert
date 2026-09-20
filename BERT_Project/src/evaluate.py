"""
evaluate.py - Đánh giá mô hình BERT trên tập kiểm thử độc lập (Test Set) đúng 1 lần.
Mục tiêu:
1. Tính toán các chỉ số học thuật: Accuracy, Precision, Recall, Macro/Weighted F1.
2. Vẽ và lưu Ma trận nhầm lẫn (Confusion Matrix).
3. Xuất bảng so sánh tổng hợp với Baseline và các kết quả lịch sử.
4. Trích xuất các ca dự đoán sai phục vụ Phân Tích Lỗi (Error Analysis).
"""

import os
import sys
import time
import json
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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data import load_and_clean_data, split_data

def evaluate_bert(model_dir=None):
    print("="*65)
    print("ĐÁNH GIÁ MÔ HÌNH FINE-TUNED BERT TRÊN TẬP KIỂM THỬ (TEST SET)")
    print("="*65)
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if model_dir is None:
        model_dir = os.path.join(project_root, "artifacts", "model", "bert_best_model")
        
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"Không tìm thấy mô hình tại: {model_dir}. Hãy chạy train_bert.py trước!")
        
    metrics_dir = os.path.join(project_root, "artifacts", "metrics")
    figures_dir = os.path.join(project_root, "artifacts", "figures")
    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    # 1. Nạp dữ liệu kiểm thử
    df = load_and_clean_data()
    _, _, test_df = split_data(df, random_state=42)
    print(f"[*] Tập Test gồm {len(test_df)} mẫu. Phân bố: {test_df['label'].value_counts().to_dict()}")
    
    # 2. Nạp mô hình & Tokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[*] Thiết bị kiểm thử: {device}")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.to(device)
    model.eval()
    
    # 3. Tiến hành suy luận theo batch
    batch_size = 32
    texts = test_df["text"].tolist()
    true_labels = test_df["label"].tolist()
    
    all_preds = []
    all_probs = []
    
    print("\n[*] Đang thực hiện dự đoán trên Test Set...")
    start_eval = time.time()
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
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
    
    # 4. Tính toán các chỉ số
    acc = accuracy_score(true_labels, all_preds)
    prec_macro = precision_score(true_labels, all_preds, average="macro")
    rec_macro = recall_score(true_labels, all_preds, average="macro")
    f1_macro = f1_score(true_labels, all_preds, average="macro")
    f1_weighted = f1_score(true_labels, all_preds, average="weighted")
    
    prec_per_class = precision_score(true_labels, all_preds, average=None)
    rec_per_class = recall_score(true_labels, all_preds, average=None)
    f1_per_class = f1_score(true_labels, all_preds, average=None)
    
    cm = confusion_matrix(true_labels, all_preds)
    
    print("\n" + "="*50)
    print("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH BERT TRÊN TEST SET:")
    print(f"Accuracy:        {acc*100:.2f}%")
    print(f"Macro Precision: {prec_macro:.4f}")
    print(f"Macro Recall:    {rec_macro:.4f}")
    print(f"Macro F1-Score:  {f1_macro:.4f}")
    print(f"Weighted F1:     {f1_weighted:.4f}")
    print(f"Inference Time:  {eval_time:.2f}s ({len(test_df)/eval_time:.1f} samples/sec)")
    print("\nChi tiết Classification Report:")
    print(classification_report(true_labels, all_preds, target_names=["Negative (0)", "Positive (1)"], digits=4))
    print("="*50)
    
    # 5. Lưu kết quả metrics
    bert_metrics = {
        "model_name": "Fine-Tuned BERT (bert-base-uncased)",
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
    
    metrics_path = os.path.join(metrics_dir, "bert_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(bert_metrics, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu BERT metrics tại: {metrics_path}")
    
    # 6. Vẽ và lưu Confusion Matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Negative (0)", "Positive (1)"],
                yticklabels=["Negative (0)", "Positive (1)"],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title("BERT Confusion Matrix", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.tight_layout()
    cm_path = os.path.join(figures_dir, "bert_confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[+] Đã lưu biểu đồ confusion matrix tại: {cm_path}")
    
    # 7. Trích xuất các ca dự đoán sai phục vụ Phân Tích Lỗi (Error Analysis)
    test_df_eval = test_df.copy()
    test_df_eval["pred"] = all_preds
    test_df_eval["prob_0"] = all_probs[:, 0]
    test_df_eval["prob_1"] = all_probs[:, 1]
    test_df_eval["confidence"] = np.max(all_probs, axis=1)
    
    errors = test_df_eval[test_df_eval["label"] != test_df_eval["pred"]].copy()
    print(f"\n[*] Tổng số ca dự đoán sai: {len(errors)} / {len(test_df)} ({len(errors)/len(test_df)*100:.2f}%)")
    
    # Lấy 10 False Positives (Thực tế là 0 nhưng đoán là 1) và 10 False Negatives (Thực tế là 1 nhưng đoán là 0)
    fps = errors[errors["label"] == 0].sort_values("confidence", ascending=False).head(10)
    fns = errors[errors["label"] == 1].sort_values("confidence", ascending=False).head(10)
    
    selected_errors = pd.concat([fps, fns]).to_dict(orient="records")
    
    error_cases_file = os.path.join(metrics_dir, "error_cases.json")
    with open(error_cases_file, "w", encoding="utf-8") as f:
        json.dump(selected_errors, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã trích xuất 20 ca dự đoán sai đặc trưng tại: {error_cases_file}")
    
    return bert_metrics

if __name__ == "__main__":
    evaluate_bert()
