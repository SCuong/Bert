# 04. Báo Cáo Phân Tích Định Tính Ca Lỗi Dự Đoán Của BERT (Qualitative Error Analysis)

> [!NOTE]
> **Phạm vi & Phương pháp luận:**  
> Báo cáo này khảo sát chi tiết **20 ca dự đoán sai có độ tin cậy cao nhất (highest-confidence errors)** của mô hình Fine-Tuned BERT trên tập kiểm thử độc lập (Test Set, 3,949 mẫu), gồm **10 ca False Positive (FP)** và **10 ca False Negative (FN)** được trích xuất tại `artifacts/metrics/error_cases.json`.  
> **Lưu ý quan trọng về phạm vi phân tích:** Đây là mẫu chọn lọc có chủ đích gồm các ca lỗi cực đoan (highest-confidence misclassifications), **KHÔNG PHẢI** là mẫu ngẫu nhiên hay đại diện thống kê cho toàn bộ 599 ca lỗi của BERT trên Test Set. Việc khảo sát các ca lỗi này nhằm mục đích nhận diện các trường hợp biên (edge cases), mẫu hình ngôn ngữ phức tạp và dấu hiệu về chất lượng dữ liệu. Các tỷ lệ phần trăm nêu trong báo cáo này chỉ áp dụng cụ thể cho mẫu 20 ca được khảo sát, không suy rộng cho toàn bộ tập kiểm thử.

---

## 1. Bảng Khảo Sát Chi Tiết 20 Ca Lỗi (Per-Case Analysis Table)

