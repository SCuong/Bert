# Dàn Ý Bài Thuyết Trình: Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

**Tổng số slide:** 15 slide  
**Thời lượng dự kiến:** 8 - 10 phút  
**Hệ thống thiết kế:** Đại học Bách Khoa - ĐHĐN (DUT)  
**File trình chiếu chính thức:** `presentation/BERT_Project_Final.pptx`

---

### Slide 1: Trang Tiêu Đề (DUT Title Slide)
- **Tiêu đề lớn:** ĐỒ ÁN MÔN HỌC: TRÍ TUỆ NHÂN TẠO
- **Đề tài chính thức:** Ứng Dụng Mô Hình BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
- **Tiêu đề tiếng Anh:** Fine-Tuning BERT for Hotel Review Sentiment Classification
- **Quy trình phương pháp luận:** Tuân thủ chuẩn mực 6 giai đoạn `AI Project Cycle` (Scope & Plan -> Data -> Models -> Deployment -> Maintenance -> Feedback)
- **Thông tin đồ án:** Giảng viên hướng dẫn môn học & Nhóm sinh viên thực hiện

### Slide 2: Bối Cảnh & Mục Tiêu Nghiên Cứu (Scope & Plan)
- **Bối cảnh thực tế:** Sự bùng nổ của đánh giá khách sạn trực tuyến trên Booking.com; nhu cầu tự động hóa phân loại phản hồi khách hàng.
- **Phát biểu bài toán:** Input văn bản nhận xét tiếng Anh -> Output nhãn nhị phân (1: Tích cực, 0: Tiêu cực) kèm độ tin cậy.
- **Các bên liên quan (Stakeholders):** Ban quản lý khách sạn, khách hàng lưu trú, kỹ sư AI.
- **Mục tiêu kỹ thuật & Tiêu chí đánh giá:** Xây dựng mô hình cơ sở TF-IDF + Logistic Regression, fine-tuning chuẩn mực BERT, đánh giá đối đầu khách quan trên Held-Out Test Set (3,949 mẫu), kiểm soát chống rò rỉ dữ liệu (Zero Leakage) và phân tích định tính ca lỗi.

### Slide 3: Tiến Hóa Kiến Trúc: Từ RNN/LSTM Đến Transformer
- **Hạn chế của RNN/LSTM:** Điểm nghẽn xử lý tuần tự (Sequential Recurrence Bottleneck) không song song hóa được trên GPU; suy giảm thông tin ngữ cảnh xa (Vanishing Gradient).
- **Đột phá của Transformer (Vaswani et al., 2017):** Loại bỏ hoàn toàn mạng đệ quy; xử lý song song toàn bộ các từ trong chuỗi; kết nối trực tiếp mọi cặp từ qua cơ chế Self-Attention với đường truyền $\mathcal{O}(1)$; Positional Encoding mã hóa vị trí từ.

### Slide 4: Kiến Trúc BERT & Cơ Chế Multi-Head Self-Attention
- **Bản chất của BERT:** Sử dụng khối Encoder của Transformer (12 tầng ở bản Base); Deeply Bidirectional (nhìn đồng thời ngữ cảnh hai chiều tự do).
- **Cơ chế tính toán Scaled Dot-Product Attention:**
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$
- **Multi-Head Attention (12 heads):** Mỗi đầu chú ý học song song một khía cạnh ngôn ngữ khác nhau (cú pháp, đại từ, phủ định).
- **Token đặc biệt:** `[CLS]` (vector đại diện phân loại) và `[SEP]` (phân tách câu).

### Slide 5: Phân Tích Khám Phá Dữ Liệu (Data & EDA)
- **Tập dữ liệu:** `data/dts_20k_raw.csv` do giảng viên cung cấp (20,000 mẫu thô).
- **Kiểm toán dữ liệu (Data Audit):** Loại bỏ 255 mẫu (5 rỗng, 127 nhãn xung đột, 123 trùng lặp), còn 19,745 mẫu sạch (9,921 Negative - 50.25%, 9,824 Positive - 49.75%).
- **Phân chia Stratified Split (Seed 42):** Train: 13,821 (70%) | Val: 1,975 (10%) | Test: 3,949 (20%) — Xác nhận 0% rò rỉ dữ liệu.
- **Phân vị độ dài token BERT (Train+Val Scope):** Mean: 42.33 | Median: 30.0 | p90: 94.0 | p95: 121.0 | Max: 425 tokens.
- **Quyết định cấu hình:** Chọn `MAX_LENGTH = 128` (bảo toàn 96.07% văn bản, tối ưu chi phí tính toán $\mathcal{O}(L^2)$ và bộ nhớ kích hoạt).

