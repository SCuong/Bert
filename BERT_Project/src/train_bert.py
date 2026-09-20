"""
train_bert.py - Huấn luyện và tinh chỉnh (Fine-tuning) mô hình BERT cho bài toán phân loại cảm xúc.
Mô hình nền tảng: google-bert/bert-base-uncased (110M tham số).
Khắc phục triệt để các sai lăm trong tài liệu cũ:
1. Đồng bộ hoàn toàn Tokenizer và Model uncased.
2. Cho phép cập nhật trọng số toàn bộ các tầng Encoder (True Fine-Tuning).
3. Sử dụng bộ tối ưu AdamW, lr=2e-5, weight decay=0.01.
4. Huấn luyện 2-3 epochs, lưu và phục hồi checkpoint có validation F1 tốt nhất.
"""

import os
import sys
import time
import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    TrainerCallback
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Đảm bảo import được src.data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data import load_and_clean_data, split_data

class HotelReviewDataset(Dataset):
    """Dataset PyTorch thuần túy cho bài toán phân loại đánh giá khách sạn"""
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = list(texts)
        self.labels = list(labels)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        item = {key: val.squeeze(0) for key, val in encoding.items()}
        item["labels"] = torch.tensor(label, dtype=torch.long)
        return item

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    acc = accuracy_score(labels, preds)
    prec = precision_score(labels, preds, average="macro", zero_division=0)
    rec = recall_score(labels, preds, average="macro", zero_division=0)
    f1 = f1_score(labels, preds, average="macro", zero_division=0)
    return {
        "accuracy": acc,
        "macro_precision": prec,
        "macro_recall": rec,
        "macro_f1": f1
    }

class LossHistoryCallback(TrainerCallback):
    """Callback để ghi nhận loss và metrics qua từng epoch"""
    def __init__(self):
        self.history = []
        
    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        if metrics:
            self.history.append({
                "epoch": state.epoch,
                "step": state.global_step,
                **metrics
            })

def train_bert(epochs=3, batch_size=16, lr=2e-5, max_length=128, seed=42):
    print("="*65)
    print("BẮT ĐẦU FINE-TUNING BERT: google-bert/bert-base-uncased")
    print("="*65)
    
    set_seed(seed)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[*] Thiết bị tính toán: {device}")
    if device == "cuda":
        print(f"[*] Tên GPU: {torch.cuda.get_device_name(0)}")
        print(f"[*] Bộ nhớ VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
        
    # 1. Nạp dữ liệu
    df = load_and_clean_data()
    train_df, val_df, test_df = split_data(df, random_state=seed)
    
    # 2. Tokenizer
    model_name = "bert-base-uncased"
    print(f"\n[*] Đang khởi tạo Tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print("[*] Đang khởi tạo PyTorch Dataset...")
    train_ds = HotelReviewDataset(train_df["text"], train_df["label"], tokenizer, max_length=max_length)
    val_ds = HotelReviewDataset(val_df["text"], val_df["label"], tokenizer, max_length=max_length)
    test_ds = HotelReviewDataset(test_df["text"], test_df["label"], tokenizer, max_length=max_length)
    
    # 3. Khởi tạo Mô hình
    print(f"[*] Đang tải mô hình tiền huấn luyện: {model_name}")
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.to(device)
    
    # Thư mục lưu checkpoint và artifacts
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    checkpoints_dir = os.path.join(project_root, "artifacts", "model", "bert_checkpoints")
    best_model_dir = os.path.join(project_root, "artifacts", "model", "bert_best_model")
    figures_dir = os.path.join(project_root, "artifacts", "figures")
    metrics_dir = os.path.join(project_root, "artifacts", "metrics")
    
    os.makedirs(checkpoints_dir, exist_ok=True)
    os.makedirs(best_model_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(metrics_dir, exist_ok=True)
    
    # 4. Cấu hình TrainingArguments
    training_args = TrainingArguments(
        output_dir=checkpoints_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=lr,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size * 2,
        num_train_epochs=epochs,
        weight_decay=0.01,
        warmup_ratio=0.1,
        fp16=(device == "cuda"),
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        logging_strategy="steps",
        logging_steps=50,
        save_total_limit=2,
        seed=seed,
        report_to="none"
    )
    
    history_cb = LossHistoryCallback()
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=[history_cb]
    )
    
    # 5. Huấn luyện
    print("\n[*] Bắt đầu quá trình huấn luyện (Fine-Tuning)...")
    start_time = time.time()
    train_result = trainer.train()
    training_time = time.time() - start_time
    print(f"\n[+] Quá trình huấn luyện hoàn tất sau {training_time:.2f} giây ({training_time/60:.2f} phút).")
    
    # 6. Lưu best model & tokenizer
    print(f"[*] Đang lưu mô hình tốt nhất về: {best_model_dir}")
    trainer.save_model(best_model_dir)
    tokenizer.save_pretrained(best_model_dir)
    print("[+] Mô hình và Tokenizer đã được lưu thành công.")
    
    # 7. Lưu lịch sử huấn luyện
    history_file = os.path.join(metrics_dir, "bert_training_history.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump({
            "model_name": model_name,
            "training_time_seconds": training_time,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": lr,
            "max_length": max_length,
            "history": history_cb.history,
            "train_runtime": train_result.metrics.get("train_runtime", training_time),
            "train_loss": train_result.metrics.get("train_loss", 0.0)
        }, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu lịch sử huấn luyện tại: {history_file}")
    
    # 8. Vẽ đồ thị Loss & Accuracy qua các Epoch
    if len(history_cb.history) > 0:
        epochs_logged = [h["epoch"] for h in history_cb.history]
        val_losses = [h.get("eval_loss", 0.0) for h in history_cb.history]
        val_accs = [h.get("eval_accuracy", 0.0) for h in history_cb.history]
        val_f1s = [h.get("eval_macro_f1", 0.0) for h in history_cb.history]
        
        plt.figure(figsize=(10, 4.5))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_logged, val_losses, marker="o", color="#e74c3c", linewidth=2, label="Val Loss")
        plt.title("Validation Loss across Epochs", fontsize=12, fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(epochs_logged, val_accs, marker="s", color="#2ecc71", linewidth=2, label="Val Accuracy")
        plt.plot(epochs_logged, val_f1s, marker="^", color="#3498db", linewidth=2, label="Val Macro F1")
        plt.title("Validation Metrics across Epochs", fontsize=12, fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Score")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        
        plt.tight_layout()
        curve_path = os.path.join(figures_dir, "training_history.png")
        plt.savefig(curve_path, dpi=300)
        plt.close()
        print(f"[+] Đã lưu đồ thị quá trình huấn luyện tại: {curve_path}")

    return best_model_dir

if __name__ == "__main__":
    train_bert()
