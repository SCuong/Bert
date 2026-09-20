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

BASELINE_METRICS_PATH = os.path.join(METRICS_DIR, "baseline_metrics.json")
BERT_METRICS_PATH = os.path.join(METRICS_DIR, "bert_metrics.json")
ERROR_CASES_PATH = os.path.join(METRICS_DIR, "error_cases.json")
BERT_TRAINING_HISTORY_PATH = os.path.join(METRICS_DIR, "bert_training_history.json")
TOKEN_STATS_PATH = os.path.join(METRICS_DIR, "token_length_stats.json")

# =============================================================================
# THIẾT LẬP MÔ HÌNH & TÁI LẬP (MODEL & REPRODUCIBILITY CONFIG)
# =============================================================================
MODEL_NAME = "google-bert/bert-base-uncased"
RANDOM_SEED = 42

# Tỷ lệ phân chia tập dữ liệu (Stratified)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.10
TEST_RATIO = 0.20

# Độ dài chuỗi tối đa: Giá trị mặc định / ứng viên ban đầu (Candidate: 128)
# Sẽ được kiểm chứng qua các phân vị (p90, p95, p99) và tỷ lệ cắt cụt từ EDA token-length thực tế
# để quyết định giữ 128 hay chuyển sang 256.
MAX_LENGTH = 128

# Siêu tham số huấn luyện BERT
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
NUM_EPOCHS = 3
WARMUP_RATIO = 0.1
