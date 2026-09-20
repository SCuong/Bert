# Dàn Ý Bài Thuyết Trình: Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn

**Tổng số slide:** 15 slide  
**Thời lượng dự kiến:** 7 - 10 phút  
**Phong cách thiết kế:** Học thuật, chuyên nghiệp, tối giản chữ, giàu biểu đồ thực nghiệm, không AI slop.

---

### Slide 1: Trang Tiêu Đề (Title Slide)
- **Tiêu đề lớn:** Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
- **Tiêu đề phụ:** Fine-Tuning BERT for Hotel Review Sentiment Classification
- **Môn học:** Trí tuệ Nhân tạo (Artificial Intelligence)
- **Quy trình:** Tuân thủ chuẩn mực `AI Project Cycle`
- **Thông tin:** Giảng viên hướng dẫn & Nhóm sinh viên thực hiện

### Slide 2: Bối Cảnh & Mục Tiêu (Scope & Problem Statement)
- **Bối cảnh:** Sự bùng nổ của đánh giá trực tuyến (Booking.com, TripAdvisor) và nhu cầu tự động hóa phân tích phản hồi khách hàng.
- **Phát biểu bài toán:** Input văn bản tiếng Anh -> Output nhãn nhị phân (Positive / Negative) kèm xác suất tin cậy.
- **Bên liên quan (Stakeholders):** Khách sạn, khách lưu trú, đội ngũ kỹ sư AI.
- **Tiêu chí thành công (Success KPIs):** Accuracy $\ge 88\%$, Macro F1 $\ge 0.88$, tính tái lập và khả năng giải thích lỗi.

### Slide 3: Tiến Hóa Kiến Trúc: Từ RNN/LSTM Đến Transformer
- **Hạn chế của RNN/LSTM:** Xử lý tuần tự không song song hóa được, tắc nghẽn gradient trên chuỗi dài (Vanishing Gradient).
- **Bước ngoặt Transformer (2017):** Loại bỏ hoàn toàn mạng hồi quy, tính toán song song 100% trên GPU, kết nối trực tiếp mọi cặp từ bằng Self-Attention.
- **So sánh trực quan:** Xử lý theo thời gian $t$ vs. Xử lý ma trận đồng thời.

### Slide 4: Kiến Trúc BERT & Cơ Chế Self-Attention
- **Bản chất của BERT:** Sử dụng phần Encoder của Transformer xếp chồng (12 tầng ở bản Base).
- **Deeply Bidirectional:** Đọc đồng thời hai chiều trái và phải ở mọi tầng.
- **Cơ chế tính toán Scaled Dot-Product Attention:**
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$
- **Multi-Head Attention (12 heads):** Mỗi đầu chú ý học một mối liên kết cú pháp/ngữ nghĩa độc lập.

### Slide 5: Phân Tích Dữ Liệu Khách Sạn (Data & EDA)
- **Tập dữ liệu:** `dts_20k_raw.csv` (20,000 đánh giá từ nền tảng Booking.com).
- **Phân bố nhãn:** Cân bằng hoàn hảo 50% Positive (10,000) và 50% Negative (10,000).
- **Phân tích độ dài văn bản:** Trung vị 25 từ, 90% dưới 128 từ, 97% dưới 256 từ -> Căn cứ lựa chọn `max_length = 128/256`.
- **Đặc thù Booking.com:** Cụm từ `"No Negative"` xuất hiện tự nhiên trong các đánh giá hài lòng.

### Slide 6: Quy Trình Nghiên Cứu Chuẩn Mực (Project Pipeline)
- **Sơ đồ luồng xử lý:** Raw Data -> Minimal Cleaning -> Stratified Split (70/10/20, seed=42) -> Baseline -> BERT Fine-tuning -> Comprehensive Evaluation -> Demo App.
- **Nguyên tắc chống rò rỉ dữ liệu (No Data Leakage):** Tập Test chỉ được đánh giá duy nhất một lần ở bước cuối cùng.

### Slide 7: Mô Hình Cơ Sở (Baseline): TF-IDF + Logistic Regression
- **Triết lý AI Project Cycle:** *"Start from simple to more complex models"*.
- **Kiến trúc Baseline:** N-gram (1, 2), 10,000 features, Sublinear TF scaling kết hợp Logistic Regression (L-BFGS).
- **Kết quả đạt được:** Thiết lập mốc đối sánh vững chắc trước khi áp dụng Deep Learning.

