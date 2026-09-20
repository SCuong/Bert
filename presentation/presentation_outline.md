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
- **Bối cảnh:** Sự bùng nổ của đánh giá khách sạn trực tuyến và nhu cầu tự động hóa phân tích phản hồi khách hàng.
- **Phát biểu bài toán:** Input văn bản tiếng Anh -> Output nhãn nhị phân (Positive / Negative) kèm xác suất tin cậy.
- **Bên liên quan (Stakeholders):** Khách sạn, khách lưu trú, đội ngũ kỹ sư AI.
- **Tiêu chí thành công (Success Criteria):** Pipeline chuẩn mực, Zero Data Leakage, so sánh công bằng giữa Baseline và BERT, kiểm soát tính tái lập (`controlled for reproducibility with fixed seeds and documented environment`), giải thích ca lỗi.

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
- **Tập dữ liệu:** `dts_20k_raw.csv` (Teacher-provided hotel-review sentiment dataset, 20,000 mẫu ban đầu).
- **Kiểm toán dữ liệu (Data Audit):** Loại bỏ 255 mẫu (5 rỗng, 127 nhãn xung đột, 123 trùng lặp), còn 19,745 mẫu sạch (9,921 Negative, 9,824 Positive).
- **Phân chia Stratified Split (70/10/20, seed=42):** Train (13,821), Val (1,975), Test (3,949) — Xác nhận Zero Data Leakage.
- **Phân vị độ dài token BERT (Train+Val Scope, 15,796 mẫu):** Mean: 42.33 | Median: 30.0 | p90: 94.0 | p95: 121.0 | Max: 425 tokens.
- **Quyết định cấu hình:** Chọn `MAX_LENGTH = 128` (chỉ cắt cụt 3.93%, tối ưu cho GPU 8GB VRAM).

### Slide 6: Quy Trình Nghiên Cứu Chuẩn Mực (Project Pipeline)
- **Sơ đồ luồng xử lý:** Raw Data -> Pre-split Audit (Missing, Duplicates, Conflicting) -> Stratified Split (70/10/20, seed=42) -> Baseline -> BERT Fine-tuning -> Comprehensive Evaluation -> Demo App.
- **Nguyên tắc chống rò rỉ dữ liệu (No Data Leakage):** Tập Test chỉ được đánh giá duy nhất một lần ở bước cuối cùng.

### Slide 7: Mô Hình Cơ Sở (Baseline): TF-IDF + Logistic Regression
- **Triết lý AI Project Cycle:** *"Start from simple to more complex models"*.
- **Kiến trúc Baseline:** N-gram (1, 2), 10,000 features, Sublinear TF scaling kết hợp Logistic Regression (L-BFGS).
- **Kết quả đạt được:** Thiết lập mốc đối sánh vững chắc trước khi áp dụng Deep Learning.

### Slide 8: Thiết Kế Thực Nghiệm & Chiến Lược Fine-Tuning
- **Lựa chọn mô hình:** `google-bert/bert-base-uncased` (12 tầng, 768 chiều ẩn, 12 attention heads, ~110M tham số).
- **Đồng bộ Tokenizer & Model:** AutoTokenizer và AutoModel uncased, từ điển 30,522 WordPiece tokens.
- **Cấu hình siêu tham số:**
  - Max Length: 128 (đã xác nhận dựa trên phân vị p95 = 121 tokens từ EDA trên tập Train+Val).
  - Optimizer: AdamW với Decoupled Weight Decay = 0.01.
  - Learning rate: $2 \times 10^{-5}$ kết hợp Linear Warmup Scheduler (10% số bước).
  - Số epochs: 2–3 epochs (kiểm soát chặt chẽ qua Validation Loss & Macro F1).
- **Chiến lược Checkpoint:** Tự động chọn và phục hồi Checkpoint có Validation F1 tốt nhất.

### Slide 9: Triển Khai Kỹ Thuật Fine-Tuning BERT
- **Kiến trúc thuần PyTorch:** Kế thừa trực tiếp `torch.utils.data.Dataset`, không phụ thuộc thư viện ngoài `datasets`.
- **Tương thích API:** Sử dụng `processing_class` cho các phiên bản Hugging Face Transformers mới.
- **Giám sát quá trình huấn luyện:** Ghi nhận cả đường cong Train Loss và Validation Loss qua từng epoch.
- **Quản lý Artifacts:** Trọng số mô hình, metrics JSON và biểu đồ 300 DPI.

### Slide 10: Bảng So Sánh Kết Quả Thực Nghiệm Tổng Hợp
- Bảng so sánh phương pháp trên cùng tập dữ liệu:
  1. TF-IDF + Logistic Regression (Mô hình cơ sở mới của nhóm — Pending Experiment)
  2. Fine-Tuned BERT (Mô hình chính mới của nhóm — Pending Experiment)
  3. NNLM Google Embedding (Tham khảo: 79.00%, Precision/Recall/F1: Not reported)
  4. BiLSTM (Tham khảo: 75.00%, Precision/Recall/F1: Not reported)
  5. Old "BERT" (Tham khảo: 65.20%, Precision/Recall/F1: Not reported)
- **Các chỉ số đối sánh:** Accuracy, Macro Precision, Macro Recall, Macro F1.

### Slide 11: Ma Trận Nhầm Lẫn & Phân Tích Độ Chính Xác Từng Lớp
- Biểu đồ Heatmap Confusion Matrix của Baseline vs. BERT trên Test Set.
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
- Tóm tắt 3 kết quả chính: Pipeline chuẩn mực không rò rỉ, đánh giá khách quan giữa Baseline và BERT, đóng gói sản phẩm hoàn chỉnh.
- Trích dẫn học thuật chuẩn mực: Vaswani et al. (2017), Devlin et al. (2018), Hugging Face Transformers.
