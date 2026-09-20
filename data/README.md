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
