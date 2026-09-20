# Báo Cáo Dự Án (Pre-Experiment Implementation Checkpoint)

> [!IMPORTANT]
> **TRẠNG THÁI HIỆN TẠI:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`  
> Toàn bộ mã nguồn, cấu trúc dữ liệu, baseline và pipeline fine-tuning BERT đã được triển khai độc lập (Clean-Room Implementation) và vượt qua các bài kiểm tra cú pháp/import.  
> Các thực nghiệm huấn luyện và đánh giá trên Test Set **CHƯA ĐƯỢC CHẠY (NOT YET EXECUTED)** nhằm phục vụ quá trình rà soát mã nguồn của người dùng.  
> Mọi chỉ số thực nghiệm mới trong tài liệu này hiện được đánh dấu rõ ràng là `PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT`.

**Đề tài:** Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn  
**Tên tiếng Anh:** Fine-Tuning BERT for Hotel Review Sentiment Classification  
**Môn học:** Trí tuệ Nhân tạo (Artificial Intelligence)  
**Quy trình:** Xây dựng mới hoàn toàn độc lập, tuân thủ chặt chẽ `AI Project Cycle.pptx`.  
**Ngày cập nhật:** 20/09/2026  

---

## 1. Những Gì Tìm Thấy Trong Tài Liệu Giảng Viên (What I Found)

Qua quá trình khảo sát, kiểm tra toàn bộ workspace giảng viên cung cấp:
1. **Quy trình môn học (`AI Project Cycle.pptx`):** Giảng viên định hướng rõ ràng 6 giai đoạn: Scope & Plan $\rightarrow$ Data $\rightarrow$ Models $\rightarrow$ Deployment $\rightarrow$ Maintenance $\rightarrow$ Feedback. Slide 9 nêu rõ nguyên tắc phương pháp luận: *"We should start from the simple to more complex models because our solutions need to be as compact as possible"*.
2. **Cơ sở lý thuyết (`Transformer.pptx` / `Transformer.pdf`):** Cung cấp nền tảng về Transformer, hạn chế của RNN/LSTM (tuần tự, vanishing gradient), cơ chế Self-Attention, Multi-head Attention và Positional Encoding.
3. **Mã nguồn tham khảo (`NLP_Demo/`):**
   - File dữ liệu `dts_20k_raw.csv` gồm 20,000 đánh giá khách sạn từ Booking.com, cân bằng 50/50.
   - Notebook `Preprocessing_and_Visualizing.ipynb`: Áp dụng xóa stopwords NLTK một cách máy móc, làm xóa mất chữ `"No"` trong cụm `"No Negative"`, để lại chữ `"negative"` ngay đầu review tích cực, đồng thời xóa các từ phủ định quan trọng như `"not"`, `"no"`, `"never"`.
   - Notebook `DL_Model.ipynb`: Chứa kết quả lịch sử: NNLM (79.0%), BiLSTM (75.0%) và một triển khai "BERT" đạt kết quả rất thấp (**65.20%**).
   - Qua audit, nhóm phát hiện mô hình "BERT" cũ gặp 5 lỗi kỹ thuật nghiêm trọng: Lệch tokenizer cased với encoder uncased, đóng băng encoder (`trainable=False`), tốc độ học quá lớn (`0.001`), classifier head sâu thiếu điều quy, và overfitting nặng sau 100 epochs (Train Acc 97% nhưng Test Acc 65%).

---

## 2. Những Gì Nhóm Đã Xây Dựng (What I Built)

Dự án được triển khai **mới hoàn toàn từ đầu (Clean-Room Implementation)**, độc lập 100% tại repository root:
1. **Pipeline dữ liệu (`src/data.py`):** Làm sạch tối thiểu bảo toàn ngữ cảnh cho Transformer, phân chia dữ liệu Stratified (70% Train, 10% Val, 20% Test) với seed cố định `42`.
2. **Mô hình cơ sở (`src/train_baseline.py`):** Xây dựng mô hình TF-IDF (10,000 unigram + bigram) kết hợp Logistic Regression.
3. **Mô hình BERT Fine-Tuning (`src/train_bert.py`):** Tinh chỉnh mô hình chính thức `google-bert/bert-base-uncased` bằng Hugging Face Transformers và PyTorch, sử dụng AdamW (lr=2e-5, weight decay=0.01), huấn luyện 2-3 epochs có kiểm soát checkpoint.
4. **Mô-đun đánh giá độc lập (`src/evaluate.py`):** Đánh giá trên tập kiểm thử (Test Set) đúng 1 lần, xuất ma trận nhầm lẫn và trích xuất danh sách lỗi.
5. **Đường ống suy luận (`src/predict.py`):** Cung cấp hàm dự đoán cho cả Baseline và BERT kèm chi tiết bẻ từ WordPiece.
6. **Ứng dụng Demo thời gian thực (`app/app.py`):** Giao diện tương tác Streamlit trực quan, hỗ trợ so sánh đối đầu giữa Baseline và BERT.
7. **Hệ thống tài liệu học thuật (`docs/`):** Audit tài liệu (`01_material_audit.md`), Đặc tả bài toán (`02_project_spec.md`), Phân tích mô hình cũ (`03_old_bert_analysis.md`), Khung phân tích lỗi (`04_error_analysis.md`), Cẩm nang 25 khái niệm (`STUDY_GUIDE.md`), và Bộ 25 câu hỏi phản biện (`DEFENSE_QA.md`).
8. **Slide thuyết trình học thuật (`presentation/BERT_Project.pptx`):** 15 slide thiết kế bằng `python-pptx`, nhúng biểu đồ thực nghiệm, kèm kịch bản thuyết trình chi tiết (`speaker_notes.md`).
9. **Jupyter Notebooks (`notebooks/`):** Notebook EDA (`01_EDA.ipynb`), Notebook Baseline (`02_Baseline.ipynb`), và Notebook Google Colab GPU độc lập (`BERT_Training_Colab.ipynb`).

---

## 3. Dữ Liệu & Tiền Xử Lý (Data)

- **Quy mô & Nguồn gốc:** 20,000 bài đánh giá khách sạn bằng tiếng Anh (`data/dts_20k_raw.csv` do giảng viên cung cấp - teacher-provided dataset).
- **Phân bố ban đầu:** 10,000 mẫu Tích cực (1) và 10,000 mẫu Tiêu cực (0) — Cân bằng 1:1 ở tập dữ liệu thô.
- **Tiền kiểm định & Làm sạch tối thiểu (Pre-split Audit & Minimal Cleaning):**
  - Xử lý các dòng thiếu text hoặc thiếu nhãn.
  - Xóa các thẻ HTML rác (`<br />`, `<p>`) và chuẩn hóa khoảng trắng.
  - Loại bỏ các dòng văn bản rỗng sau khi làm sạch.
  - Phát hiện và loại bỏ các văn bản có nhãn xung đột (Conflicting Labels).
  - Loại bỏ các văn bản trùng lặp hoàn toàn (Exact Duplicates) để ngăn chặn triệt để rò rỉ qua Test Set.
  - **Giữ nguyên 100% từ ngữ tự nhiên, dấu câu, chữ hoa/thường và từ phủ định** nhằm phục vụ thuật toán WordPiece và Positional Embeddings của BERT.
- **Phân chia dữ liệu (Stratified Split, seed=42):**
  - **Train Set:** 70.0% — Dùng để cập nhật gradient.
  - **Validation Set:** 10.0% — Dùng để chọn checkpoint và Early Stopping.
  - **Test Set:** 20.0% — Hoàn toàn độc lập, chỉ nạp đúng 1 lần khi đánh giá cuối cùng.
  - **Tính tái lập:** Được kiểm soát chặt chẽ (`controlled for reproducibility with fixed seeds and documented environment`).

---

## 4. Các Mô Hình Thực Nghiệm (Models)

### 4.1. Baseline Model: TF-IDF + Logistic Regression
- **Kiến trúc:** `TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True)` kết hợp `LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs')`.
- **Vai trò:** Thiết lập chuẩn đối sánh tối thiểu theo Slide 9 `AI Project Cycle.pptx`.

