# Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Transformers-5.17.0-yellow.svg)](https://huggingface.co/)
[![FastAPI](https://img.shields.io/badge/Demo-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

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
- **Tập dữ liệu:** Teacher-provided hotel-review sentiment dataset (`data/dts_20k_raw.csv`), quy mô ban đầu 20,000 mẫu thô. Trong dữ liệu quan sát thấy các marker định dạng như `'No Negative'`, `'No Positive'` (đây là quan sát hình thức dữ liệu, không phải chứng minh nguồn gốc độc lập). Sau kiểm toán dữ liệu và loại bỏ 255 mẫu (rỗng, xung đột nhãn, trùng lặp), tập sạch còn **19,745 mẫu duy nhất** (9,921 Negative, 9,824 Positive), phân chia Stratified Split (Seed 42) thành Train (13,821), Validation (1,975), và Test (3,949).

---

## 2. Bảng So Sánh Kết Quả Chính Thức (Official Test Results)

> [!NOTE]
> Kết quả đánh giá đối đầu được thực hiện đồng thời trên cùng tập kiểm thử độc lập (**Held-Out Test Set: 3,949 mẫu**), được niêm phong hoàn toàn trong suốt quá trình phát triển mô hình.  

| Mô Hình / Phương Pháp | Vai Trò / Nền Tảng | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Thời Gian Suy Luận | Tốc Độ Suy Luận |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | *Mô hình cơ sở mới (Nhóm)* | 81.94% | 0.8208 | 0.8193 | 0.8192 | 0.8192 | **0.137 s** | **28,784 mẫu/s** |
| **Fine-Tuned BERT (`bert-base-uncased`)** | *Mô hình chính mới (Nhóm)* | **84.83%** | **0.8486** | **0.8482** | **0.8483** | **0.8483** | 307.30 s | 12.85 mẫu/s |
| **Mức độ cải thiện ($\Delta$ = BERT - Baseline)** | *Độ chênh lệch thực tế* | **+2.89 điểm phần trăm** | **+0.0278** | **+0.0289** | **+0.0291** | **+0.0291** | *+307.16 s* | *-28,771 mẫu/s* |

> [!NOTE]
> **CHÚ THÍCH THAM KHẢO LỊCH SỬ (HISTORICAL REFERENCE ONLY):**  
> Kết quả mô hình cũ trong tài liệu môn học (`DL_Model.ipynb`):  
> - NNLM (Neural Network Language Model): 79.00% Accuracy  
> - BiLSTM: 75.00% Accuracy  
> - Old BERT (Triển khai lỗi kỹ thuật): **65.20% Accuracy**  
> Các kết quả này thuộc về các cấu hình, tập dữ liệu thử nghiệm và quy trình khác nhau, **không phải là phép so sánh đối chứng có kiểm soát (controlled comparison)**. Pipeline Fine-Tuning mới của nhóm đạt 84.83% Accuracy, khắc phục các hạn chế kỹ thuật chính của triển khai cũ (xem chi tiết tại [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md)). Mức cải thiện đối chứng có kiểm soát chính thức là so với mô hình Baseline chuẩn mực (+2.89 điểm phần trăm Accuracy, +0.0291 Macro F1).

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
│   ├── main.py                   # FastAPI backend, reuse canonical BERT inference
│   ├── templates/index.html      # Single-page presentation interface
│   └── static/                   # Custom CSS and vanilla JavaScript
├── artifacts/
│   ├── metrics/                  # Kết quả định lượng dạng JSON (baseline, bert, errors, token stats)
│   ├── figures/                  # Biểu đồ trực quan hóa (EDA, Confusion Matrix, History)
│   └── model/                    # Trọng số mô hình đã huấn luyện (loại trừ qua .gitignore)
└── presentation/
    ├── generate_presentation.py  # Script sinh slide theo DUT-style template supplied for this project
    ├── presentation_outline.md   # Dàn ý chi tiết 13 slide
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
*Lệnh này thực hiện Data Audit, loại bỏ 255 mẫu không hợp lệ/trùng lặp/xung đột nhãn (còn 19,745 mẫu hợp lệ), phân chia Stratified Split 70/10/20 và xác nhận không có văn bản trùng khớp chính xác giữa các tập. Phân tích độ dài token trên tập Train+Validation (15,796 mẫu) ghi nhận Mean 42.33, Median 30.0, p95 121.0, Max 425 và tỷ lệ vượt 128 tokens là 3.93%; kết quả được lưu trong `artifacts/metrics/data_audit.json`, `artifacts/metrics/token_length_stats.json` và các biểu đồ liên quan.*

> [!WARNING]
> Kiểm toán hậu nghiệm chỉ đọc với chuẩn hóa Unicode NFC, loại khoảng trắng đầu/cuối và `casefold()` phát hiện một số giao thoa khác biệt chủ yếu ở chữ hoa/thường: Train–Validation 3, Train–Test 10 cặp dòng (9 văn bản chuẩn hóa duy nhất), Validation–Test 2. Trong đó có 14 cặp cùng nhãn và 1 cặp trái nhãn. Kết quả thực nghiệm đóng băng không được tính lại và được báo cáo nguyên trạng. Báo cáo có cấu trúc được lưu tại `artifacts/metrics/case_normalized_overlap_audit.json`.

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
*Tạo tệp trình chiếu `presentation/BERT_Project_Final.pptx` (13 slide) theo DUT-style template supplied for this project, sử dụng các số liệu và biểu đồ thực nghiệm đã đóng băng.*

### 4.7. Khởi chạy ứng dụng Web Demo (FastAPI)
```bash
uvicorn app.main:app --reload
```
*Mở trình duyệt tại `http://127.0.0.1:8000` để trải nghiệm giao diện phân tích cảm xúc bằng Fine-Tuned BERT. Endpoint `POST /api/predict` gọi lại trực tiếp `src.predict.predict_bert`, do đó xác suất hiển thị là đầu ra thực tế của mô hình. Mô hình/tokenizer được cache bởi pipeline suy luận chuẩn và không nạp lại cho mỗi request.*

---

## 5. Môi Trường Phần Cứng & Yêu Cầu Kỹ Thuật

- **Môi trường thực nghiệm chính thức:**
  - **Phần cứng máy chủ:** GPU NVIDIA GeForce RTX 5050 Laptop GPU (8GB VRAM), CPU Intel Core / AMD x86_64 đa lõi, 16GB RAM, Windows 11.
  - **Môi trường thực thi chính thức:** Môi trường Python nội bộ sử dụng gói PyTorch phiên bản CPU (`2.14.0+cpu`). Toàn bộ quá trình huấn luyện BERT 3 epochs chính thức được thực hiện trên CPU với tổng thời gian là **15,617.19 giây (~4.34 giờ / 260.29 phút)**.
- **Phương án dự phòng đám mây (Cloud Option):**
  - Cung cấp sẵn notebook [`notebooks/BERT_Training_Colab.ipynb`](notebooks/BERT_Training_Colab.ipynb) độc lập, cấu hình sẵn sàng chạy trên Google Colab GPU (T4/A100) với tính năng *"Run All"*, cho phép hoàn tất huấn luyện trong ~15-20 phút khi có GPU.

## 6. Nguồn triển khai và bằng chứng chuẩn

- `src/` là triển khai được duy trì và dùng làm pipeline chuẩn của dự án.
- `artifacts/metrics/` chứa bằng chứng thực nghiệm đã đóng băng; số liệu báo cáo chính thức phải được đối chiếu từ các artifact này.
- `notebooks/` lưu nội dung khám phá/lịch sử và không thay thế pipeline chuẩn trong `src/`.
- Dữ liệu thô do giảng viên cung cấp và trọng số mô hình có thể được giữ cục bộ, không đưa vào Git.
