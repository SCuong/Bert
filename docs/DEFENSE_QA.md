# Bộ Câu Hỏi & Trả Lời Phản Biện Đồ Án (Defense Q&A)

**Dành cho sinh viên bảo vệ đồ án Trí tuệ Nhân tạo (AI)**  
**Đề tài:** Ứng dụng BERT trong phân loại cảm xúc đánh giá khách sạn  
**Quy cách trả lời:** Mỗi câu hỏi gồm **[Trả lời ngắn - 30s]** (trả lời nhanh, chuẩn xác, tự tin) và **[Trả lời mở rộng - 1-2 phút]** (chuyên sâu kỹ thuật, dẫn chứng số liệu thực nghiệm để gây ấn tượng với hội đồng).

---

### Câu 1: BERT viết tắt của từ gì và được công bố bởi ai, vào năm nào?
- **[Trả lời ngắn]:** BERT là viết tắt của **Bidirectional Encoder Representations from Transformers**, do nhóm nghiên cứu tại Google AI công bố vào tháng 10 năm 2018 (tác giả chính là Jacob Devlin và các cộng sự).
- **[Trả lời mở rộng]:** Bài báo gốc có tiêu đề *"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"*. Mô hình đánh dấu bước ngoặt lịch sử trong NLP khi phá vỡ kỷ lục tại 11 tác vụ ngôn ngữ tự nhiên tiêu chuẩn (như GLUE benchmark, SQuAD) nhờ khả năng nắm bắt ngữ cảnh hai chiều thực sự thông qua cơ chế Masked Language Modeling.

---

### Câu 2: BERT khác gì so với kiến trúc Transformer gốc trong bài báo "Attention Is All You Need"?
- **[Trả lời ngắn]:** Transformer gốc (2017) là một kiến trúc **Encoder-Decoder** đầy đủ phục vụ cho bài toán dịch máy. Còn BERT **chỉ sử dụng phần Encoder** của Transformer, chuyên trách nhiệm vụ thấu hiểu và biểu diễn ngữ nghĩa của văn bản.
- **[Trả lời mở rộng]:** Transformer gốc gồm các khối Encoder để trích xuất đặc trưng câu nguồn và Decoder tự hồi quy (dùng Masked Self-Attention) để sinh từng từ câu đích. Do bài toán phân loại cảm xúc chỉ cần hiểu nội dung chứ không cần sinh văn bản mới, BERT chỉ xếp chồng các tầng Encoder (12 tầng ở bản Base, 24 tầng ở bản Large) để tận dụng cơ chế Self-Attention hai chiều tự do ở mọi vị trí.

---

### Câu 3: Vì sao BERT chỉ sử dụng Encoder mà không dùng Decoder?
- **[Trả lời ngắn]:** Vì mục tiêu của BERT là hiểu ngôn ngữ (Language Understanding) và phân loại chuỗi (Classification), không phải là sinh văn bản tự hồi quy (Language Generation).
- **[Trả lời mở rộng]:** Decoder bắt buộc phải dùng Masked Self-Attention để che các từ phía sau (không cho nhìn tương lai), làm giảm khả năng nắm bắt toàn diện ngữ cảnh. Trong khi đó, Encoder cho phép một từ nhìn thấy đồng thời cả các từ đứng trước và đứng sau nó tại mọi tầng tính toán, tạo ra vector biểu diễn ngữ nghĩa hai chiều phong phú nhất cho tác vụ phân loại.

---

### Câu 4: Fine-tuning là gì? Nó khác gì so với Feature Extraction?
- **[Trả lời ngắn]:** Feature Extraction là đóng băng mô hình gốc và chỉ huấn luyện một bộ phân loại mới phía trên. Còn Fine-tuning là cập nhật **cả bộ phân loại mới và toàn bộ (hoặc phần lớn) trọng số của mô hình BERT gốc** với tốc độ học nhỏ.
- **[Trả lời mở rộng]:** Trong notebook cũ của môn học (`DL_Model.ipynb`), tác giả đặt `trainable=False`, đó chỉ là Feature Extraction. Trong đồ án này, chúng em thực hiện Full Fine-Tuning: các ma trận Query, Key, Value và Feed-Forward của tất cả 12 tầng Transformer đều được lan truyền ngược và tinh chỉnh nhẹ để thích ứng tối đa với miền từ vựng đánh giá khách sạn.

