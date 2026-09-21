# Dàn Ý Bài Thuyết Trình: Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

**Học phần:** Trí tuệ Nhân tạo (Artificial Intelligence)  
**Tổng số slide:** 13 slide  
**Thời lượng dự kiến:** 8 - 10 phút  
**Hệ thống thiết kế:** DUT-style template supplied for this project (Nền sáng tương phản cao `#F8FAFC`, Dark Theme tại Slide 1 và Slide 13)  
**File trình chiếu chính thức:** `presentation/BERT_Project_Final.pptx`  
**Mã nguồn sinh tự động:** `presentation/generate_presentation.py`

---

### Slide 1: Trang Tiêu Đề (Title Slide — Dark Theme)
- **Thiết kế:** Nền xanh đậm thương hiệu DUT từ template (`Template-DUT-Total - Copy (1).pptx`), toàn bộ chữ màu trắng và xám sáng (`#FFFFFF` & `#E2E8F0`), tương phản sắc nét.
- **Tiêu đề chính:** NGHIÊN CỨU VÀ ỨNG DỤNG MÔ HÌNH BERT CHO BÀI TOÁN PHÂN LOẠI CẢM XÚC ĐÁNH GIÁ KHÁCH SẠN
- **Tiêu đề tiếng Anh:** Fine-Tuning BERT for Hotel Review Sentiment Classification
- **Thông tin học thuật:**
  - Học phần: Trí tuệ Nhân tạo (Artificial Intelligence)
  - Giảng viên hướng dẫn: TS. Huỳnh Hữu Hưng
  - Sinh viên thực hiện: [Họ và tên sinh viên / Nhóm thực hiện]
  - Đơn vị: Trường Đại học Bách Khoa – Đại học Đà Nẵng
  - Thời gian: Tháng 09/2026

---

### Slide 2: Bối Cảnh Bài Toán & Mục Tiêu Nghiên Cứu (Scope & Objective — Light Theme)
- **Thiết kế:** Bố cục 2 thẻ so sánh song song (Side-by-Side Cards), nền thẻ trắng viền xám, tiêu đề thẻ xanh thép và xanh navy.
- **Thẻ 1: Thách thức bài toán (Problem):**
  - *Phân loại cảm xúc trực tuyến:* Nhu cầu tự động hóa phân tích hàng ngàn đánh giá khách sạn để nâng cao chất lượng dịch vụ lưu trú.
  - *Ngữ cảnh phức tạp:* Ngôn ngữ đánh giá chứa nhiều câu đa ý, cảm xúc hỗn hợp (mixed sentiment) và cấu trúc phủ định tinh vi.
  - *Hạn chế mô hình cũ:* Mô hình truyền thống (BoW/TF-IDF) bỏ qua trật tự từ; mô hình tuần tự (RNN/LSTM) gặp điểm nghẽn tính toán và suy giảm ngữ cảnh xa.
- **Thẻ 2: Mục tiêu & Đóng góp (Objective):**
  - *Quy trình chuẩn mực khép kín:* Triển khai đầy đủ 6 giai đoạn AI Project Cycle; kiểm toán exact-match trước split và case-normalized hậu nghiệm.
  - *Thực nghiệm đối chứng công bằng:* Huấn luyện mô hình cơ sở TF-IDF + Logistic Regression và Fine-tuning BERT (`bert-base-uncased`) trên cùng dữ liệu chuẩn.
  - *Đánh giá khách quan & Triển khai:* Đóng băng và kiểm thử trên Held-Out Test Set (3,949 mẫu); phân tích định tính ca lỗi và đóng gói Web UI Streamlit.

---

### Slide 3: Quy Trình Nghiên Cứu Chuẩn Mực (AI Project Cycle — Light Theme)
- **Thiết kế:** 7 thẻ quy trình nằm ngang (Horizontal Process Cards 01–07) kèm số thứ tự nổi bật và màu sắc phân tầng.
- **7 bước nghiên cứu khép kín:**
  - **01. Data Audit:** Loại bỏ 255 mẫu lỗi, xung đột nhãn và trùng lặp.
  - **02. Token EDA:** Phân tích phân vị độ dài token, chọn `MAX_LENGTH = 128`.
  - **03. Data Split:** Phân chia Stratified 70/10/20 với seed 42 cố định (13,821 / 1,975 / 3,949).
  - **04. Baseline:** Xây dựng mô hình cơ sở TF-IDF (10k features) + Logistic Regression.
  - **05. BERT Train:** Full fine-tuning 110M tham số, lưu checkpoint theo Validation Macro F1.
  - **06. Frozen Test:** Đánh giá đúng 1 lần duy nhất trên tập Test Set đã niêm phong.
  - **07. Error & Demo:** Kiểm toán chuyên sâu 20 ca lỗi cực đoan; đóng gói Web UI Streamlit.
