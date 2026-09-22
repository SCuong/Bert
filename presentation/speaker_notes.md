# Kịch Bản Thuyết Trình Bảo Vệ Đồ Án (Speaker Notes)

**Đề tài:** Nghiên Cứu và Ứng Dụng Mô Hình BERT Cho Bài Toán Phân Loại Cảm Xúc Đánh Giá Khách Sạn  
**Fine-Tuning BERT for Hotel Review Sentiment Classification**  
**Học phần:** Trí tuệ Nhân tạo (Artificial Intelligence)  
**Thời lượng trình bày chuẩn:** 8 - 10 phút (13 slides)  
**Nguyên tắc trình bày:** Phong thái tự tin, mạch lạc; hướng sự chú ý của Hội đồng vào các thẻ chỉ số lớn (KPI cards) và biểu đồ thực nghiệm; nhấn mạnh tính trung thực khoa học, quy trình chuẩn mực và việc tuân thủ nghiêm ngặt chuẩn mực AI Project Cycle.

---

### Slide 1: Trang Tiêu Đề (00:00 - 00:35)
> *"Kính thưa Quý Thầy/Cô trong Hội đồng chấm đồ án và các bạn sinh viên,*  
> *Hôm nay, em xin đại diện nhóm sinh viên thực hiện đề tài kính trình bày báo cáo nghiên cứu: **'Nghiên cứu và ứng dụng mô hình BERT cho bài toán phân loại cảm xúc đánh giá khách sạn' (Fine-Tuning BERT for Hotel Review Sentiment Classification)** trong học phần **Trí tuệ Nhân tạo (Artificial Intelligence)** dưới sự hướng dẫn của TS. Huỳnh Hữu Hưng.*  
> *Đề tài của chúng em được xây dựng độc lập hoàn toàn từ đầu (from scratch), tuân thủ 6 giai đoạn của **AI Project Cycle** và hướng tới một minh chứng thực nghiệm trung thực, được kiểm soát tính tái lập và giải thích rõ ràng về giá trị của mô hình Transformer so với phương pháp học máy truyền thống."*

---

### Slide 2: Bối Cảnh Bài Toán & Mục Tiêu Nghiên Cứu (00:35 - 01:20)
> *"Về bối cảnh thực tế (như Quý Thầy/Cô thấy ở thẻ bên trái): Trong ngành du lịch và dịch vụ lưu trú, việc phân tích phản hồi trực tuyến của khách hàng đóng vai trò sống còn. Tuy nhiên, ngôn ngữ tự nhiên trong đánh giá khách sạn chứa đựng nhiều thách thức ngữ nghĩa phức tạp: câu chứa cảm xúc hỗn hợp (vừa khen vừa chê), cấu trúc phủ định hoặc nhượng bộ tinh vi. Các mô hình truyền thống như Bag-of-Words bỏ qua trật tự từ, trong khi các mạng hồi quy RNN/LSTM gặp điểm nghẽn tính toán tuần tự và suy giảm ngữ cảnh xa.*  
> *Từ thách thức đó, mục tiêu của đề tài (ở thẻ bên phải) được xác định rõ ràng qua 3 đóng góp:  
> 1. Thiết lập quy trình nghiên cứu chuẩn mực khép kín, kiểm toán exact-match trước khi chia dữ liệu và kiểm toán case-normalized hậu nghiệm.  
> 2. Huấn luyện thực nghiệm đối chứng công bằng giữa mô hình cơ sở TF-IDF + Logistic Regression và mô hình chính Fine-Tuned BERT trên cùng một dữ liệu chuẩn.  
> 3. Đánh giá khách quan trên tập kiểm thử độc lập đã niêm phong (Held-Out Test Set 3,949 mẫu), phân tích định tính chuyên sâu các ca lỗi và đóng gói ứng dụng tương tác thời gian thực."*

---

