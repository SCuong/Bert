# Báo Cáo Rà Soát Trước Thực Nghiệm (Pre-Experiment Review)

**Dự án:** Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn (Fine-Tuning BERT for Hotel Review Sentiment Classification)  
**Trạng thái checkpoint:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`  
**Ngày thực hiện:** 20/09/2026  
**Nguyên tắc:** Clean-Room Implementation độc lập 100%, chưa chạy huấn luyện mô hình, toàn bộ chỉ số thực nghiệm mới đang ở trạng thái `PLACEHOLDER`.

---

## 1. Cây Thư Mục Dự Án (Project Tree)

```text
.
├── .gitignore
├── README.md                          # Hướng dẫn tổng quan dự án
├── requirements.txt                  # Danh sách thư viện và phiên bản
├── FINAL_REPORT.md                   # Báo cáo tổng kết 11 mục chuẩn học thuật
├── data/
│   ├── README.md                     # Đặc tả tập dữ liệu và nguồn gốc Booking.com
│   └── dts_20k_raw.csv               # Dữ liệu gốc (20,000 mẫu, local only, gitignored)
├── docs/
│   ├── 01_material_audit.md          # Khảo sát & audit toàn bộ tài liệu cũ
│   ├── 02_project_spec.md            # Đặc tả bài toán theo AI Project Cycle
│   ├── 03_old_bert_analysis.md       # Phân tích nguyên nhân thất bại của code BERT cũ
│   ├── 04_error_analysis.md          # Khung phân tích định tính ca dự đoán sai (Placeholder)
│   ├── STUDY_GUIDE.md                # Cẩm nang giải thích 25 khái niệm cốt lõi (Tiếng Việt)
│   ├── DEFENSE_QA.md                 # Bộ 25 câu hỏi & câu trả lời phản biện trước Hội đồng
│   └── PRE_EXPERIMENT_REVIEW.md      # Tài liệu rà soát hiện tại
├── notebooks/
│   ├── 01_EDA.ipynb                  # Notebook phân tích khám phá dữ liệu & trực quan hóa
│   ├── 02_Baseline.ipynb             # Notebook huấn luyện & đánh giá Baseline
│   └── BERT_Training_Colab.ipynb     # Notebook huấn luyện BERT trên Google Colab GPU (Run All)
├── src/
│   ├── __init__.py
│   ├── config.py                     # Cấu hình tập trung (Single Source of Truth)
│   ├── data.py                       # Nạp dữ liệu, làm sạch tối thiểu, phân chia Stratified
│   ├── train_baseline.py             # Huấn luyện mô hình cơ sở TF-IDF + Logistic Regression
│   ├── train_bert.py                 # Huấn luyện & fine-tuning mô hình BERT chính thức
│   ├── evaluate.py                   # Đánh giá độc lập trên Test Set & trích xuất ca lỗi
│   └── predict.py                    # Pipeline suy luận và giải thích WordPiece tokens
├── app/
│   └── app.py                        # Ứng dụng Web tương tác bằng Streamlit
├── artifacts/
│   ├── metrics/                      # Thư mục lưu kết quả JSON (sẽ tạo sau khi chạy)
│   ├── figures/                      # Thư mục lưu biểu đồ PNG (sẽ tạo sau khi chạy)
│   └── model/
│       └── README.md                 # Hướng dẫn thư mục artifacts/model
└── presentation/
    ├── generate_presentation.py      # Script Python tự động sinh slide PowerPoint
    ├── presentation_outline.md       # Dàn ý chi tiết 15 slide
    └── speaker_notes.md              # Kịch bản thuyết trình mẫu 8-10 phút