---

### Câu 5: Tại sao nhóm không huấn luyện mô hình BERT từ đầu (Train from Scratch)?
- **[Trả lời ngắn]:** Vì huấn luyện từ đầu đòi hỏi hàng tỷ từ ngữ, cụm siêu máy tính hàng chục ngàn USD, và tập dữ liệu 20,000 mẫu của đồ án quá nhỏ sẽ dẫn đến overfitting ngay lập tức.
- **[Trả lời mở rộng]:** BERT-base có 110 triệu tham số. Để các tham số này hội tụ mà không overfit, Google đã phải tiền huấn luyện trên 3.3 tỷ từ từ Wikipedia và BookCorpus trong nhiều ngày trên 64 chip TPU. Fine-tuning cho phép chúng em kế thừa toàn bộ tri thức ngôn ngữ đồ sộ đó. Trong thực nghiệm chính thức của nhóm trên môi trường CPU đa lõi (PyTorch `2.14.0+cpu`), 3 epochs huấn luyện diễn ra trong **15,617.19 giây (~4.34 giờ)**; hoặc có thể hoàn tất trong khoảng 15-20 phút nếu huấn luyện trên GPU như Google Colab T4.

---

### Câu 6: Token `[CLS]` được dùng để làm gì?
- **[Trả lời ngắn]:** `[CLS]` là token phân loại đặc biệt được chèn vào đầu mỗi chuỗi. Vector đầu ra tương ứng với vị trí `[CLS]` được dùng làm vector đại diện tổng quát cho toàn bộ câu để đưa vào lớp phân loại.
- **[Trả lời mở rộng]:** Do cơ chế Self-Attention của Transformer kết nối tất cả các token với nhau, token `[CLS]` sau 12 tầng mã hóa đã thu thập và tổng hợp thông tin từ mọi từ trong câu. Ta chỉ cần lấy vector ẩn tại vị trí này ($h_{\text{[CLS]}} \in \mathbb{R}^{768}$), đưa qua một lớp Linear ($768 \rightarrow 2$) và hàm Softmax là có thể dự đoán xác suất cảm xúc.

---

### Câu 7: Vì sao nhóm chọn phiên bản `bert-base-uncased` thay vì `cased`?
- **[Trả lời ngắn]:** Vì bài toán phân loại đánh giá khách sạn không phụ thuộc nhiều vào chữ hoa/thường, và bản `uncased` có khả năng chống nhiễu tốt hơn trước lỗi viết hoa tùy tiện của người dùng trên Internet.
- **[Trả lời mở rộng]:** Khách hàng đánh giá khách sạn thường viết hoa tự do (ví dụ: *"GREAT"*, *"Great"*, *"great"*). Phiên bản `uncased` tự động chuyển toàn bộ văn bản về chữ thường, giúp gom chung các biến thể này về cùng một token ID, giảm dung lượng từ điển và tránh phân mảnh biểu diễn. Trừ các bài toán nhận dạng thực thể có tên (NER) thì `cased` mới thực sự cần thiết.

---

### Câu 8: Tốc độ học (Learning Rate) `2e-5` có ý nghĩa gì? Tại sao không dùng `1e-3` như trong code cũ?
- **[Trả lời ngắn]:** `2e-5` là tốc độ học rất nhỏ, giúp giữ lại tri thức ngôn ngữ đã học của BERT và chỉ tinh chỉnh nhẹ các trọng số. Tốc độ `1e-3` quá lớn, sẽ phá hủy hoàn toàn các trọng số tiền huấn luyện (hiện tượng Catastrophic Forgetting).
- **[Trả lời mở rộng]:** Khi mạng nơ-ron đã ở trạng thái tối ưu cục bộ rất tốt từ giai đoạn Pre-training, một bước nhảy gradient lớn ($10^{-3}$) sẽ làm các trọng số bị chệch khỏi vùng hội tụ tốt, khiến mô hình hoạt động bất ổn định và overfit trên tầng phân loại mới. Nghiên cứu thực nghiệm của Devlin et al. khuyến nghị learning rate cho fine-tuning BERT luôn nằm trong khoảng $[2 \times 10^{-5}, 5 \times 10^{-5}]$.

---