| ID | Nhãn Thực | Nhãn Đoán | Confidence | Độ dài Token | Cắt cụt? | Trích đoạn Đánh Giá (Excerpt) | Mẫu hình Ngôn ngữ / Dữ liệu | Phân tích Ngữ nghĩa & Kỹ thuật | Độ tin cậy Phân tích |
| :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- | :--- | :-: |
| **01** | 0 (Neg) | 1 (Pos) | 0.9980 | 33 | Không | *"Paying for parking The rooms are nice and clean and the beds are really comfortable..."* | Cảm xúc pha trộn; biểu thức tích cực chiếm đa số so với một lời phàn nàn | Đánh giá mở đầu bằng phàn nàn về phí đỗ xe, nhưng phần lớn văn bản chứa lời khen ngợi về phòng, giường, hồ bơi, xông hơi và kết luận *"Overall nice stay"*. Dự đoán lớp 1 phù hợp với việc các biểu thức tích cực chiếm ưu thế trong văn bản so với lời phàn nàn đơn lẻ. | High |
| **02** | 0 (Neg) | 1 (Pos) | 0.9980 | 21 | Không | *"Nice room with good facilities Clean and tidy Good location the staff were very attentive excellent breakfast"* | Văn bản hoàn toàn chứa từ ngữ tích cực; dấu hiệu bất tương thích nhãn-ngữ nghĩa | Toàn bộ văn bản chứa các biểu thức đánh giá tích cực (*"Nice"*, *"good"*, *"Clean"*, *"attentive"*, *"excellent"*), không xuất hiện từ ngữ tiêu cực rõ ràng. Dự đoán lớp 1 phù hợp với ngữ nghĩa bề mặt; sự khác biệt này cho thấy dấu hiệu possible label ambiguity hoặc label noise trong dữ liệu gốc. | High |
| **03** | 0 (Neg) | 1 (Pos) | 0.9980 | 6 | Không | *"nothing everything was excellent"* | Ghép trường biểu mẫu nguồn (*Dislike: nothing* + *Like: everything was excellent*) | Văn bản có cấu trúc ghép hai trường dữ liệu biểu mẫu không dấu phân cách (*"nothing"* và *"everything was excellent"*). Thông điệp giao tiếp tổng thể là tích cực. Nhãn nhị phân 0 cho thấy dấu hiệu artifact từ quá trình trích xuất dữ liệu gốc. | High |
| **04** | 0 (Neg) | 1 (Pos) | 0.9979 | 12 | Không | *"All staff in the slow everything Wifi very good"* | Cú pháp phi chuẩn, ngữ pháp vỡ kết hợp cảm xúc pha trộn | Câu văn phi chuẩn (*"All staff in the slow everything"*) đi kèm mệnh đề tích cực (*"Wifi very good"*). Dự đoán lớp 1 phản ánh sự hiện diện của cụm từ đánh giá cao (*"very good"*), trong khi cấu trúc câu lỗi có thể gây khó khăn cho việc xử lý ngữ nghĩa tiêu cực. | Medium |
| **05** | 0 (Neg) | 1 (Pos) | 0.9979 | 23 | Không | *"It s not Kensington it s Shepherd s Bush a bit miss leading On the location front Staff and cleanliness"* | Phủ định, phàn nàn vị trí, lỗi chính tả kết hợp khía cạnh tích cực | Đánh giá phản ánh vị trí không đúng mô tả (*"miss leading"* viết sai chính tả), đồng thời nhắc đến *"Staff and cleanliness"*. Dự đoán lớp 1 phù hợp với các thuộc tính tích cực được nhắc đến, trong khi từ sai chính tả và phủ định vị trí đặt ra thách thức phân loại. | High |
| **06** | 0 (Neg) | 1 (Pos) | 0.9978 | 14 | Không | *"Decor could do with freshening up Staff very welcoming very pleasant"* | Góp ý nhẹ nhàng đối lập lời khen nhân viên rõ rệt | Nhận xét góp ý nhẹ (*"Decor could do with freshening up"*) đi kèm các tính từ khen ngợi nhân viên (*"very welcoming very pleasant"*). Dự đoán lớp 1 phù hợp với sự nổi bật của các biểu thức khen ngợi. | High |
| **07** | 0 (Neg) | 1 (Pos) | 0.9978 | 21 | Không | *"Smell mould the price of Valet arking Staff excellent Chino lation s amazing as always"* | Phàn nàn về vệ sinh/giá cả xen lẫn khen ngợi và lỗi chính tả | Phàn nàn về mùi mốc (*"Smell mould"*) và giá đỗ xe (*"Valet arking"* lỗi chính tả), nhưng chứa lời khen ngợi mạnh (*"Staff excellent"*, *"amazing as always"*). Dự đoán lớp 1 phù hợp với mật độ các biểu thức khen ngợi rõ rệt trong câu. | High |
| **08** | 0 (Neg) | 1 (Pos) | 0.9977 | 11 | Không | *"No bar fridge in room Excellent value for money"* | Phủ định tiện ích cụ thể đối lập với đánh giá giá trị tổng thể xuất sắc | Nêu việc thiếu tủ lạnh mini (*"No bar fridge"*), đi liền với đánh giá giá trị tổng thể (*"Excellent value for money"*). Dự đoán lớp 1 phù hợp với kết luận giá trị tích cực; sự đối lập với nhãn 0 thể hiện sự căng thẳng giữa đánh giá chi tiết và nhãn tổng thể. | High |
| **09** | 0 (Neg) | 1 (Pos) | 0.9975 | 39 | Không | *"The Hotel doesn t have fitness facilities like a gym steam or sauna These would make our stay very enjoyable..."* | Cấu trúc giả định/phủ định tiện ích đối lập lời khen dịch vụ | Nêu việc thiếu phòng gym dưới dạng giả định (*"These would make our stay very enjoyable"*), sau đó khen ngợi phòng ốc và nhân viên nhiệt tình. Mật độ từ ngữ tích cực chiếm ưu thế phù hợp với dự đoán lớp 1. | High |
| **10** | 0 (Neg) | 1 (Pos) | 0.9975 | 45 | Không | *"Wish it was closer it was about 15 min bus ride to downtown Otherwise it wasn t a bad hotel I liked the rooms..."* | Cấu trúc litotes (*"wasn t a bad hotel"*) và lời khen chi tiết | Phàn nàn khoảng cách nhẹ, sau đó dùng cấu trúc litotes (*"wasn t a bad hotel"*) và đánh giá tích cực (*"liked the rooms"*, phòng rộng, bãi đỗ xe tiện lợi). Dự đoán lớp 1 phản ánh sự chi phối của các nhận xét hài lòng sau cấu trúc litotes. | High |
| **11** | 1 (Pos) | 0 (Neg) | 0.9957 | 40 | Không | *"Unpleasant smell all around the hotel specially from the toilet and bathroom It seems that they only clean with water..."* | Phàn nàn nghiêm trọng về vệ sinh xen lẫn vị trí tốt; nhãn thực tế mang tính đối lập | Văn bản mô tả mùi khó chịu và vấn đề vệ sinh, chỉ kèm một câu khen vị trí ở cuối (*"location was great"*). Dự đoán lớp 0 phù hợp với trọng tâm phàn nàn vệ sinh; nhãn thực 1 cho thấy dấu hiệu apparent semantic-label mismatch hoặc label noise. | High |
| **12** | 1 (Pos) | 0 (Neg) | 0.9956 | 39 | Không | *"I did not like the standerd room i booked it was very poor old cold and isolated... had to chang to a bitter room and pay moreNo Positive"* | Văn bản hoàn toàn tiêu cực có dấu hiệu *"No Positive"*; nhãn thực mang tính đối lập | Văn bản chứa toàn bộ từ ngữ phàn nàn (*"did not like"*, *"poor old cold and isolated"*) và kết thúc bằng thẻ *"No Positive"*. Dự đoán lớp 0 phù hợp với ngữ nghĩa bề mặt; nhãn thực 1 cho thấy dấu hiệu rõ ràng của possible label noise trong dữ liệu. | High |
| **13** | 1 (Pos) | 0 (Neg) | 0.9953 | 42 | Không | *"I paid 409 for a basic twin room The hotel was nice but the price is bloody extortionate Not worth the money at all... No Positive"* | Bất bình gay gắt về giá cả có dấu hiệu *"No Positive"*; nhãn thực mang tính đối lập | Dù có cụm từ *"hotel was nice"*, trọng tâm phê phán gay gắt giá tiền (*"bloody extortionate"*, *"Not worth the money at all"*, *"No Positive"*). Dự đoán lớp 0 phù hợp với phàn nàn giá cả nổi bật; nhãn thực 1 phản ánh dấu hiệu label ambiguity hoặc label noise. | High |
| **14** | 1 (Pos) | 0 (Neg) | 0.9950 | 126 | Không | *"This hotel is like finding an oasis in a neighborhood that has seen better days... sleep was interrupted several times... not stay in this neighborhood again."* | Đánh giá dài, chuyển dịch quan điểm từ khen ngợi sang kết luận tiêu cực vì ngoại cảnh | Người đánh giá mở đầu bằng lời khen ngợi (*"oasis"*, *"clean"*, *"freshly refurnished"*), nhưng phần sau mô tả tiếng ồn bên ngoài làm mất ngủ và kết luận không quay lại. Dự đoán lớp 0 phù hợp với kết luận tiêu cực mạnh mẽ ở phần cuối văn bản. | High |
| **15** | 1 (Pos) | 0 (Neg) | 0.9946 | 51 | Không | *"The small rooms We booked a window room but were told that none were available... in the middle of SOHO why would you Good place to rest your head"* | Phàn nàn diện tích phòng đi kèm sự hợp lý hóa thực tế | Khách phàn nàn phòng nhỏ và không cửa sổ, sau đó đưa ra cách nhìn nhận thực tế (*"ở giữa SOHO thì cần gì phòng to"*, *"Good place to rest your head"*). Dự đoán lớp 0 phù hợp với sự lặp lại của phàn nàn diện tích phòng trong văn bản. | High |
| **16** | 1 (Pos) | 0 (Neg) | 0.9944 | 117 | Không | *"If you've stayed at a Kimpton Hotel before... some people in my group didn't see it that way. They saw it as an old hotel... I disagree. The service was great..."* | Dẫn ý kiến chê bai của người khác rồi bác bỏ (*"I disagree"*); thách thức suy luận ngữ cảnh | Khách dẫn lời bạn bè chê khách sạn cũ kỹ rồi tuyên bố *"I disagree. The service was great..."*. Việc tách biệt quan điểm được trích dẫn (attributed perspective) với lập trường khẳng định của tác giả (author's stance) đặt ra thách thức suy luận cho mô hình. | High |
| **17** | 1 (Pos) | 0 (Neg) | 0.9943 | 74 | Không | *"Booking com didn t book 2 rooms that we had payed for... totally disgusted with booking com will not use them again... I want a explanationNo Positive"* | Khiếu nại dịch vụ đặt phòng kèm thẻ *"No Positive"*; nhãn thực mang tính đối lập | Văn bản thể hiện sự bức xúc với nền tảng đặt phòng (*"totally disgusted with booking com"*, *"No Positive"*). Dự đoán lớp 0 phản ánh sắc thái phàn nàn gay gắt; nhãn thực 1 cho thấy dấu hiệu apparent data-label mismatch. | High |
| **18** | 1 (Pos) | 0 (Neg) | 0.9940 | 23 | Không | *"Rooms not soundproof at all you hear people in the hallway Small bed rooftop and pool was nice Good location"* | Cảm xúc pha trộn; chê cách âm và giường nhỏ xen lẫn khen hồ bơi và vị trí | Phàn nàn về cách âm (*"not soundproof at all"*) và giường nhỏ được đặt cạnh lời khen hồ bơi và vị trí. Dự đoán lớp 0 phù hợp với việc các phàn nàn phòng ốc được mô tả cụ thể. | High |
| **19** | 1 (Pos) | 0 (Neg) | 0.9939 | 59 | Không | *"television would not work over 5 days despite 4 reports hotel denied responsibility... this is ridiculous... never will againNo Positive"* | Phàn nàn dịch vụ kèm thẻ *"No Positive"*; nhãn thực mang tính đối lập | Khách hàng bức xúc vì tivi hỏng 5 ngày không được giải quyết và thái độ xử lý (*"hotel denied responsibility"*, *"No Positive"*). Dự đoán lớp 0 nhất quán với ngữ nghĩa bề mặt của văn bản; nhãn thực 1 cho thấy dấu hiệu possible label noise. | High |
| **20** | 1 (Pos) | 0 (Neg) | 0.9938 | 31 | Không | *"Rooms are very dark no extra outlets in the bathroom no proper fan in the bathroom ventilation system was odd Location is fairly good staff was friendly and helpful"* | Liệt kê nhiều khuyết điểm phòng ốc đối lập với vị trí và thái độ nhân viên | Đưa ra nhiều điểm trừ cụ thể trong phòng (tối, thiếu ổ cắm, thiếu quạt, thông gió kỳ lạ) trước khi khen vị trí và nhân viên. Dự đoán lớp 0 phù hợp với sự tích lũy của các chi tiết phàn nàn cụ thể về phòng. | High |

---

## 2. Thống Kê Phân Bố Nhóm Lỗi Trên Mẫu Khảo Sát (Sample Category Distribution)

Dựa trên việc phân loại các hiện tượng ngôn ngữ và dữ liệu trên **mẫu 20 ca lỗi có độ tin cậy cao nhất**:

| Nhóm Hiện Tượng Ngôn Ngữ / Dữ Liệu | Số ca xuất hiện (trên mẫu 20 ca) | Tỷ lệ trong mẫu (%) | Các ca điển hình |
| :--- | :---: | :---: | :--- |
| **Cảm xúc pha trộn / Mệnh đề cạnh tranh (Mixed Sentiment / Competing Clauses)** | **15 / 20** | **75.0%** | Case 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18, 20 |
| **Dấu hiệu mơ hồ nhãn hoặc nhiễu nhãn (Possible Label Ambiguity / Label Noise)** | **8 / 20** | **40.0%** | Case 1, 2, 3, 11, 12, 13, 17, 19 |
| **Cấu trúc phủ định hoặc nhượng bộ (Negation or Concessive Structure)** | **8 / 20** | **40.0%** | Case 5, 8, 9, 10, 15, 16, 18, 20 |
| **Tác động của định dạng biểu mẫu nguồn (Template / Source Marker Effects)** | **6 / 20** | **30.0%** | Case 3, 8, 12, 13, 17, 19 |
| **Văn bản phi chuẩn: lỗi ngữ pháp, chính tả (Noisy Grammar, Spelling, Malformed Text)** | **4 / 20** | **20.0%** | Case 4, 5, 7, 12 |
| **Khiếu nại nền tảng trung gian vs. Dịch vụ khách sạn (Domain / Platform Complaint)** | **2 / 20** | **10.0%** | Case 14, 17 |
| **Thách thức suy luận ngữ cảnh của mô hình (Plausible Model Reasoning Failure)** | **1 / 20** | **5.0%** | Case 16 |

*(Lưu ý: Một ca lỗi có thể thuộc về nhiều nhóm hiện tượng đồng thời. Các tỷ lệ trên chỉ đại diện cho mẫu 20 ca lỗi có độ tin cậy cao nhất được khảo sát, không đại diện cho toàn bộ 599 ca lỗi của mô hình).*

---

## 3. Quan Sát Chi Tiết Giữa False Positive (FP) và False Negative (FN)

### 3.1. Đặc trưng của nhóm False Positive được khảo sát (Thực tế: 0, Mô hình đoán: 1)
- **Đặc điểm nội dung:** Người đánh giá đưa ra đánh giá tổng thể là tiêu cực (nhãn 0), nhưng nội dung văn bản lại dành phần lớn dung lượng để khen ngợi các khía cạnh cụ thể (nhân viên, vị trí, tiện nghi), chỉ kèm theo một phàn nàn nhỏ (ví dụ: phí đỗ xe ở Case 01, trang trí cần làm mới ở Case 06, thiếu tủ lạnh ở Case 08). Dự đoán của mô hình phản ánh sự chi phối của các biểu thức tích cực chiếm đa số trong văn bản.
- **Trường hợp dấu hiệu nhiễu nhãn:** Case 02 và Case 03 là những văn bản thể hiện sự hài lòng và khen ngợi rõ rệt, không chứa biểu thức tiêu cực nào, nhưng mang nhãn 0 trong tập dữ liệu gốc.

### 3.2. Đặc trưng của nhóm False Negative được khảo sát (Thực tế: 1, Mô hình đoán: 0)
- **Đặc điểm nội dung:** Người đánh giá phàn nàn gay gắt và liệt kê hàng loạt vấn đề nghiêm trọng (mùi hôi ở Case 11, giá cả ở Case 13, sự cố tivi ở Case 19, phòng tối và thiếu tiện nghi ở Case 20). Dự đoán lớp 0 của mô hình phù hợp với các biểu thức phàn nàn chiếm ưu thế trong văn bản.
- **Sự xuất hiện của thẻ nguồn `"No Positive"`:** Xuất hiện ở 4/10 ca FN được khảo sát (Case 12, 13, 17, 19). Đây là dấu hiệu sinh ra từ hệ thống thu thập dữ liệu (khi người dùng để trống ô đánh giá tích cực). Việc văn bản chứa phàn nàn áp đảo nhưng nhãn lại là 1 (Positive) cho thấy dấu hiệu apparent semantic-label mismatch hoặc label noise từ nguồn dữ liệu ban đầu.
- **Thách thức suy luận ngữ cảnh (Case 16):** Đây là ca lỗi thể hiện rõ hạn chế trong việc mô hình hóa ngữ dụng học. Tác giả dẫn lại quan điểm tiêu cực của bạn bè để rồi bác bỏ (*"They saw it as an old hotel... I disagree. The service was great"*). Việc tách biệt quan điểm được dẫn lại với lập trường khẳng định của tác giả là một thách thức đối với mô hình phân loại chuỗi thông thường.

---

## 4. Đánh Giá Hiện Tượng Cắt Cụt Văn Bản (Truncation Observations)

- **Đo lường thực tế:** Trong mẫu 20 ca lỗi có độ tin cậy cao nhất được khảo sát, **0 / 20 ca bị cắt cụt** (`truncation_count = 0`).
- **Phân bố độ dài token:** Độ dài token của 20 ca này dao động từ 6 đến 126 tokens (đo lường bằng `AutoTokenizer.from_pretrained(BERT_BEST_MODEL_DIR)` với `max_length = 128`).
- **Kết luận trong phạm vi mẫu:** Đối với 20 ca lỗi cực đoan được khảo sát, ngưỡng `MAX_LENGTH = 128` bảo toàn trọn vẹn văn bản. Do đó, hiện tượng cắt cụt không phải là nguyên nhân gây ra lỗi trong nhóm 20 ca này. Tuy nhiên, quan sát này không loại trừ khả năng cắt cụt có thể ảnh hưởng đến các ca lỗi dài khác trong toàn bộ 599 ca lỗi trên tập kiểm thử (nơi p99 đạt 168 tokens).

---

## 5. Nhận Định Về Chất Lượng Dữ Liệu & Tính Mơ Hồ Của Nhãn (Data Quality & Label Noise)

1. **Giới hạn của bài toán nhị phân (Binary Classification Bottleneck):** Đánh giá khách sạn trong thực tế thường mang tính đa khía cạnh (*Aspect-Based*). Người dùng có thể hài lòng về nhân viên nhưng không hài lòng về tiện nghi phòng. Việc ép các văn bản chứa cảm xúc phức tạp vào một nhãn nhị phân duy nhất (0 hoặc 1) tạo ra tính mơ hồ cố hữu (inherent ambiguity).
2. **Dấu hiệu nhiễu nhãn trong tập dữ liệu:**
   - Trong mẫu 20 ca khảo sát, có 8 ca (ví dụ: Case 02, 03, 11, 12, 13, 17, 19) xuất hiện sự mâu thuẫn rõ rệt giữa ngữ nghĩa bề mặt của văn bản và nhãn ground-truth được gán.
   - Khi mô hình dự đoán ngược lại nhãn gốc với xác suất rất cao ($> 99.3\%$), dự đoán của mô hình thể hiện sự nhất quán với ngữ nghĩa bề mặt của văn bản hơn là nhãn nhị phân trong dữ liệu.

---

## 6. Giới Hạn Của Phân Tích Định Tính (Limitations)

- **Kích thước và tính chất mẫu:** Khảo sát tập trung vào 20 ca lỗi có độ tin cậy cao nhất (highest-confidence errors), đại diện cho một phần nhỏ (khoảng 3.3%) của 599 ca lỗi trên Test Set. Mẫu này thiên về các trường hợp cực đoan và không phản ánh các ca lỗi ở vùng ranh giới quyết định (nơi xác suất dự đoán gần 0.50).
- **Tính định tính trong phân loại:** Việc gán nhãn nguyên nhân ngôn ngữ dựa trên phân tích thủ công của kỹ sư, dù đã tuân thủ các tiêu chí khách quan dựa trên bằng chứng văn bản.

---

## 7. Trả Lời Câu Hỏi Nghiên Cứu Số 3 (Evidence-Based Answer to RQ3)

> **Câu hỏi nghiên cứu 3 (RQ3):** *Bản chất của các trường hợp mà mô hình BERT dự đoán sai là gì? Lỗi bắt nguồn từ hạn chế kiến trúc mô hình hay do chất lượng và tính mơ hồ của dữ liệu?*

**Trả lời dựa trên bằng chứng thực nghiệm:**
1. **Dữ liệu và bản chất bài toán đóng vai trò chính trong phần lớn ca lỗi cực đoan được khảo sát:**
   - Trong mẫu 20 ca lỗi được khảo sát, 15/20 ca (75.0%) mang đặc trưng cảm xúc pha trộn (Mixed Sentiment), nơi các khía cạnh đối lập cùng xuất hiện trong một văn bản.
   - Có 8/20 ca (40.0%) cho thấy dấu hiệu bất tương thích giữa ngữ nghĩa văn bản và nhãn dữ liệu (possible label ambiguity / label noise hoặc tàn dư biểu mẫu nguồn như `"No Positive"`). Trong các trường hợp này, dự đoán của mô hình thể hiện sự nhất quán với ngữ nghĩa bề mặt của văn bản hơn là nhãn nhị phân được gán.
2. **Hạn chế mô hình hóa ngôn ngữ sâu xuất hiện ở mức độ tinh tế:**
   - Mô hình xử lý tốt các cấu trúc phủ định thông thường và litotes (như *"wasn t a bad hotel"*).
   - Thách thức thực sự đối với kiến trúc phân loại chuỗi nằm ở các cấu trúc ngữ dụng học phức tạp (như phân biệt quan điểm trích dẫn của người khác với lập trường cá nhân của tác giả ở Case 16) và sự vắng mặt của cơ chế phân tích theo từng khía cạnh (Aspect-Based Sentiment Analysis).
   - Trong phạm vi 20 ca lỗi cực đoan được khảo sát, cắt cụt độ dài văn bản không phải là nguyên nhân gây lỗi (0/20 ca bị cắt cụt).
