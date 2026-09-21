# REVIEW REQUEST

request_commit_sha: e3a4fbca3927732a04c522fafbd0497a173d167a
status: READY_FOR_REVIEW

## Executive Summary

Phase `overnight-007` đã hoàn thành toàn diện việc khảo sát định tính dựa trên bằng chứng (evidence-based qualitative analysis) đối với **20 ca dự đoán sai có độ tin cậy cao nhất** của mô hình BERT trên tập Test Set độc lập (10 False Positives và 10 False Negatives) từ `artifacts/metrics/error_cases.json`.
- **Nguyên tắc bất biến:** Tuyệt đối không chạy lại Test evaluation, không retrain, không tinh chỉnh siêu tham số và không thay đổi bất kỳ artifact mô hình hay kết quả Test đã đóng băng.
- **Sản phẩm hoàn thành:** Đã hoàn thiện báo cáo phân tích học thuật `docs/04_error_analysis.md` và tệp tổng hợp máy đọc `artifacts/metrics/error_analysis_summary.json`.

---

## Qualitative Methodology & Analysis Scope

1. **Phạm vi khảo sát:** 20 ca lỗi cực đoan (highest-confidence errors) được trích xuất từ 599 ca lỗi của BERT trên Test Set (3,949 mẫu). Đây là mẫu có chủ đích nhằm mổ xẻ các trường hợp biên và hạn chế sâu nhất, không phải mẫu ngẫu nhiên đại diện cho toàn bộ 599 ca lỗi.
2. **Đo lường độ dài token:** Sử dụng đúng tokenizer đã đóng băng `AutoTokenizer.from_pretrained(BERT_BEST_MODEL_DIR)` để đo độ dài token thực tế của từng ca (dao động từ 6 đến 126 tokens).
3. **Phân loại nguyên nhân khách quan:** Phân loại dựa trên bằng chứng văn bản thực tế, không gượng ép vào các giả định định kiến (không gán nhãn sarcasm khi văn bản không hỗ trợ; phân định rõ giữa lỗi suy luận mô hình, cảm xúc pha trộn và nghi vấn nhiễu nhãn).

---

## Category Counts & Truncation Statistics

Thống kê tổng hợp từ 20 ca khảo sát (dữ liệu máy đọc tại `artifacts/metrics/error_analysis_summary.json`):

- **Tổng số ca khảo sát:** 20 ca (10 False Positives, 10 False Negatives).
- **Số ca bị cắt cụt văn bản (`token_length > 128`):** **0 / 20 ca** (0.0%). Mọi ca lỗi cực đoan đều nằm trọn vẹn trong ngưỡng 128 tokens.
- **Phân bố các nhóm nguyên nhân ngôn ngữ & dữ liệu:**
  - `mixed sentiment / competing clauses`: **15 / 20 ca** (75.0%)
  - `possible label ambiguity or label noise`: **8 / 20 ca** (40.0%)
  - `negation or concessive structure`: **8 / 20 ca** (40.0%)
  - `template/source marker effects`: **6 / 20 ca** (30.0%)
  - `noisy grammar, spelling, or malformed text`: **4 / 20 ca** (20.0%)
  - `domain/platform complaint versus hotel sentiment`: **2 / 20 ca** (10.0%)
  - `plausible model reasoning failure`: **1 / 20 ca** (5.0%)

---

## Key Observations

### 1. Nhóm False Positive (Thực tế: 0, Dự đoán: 1, 10 ca)
- Phần lớn văn bản chứa cảm xúc tích cực áp đảo (khen ngợi phòng ốc, nhân viên, vị trí) nhưng chỉ kèm một phàn nàn nhỏ (ví dụ: phí đỗ xe ở Case 01, cần sơn mới ở Case 06, thiếu tủ lạnh ở Case 08). Mô hình tập trung vào mật độ từ tích cực dày đặc nên dự đoán nhãn 1.
- Case 02 hoàn toàn là văn bản khen ngợi không có từ tiêu cực nào; Case 03 là tàn dư ghép nối form khảo sát (*"nothing everything was excellent"*), thể hiện sự không tương thích giữa nội dung và nhãn 0.