### Slide 8: Khảo Sát & Chỉ Ra Sai Sót Trong Mô Hình BERT Cũ
- **Phân tích kỹ thuật notebook `DL_Model.ipynb`:**
  1. *Lệch bảng từ vựng:* Cased Preprocess đi cùng Uncased Encoder (mã hóa sai token).
  2. *Đóng băng mô hình:* `trainable=False` (chỉ là Feature Extraction của Small BERT, không phải Fine-tuning).
  3. *Tốc độ học quá cao:* `lr=0.001` (gấp 50 lần mức khuyến nghị).
  4. *Overfitting cực nặng:* Train 100 epochs với MLP head sâu không dropout -> Train Acc 97.1%, nhưng Test Acc tụt xuống **65.2%**.

### Slide 9: Phương Pháp Fine-Tuning BERT Chuẩn Của Nhóm
- **Mô hình:** `google-bert/bert-base-uncased` (110M tham số).
- **Đồng bộ Tokenizer & Model:** `AutoTokenizer` và `BertForSequenceClassification`.
- **Cấu hình tối ưu:**
  - Optimizer: AdamW với Weight Decay = 0.01.
  - Learning rate: $2 \times 10^{-5}$ với Linear Warmup Scheduler.
  - Số epochs: 2–3 epochs (kiểm soát chặt chẽ qua Validation Loss).
  - Tự động nạp Checkpoint tốt nhất (`load_best_model_at_end=True`).

### Slide 10: Bảng So Sánh Kết Quả Thực Nghiệm Tổng Hợp
- Bảng so sánh 5 phương pháp trên cùng tập dữ liệu:
  1. TF-IDF + Logistic Regression (Mô hình cơ sở mới — Placeholder)
  2. NNLM Google Embedding (Historical result from supplied notebook: 79.0%)
  3. BiLSTM (Historical result from supplied notebook: 75.0%)
  4. Old "BERT" (Historical result from supplied notebook: 65.2%)
  5. Fine-tuned BERT (Mô hình mới của nhóm — Placeholder)
- **Các chỉ số đối sánh:** Accuracy, Macro Precision, Macro Recall, Macro F1, Thời gian huấn luyện.

### Slide 11: Ma Trận Nhầm Lẫn & Phân Tích Độ Chính Xác Từng Lớp
- Biểu đồ Heatmap Confusion Matrix của Baseline vs. BERT trên 4,000 mẫu Test.
- So sánh chi tiết độ chính xác của lớp Tiêu cực (0) và lớp Tích cực (1) (Sẽ sinh tự động sau khi chạy `train_baseline.py` và `evaluate.py`).

### Slide 12: Khung Phân Tích Lỗi Định Tính (Error Analysis Framework)
- Phương pháp luận khảo sát định tính 4 nhóm nguyên nhân gây ra lỗi dự đoán:
  - *Mixed Sentiment:* Khách khen vị trí nhưng chê cách âm / vệ sinh.
  - *Phủ định phức tạp / Đảo ngữ:* Cấu trúc phủ định kép tinh vi.
  - *Châm biếm / Sarcasm:* Lời khen mang hàm ý chê bai.
  - *Nhiễu nhãn / Cắt cụt:* Lỗi gán nhãn gốc hoặc review vượt quá `max_length`.
- Trích xuất 20 ca lỗi thực tế sẽ thực hiện qua `evaluate.py`.

### Slide 13: Ứng Dụng Thực Tế: Demo Streamlit
- Giao diện trực quan cho người dùng nhập review hoặc chọn tình huống thử nghiệm.
- Minh họa quá trình bẻ từ WordPiece (`[CLS]`, `##tokens`, `[SEP]`).
- Hiển thị xác suất dự đoán và nhãn phân loại theo thời gian thực.
- So sánh kết quả tức thời giữa Baseline và BERT trên cùng một văn bản.

### Slide 14: Giới Hạn & Hướng Phát Triển Tương Lai
- **Giới hạn hiện tại:** Bài toán nhị phân 0/1 chưa nắm bắt được đánh giá trung lập (3 sao); chi phí tính toán cao hơn mô hình tuyến tính khi triển khai quy mô lớn.
- **Hướng phát triển:** Phân loại cảm xúc đa khía cạnh (Aspect-Based Sentiment Analysis - ABSA); nén mô hình bằng DistilBERT hoặc ONNX Runtime để tăng tốc suy luận.

### Slide 15: Kết Luận & Tài Liệu Tham Khảo
- Tóm tắt 3 kết quả chính: Khắc phục lỗi kỹ thuật cũ, chứng minh sự vượt trội của BERT, đóng gói sản phẩm hoàn chỉnh.
- Trích dẫn học thuật chuẩn mực: Vaswani et al. (2017), Devlin et al. (2018), Hugging Face, Booking.com dataset.
