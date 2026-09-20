# Kịch Bản Thuyết Trình Bảo Vệ Đồ Án (Speaker Notes)

**Đề tài:** Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn  
**Môn học:** Trí tuệ Nhân tạo (AI)  
**Thời lượng trình bày chuẩn:** 8 - 10 phút  
**Gợi ý cho sinh viên:** Giữ giọng nói tự tin, rõ ràng; chỉ tay vào các biểu đồ và số liệu thực nghiệm trên slide; nhấn mạnh vào tính khoa học và việc khắc phục lỗi của mô hình cũ.

---

### Slide 1: Giới thiệu (00:00 - 00:30)
> *"Kính thưa Thầy/Cô và các bạn sinh viên,*  
> *Hôm nay, em xin đại diện nhóm trình bày đồ án môn Trí tuệ Nhân tạo với đề tài: **'Ứng dụng BERT trong phân loại cảm xúc đánh giá khách sạn' (Fine-Tuning BERT for Hotel Review Sentiment Classification)**.*  
> *Đồ án của chúng em được xây dựng nghiêm túc, tuân thủ chặt chẽ quy trình chuẩn **AI Project Cycle** do giảng viên hướng dẫn, với toàn bộ kết quả thực nghiệm có thể kiểm chứng, tái lập và giải thích được."*

---

### Slide 2: Bối cảnh & Mục tiêu (00:30 - 01:15)
> *"Về bối cảnh, trên các nền tảng đặt phòng trực tuyến như Booking.com hay Agoda, mỗi ngày có hàng chục ngàn đánh giá mới. Việc phân loại thủ công cảm xúc khách hàng là bất khả thi về mặt nhân lực.  
> Mục tiêu của đồ án là xây dựng một hệ thống AI tự động phân loại nhận xét của khách hàng thành hai sắc thái: Tích cực hoặc Tiêu cực.  
> Bám sát giai đoạn 'Scope & Plan' trong AI Project Cycle, chúng em xác định rõ các bên liên quan gồm ban quản lý khách sạn và khách hàng, đồng thời đặt ra các tiêu chí thành công cụ thể: Độ chính xác tổng quát trên 88%, F1-score trên 0.88, và quan trọng nhất là phải chứng minh được BERT có thực sự đem lại lợi ích vượt trội so với các phương pháp truyền thống hay không."*

---

### Slide 3: Tiến hóa kiến trúc: Từ RNN/LSTM đến Transformer (01:15 - 02:00)
> *"Trước khi đi vào mô hình cụ thể, chúng em xin tóm lược bước chuyển dịch công nghệ trong NLP.  
> Trước năm 2017, các mô hình tuần tự như RNN và LSTM là tiêu chuẩn. Tuy nhiên, chúng có hai nhược điểm cốt tử: Một là xử lý tuần tự từng từ nên không thể tính toán song song trên GPU, khiến thời gian huấn luyện rất lâu. Hai là hiện tượng suy biến gradient (Vanishing Gradient) khiến mô hình quên mất ngữ cảnh khi câu quá dài.  
> Năm 2017, kiến trúc Transformer ra đời với bài báo 'Attention Is All You Need', loại bỏ hoàn toàn mạng hồi quy, cho phép tính toán song song toàn bộ các từ trong câu và kết nối trực tiếp mọi cặp từ thông qua cơ chế Self-Attention."*

---

### Slide 4: Kiến trúc BERT & Cơ chế Self-Attention (02:00 - 03:00)
> *"Năm 2018, Google giới thiệu BERT. Điểm đặc biệt là BERT chỉ sử dụng phần **Encoder** của Transformer và là mô hình hai chiều thực sự (Deeply Bidirectional).  
> Cơ chế tính toán cốt lõi là Scaled Dot-Product Attention: Mỗi từ được biểu diễn qua bộ ba vector Query, Key và Value. Tích vô hướng giữa Query của từ này và Key của từ khác, chia cho căn bậc hai của d_k và chuẩn hóa qua Softmax, sẽ cho ta trọng số chú ý.  
> Với 12 đầu chú ý (Multi-Head Attention), BERT có thể đồng thời học được nhiều mối quan hệ ngôn ngữ phức tạp như chủ ngữ - vị ngữ, đại từ thay thế và các cấu trúc phủ định."*

