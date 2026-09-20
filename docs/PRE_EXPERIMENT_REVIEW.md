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

1. **`artifacts/metrics/baseline_test_metrics.json` & `artifacts/metrics/bert_test_metrics.json`**: Chưa được sinh (do chưa chạy `evaluate.py`).
2. **`artifacts/metrics/comparative_metrics.json`**: Chưa được sinh (do chưa chạy `evaluate.py`).
3. **`artifacts/metrics/error_cases.json`**: Chưa được sinh (do chưa chạy trích xuất lỗi).
4. **`artifacts/figures/*_test_confusion_matrix.png`**: Chưa được sinh (do chưa chạy `evaluate.py`).

*(Lưu ý: `artifacts/metrics/baseline_validation_metrics.json`, `artifacts/figures/baseline_val_confusion_matrix.png`, `artifacts/metrics/bert_validation_metrics.json`, `artifacts/figures/bert_val_confusion_matrix.png`, `artifacts/metrics/bert_training_history.json`, `artifacts/figures/training_history.png`, cùng mô hình local `artifacts/model/baseline_tfidf_lr.joblib` và `artifacts/model/bert_best_model/` đã được sinh và kiểm chứng tính hoàn thiện 100%).*

---

## 4. Trạng Thái Các Khâu Thực Nghiệm

1. **EDA & Token Length Distribution:** **ĐÃ THỰC THI (EXECUTED)**
   - Lệnh: `python -m src.data`
   - Kết quả: Data Audit loại bỏ 255 mẫu không hợp lệ/trùng lặp/xung đột, còn 19,745 mẫu sạch (Zero Data Leakage). Đo lường độ dài token trên tập Train+Val (15,796 mẫu) với p95 = 121.0 tokens, chỉ cắt cụt 3.93% tại 128. Đã chốt lựa chọn `MAX_LENGTH = 128` và xuất `artifacts/metrics/data_audit.json`, `artifacts/metrics/token_length_stats.json`, `artifacts/figures/class_distribution.png`, `artifacts/figures/token_length_distribution.png`.
2. **Baseline Training & Validation Evaluation:** **ĐÃ THỰC THI (EXECUTED)**
   - Lệnh: `python -m src.train_baseline`
   - Kết quả: Huấn luyện TF-IDF + Logistic Regression trên Train Set (13,821 mẫu), đánh giá phát triển trên Validation Set (1,975 mẫu). Đạt Accuracy 81.01%, Macro Precision 0.8116, Macro Recall 0.8100, Macro F1 0.8098, Weighted F1 0.8099. Thời gian huấn luyện 0.68s, thời gian suy luận 0.114s (~17,378 mẫu/s). Ma trận nhầm lẫn: 838 TN, 154 FP, 221 FN, 762 TP. Đã lưu `artifacts/metrics/baseline_validation_metrics.json`, `artifacts/figures/baseline_val_confusion_matrix.png` cùng mô hình local `artifacts/model/baseline_tfidf_lr.joblib`. Tập Test Set được niêm phong hoàn toàn.
3. **BERT Fine-Tuning & Validation Evaluation:** **ĐÃ THỰC THI (EXECUTED)**
   - Lệnh: `python -m src.train_bert`
   - Kết quả: Huấn luyện `google-bert/bert-base-uncased` trong 3 epochs (2,592 steps) trên Train Set (13,821 mẫu). Đánh giá phát triển trên Validation Set (1,975 mẫu). Đạt Accuracy 83.90%, Macro Precision 0.8393, Macro Recall 0.8389, Macro F1 0.8389, Weighted F1 0.8389. Thời gian huấn luyện 15,617.19s (~260.29 phút trên CPU), thời gian suy luận 171.58s (~11.5 mẫu/s). Ma trận nhầm lẫn: 848 TN, 144 FP, 174 FN, 809 TP. Tự động chọn checkpoint tốt nhất `checkpoint-2592`. Đã lưu `artifacts/metrics/bert_validation_metrics.json`, `artifacts/figures/bert_val_confusion_matrix.png`, `artifacts/metrics/bert_training_history.json`, `artifacts/figures/training_history.png` và mô hình local `artifacts/model/bert_best_model/`. Toàn bộ quá trình giữ nguyên niêm phong tập Test Set.
4. **Comparative Test Set Evaluation & Error Extraction:** `CHƯA CHẠY (NOT YET EXECUTED)`
   - Lệnh: `python -m src.evaluate`
   - Mục tiêu: Đánh giá so sánh đối đầu cả Baseline và BERT trên cùng tập Test Set độc lập; lưu `artifacts/metrics/baseline_test_metrics.json`, `artifacts/metrics/bert_test_metrics.json`, `artifacts/metrics/comparative_metrics.json` và trích xuất 20 ca lỗi thực tế (False Positives và False Negatives) vào `artifacts/metrics/error_cases.json`. Fail-fast nếu thiếu artifact mô hình.
5. **PowerPoint Deck Generation:** `CHƯA CHẠY BẢN CHÍNH THỨC (CHỈ HỖ TRỢ --DRAFT)`
   - Lệnh: `python -m presentation.generate_presentation --draft`
   - Mục tiêu: Nhúng các biểu đồ và số liệu thực nghiệm thực tế vào file slide PowerPoint sau khi hoàn tất training và evaluation.

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