### Câu 9: Tại sao BERT chỉ cần huấn luyện trong 2 đến 4 epochs?
- **[Trả lời ngắn]:** Vì BERT đã học sẵn phần lớn tri thức biểu diễn ngôn ngữ trong giai đoạn tiền huấn luyện. Huấn luyện quá 4 epochs trên tập dữ liệu nhỏ sẽ khiến mô hình bị ghi nhớ máy móc (Overfitting).
- **[Trả lời mở rộng]:** Đồ thị huấn luyện thực tế của chúng em cho thấy Validation Loss đạt điểm tối ưu ngay ở epoch 1-2, và Validation Macro F1 đạt đỉnh ở epoch 3 (0.8389). Việc kéo dài lên 100 epochs như notebook cũ không làm tăng thêm thông tin mới mà chỉ khiến mô hình overfit nặng nề (Train Accuracy đạt 97% nhưng Test Accuracy tụt xuống 65.20%).

---

### Câu 10: Tiền xử lý cho BERT khác gì so với tiền xử lý cho mô hình truyền thống (TF-IDF, Naive Bayes)?
- **[Trả lời ngắn]:** Mô hình truyền thống thường xóa stopwords, bỏ dấu câu và lemmatize. Ngược lại, BERT yêu cầu giữ nguyên văn bản tự nhiên, bảo toàn stopwords (nhất là từ phủ định) và cấu trúc câu để hiểu ngữ cảnh trọn vẹn.
- **[Trả lời mở rộng]:** Các từ như *"not"*, *"no"*, *"never"*, *"but"* trong danh sách stopwords của NLTK mang ý nghĩa đảo ngược cảm xúc. Nếu xóa chúng, câu *"The room is not clean"* sẽ biến thành *"room clean"* (từ tiêu cực thành tích cực). BERT dùng WordPiece Tokenization và Positional Encoding, có thể tự xử lý ngữ pháp tự nhiên mà không cần can thiệp thô bạo vào văn bản.

---

### Câu 11: Tại sao cần có Validation Set bên cạnh Train và Test Set?
- **[Trả lời ngắn]:** Train set dùng để cập nhật trọng số, Validation set dùng để theo dõi tiến trình học và chọn checkpoint tốt nhất. Test set chỉ dùng duy nhất một lần ở bước cuối cùng để kiểm tra độc lập nhằm chống rò rỉ dữ liệu.
- **[Trả lời mở rộng]:** Nếu dùng Test set để chọn epoch dừng hoặc chỉnh siêu tham số, thông tin từ Test set sẽ gián tiếp rò rỉ vào mô hình (Data Leakage), dẫn đến kết quả đánh giá bị thổi phồng. Validation set đóng vai trò là tập đệm khách quan để đưa ra quyết định Early Stopping và Model Selection.

---

### Câu 12: F1-Score là gì và tại sao nhóm dùng Validation Macro F1 để chọn Checkpoint tốt nhất?
- **[Trả lời ngắn]:** F1-score là trung bình điều hòa giữa Precision và Recall. Nhóm chọn **Validation Macro F1** (`metric_for_best_model="eval_macro_f1"`) làm tiêu chí chọn checkpoint tốt nhất vì nó đánh giá đồng đều năng lực phân loại trên cả hai lớp Positive và Negative.
- **[Trả lời mở rộng]:** Macro F1 tính F1 riêng biệt cho từng lớp rồi lấy trung bình cộng không trọng số: $\text{Macro F1} = \frac{F_{1,\text{neg}} + F_{1,\text{pos}}}{2}$. Điều này đảm bảo mô hình không bị thiên vị sang một lớp nào. Trong thực nghiệm, tại Epoch 3, Validation Macro F1 đạt đỉnh **0.8389** (ứng với checkpoint tốt nhất `checkpoint-2592`), mang lại hiệu năng tối ưu trên tập kiểm thử (Test Macro F1 đạt 0.8483).

---

