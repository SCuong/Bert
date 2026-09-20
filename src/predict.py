"""
predict.py - Pipeline suy luận (Inference) cho bài toán phân loại cảm xúc đánh giá khách sạn.
Hỗ trợ:
1. Dự đoán bằng mô hình Baseline (TF-IDF + Logistic Regression).
2. Dự đoán bằng mô hình Fine-tuned BERT (kèm độ tin cậy và chi tiết bẻ từ WordPiece).
Sử dụng cấu hình tập trung từ src/config.py.
"""

import os
import sys
import joblib
import numpy as np

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
    MODEL_NAME,
    MAX_LENGTH,
    BASELINE_MODEL_PATH,
    BERT_BEST_MODEL_DIR
)

# Biến toàn cục cache mô hình để suy luận nhanh
_BASELINE_PIPELINE = None
_BERT_TOKENIZER = None
_BERT_MODEL = None
_TORCH_DEVICE = None

def load_baseline():
    global _BASELINE_PIPELINE
    if _BASELINE_PIPELINE is None:
        if not os.path.exists(BASELINE_MODEL_PATH):
            raise FileNotFoundError(f"Không tìm thấy mô hình baseline tại: {BASELINE_MODEL_PATH}. Hãy chạy train_baseline.py trước!")
        _BASELINE_PIPELINE = joblib.load(BASELINE_MODEL_PATH)
    return _BASELINE_PIPELINE

def predict_baseline(text: str):
    """
    Dự đoán cảm xúc bằng mô hình TF-IDF + Logistic Regression.
    """
    pipeline = load_baseline()
    prob = pipeline.predict_proba([text])[0]
    pred_idx = int(np.argmax(prob))
    label_name = "Positive" if pred_idx == 1 else "Negative"
    confidence = float(prob[pred_idx])

    return {
        "model": "TF-IDF + Logistic Regression",
        "label": label_name,
        "label_id": pred_idx,
        "confidence": confidence,
        "prob_negative": float(prob[0]),
        "prob_positive": float(prob[1])
    }

def load_bert(model_path=None):
    global _BERT_TOKENIZER, _BERT_MODEL, _TORCH_DEVICE
    if _BERT_MODEL is None:
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
        except ImportError:
            raise ImportError("Chưa cài đặt thư viện 'torch' hoặc 'transformers'.")

        if model_path is None:
            model_path = BERT_BEST_MODEL_DIR

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Chưa có trọng số mô hình BERT tại: {model_path}. Hãy chạy train_bert.py trước!")

        _TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        _BERT_TOKENIZER = AutoTokenizer.from_pretrained(model_path)
        _BERT_MODEL = AutoModelForSequenceClassification.from_pretrained(model_path)
        _BERT_MODEL.to(_TORCH_DEVICE)
        _BERT_MODEL.eval()

    return _BERT_TOKENIZER, _BERT_MODEL, _TORCH_DEVICE

def predict_bert(text: str, model_path=None):
    """
    Dự đoán cảm xúc bằng mô hình BERT đã fine-tune.
    Trả về nhãn, độ tin cậy, phân bố xác suất và danh sách các tokens WordPiece.
    """
    import torch
    tokenizer, model, device = load_bert(model_path)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_LENGTH)
    token_strings = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    pred_idx = int(np.argmax(probs))
    label_name = "Positive" if pred_idx == 1 else "Negative"
    confidence = float(probs[pred_idx])

    return {
        "model": f"BERT ({MODEL_NAME})",
        "label": label_name,
        "label_id": pred_idx,
        "confidence": confidence,
        "prob_negative": float(probs[0]),
        "prob_positive": float(probs[1]),
        "tokens": token_strings
    }

if __name__ == "__main__":
    sample_text = "The room was a bit small, but the staff was exceptionally helpful and the breakfast was delicious!"
    print(f"[*] Input text: '{sample_text}'\n")

    # Thử nghiệm Baseline
    try:
        res_base = predict_baseline(sample_text)
        print("[+] Kết quả Baseline:")
        print(f"    - Label: {res_base['label']} ({res_base['confidence']*100:.2f}%)")
        print(f"    - Probabilities: [Neg: {res_base['prob_negative']:.4f}, Pos: {res_base['prob_positive']:.4f}]")
    except Exception as e:
        print(f"[-] Lỗi Baseline: {e}")

    # Thử nghiệm BERT
    try:
        res_bert = predict_bert(sample_text)
        print("\n[+] Kết quả BERT:")
        print(f"    - Label: {res_bert['label']} ({res_bert['confidence']*100:.2f}%)")
        print(f"    - Probabilities: [Neg: {res_bert['prob_negative']:.4f}, Pos: {res_bert['prob_positive']:.4f}]")
        print(f"    - WordPiece Tokens: {res_bert['tokens'][:15]}...")
    except Exception as e:
        print(f"[-] Lỗi BERT (có thể chưa hoàn tất huấn luyện): {e}")
