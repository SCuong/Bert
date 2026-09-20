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
> *"Về bối cảnh, trên các nền tảng đánh giá khách sạn trực tuyến, mỗi ngày có hàng chục ngàn đánh giá mới. Việc phân loại thủ công cảm xúc khách hàng là bất khả thi về mặt nhân lực.  
> Mục tiêu của đồ án là xây dựng một hệ thống AI tự động phân loại nhận xét của khách hàng thành hai sắc thái: Tích cực hoặc Tiêu cực.  
> Bám sát giai đoạn 'Scope & Plan' trong AI Project Cycle, chúng em xác định rõ các bên liên quan gồm ban quản lý khách sạn và khách hàng, đồng thời đặt ra các tiêu chí cốt lõi: Pipeline đúng chuẩn học thuật, đánh giá không rò rỉ dữ liệu (Zero Data Leakage), so sánh đối đầu công bằng giữa Baseline và BERT, kiểm soát tính tái lập qua cố định seed 42 và giải thích sâu sắc các ca lỗi thực nghiệm."*

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
> Qua quy trình kiểm toán dữ liệu (Data Audit), chúng em loại bỏ 255 mẫu gồm 5 mẫu rỗng, 127 mẫu xung đột nhãn và 123 mẫu trùng lặp văn bản, thu được 19,745 mẫu sạch duy nhất (9,921 Negative, 9,824 Positive).  
> Để chọn độ dài chuỗi tối ưu, chúng em đo lường trực tiếp bằng Tokenizer WordPiece của BERT trên tập Train+Val (15,796 mẫu) để giữ tập Test hoàn toàn độc lập. Kết quả thực nghiệm cho thấy: độ dài trung bình là 42.33 tokens, trung vị 30 tokens, và phân vị 95 là 121 tokens.  
> Với ngưỡng MAX_LENGTH = 128, chúng em bảo toàn trọn vẹn 96.07% toàn bộ văn bản (chỉ cắt cụt 3.93%), vừa tối ưu hóa chi phí tính toán O(L^2) vừa đảm bảo an toàn bộ nhớ trên GPU 8GB VRAM mà không lo tràn bộ nhớ (OOM)."*

---

### Slide 6: Quy trình nghiên cứu chuẩn mực (04:00 - 04:45)
> *"Để đảm bảo tính khoa học và ngăn chặn rò rỉ dữ liệu (Data Leakage), chúng em thực hiện kiểm toán tiền phân chia (Pre-split Audit), loại bỏ các dòng thiếu, rỗng, xung đột nhãn và trùng lặp hoàn toàn.  
> Sau đó phân chia dữ liệu thành Train (70%), Validation (10%) và Test (20%) theo Stratified Split, cố định random seed 42 và kiểm tra giao tập (Zero Overlap).  
> Tập Test hoàn toàn độc lập, chỉ được nạp đúng một lần khi đánh giá mô hình cuối cùng."*

---

### Slide 7: Mô hình cơ sở (Baseline): TF-IDF + Logistic Regression (04:45 - 05:30)
> *"Theo đúng lời dạy trong slide bài giảng: 'We should start from simple to more complex models', chúng em không vội vàng áp dụng ngay Deep Learning mà xây dựng mô hình cơ sở: **TF-IDF kết hợp Logistic Regression**.  
> Mô hình baseline đạt độ chính xác khá tốt và thời gian huấn luyện cực kỳ nhanh. Đây là mốc đối sánh vững chắc để trả lời câu hỏi nghiên cứu số 1: 'Liệu sự phức tạp của BERT có thực sự đem lại giá trị vượt trội so với giải pháp tuyến tính compact?'"*

---

### Slide 8: Thiết kế thực nghiệm & Chiến lược Fine-Tuning (05:30 - 06:45)
> *"Tiếp theo, chúng em thiết kế thực nghiệm Fine-tuning cho mô hình BERT:  
> Lựa chọn mô hình nền tảng `google-bert/bert-base-uncased` với 12 tầng Transformer, 768 chiều ẩn và 110 triệu tham số.  
> Đồng bộ tuyệt đối Tokenizer và Model uncased.  
> Cập nhật toàn bộ trọng số Encoder (True Fine-Tuning) để mô hình thích ứng với ngôn ngữ đánh giá khách sạn.  
> Cấu hình bộ tối ưu hóa AdamW với Weight Decay 0.01, tốc độ học chuẩn 2e-5 kết hợp Linear Warmup Scheduler trong 10% số bước.  
> Huấn luyện có kiểm soát trong 2-3 epochs, tự động lưu và phục hồi checkpoint có Validation Macro F1 tốt nhất."*

---

### Slide 9: Triển khai kỹ thuật Fine-Tuning BERT (06:45 - 07:30)
> *"Về mặt triển khai kỹ thuật, nhóm xây dựng pipeline thuần PyTorch:  
> Kế thừa trực tiếp `torch.utils.data.Dataset`, loại bỏ hoàn toàn phụ thuộc vào thư viện ngoài `datasets`.  
> Tương thích với API Hugging Face Transformers hiện đại qua tham số `processing_class`.  
> Trong quá trình huấn luyện, nhóm ghi nhận chi tiết cả đường cong Train Loss và Validation Loss qua từng epoch để phát hiện sớm hiện tượng phân kỳ (Overfitting).  
> Toàn bộ artifacts gồm trọng số, metrics JSON và biểu đồ 300 DPI đều được quản lý tự động và có cấu trúc rõ ràng."*

---

### Slide 10: Kết quả thực nghiệm tổng hợp (07:30 - 08:30)
> *"Kính thưa Thầy/Cô, đây là bảng kết quả thực nghiệm tổng hợp trên cùng tập kiểm thử Test Set:  
> Trọng tâm của bài toán là đối sánh giữa Baseline TF-IDF + Logistic Regression và Fine-Tuned BERT của nhóm.  
> [Trình bày các con số thực tế từ bảng so sánh sau khi chạy thực nghiệm]:  
> - Baseline TF-IDF + Logistic Regression đạt Accuracy ...%, Macro F1 ...  
> - Mô hình Fine-Tuned BERT của chúng em đạt Accuracy ...%, Macro F1 ...  
> Ngoài ra, để tham khảo ngữ cảnh môn học, các kết quả lịch sử ghi nhận trong notebook `DL_Model.ipynb` cho thấy NNLM đạt Accuracy 79.00%, BiLSTM đạt 75.00%, và mô hình BERT cũ chỉ đạt 65.20% (do bị đóng băng encoder và lệch tokenizer). Các chỉ số khác của các mô hình tham khảo này không được tài liệu cũ báo cáo."*

---

### Slide 11: Ma trận nhầm lẫn & Đánh giá chi tiết (08:30 - 09:00)
> *"Quan sát ma trận nhầm lẫn trên tập kiểm thử độc lập (được sinh tự động sau khi chạy mô hình), chúng em phân tích chi tiết mức độ cân bằng ở cả hai lớp:  
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
> *"Tóm lại, đồ án đã hoàn thành các mục tiêu đề ra: Xây dựng pipeline xử lý dữ liệu và mô hình hóa chuẩn mực không rò rỉ, đánh giá đối đầu công bằng giữa Baseline và Fine-Tuned BERT, và cung cấp đầy đủ tài liệu học tập cùng sản phẩm demo trực quan.  
> Em xin chân thành cảm ơn Thầy/Cô và các bạn đã chú ý lắng nghe. Nhóm em rất mong nhận được những câu hỏi nhận xét và góp ý từ Hội đồng!"*