### Câu 13: Trong những tình huống nào mô hình BERT có thể cho kết quả kém hơn Logistic Regression?
- **[Trả lời ngắn]:** BERT có thể kém hơn Logistic Regression khi: tập dữ liệu quá nhỏ dẫn đến overfit, dữ liệu chủ yếu là từ khóa ngắn/nhiễu, xảy ra quên thảm khốc (catastrophic forgetting), hoặc do các lỗi triển khai kỹ thuật.
- **[Trả lời mở rộng]:** 
  1. *Kích thước dữ liệu quá nhỏ:* Nếu chỉ có vài trăm mẫu, mô hình 110M tham số rất dễ overfit, trong khi mô hình tuyến tính ít tham số lại khái quát hóa tốt hơn.
  2. *Đặc trưng dạng từ khóa rời rạc:* Nếu văn bản là các chuỗi từ khóa ngắt quãng không có cấu trúc ngữ pháp, ưu thế chú ý ngữ cảnh hai chiều của BERT không phát huy tác dụng bằng tần suất từ khóa trong TF-IDF.
  3. *Lỗi kỹ thuật triển khai:* Như trong `DL_Model.ipynb` của tài liệu môn học, việc dùng learning rate quá lớn ($10^{-3}$), đóng băng encoder, hoặc lệch bảng từ vựng đã khiến BERT chỉ đạt 65.20% (thua xa các mô hình cơ sở).
  4. *Mất cân bằng dữ liệu cực đoan:* Nếu không gán trọng số lớp (class weights), BERT có thể dự đoán thiên lệch về lớp đa số.

---

### Câu 14: Tập dữ liệu `dts_20k_raw.csv` có nguồn gốc từ đâu và có đặc điểm gì cần lưu ý?
- **[Trả lời ngắn]:** Đây là tập dữ liệu đánh giá cảm xúc khách sạn do giảng viên cung cấp (teacher-provided dataset), bắt nguồn từ các đánh giá trên Booking.com, gồm 20,000 mẫu thô.
- **[Trả lời mở rộng]:** Trên Booking.com, biểu mẫu chia thành hai ô riêng: mặt tiêu cực và mặt tích cực. Khi khách hài lòng và không có phàn nàn, hệ thống tự điền `"No Negative"`. Sau quá trình kiểm toán tự động, nhóm loại bỏ 5 mẫu rỗng, 127 mẫu có nhãn mâu thuẫn (conflicting labels), và 123 mẫu trùng lặp hoàn toàn, thu được tập dữ liệu sạch gồm 19,745 mẫu chuẩn mực.

---

### Câu 15: Vì sao ở Epoch 3, Validation Loss tăng nhưng Validation Macro F1 lại đạt giá trị cao nhất? Nhóm xử lý chọn Checkpoint ra sao?
- **[Trả lời ngắn]:** Do hàm mất mát Cross-Entropy phạt nặng mức độ tự tin ở một số ít mẫu khó hoặc có nhãn nhiễu, trong khi phần lớn mẫu còn lại được phân loại chính xác hơn. Nhóm dùng tiêu chí **Validation Macro F1** để chọn checkpoint tốt nhất.
- **[Trả lời mở rộng]:** Trong tiến trình huấn luyện BERT:
  - Epoch 1: Val Loss 0.3541, Val Macro F1 0.8359
  - Epoch 2: Val Loss 0.3702, Val Macro F1 0.8384
  - Epoch 3: Val Loss 0.4503, Val Macro F1 **0.8389** (Đạt đỉnh)
  Cross-Entropy đo lường xác suất ($-\log p$). Khi mô hình học sâu, nó phân loại đúng nhiều mẫu hơn (đẩy F1 tăng), nhưng ở một số mẫu biên mơ hồ hoặc có nhãn bất thường, xác suất bị lệch nhẹ khiến tổng Loss tăng. Vì mục tiêu cuối cùng của bài toán là độ chính xác phân loại cảm xúc, việc lựa chọn checkpoint theo Validation Macro F1 (`checkpoint-2592`) là hoàn toàn chuẩn xác về mặt khoa học.

---

### Câu 16: Nếu một bài đánh giá có độ dài vượt quá `max_length = 128` thì điều gì xảy ra?
- **[Trả lời ngắn]:** Văn bản sẽ bị cắt cụt (Truncation), các token vượt quá 128 sẽ bị loại bỏ và không tham gia tính toán Self-Attention.
- **[Trả lời mở rộng]:** Phân tích phân vị độ dài token trên tập Train+Val (15,796 mẫu) cho thấy phân vị 95% (p95) là 121 tokens và phân vị 90% (p90) là 94 tokens. Ngưỡng `MAX_LENGTH = 128` bảo toàn trọn vẹn 96.07% số văn bản trong tập dữ liệu. Việc chọn 128 thay vì 256 giúp giảm $4\times$ kích thước ma trận Attention ($\mathcal{O}(L^2)$) và tiết kiệm bộ nhớ kích hoạt đáng kể, chỉ chấp nhận cắt cụt 3.93% văn bản dài.