### 2. Nhóm False Negative (Thực tế: 1, Dự đoán: 0, 10 ca)
- Khách hàng phàn nàn rất gay gắt về những trải nghiệm tồi tệ (mùi hôi ở Case 11, giá cả cắt cổ ở Case 13, tivi hỏng 5 ngày ở Case 19). Văn bản chứa cảm xúc tiêu cực rõ rệt khiến mô hình tự tin dự đoán nhãn 0 ($>99.3\%$).
- 4/10 ca FN (Case 12, 13, 17, 19) kết thúc bằng thẻ `"No Positive"`, phản ánh việc người dùng bỏ trống ô đánh giá tích cực trên nền tảng đặt phòng. Nhãn 1 trong dataset cho thấy khả năng cao bị lỗi đảo nhãn hoặc lỗi thu thập dữ liệu.
- **Lỗi suy luận ngữ cảnh thực sự (Case 16):** Tác giả trích dẫn lời bạn bè chê khách sạn cũ rồi tuyên bố phản bác (*"They saw it as an old hotel... I disagree. The service was great"*). Mô hình chưa phân biệt được quan điểm được trích dẫn (attributed view) và lập trường của tác giả (author's stance).

### 3. Nhận Định Về Chất Lượng Dữ Liệu & Tính Mơ Hồ Của Nhãn (Với Ngôn Ngữ Thận Trọng)
- Bằng chứng văn bản cho thấy một tỷ lệ đáng kể (ước tính 6 đến 8 ca trong 20 ca khảo sát) có sự mâu thuẫn rõ rệt giữa ngữ nghĩa tự nhiên và nhãn nhị phân trong dataset. Mặc dù không thể khẳng định chắc chắn 100% ý định ban đầu của người dùng nếu không có dữ liệu gốc đầy đủ, nhưng sự tồn tại của các dấu hiệu biểu mẫu (`"No Positive"`, phàn nàn nền tảng Booking.com) chỉ ra rằng một phần các ca lỗi tự tin nhất của BERT thực chất phản ánh sự bất cập của việc gán nhãn nhị phân trên văn bản đa khía cạnh (Aspect-Based Reviews) hơn là sự yếu kém trong khả năng hiểu ngôn ngữ của mô hình.

---

## Verification & Integrity Checklist

- [x] Đầy đủ 20 ca lỗi từ `error_cases.json` được khảo sát chi tiết (Case 01 đến Case 20).
- [x] Số lượng 10 FP và 10 FN được phân định chính xác.
- [x] Độ dài token được đo lường bằng tokenizer đóng băng của BERT (`AutoTokenizer.from_pretrained(BERT_BEST_MODEL_DIR)`).
- [x] Khẳng định không có ca nào bị cắt cụt vì toàn bộ độ dài token $\le 128$.
- [x] Thống kê phân nhóm khớp chính xác 100% giữa bảng phân tích và tệp `error_analysis_summary.json`.
- [x] Không có lệnh huấn luyện, tinh chỉnh hoặc dự đoán Test Set nào được thực thi.
- [x] Toàn bộ trọng số mô hình và kết quả thực nghiệm Test Set được giữ nguyên vẹn 100%.

---

## Files Changed

- `docs/04_error_analysis.md`: Báo cáo phân tích định tính ca lỗi chuyên sâu (bảng 20 ca, thống kê phân nhóm, so sánh FP/FN, nhận định cắt cụt, chất lượng dữ liệu và câu trả lời cho RQ3).
- `artifacts/metrics/error_analysis_summary.json`: Tệp JSON tổng hợp có cấu trúc, chứa đầy đủ các trường máy đọc cho từng ca và số lượng thống kê phân nhóm.

---

## Known Issues

- Không có blocker. Bằng chứng định tính đã sẵn sàng cho giai đoạn đóng gói tài liệu báo cáo và slide thuyết trình.

---

## Proposed Next Phase

- **Final Packaging & Delivery Phase:**
  1. Hoàn thiện `FINAL_REPORT.md` (đồng bộ kết quả thực nghiệm Test Set, so sánh Validation vs Test, phân tích lỗi định tính và trả lời 3 câu hỏi nghiên cứu).
  2. Tạo bài thuyết trình PowerPoint chính thức (`python -m presentation.generate_presentation`) không dùng cờ `--draft`.
  3. Cập nhật `README.md` với kết quả nghiên cứu và hướng dẫn demo.
  4. Kiểm thử khói (smoke test) ứng dụng Web Demo (`app/app.py`).
  5. Đồng bộ tài liệu ôn tập và câu hỏi phản biện (`docs/STUDY_GUIDE.md`, `docs/DEFENSE_QA.md`).
