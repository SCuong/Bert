"""
train_bert.py - Huấn luyện và tinh chỉnh (Fine-tuning) mô hình BERT cho bài toán phân loại cảm xúc.
Mô hình nền tảng: google-bert/bert-base-uncased (110M tham số).
Sử dụng cấu hình tập trung từ src/config.py:
- Đồng bộ Tokenizer và Model uncased.
- Cập nhật trọng số toàn bộ các tầng Encoder (True Fine-Tuning).
- Sử dụng bộ tối ưu AdamW với weight decay và learning rate chuẩn.
- Huấn luyện có kiểm soát, lưu và phục hồi checkpoint tốt nhất.
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

# Đảm bảo repository root luôn có trong sys.path khi chạy trực tiếp hoặc dạng module
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import inspect
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

# Import cấu hình tập trung
from src.config import (
    MODEL_NAME,
    MAX_LENGTH,
    RANDOM_SEED,
    BATCH_SIZE,
    LEARNING_RATE,
    WEIGHT_DECAY,
    NUM_EPOCHS,
    WARMUP_RATIO,
    BERT_BEST_MODEL_DIR,
    BERT_CHECKPOINTS_DIR,
    FIGURES_DIR,
    BERT_TRAINING_HISTORY_PATH
)
from src.data import load_and_validate_data, get_train_val_split

class HotelReviewDataset(Dataset):
    """Dataset PyTorch thuần túy cho bài toán phân loại đánh giá khách sạn"""
    def __init__(self, texts, labels, tokenizer, max_length=MAX_LENGTH):
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

def set_seed(seed=RANDOM_SEED):
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

def train_bert(epochs=NUM_EPOCHS, batch_size=BATCH_SIZE, lr=LEARNING_RATE, max_length=MAX_LENGTH, seed=RANDOM_SEED):
    print("="*65)
    print(f"BẮT ĐẦU FINE-TUNING BERT: {MODEL_NAME}")
    print("="*65)

    set_seed(seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[*] Thiết bị tính toán: {device}")
    if device == "cuda":
        print(f"[*] Tên GPU: {torch.cuda.get_device_name(0)}")
        print(f"[*] Bộ nhớ VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")

    # 1. Nạp dữ liệu (Giai đoạn huấn luyện chỉ sử dụng Train và Validation; Test set chỉ nạp ở evaluate.py)
    df = load_and_validate_data()
    train_df, val_df = get_train_val_split(df, random_state=seed)

    # 2. Tokenizer
    print(f"\n[*] Đang khởi tạo Tokenizer: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print(f"[*] Đang khởi tạo PyTorch Dataset (max_length={max_length})...")
    train_ds = HotelReviewDataset(train_df["text"], train_df["label"], tokenizer, max_length=max_length)
    val_ds = HotelReviewDataset(val_df["text"], val_df["label"], tokenizer, max_length=max_length)

    # 3. Khởi tạo Mô hình
    print(f"[*] Đang tải mô hình tiền huấn luyện: {MODEL_NAME}")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    model.to(device)

    # Thư mục lưu checkpoint và artifacts
    os.makedirs(BERT_CHECKPOINTS_DIR, exist_ok=True)
    os.makedirs(BERT_BEST_MODEL_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(BERT_TRAINING_HISTORY_PATH), exist_ok=True)

    # 4. Cấu hình TrainingArguments
    training_args = TrainingArguments(
        output_dir=BERT_CHECKPOINTS_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=lr,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size * 2,
        num_train_epochs=epochs,
        weight_decay=WEIGHT_DECAY,
        warmup_ratio=WARMUP_RATIO,
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

    # Tương thích với API Hugging Face Transformers mới (processing_class thay cho tokenizer)
    trainer_init_params = inspect.signature(Trainer.__init__).parameters
    trainer_kwargs = {
        "model": model,
        "args": training_args,
        "train_dataset": train_ds,
        "eval_dataset": val_ds,
        "compute_metrics": compute_metrics,
        "callbacks": [history_cb]
    }
    if "processing_class" in trainer_init_params:
        trainer_kwargs["processing_class"] = tokenizer
    else:
        trainer_kwargs["tokenizer"] = tokenizer

    trainer = Trainer(**trainer_kwargs)

    # 5. Huấn luyện
    print("\n[*] Bắt đầu quá trình huấn luyện (Fine-Tuning)...")
    start_time = time.time()
    train_result = trainer.train()
    training_time = time.time() - start_time
    print(f"\n[+] Quá trình huấn luyện hoàn tất sau {training_time:.2f} giây ({training_time/60:.2f} phút).")

    # 6. Lưu best model & tokenizer
    print(f"[*] Đang lưu mô hình tốt nhất về: {BERT_BEST_MODEL_DIR}")
    trainer.save_model(BERT_BEST_MODEL_DIR)
    tokenizer.save_pretrained(BERT_BEST_MODEL_DIR)
    print("[+] Mô hình và Tokenizer đã được lưu thành công.")

    # 7. Trích xuất lịch sử huấn luyện chi tiết từ trainer.state.log_history (bao gồm cả Train Loss và Val Loss)
    train_loss_points = []
    eval_points = []
    for entry in trainer.state.log_history:
        if "loss" in entry and "epoch" in entry:
            train_loss_points.append({
                "epoch": entry["epoch"],
                "step": entry["step"],
                "train_loss": entry["loss"]
            })
        if "eval_loss" in entry and "epoch" in entry:
            eval_points.append({
                "epoch": entry["epoch"],
                "step": entry["step"],
                "eval_loss": entry["eval_loss"],
                "eval_accuracy": entry.get("eval_accuracy", 0.0),
                "eval_macro_f1": entry.get("eval_macro_f1", 0.0)
            })

    history_payload = {
        "model_name": MODEL_NAME,
        "training_time_seconds": training_time,
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": lr,
        "max_length": max_length,
        "train_loss_history": train_loss_points,
        "eval_history": eval_points,
        "callback_history": history_cb.history,
        "train_runtime": train_result.metrics.get("train_runtime", training_time),
        "final_train_loss": train_result.metrics.get("train_loss", 0.0)
    }

    with open(BERT_TRAINING_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history_payload, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu lịch sử huấn luyện tại: {BERT_TRAINING_HISTORY_PATH}")

    # 8. Vẽ đồ thị Train Loss, Validation Loss & Validation Metrics qua các Epoch
    if len(eval_points) > 0:
        val_epochs = [h["epoch"] for h in eval_points]
        val_losses = [h["eval_loss"] for h in eval_points]
        val_accs = [h["eval_accuracy"] for h in eval_points]
        val_f1s = [h["eval_macro_f1"] for h in eval_points]

        plt.figure(figsize=(11, 4.5))

        # Subplot 1: Loss curves (Train Loss + Validation Loss)
        plt.subplot(1, 2, 1)
        if len(train_loss_points) > 0:
            tr_epochs = [h["epoch"] for h in train_loss_points]
            tr_losses = [h["train_loss"] for h in train_loss_points]
            plt.plot(tr_epochs, tr_losses, color="#3498db", alpha=0.6, linewidth=1.5, label="Train Loss (Step)")
        plt.plot(val_epochs, val_losses, marker="o", color="#e74c3c", linewidth=2, label="Validation Loss")
        plt.title("Training & Validation Loss across Epochs", fontsize=12, fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()

        # Subplot 2: Validation Metrics (Accuracy & Macro F1)
        plt.subplot(1, 2, 2)
        plt.plot(val_epochs, val_accs, marker="s", color="#2ecc71", linewidth=2, label="Val Accuracy")
        plt.plot(val_epochs, val_f1s, marker="^", color="#9b59b6", linewidth=2, label="Val Macro F1")
        plt.title("Validation Accuracy & Macro F1 across Epochs", fontsize=12, fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Score")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()

        plt.tight_layout()
        curve_path = os.path.join(FIGURES_DIR, "training_history.png")
        plt.savefig(curve_path, dpi=300)
        plt.close()
        print(f"[+] Đã lưu đồ thị quá trình huấn luyện tại: {curve_path}")

    return BERT_BEST_MODEL_DIR

if __name__ == "__main__":
    train_bert()
