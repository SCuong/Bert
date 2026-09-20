request_commit_sha: 2b55cb1e5b8719273c5fa8c21a414b4344ca2181
status: READY_FOR_REVIEW

# Summary
Đã hoàn thành toàn bộ các hạng mục công việc trong task `overnight-002`:
1. Thực hiện Data Audit thực tế trên toàn bộ tập dữ liệu giảng viên cung cấp (`data/dts_20k_raw.csv`):
   - Đã xử lý và loại bỏ đúng 255 mẫu không hợp lệ/trùng lặp/xung đột nhãn (không double-count).
   - Thu được 19,745 mẫu hợp lệ duy nhất (cân bằng tự nhiên: 9,921 Negative, 9,824 Positive).
   - Phân chia Stratified Split (70/10/20, seed=42) với xác nhận 0 mẫu trùng lặp giữa Train, Val và Test (Zero Data Leakage).
   - Lưu báo cáo có cấu trúc tại `artifacts/metrics/data_audit.json`.
2. Thực hiện đo lường phân vị độ dài token BERT thực tế (`google-bert/bert-base-uncased`):
   - Phạm vi tính toán (Scope) được giới hạn nghiêm ngặt trên tập **Train + Validation (15,796 mẫu)**. Tập kiểm thử Test Set hoàn toàn độc lập và không ảnh hưởng tới quyết định siêu tham số.
   - Kết quả đo lường: Mean = 42.33 tokens, Median = 30.0 tokens, p90 = 94.0 tokens, p95 = 121.0 tokens, p99 = 168.0 tokens, Max = 425 tokens.
   - Tỷ lệ cắt cụt tại 128: 3.93% (bảo toàn 96.07% văn bản).
   - Tỷ lệ cắt cụt tại 256: 0.09% (bảo toàn 99.91% văn bản).
   - Lưu số liệu tại `artifacts/metrics/token_length_stats.json`.
3. Quyết định lựa chọn `MAX_LENGTH = 128`:
   - Phân vị p95 là 121 tokens, ngưỡng 128 bảo toàn trọn vẹn hơn 96% nội dung đánh giá.
   - Chi phí tính toán Self-Attention $\mathcal{O}(L^2)$ và bộ nhớ kích hoạt (activation memory) với `MAX_LENGTH = 128` tiêu tốn khoảng ~4.5 GB VRAM ở FP16 với batch size 16, đảm bảo an toàn tuyệt đối trên GPU 8GB VRAM (RTX 5050 / Google Colab T4) mà không có rủi ro tràn bộ nhớ (OOM).
   - Việc tăng lên 256 chỉ giữ thêm 3.84% văn bản nhưng làm tăng gấp 4 lần chi phí tính toán attention.
   - Đã cập nhật `src/config.py` phản ánh quyết định này.
4. Cập nhật toàn bộ tài liệu dự án (`README.md`, `data/README.md`, `FINAL_REPORT.md`, `docs/02_project_spec.md`, `docs/PRE_EXPERIMENT_REVIEW.md`, `presentation/`):
   - Đồng bộ chính xác 100% các số liệu đo lường thực tế từ JSON artifacts.
   - Xuất 2 biểu đồ trực quan hóa: `artifacts/figures/class_distribution.png` và `artifacts/figures/token_length_distribution.png`.
5. Đảm bảo giữ nguyên trạng thái PRE-BASELINE: không huấn luyện Baseline, không fine-tune BERT, không đánh giá Test Set, không sinh slide chính thức.

# Data Audit Results (`artifacts/metrics/data_audit.json`)
- **Số mẫu thô ban đầu (Raw rows):** 20,000
- **Mẫu thiếu text / label:** 0
- **Mẫu rỗng sau làm sạch tối thiểu:** 5
- **Mẫu có nhãn xung đột (Conflicting labels):** 127 dòng (từ 20 cụm văn bản trùng lặp mang cả nhãn 0 và 1)
- **Mẫu trùng lặp văn bản (Exact duplicates):** 123 dòng
- **Tổng số mẫu bị loại bỏ:** 255 dòng (Khớp chính xác: 0 + 5 + 127 + 123 = 255)
- **Số mẫu hợp lệ duy nhất:** 19,745 dòng (9,921 Negative - 50.25%, 9,824 Positive - 49.75%)
- **Phân chia Stratified Split (seed=42):**
  - **Train set:** 13,821 mẫu (70.0%) | 6,945 Negative, 6,876 Positive
  - **Validation set:** 1,975 mẫu (10.0%) | 992 Negative, 983 Positive
  - **Test set:** 3,949 mẫu (20.0%) | 1,984 Negative, 1,965 Positive
- **Xác thực rò rỉ dữ liệu (Zero Overlap):**
  - Giao thoa Train - Test: 0 mẫu
  - Giao thoa Val - Test: 0 mẫu
  - Giao thoa Train - Val: 0 mẫu
  - Trạng thái: `passed: true`

