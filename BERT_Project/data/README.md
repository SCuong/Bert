# Hướng Dẫn & Đặc Tả Dữ Liệu: Hotel Reviews Sentiment Dataset

## 1. Nguồn gốc dữ liệu (Data Provenance)
- **Tập dữ liệu sử dụng:** `dts_20k_raw.csv` do giảng viên cung cấp trong thư mục `Bài giảng/AI.Code/NLP_Demo/dts_20k_raw.csv`.
- **Nguồn gốc thực tế:** Dữ liệu được trích xuất từ tập dữ liệu công khai trên Kaggle (*"515K Hotel Reviews Data in Europe"*, thu thập từ nền tảng đặt phòng Booking.com). 
- **Cấu trúc đặc thù:** Trong khảo sát của Booking.com, khách hàng được yêu cầu điền vào hai trường độc lập:
  1. *Negative Review:* Nhận xét tiêu cực (nếu không có phàn nàn gì, người dùng thường điền cụm mặc định `"No Negative"`).
  2. *Positive Review:* Nhận xét tích cực (nếu không có lời khen nào, người dùng thường điền cụm mặc định `"No Positive"`).
  Khi hai trường này được ghép nối lại để tạo thành văn bản hoàn chỉnh, cụm từ `"No Negative"` xuất hiện phổ biến ở đầu các nhận xét tích cực.

---

## 2. Thông số & Phân bố dữ liệu

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Tổng số dòng** | 20,000 mẫu |
| **Số cột (Schema)** | 2 cột: `text` (văn bản đánh giá), `label` (nhãn nhị phân) |
| **Số mẫu Positive (1)** | 10,000 mẫu (50.0%) |
| **Số mẫu Negative (0)** | 10,000 mẫu (50.0%) |
| **Độ cân bằng nhãn** | Cân bằng hoàn hảo (1:1) |
| **Dòng trống (Missing values)** | 5 dòng trong tệp thô có văn bản rỗng hoặc chỉ chứa khoảng trắng |

---

## 3. Chiến lược phân chia dữ liệu (Data Splitting Strategy)

Nhằm đảm bảo tính khoa học và ngăn chặn hoàn toàn hiện tượng rò rỉ dữ liệu (Data Leakage):
- **Tỷ lệ phân chia:**
  - **Train set:** 70% (14,000 mẫu) — Dùng để huấn luyện mô hình.
  - **Validation set:** 10% (2,000 mẫu) — Dùng để chọn checkpoint tốt nhất, theo dõi loss và tránh overfitting.
  - **Test set:** 20% (4,000 mẫu) — Tập kiểm thử độc lập, chỉ được nạp đúng một lần khi đánh giá mô hình cuối cùng.
- **Phương pháp phân chia:** `StratifiedShuffleSplit` từ thư viện `scikit-learn` nhằm bảo toàn tuyệt đối tỷ lệ cân bằng 50/50 của hai nhãn ở cả 3 tập.
- **Random Seed:** Cố định `seed = 42` xuyên suốt tất cả các thực nghiệm để đảm bảo 100% tính tái lập (reproducibility).

---

## 4. Nguyên tắc tiền xử lý (Preprocessing Principles)

Khác với quy trình NLP cổ điển trong `Preprocessing_and_Visualizing.ipynb` của sinh viên khóa trước:
- **KHÔNG xóa stopwords:** Trong bài toán cảm xúc, các stopword như *"not"*, *"no"*, *"never"*, *"but"*, *"very"* mang thông tin ngữ nghĩa quyết định (ví dụ: *"not good"* khác hoàn toàn *"good"*).
- **KHÔNG lemmatize cả câu:** Mô hình BERT sử dụng thuật toán tách từ con (WordPiece Tokenization) và có ma trận nhúng vị trí (Positional Embeddings), có khả năng tự động xử lý các biến thể hình thái học của từ trong ngữ cảnh tự nhiên.
- **Xử lý tối thiểu (Minimal Cleaning):**
  - Xóa bỏ các thẻ HTML rác nếu có (`<br />`, `<p>`).
  - Chuẩn hóa các khoảng trắng thừa.
  - Loại bỏ 5 dòng văn bản rỗng trong tập thô để tránh lỗi khi nạp vào DataLoader.