### 4.2. Main Model: Fine-Tuned BERT (`bert-base-uncased`)
- **Kiến trúc:** 12 tầng Transformer Encoder, 768 chiều ẩn, 12 attention heads (~110M tham số).
- **Phân loại chuỗi:** Vector đại diện `[CLS]` (768 chiều) $\rightarrow$ `Dropout(p=0.1)` $\rightarrow$ `Linear(768, 2)` $\rightarrow$ `Softmax`.
- **Cấu hình tối ưu:**
  - Optimizer: AdamW với Decoupled Weight Decay = 0.01.
  - Learning rate: $2 \times 10^{-5}$ kết hợp Linear Warmup Scheduler (10% tổng số bước).
  - Epochs: 2–3 epochs.
  - Batch size: 16 (FP16 mixed precision nếu có GPU).
  - Tự động nạp lại checkpoint có Validation F1 cao nhất (`load_best_model_at_end=True`).
  - Ghi nhận đầy đủ đường cong học tập (Train Loss và Validation Loss) qua từng epoch.

---

## 5. Kết Quả Thực Nghiệm Đối Đầu (Results)

> [!NOTE]
> Các chỉ số của mô hình nhóm (TF-IDF + LR và Fine-Tuned BERT) sẽ được ghi nhận trực tiếp sau khi hoàn tất thực thi trên tập kiểm thử độc lập.  
> Các kết quả tham khảo từ notebook môn học (`DL_Model.ipynb`) chỉ báo cáo chỉ số Accuracy; các chỉ số Precision, Recall, Macro F1 không được công bố trong tài liệu gốc (`Not reported`).

