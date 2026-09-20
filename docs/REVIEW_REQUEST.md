request_commit_sha: 48e69dac96c68f7ece6e58b717d46b82331280df
status: READY_FOR_REVIEW

# Summary of Provenance & Protocol Fixes
Đã hoàn thành toàn bộ các hạng mục công việc trong task `overnight-003`:

1. **Khắc phục triệt để tính tái lập của EDA JSON Artifacts (Source-Reproducible EDA):**
   - Cập nhật `src/data.py` để sinh đầy đủ các trường `selected_max_length`, `decision_rationale` cùng các giá trị làm tròn tường minh (`round(..., 2)` và `round(..., 1)`).
   - Tệp `artifacts/metrics/token_length_stats.json` giờ đây hoàn toàn do `python -m src.data` tự động sinh ra trực tiếp từ mã nguồn mà không cần chỉnh sửa thủ công (không manual post-editing).
   - Đã chạy kiểm chứng 2 lần liên tiếp `python -m src.data`: xác nhận nội dung file JSON sau lần chạy thứ hai hoàn toàn đồng nhất với lần chạy thứ nhất (`git diff` rỗng).

2. **Loại bỏ toàn bộ tuyên bố phần cứng chưa qua đo lường thực tế (Hardware Claims Removal):**
   - Đã rà soát và loại bỏ/viết lại toàn bộ các khẳng định chưa được đo lường thực nghiệm:
     - Xóa các con số ước lượng bộ nhớ `~4.5 GB VRAM`.
     - Xóa các khẳng định tuyệt đối `without OOM risk` / `an toàn tuyệt đối`.
     - Xóa mô tả không chính xác về Google Colab T4 như một GPU 8GB (chỉ nêu Colab GPU T4 hoặc môi trường phần cứng máy tính cá nhân RTX 5050 8GB).
   - Giữ lại đầy đủ cơ sở toán học lý thuyết: sequence length tăng từ 128 lên 256 làm tăng gấp 4 lần kích thước ma trận self-attention theo quy luật $\mathcal{O}(L^2)$ nhưng chỉ tăng thêm 3.84% độ phủ văn bản (p95 = 121.0 tokens, 3.93% truncation tại 128 so với 0.09% tại 256). Mức tiêu thụ bộ nhớ và thời gian thực thi thực tế sẽ được đo lường trực tiếp trong quá trình huấn luyện.

3. **Niêm phong tập kiểm thử (Sealed Test Set) trong giai đoạn phát triển:**
   - Cập nhật `src/train_baseline.py`:
     - Phân chia `train_df, val_df, _ = split_data(df, random_state=RANDOM_SEED)` - tập Test Set hoàn toàn không bị nạp, dự đoán hay đánh giá.
     - Huấn luyện TF-IDF + Logistic Regression trên Train Set và chỉ đánh giá phát triển trên Validation Set.
     - Lưu kết quả vào `artifacts/metrics/baseline_validation_metrics.json` và biểu đồ `artifacts/figures/baseline_val_confusion_matrix.png`.
     - Lưu mô hình tại `artifacts/model/baseline_tfidf_lr.joblib`.
   - Chuẩn hóa định nghĩa đường dẫn trong `src/config.py`:
     - Tách biệt rõ `BASELINE_VAL_METRICS_PATH`, `BASELINE_VAL_CM_PATH` (phát triển) với `BASELINE_TEST_METRICS_PATH`, `BASELINE_TEST_CM_PATH`, `BERT_TEST_METRICS_PATH`, `BERT_TEST_CM_PATH`, `COMPARATIVE_METRICS_PATH` (đánh giá cuối cùng).

