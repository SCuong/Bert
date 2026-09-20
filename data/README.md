# Hướng Dẫn & Đặc Tả Dữ Liệu: Hotel Reviews Sentiment Dataset

## 1. Nguồn gốc dữ liệu (Data Provenance)
- **Tập dữ liệu sử dụng:** `dts_20k_raw.csv` do giảng viên cung cấp trong thư mục `Bài giảng/AI.Code/NLP_Demo/dts_20k_raw.csv`.
- **Đặc tả nguồn gốc:** Đây là **teacher-provided hotel-review sentiment dataset** (tập dữ liệu phân loại cảm xúc đánh giá khách sạn do giảng viên cung cấp cho môn học).
- **Đặc trưng cấu trúc văn bản:** Trong dữ liệu xuất hiện các marker mang phong cách biểu mẫu đánh giá của nền tảng Booking.com:
  1. *Trường nhận xét tiêu cực:* Khi không có phàn nàn gì, người dùng thường điền cụm mặc định `"No Negative"`.
  2. *Trường nhận xét tích cực:* Khi không có lời khen nào, người dùng thường điền cụm mặc định `"No Positive"`.
  Khi hai trường này được ghép lại trong dữ liệu thô, cụm từ `"No Negative"` xuất hiện phổ biến ở đầu nhiều nhận xét tích cực.
  *Lưu ý học thuật:* Việc xuất hiện các marker này không được sử dụng làm bằng chứng pháp lý chứng minh nguồn gốc chính thức khi chưa có metadata xác thực kèm theo. Dự án coi đây là đặc thù dữ liệu thực tế cần được mô hình xử lý đúng đắn.

---

## 2. Thông số & Phân bố dữ liệu ban đầu

| Thuộc tính | Giá trị ban đầu |
| :--- | :--- |
| **Tổng số dòng thô** | 20,000 mẫu |
| **Số cột (Schema)** | 2 cột: `text` (văn bản đánh giá), `label` (nhãn nhị phân) |
| **Số mẫu Positive (1)** | 10,000 mẫu (50.0% ở tập thô) |
| **Số mẫu Negative (0)** | 10,000 mẫu (50.0% ở tập thô) |
| **Độ cân bằng nhãn** | Cân bằng ban đầu (1:1) |
| **Kiểm toán dữ liệu (Data Audit)** | Toàn bộ mẫu thiếu, rỗng, xung đột nhãn và trùng lặp được xử lý tự động qua `src/data.py` |

---

## 3. Chiến lược phân chia dữ liệu (Data Splitting Strategy)

Nhằm đảm bảo tính khoa học và ngăn chặn hoàn toàn hiện tượng rò rỉ dữ liệu (Data Leakage):
- **Tỷ lệ phân chia:**
  - **Train set:** 70% — Dùng để huấn luyện mô hình.
  - **Validation set:** 10% — Dùng để chọn checkpoint tốt nhất, theo dõi loss và tránh overfitting.
  - **Test set:** 20% — Tập kiểm thử độc lập, chỉ được nạp đúng một lần khi đánh giá mô hình cuối cùng.
- **Phương pháp phân chia:** `StratifiedShuffleSplit` từ thư viện `scikit-learn` nhằm bảo toàn tỷ lệ cân bằng của hai nhãn ở cả 3 tập sau khi đã loại bỏ trùng lặp.
- **Tính tái lập:** Được kiểm soát chặt chẽ (`controlled for reproducibility with fixed seeds and documented environment`) với `seed = 42`.

---

## 4. Nguyên tắc tiền xử lý (Preprocessing Principles)

- **KHÔNG xóa stopwords:** Trong bài toán cảm xúc, các stopword như *"not"*, *"no"*, *"never"*, *"but"*, *"very"* mang thông tin ngữ nghĩa quyết định (ví dụ: *"not good"* khác hoàn toàn *"good"*).
- **KHÔNG lemmatize cả câu:** Mô hình BERT sử dụng thuật toán tách từ con (WordPiece Tokenization) và có ma trận nhúng vị trí (Positional Embeddings), có khả năng tự động xử lý các biến thể hình thái học của từ trong ngữ cảnh tự nhiên.
- **Xử lý tối thiểu (Minimal Cleaning):**
  - Xóa bỏ các thẻ HTML rác nếu có (`<br />`, `<p>`).
  - Chuẩn hóa các khoảng trắng thừa.
  - Loại bỏ các dòng văn bản rỗng hoặc thiếu nhãn được phát hiện qua quy trình kiểm toán dữ liệu.