- **Banner nguyên tắc cốt lõi (Bottom Callout):** Xây dựng độc lập từ đầu (from scratch) • Kiểm soát giao thoa dữ liệu • Đóng băng siêu tham số trước khi mở niêm phong tập kiểm thử.

---

### Slide 4: Tập Dữ Liệu & Kết Quả Kiểm Toán Chống Rò Rỉ (Dataset & Data Audit — Light Theme)
- **Thiết kế:** Lưới 4 thẻ chỉ số lớn (2x2 KPI Cards) với số liệu to bản (28pt) và mã màu trực quan.
- **4 chỉ số dữ liệu cốt lõi:**
  - **20,000 mẫu thô ban đầu:** Tập dữ liệu đánh giá khách sạn tiếng Anh do GV cung cấp; chứa các định dạng đặc thù (`'No Negative'`, `'No Positive'`).
  - **255 mẫu lỗi đã loại bỏ (Data Audit):** Loại bỏ 5 mẫu rỗng, 127 mẫu nhãn xung đột (từ 20 văn bản) và 123 mẫu trùng lặp tuyệt đối trước khi phân chia.
  - **19,745 mẫu sạch duy nhất:** Cân bằng lớp lý tưởng: 9,921 Tiêu cực (50.25%) và 9,824 Tích cực (49.75%). Bảo đảm tính đại diện khách quan.
  - **70% / 10% / 20% Stratified Split (Seed 42):** Train: 13,821 mẫu | Validation: 1,975 mẫu | Test: 3,949 mẫu. Pipeline xác nhận 0 giao thoa chuỗi chính xác; kiểm toán hậu nghiệm có `casefold()` phát hiện 3 / 10 / 2 cặp lần lượt ở Train–Validation / Train–Test / Validation–Test.

---

### Slide 5: Phân Bố Độ Dài Token & Quyết Định MAX_LENGTH (EDA & MAX_LENGTH — Light Theme)
- **Thiết kế:** Bố cục 2 cột (Cột trái: Biểu đồ phân bố độ dài token thực tế; Cột phải: 2 thẻ KPI và 1 thẻ quyết định kỹ thuật màu xanh lá).
- **Trực quan hóa:** `figures/token_length_distribution.png` (Histogram & KDE phân bố độ dài token BERT).
- **Số liệu thống kê (Train + Validation Scope):**
  - Trung vị: 30 tokens | Trung bình: 42.33 tokens.
  - Phân vị p90: 94 tokens | p95: 121 tokens | p99: 168 tokens | Max: 425 tokens.
  - Tỷ lệ chuỗi dài > 128 tokens: 3.93% (620 mẫu).
  - Tỷ lệ chuỗi dài > 256 tokens: 0.09%.
- **Quyết định cấu hình `MAX_LENGTH = 128`:**
  - Trong phạm vi Train + Validation, 96.07% văn bản không vượt quá 128 tokens (p95 = 121 tokens).
  - Giảm 4x kích thước ma trận Attention $\mathcal{O}(L^2)$ và bộ nhớ kích hoạt so với ngưỡng 256.
  - Cân đối tối ưu giữa việc giữ trọn vẹn ngữ cảnh và khả năng huấn luyện ổn định trên CPU.

---

### Slide 6: Thiết Lập Thực Nghiệm Đối Chứng: Baseline vs BERT (Experimental Setup — Light Theme)
- **Thiết kế:** Bố cục 2 thẻ so sánh đối đầu chi tiết (Side-by-Side Setup Cards).
- **Thẻ trái: Mô hình cơ sở (Baseline — TF-IDF + Logistic Regression):**
  - Đặc trưng: TF-IDF (Unigrams + Bigrams), từ điển `max_features = 10,000`.
  - Biến đổi tần suất: `sublinear_tf = True` ($1 + \log(tf)$) hạn chế ảnh hưởng của từ xuất hiện quá nhiều.
  - Phân loại: Logistic Regression với chuẩn hóa L2 (Ridge), $C = 1.0$, solver `lbfgs`.
  - Vai trò: Mốc đối chứng chuẩn mực theo nguyên tắc *"Start simple to complex models"*.
  - Tốc độ: Huấn luyện cực nhanh (0.68s), suy luận ~28,784 mẫu/giây trên CPU.
