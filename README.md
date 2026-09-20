# Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Transformers-4.x-yellow.svg)](https://huggingface.co/)
[![Streamlit](https://img.shields.io/badge/Demo-Streamlit-FF4B4B.svg)](https://streamlit.io/)

Đồ án môn học **Trí Tuệ Nhân Tạo (Artificial Intelligence)**  
Xây dựng mới hoàn toàn độc lập (Clean-Room Implementation), tuân thủ chặt chẽ quy trình chuẩn **AI Project Cycle** (Scope & Plan $\rightarrow$ Data $\rightarrow$ Models $\rightarrow$ Deployment $\rightarrow$ Maintenance $\rightarrow$ Feedback).

> [!IMPORTANT]
> **TRẠNG THÁI HIỆN TẠI:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`  
> Mã nguồn đã được cấu trúc và kiểm tra tính hợp lệ. Các thực nghiệm huấn luyện và đánh giá trên Test Set đang ở trạng thái `NOT YET EXECUTED` và sẽ được thực thi sau khi hoàn tất rà soát mã nguồn.

---

## 1. Giới Thiệu Đề Tài

Bài toán đặt ra: **Tự động phân loại cảm xúc (Sentiment Analysis) của các bài đánh giá khách sạn bằng tiếng Anh thành Tích cực (Positive - 1) hoặc Tiêu cực (Negative - 0)**.

- **Mô hình cốt lõi:** `google-bert/bert-base-uncased` (110M tham số), fine-tuning có kiểm soát bằng PyTorch và Hugging Face Transformers.
- **Mô hình cơ sở (Baseline):** TF-IDF (10,000 unigram + bigram) kết hợp Logistic Regression.
- **Tập dữ liệu:** 20,000 bài đánh giá khách sạn từ nền tảng Booking.com (`data/dts_20k_raw.csv`), cân bằng 50/50.

---

## 2. Bảng So Sánh Kết Quả (Results Table)

> [!NOTE]
> Các kết quả của NNLM, BiLSTM và Old BERT được trích xuất trực tiếp từ notebook tham khảo `DL_Model.ipynb` và được ghi nhận dưới dạng kết quả lịch sử.  
> Các chỉ số của mô hình mới (TF-IDF + LR và Fine-Tuned BERT) sẽ được cập nhật sau khi hoàn tất thực nghiệm.

| Mô Hình / Phương Pháp | Nguồn / Phân Loại | Accuracy | Macro Precision | Macro Recall | Macro F1 | Thời Gian Train |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **NNLM (Google Embedding)** | *Historical result from supplied notebook* | 79.00% | 0.7900 | 0.7900 | 0.7900 | ~10 epochs |
| **BiLSTM (2-layer)** | *Historical result from supplied notebook* | 75.00% | 0.7500 | 0.7500 | 0.7500 | ~50 epochs |
| **Old "BERT" (Bị lỗi kỹ thuật)** | *Historical result from supplied notebook* | 65.20% | 0.6550 | 0.6520 | 0.6500 | ~100 epochs |
| **TF-IDF + Logistic Regression** | *Baseline mới của nhóm* | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` |
| **Fine-Tuned BERT (Ours)** | *Mô hình chính của nhóm* | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` |

*Chi tiết phân tích lỗi kỹ thuật của mô hình cũ xem tại:* [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md)

---

## 3. Cấu Trúc Thư Mục Dự Án
 
```text
.
├── README.md                      # Tài liệu hướng dẫn toàn diện của dự án
├── requirements.txt              # Danh sách thư viện và phiên bản phụ thuộc
├── FINAL_REPORT.md               # Báo cáo tổng kết 11 mục chuẩn học thuật
├── data/
│   ├── README.md                 # Đặc tả dữ liệu và phân tích nguồn gốc Booking.com
│   └── dts_20k_raw.csv           # File dữ liệu thô (20,000 mẫu, local only)
├── docs/
│   ├── 01_material_audit.md      # Khảo sát & audit toàn bộ tài liệu cũ
│   ├── 02_project_spec.md        # Đặc tả bài toán theo AI Project Cycle
│   ├── 03_old_bert_analysis.md   # Phân tích nguyên nhân thất bại của code BERT cũ
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
│   ├── data.py                   # Nạp dữ liệu, làm sạch tối thiểu, phân chia Stratified
│   ├── train_baseline.py         # Huấn luyện mô hình cơ sở TF-IDF + Logistic Regression
│   ├── train_bert.py             # Huấn luyện & fine-tuning mô hình BERT chính thức
│   ├── evaluate.py               # Đánh giá độc lập trên Test Set & trích xuất ca lỗi
│   └── predict.py                # Pipeline suy luận và giải thích WordPiece tokens
├── app/
│   └── app.py                    # Ứng dụng Web tương tác bằng Streamlit
├── artifacts/
│   ├── metrics/                  # Kết quả định lượng dạng JSON (baseline, bert, errors)
│   ├── figures/                  # Biểu đồ trực quan hóa (EDA, Confusion Matrix, History)
│   └── model/                    # Trọng số mô hình đã huấn luyện (loại trừ qua .gitignore)
└── presentation/
    ├── BERT_Project.pptx         # File slide PowerPoint học thuật 15 trang
    ├── generate_presentation.py  # Script Python tự động sinh slide
    ├── presentation_outline.md   # Dàn ý chi tiết 15 slide
    └── speaker_notes.md          # Kịch bản thuyết trình mẫu 8-10 phút
```

---

## 4. Hướng Dẫn Cài Đặt & Chạy Dự Án

### 4.1. Thiết lập môi trường
Khuyến nghị sử dụng Python 3.10 hoặc 3.11.

```bash
# Cài đặt toàn bộ thư viện cần thiết từ thư mục gốc
pip install -r requirements.txt
```

### 4.2. Khám phá & Làm sạch dữ liệu (EDA)
```bash
python src/data.py
```
*Lệnh này sẽ tự động nạp dữ liệu, kiểm tra tính toàn vẹn, thực hiện Stratified Split và xuất biểu đồ `class_distribution.png` cùng `length_distribution.png` vào thư mục `artifacts/figures/`.*

### 4.3. Huấn luyện mô hình cơ sở (Baseline)
```bash
python src/train_baseline.py
```
*Huấn luyện mô hình TF-IDF + Logistic Regression, lưu kết quả vào `artifacts/metrics/baseline_metrics.json` và vẽ `artifacts/figures/baseline_confusion_matrix.png`.*

### 4.4. Huấn luyện & Fine-tuning BERT
```bash
python src/train_bert.py
```
*Tự động nhận diện phần cứng, fine-tune mô hình `bert-base-uncased`, lưu checkpoint tốt nhất vào `artifacts/model/bert_best_model` và vẽ đường cong học tập `artifacts/figures/training_history.png`.*

### 4.5. Đánh giá trên tập kiểm thử (Test Evaluation)
```bash
python src/evaluate.py
```
*Nạp mô hình tốt nhất, đánh giá duy nhất 1 lần trên 3,999 mẫu Test Set, lưu `artifacts/metrics/bert_metrics.json` và trích xuất 20 ca lỗi vào `artifacts/metrics/error_cases.json`.*

### 4.6. Tạo slide PowerPoint thuyết trình
```bash
python presentation/generate_presentation.py
```
*Sinh file PowerPoint học thuật hoàn chỉnh `presentation/BERT_Project.pptx`.*

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
  - Cung cấp sẵn notebook [`notebooks/BERT_Training_Colab.ipynb`](notebooks/BERT_Training_Colab.ipynb) độc lập, sẵn sàng chạy mượt mà trên Google Colab GPU T4 miễn phí với tính năng *"Run All"*.