### Slide 3: Quy Trình Nghiên Cứu Chuẩn Mực (AI Project Cycle) (01:20 - 02:05)
> *"Trên màn hình là 7 bước nghiên cứu khép kín bám sát AI Project Cycle mà nhóm đã kiên định tuân thủ:  
> - Bắt đầu từ Bước 1: Kiểm toán dữ liệu (Data Audit) để loại bỏ 255 mẫu lỗi và trùng lặp;  
> - Bước 2: Phân tích phân vị độ dài token để đưa ra quyết định MAX_LENGTH=128 có cơ sở định lượng;  
> - Bước 3: Phân chia Stratified 70/10/20 với seed 42 cố định;  
> - Bước 4: Xây dựng mô hình cơ sở TF-IDF + Logistic Regression theo triết lý 'Start simple to complex models';  
> - Bước 5: Fine-tuning toàn bộ 110M tham số của BERT, lưu checkpoint dựa trên Validation Macro F1;  
> - Bước 6: Đánh giá độc lập đúng 1 lần duy nhất trên tập Test Set đã niêm phong;  
> - Và Bước 7: Phân tích định tính 20 ca lỗi cực đoan và đóng gói Web UI FastAPI.
> Nguyên tắc cốt lõi xuyên suốt là kiểm soát giao thoa dữ liệu và đóng băng siêu tham số trước khi mở niêm phong tập kiểm thử."*

---

### Slide 4: Tập Dữ Liệu & Kết Quả Kiểm Toán Chống Rò Rỉ (02:05 - 02:50)
> *"Về dữ liệu (Slide 4): Từ tập dữ liệu 20,000 nhận xét thô do Thầy cung cấp, qua kiểm toán tự động, nhóm phát hiện và loại bỏ 255 mẫu không đạt chuẩn (thẻ đỏ): gồm 5 mẫu rỗng sau làm sạch, 127 mẫu nhãn xung đột (xuất phát từ 20 đoạn văn bản giống hệt nhau nhưng bị gán cả hai nhãn 0 và 1) và 123 mẫu trùng lặp hoàn toàn.  
> Kết quả, chúng em thu được **19,745 mẫu sạch duy nhất** (thẻ xanh lá) với tỷ lệ phân bổ hai lớp cân bằng lý tưởng: 50.25% Tiêu cực và 49.75% Tích cực.  
> Tập dữ liệu sạch này được phân chia thành Train 13,821 mẫu, Validation 1,975 mẫu và Test 3,949 mẫu. Pipeline dùng phép giao tập hợp chuỗi và xác nhận không có văn bản trùng khớp chính xác giữa các tập; implementation không dùng SHA-256. Kiểm toán hậu nghiệm với Unicode NFC, `strip()` và `casefold()` phát hiện lần lượt 3, 10 và 2 cặp giao thoa ở Train–Validation, Train–Test và Validation–Test, trong đó có 1 cặp trái nhãn. Đây là giới hạn hậu nghiệm; kết quả đóng băng không được tính lại."*

---

### Slide 5: Phân Bố Độ Dài Token & Quyết Định MAX_LENGTH (02:50 - 03:40)
> *"Một quyết định kỹ thuật quan trọng là việc lựa chọn `MAX_LENGTH`. Thay vì chọn cảm tính, nhóm đã phân tích phân vị độ dài token WordPiece trên 15,796 mẫu thuộc tập Train và Validation.  
> Biểu đồ bên trái cho thấy phân bố lệch phải rất rõ: Trung vị độ dài chỉ là 30 tokens, trung bình 42.33 tokens, phân vị p90 là 94 tokens, p95 là 121 tokens và p99 là 168 tokens.  
> Nhóm quyết định lựa chọn **MAX_LENGTH = 128**.  
> Cơ sở của quyết định này là: Ngưỡng 128 bao phủ trọn vẹn 96.07% toàn bộ văn bản (chỉ 3.93% số mẫu bị cắt cụt, p95 = 121), đồng thời giúp giảm 4 lần kích thước ma trận Attention bậc hai $O(L^2)$ và bộ nhớ kích hoạt so với ngưỡng 256 (nơi tỷ lệ vượt ngưỡng chỉ còn 0.09%). Đây là sự đánh đổi tối ưu để mô hình huấn luyện ổn định và hiệu quả trên tài nguyên CPU."*