---

### Câu 17: Cơ chế Self-Attention tính toán độ tương đồng giữa các từ như thế nào?
- **[Trả lời ngắn]:** Dựa trên tích vô hướng (Dot-product) giữa vector Query của từ này và vector Key của từ khác, chia cho $\sqrt{d_k}$ và chuẩn hóa qua hàm Softmax.
- **[Trả lời mở rộng]:** Công thức $\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$. Nếu hai từ có liên quan chặt chẽ về mặt ngữ nghĩa hoặc cú pháp, tích vô hướng của chúng sẽ có giá trị dương lớn, dẫn đến trọng số Softmax cao, khiến vector Value của từ đó đóng góp nhiều vào biểu diễn tổng hợp của từ hiện tại.

---

### Câu 18: Tại sao lại cần hệ số co giãn $\frac{1}{\sqrt{d_k}}$ trong công thức Scaled Dot-Product Attention?
- **[Trả lời ngắn]:** Để ngăn tích vô hướng trở nên quá lớn khi số chiều $d_k$ lớn, tránh đẩy hàm Softmax vào vùng bão hòa gradient cực nhỏ (vanishing gradient).
- **[Trả lời mở rộng]:** Khi $d_k$ lớn (ví dụ $d_k = 64$), tích vô hướng của hai vector độc lập có phương sai xấp xỉ $d_k$. Nếu không chia cho $\sqrt{d_k}$, các giá trị đầu vào của Softmax sẽ rất phân cực (một giá trị cực lớn, các giá trị khác rất nhỏ), làm đạo hàm của Softmax triệt tiêu về 0, cản trở việc học của thuật toán lan truyền ngược.

---

### Câu 19: Bộ tối ưu hóa AdamW khác gì so với Adam thông thường?
- **[Trả lời ngắn]:** AdamW tách rời cơ chế suy giảm trọng số (Weight Decay) ra khỏi việc cập nhật gradient tích lũy của các moment, giúp điều quy (regularization) hiệu quả hơn rất nhiều.
- **[Trả lời mở rộng]:** Trong Adam gốc (Loshchilov & Hutter, 2019), L2 regularization được cộng trực tiếp vào hàm mất mát, dẫn đến việc các trọng số có gradient lớn lại bị phạt ít hơn. AdamW áp dụng weight decay trực tiếp lên bước cập nhật trọng số ($\theta_{t+1} = \theta_t - \eta \lambda \theta_t - \dots$), giúp kiểm soát độ lớn tham số chuẩn xác và chống overfitting vượt trội cho Transformer.

---

### Câu 20: Dropout là gì và đóng vai trò gì trong mô hình phân loại chuỗi?
- **[Trả lời ngắn]:** Dropout là kỹ thuật điều quy ngẫu nhiên "tắt" (gán bằng 0) một tỷ lệ nơ-ron trong quá trình huấn luyện nhằm ngăn chặn các nơ-ron đồng thích nghi (co-adaptation).
- **[Trả lời mở rộng]:** Trong kiến trúc `BertForSequenceClassification`, một lớp `Dropout(p=0.1)` được đặt giữa vector `[CLS]` (768 chiều) và lớp phân loại tuyến tính. Điều này buộc mô hình không được phụ thuộc tuyệt đối vào bất kỳ một chiều đặc trưng đơn lẻ nào, tăng khả năng tổng quát hóa trên dữ liệu mới.

---

### Câu 21: Nhóm đã thực hiện phân tích lỗi (Error Analysis) như thế nào và rút ra kết luận gì?
- **[Trả lời ngắn]:** Nhóm khảo sát định tính chi tiết **mẫu 20 ca lỗi có độ tin cậy cao nhất (10 FP, 10 FN)** trên tập Test, phân tích theo các mẫu hình ngôn ngữ cụ thể. Kết quả cho thấy lỗi chủ yếu xuất phát từ tính đa khía cạnh của cảm xúc và dấu hiệu mơ hồ nhãn.
- **[Trả lời mở rộng]:** Trong mẫu 20 ca lỗi cực đoan được khảo sát (`docs/04_error_analysis.md`):
  - 15/20 ca (75%) mang đặc trưng cảm xúc pha trộn (Mixed Sentiment), vừa khen vừa chê.
  - 8/20 ca (40%) cho thấy dấu hiệu possible label ambiguity / label noise (ngữ nghĩa mâu thuẫn với nhãn ground-truth).
  - 0/20 ca bị cắt cụt độ dài (tất cả đều $\le 126$ tokens).
  *Lưu ý:* Phân tích này tập trung vào mẫu 20 ca lỗi cực đoan nhằm phát hiện các trường hợp biên, không suy rộng đại diện cho toàn bộ 599 ca lỗi trên tập kiểm thử.

