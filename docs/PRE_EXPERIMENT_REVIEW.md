# Báo Cáo Rà Soát Trước Thực Nghiệm (Pre-Experiment Review)

**Dự án:** Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn (Fine-Tuning BERT for Hotel Review Sentiment Classification)  
**Trạng thái checkpoint:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`  
**Ngày thực hiện:** 20/09/2026  
**Nguyên tắc:** Triển khai độc lập mới hoàn toàn từ đầu; không tái sử dụng mã nguồn tham khảo (independent implementation from scratch; reference code was not reused), chưa chạy huấn luyện mô hình, toàn bộ chỉ số thực nghiệm mới đang ở trạng thái `PLACEHOLDER`.

---

## 1. Cây Thư Mục Dự Án (Project Tree)

```text
.
├── .gitignore
├── README.md                          # Hướng dẫn tổng quan dự án
├── requirements.txt                  # Danh sách thư viện và phiên bản
├── FINAL_REPORT.md                   # Báo cáo tổng kết 11 mục chuẩn học thuật
├── data/
│   ├── README.md                     # Đặc tả tập dữ liệu (teacher-provided dataset)
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

1. **EDA & Token Length Distribution:**
   - Lệnh: `python -m src.data`
   - Mục tiêu: Thực hiện Data Audit, đo lường phân vị độ dài token BERT thực tế, xuất `class_distribution.png` và `token_length_distribution.png`.
2. **Baseline Training & Evaluation:**
   - Lệnh: `python -m src.train_baseline`
   - Mục tiêu: Thiết lập mốc Accuracy, F1 và Confusion Matrix thực tế cho TF-IDF + Logistic Regression trên tập Test.
3. **BERT Fine-Tuning:**
   - Lệnh: `python -m src.train_bert`
   - Mục tiêu: Huấn luyện `bert-base-uncased` trong 2-3 epochs trên GPU/CPU, ghi nhận đường cong học tập thực tế (Train Loss & Val Loss).
4. **BERT Test Set Evaluation & Error Extraction:**
   - Lệnh: `python -m src.evaluate`
   - Mục tiêu: Đánh giá duy nhất 1 lần trên Test Set và trích xuất 20 ca lỗi thực tế (False Positives và False Negatives).
5. **PowerPoint Deck Generation:**
   - Lệnh: `python -m presentation.generate_presentation` (hoặc `--draft` khi chưa chạy thực nghiệm)
   - Mục tiêu: Nhúng các biểu đồ và số liệu thực nghiệm thực tế vào file slide PowerPoint.

---

## 5. Các Vấn Đề Kỹ Thuật Đã Nhận Diện & Đã Xử Lý (Known Issues & Fixes)

1. **Vấn đề mã hóa UTF-8 trên Windows Console (cp1252):**
   - *Hiện tượng:* Khi in tiếng Việt ra console Windows, Python gặp lỗi `UnicodeEncodeError: 'charmap' codec can't encode character`.
   - *Xử lý:* Đã bổ sung `sys.stdout.reconfigure(encoding='utf-8')` và `sys.stderr.reconfigure(encoding='utf-8')` vào đầu tất cả các file mã nguồn.
2. **Tương thích API Hugging Face Transformers mới (`processing_class`):**
   - *Hiện tượng:* Phiên bản Transformers mới loại bỏ tham số `tokenizer` trong `Trainer.__init__`, thay thế bằng `processing_class`.
   - *Xử lý:* Kiểm tra tham số runtime bằng `inspect.signature` để tự động truyền `processing_class` hoặc `tokenizer` tương thích tuyệt đối.
3. **Xử lý Missing Labels & Kiểm toán rò rỉ không double-count:**
   - *Hiện tượng:* Ép kiểu `df['label'].astype(int)` trước khi xử lý missing values có thể gây lỗi non-finite value.
   - *Xử lý:* Rà soát missing text và missing label độc lập, loại bỏ trước khi ép kiểu và xác thực miền `{0, 1}`, có assertion kiểm tra tính nhất quán số lượng loại bỏ.
4. **Cô lập Test Dataset trong quá trình huấn luyện:**
   - *Hiện tượng:* `train_bert.py` từng khởi tạo `test_ds` dù không dùng tới.
   - *Xử lý:* Loại bỏ hoàn toàn `test_ds` khỏi `train_bert.py`; tập Test chỉ được nạp ở `evaluate.py`.
5. **Chuẩn hóa Package Entrypoints:**
   - *Hiện tượng:* Chạy `python src/xxx.py` trực tiếp có thể gây lỗi `ModuleNotFoundError: No module named 'src'`.
   - *Xử lý:* Chuẩn hóa toàn bộ câu lệnh sang `python -m src.<module>`, đồng thời bổ sung `sys.path.insert(0, REPO_ROOT)` làm phương án dự phòng.

---

## 6. Các Giả Định Kỹ Thuật (Assumptions)

1. **Dataset:** Sử dụng tập dữ liệu `dts_20k_raw.csv` do giảng viên cung cấp (teacher-provided dataset), giữ nguyên câu tự nhiên cho BERT.
2. **Hardware:** Máy hiện tại có Python 3.11, PyTorch và Transformers đã cài đặt sẵn sàng.
3. **Random Seed & Tái lập:** Cố định `seed = 42` xuyên suốt (`controlled for reproducibility with fixed seeds and documented environment`).
4. **Độ dài chuỗi (Max Length):** Candidate ban đầu là 128, sẽ được quyết định chính thức sau khi phân tích phân vị độ dài token từ EDA.

---

## 7. Các Lệnh Chính Xác Dự Kiến Chạy Sau Khi Review

Khi người dùng phê duyệt tiến hành chạy thực nghiệm:

```powershell
# Bước 1: Sinh biểu đồ phân tích khám phá dữ liệu (EDA)
python -m src.data

# Bước 2: Huấn luyện và đánh giá Baseline (TF-IDF + Logistic Regression)
python -m src.train_baseline

# Bước 3: Huấn luyện & Fine-tuning BERT
python -m src.train_bert

# Bước 4: Đánh giá mô hình BERT trên Test Set & Trích xuất 20 ca lỗi thực tế
python -m src.evaluate

# Bước 5: Sinh slide PowerPoint nhúng biểu đồ và số liệu thực tế
python -m presentation.generate_presentation

# Bước 6: Khởi chạy ứng dụng Web Demo Streamlit
streamlit run app/app.py
```