---

### Slide 6: Thiết Lập Thực Nghiệm Đối Chứng: Baseline vs BERT (03:40 - 04:30)
> *"Tại Slide 6 là bảng thiết lập đối chứng chi tiết giữa hai mô hình:  
> - Ở thẻ bên trái: Mô hình cơ sở sử dụng TF-IDF với 10,000 đặc trưng unigram và bigram, áp dụng thang đo Sublinear TF ($1 + \log(tf)$) để làm mịn tần suất từ, kết hợp Logistic Regression chuẩn hóa L2 với solver L-BFGS. Mô hình này đóng vai trò mốc đối chứng chuẩn mực theo nguyên tắc 'Start simple to complex', với ưu thế huấn luyện trong 0.68 giây và suy luận đạt hơn 28,700 mẫu/giây trên CPU.  
> - Ở thẻ bên phải: Mô hình chính là BERT bản `bert-base-uncased` với 110 triệu tham số. Tiền xử lý chỉ loại bỏ thẻ HTML, chuẩn hóa khoảng trắng và bảo toàn nguyên vẹn cấu trúc câu; tokenizer WordPiece tự động xử lý chữ thường theo cấu hình uncased. Mỗi khối encoder của Transformer bao gồm self-attention, feed-forward layers, residual connections và layer normalization. Nhóm thực hiện **Full Fine-Tuning toàn bộ 110M tham số**, sử dụng thuật toán AdamW với learning rate chuẩn $2\times 10^{-5}$, warmup ratio 0.1, batch size 16 và huấn luyện trong 3 epochs, tự động lưu checkpoint có Validation Macro F1 cao nhất."*

---

### Slide 7: Quá Trình Huấn Luyện BERT & Động Lực Học Tập (04:30 - 05:20)
> *"Slide 7 trình bày đồ thị và số liệu quá trình huấn luyện BERT trên CPU: Tổng thời gian thực thi là 15,617 giây (~4.34 giờ) cho 2,592 steps.  
> Quan sát thẻ bên phải: Train Loss trung bình qua từng epoch giảm đều đặn từ 0.4385 xuống 0.2877 và 0.2022. Trên tập Validation, Macro F1 tăng từ 0.8310 ở Epoch 1 lên 0.8387 ở Epoch 2 và đạt đỉnh **0.8389** tại Epoch 3.  
> Về hiện tượng Validation Loss ở Epoch 3 tăng nhẹ lên 0.5461 trong khi Macro F1 đạt đỉnh cao nhất: Nhóm xin giải thích rõ đây là đặc tính cố hữu của hàm Cross-Entropy ($-\log p$). Hàm này phạt rất nặng mức độ tự tin ở một vài mẫu biên khó phân định, khiến tổng loss tăng lên; trong khi đó, ranh giới phân loại nhãn cứng của mô hình lại được tối ưu hóa tốt hơn, thể hiện qua việc Macro F1 đạt đỉnh. Vì vậy, việc lựa chọn `checkpoint-2592` tại cuối Epoch 3 là hoàn toàn chính xác về mặt khoa học."*

---

### Slide 8: Kết Quả So Sánh Đối Đầu Trên Held-Out Test Set (05:20 - 06:15)
> *"Kính thưa Quý Thầy/Cô, đây là **slide kết quả quan trọng nhất** của đề tài: Kết quả kiểm thử đối đầu chính thức trên tập Held-Out Test Set 3,949 mẫu sau khi đã đóng băng hoàn toàn tham số hai mô hình.  
> - Mô hình cơ sở (TF-IDF + LR) đạt Accuracy **81.94%** và Macro F1 **0.8192**.  
> - Mô hình chính Fine-Tuned BERT đạt Accuracy **84.83%** và Macro F1 **0.8483**.  
> - Nhìn sang thẻ xanh lá bên phải: BERT vượt trội Baseline **+2.89 điểm phần trăm về Accuracy** và **+0.0291 về Macro F1** (+2.91 percentage points trên thang phần trăm). Mức cải thiện này tương đương với việc BERT giúp giảm chính xác **114 ca dự đoán sai** trên tập kiểm thử (giảm 16.0% tổng lỗi).  
> Quan sát ở banner bên dưới: Chỉ số Validation Macro F1 (83.89%) và Test Macro F1 (84.83%) rất sát nhau, hoàn toàn nhất quán với hiệu năng quan sát được trên cả hai tập held-out độc lập. Đổi lại, việc tăng độ chính xác đòi hỏi sự đánh đổi về tài nguyên: thời gian suy luận của BERT trên CPU là 307.3 giây (~12.85 mẫu/s), chậm hơn so với 0.137 giây của mô hình tuyến tính."*

