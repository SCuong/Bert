request_commit_sha: 0a47a1ea9f131da41d014457e5dc815ff89e4726
status: READY_FOR_REVIEW

# Summary
Đã hoàn thành toàn bộ các hạng mục công việc trong task `overnight-001` trước khi tiến hành thực nghiệm:
1. Chuẩn hóa entrypoints từ repository root theo định dạng package:
   - `python -m src.data`
   - `python -m src.train_baseline`
   - `python -m src.train_bert`
   - `python -m src.evaluate`
   - `python -m src.predict`
   - `python -m presentation.generate_presentation`
   - `streamlit run app/app.py`
2. Cập nhật `src/data.py`:
   - `__main__` chỉ thực hiện nạp/kiểm toán dữ liệu, kiểm tra rò rỉ split, phân tích độ dài token BERT thực tế và xuất biểu đồ/thống kê; tuyệt đối không huấn luyện mô hình.
   - Sử dụng `pd.to_numeric(df["label"], errors="raise").astype(int)` để xử lý nhãn sau khi đã drop missing, không double-count mẫu bị loại bỏ.
3. Cập nhật và kiểm chứng tương thích Hugging Face `Trainer`:
   - Xác thực `Trainer.__init__` của phiên bản thư viện hiện tại sử dụng tham số `processing_class` (tham số `tokenizer` đã bị deprecated/removed).
   - Code `src/train_bert.py` đã tương thích tự động qua `inspect.signature`.
4. Rà soát `src/train_bert.py`:
   - Quá trình training chỉ nạp và khởi tạo `train_ds` và `val_ds`; tập kiểm thử Test Set hoàn toàn không bị khởi tạo hay sử dụng trong training.
5. Kiểm soát `MAX_LENGTH = 128` như một candidate value; phân vị độ dài token (median, p90, p95, p99) và tỷ lệ cắt cụt tại 128 và 256 được cấu hình đo lường qua EDA trước khi chốt cấu hình chính thức.
6. Rà soát và chuẩn hóa toàn bộ văn phong trong tài liệu (`README.md`, `FINAL_REPORT.md`, `docs/PRE_EXPERIMENT_REVIEW.md`, `docs/03_old_bert_analysis.md`, `presentation/generate_presentation.py`):
   - Mô tả dữ liệu là "teacher-provided hotel-review sentiment dataset".
   - Phân tích marker phong cách Booking.com như đặc trưng hình thức, không khẳng định bản quyền.
   - Loại bỏ các tuyên bố KPI võ đoán trước thực nghiệm.
   - Thay thế các thuật ngữ "Clean-Room" bằng "triển khai độc lập mới hoàn toàn từ đầu; không tái sử dụng mã nguồn tham khảo (independent implementation from scratch; reference code was not reused)".
   - Thay "100% reproducible" bằng "tính tái lập có kiểm soát với fixed seed và tài liệu hóa môi trường (controlled for reproducibility with fixed seeds and documented environment)".
7. Đảm bảo trạng thái báo cáo và slide giữ nguyên ở mức tiền thực nghiệm (pre-experiment); `generate_presentation.py` có Fail-Fast Guard từ chối tạo slide chính thức nếu thiếu metrics thực tế.
8. Đảm bảo không có bất kỳ thực nghiệm huấn luyện mô hình hay đánh giá Test Set nào bị chạy trước phép.

# Verification
1. **Kiểm tra import module từ repository root:**
   - Lệnh: `python -c "import src.config; import src.data; import src.train_baseline; import src.train_bert; import src.evaluate; import src.predict; import presentation.generate_presentation; print('All modules imported successfully!')"`
   - Kết quả: `All modules imported successfully!` (Không gặp lỗi import từ `src`).
2. **Kiểm tra chữ ký tham số Hugging Face Trainer:**
   - Lệnh: `python -c "import inspect; from transformers import Trainer; params = inspect.signature(Trainer.__init__).parameters; print('processing_class:', 'processing_class' in params); print('tokenizer:', 'tokenizer' in params)"`
   - Kết quả: `processing_class: True`, `tokenizer: False` (Khớp hoàn toàn với implementation của nhóm).
3. **Kiểm tra Fail-Fast Guard của trình tạo Presentation:**
   - Lệnh: `python -m presentation.generate_presentation` (không kèm `--draft`)
   - Kết quả: Bắn ngoại lệ `RuntimeError: FAIL FAST GUARD: Không tìm thấy kết quả thực nghiệm thực tế...` đúng như thiết kế.
4. **Kiểm tra kiểm toán dữ liệu (Data Audit) trên synthetic edge cases:**
   - Xử lý chính xác null text, null label, empty text sau clean, conflicting labels và exact duplicate; tổng số mẫu loại bỏ khớp 100% không double-count.
5. **Kiểm tra trạng thái thực nghiệm:**
   - Không có artifact weights, metrics hoặc kết quả kiểm thử nào được sinh ra trước thời hạn.

# Files Changed
- `src/data.py`
- `README.md`
- `FINAL_REPORT.md`
- `docs/PRE_EXPERIMENT_REVIEW.md`
- `docs/03_old_bert_analysis.md`
- `presentation/generate_presentation.py`
- `docs/REVIEW_REQUEST.md`

# Known Issues
- Không có blocker. Hệ thống hoàn toàn sẵn sàng cho phase thực nghiệm tiếp theo.

# Proposed Next Phase
- Thực hiện Phase EDA & Baseline:
  1. Chạy `python -m src.data` để kiểm toán dữ liệu thực tế, đo lường phân vị độ dài token và xuất biểu đồ phân bố.
  2. Chạy `python -m src.train_baseline` để thiết lập mốc so sánh cơ sở (TF-IDF + Logistic Regression).