4. **Chuẩn bị mô-đun đánh giá so sánh đối đầu cuối cùng (`src/evaluate.py`):**
   - Đã tái cấu trúc `src/evaluate.py` để đánh giá đồng thời cả mô hình Baseline (`baseline_tfidf_lr.joblib`) và mô hình Fine-Tuned BERT (`bert_best_model/`) trên cùng một tập Test Set độc lập trong cùng một lệnh chạy duy nhất.
   - Tích hợp **Fail-Fast Guard**: kiểm tra sự tồn tại của cả hai artifact mô hình; nếu thiếu một hoặc cả hai mô hình, chương trình lập tức báo lỗi `RuntimeError` và dừng ngay trước khi nạp dữ liệu hay chạm vào Test Set.
   - Không thực thi đánh giá Test Set trong phase này (chỉ kiểm chứng fail-fast guard khi thiếu mô hình).

5. **Đồng bộ hóa tài liệu và mã nguồn thuyết trình:**
   - Đã cập nhật `README.md`, `FINAL_REPORT.md`, `data/README.md`, `docs/02_project_spec.md`, `docs/PRE_EXPERIMENT_REVIEW.md`, `presentation/generate_presentation.py`, `presentation/presentation_outline.md`, `presentation/speaker_notes.md`.
   - Phân biệt rõ ràng giữa chỉ số validation (phát triển) và chỉ số test (đánh giá đối đầu cuối cùng).
   - Chuẩn hóa nguyên tắc bất biến của tập Test: không có bất kỳ nhãn, dự đoán hay chỉ số nào của Test Set được kiểm tra hoặc sử dụng cho việc ra quyết định mô hình/siêu tham số trước lượt đánh giá so sánh cuối cùng.

# Proof of EDA JSON Reproducibility
- Lệnh thực thi: `python -m src.data`
- Chạy lần 1: Sinh `artifacts/metrics/data_audit.json` và `artifacts/metrics/token_length_stats.json`.
- Chạy lần 2: `python -m src.data` thực thi thành công; `git diff artifacts/metrics/token_length_stats.json artifacts/metrics/data_audit.json` cho kết quả rỗng 100%.
- Toàn bộ các trường `candidate_max_length`, `selected_max_length`, `decision_rationale` và các giá trị phân vị làm tròn đều do chính mã nguồn `src/data.py` xuất ra.

# Confirmation of Hardware Claims Removal
- Đã loại bỏ tất cả các cụm `~4.5 GB VRAM`, `without OOM risk`, `an toàn tuyệt đối`, và không còn tài liệu nào mô tả Colab T4 là GPU 8GB.
- Tất cả tài liệu đều nêu rõ mức tiêu thụ bộ nhớ và thời gian thực thi sẽ được đo lường thực nghiệm trong pha huấn luyện mô hình.

# Confirmation of Test Set Sealing & Baseline Training
- `src/train_baseline.py` không chứa bất kỳ lời gọi hàm hay biến nào đánh giá trên Test Set.
- Đầu ra của `src/train_baseline.py` được cấu hình ghi vào `artifacts/metrics/baseline_validation_metrics.json` và `artifacts/figures/baseline_val_confusion_matrix.png`.
- Chưa thực thi huấn luyện Baseline hay BERT trong phase này; không có file metrics hay weights nào bị tạo giả mạo.

# Prepared Comparative Evaluator (`src/evaluate.py`)
- Cơ chế hoạt động:
  1. Kiểm tra fail-fast: nếu thiếu `artifacts/model/baseline_tfidf_lr.joblib` hoặc `artifacts/model/bert_best_model`, ném lỗi `RuntimeError` ngay lập tức.
  2. Nạp dữ liệu và trích xuất tập `test_df` (3,949 mẫu).
  3. Đánh giá Baseline trên Test Set, lưu `artifacts/metrics/baseline_test_metrics.json` và `artifacts/figures/baseline_test_confusion_matrix.png`.
  4. Đánh giá BERT trên Test Set, lưu `artifacts/metrics/bert_test_metrics.json`, `artifacts/figures/bert_test_confusion_matrix.png` và trích xuất 20 ca lỗi vào `artifacts/metrics/error_cases.json`.
  5. Xuất bảng so sánh đối đầu tổng hợp vào `artifacts/metrics/comparative_metrics.json` và in bảng đối chiếu console.
