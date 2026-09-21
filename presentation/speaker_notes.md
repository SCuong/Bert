# Kịch Bản Thuyết Trình Bảo Vệ Đồ Án (Speaker Notes)

**Đề tài:** Ứng Dụng Mô Hình BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn  
**Môn học:** Trí tuệ Nhân tạo (AI)  
**Thời lượng trình bày chuẩn:** 8 - 10 phút  
**Gợi ý cho sinh viên:** Giữ giọng nói tự tin, mạch lạc; chỉ tay vào các biểu đồ và số liệu thực nghiệm trên slide; nhấn mạnh vào tính khoa học, tính trung thực học thuật và việc khắc phục triệt để các sai lầm kỹ thuật của mô hình cũ.

---

### Slide 1: Giới thiệu (00:00 - 00:30)
> *"Kính thưa Quý Thầy/Cô trong Hội đồng và các bạn sinh viên,*  
> *Hôm nay, em xin đại diện nhóm trình bày đồ án môn học Trí tuệ Nhân tạo với đề tài: **'Ứng Dụng Mô Hình BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn' (Fine-Tuning BERT for Hotel Review Sentiment Classification)**.*  
> *Đồ án của chúng em được triển khai mới hoàn toàn từ đầu, tuân thủ chặt chẽ 6 giai đoạn chuẩn mực của **AI Project Cycle** do giảng viên hướng dẫn. Mọi kết quả và số liệu trong bài báo cáo đều được trích xuất từ các tệp artifact thực nghiệm có thể kiểm chứng, tái lập và giải thích rõ ràng."*

---

### Slide 2: Bối cảnh & Mục tiêu nghiên cứu (00:30 - 01:15)
> *"Về bối cảnh thực tế, trên các nền tảng du lịch trực tuyến như Booking.com, mỗi ngày có hàng chục ngàn bài đánh giá của khách hàng được đăng tải. Việc phân loại thủ công cảm xúc khách hàng là bất khả thi về mặt nhân lực và thiếu tính kịp thời.  
> Mục tiêu cốt lõi của đồ án là xây dựng một hệ thống AI tự động phân loại nhận xét của khách lưu trú thành hai lớp: Tích cực (1) hoặc Tiêu cực (0) kèm xác suất tin cậy.  
> Bám sát giai đoạn 'Scope & Plan' trong AI Project Cycle, chúng em xác định rõ các bên liên quan gồm ban quản lý khách sạn, khách hàng và kỹ sư AI; đồng thời đặt ra 4 mục tiêu kỹ thuật: Xây dựng baseline chuẩn xác, fine-tuning BERT đúng chuẩn học thuật, đánh giá đối đầu khách quan trên Held-Out Test Set 3,949 mẫu, và phân tích định tính chuyên sâu các ca dự đoán sai."*

---

### Slide 3: Tiến hóa kiến trúc: Từ RNN/LSTM đến Transformer (01:15 - 02:00)
> *"Trước khi đi vào mô hình cụ thể, chúng em xin tóm lược bước chuyển dịch công nghệ trong Xử lý Ngôn ngữ Tự nhiên.  
> Trước năm 2017, các mô hình mạng nơ-ron tuần tự như RNN và LSTM là tiêu chuẩn hàng đầu. Tuy nhiên, chúng có hai điểm nghẽn lớn:  
> Thứ nhất là 'Sequential Recurrence Bottleneck': Muốn xử lý từ thứ t, mô hình bắt buộc phải đợi trạng thái ẩn của từ thứ t-1, khiến việc tính toán không thể song song hóa trên GPU, thời gian huấn luyện rất lâu.  
> Thứ hai là hiện tượng suy giảm thông tin ngữ cảnh xa (Vanishing Gradient): Qua các bước đệ quy dài, thông tin ở đầu câu bị suy giảm hoặc méo mó.  
> Năm 2017, kiến trúc Transformer ra đời với bài báo 'Attention Is All You Need', loại bỏ hoàn toàn đệ quy tuần tự, cho phép tính toán song song toàn bộ chuỗi văn bản trong cùng một tầng và kết nối trực tiếp mọi cặp từ thông qua cơ chế Self-Attention với độ dài đường truyền O(1)."*

---