```

---

## 2. Danh Sách Tệp Đã Triển Khai (Implemented Files)

| Đường Dẫn Tệp | Mục Đích & Vai Trò | Trạng Thái Cú Pháp |
| :--- | :--- | :---: |
| `requirements.txt` | Khai báo các thư viện phụ thuộc (`torch`, `transformers`, `scikit-learn`...) | Đã xác thực |
| `src/config.py` | Cấu hình tập trung (Single Source of Truth) cho toàn bộ pipeline | Đã biên dịch (Pass) |
| `src/data.py` | Nạp dữ liệu, audit leakage, Stratified split (70/10/20, seed=42) | Đã biên dịch (Pass) |
| `src/train_baseline.py` | Pipeline TF-IDF (10k n-grams) + Logistic Regression (L-BFGS) | Đã biên dịch (Pass) |
| `src/train_bert.py` | Fine-tuning `bert-base-uncased` với PyTorch Dataset thuần, AdamW, lr=2e-5 | Đã biên dịch (Pass) |
| `src/evaluate.py` | Đánh giá trên Test Set, lưu confusion matrix, trích xuất ca lỗi | Đã biên dịch (Pass) |
| `src/predict.py` | Pipeline suy luận Baseline & BERT, giải thích token WordPiece | Đã biên dịch (Pass) |
| `app/app.py` | Giao diện Web tương tác Streamlit với các kịch bản thử nghiệm | Đã biên dịch (Pass) |
| `presentation/generate_presentation.py` | Sinh slide PowerPoint 15 trang bằng `python-pptx` | Đã biên dịch (Pass) |
| `notebooks/01_EDA.ipynb` | Notebook khám phá dữ liệu | JSON hợp lệ (Pass) |
| `notebooks/02_Baseline.ipynb` | Notebook huấn luyện & đánh giá Baseline | JSON hợp lệ (Pass) |
| `notebooks/BERT_Training_Colab.ipynb` | Notebook huấn luyện BERT trên Colab (Run All) | JSON hợp lệ (Pass) |
| `docs/*.md` | Bộ tài liệu học thuật hoàn chỉnh (Audit, Spec, Old BERT, QA, Study Guide) | Hoàn thành |

---

## 3. Các Tệp & Khâu Chưa Được Runtime Verified

1. **`artifacts/metrics/baseline_metrics.json`**: Chưa được sinh (do chưa chạy `train_baseline.py`).
2. **`artifacts/metrics/bert_metrics.json`**: Chưa được sinh (do chưa chạy `evaluate.py`).
3. **`artifacts/metrics/error_cases.json`**: Chưa được sinh (do chưa chạy trích xuất lỗi).
4. **`artifacts/figures/*.png`**: Các biểu đồ (`class_distribution.png`, `baseline_confusion_matrix.png`, `bert_confusion_matrix.png`, `training_history.png`) chưa được xuất ra đĩa.
5. **`artifacts/model/bert_best_model/`**: Trọng số mô hình BERT chưa được lưu.

---

## 4. Các Thực Nghiệm Chưa Chạy (Unexecuted Experiments)

1. **Baseline Training & Evaluation:**
   - Lệnh: `python src/train_baseline.py`
   - Mục tiêu: Thiết lập mốc Accuracy, F1 và Confusion Matrix thực tế cho TF-IDF + Logistic Regression trên 4,000 mẫu Test.
2. **BERT Fine-Tuning:**
   - Lệnh: `python src/train_bert.py`
   - Mục tiêu: Huấn luyện `bert-base-uncased` trong 2-3 epochs trên GPU/CPU, ghi nhận đường cong học tập thực tế.
3. **BERT Test Set Evaluation & Error Extraction:**
   - Lệnh: `python src/evaluate.py`
   - Mục tiêu: Đánh giá duy nhất 1 lần trên Test Set và trích xuất 20 ca lỗi thực tế (False Positives và False Negatives).
4. **PowerPoint Deck Generation:**
   - Lệnh: `python presentation/generate_presentation.py`
   - Mục tiêu: Nhúng các biểu đồ và số liệu thực nghiệm thực tế vào file `presentation/BERT_Project.pptx`.

---

## 5. Các Vấn Đề Kỹ Thuật Đã Nhận Diện & Đã Xử Lý (Known Issues & Fixes)

1. **Vấn đề mã hóa UTF-8 trên Windows Console (cp1252):**
   - *Hiện tượng:* Khi in tiếng Việt ra console Windows, Python gặp lỗi `UnicodeEncodeError: 'charmap' codec can't encode character`.
   - *Xử lý:* Đã bổ sung `sys.stdout.reconfigure(encoding='utf-8')` và `sys.stderr.reconfigure(encoding='utf-8')` vào đầu tất cả các file mã nguồn.
2. **Loại bỏ phụ thuộc thư viện bên ngoài `datasets`:**
   - *Hiện tượng:* Gói `datasets` của Hugging Face có thể gây xung đột phụ thuộc hoặc yêu cầu cấu hình bổ sung.
   - *Xử lý:* Viết lại `HotelReviewDataset` bằng lớp `torch.utils.data.Dataset` thuần túy của PyTorch, giúp mã nguồn nhẹ hơn và hoàn toàn không phụ thuộc vào gói `datasets`.
3. **Cô lập Dataset và Tránh rò rỉ vào Git:**
   - *Hiện tượng:* File `dts_20k_raw.csv` có dung lượng tương đối lớn và không nên commit trực tiếp vào source control.
   - *Xử lý:* Cấu hình `.gitignore` loại trừ file CSV và thư mục model weights, giữ dataset cục bộ trong `data/dts_20k_raw.csv` với cơ chế fallback tự động.

---

## 6. Các Giả Định Kỹ Thuật (Assumptions)

1. **Dataset:** Sử dụng file `dts_20k_raw.csv` (20,000 mẫu) do giảng viên cung cấp, giữ nguyên câu tự nhiên cho BERT.
2. **Hardware:** Máy hiện tại có Python 3.11, PyTorch và Transformers đã cài đặt sẵn sàng. Nếu huấn luyện trên GPU thì dùng FP16, nếu trên CPU thì tự động điều chỉnh số batch hoặc sử dụng Colab GPU notebook (`BERT_Training_Colab.ipynb`).
3. **Random Seed:** Cố định `seed = 42` xuyên suốt để đảm bảo tính tái lập 100%.

---

## 7. Các Lệnh Chính Xác Dự Kiến Chạy Sau Khi Review

Khi người dùng phê duyệt tiến hành chạy thực nghiệm:

```powershell
# Bước 1: Sinh biểu đồ phân tích khám phá dữ liệu (EDA)
python src/data.py

# Bước 2: Huấn luyện và đánh giá Baseline (TF-IDF + Logistic Regression)
python src/train_baseline.py

# Bước 3: Huấn luyện & Fine-tuning BERT
python src/train_bert.py

# Bước 4: Đánh giá mô hình BERT trên Test Set & Trích xuất 20 ca lỗi thực tế
python src/evaluate.py

# Bước 5: Sinh slide PowerPoint nhúng biểu đồ và số liệu thực tế
python presentation/generate_presentation.py

# Bước 6: Khởi chạy ứng dụng Web Demo Streamlit
streamlit run app/app.py
```