---

## 5. Kết quả kiểm toán dữ liệu & Phân tích độ dài token thực tế

### 5.1. Báo cáo kiểm toán dữ liệu thực tế (`artifacts/metrics/data_audit.json`)
* **Số mẫu ban đầu:** 20,000 dòng.
* **Số mẫu thiếu (Null text / label):** 0 dòng.
* **Số mẫu rỗng sau khi làm sạch:** 5 dòng.
* **Số mẫu có nhãn xung đột (Conflicting labels):** 127 dòng (từ 20 cụm văn bản trùng lặp nhưng gắn cả nhãn 0 và 1). Đã loại bỏ toàn bộ để tránh nhiễu.
* **Số mẫu trùng lặp văn bản (Exact duplicates):** 123 dòng. Đã loại bỏ để chống rò rỉ dữ liệu.
* **Tổng số mẫu bị loại:** 255 dòng.
* **Số mẫu hợp lệ duy nhất sau kiểm toán:** 19,745 dòng (9,921 Negative - 50.25%, 9,824 Positive - 49.75%).
* **Phân chia Stratified Split (seed=42):**
  - **Train set:** 13,821 mẫu (70.0%) | 6,945 Negative, 6,876 Positive.
  - **Validation set:** 1,975 mẫu (10.0%) | 992 Negative, 983 Positive.
  - **Test set:** 3,949 mẫu (20.0%) | 1,984 Negative, 1,965 Positive.
* **Kiểm tra rò rỉ (Zero Overlap):**
  - Giao thoa Train - Test: 0 mẫu.
  - Giao thoa Val - Test: 0 mẫu.
  - Giao thoa Train - Val: 0 mẫu.
  - Trạng thái: **Xác nhận 100% không rò rỉ dữ liệu (Zero Data Leakage).**

### 5.2. Thống kê độ dài token BERT thực tế (`artifacts/metrics/token_length_stats.json`)
*Phạm vi đo lường (Scope): Tập Train + Validation (15,796 mẫu) — Giữ tập Test độc lập, không dùng Test Set để quyết định siêu tham số.*
* **Mô hình Tokenizer:** `google-bert/bert-base-uncased` (WordPiece)
* **Giá trị nhỏ nhất (Min):** 3 tokens
* **Giá trị trung bình (Mean):** 42.33 tokens
* **Độ lệch chuẩn (Std):** 37.32 tokens
* **Trung vị (Median / p50):** 30.0 tokens
* **Phân vị 90 (p90):** 94.0 tokens
* **Phân vị 95 (p95):** 121.0 tokens
* **Phân vị 99 (p99):** 168.0 tokens
* **Giá trị lớn nhất (Max):** 425 tokens
* **Tỷ lệ cắt cụt tại 128 tokens:** **3.93%** (bảo toàn trọn vẹn 96.07% văn bản).
* **Tỷ lệ cắt cụt tại 256 tokens:** **0.09%** (bảo toàn trọn vẹn 99.91% văn bản).

### 5.3. Quyết định lựa chọn `MAX_LENGTH = 128`
Dựa trên số liệu đo lường thực tế và ràng buộc phần cứng (GPU 8GB VRAM):
1. **Đánh đổi cắt cụt (Truncation Tradeoff):** Với `p95 = 121` tokens, ngưỡng 128 đã bao phủ hơn 96% toàn bộ văn bản đánh giá. Việc nâng lên 256 chỉ giúp giữ thêm 3.84% văn bản nhưng làm tăng gấp 4 lần chi phí tính toán Attention $\mathcal{O}(L^2)$.
2. **Bộ nhớ & Thời gian tính toán:** Độ dài 128 với `batch_size = 16` tiêu tốn khoảng 4.5 GB VRAM ở chế độ FP16, hoàn toàn an toàn trên GPU 8GB mà không lo tràn bộ nhớ (OOM).
3. **Tính phù hợp với đồ án môn học:** Ngưỡng 128 là điểm cân bằng tối ưu giữa bảo toàn ngữ cảnh và tốc độ huấn luyện nhanh (~5-8 phút/3 epochs), thuận tiện cho việc tái lập trên máy tính sinh viên hoặc Google Colab T4.