### Slide 4: Kiến trúc BERT & Cơ chế Multi-Head Self-Attention (02:00 - 03:00)
> *"Năm 2018, Google giới thiệu mô hình BERT. Điểm khác biệt mấu chốt là BERT chỉ sử dụng khối **Encoder** của Transformer và là mô hình ngữ cảnh hai chiều thực sự (Deeply Bidirectional).  
> Cơ chế tính toán trung tâm là Scaled Dot-Product Attention: Mỗi từ được biểu diễn qua bộ ba vector Query (Q), Key (K) và Value (V). Tích vô hướng giữa Q và K, chia cho căn bậc hai của d_k và chuẩn hóa qua Softmax, sẽ xác định trọng số chú ý giữa các từ trong câu.  
> Với 12 đầu chú ý độc lập (Multi-Head Attention), BERT có thể đồng thời học được nhiều mối quan hệ ngôn ngữ phức tạp như cấu trúc chủ-vị, đại từ thay thế và các biểu thức phủ định.  
> Hai token đặc biệt là [CLS] ở đầu câu (làm vector đại diện phân loại) và [SEP] ở cuối câu."*

---

### Slide 5: Phân tích khám phá dữ liệu (Data & EDA) (03:00 - 04:00)
> *"Bám sát giai đoạn 'Data' trong AI Project Cycle, chúng em sử dụng tập dữ liệu 20,000 đánh giá khách sạn do giảng viên cung cấp.  
> Qua quy trình kiểm toán tự động (Data Audit), chúng em loại bỏ 255 mẫu gồm 5 mẫu rỗng, 127 mẫu xung đột nhãn (từ 20 đoạn văn bản giống hệt nhau nhưng mang cả nhãn 0 và 1), và 123 mẫu trùng lặp hoàn toàn, thu được **19,745 mẫu sạch duy nhất** (50.25% Negative, 49.75% Positive).  
> Phân chia dữ liệu theo Stratified Split (Seed 42) thành Train 70% (13,821 mẫu), Validation 10% (1,975 mẫu) và Test 20% (3,949 mẫu), xác nhận 0% rò rỉ dữ liệu giữa các tập.  
> Đặc biệt, chúng em đo lường phân vị độ dài token BERT thực tế trên tập Train+Val (15,796 mẫu): Trung vị là 30 tokens, trung bình 42.33 tokens, phân vị p95 là 121 tokens. Quyết định chọn **MAX_LENGTH = 128** bảo toàn trọn vẹn 96.07% số văn bản trong tập dữ liệu (chỉ cắt cụt 3.93%), giúp tối ưu hóa chi phí tính toán bậc hai O(L^2) và bộ nhớ kích hoạt so với ngưỡng 256."*

---

### Slide 6: Quy trình nghiên cứu chuẩn mực (04:00 - 04:45)
> *"Để đảm bảo tính khoa học và ngăn chặn rò rỉ dữ liệu (No Data Leakage), quy trình nghiên cứu của nhóm được chia làm 3 khối rõ ràng:  
> Khối 1: Tiền xử lý bảo toàn ngữ cảnh: Giữ nguyên từ phủ định ('not', 'never'), dấu câu và cấu trúc ngữ pháp tự nhiên.  
> Khối 2: Mô hình hóa: Bắt đầu từ mô hình cơ sở TF-IDF + Logistic Regression để làm mốc đối sánh, sau đó phát triển mô hình chính Fine-Tuned BERT.  
> Khối 3: Đánh giá độc lập: Tập kiểm thử (Test Set: 3,949 mẫu) được niêm phong hoàn toàn trong quá trình phát triển và chỉ được mở ra đánh giá đối đầu đúng 1 lần duy nhất khi cả hai mô hình đã đóng băng tham số."*

---

### Slide 7: Mô hình cơ sở: TF-IDF + Logistic Regression (04:45 - 05:30)
> *"Theo đúng nguyên tắc phương pháp luận ở Slide 9 trong AI Project Cycle: 'Start from simple to more complex models', chúng em không vội áp dụng ngay Deep Learning mà xây dựng mô hình cơ sở: **TF-IDF kết hợp Logistic Regression**.  
> Cấu hình: Trích xuất 10,000 unigrams và bigrams với thang đo Sublinear TF, kết hợp thuật toán tối ưu L-BFGS.  
> Kết quả trên tập Test Set độc lập (3,949 mẫu): Mô hình đạt Accuracy **81.94%**, Macro Precision 0.8208, Macro Recall 0.8193, Macro F1 **0.8192**.  
> Điểm mạnh vượt trội của mô hình cơ sở là tốc độ: Huấn luyện chỉ mất 0.68 giây và suy luận đạt hơn 28,700 mẫu/giây trên CPU. Đây là mốc đối sánh vững chắc để kiểm chứng năng lực thực sự của Transformer."*