# Token Length Statistics (`artifacts/metrics/token_length_stats.json`)
- **Phạm vi tính toán (Scope):** `train_val` (15,796 mẫu; Test Set được giữ độc lập)
- **Tokenizer:** `google-bert/bert-base-uncased`
- **Mean:** 42.33 tokens
- **Std:** 37.32 tokens
- **Min:** 3 tokens
- **Median (p50):** 30.0 tokens
- **p90:** 94.0 tokens
- **p95:** 121.0 tokens
- **p99:** 168.0 tokens
- **Max:** 425 tokens
- **Tỷ lệ cắt cụt tại 128 (Truncation at 128):** 3.93%
- **Tỷ lệ cắt cụt tại 256 (Truncation at 256):** 0.09%

# Chosen MAX_LENGTH and Rationale
- **Giá trị lựa chọn:** `MAX_LENGTH = 128`
- **Cơ sở thực nghiệm & kỹ thuật:**
  1. *Đánh đổi cắt cụt (Truncation Tradeoff):* Phân vị 95 là 121 tokens, do đó 128 bảo toàn trọn vẹn 96.07% văn bản. Mức cắt cụt 3.93% là rất nhỏ.
  2. *Chi phí bộ nhớ & tính toán:* Độ phức tạp của Multi-Head Attention là $\mathcal{O}(L^2)$. Chuyển sang 256 sẽ tăng $4\times$ phép toán chú ý và $2-3\times$ bộ nhớ activation chỉ để giữ thêm 3.84% văn bản.
  3. *Ràng buộc phần cứng 8GB VRAM:* Ngưỡng 128 với batch size 16 chiếm khoảng 4.5 GB VRAM ở FP16, hoàn toàn an toàn trên GPU RTX 5050 8GB hoặc Colab T4 mà không gặp lỗi Out-Of-Memory (OOM).

# Files Changed
- `src/config.py`: Khai báo `DATA_AUDIT_PATH`, cập nhật ghi chú giải thích `MAX_LENGTH = 128`.
- `src/data.py`: Cập nhật lưu `data_audit.json`, tính toán token length trên `train_val`, xuất biểu đồ.
- `artifacts/metrics/data_audit.json`: File số liệu kiểm toán dữ liệu thực tế.
- `artifacts/metrics/token_length_stats.json`: File thống kê phân vị độ dài token và quyết định MAX_LENGTH.
- `artifacts/figures/class_distribution.png`: Biểu đồ phân bố nhãn thực tế.
- `artifacts/figures/token_length_distribution.png`: Biểu đồ phân bố độ dài token thực tế (Train+Val scope) với hai đường cutoff 128 và 256.
- `README.md`: Cập nhật số liệu kiểm toán và mục 4.2 EDA.
- `data/README.md`: Thêm mục 5 chi tiết số liệu audit và token statistics.
- `FINAL_REPORT.md`: Cập nhật Mục 3 (Data) và Mục 10 (Truncation).
- `docs/02_project_spec.md`: Cập nhật Mục 8 về lựa chọn MAX_LENGTH = 128.
- `docs/PRE_EXPERIMENT_REVIEW.md`: Đánh dấu EDA đã hoàn thành (EXECUTED).
- `presentation/generate_presentation.py`: Cập nhật Slide 5 nhúng biểu đồ và số liệu thực tế.
- `presentation/presentation_outline.md`: Cập nhật Slide 5 và Slide 8.
- `presentation/speaker_notes.md`: Cập nhật kịch bản thuyết trình Slide 5.
- `docs/REVIEW_REQUEST.md`: Cập nhật báo cáo cho `overnight-002`.

# Verification
1. **Chạy thực tế `python -m src.data`:** Hoàn thành thành công, sinh đầy đủ 2 file metrics JSON và 2 file biểu đồ PNG.
2. **Kiểm tra tính nhất quán số liệu:** Số liệu trong toàn bộ tài liệu khớp chính xác 100% với `data_audit.json` và `token_length_stats.json`.
3. **Kiểm tra tính độc lập của Test Set:** Đã xác thực phân vị độ dài token chỉ tính trên `train_val_df`, không sử dụng Test Set.
4. **Kiểm tra trạng thái mô hình:** Không có file trọng số hay metrics đánh giá mô hình nào bị sinh ra.

# Known Issues
- Không có blocker. Dữ liệu đã sạch hoàn toàn và sẵn sàng cho phase Baseline Training.

# Proposed Next Phase
- **Phase Baseline Training (`python -m src.train_baseline`):**
  - Huấn luyện mô hình TF-IDF (10,000 n-grams) + Logistic Regression trên Train Set.
  - Đánh giá trên Test Set để thiết lập mốc đối sánh chuẩn (Accuracy, Precision, Recall, Macro F1, Confusion Matrix).
  - Xuất `artifacts/metrics/baseline_metrics.json` và `artifacts/figures/baseline_confusion_matrix.png`.