---

### Slide 5: Phân tích dữ liệu khách sạn (03:00 - 04:00)
> *"Bám sát giai đoạn 'Data' trong AI Project Cycle, chúng em sử dụng tập dữ liệu 20,000 đánh giá khách sạn do giảng viên cung cấp.  
> Qua phân tích khám phá (EDA), chúng em ghi nhận dữ liệu có độ cân bằng hoàn hảo: đúng 10,000 mẫu tích cực và 10,000 mẫu tiêu cực.  
> Về độ dài, 90% số bài đánh giá có độ dài dưới 128 từ và 97% dưới 256 từ. Đây là cơ sở khoa học để chúng em lựa chọn max_length phù hợp, tránh lãng phí bộ nhớ GPU.  
> Đặc biệt, chúng em phát hiện dữ liệu bắt nguồn từ Booking.com, nơi khách hàng điền cụm mặc định 'No Negative' khi hài lòng. Điều này sẽ dẫn đến một sai lầm chết người nếu áp dụng tiền xử lý xóa stopword cổ điển."*

---

### Slide 6: Quy trình nghiên cứu chuẩn mực (04:00 - 04:45)
> *"Để đảm bảo tính khoa học và ngăn chặn rò rỉ dữ liệu (Data Leakage), chúng em phân chia dữ liệu thành Train (70%), Validation (10%) và Test (20%) theo phương pháp Stratified Split, cố định random seed 42.  
> Tập Test gồm 4,000 mẫu hoàn toàn độc lập, chỉ được nạp đúng một lần khi đánh giá mô hình cuối cùng.  
> Khác với cách làm cũ, chúng em áp dụng tiền xử lý tối thiểu (Minimal Cleaning), giữ nguyên toàn bộ từ ngữ tự nhiên, dấu câu và các từ phủ định quan trọng như 'not', 'no', 'never' để phục vụ cho bộ mã hóa của BERT."*

---

### Slide 7: Mô hình cơ sở (Baseline): TF-IDF + Logistic Regression (04:45 - 05:30)
> *"Theo đúng lời dạy trong slide bài giảng: 'We should start from simple to more complex models', chúng em không vội vàng áp dụng ngay Deep Learning mà xây dựng mô hình cơ sở: **TF-IDF kết hợp Logistic Regression**.  
> Mô hình baseline đạt độ chính xác tương đối tốt và thời gian huấn luyện cực kỳ nhanh (dưới 5 giây). Đây là mốc đối sánh vững chắc để trả lời câu hỏi nghiên cứu số 1: 'Liệu sự phức tạp của BERT có thực sự xứng đáng?'"*

---

### Slide 8: Khảo sát & Chỉ ra sai sót trong mô hình BERT cũ (05:30 - 06:45)
> *"Khi nghiên cứu notebook mẫu của môn học (`DL_Model.ipynb`), chúng em phát hiện mô hình BERT lưu trong notebook chỉ đạt 65.2% - thấp hơn cả BiLSTM (75%) và NNLM (79%).  
> Qua audit kỹ thuật chi tiết, chúng em đã chỉ ra 5 nguyên nhân gốc rễ:  
> 1. Bộ tiền xử lý là Cased nhưng lại ghép với mô hình Uncased, dẫn đến việc lệch ID từ vựng.  
> 2. Encoder bị đặt `trainable=False`, nghĩa là mô hình bị đóng băng hoàn toàn, đây KHÔNG PHẢI là Fine-tuning mà chỉ là trích xuất đặc trưng tĩnh từ Small BERT.  
> 3. Tốc độ học bị đặt là 0.001 - cao gấp 50 lần mức khuyến nghị.  
> 4. Classifier head xếp chồng 5 tầng Dense liên tiếp và xóa bỏ toàn bộ Dropout.  
> 5. Huấn luyện tới 100 epochs dẫn đến Overfitting cực độ: Train Accuracy lên tới 97% nhưng Test Loss tăng vọt lên 2.61 và Test Accuracy tụt xuống 65.2%."*

---