---

### Slide 8: Phân tích sự cố mô hình cũ & Khác biệt pipeline mới (05:30 - 06:45)
> *"Một đóng góp quan trọng của nhóm là khảo sát và làm rõ nguyên nhân vì sao trong notebook tham khảo của môn học (`DL_Model.ipynb`), mô hình 'BERT' chỉ đạt kết quả rất thấp là **65.20% Accuracy**, thua cả NNLM (79%) và BiLSTM (75%).  
> Nhóm đã tìm ra 5 sai lầm kỹ thuật nghiêm trọng trong code cũ:  
> 1. Lệch từ điển: Preprocessing cased ghép với encoder uncased.  
> 2. Đóng băng Encoder (`trainable=False`), chỉ coi BERT như bộ trích xuất đặc trưng tĩnh.  
> 3. Learning Rate 1e-3, quá lớn gấp 50 lần chuẩn, phá hủy hoàn toàn trọng số tiền huấn luyện.  
> 4. Head quá sâu (5 tầng Dense liên tiếp không Dropout).  
> 5. Huấn luyện 100 epochs dẫn đến overfitting cực độ: Train Acc đạt 97% nhưng Test Acc sụp đổ về 65.20%.  
> Pipeline mới của nhóm khắc phục triệt để: Đồng bộ uncased, Full Fine-Tuning 110M tham số, AdamW với LR 2e-5 + Warmup, 1 tầng Linear + Dropout(0.1), và huấn luyện 3 epochs có kiểm soát checkpoint."*

---

### Slide 9: Quá trình huấn luyện & Động lực học tập của BERT (06:45 - 07:30)
> *"Về quá trình huấn luyện BERT: Do môi trường thực thi sử dụng PyTorch CPU (`2.14.0+cpu`), 3 epochs huấn luyện (2,592 steps) diễn ra trong **15,617.19 giây (~4.34 giờ)**.  
> Động lực học tập ghi nhận: Train Loss giảm liên tục từ 0.4077 xuống 0.2885 và 0.1983.  
> Trên tập Validation: Macro F1 tăng liên tục từ 0.8359 ở Epoch 1 lên 0.8384 ở Epoch 2 và đạt đỉnh **0.8389** ở Epoch 3.  
> Điểm thú vị là ở Epoch 3, Validation Loss tăng nhẹ lên 0.4503 trong khi Macro F1 lại đạt giá trị cao nhất. Đây là hiện tượng bình thường khi Cross-Entropy phạt nặng xác suất ở một số ít mẫu biên khó hoặc có nhãn nhiễu, trong khi phần lớn mẫu được phân loại chuẩn xác hơn. Việc nhóm lựa chọn Checkpoint theo Validation Macro F1 (`checkpoint-2592`) là hoàn toàn chuẩn xác về mặt khoa học."*

---

### Slide 10: Kết quả thực nghiệm đối đầu trên Test Set (07:30 - 08:15)
> *"Kính thưa Thầy/Cô, đây là bảng so sánh kết quả thực nghiệm đối đầu chính thức trên cùng tập kiểm thử độc lập Held-Out Test Set (3,949 mẫu):  
> - **Mô hình cơ sở (TF-IDF + Logistic Regression):** Đạt Accuracy 81.94%, Macro F1 0.8192.  
> - **Mô hình chính (Fine-Tuned BERT):** Đạt Accuracy **84.83%**, Macro Precision 0.8486, Macro Recall 0.8482, Macro F1 **0.8483**.  
> - **Mức độ cải thiện:** BERT vượt Baseline **+2.89 điểm phần trăm Accuracy** và **+0.0291 Macro F1**.  
> So với kết quả 65.20% trong notebook cũ môn học, pipeline mới của nhóm đạt 84.83%, cải thiện vượt bậc **+19.63 điểm phần trăm**, khôi phục trọn vẹn vị thế vượt trội của BERT như lý thuyết đã khẳng định."*

---

