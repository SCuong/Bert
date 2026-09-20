# Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Transformers-4.x-yellow.svg)](https://huggingface.co/)
[![Streamlit](https://img.shields.io/badge/Demo-Streamlit-FF4B4B.svg)](https://streamlit.io/)

Đồ án môn học **Trí Tuệ Nhân Tạo (Artificial Intelligence)**  
Triển khai độc lập mới hoàn toàn từ đầu; không tái sử dụng mã nguồn tham khảo (independent implementation from scratch; reference code was not reused), tuân thủ chặt chẽ quy trình chuẩn **AI Project Cycle** (Scope & Plan $\rightarrow$ Data $\rightarrow$ Models $\rightarrow$ Deployment $\rightarrow$ Maintenance $\rightarrow$ Feedback).

> [!IMPORTANT]
> **TRẠNG THÁI HIỆN TẠI:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`  
> Mã nguồn đã được cấu trúc và kiểm tra tính hợp lệ. Các thực nghiệm huấn luyện và đánh giá trên Test Set đang ở trạng thái `NOT YET EXECUTED` và sẽ được thực thi sau khi hoàn tất rà soát mã nguồn.

---

## 1. Giới Thiệu Đề Tài

Bài toán đặt ra: **Tự động phân loại cảm xúc (Sentiment Analysis) của các bài đánh giá khách sạn bằng tiếng Anh thành Tích cực (Positive - 1) hoặc Tiêu cực (Negative - 0)**.

- **Mô hình cốt lõi:** `google-bert/bert-base-uncased` (110M tham số), fine-tuning có kiểm soát bằng PyTorch và Hugging Face Transformers.
- **Mô hình cơ sở (Baseline):** TF-IDF (10,000 unigram + bigram) kết hợp Logistic Regression.
- **Tập dữ liệu:** Teacher-provided hotel-review sentiment dataset (`data/dts_20k_raw.csv`), quy mô ban đầu 20,000 mẫu. Sau kiểm toán dữ liệu và loại bỏ 255 mẫu (rỗng, xung đột nhãn, trùng lặp), tập sạch còn 19,745 mẫu duy nhất (9,921 Negative, 9,824 Positive), chứa các marker đặc thù phong cách Booking.com (như `"No Negative"` trong các bài đánh giá hài lòng).

---

## 2. Bảng So Sánh Kết Quả (Results Table)

> [!NOTE]
> Các chỉ số thực nghiệm của nhóm (TF-IDF + LR và Fine-Tuned BERT) sẽ được ghi nhận trực tiếp sau khi hoàn tất thực thi trên tập kiểm thử độc lập.  
> Các kết quả tham khảo từ notebook cũ (`DL_Model.ipynb`) chỉ công bố chỉ số Accuracy (NNLM: 79.00%, BiLSTM: 75.00%, Old BERT: 65.20%); các chỉ số Precision, Recall, Macro F1 không được tài liệu cũ báo cáo (`Not reported`).

| Mô Hình / Phương Pháp | Vai Trò / Phân Loại | Accuracy | Macro Precision | Macro Recall | Macro F1 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | *Baseline mới của nhóm* | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` |
| **Fine-Tuned BERT (Ours)** | *Mô hình chính mới của nhóm* | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` |

*Tham khảo kết quả lịch sử (`DL_Model.ipynb`):* NNLM: Acc 79.00% | BiLSTM: Acc 75.00% | Old BERT: Acc 65.20% (Chi tiết phân tích lỗi kỹ thuật xem tại [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md)).

---

## 3. Cấu Trúc Thư Mục Dự Án
 
```text
.
├── README.md                      # Tài liệu hướng dẫn toàn diện của dự án
├── requirements.txt              # Danh sách thư viện và phiên bản phụ thuộc
├── FINAL_REPORT.md               # Báo cáo tổng kết 11 mục chuẩn học thuật
├── data/
│   ├── README.md                 # Đặc tả dữ liệu và phân tích đặc trưng văn bản
│   └── dts_20k_raw.csv           # File dữ liệu thô (20,000 mẫu, local only, gitignored)
├── docs/
│   ├── 01_material_audit.md      # Khảo sát & audit toàn bộ tài liệu cũ
│   ├── 02_project_spec.md        # Đặc tả bài toán theo AI Project Cycle
│   ├── 03_old_bert_analysis.md   # Phân tích nguyên nhân thất bại của code BERT cũ (tham khảo)
│   ├── 04_error_analysis.md      # Khung phân tích định tính ca dự đoán sai của BERT
│   ├── STUDY_GUIDE.md            # Cẩm nang giải thích 25 khái niệm cốt lõi (Tiếng Việt)
│   ├── DEFENSE_QA.md             # Bộ 25+ câu hỏi & câu trả lời phản biện trước Hội đồng
│   └── PRE_EXPERIMENT_REVIEW.md  # Báo cáo kiểm tra trước thực nghiệm
├── notebooks/
│   ├── 01_EDA.ipynb              # Notebook phân tích khám phá dữ liệu & trực quan hóa
│   ├── 02_Baseline.ipynb         # Notebook huấn luyện & đánh giá Baseline
│   └── BERT_Training_Colab.ipynb # Notebook huấn luyện BERT trên Google Colab GPU (Run All)
├── src/
│   ├── __init__.py
│   ├── config.py                 # Cấu hình tập trung (Single Source of Truth)
│   ├── data.py                   # Nạp dữ liệu, làm sạch tối thiểu, audit leakage, Stratified split
│   ├── train_baseline.py         # Huấn luyện mô hình cơ sở TF-IDF + Logistic Regression
│   ├── train_bert.py             # Huấn luyện & fine-tuning mô hình BERT chính thức
│   ├── evaluate.py               # Đánh giá độc lập trên Test Set & trích xuất ca lỗi
│   └── predict.py                # Pipeline suy luận và giải thích WordPiece tokens
├── app/
│   └── app.py                    # Ứng dụng Web tương tác bằng Streamlit
├── artifacts/
│   ├── metrics/                  # Kết quả định lượng dạng JSON (baseline, bert, errors, token stats)
│   ├── figures/                  # Biểu đồ trực quan hóa (EDA, Confusion Matrix, History)
│   └── model/                    # Trọng số mô hình đã huấn luyện (loại trừ qua .gitignore)
└── presentation/
    ├── generate_presentation.py  # Script Python tự động sinh slide PowerPoint
    ├── presentation_outline.md   # Dàn ý chi tiết 15 slide
    └── speaker_notes.md          # Kịch bản thuyết trình mẫu 8-10 phút
```

---

## 4. Hướng Dẫn Cài Đặt & Chạy Dự Án (Chạy Dạng Package từ Root)

### 4.1. Thiết lập môi trường
Khuyến nghị sử dụng Python 3.10 hoặc 3.11. Toàn bộ quy trình được kiểm soát tính tái lập (`controlled for reproducibility with fixed seeds and documented environment`).

```bash
# Cài đặt toàn bộ thư viện cần thiết từ thư mục gốc
pip install -r requirements.txt
```

### 4.2. Khám phá & Làm sạch dữ liệu (EDA)
```bash
python -m src.data
```
*Lệnh này thực hiện Data Audit, loại bỏ 255 mẫu không hợp lệ/trùng lặp/xung đột nhãn (còn 19,745 mẫu hợp lệ), phân chia Stratified Split (70/10/20, Zero Data Leakage), đo lường phân vị độ dài token BERT thực tế trên tập Train+Val (Mean: 42.33, Median: 30.0, p95: 121.0, Max: 425, cắt cụt tại 128: 3.93%), xác nhận lựa chọn MAX_LENGTH = 128 và xuất các artifacts `artifacts/metrics/data_audit.json`, `artifacts/metrics/token_length_stats.json`, `artifacts/figures/class_distribution.png`, `artifacts/figures/token_length_distribution.png`.*

### 4.3. Huấn luyện mô hình cơ sở (Baseline)
```bash
python -m src.train_baseline
```
*Huấn luyện mô hình TF-IDF + Logistic Regression trên Train Set, đánh giá phát triển trên Validation Set, lưu kết quả vào `artifacts/metrics/baseline_validation_metrics.json`, vẽ `artifacts/figures/baseline_val_confusion_matrix.png`, và lưu mô hình tại `artifacts/model/baseline_tfidf_lr.joblib`. Tập Test Set được niêm phong hoàn toàn trong giai đoạn này.*

### 4.4. Huấn luyện & Fine-tuning BERT
```bash
python -m src.train_bert
```
*Tự động nhận diện phần cứng (GPU/CPU), fine-tune mô hình `bert-base-uncased`, lưu checkpoint tốt nhất vào `artifacts/model/bert_best_model` và vẽ đường cong học tập (Train Loss + Val Loss) tại `artifacts/figures/training_history.png`.*

### 4.5. Đánh giá trên tập kiểm thử (Comparative Test Evaluation)
```bash
python -m src.evaluate
```
*Đánh giá so sánh đối đầu giữa Baseline và Fine-Tuned BERT trên tập kiểm thử độc lập (Test Set) đúng 1 lần sau khi cả hai mô hình đã hoàn tất huấn luyện. Tự động kích hoạt fail-fast guard nếu thiếu bất kỳ artifact mô hình nào. Lưu `artifacts/metrics/baseline_test_metrics.json`, `artifacts/metrics/bert_test_metrics.json`, `artifacts/metrics/comparative_metrics.json` và trích xuất 20 ca lỗi vào `artifacts/metrics/error_cases.json`.*

### 4.6. Tạo slide PowerPoint thuyết trình
```bash
# Tạo bản nháp kiểm tra định dạng khi chưa chạy thực nghiệm
python -m presentation.generate_presentation --draft

# Tạo bài thuyết trình chính thức sau khi đã có kết quả thực nghiệm thực tế
python -m presentation.generate_presentation
```
*(Trạng thái hiện tại: presentation generator implemented; final deck pending experiment results).*

### 4.7. Khởi chạy ứng dụng Web Demo (Streamlit)
```bash
streamlit run app/app.py
```
*Mở trình duyệt tại `http://localhost:8501` để trải nghiệm giao diện phân tích cảm xúc thời gian thực.*

---

## 5. Môi Trường Phần Cứng & Yêu Cầu Kỹ Thuật

- **Môi trường thực nghiệm:**
  - GPU: NVIDIA GeForce RTX 5050 Laptop GPU (8GB VRAM), CUDA 13.1.
  - CPU: Intel / AMD x86_64, 16GB RAM.
  - OS: Windows 11.
- **Phương án dự phòng đám mây (Cloud Fallback):**
  - Cung cấp sẵn notebook [`notebooks/BERT_Training_Colab.ipynb`](notebooks/BERT_Training_Colab.ipynb) độc lập, sẵn sàng chạy trên Google Colab GPU (T4) với tính năng *"Run All"*.
  - Mức tiêu thụ bộ nhớ VRAM và thời gian thực thi thực tế sẽ được đo lường và ghi nhận trực tiếp trong quá trình huấn luyện thay vì dựa trên các con số ước lượng lý thuyết.
