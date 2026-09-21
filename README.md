# Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Transformers-4.x-yellow.svg)](https://huggingface.co/)
[![Streamlit](https://img.shields.io/badge/Demo-Streamlit-FF4B4B.svg)](https://streamlit.io/)

Đồ án môn học **Trí Tuệ Nhân Tạo (Artificial Intelligence)**  
Triển khai độc lập mới hoàn toàn từ đầu; không tái sử dụng mã nguồn tham khảo (independent implementation from scratch; reference code was not reused), tuân thủ chặt chẽ quy trình chuẩn **AI Project Cycle** (Scope & Plan $\rightarrow$ Data $\rightarrow$ Models $\rightarrow$ Deployment $\rightarrow$ Maintenance $\rightarrow$ Feedback).

> [!NOTE]
> **TRẠNG THÁI HIỆN TẠI:** `FINAL EXPERIMENT COMPLETED`  
> Toàn bộ các thực nghiệm huấn luyện, đánh giá độc lập trên tập kiểm thử (Held-Out Test Set, 3,949 mẫu), và phân tích định tính ca lỗi đã hoàn tất thành công. Mọi kết quả định lượng được trích xuất trực tiếp từ các tệp artifact chính thức tại `artifacts/metrics/`.

---

## 1. Giới Thiệu Đề Tài

Bài toán đặt ra: **Tự động phân loại cảm xúc (Sentiment Analysis) của các bài đánh giá khách sạn bằng tiếng Anh thành Tích cực (Positive - 1) hoặc Tiêu cực (Negative - 0)**.

- **Mô hình cốt lõi:** `google-bert/bert-base-uncased` (110M tham số), fine-tuning toàn diện (Full Fine-Tuning) bằng PyTorch và Hugging Face Transformers.
- **Mô hình cơ sở (Baseline):** TF-IDF (10,000 unigram + bigram) kết hợp Logistic Regression.
- **Tập dữ liệu:** Teacher-provided hotel-review sentiment dataset (`data/dts_20k_raw.csv`), quy mô ban đầu 20,000 mẫu. Sau kiểm toán dữ liệu và loại bỏ 255 mẫu (rỗng, xung đột nhãn, trùng lặp), tập sạch còn **19,745 mẫu duy nhất** (9,921 Negative, 9,824 Positive), phân chia Stratified Split (Seed 42) thành Train (13,821), Validation (1,975), và Test (3,949).

---

## 2. Bảng So Sánh Kết Quả Chính Thức (Official Test Results)

> [!NOTE]
> Kết quả đánh giá đối đầu được thực hiện đồng thời trên cùng tập kiểm thử độc lập (**Held-Out Test Set: 3,949 mẫu**), được niêm phong hoàn toàn trong suốt quá trình phát triển mô hình.  
> Các kết quả tham khảo từ notebook cũ môn học (`DL_Model.ipynb`) chỉ báo cáo Accuracy (NNLM: 79.00%, BiLSTM: 75.00%, Old BERT: 65.20%); các chỉ số Precision, Recall, Macro F1 không được tài liệu cũ công bố (`Not reported`).

| Mô Hình / Phương Pháp | Vai Trò / Nền Tảng | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Thời Gian Suy Luận | Tốc Độ Suy Luận |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | *Mô hình cơ sở mới (Nhóm)* | 81.94% | 0.8208 | 0.8193 | 0.8192 | 0.8192 | **0.137 s** | **28,784 mẫu/s** |
| **Fine-Tuned BERT (`bert-base-uncased`)** | *Mô hình chính mới (Nhóm)* | **84.83%** | **0.8486** | **0.8482** | **0.8483** | **0.8483** | 307.30 s | 12.85 mẫu/s |
| **Mức độ cải thiện ($\Delta$ = BERT - Baseline)** | *Độ chênh lệch thực tế* | **+2.89%** | **+0.0278** | **+0.0289** | **+0.0291** | **+0.0291** | *+307.16 s* | *-28,771 mẫu/s* |

*So sánh với kết quả lịch sử trong tài liệu môn học (`DL_Model.ipynb`):*  
- NNLM (Neural Network Language Model): 79.00% Accuracy  
- BiLSTM: 75.00% Accuracy  
- Old BERT (Triển khai lỗi kỹ thuật): **65.20% Accuracy**  
$\rightarrow$ **Pipeline Fine-Tuning mới của nhóm đạt 84.83% Accuracy**, cải thiện **+19.63 điểm phần trăm** so với code BERT cũ của môn học (xem phân tích tại [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md)).

---

## 3. Cấu Trúc Thư Mục Dự Án
 
```text
.
├── README.md                      # Tài liệu tổng quan của dự án
├── requirements.txt              # Danh sách thư viện phụ thuộc
├── FINAL_REPORT.md               # Báo cáo tổng kết hoàn chỉnh 17 mục chuẩn học thuật
├── data/
│   ├── README.md                 # Đặc tả dữ liệu và phân tích đặc trưng văn bản
│   └── dts_20k_raw.csv           # File dữ liệu thô (20,000 mẫu, local only, gitignored)
├── docs/
│   ├── 01_material_audit.md      # Khảo sát & audit toàn bộ tài liệu cũ
│   ├── 02_project_spec.md        # Đặc tả bài toán theo AI Project Cycle
│   ├── 03_old_bert_analysis.md   # Phân tích nguyên nhân thất bại của code BERT cũ (tham khảo)
│   ├── 04_error_analysis.md      # Báo cáo phân tích định tính 20 ca lỗi cực đoan của BERT
│   ├── STUDY_GUIDE.md            # Cẩm nang giải thích 25 khái niệm cốt lõi (Tiếng Việt)
│   └── DEFENSE_QA.md             # Bộ 25 câu hỏi & câu trả lời phản biện trước Hội đồng
├── notebooks/
│   ├── 01_EDA.ipynb              # Notebook phân tích khám phá dữ liệu & trực quan hóa
│   ├── 02_Baseline.ipynb         # Notebook huấn luyện & đánh giá Baseline
│   └── BERT_Training_Colab.ipynb # Notebook huấn luyện BERT trên Google Colab GPU (Run All)
├── src/
│   ├── __init__.py
│   ├── config.py                 # Cấu hình tập trung (Single Source of Truth)
│   ├── data.py                   # Nạp dữ liệu, làm sạch, audit leakage, Stratified split, EDA
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
    ├── generate_presentation.py  # Script Python tự động sinh slide PowerPoint chuẩn DUT
    ├── presentation_outline.md   # Dàn ý chi tiết 15 slide
    ├── speaker_notes.md          # Kịch bản thuyết trình mẫu 8-10 phút
    └── BERT_Project_Final.pptx   # File trình chiếu PowerPoint hoàn chỉnh
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
*Huấn luyện mô hình TF-IDF + Logistic Regression trên Train Set (13,821 mẫu), đánh giá phát triển trên Validation Set (1,975 mẫu), lưu kết quả vào `artifacts/metrics/baseline_validation_metrics.json`, vẽ `artifacts/figures/baseline_val_confusion_matrix.png`, và lưu mô hình tại `artifacts/model/baseline_tfidf_lr.joblib`.*

### 4.4. Huấn luyện & Fine-tuning BERT
```bash
python -m src.train_bert
```
*Fine-tune mô hình `bert-base-uncased` trong 3 epochs (2,592 steps), tự động lưu checkpoint có Validation Macro F1 cao nhất vào `artifacts/model/bert_best_model/` và vẽ đường cong học tập (Train Loss + Val Loss) tại `artifacts/figures/training_history.png`.*

### 4.5. Đánh giá trên tập kiểm thử (Comparative Test Evaluation)
```bash
python -m src.evaluate
```
*Đánh giá so sánh đối đầu giữa Baseline và Fine-Tuned BERT trên tập kiểm thử độc lập (Test Set: 3,949 mẫu) đúng 1 lần sau khi cả hai mô hình đã hoàn tất huấn luyện. Xuất `artifacts/metrics/baseline_test_metrics.json`, `artifacts/metrics/bert_test_metrics.json`, `artifacts/metrics/comparative_metrics.json`, vẽ ma trận nhầm lẫn Test và trích xuất danh sách ca lỗi vào `artifacts/metrics/error_cases.json`.*

### 4.6. Tạo slide PowerPoint thuyết trình
```bash
python -m presentation.generate_presentation
```
*Tạo tệp trình chiếu PowerPoint chính thức `presentation/BERT_Project_Final.pptx` (15 slide) dựa trên hệ thống thiết kế Đại học Bách Khoa - ĐHĐN (DUT) với các số liệu và biểu đồ thực nghiệm chính thức.*

### 4.7. Khởi chạy ứng dụng Web Demo (Streamlit)
```bash
streamlit run app/app.py
```
*Mở trình duyệt tại `http://localhost:8501` để trải nghiệm giao diện phân tích cảm xúc thời gian thực so sánh đối đầu giữa Baseline và Fine-Tuned BERT.*

---

## 5. Môi Trường Phần Cứng & Yêu Cầu Kỹ Thuật

- **Môi trường thực nghiệm chính thức:**
  - **Phần cứng máy chủ:** GPU NVIDIA GeForce RTX 5050 Laptop GPU (8GB VRAM), CPU Intel Core / AMD x86_64 đa lõi, 16GB RAM, Windows 11.
  - **Môi trường thực thi chính thức:** Môi trường Python nội bộ sử dụng gói PyTorch phiên bản CPU (`2.14.0+cpu`). Toàn bộ quá trình huấn luyện BERT 3 epochs chính thức được thực hiện trên CPU với tổng thời gian là **15,617.19 giây (~4.34 giờ / 260.29 phút)**.
- **Phương án dự phòng đám mây (Cloud Option):**
  - Cung cấp sẵn notebook [`notebooks/BERT_Training_Colab.ipynb`](notebooks/BERT_Training_Colab.ipynb) độc lập, cấu hình sẵn sàng chạy trên Google Colab GPU (T4/A100) với tính năng *"Run All"*, cho phép hoàn tất huấn luyện trong ~15-20 phút khi có GPU.