### Slide 11: Ma trận nhầm lẫn & So sánh chi tiết từng lớp (08:15 - 08:45)
> *"Quan sát ma trận nhầm lẫn của hai mô hình trên 3,949 mẫu Test Set:  
> - Ở lớp Tiêu cực: BERT nhận diện chính xác 1,711 mẫu (tăng 20 mẫu so với Baseline).  
> - Ở lớp Tích cực: BERT nhận diện chính xác 1,639 mẫu (tăng 94 mẫu so với Baseline).  
> - Đáng chú ý nhất, số ca False Negative (bỏ sót đánh giá tích cực thành tiêu cực) của BERT **giảm mạnh 94 ca**, từ 420 ca ở Baseline xuống chỉ còn 326 ca ở BERT — tương đương mức giảm tới **22.38%**!  
> Tổng số lỗi dự đoán sai trên toàn bộ tập kiểm thử giảm từ 713 ca xuống 599 ca (giảm 114 ca lỗi)."*

---

### Slide 12: Báo cáo phân tích lỗi định tính (08:45 - 09:30)
> *"Để hiểu rõ bản chất 599 ca lỗi của BERT, nhóm đã khảo sát định tính chi tiết **mẫu 20 ca lỗi có độ tin cậy cao nhất (10 FP, 10 FN)** trích xuất từ `error_cases.json`.  
> Thống kê trên mẫu 20 ca khảo sát cho thấy:  
> - 15/20 ca (75%) xuất phát từ 'Mixed Sentiment': Khách khen vị trí nhưng chê cách âm và vệ sinh. Việc ép bài viết đa khía cạnh vào một nhãn nhị phân tạo ra tính mơ hồ cố hữu.  
> - 8/20 ca (40%) mang dấu hiệu mâu thuẫn nhãn rõ rệt (ví dụ: bài viết kết thúc bằng thẻ 'No Positive' và toàn lời bức xúc nhưng nhãn lại là 1). Ở các ca này, dự đoán của BERT thực chất phản ánh đúng ngữ nghĩa bài viết hơn nhãn trong dữ liệu.  
> - Đặc biệt, **0/20 ca bị cắt cụt** (độ dài token tối đa chỉ 126 <= 128). Điều này khẳng định cắt cụt không phải là nguyên nhân gây ra các ca lỗi cực đoan nhất được khảo sát."*

---

### Slide 13: Ứng dụng Demo Streamlit (09:30 - 10:00)
> *"Nhóm cũng đã đóng gói toàn bộ mô hình thành ứng dụng Web trực quan bằng Streamlit (`app/app.py`).  
> Ứng dụng cho phép so sánh đối đầu song song giữa Baseline và BERT trên cùng một văn bản.  
> Khi thử nghiệm với các câu đánh giá phức tạp:  
> - Câu có litotes: 'The room was not bad, actually quite comfortable' -> BERT dự đoán chính xác Positive, trong khi TF-IDF bị nhiễu bởi từ 'bad'.  
> - Câu đảo ngữ: 'Not a single complaint about the wonderful staff' -> BERT hiểu 'Not a single' đảo nghĩa 'complaint', trong khi TF-IDF phân loại nhầm sang Negative.  
> Giao diện còn trực quan hóa các token con WordPiece (`##`), giúp giải thích sinh động cơ chế hoạt động của BERT cho người dùng."*

---

### Slide 14 & 15: Giới hạn, Hướng phát triển & Kết luận (10:00 - 10:30)
> *"Về giới hạn: Đồ án hiện chỉ giải quyết bài toán nhị phân, và tốc độ suy luận của BERT trên CPU (~12.85 mẫu/s) chậm hơn nhiều so với mô hình tuyến tính. Hướng phát triển tiếp theo là triển khai Phân tích Cảm xúc Đa Khía cạnh (ABSA) và nén mô hình bằng DistilBERT hoặc ONNX Runtime.  
> Tóm lại, đồ án đã hoàn thành trọn vẹn quy trình AI Project Cycle, phục hồi thành công tiềm năng của BERT, chứng minh tính vượt trội qua số liệu thực nghiệm trung thực và đóng gói sản phẩm hoàn chỉnh.  
> Em xin chân thành cảm ơn Quý Thầy Cô và Hội Đồng đã chú ý lắng nghe. Nhóm em rất mong nhận được những câu hỏi và đóng góp quý báu từ Thầy Cô!"*
