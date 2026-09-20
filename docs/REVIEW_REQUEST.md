request_commit_sha: 2a8a407627a56541b86053a98ec2973fe8127cbe
status: READY_FOR_REVIEW

# Summary of Split-Sealing & EDA-Rationale Fixes
Đã hoàn thành toàn bộ các yêu cầu của task `overnight-004`:

1. **Sinh tự động `decision_rationale` từ số liệu đo lường thực tế (Data-Derived Rationale):**
   - Đã loại bỏ hoàn toàn các giá trị hard-coded (`96.07%`, `121.0`, `3.93%`, `3.84%`) trong `decision_rationale` tại `src/data.py`.
   - Chuỗi giải thích hiện được sinh động trực tiếp từ các biến đã tính toán trong `stats_dict` (`MAX_LENGTH`, `pct_preserved_128`, `p95_val`, `pct_truncated_128`, `coverage_gain_256`).
   - Đã chạy kiểm chứng 2 lần liên tiếp `python -m src.data`: xác nhận `artifacts/metrics/token_length_stats.json` bảo toàn 100% số liệu thực nghiệm đã duyệt và cho `git diff` rỗng.

2. **Niêm phong triệt để việc in ấn/báo cáo thông tin Test Set trong quá trình huấn luyện (Fully Sealed Test-Set Reporting):**
   - Bổ sung tham số `verbose_test: bool = False` vào hàm `split_data()` trong `src/data.py`. Khi ở chế độ mặc định (hoặc khi gọi qua `get_train_val_split()`), hàm chỉ in:
     `Test set:  [SEALED — Held out for final evaluation]`
     Tuyệt đối không in số lượng mẫu hay phân bố nhãn của tập Test.
   - Thêm hàm `get_train_val_split(df)` chuyên biệt cho pha phát triển, chỉ trả về `(train_df, val_df)`.
   - Cập nhật cả `src/train_baseline.py` và `src/train_bert.py` sử dụng `get_train_val_split(df)`.
   - Giữ nguyên việc in đầy đủ thông tin Test Set khi chạy standalone EDA/Audit (`python -m src.data`) hoặc khi đánh giá so sánh cuối cùng (`python -m src.evaluate`) qua cờ `verbose_test=True`.

3. **Huấn luyện thực tế mô hình Baseline trên Train Set & Đánh giá trên Validation Set (Validation-Only Baseline):**
   - Đã chạy thực tế: `python -m src.train_baseline`.
   - Mô hình TF-IDF (10,000 n-grams) + Logistic Regression (C=1.0, L-BFGS, seed=42) được huấn luyện trên 13,821 mẫu Train.
   - Đánh giá phát triển độc lập trên 1,975 mẫu Validation.
   - Lưu trữ đầy đủ kết quả đo lường vào `artifacts/metrics/baseline_validation_metrics.json` và biểu đồ ma trận nhầm lẫn vào `artifacts/figures/baseline_val_confusion_matrix.png`.
   - Mô hình huấn luyện được lưu tại `artifacts/model/baseline_tfidf_lr.joblib` và được xác nhận đã bị Git bỏ qua (Git-ignored) theo `.gitignore`.
   - Không có bất kỳ hyperparameter nào bị tinh chỉnh sau khi có kết quả Validation; đây là mốc đối sánh tham chiếu cố định.

# Exact Baseline Validation Metrics (`artifacts/metrics/baseline_validation_metrics.json`)
- **Evaluation Split:** `validation`
- **Validation Sample Count:** 1,975
- **Accuracy:** 81.01% (`0.810126582278481`)
- **Macro Precision:** 0.8116 (`0.8115951441377918`)
- **Macro Recall:** 0.8100 (`0.8099680454828865`)
- **Macro F1-Score:** 0.8098 (`0.8098450029770088`)
- **Weighted F1-Score:** 0.8099 (`0.8098783478942885`)
- **Class 0 (Negative):**
  - Precision: 0.7913 (`0.7913125590179415`)
  - Recall: 0.8448 (`0.844758064516129`)
  - F1-Score: 0.8172 (`0.8171623598244758`)
- **Class 1 (Positive):**
  - Precision: 0.8319 (`0.8318777292576419`)
  - Recall: 0.7752 (`0.775178026449644`)
  - F1-Score: 0.8025 (`0.8025276461295419`)
- **Training Time:** 0.68 giây (`0.676741361618042` s)
- **Validation Inference Time:** 0.114 giây (`0.11364960670471191` s) — Tốc độ xử lý: ~17,378 mẫu/giây

# Confusion-Matrix Consistency Check
- **Ma trận nhầm lẫn (Validation):**
  - True Negatives (TN): 838
  - False Positives (FP): 154
  - False Negatives (FN): 221
  - True Positives (TP): 762
