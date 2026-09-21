# 04. Báo Cáo Phân Tích Định Tính Ca Lỗi Dự Đoán Của BERT (Qualitative Error Analysis)

> [!NOTE]
> **Phạm vi & Phương pháp luận:**  
> Báo cáo này khảo sát chi tiết **20 ca dự đoán sai có độ tin cậy cao nhất (highest-confidence errors)** của mô hình Fine-Tuned BERT trên tập kiểm thử độc lập (Test Set, 3,949 mẫu), gồm **10 ca False Positive (FP)** và **10 ca False Negative (FN)** được trích xuất tại `artifacts/metrics/error_cases.json`.  
> **Lưu ý quan trọng:** Đây là mẫu chọn lọc các ca lỗi cực đoan (high-confidence misclassifications), **KHÔNG PHẢI** là mẫu ngẫu nhiên hay đại diện thống kê cho toàn bộ 599 ca lỗi của BERT trên Test Set. Việc khảo sát các ca lỗi này nhằm mục đích phát hiện các trường hợp biên (edge cases), mẫu hình ngôn ngữ phức tạp và các vấn đề về chất lượng dữ liệu gốc.

---

## 1. Bảng Khảo Sát Chi Tiết 20 Ca Lỗi (Per-Case Analysis Table)

| ID | Nhãn Thực | Nhãn Đoán | Confidence | Độ dài Token | Cắt cụt? | Trích đoạn Đánh Giá (Excerpt) | Mẫu hình Ngôn ngữ / Dữ liệu | Giải thích Kỹ thuật & Nguyên nhân | Độ tin cậy Phân tích |
| :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- | :--- | :-: |
| **01** | 0 (Neg) | 1 (Pos) | 0.9980 | 33 | Không | *"Paying for parking The rooms are nice and clean and the beds are really comfortable..."* | Cảm xúc pha trộn; lời khen áp đảo lời chê duy nhất | Đánh giá mở đầu bằng phàn nàn về phí đỗ xe, nhưng phần lớn văn bản chứa lời khen mạnh mẽ về phòng, giường, hồ bơi, xông hơi và kết luận *"Overall nice stay"*. Mô hình chú ý vào các từ tích cực áp đảo. | High |
| **02** | 0 (Neg) | 1 (Pos) | 0.9980 | 21 | Không | *"Nice room with good facilities Clean and tidy Good location the staff were very attentive excellent breakfast"* | Văn bản hoàn toàn tích cực; nghi vấn nhiễu nhãn gốc | Toàn bộ văn bản chỉ chứa các từ ngữ khen ngợi tuyệt đối (*"Nice"*, *"good"*, *"Clean"*, *"attentive"*, *"excellent"*), không có từ tiêu cực nào. Nhãn thực 0 là lỗi gán nhãn rõ ràng từ dữ liệu gốc. | High |
| **03** | 0 (Neg) | 1 (Pos) | 0.9980 | 6 | Không | *"nothing everything was excellent"* | Ghép trường biểu mẫu nguồn (*Dislike: nothing* + *Like: everything was excellent*) | Người dùng điền *"nothing"* vào ô Không thích và *"everything was excellent"* vào ô Hài lòng. Khi ghép chuỗi không dấu phân tách, ý định thực tế là tích cực 100%. Nhãn 0 là artifact biểu mẫu. | High |
| **04** | 0 (Neg) | 1 (Pos) | 0.9979 | 12 | Không | *"All staff in the slow everything Wifi very good"* | Cú pháp lỗi, ngữ pháp vỡ kết hợp cảm xúc pha trộn | Câu tiếng Anh lỗi (*"All staff in the slow everything"* phàn nàn nhân viên) đi kèm *"Wifi very good"*. Mô hình gán trọng số cao cho *"very good"* và bỏ sót ngữ nghĩa tiêu cực bị lỗi ngữ pháp. | Medium |
| **05** | 0 (Neg) | 1 (Pos) | 0.9979 | 23 | Không | *"It s not Kensington it s Shepherd s Bush a bit miss leading On the location front Staff and cleanliness"* | Phủ định, phàn nàn vị trí, lỗi chính tả kết hợp khía cạnh tích cực | Phàn nàn vị trí không đúng quảng cáo (*"miss leading"* viết sai chính tả), nhưng liệt kê *"Staff and cleanliness"*. Mô hình bị đánh lừa bởi từ tích cực và bỏ qua ngữ nghĩa của từ sai chính tả. | High |
| **06** | 0 (Neg) | 1 (Pos) | 0.9978 | 14 | Không | *"Decor could do with freshening up Staff very welcoming very pleasant"* | Lời chê mang tính góp ý nhẹ nhàng đối lập lời khen nhân viên mạnh mẽ | Lời góp ý nhẹ (*"Decor could do with freshening up"*) bị lấn át hoàn toàn bởi các tính từ khen ngợi nhân viên (*"very welcoming very pleasant"*), khiến mô hình dự đoán Positive. | High |
| **07** | 0 (Neg) | 1 (Pos) | 0.9978 | 21 | Không | *"Smell mould the price of Valet arking Staff excellent Chino lation s amazing as always"* | Phàn nàn nghiêm trọng về vệ sinh/giá cả xen lẫn lời khen tột độ và lỗi gõ phím | Phàn nàn mùi mốc (*"Smell mould"*) và giá đỗ xe (*"Valet arking"* lỗi chính tả), nhưng khen *"Staff excellent"* và *"amazing as always"*. Mô hình ưu tiên các từ cực đoan tích cực. | High |
| **08** | 0 (Neg) | 1 (Pos) | 0.9977 | 11 | Không | *"No bar fridge in room Excellent value for money"* | Phủ định tiện ích cụ thể đối lập với đánh giá giá trị tổng thể xuất sắc | Nêu việc thiếu tủ lạnh (*"No bar fridge"*), nhưng khẳng định *"Excellent value for money"*. Mô hình đánh giá cao lời tổng kết giá trị hơn sự thiếu hụt tiện ích đơn lẻ. | High |
| **09** | 0 (Neg) | 1 (Pos) | 0.9975 | 39 | Không | *"The Hotel doesn t have fitness facilities like a gym steam or sauna These would make our stay very enjoyable..."* | Cấu trúc giả định/phủ định tiện ích đối lập lời khen dịch vụ | Nêu việc thiếu phòng gym dưới dạng giả định (*"These would make our stay very enjoyable"*), sau đó khen ngợi phòng ốc và nhân viên nhiệt tình. Mật độ từ tích cực lấn át sự thiếu thốn tiện ích. | High |
| **10** | 0 (Neg) | 1 (Pos) | 0.9975 | 45 | Không | *"Wish it was closer it was about 15 min bus ride to downtown Otherwise it wasn t a bad hotel I liked the rooms..."* | Cấu trúc phủ định kép/litotes (*"wasn t a bad hotel"*) và lời khen chi tiết | Phàn nàn khoảng cách địa lý ở mức nhẹ, sau đó dùng litotes (*"wasn t a bad hotel"*) và khen phòng rộng rãi, bãi đỗ xe tiện lợi. Mô hình xử lý tốt litotes nên xếp vào Positive. | High |
| **11** | 1 (Pos) | 0 (Neg) | 0.9957 | 40 | Không | *"Unpleasant smell all around the hotel specially from the toilet and bathroom It seems that they only clean with water..."* | Phàn nàn nghiêm trọng về vệ sinh xen lẫn vị trí tốt; nhãn thực tế bất thường | Mô hình dự đoán Negative là hoàn toàn hợp lý về mặt ngữ nghĩa vì văn bản mô tả mùi hôi khó chịu và không dùng chất tẩy rửa. Nhãn gốc 1 là trường hợp rất đáng ngờ về chất lượng gán nhãn. | High |
| **12** | 1 (Pos) | 0 (Neg) | 0.9956 | 39 | Không | *"I did not like the standerd room i booked it was very poor old cold and isolated... had to chang to a bitter room and pay moreNo Positive"* | Văn bản hoàn toàn tiêu cực có dấu hiệu *"No Positive"*; nhãn thực tế bị đảo ngược | Văn bản chỉ chứa từ ngữ phàn nàn và kết thúc bằng tag nguồn *"No Positive"*. Mô hình dự đoán Negative chính xác 100% về mặt ngữ nghĩa. Nhãn 1 trong dữ liệu là lỗi đảo nhãn rõ rệt. | High |
| **13** | 1 (Pos) | 0 (Neg) | 0.9953 | 42 | Không | *"I paid 409 for a basic twin room The hotel was nice but the price is bloody extortionate Not worth the money at all... No Positive"* | Bất bình gay gắt về giá cả có dấu hiệu *"No Positive"*; nhãn thực tế bị lỗi | Mặc dù có câu *"hotel was nice"*, trọng tâm là chỉ trích mức giá cắt cổ (*"bloody extortionate"*, *"Not worth the money at all"*). Mô hình bắt đúng cảm xúc tiêu cực; nhãn 1 là nhiễu nhãn. | High |
| **14** | 1 (Pos) | 0 (Neg) | 0.9950 | 126 | Không | *"This hotel is like finding an oasis in a neighborhood that has seen better days... sleep was interrupted several times... not stay in this neighborhood again."* | Đánh giá dài, dịch chuyển quan điểm từ khen ngợi sang kết luận tiêu cực vì ngoại cảnh | Mở đầu khen ngợi như ốc đảo, nhưng kết luận gay gắt vì tiếng ồn bên ngoài và khẳng định không quay lại. Mô hình bị chi phối bởi đoạn kết luận tiêu cực, trong khi nhãn tổng thể của khách là 1. | High |
| **15** | 1 (Pos) | 0 (Neg) | 0.9946 | 51 | Không | *"The small rooms We booked a window room but were told that none were available... in the middle of SOHO why would you Good place to rest your head"* | Phàn nàn diện tích phòng nhưng chấp nhận hợp lý hóa vì vị trí trung tâm | Khách chê phòng nhỏ không cửa sổ, nhưng tự hợp lý hóa *"ở giữa SOHO thì cần gì phòng to"*. Mô hình tập trung vào sự lặp lại của phàn nàn phòng nhỏ mà không hiểu được sự thỏa hiệp ngầm. | High |
| **16** | 1 (Pos) | 0 (Neg) | 0.9944 | 117 | Không | *"If you've stayed at a Kimpton Hotel before... some people in my group didn't see it that way. They saw it as an old hotel... I disagree. The service was great..."* | Trích dẫn ý kiến chê bai của người khác rồi bác bỏ (*"I disagree"*); lỗi suy luận ngữ cảnh của mô hình | Khách dẫn lời bạn bè chê khách sạn cũ kỹ rồi tuyên bố *"Tôi không đồng ý, dịch vụ rất tuyệt"*. Mô hình bị nhầm lẫn giữa lời trích dẫn tiêu cực và quan điểm cá nhân tích cực của tác giả. | High |
| **17** | 1 (Pos) | 0 (Neg) | 0.9943 | 74 | Không | *"Booking com didn t book 2 rooms that we had payed for... totally disgusted with booking com will not use them again... I want a explanationNo Positive"* | Khiếu nại nền tảng đặt phòng (Booking.com) có *"No Positive"*; nhãn gốc bị sai lệch | Toàn bộ văn bản trút giận lên nền tảng Booking.com vì lỗi đặt phòng, không liên quan đến trải nghiệm tại khách sạn. Mô hình nhận diện cảm xúc tiêu cực; nhãn 1 là lỗi gán nhãn nghiêm trọng. | High |
| **18** | 1 (Pos) | 0 (Neg) | 0.9940 | 23 | Không | *"Rooms not soundproof at all you hear people in the hallway Small bed rooftop and pool was nice Good location"* | Cảm xúc pha trộn; chê cách âm và giường nhỏ xen lẫn khen hồ bơi và vị trí | Phàn nàn phòng ồn và giường nhỏ được đặt cạnh lời khen hồ bơi và vị trí. Mô hình cho trọng số cao hơn vào yếu tố cách âm và giường ngủ, dẫn đến dự đoán Negative. | High |
| **19** | 1 (Pos) | 0 (Neg) | 0.9939 | 59 | Không | *"television would not work over 5 days despite 4 reports hotel denied responsibility... this is ridiculous... never will againNo Positive"* | Trải nghiệm tồi tệ về dịch vụ kỹ thuật có *"No Positive"*; nhãn gốc bị đảo ngược | Khách hàng bức xúc vì tivi hỏng 5 ngày và thái độ vô trách nhiệm của khách sạn, khẳng định không quay lại. Mô hình đoán Negative hoàn toàn chính xác; nhãn 1 là lỗi nhãn dữ liệu. | High |
| **20** | 1 (Pos) | 0 (Neg) | 0.9938 | 31 | Không | *"Rooms are very dark no extra outlets in the bathroom no proper fan in the bathroom ventilation system was odd Location is fairly good staff was friendly and helpful"* | Liệt kê nhiều khuyết điểm phòng ốc đối lập với vị trí và thái độ nhân viên | Đưa ra 4 điểm trừ cụ thể trong phòng (tối, thiếu ổ cắm, thiếu quạt, thông gió kỳ lạ) rồi mới khen vị trí và nhân viên. Sự tích lũy các từ tiêu cực khiến mô hình thiên về Negative. | High |