---

### Slide 9: So Sánh Ma Trận Nhầm Lẫn Trên Tập Test (06:15 - 07:05)
> *"Đi sâu vào ma trận nhầm lẫn của 3,949 mẫu Test (Slide 9):  
> - Baseline mắc 713 ca lỗi (18.06%), trong khi BERT chỉ còn 599 ca lỗi (15.17%).  
> - Điểm cải thiện giá trị nhất nằm ở thẻ bên dưới: Số ca **False Negative** (tức khách khen tích cực nhưng mô hình đoán sai thành tiêu cực) đã **giảm mạnh 94 ca** — từ 420 ca ở Baseline xuống chỉ còn 326 ca ở BERT, tương đương mức giảm tới **22.38%**!  
> - Đồng thời, số ca False Positive cũng giảm 20 ca (từ 293 xuống 273). Như vậy, BERT cải thiện đồng bộ và toàn diện cả hai lớp cảm xúc, nâng cao đồng thời cả Precision (+2.78%) và Recall (+2.89%)."*

---

### Slide 10: Phân Tích Lỗi Định Tính Trên Mẫu 20 Ca Tự Tin Nhất (07:05 - 08:00)
> *"Để hiểu tường tận nguyên nhân vì sao BERT vẫn còn 599 ca lỗi, nhóm đã tiến hành kiểm toán định tính chi tiết trên **mẫu 20 ca lỗi có độ tự tin cao nhất (10 FP, 10 FN)** trích xuất từ `error_cases.json`. Kết quả phân loại lỗi ở lưới 2x2 cho thấy:  
> 1. **75% ca lỗi (15/20 ca)** bắt nguồn từ 'Cảm xúc hỗn hợp' (Mixed Sentiment / Competing Clauses): Khách khen phòng ốc, vị trí nhưng phàn nàn gay gắt về tiếng ồn hoặc thái độ lễ tân. Nhãn nhị phân đơn lẻ không đủ khả năng đại diện cho các văn bản đa chiều như vậy.  
> 2. **40% ca lỗi (8/20 ca)** xuất hiện hiện tượng 'Mơ hồ nhãn hoặc khả năng nhiễu nhãn' (Possible label ambiguity / label noise): Văn bản chứa toàn từ ngữ khen ngợi nhưng ground-truth lại mang nhãn 0. Mô hình thực chất đã dự đoán đúng theo ngữ nghĩa thực của bài viết.  
> 3. Cấu trúc phủ định phức tạp và các marker biểu mẫu như `'No Positive'`, `'No Negative'` chiếm lần lượt 8 và 6 ca.  
> 4. Đặc biệt, ở thẻ xanh số 4: **0/20 ca lỗi được kiểm toán vượt quá ngưỡng MAX_LENGTH=128** (độ dài thực tế từ 6 đến 126 tokens). Quan sát này chỉ áp dụng cho 20 ca được chọn và không được suy rộng thành kết luận nhân quả cho toàn bộ lỗi.  
> Lưu ý: Các thống kê định tính trên chỉ áp dụng trong phạm vi 20 ca lỗi có độ tự tin cao nhất được kiểm toán, không suy rộng cho toàn bộ 599 ca lỗi của BERT."*

---