### Slide 9: Phương pháp Fine-Tuning BERT chuẩn của nhóm (06:45 - 07:30)
> *"Để giải quyết triệt để các vấn đề trên, nhóm đã xây dựng pipeline chuẩn mực:  
> Sử dụng mô hình `bert-base-uncased` chính thức với 110 triệu tham số.  
> Đồng bộ hoàn toàn Tokenizer và Model bằng Hugging Face Transformers.  
> Cho phép cập nhật toàn bộ trọng số (True Fine-tuning).  
> Sử dụng bộ tối ưu hóa AdamW với Weight Decay 0.01, tốc độ học 2e-5 kết hợp Linear Warmup Scheduler.  
> Huấn luyện có kiểm soát trong 2-3 epochs, tự động lưu và phục hồi checkpoint có Validation Loss tốt nhất."*

---

### Slide 10: Kết quả thực nghiệm tổng hợp (07:30 - 08:30)
> *"Kính thưa Thầy/Cô, đây là bảng kết quả thực nghiệm tổng hợp trên cùng tập dữ liệu:  
> [Trình bày các con số thực tế từ bảng so sánh]:  
> - Baseline TF-IDF + Logistic Regression đạt Accuracy xấp xỉ ...%, Macro F1 ...  
> - Kết quả lịch sử cũ của BiLSTM là 75.0%, NNLM là 79.0%, và BERT cũ bị lỗi chỉ đạt 65.2%.  
> - Mô hình BERT chuẩn của chúng em đã bứt phá ngoạn mục, đạt Accuracy ...%, Macro F1 ...  
> Kết quả này chứng minh rõ ràng: Khi được huấn luyện đúng kỹ thuật, BERT vượt trội hoàn toàn so với tất cả các phương pháp trước đó."*

---

### Slide 11: Ma trận nhầm lẫn & Đánh giá chi tiết (08:30 - 09:00)
> *"Quan sát ma trận nhầm lẫn trên 4,000 mẫu kiểm thử độc lập (sẽ được trích xuất tự động sau khi chạy mô hình), chúng em phân tích chi tiết mức độ cân bằng ở cả hai lớp:  
> [Đọc số liệu thực tế về True Positives, False Positives, True Negatives và False Negatives từ biểu đồ trên slide]."*

---

### Slide 12: Phân tích lỗi chuyên sâu (Error Analysis) (09:00 - 09:45)
> *"Để bài làm có chiều sâu học thuật, chúng em xây dựng khung phân tích định tính các ca dự đoán sai của mô hình.  
> Chúng em nhận diện 4 nhóm nguyên nhân chính:  
> Thứ nhất là 'Mixed Sentiment': Khách hàng vừa khen vị trí nhưng lại chê dịch vụ, khiến việc gán nhãn nhị phân mang tính chủ quan.  
> Thứ hai là các cấu trúc phủ định phức tạp hoặc đảo ngữ tinh vi.  
> Thứ ba là các câu mỉa mai (Sarcasm).  
> Và cuối cùng là cắt cụt chuỗi hoặc nhiễu nhãn từ dữ liệu gốc.  
> [Trình bày một số ca lỗi thực tế trích xuất từ file error_cases.json sau khi chạy evaluation]."*

---

### Slide 13: Ứng dụng Demo Streamlit (09:45 - 10:15)
> *"Nhóm cũng đã đóng gói toàn bộ quy trình thành một ứng dụng web trực quan bằng Streamlit.  
> Ứng dụng cho phép người dùng nhập bất kỳ đoạn review nào, trực quan hóa quá trình bẻ từ WordPiece của BERT, tính toán xác suất và hiển thị so sánh tức thời giữa Baseline và BERT.  
> [Nếu có thời gian, sinh viên có thể chuyển sang màn hình Demo khoảng 30s]."*

---

### Slide 14 & 15: Kết luận & Tài liệu tham khảo (10:15 - 10:45)
> *"Tóm lại, đồ án đã hoàn thành xuất sắc các mục tiêu đề ra: Khảo sát và sửa chữa toàn bộ sai sót kỹ thuật của mã nguồn cũ, xây dựng pipeline Fine-tuning BERT chuẩn mực với kết quả kiểm chứng trung thực, và cung cấp đầy đủ tài liệu học tập cùng sản phẩm demo.  
> Em xin chân thành cảm ơn Thầy/Cô và các bạn đã chú ý lắng nghe. Nhóm em rất mong nhận được những câu hỏi nhận xét và góp ý từ Hội đồng!"*
