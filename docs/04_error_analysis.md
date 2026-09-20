# 04. Khung Phân Tích Lỗi Định Tính (Qualitative Error Analysis Framework)

> [!IMPORTANT]
> **TRẠNG THÁI HIỆN TẠI:** `PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT`  
> Mô hình BERT chưa được huấn luyện và đánh giá trên Test Set.  
> Toàn bộ các ca lỗi và số liệu thống kê dưới đây là **KHUNG PHƯƠNG PHÁP LUẬN & DỮ LIỆU MẪU ĐỊNH DẠNG (PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT)**.  
> Dữ liệu thực nghiệm thực tế sẽ được tự động trích xuất và cập nhật sau khi chạy `python src/evaluate.py`.

---

## 1. Mục Tiêu & Phương Pháp Luận Phân Tích Lỗi

Theo quy trình chuẩn `AI Project Cycle`, việc phân tích lỗi không chỉ dừng lại ở các chỉ số tổng hợp (Accuracy, F1), mà cần khảo sát định tính từng mẫu dự đoán sai để:
1. Xác định các mẫu hình ngôn ngữ mà mô hình chưa xử lý tốt.
2. Đánh giá tác động của độ dài văn bản (Truncation).
3. Phát hiện khả năng nhiễu nhãn (Label Noise) từ dữ liệu gốc.
4. Đề xuất hướng cải tiến cho các phiên bản tiếp theo.

---

## 2. Khung Phân Loại Các Nhóm Lỗi Dự Kiến (Hypothetical Taxonomy)

Dựa trên khảo sát ngôn ngữ học đối với bài toán đánh giá khách sạn, 4 nhóm nguyên nhân chính được thiết lập để phân loại khi mô hình chạy thực tế:

| Nhóm Lỗi | Mô tả đặc trưng ngôn ngữ |
| :--- | :--- |
| **1. Cảm xúc pha trộn (Mixed Sentiment)** | Văn bản chứa đồng thời cả lời khen (vị trí, nhân viên) lẫn lời chê (tiếng ồn, vệ sinh). Nhãn nhị phân không phản ánh được sự đa chiều. |
| **2. Phủ định phức tạp (Complex Negation)** | Cấu trúc phủ định kép (*"not bad at all"*), phủ định của từ tiêu cực (*"nothing to complain about"*), hoặc đảo ngữ. |
| **3. Châm biếm / Mỉa mai (Sarcasm)** | Sử dụng từ ngữ tích cực bề mặt để diễn tả trải nghiệm tồi tệ (*"free swimming pool in our leaking bathroom"*). |
| **4. Cắt cụt & Nhiễu nhãn (Truncation & Label Noise)** | Văn bản vượt quá `max_length` làm mất đoạn kết luận quan trọng, hoặc khách hàng đánh giá điểm số không tương thích với nội dung nhận xét. |

---

## 3. Bảng Khảo Sát 20 Ca Lỗi (PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT)

*Bảng này sẽ được điền tự động từ tệp `artifacts/metrics/error_cases.json` sau khi hoàn tất lệnh `python src/evaluate.py`.*

| ID | Nhãn Thực | Nhãn Đoán | Confidence | Trích đoạn Đánh Giá (Review Text) | Phân Loại Lỗi | Phân Tích Kỹ Thuật |
| :-: | :-: | :-: | :-: | :--- | :--- | :--- |
| **01** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **02** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **03** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **04** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **05** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **06** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **07** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **08** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **09** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **10** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **11** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **12** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **13** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **14** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **15** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **16** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **17** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **18** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **19** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |
| **20** | `[TBD]` | `[TBD]` | `[TBD]` | *PLACEHOLDER — TO BE GENERATED AFTER EXPERIMENT* | `[Pending]` | `[Pending]` |

---

## 4. Quy Trình Cập Nhật Sau Khi Chạy Thực Nghiệm

1. Chạy `python src/train_bert.py` để lưu mô hình tốt nhất vào `artifacts/model/bert_best_model/`.
2. Chạy `python src/evaluate.py` để suy luận trên toàn bộ 4,000 mẫu Test Set.
3. Script `evaluate.py` sẽ tự động lọc các mẫu có `label != pred`, sắp xếp theo confidence cao nhất và lưu vào `artifacts/metrics/error_cases.json`.
4. Điền nội dung thực tế vào bảng trên và vẽ biểu đồ phân bố lỗi vào `artifacts/figures/error_categories.png`.