---

## 2. Thống Kê Phân Bố Nhóm Lỗi (Aggregate Category Counts)

Dựa trên việc gán nhãn nguyên nhân cho 20 ca lỗi thực nghiệm:

| Nhóm Nguyên Nhân Ngôn Ngữ / Dữ Liệu | Số ca xuất hiện (trên 20 ca) | Tỷ lệ (%) | Các ca điển hình |
| :--- | :---: | :---: | :--- |
| **Cảm xúc pha trộn / Mệnh đề cạnh tranh (Mixed Sentiment / Competing Clauses)** | **15** | **75.0%** | Case 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18, 20 |
| **Nghi vấn chất lượng nhãn / Nhiễu nhãn (Possible Label Ambiguity / Label Noise)** | **8** | **40.0%** | Case 1, 2, 3, 11, 12, 13, 17, 19 |
| **Cấu trúc phủ định hoặc nhượng bộ (Negation or Concessive Structure)** | **8** | **40.0%** | Case 5, 8, 9, 10, 15, 16, 18, 20 |
| **Tác động của định dạng biểu mẫu nguồn (Template / Source Marker Effects)** | **6** | **30.0%** | Case 3, 8, 12, 13, 17, 19 |
| **Lỗi ngữ pháp, chính tả, văn bản biến dạng (Noisy Grammar, Spelling, Malformed Text)** | **4** | **20.0%** | Case 4, 5, 7, 12 |
| **Khiếu nại nền tảng trung gian vs. Dịch vụ khách sạn (Domain / Platform Complaint)** | **2** | **10.0%** | Case 14, 17 |
| **Lỗi suy luận ngữ cảnh thực sự của mô hình (Plausible Model Reasoning Failure)** | **1** | **5.0%** | Case 16 |