- **Thẻ phải: Mô hình chính (Fine-Tuned BERT):**
  - Mô hình gốc: `google-bert/bert-base-uncased` (110M tham số, 12 layers, 12 heads).
  - Cơ chế: Full Fine-Tuning toàn bộ 110M tham số của Transformer Encoder.
  - Kiến trúc: Mỗi khối encoder gồm self-attention, feed-forward layers, residual connections và layer normalization.
  - Siêu tham số: AdamW, $lr = 2\times 10^{-5}$, warmup ratio = 0.1, weight decay = 0.01.
  - Cấu hình: Batch size = 16, epochs = 3 (2,592 steps), `MAX_LENGTH = 128`.
  - Checkpoint: Tự động lưu checkpoint có Validation Macro F1 cao nhất (Epoch 3).

---

### Slide 7: Quá Trình Huấn Luyện BERT & Động Lực Học Tập (Training Dynamics — Light Theme)
- **Thiết kế:** Bố cục 2 cột (Cột trái: Đồ thị lịch sử huấn luyện thực tế; Cột phải: Thẻ tiến trình 3 epochs và Thẻ giải thích hiện tượng loss).
- **Trực quan hóa:** `figures/training_history.png` (Biểu đồ Train Loss theo step và Validation F1/Loss theo epoch).
- **Tiến trình 3 epochs trên CPU (15,617.19s ~ 4.34 giờ):**
  - Epoch 1: Train Loss (step avg) 0.4385 | Val Acc 83.14% | Val F1 0.8310
  - Epoch 2: Train Loss (step avg) 0.2877 | Val Acc 83.90% | Val F1 0.8387
  - Epoch 3: Train Loss (step avg) 0.2022 | Val Acc 83.90% | Val F1 **0.8389** (Đạt đỉnh)
  - Trainer aggregate training loss toàn bộ quá trình: 0.3071
- **Lựa chọn Checkpoint & Giải thích Loss:**
  - Chọn `checkpoint-2592` (cuối Epoch 3, đạt đỉnh Validation Macro F1 = 83.89%).
  - Giải thích loss: Cross-entropy ($-\log p$) phạt nặng độ tự tin ở một số ít mẫu biên mơ hồ khiến validation loss tăng nhẹ, trong khi phân loại nhãn cứng vẫn đạt hiệu năng đỉnh cao nhất.

---

### Slide 8: Kết Quả So Sánh Đối Đầu Trên Held-Out Test Set (Main Results — Light Theme)
- **Thiết kế:** Slide kết quả trung tâm (Visual Hero Slide). 3 thẻ số liệu lớn nổi bật: Baseline vs BERT vs Mức cải thiện Delta ($\Delta$), kèm banner kết luận bên dưới.
- **Thẻ 1: Baseline (TF-IDF + LR):**
  - Accuracy: **81.94%** (0.8194) | Macro F1-Score: **0.8192** (0.8192)
  - Macro P / R: 0.8208 / 0.8193 | Weighted F1: 0.8192
  - Tốc độ: 28,784 mẫu/s (0.137s)
- **Thẻ 2: Fine-Tuned BERT (Chính):**
  - Accuracy: **84.83%** (0.8483) | Macro F1-Score: **0.8483** (0.8483)
  - Macro P / R: 0.8486 / 0.8482 | Weighted F1: 0.8483
  - Tốc độ: 12.85 mẫu/s (307.3s)
- **Thẻ 3: Mức cải thiện đối chứng ($\Delta$):**
  - Accuracy Cải Thiện: **+2.89 percentage points** (+0.0289)
  - Macro F1 Cải Thiện: **+0.0291** (+2.91 percentage points khi quy đổi thang phần trăm)
  - Giảm 114 ca dự đoán sai (-16.0%) | Đánh đổi: Thời gian suy luận lớn hơn trên CPU
- **Banner khoa học:**
  - Minh chứng khoa học thực chất: BERT vượt trội Baseline toàn diện trên cả 5 chỉ số phân loại (+2.89 percentage points Accuracy, +0.0291 Macro F1).
  - Tính nhất quán giữa các tập: Chỉ số Validation Macro F1 (83.89%) và Test Macro F1 (84.83%) sát nhau, nhất quán với hiệu năng quan sát được trên cả hai tập held-out (Validation and Test metrics are close, consistent with similar observed performance across the two held-out splits).
  - Đánh đổi kỹ thuật: Nâng cao độ chính xác và giảm 114 ca lỗi (-16.0%) đi kèm chi phí tính toán và độ trễ suy luận lớn hơn trên CPU (12.85 mẫu/s vs 28,784 mẫu/s).