- **Kiểm tra tổng số mẫu:**
  - Hàng 0 (Negative support): 838 + 154 = 992 (khớp chính xác số lượng nhãn 0 trong tập Validation)
  - Hàng 1 (Positive support): 221 + 762 = 983 (khớp chính xác số lượng nhãn 1 trong tập Validation)
  - Tổng số mẫu ma trận: 992 + 983 = 1,975 (khớp 100% với `validation_sample_count = 1975`).
  - Trạng thái: `passed: true`.

# Confirmation of Local Model & Git Ignore
- Tệp mô hình `artifacts/model/baseline_tfidf_lr.joblib` tồn tại cục bộ trên đĩa (`Test-Path` trả về `True`).
- Tệp mô hình được loại trừ thông qua quy tắc `*.joblib` và `artifacts/model/*` trong `.gitignore`.
- Xác nhận `git status` không hiển thị tệp này trong danh sách tracked/untracked files.

# Confirmation of Sealed Test Set & No Final Test Artifacts
- Xác nhận không có tệp nào sau đây được sinh ra hoặc tồn tại trong workspace:
  - Không có `baseline_test_metrics.json`
  - Không có `bert_test_metrics.json`
  - Không có `comparative_metrics.json`
  - Không có `error_cases.json` từ final evaluation
- Toàn bộ kết quả mới được dán nhãn rõ ràng là kết quả đánh giá trên tập **Validation** trong giai đoạn phát triển, không được trình bày như kết quả Test cuối cùng.
- Không đưa ra bất kỳ nhận định nào về việc BERT vượt trội hay kém hơn Baseline trong giai đoạn này.

# Verification Commands Actually Run
1. `python -m src.data`: Chạy thành công, sinh `token_length_stats.json` với rationale tính toán động.
2. `python -m src.data` (lần 2): Xác nhận tính tái lập 100% (`git diff` rỗng).
3. `python -c "from src.data import load_and_validate_data, get_train_val_split; df = load_and_validate_data(); train_df, val_df = get_train_val_split(df)"`: Xác nhận chỉ in `Test set: [SEALED — Held out for final evaluation]`, không để lộ số lượng mẫu hay phân bố nhãn của Test Set.
4. `python -m src.train_baseline`: Huấn luyện thành công, lưu metrics validation và confusion matrix.
5. `Test-Path A:\Bert\artifacts\model\baseline_tfidf_lr.joblib`: Trả về `True`.
6. `git status`: Xác nhận mô hình bị Git-ignore và chỉ có các artifacts validation được đưa vào tracking.

# Files Changed
- `src/data.py`: Sinh `decision_rationale` tự động từ `stats_dict`; thêm cờ `verbose_test` và hàm `get_train_val_split`.
- `src/train_baseline.py`: Sử dụng `get_train_val_split`, huấn luyện và đánh giá trên Validation Set.
- `src/train_bert.py`: Cập nhật sử dụng `get_train_val_split` để niêm phong Test Set trong giai đoạn huấn luyện.
- `src/evaluate.py`: Truyền tường minh `verbose_test=True` khi gọi `split_data`.
- `artifacts/metrics/baseline_validation_metrics.json`: Tệp metrics thực nghiệm thực tế trên tập Validation.
- `artifacts/figures/baseline_val_confusion_matrix.png`: Biểu đồ ma trận nhầm lẫn trên tập Validation.
- `README.md`: Bổ sung kết quả Baseline Validation thực tế tại Mục 4.3.
- `FINAL_REPORT.md`: Cập nhật Mục 4.1 với số liệu Baseline Validation thực tế.
- `docs/PRE_EXPERIMENT_REVIEW.md`: Cập nhật trạng thái Baseline Training & Validation Evaluation thành `ĐÃ THỰC THI (EXECUTED)`.
- `presentation/generate_presentation.py`: Nạp và hiển thị `BASELINE_VAL_METRICS_PATH` trên Slide 7.
- `presentation/presentation_outline.md`: Cập nhật Slide 7 với kết quả Baseline Validation.
- `presentation/speaker_notes.md`: Cập nhật kịch bản thuyết trình Slide 7 với kết quả Baseline Validation.

# Known Issues
- Không có blocker. Baseline reference đã được thiết lập vững chắc, sẵn sàng cho pha fine-tuning BERT.

# Proposed Next Phase
- **Phase BERT Fine-Tuning (`python -m src.train_bert`):**
  - Fine-tune mô hình `google-bert/bert-base-uncased` (AdamW, lr=2e-5, batch_size=16, max_length=128, 3 epochs) trên tập Train Set (13,821 mẫu).
  - Giám sát Train Loss và Validation Loss qua từng epoch; tự động chọn checkpoint có Validation Macro F1 tốt nhất lưu tại `artifacts/model/bert_best_model`.
  - Xuất biểu đồ quá trình học tập tại `artifacts/figures/training_history.png` và lịch sử tại `artifacts/metrics/bert_training_history.json`.
  - Tiếp tục giữ nguyên niêm phong tập Test Set cho đến khi hoàn tất huấn luyện BERT.