---

### Câu 22: Ứng dụng Demo Streamlit hoạt động như thế nào?
- **[Trả lời ngắn]:** Demo nạp mô hình Baseline và BERT từ thư mục artifacts, nhận văn bản từ người dùng, chạy qua pipeline suy luận, hiển thị so sánh đối đầu song song xác suất và giải thích bẻ từ WordPiece.
- **[Trả lời mở rộng]:** Ứng dụng cung cấp 4 câu đánh giá mẫu thể hiện các trường hợp phức tạp (như câu phủ định kép, khen chê pha trộn). Giao diện hiển thị trực quan xác suất dự đoán của cả hai mô hình, làm nổi bật sự vượt trội của BERT trong việc xử lý ngữ cảnh đảo nghĩa so với mô hình túi từ TF-IDF.

---

### Câu 23: Làm thế nào để đảm bảo tính tái lập (Reproducibility) của toàn bộ project?
- **[Trả lời ngắn]:** Bằng cách cố định random seed = 42 ở mọi cấp độ (Python, NumPy, PyTorch, Scikit-learn), lưu cấu hình tập trung tại `src/config.py`, và đóng gói môi trường qua `requirements.txt`.
- **[Trả lời mở rộng]:** Dự án được kiểm soát tính tái lập nghiêm ngặt (`controlled for reproducibility with fixed seeds and documented environment`). Tuy nhiên, do các phép toán số học dấu phẩy động trên phần cứng CPU/GPU và các luồng tính toán song song, các chỉ số thực nghiệm có thể có sai lệch rất nhỏ ở chữ số thập phân thứ 4 hoặc thứ 5 giữa các hệ thống khác nhau, điều này là hoàn toàn bình thường trong kỹ thuật học sâu.

---

### Câu 24: Dự án tuân thủ quy trình `AI Project Cycle` của môn học như thế nào?
- **[Trả lời ngắn]:** Đồ án thực hiện đầy đủ 6 bước chuẩn: Scope & Plan $\rightarrow$ Data $\rightarrow$ Models $\rightarrow$ Deployment $\rightarrow$ Maintenance $\rightarrow$ Feedback.
- **[Trả lời mở rộng]:** Nhóm tuân thủ chặt chẽ Slide 9 `AI Project Cycle.pptx`: Bắt đầu từ mô hình đơn giản nhất (TF-IDF + Logistic Regression) để làm mốc so chuẩn trước khi phát triển mô hình phức tạp hơn (BERT). Đồng thời, nhóm thực hiện kiểm toán dữ liệu nghiêm ngặt, loại bỏ mẫu trùng lặp/xung đột, và niêm phong tập kiểm thử độc lập (Zero Leakage).

---

### Câu 25: Điểm khác biệt lớn nhất giữa đồ án của nhóm và các bài tham khảo trước đây là gì?
- **[Trả lời ngắn]:** Triển khai mới hoàn toàn từ đầu (clean-room implementation), kiểm toán và phục hồi tiềm năng của BERT so với code cũ môn học (tăng từ 65.20% lên 84.83%), phân tích định tính ca lỗi học thuật và minh chứng bằng số liệu artifact thực tế.
- **[Trả lời mở rộng]:** Nhóm không sao chép mã nguồn tham khảo mà xây dựng độc lập từng module. Nhóm đã tìm ra 5 sai lầm kỹ thuật trong `DL_Model.ipynb` (lệch tokenizer, freeze encoder, lr quá lớn, overfitting 100 epochs), từ đó xây dựng pipeline chuẩn mực đạt 84.83% Test Accuracy. Mọi số liệu trong báo cáo và slide thuyết trình đều có artifact tương ứng kiểm chứng.