### Slide 11: Ứng Dụng Tương Tác Thời Gian Thực (FastAPI Demo) (08:00 - 08:45)
> *"Toàn bộ kết quả nghiên cứu đã được nhóm đóng gói thành ứng dụng Web trực quan bằng FastAPI tại `app/main.py`.
> Thẻ bên trái là ví dụ minh họa giao diện với một câu chứa cảm xúc nhượng bộ; đây không phải một benchmark đóng băng hay bằng chứng định lượng bổ sung. Khi chạy, ứng dụng hiển thị nhãn, độ tin cậy và xác suất Positive / Negative lấy trực tiếp từ pipeline BERT chuẩn.
> Ứng dụng phục vụ trang Jinja2 và endpoint `POST /api/predict`; model/tokenizer được cache bởi pipeline suy luận chuẩn, còn giao diện xử lý trạng thái tải và lỗi theo cách không lộ stack trace."*

---

### Slide 12: Hạn Chế Của Nghiên Cứu & Hướng Phát Triển (08:45 - 09:30)
> *"Tại Slide 12, nhóm thẳng thắn nhìn nhận các hạn chế và đề xuất hướng phát triển tương lai:  
> - **4 Hạn chế của nghiên cứu (thẻ trái):**  
>   1. Phạm vi nhị phân (Binary sentiment only): Hiện tại chỉ phân loại 2 lớp, chưa xử lý lớp trung lập 3 sao (Neutral) hay cảm xúc đa mức độ;  
>   2. Phạm vi kiểm toán lỗi (Selected qualitative analysis): Kiểm toán định tính chỉ tập trung vào 20 ca lỗi tự tin nhất, chưa bao quát toàn bộ 599 ca lỗi của BERT;  
>   3. Chi phí suy luận trên CPU (BERT CPU inference cost): Tốc độ ~12.85 mẫu/s chậm hơn nhiều so với baseline, cần tài nguyên GPU khi đưa vào sản xuất quy mô lớn;  
>   4. Cắt cụt chuỗi (Sequence truncation): 3.93% văn bản trong tập Train + Validation vượt quá ngưỡng MAX_LENGTH=128.  
> - **3 Hướng phát triển tương lai (thẻ phải):**  
>   1. Phân tích cảm xúc theo khía cạnh (ABSA): Nhận diện cảm xúc chi tiết theo từng thực thể như vị trí, phòng ốc, phục vụ;  
>   2. Tối ưu hóa & nén mô hình (Efficient/distilled models): Áp dụng DistilBERT, TinyBERT hoặc ONNX Runtime để tăng tốc suy luận;  
>   3. Mở rộng đa ngữ & Tiếng Việt (Vietnamese / multilingual extension): Thử nghiệm PhoBERT trên dữ liệu khách sạn Việt Nam.  
> Cuối cùng, 3 kết luận cốt lõi là: Quy trình có kiểm soát và báo cáo minh bạch giao thoa dữ liệu; BERT vượt Baseline +2.89 điểm phần trăm Accuracy và +0.0291 Macro F1; các mẫu lỗi được kiểm toán thường liên quan cảm xúc pha trộn và khả năng mơ hồ nhãn."*

---

### Slide 13: Kết Luận & Phiên Hỏi Đáp (Q&A) (09:30 - 10:00)
> *"Kính thưa Quý Thầy/Cô trong Hội đồng và các bạn sinh viên,  
> Trên đây là toàn bộ nội dung báo cáo đề tài nghiên cứu và ứng dụng mô hình BERT cho bài toán phân loại cảm xúc đánh giá khách sạn trong học phần Trí tuệ Nhân tạo của nhóm chúng em.  
> Chúng em xin chân thành cảm ơn Quý Thầy/Cô đã dành thời gian quý báu lắng nghe và theo dõi.  
> Sau đây, nhóm em kính mời Quý Thầy/Cô và Hội đồng đặt câu hỏi và đưa ra những lời góp ý quý báu để chúng em hoàn thiện nghiên cứu tốt hơn nữa. Em xin trân trọng cảm ơn!"*