---

### Slide 9: So Sánh Ma Trận Nhầm Lẫn Trên Tập Test (Confusion Matrix — Light Theme)
- **Thiết kế:** Bố cục 2 cột trực quan (Trái: CM Baseline; Phải: CM BERT) kèm nhãn thông số và 2 thẻ phân tích kết luận bên dưới.
- **Trực quan hóa:**
  - Baseline CM: `TN = 1,691 | FP = 293 | FN = 420 | TP = 1,545` (Tổng lỗi: 713 ca / 18.06%).
  - BERT CM: `TN = 1,711 | FP = 273 | FN = 326 | TP = 1,639` (Tổng lỗi: 599 ca / 15.17%).
- **2 Kết luận chuyên sâu:**
  - *Giảm mạnh False Negatives (Bỏ sót tích cực):* BERT giảm **94 ca FN** (từ 420 xuống 326 ca, giảm **22.38%**), nhận diện chính xác thêm 94 đánh giá tích cực so với Baseline.
  - *Giảm đồng thời cả FP và FN:* BERT giảm 20 ca FP và 94 ca FN (tổng giảm 114 ca lỗi, -16.0%), cải thiện đồng bộ cả Precision (+2.78%) và Recall (+2.89%).

---

### Slide 10: Phân Tích Lỗi Định Tính Trên Mẫu 20 Ca Tự Tin Nhất (Error Analysis — Light Theme)
- **Thiết kế:** Lưới 2x2 gồm 4 thẻ phân loại lỗi có mã màu riêng biệt + Footnote ghi rõ phạm vi kiểm toán.
- **4 phân loại lỗi kiểm toán chuyên sâu:**
  - **01. Cảm xúc hỗn hợp (Mixed Sentiment) — 15/20 ca:** 15/20 mẫu kiểm toán chứa đồng thời mệnh đề khen và chê (ví dụ: 'phòng rộng nhưng phục vụ tệ'). Nhãn nhị phân đơn lẻ gặp khó khăn khi đại diện đầy đủ văn bản đa chiều cảm xúc.
  - **02. Mơ hồ nhãn / Khả năng nhiễu nhãn (Possible label ambiguity / noise) — 8/20 ca:** 8/20 mẫu bộc lộ mâu thuẫn rõ rệt giữa nhãn ground-truth và ngữ nghĩa bề mặt văn bản. Dự đoán của mô hình thể hiện sự nhất quán với ngữ nghĩa bài viết hơn là nhãn được gán.
  - **03. Phủ định / Nhượng bộ & Template Markers — 8 & 6 ca:** 8/20 ca chứa cấu trúc phủ định hoặc nhượng bộ ('not bad', 'didn't like'); 6/20 ca mang dấu vết biểu mẫu ghép chuỗi đặc thù ('No Positive', 'No Negative', 'nothing').
  - **04. Kiểm toán cắt cụt chuỗi (Truncation Audit) — 0/20 ca:** Không ca nào trong 20 selected highest-confidence error cases vượt MAX_LENGTH=128 (độ dài thực tế 6–126 tokens); không suy rộng quan sát này cho toàn bộ lỗi.
- **Footnote:** * Thống kê chỉ áp dụng trong phạm vi 20 ca lỗi có độ tự tin cao nhất được kiểm toán (within the 20 selected highest-confidence errors), không suy rộng cho toàn bộ 599 ca lỗi của BERT.

---

### Slide 11: Ứng Dụng Tương Tác Thời Gian Thực (Streamlit Demo — Light Theme)
- **Thiết kế:** Bố cục 2 cột (Cột trái: Thẻ mô phỏng giao diện Web Streamlit thực tế; Cột phải: 3 thẻ tính năng nổi bật).
- **Cột trái — Mockup UI Web (`app/app.py`, minh họa giao diện; không phải benchmark đóng băng):**
  - Mẫu kiểm thử: *"The room was a bit small, but the location was great and breakfast was delicious!"*
  - Khi chạy, ứng dụng hiển thị nhãn dự đoán và độ tin cậy của BERT cùng Baseline.
  - Ứng dụng hiển thị danh sách token WordPiece của văn bản đầu vào.
  - Độ trễ được đo trực tiếp khi suy luận và phụ thuộc phần cứng, môi trường thực thi.
- **Cột phải — 3 Tính năng nổi bật:**
  - *Triển khai cục bộ khép kín:* Nạp tự động trọng số đã đóng băng từ `artifacts/model/bert_best_model/`; đo lường và hiển thị độ trễ suy luận thời gian thực.
  - *So sánh đối đầu song song:* Cho phép thử nghiệm trực tiếp khả năng nắm bắt ngữ cảnh câu giữa TF-IDF và Transformer trên cùng một văn bản đầu vào.
  - *Trực quan hóa cơ chế BERT:* Hiển thị danh sách token WordPiece (`##`), minh họa trực quan cơ chế tách từ và biểu diễn vector.

---

### Slide 12: Hạn Chế Của Nghiên Cứu & Hướng Phát Triển (Limitations & Future Work — Light Theme)
- **Thiết kế:** Bố cục 2 thẻ song song (Trái: Hạn chế; Phải: Hướng phát triển) + Banner 3 kết luận cốt lõi bên dưới.
- **Thẻ trái — Hạn chế hiện tại (Limitations):**
  - *Phân loại nhị phân (Binary sentiment only):* Hiện tại chỉ phân loại 2 lớp (Tích cực / Tiêu cực), chưa xử lý lớp trung lập (3 sao / Neutral) hoặc cảm xúc nhiều mức độ.
  - *Phạm vi kiểm toán lỗi (Selected qualitative analysis):* Chỉ tập trung kiểm toán 20 ca lỗi có độ tự tin cao nhất (highest-confidence errors), không suy rộng cho toàn bộ 599 ca lỗi của BERT.
  - *Chi phí suy luận trên CPU (BERT CPU inference cost):* Tốc độ ~12.85 mẫu/s (307.3s cho 3,949 mẫu) chậm hơn nhiều so với mô hình cơ sở (~28,784 mẫu/s) khi triển khai thực tế.
  - *Cắt cụt độ dài token (Sequence truncation):* 3.93% văn bản trong tập Train + Validation (620 mẫu) vượt quá ngưỡng MAX_LENGTH=128.
- **Thẻ phải — Hướng phát triển tương lai (Future Work):**
  - *Phân tích cảm xúc theo khía cạnh (ABSA):* Nhận diện cụ thể cảm xúc khách hàng theo từng thực thể dịch vụ (vị trí, phòng ốc, vệ sinh, giá cả, phục vụ).
  - *Tối ưu hóa & nén mô hình (Efficient/distilled models):* Triển khai các mô hình nhỏ gọn hơn (DistilBERT, TinyBERT) hoặc lượng tử hóa kết hợp ONNX Runtime / TensorRT để tăng tốc độ suy luận.
  - *Mở rộng đa ngữ & Tiếng Việt (Vietnamese / multilingual extension):* Huấn luyện và đánh giá trên các mô hình tiếng Việt chuyên biệt (PhoBERT, ViBERT) hoặc đa ngữ (mBERT, XLM-RoBERTa).
- **Banner dưới — 3 Kết luận cốt lõi:**
  - (1) Quy trình chuẩn mực, kiểm soát và báo cáo minh bạch giao thoa dữ liệu.
  - (2) BERT vượt trội Baseline toàn diện (+2.89 percentage points Acc, +0.0291 Macro F1).
  - (3) Lỗi thực tế bắt nguồn từ cảm xúc pha trộn và mâu thuẫn nhãn.

---

### Slide 13: Kết Luận & Phiên Hỏi Đáp (Q&A — Dark Theme)
- **Thiết kế:** Nền xanh đậm thương hiệu DUT từ template (`Slide 14`), chữ trắng tương phản cao.
- **Tiêu đề lớn:** TRÂN TRỌNG CẢM ƠN!
- **Nội dung:**
  - Khẳng định tên đề tài: NGHIÊN CỨU VÀ ỨNG DỤNG MÔ HÌNH BERT CHO BÀI TOÁN PHÂN LOẠI CẢM XÚC ĐÁNH GIÁ KHÁCH SẠN
  - Học phần: Trí tuệ Nhân tạo (Artificial Intelligence)
  - Giảng viên hướng dẫn: TS. Huỳnh Hữu Hưng
  - Sinh viên thực hiện: [Họ và tên sinh viên / Nhóm thực hiện]
  - Đơn vị: Trường Đại học Bách Khoa – Đại học Đà Nẵng
  - Kêu gọi phiên Hỏi & Đáp: XIN KÍNH MỜI QUÝ THẦY CÔ VÀ HỘI ĐỒNG ĐẶT CÂU HỎI! (PHIÊN HỎI & ĐÁP — Q&A).