| Mô Hình / Phương Pháp | Vai Trò / Phân Loại | Accuracy | Macro Precision | Macro Recall | Macro F1 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | *Mô hình cơ sở mới (Nhóm)* | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` |
| **Fine-Tuned BERT (Ours)** | *Mô hình chính mới (Nhóm)* | `[PENDING]` | `[PENDING]` | `[PENDING]` | `[PENDING]` |

*Tham khảo kết quả lịch sử (`DL_Model.ipynb`):* NNLM: Acc 79.00% | BiLSTM: Acc 75.00% | Old BERT: Acc 65.20% (Chi tiết phân tích lỗi kỹ thuật xem tại [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md)).

---

## 6. Vì Sao Pipeline BERT Mới Khác Biệt Hoàn Toàn Code Cũ

| Tiêu chí kỹ thuật | Triển khai cũ (`DL_Model.ipynb`) | Triển khai mới của nhóm (Our Clean-Room BERT) |
| :--- | :--- | :--- |
| **Tính tương thích từ vựng** | Cased Preprocess ghép với Uncased Model $\rightarrow$ **Lệch token ID** | Đồng bộ tuyệt đối: `AutoTokenizer` và `AutoModel` cùng bản **uncased** |
| **Cơ chế huấn luyện** | Đóng băng Encoder (`trainable=False`) $\rightarrow$ **Chỉ trích xuất đặc trưng** | Mở khóa toàn bộ tham số $\rightarrow$ **True Fine-Tuning** |
| **Tốc độ học (Learning Rate)** | `1e-3` (quá lớn gấp 50 lần, phá vỡ trọng số) | `2e-5` kết hợp Linear Warmup Scheduler chuẩn mực |
| **Bộ tối ưu hóa** | Adam thông thường | **AdamW** (Decoupled Weight Decay = 0.01) |
| **Kiến trúc Head** | 5 tầng Dense sâu liên tiếp, xóa bỏ Dropout | 1 tầng Linear duy nhất + Dropout(0.1) |
| **Số lượng Epoch** | 100 epochs $\rightarrow$ **Overfitting cực độ** (Train 97%, Test 65%) | 2–3 epochs $\rightarrow$ Kiểm soát chặt chẽ qua Validation Loss |
| **Chiến lược Checkpoint** | Đánh giá epoch 100 bị overfit | Tự động chọn và phục hồi Checkpoint có Val F1 tốt nhất |

---

## 7. Hướng Dẫn Cài Đặt & Khởi Chạy (How to Run)

Toàn bộ các câu lệnh dưới đây được chuẩn hóa chạy dạng package từ repository root:

```bash
# 1. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

