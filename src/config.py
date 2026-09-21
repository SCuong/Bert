"""
config.py - Nguồn cấu hình tập trung duy nhất (Single Source of Truth) cho toàn bộ dự án.
Đảm bảo tính nhất quán giữa data preprocessing, baseline, BERT fine-tuning, evaluation và inference.
"""

import os

# =============================================================================
# ĐƯỜNG DẪN DỰ ÁN (PROJECT PATHS)
# =============================================================================
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DEFAULT_DATA_PATH = os.path.join(DATA_DIR, "dts_20k_raw.csv")
FALLBACK_DATA_PATH = os.path.abspath(
    os.path.join(PROJECT_ROOT, "Bài giảng", "AI.Code", "NLP_Demo", "dts_20k_raw.csv")
)

ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "artifacts")
METRICS_DIR = os.path.join(ARTIFACTS_DIR, "metrics")
FIGURES_DIR = os.path.join(ARTIFACTS_DIR, "figures")
MODEL_DIR = os.path.join(ARTIFACTS_DIR, "model")

BASELINE_MODEL_PATH = os.path.join(MODEL_DIR, "baseline_tfidf_lr.joblib")
BERT_BEST_MODEL_DIR = os.path.join(MODEL_DIR, "bert_best_model")
BERT_CHECKPOINTS_DIR = os.path.join(MODEL_DIR, "bert_checkpoints")

# Metrics & Figures paths - Development / Validation
BASELINE_VAL_METRICS_PATH = os.path.join(METRICS_DIR, "baseline_validation_metrics.json")
BASELINE_VAL_CM_PATH = os.path.join(FIGURES_DIR, "baseline_val_confusion_matrix.png")

BERT_VAL_METRICS_PATH = os.path.join(METRICS_DIR, "bert_validation_metrics.json")
BERT_VAL_CM_PATH = os.path.join(FIGURES_DIR, "bert_val_confusion_matrix.png")

# Completion Marker / Manifest (Chỉ ghi khi quá trình huấn luyện và đánh giá validation hoàn tất thành công)
BERT_COMPLETION_MANIFEST_PATH = os.path.join(BERT_BEST_MODEL_DIR, "model_completion_manifest.json")

# Metrics & Figures paths - Final Test Evaluation
BASELINE_TEST_METRICS_PATH = os.path.join(METRICS_DIR, "baseline_test_metrics.json")
BASELINE_TEST_CM_PATH = os.path.join(FIGURES_DIR, "baseline_test_confusion_matrix.png")

BERT_TEST_METRICS_PATH = os.path.join(METRICS_DIR, "bert_test_metrics.json")
BERT_TEST_CM_PATH = os.path.join(FIGURES_DIR, "bert_test_confusion_matrix.png")

COMPARATIVE_METRICS_PATH = os.path.join(METRICS_DIR, "comparative_metrics.json")
ERROR_CASES_PATH = os.path.join(METRICS_DIR, "error_cases.json")
ERROR_ANALYSIS_SUMMARY_PATH = os.path.join(METRICS_DIR, "error_analysis_summary.json")
BERT_TRAINING_HISTORY_PATH = os.path.join(METRICS_DIR, "bert_training_history.json")
TOKEN_STATS_PATH = os.path.join(METRICS_DIR, "token_length_stats.json")
DATA_AUDIT_PATH = os.path.join(METRICS_DIR, "data_audit.json")

def check_bert_model_completeness(model_dir: str = BERT_BEST_MODEL_DIR) -> list[str]:
    """
    Kiểm tra tính hoàn thiện của artifact mô hình BERT:
    1. Thư mục tồn tại
    2. config.json tồn tại
    3. Trọng số mô hình tồn tại (model.safetensors hoặc pytorch_model.bin)
    4. Tokenizer files tồn tại (tokenizer_config.json và vocab.txt/tokenizer.json)
    5. Manifest hoàn thành (model_completion_manifest.json) tồn tại
    Trả về danh sách các lỗi/thiếu sót (rỗng nếu hoàn thiện 100%).
    """
    missing = []
    if not os.path.isdir(model_dir):
        missing.append(f"Directory does not exist: {model_dir}")
        return missing

    # 1. Config
    if not os.path.isfile(os.path.join(model_dir, "config.json")):
        missing.append("config.json is missing")

    # 2. Trọng số mô hình
    has_weights = os.path.isfile(os.path.join(model_dir, "model.safetensors")) or \
                  os.path.isfile(os.path.join(model_dir, "pytorch_model.bin"))
    if not has_weights:
        missing.append("model weights missing (neither model.safetensors nor pytorch_model.bin found)")

    # 3. Tokenizer files
    if not os.path.isfile(os.path.join(model_dir, "tokenizer_config.json")):
        missing.append("tokenizer_config.json is missing")
    has_vocab = os.path.isfile(os.path.join(model_dir, "vocab.txt")) or \
                os.path.isfile(os.path.join(model_dir, "tokenizer.json"))
    if not has_vocab:
        missing.append("tokenizer vocab missing (neither vocab.txt nor tokenizer.json found)")

    # 4. Manifest hoàn thành
    manifest_path = os.path.join(model_dir, "model_completion_manifest.json")
    if not os.path.isfile(manifest_path):
        missing.append("model_completion_manifest.json is missing (training may be incomplete or interrupted)")

    return missing


# Backward compatibility aliases
BASELINE_METRICS_PATH = BASELINE_TEST_METRICS_PATH
BERT_METRICS_PATH = BERT_TEST_METRICS_PATH

# =============================================================================
# THIẾT LẬP MÔ HÌNH & TÁI LẬP (MODEL & REPRODUCIBILITY CONFIG)
# =============================================================================
MODEL_NAME = "google-bert/bert-base-uncased"
RANDOM_SEED = 42

# Tỷ lệ phân chia tập dữ liệu (Stratified)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.10
TEST_RATIO = 0.20

# Độ dài chuỗi tối đa: Đã được xác nhận dựa trên thực nghiệm EDA (Scope: Train + Val).
# Với p95 = 121.0 tokens, ngưỡng 128 bảo toàn trọn vẹn 96.07% mẫu (chỉ cắt cụt 3.93%).
# Nhân đôi sequence length từ 128 lên 256 làm tăng 4 lần kích thước ma trận self-attention
# theo quy luật O(L^2) nhưng chỉ tăng thêm 3.84% độ phủ văn bản.
# Mức tiêu thụ bộ nhớ và thời gian thực thi thực tế sẽ được đo lường trong quá trình huấn luyện.
MAX_LENGTH = 128

# Siêu tham số huấn luyện BERT
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
NUM_EPOCHS = 3
WARMUP_RATIO = 0.1