### Slide 6: Quy Trình Nghiên Cứu Chuẩn Mực (Pipeline)
- **Sơ đồ 3 khối:**
  1. *Dữ liệu & Tiền xử lý:* Bảo toàn ngữ cảnh (giữ nguyên từ phủ định, dấu câu), kiểm toán dữ liệu và phân chia Stratified.
  2. *Mô hình hóa:* Xây dựng mô hình cơ sở TF-IDF + Logistic Regression và mô hình chính Fine-Tuned BERT.
  3. *Đánh giá & Triển khai:* Đánh giá đối đầu độc lập trên Test Set đúng 1 lần duy nhất, trích xuất ca lỗi và xây dựng Demo Streamlit.

### Slide 7: Mô Hình Cơ Sở: TF-IDF + Logistic Regression (Baseline)
- **Triết lý AI Project Cycle:** *"Start from simple to more complex models"* (Slide 9).
- **Kiến trúc:** TF-IDF (10,000 unigram + bigram, sublinear_tf) kết hợp Logistic Regression (L-BFGS, C=1.0).
- **Kết quả trên Held-Out Test Set (3,949 mẫu):**
  - Accuracy: 81.94% | Macro Precision: 0.8208 | Macro Recall: 0.8193 | Macro F1: 0.8192 | Weighted F1: 0.8192
  - Thời gian suy luận: 0.137 giây (~28,784 mẫu/giây).
  - Ma trận nhầm lẫn: 1,691 TN, 293 FP, 420 FN, 1,545 TP (713 lỗi).

### Slide 8: Phân Tích Sự Cố Mô Hình Cũ & Khác Biệt Pipeline Mới
- **Khảo sát mã nguồn cũ môn học (`DL_Model.ipynb` - 65.20% Accuracy):**
  1. *Lệch Tokenizer:* Tiền xử lý cased ghép với encoder uncased.
  2. *Đóng băng Encoder:* `trainable=False` (Feature Extraction tĩnh).
  3. *Learning rate quá lớn:* $10^{-3}$ (gấp 50 lần chuẩn), phá hủy trọng số.
  4. *Head quá sâu:* 5 tầng Dense liên tiếp, loại bỏ Dropout.
  5. *Overfitting:* Huấn luyện 100 epochs (Train 97% nhưng Test sụp đổ về 65.20%).
- **Pipeline mới của nhóm:** Full Fine-Tuning, đồng bộ uncased, AdamW (lr=2e-5, warmup), 1 tầng Linear + Dropout(0.1), 3 epochs có kiểm soát checkpoint.

### Slide 9: Quá Trình Huấn Luyện & Tinh Chỉnh BERT
- **Tiến trình 3 epochs trên CPU (15,617.19s ~ 4.34 giờ, 2,592 steps):**
  - Epoch 1: Train Loss 0.4077 | Val Loss 0.3541 | Val F1 0.8359
  - Epoch 2: Train Loss 0.2885 | Val Loss 0.3702 | Val F1 0.8384
  - Epoch 3: Train Loss 0.1983 | Val Loss 0.4503 | Val F1 **0.8389** (Đạt đỉnh)
- **Động lực học tập:** Giải thích hiện tượng Val Loss tăng nhẹ ở Epoch 3 do Cross-Entropy phạt xác suất ở các mẫu khó/nhiễu, trong khi Macro F1 đạt đỉnh 0.8389. Chọn `checkpoint-2592` tối ưu.