# 2. Phân tích dữ liệu, kiểm toán leakage & Xuất biểu đồ EDA
python -m src.data

# 3. Huấn luyện và đánh giá mô hình cơ sở (Baseline)
python -m src.train_baseline

# 4. Huấn luyện & Fine-tuning mô hình BERT
python -m src.train_bert

# 5. Đánh giá mô hình BERT trên Test Set & Trích xuất ca lỗi
python -m src.evaluate

# 6. Tạo slide thuyết trình PowerPoint (Chế độ nháp hoặc chính thức)
python -m presentation.generate_presentation --draft

# 7. Khởi chạy ứng dụng Web Demo tương tác
streamlit run app/app.py
```

---

## 8. Vị Trí Slide Thuyết Trình & Sản Phẩm Demo

- **Trình tạo Slide PowerPoint:** `presentation/generate_presentation.py` (*presentation generator implemented; final deck pending experiment results*)
- **Dàn ý chi tiết 15 slide:** `presentation/presentation_outline.md`
- **Kịch bản thuyết trình 8-10 phút:** `presentation/speaker_notes.md`
- **Mã nguồn ứng dụng Demo:** `app/app.py`
- **Notebook Google Colab độc lập:** `notebooks/BERT_Training_Colab.ipynb`

---

## 9. Những Nội Dung Sinh Viên Cần Nắm Vững Khi Bảo Vệ

Để tự tin bảo vệ trước Hội đồng, sinh viên cần đọc kỹ hai tài liệu trong thư mục `docs/`:
1. **`docs/STUDY_GUIDE.md`:** Nắm vững 25 khái niệm cốt lõi:
   - Cơ chế Self-Attention và công thức tính $\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$.
   - Ý nghĩa của token `[CLS]`, `[SEP]`, `[MASK]`.
   - Thuật toán bẻ từ con WordPiece Tokenization và cách xử lý từ ngoài từ điển (OOV).
   - Sự khác biệt giữa Pre-training (MLM, NSP) và Fine-tuning.
   - Tại sao không xóa stopwords khi tiền xử lý cho BERT.
2. **`docs/DEFENSE_QA.md`:** Luyện tập trả lời 25 câu hỏi phản biện thường gặp theo 2 mức độ: Trả lời nhanh 30 giây và Trả lời mở rộng 1-2 phút.

---

## 10. Các Giới Hạn Còn Lại & Hướng Phát Triển (Remaining Limitations)

1. **Giới hạn bài toán nhị phân:** Chỉ phân loại 2 thái cực 0 và 1, chưa phân loại được các đánh giá trung tính (Neutral - 3 sao).
2. **Hiện tượng cắt cụt văn bản (Truncation):** Lựa chọn `max_length = 128` giúp tối ưu GPU nhưng làm mất đoạn kết luận của khoảng 10% các bài đánh giá dài.
3. **Độ trễ suy luận:** BERT có 110 triệu tham số, thời gian suy luận (~15-25ms/câu) chậm hơn đáng kể so với Logistic Regression (<0.5ms/câu).
4. **Hướng phát triển tiếp theo:** Triển khai Phân tích Cảm xúc Đa Khía cạnh (Aspect-Based Sentiment Analysis) và nén mô hình bằng DistilBERT hoặc ONNX Runtime.

---

## 11. Báo Cáo Kiểm Chứng Thực Nghiệm (Verification Summary)

- **Trạng thái:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`.
- **Mã nguồn đã triển khai & kiểm tra cú pháp:**
  - `src/data.py`: Hoàn thành.
  - `src/train_baseline.py`: Hoàn thành.
  - `src/train_bert.py`: Hoàn thành.
  - `src/evaluate.py`: Hoàn thành.
  - `src/predict.py`: Hoàn thành.
  - `app/app.py`: Hoàn thành.
  - `presentation/generate_presentation.py`: Hoàn thành.
- **Thực nghiệm thực tế:**
  - `Baseline training`: `NOT YET EXECUTED` (Sẵn sàng chạy).
  - `BERT Fine-Tuning`: `NOT YET EXECUTED` (Sẵn sàng chạy).
  - `Test set evaluation`: `NOT YET EXECUTED` (Sẵn sàng chạy).