- Mô-đun đã được kiểm chứng tính sẵn sàng và fail-fast, nhưng **CHƯA ĐƯỢC CHẠY** trên dữ liệu thực nghiệm.

# Verification Commands Actually Run
1. `python -m src.data`: Thành công, sinh đầy đủ metrics và figures.
2. `python -m src.data` (lần 2): Xác nhận tính tái lập 100% không đổi.
3. `python -m src.evaluate`: Kích hoạt thành công Fail-Fast Guard với thông báo lỗi:
   `RuntimeError: FAIL-FAST GUARD: Không thể thực thi đánh giá trên Test Set vì thiếu artifact mô hình:`
   `- Baseline model not found at: A:\Bert\artifacts\model\baseline_tfidf_lr.joblib`
   `- BERT best model directory not found at: A:\Bert\artifacts\model\bert_best_model`
4. `python -c "import src.config, src.data, src.train_baseline, src.evaluate"`: Exit code 0, không có lỗi cú pháp hay import.
5. `git status`: Xác nhận không có metrics, weights hay kết quả huấn luyện nào bị tạo giả mạo.

# Files Changed
- `src/config.py`: Khai báo các đường dẫn metrics/figures tách biệt cho validation và test; cập nhật ghi chú MAX_LENGTH.
- `src/data.py`: Cập nhật `stats_dict` sinh đầy đủ các trường và làm tròn tường minh trong `token_length_stats.json`.
- `src/train_baseline.py`: Chuyển phạm vi đánh giá sang Validation Set only; niêm phong tập Test Set; lưu `baseline_validation_metrics.json`.
- `src/evaluate.py`: Tái cấu trúc thành bộ đánh giá đối đầu cả Baseline và BERT trên Test Set với Fail-Fast Guard.
- `artifacts/metrics/token_length_stats.json`: Được tái sinh hoàn toàn từ `src/data.py`.
- `README.md`: Cập nhật hướng dẫn chạy `train_baseline` (validation) và `evaluate` (test); loại bỏ các ước lượng phần cứng chưa đo lường.
- `data/README.md`: Cập nhật nguyên tắc bất biến của Test Set và cơ sở kỹ thuật lựa chọn MAX_LENGTH.
- `docs/02_project_spec.md`: Cập nhật tiêu chí thành công, sơ đồ quy trình Mermaid và ràng buộc MAX_LENGTH.
- `docs/PRE_EXPERIMENT_REVIEW.md`: Cập nhật trạng thái các khâu và danh sách tệp chưa runtime-verified.
- `FINAL_REPORT.md`: Cập nhật Mục 2, 3, 7, 10 phản ánh quy trình mới và lý giải MAX_LENGTH.
- `presentation/generate_presentation.py`: Cập nhật Slide 5, Slide 7 và Slide 11.
- `presentation/presentation_outline.md`: Cập nhật Slide 5, Slide 7 và Slide 11.
- `presentation/speaker_notes.md`: Cập nhật kịch bản thuyết trình Slide 5, Slide 6, Slide 7.

# Known Issues
- Không có blocker. Quy trình kiểm soát tính toàn vẹn của dữ liệu và niêm phong tập Test đã được củng cố hoàn toàn.

# Proposed Next Phase
- **Phase Baseline Training (`python -m src.train_baseline`):**
  - Huấn luyện mô hình TF-IDF + Logistic Regression trên Train Set (13,821 mẫu).
  - Đánh giá phát triển trên Validation Set (1,975 mẫu).
  - Lưu mô hình tại `artifacts/model/baseline_tfidf_lr.joblib` và metrics tại `artifacts/metrics/baseline_validation_metrics.json`.
  - Giữ nguyên niêm phong tập Test Set cho đến khi hoàn tất huấn luyện BERT.