### Slide 10: Bảng So Sánh Kết Quả Thực Nghiệm Đối Đầu Trên Test Set
- **Bảng đối đầu chính thức trên cùng 3,949 mẫu Test Set:**
  - *TF-IDF + Logistic Regression (Baseline):* Accuracy 81.94%, Macro Precision 0.8208, Macro Recall 0.8193, Macro F1 0.8192
  - *Fine-Tuned BERT (Ours):* Accuracy **84.83%**, Macro Precision **0.8486**, Macro Recall **0.8482**, Macro F1 **0.8483**
  - *Mức độ cải thiện ($\Delta$):* **+2.89% Accuracy**, **+0.0291 Macro F1**
  - *Tham khảo lịch sử môn học (`DL_Model.ipynb`):* NNLM 79.00%, BiLSTM 75.00%, Old BERT 65.20% (Tăng **+19.63%** so với code cũ!).

### Slide 11: Ma Trận Nhầm Lẫn & So Sánh Chi Tiết Từng Lớp
- **Ma trận nhầm lẫn của Fine-Tuned BERT:** 1,711 TN, 273 FP, 326 FN, 1,639 TP (599 lỗi).
- **So sánh với Baseline:**
  - True Negatives tăng 20 mẫu (1,711 vs 1,691).
  - True Positives tăng 94 mẫu (1,639 vs 1,545).
  - False Negatives **giảm mạnh 94 ca** (từ 420 xuống 326 ca, giảm 22.38% số ca FN!).
  - Tổng số lỗi giảm 114 ca trên tập kiểm thử.

### Slide 12: Báo Cáo Phân Tích Lỗi Định Tính (Qualitative Error Analysis)
- **Khảo sát mẫu 20 ca lỗi có độ tin cậy cao nhất (10 FP, 10 FN):**
  - *Mixed Sentiment:* 15/20 ca (75.0%) chứa cảm xúc pha trộn giữa các khía cạnh.
  - *Dấu hiệu mơ hồ / nhiễu nhãn:* 8/20 ca (40.0%) có ngữ nghĩa mâu thuẫn với nhãn ground-truth.
  - *Thẻ biểu mẫu nguồn (`"No Positive"`):* 6/20 ca (30.0%).
  - *Cắt cụt độ dài token:* **0/20 ca** (đều $\le 126$ tokens).
- **Trả lời RQ3:** Lỗi bắt nguồn chủ yếu từ tính đa khía cạnh của cảm xúc và chất lượng dữ liệu gốc; cắt cụt không phải là nguyên nhân gây ra các ca lỗi cực đoan nhất.

### Slide 13: Ứng Dụng Thực Tế: Web Demo Thời Gian Thực (Streamlit)
- **Giao diện `app/app.py`:**
  - Nhập văn bản đánh giá bất kỳ; cung cấp sẵn 4 câu test mẫu phức tạp (phủ định, litotes, mệnh đề đối lập).
  - So sánh đối đầu song song (Side-by-Side) giữa Baseline và BERT.
  - Trực quan hóa giải thích bẻ từ con WordPiece (`[CLS]`, `##tokens`, `[SEP]`) và thanh đo xác suất Softmax.

### Slide 14: Giới Hạn Nghiên Cứu & Hướng Phát Triển Tương Lai
- **Giới hạn hiện tại:** Bài toán nhị phân đơn giản hóa (chưa có lớp Neutral 3 sao); chi phí tài nguyên tính toán và độ trễ suy luận trên CPU (12.85 mẫu/s vs 28,784 mẫu/s).
- **Hướng phát triển:** Phân tích Cảm xúc Đa Khía cạnh (Aspect-Based Sentiment Analysis - ABSA); nén mô hình với DistilBERT / ONNX Runtime; mở rộng ngữ liệu tiếng Việt (PhoBERT).

### Slide 15: Tổng Kết Đóng Góp & Sẵn Sàng Phản Biện (Q&A)
- **4 đóng góp nổi bật:**
  1. Hoàn thành trọn vẹn quy trình AI Project Cycle.
  2. Khôi phục tiềm năng của BERT so với code cũ (tăng từ 65.20% lên 84.83%).
  3. Minh chứng thực nghiệm trung thực với đầy đủ artifacts kiểm chứng.
  4. Hệ thống tài liệu học thuật và ứng dụng demo hoàn chỉnh.
- **Lời cảm ơn & Khởi động phiên Hỏi Đáp (Q&A).**