*(Lưu ý: Một ca lỗi có thể thuộc về nhiều nhóm nguyên nhân đồng thời).*

---

## 3. Quan Sát Chi Tiết Giữa False Positive (FP) và False Negative (FN)

### 3.1. Đặc trưng của nhóm False Positive (Thực tế: 0, Mô hình đoán: 1)
- **Cơ chế gây lỗi:** Khách hàng đánh giá tiêu cực tổng thể (nhãn 0), nhưng nội dung văn bản lại dành phần lớn dung lượng để khen ngợi các khía cạnh cụ thể (nhân viên, vị trí, tiện nghi), chỉ kèm theo một phàn nàn nhỏ (ví dụ: phí đỗ xe ở Case 01, trang trí cần làm mới ở Case 06, thiếu tủ lạnh ở Case 08).
- **Trường hợp nhiễu nhãn:** Case 02 và Case 03 là những văn bản tích cực thuần túy không chứa bất kỳ từ ngữ tiêu cực nào, nhưng lại mang nhãn 0 trong tập dữ liệu gốc.

### 3.2. Đặc trưng của nhóm False Negative (Thực tế: 1, Mô hình đoán: 0)
- **Cơ chế gây lỗi:** Khách hàng phàn nàn rất gay gắt và liệt kê hàng loạt vấn đề nghiêm trọng (mùi hôi nồng nặc ở Case 11, giá cả cắt cổ ở Case 13, tivi hỏng 5 ngày ở Case 19, phòng tối và thiếu tiện nghi ở Case 20). Về mặt ngữ nghĩa tự nhiên, các văn bản này chứa cảm xúc tiêu cực áp đảo, khiến mô hình tự tin dự đoán nhãn 0 với xác suất trên 99.3%.
- **Sự xuất hiện của thẻ nguồn `"No Positive"`:** Xuất hiện ở 4/10 ca FN (Case 12, 13, 17, 19). Đây là dấu hiệu sinh ra từ hệ thống thu thập dữ liệu (khi người dùng để trống ô đánh giá tích cực trên các trang đặt phòng trực tuyến). Mặc dù văn bản hoàn toàn tiêu cực, nhãn gốc trong dataset lại bị gán là 1 (Positive), cho thấy lỗi đảo nhãn hoặc lỗi gán nhãn tự động từ hệ thống cũ.
- **Thất bại suy luận ngữ cảnh (Case 16):** Đây là ca lỗi duy nhất thể hiện hạn chế thực sự trong khả năng hiểu ngôn ngữ sâu của BERT. Tác giả dẫn lại lời chê của bạn bè để rồi bác bỏ (*"They saw it as an old hotel... I disagree"*). Mô hình chưa phân biệt được quan điểm được trích dẫn (attributed perspective) với lập trường khẳng định của tác giả (author's stance).

---

## 4. Đánh Giá Hiện Tượng Cắt Cụt Văn Bản (Truncation Observations)

- **Số lượng ca bị cắt cụt:** **0 / 20 ca** (`truncation_count = 0`).
- **Đo lường thực tế:** Độ dài token của 20 ca dao động từ 6 đến 126 tokens (đo lường bằng `AutoTokenizer.from_pretrained(BERT_BEST_MODEL_DIR)` với `max_length = 128`).
- **Kết luận:** Ngưỡng `MAX_LENGTH = 128` bảo toàn trọn vẹn 100% nội dung của 20 ca lỗi có độ tin cậy cao nhất này. Hiện tượng cắt cụt văn bản **không phải là nguyên nhân** dẫn đến các lỗi dự đoán sai lệch nghiêm trọng nhất của mô hình.

---

## 5. Nhận Định Về Chất Lượng Dữ Liệu & Tính Mơ Hồ Của Nhãn (Data Quality & Label Noise)

1. **Giới hạn của bài toán nhị phân (Binary Classification Bottleneck):** Đánh giá khách sạn trong thực tế thường mang tính đa khía cạnh (*Aspect-Based*). Người dùng có thể cực kỳ hài lòng về nhân viên nhưng vô cùng bức xúc về cách âm. Việc ép các văn bản phức tạp này vào nhãn nhị phân 0 hoặc 1 tạo ra tính mơ hồ cố hữu (inherent ambiguity).
2. **Sự tồn tại của nhiễu nhãn thực tế (Label Noise Evidence):**
   - Ít nhất 6 đến 8 ca trong số 20 ca khảo sát (ví dụ: Case 02, 03, 12, 13, 17, 19) có sự mâu thuẫn hoàn toàn giữa ngữ nghĩa văn bản và nhãn dữ liệu gốc.
   - Khi mô hình dự đoán ngược lại nhãn gốc với độ tin cậy cực cao ($> 99.4\%$), trong nhiều trường hợp, **dự đoán của mô hình lại phản ánh chính xác ngữ nghĩa thực tế hơn nhãn trong dataset**.

---

## 6. Giới Hạn Của Phân Tích Định Tính (Limitations)

- **Kích thước mẫu:** Khảo sát tập trung vào 20 ca lỗi cực đoan (high-confidence errors), chiếm khoảng 3.3% tổng số 599 ca lỗi trên Test Set. Kết quả không phản ánh phân bố xác suất của toàn bộ tập ca lỗi (nhiều ca lỗi có thể nằm ở vùng ranh giới quyết định với confidence gần 0.50).
- **Tính chủ quan trong phân loại:** Việc gán nguyên nhân ngôn ngữ học dựa trên quan sát thủ công của kỹ sư AI, dù đã áp dụng tiêu chí bằng chứng rõ ràng.

---

## 7. Trả Lời Câu Hỏi Nghiên Cứu Số 3 (Evidence-Based Answer to RQ3)

> **Câu hỏi nghiên cứu 3 (RQ3):** *Bản chất của các trường hợp mà mô hình BERT dự đoán sai là gì? Lỗi bắt nguồn từ hạn chế kiến trúc mô hình hay do chất lượng và tính mơ hồ của dữ liệu?*

**Trả lời dựa trên bằng chứng thực nghiệm:**
1. **Phần lớn lỗi bắt nguồn từ tính mơ hồ của bài toán và chất lượng dữ liệu (Data & Task Limitations chiếm đa số):**
   - 75% số ca lỗi xuất phát từ cảm xúc pha trộn (Mixed Sentiment), nơi một văn bản chứa đồng thời các đánh giá trái ngược nhau về các khía cạnh khác nhau của dịch vụ.
   - Khoảng 30% - 40% số ca lỗi có bằng chứng rõ ràng về nhiễu nhãn (Label Noise) và tàn dư biểu mẫu nguồn (`"No Positive"`). Trong những trường hợp này, mô hình thực chất đã hiểu đúng ngữ nghĩa văn bản nhưng bị phạt oan do nhãn ground-truth bị sai.
2. **Hạn chế kiến trúc và suy luận của BERT chỉ chiếm tỷ lệ nhỏ trong các ca cực đoan:**
   - BERT xử lý rất tốt các cấu trúc phủ định thông thường và litotes.
   - Thách thức thực sự về mặt mô hình hóa nằm ở các cấu trúc ngữ dụng học phức tạp (như phân biệt lời trích dẫn của người khác với quan điểm cá nhân ở Case 16) và việc thiếu cơ chế phân tích theo từng khía cạnh (Aspect-Level Mechanism).
   - Cắt cụt độ dài văn bản không phải là nguyên nhân gây ra các ca lỗi tự tin nhất.
