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
- **[Trả lời mở rộng]:** Trong notebook cũ của môn học (`DL_Model.ipynb`), tác giả đặt `trainable=False`, đó chỉ là Feature Extraction. Trong đồ án này, chúng em thực hiện Fine-tuning thực sự: các ma trận Query, Key, Value và Feed-Forward của tất cả 12 tầng Transformer đều được lan truyền ngược và tinh chỉnh nhẹ để thích ứng tối đa với văn phong đánh giá khách sạn.

---

### Câu 5: Tại sao nhóm không huấn luyện mô hình BERT từ đầu (Train from Scratch)?
- **[Trả lời ngắn]:** Vì huấn luyện từ đầu đòi hỏi hàng tỷ từ ngữ, cụm siêu máy tính hàng chục ngàn USD, và tập dữ liệu 20,000 mẫu của đồ án quá nhỏ sẽ dẫn đến overfitting ngay lập tức.
- **[Trả lời mở rộng]:** BERT-base có 110 triệu tham số. Để các tham số này hội tụ mà không overfit, Google đã phải tiền huấn luyện trên 3.3 tỷ từ từ Wikipedia và BookCorpus trong nhiều ngày trên 64 chip TPU. Fine-tuning cho phép chúng em kế thừa toàn bộ tri thức ngôn ngữ đồ sộ đó và chỉ cần tinh chỉnh trên tập 20,000 mẫu trong vài phút trên GPU cá nhân.

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
- **[Trả lời mở rộng]:** Đồ thị huấn luyện thực tế của chúng em cho thấy Validation Loss đạt điểm tối ưu ngay ở epoch 2 hoặc 3. Việc kéo dài lên 100 epochs như notebook cũ không làm tăng thêm thông tin mới mà chỉ khiến mô hình overfit nặng nề (Train Accuracy đạt 97% nhưng Test Accuracy tụt xuống 65%).

---

### Câu 10: Tiền xử lý cho BERT khác gì so với tiền xử lý cho mô hình truyền thống (TF-IDF, Naive Bayes)?
- **[Trả lời ngắn]:** Mô hình truyền thống thường xóa stopwords, bỏ dấu câu và lemmatize. Ngược lại, BERT yêu cầu giữ nguyên văn bản tự nhiên, bảo toàn stopwords (nhất là từ phủ định) và cấu trúc câu để hiểu ngữ cảnh trọn vẹn.
- **[Trả lời mở rộng]:** Các từ như *"not"*, *"no"*, *"never"*, *"but"* trong danh sách stopwords của NLTK mang ý nghĩa đảo ngược cảm xúc. Nếu xóa chúng, câu *"The room is not clean"* sẽ biến thành *"room clean"* (từ tiêu cực thành tích cực). BERT dùng WordPiece Tokenization và Positional Encoding, có thể tự xử lý ngữ pháp tự nhiên mà không cần can thiệp thô bạo vào văn bản.

---

### Câu 11: Tại sao cần có Validation Set bên cạnh Train và Test Set?
- **[Trả lời ngắn]:** Train set dùng để cập nhật trọng số, Validation set dùng để theo dõi tiến trình học và chọn checkpoint tốt nhất. Test set chỉ dùng duy nhất một lần ở bước cuối cùng để kiểm tra độc lập nhằm chống rò rỉ dữ liệu.
- **[Trả lời mở rộng]:** Nếu dùng Test set để chọn epoch dừng hoặc chỉnh siêu tham số, thông tin từ Test set sẽ gián tiếp rò rỉ vào mô hình (Data Leakage), dẫn đến kết quả đánh giá bị thổi phồng. Validation set đóng vai trò là tập đệm khách quan để đưa ra quyết định Early Stopping và Model Selection.

---

### Câu 12: F1-Score là gì và tại sao trong bài toán này F1 lại quan trọng hơn hoặc tương đương Accuracy?
- **[Trả lời ngắn]:** F1-score là trung bình điều hòa giữa Precision và Recall. Nó phản ánh độ tin cậy thực sự của mô hình mà không bị đánh lừa bởi sự phân bố nhãn lệch.
- **[Trả lời mở rộng]:** Công thức $F_1 = 2 \cdot \frac{P \cdot R}{P + R}$. Mặc dù tập dữ liệu của chúng em cân bằng 50/50, việc báo cáo cả Macro F1 và Per-class F1 đảm bảo rằng mô hình không chỉ đoán thiên vị về một lớp mà đạt được độ chuẩn xác và độ bao phủ cao trên cả hai nhóm khách hàng hài lòng và không hài lòng.

---

### Câu 13: Nếu mô hình BERT cho kết quả thấp hơn Logistic Regression thì nguyên nhân do đâu?
- **[Trả lời ngắn]:** Đó chắc chắn là do lỗi triển khai kỹ thuật (như mâu thuẫn tokenizer, đóng băng trọng số, learning rate quá lớn hoặc overfit) chứ không phải do năng lực mô hình.
- **[Trả lời mở rộng]:** Đây chính là trường hợp đã xảy ra trong notebook cũ của môn học (`DL_Model.ipynb`), khi BERT chỉ đạt 65.2% trong khi BiLSTM đạt 75% và NNLM đạt 79%. Nguyên nhân là do tokenizer cased bị ghép nhầm với model uncased, encoder bị freeze, lr quá lớn ($0.001$) và train 100 epoch. Khi được sửa đúng chuẩn, BERT đạt hiệu năng vượt trội hơn mọi mô hình cơ sở.

---

### Câu 14: Tập dữ liệu `dts_20k_raw.csv` có đặc điểm và vấn đề tiềm ẩn nào?
- **[Trả lời ngắn]:** Dữ liệu bắt nguồn từ Booking.com, chứa cụm từ mặc định `"No Negative"` ở nhiều review tích cực, và có 5 mẫu văn bản rỗng trong file thô.
- **[Trả lời mở rộng]:** Trên Booking.com, người dùng phải điền hai ô riêng biệt là Tiêu cực và Tích cực. Khi không có gì phàn nàn, hệ thống điền chuỗi `"No Negative"`. Nếu áp dụng tiền xử lý cũ xóa từ `"No"`, câu tích cực lại bắt đầu bằng từ `"negative"`. Nhóm em đã phát hiện và xử lý vấn đề này bằng cách giữ nguyên từ ngữ tự nhiên cho BERT.

---

### Câu 15: Làm thế nào nhận biết mô hình đang bị Overfitting và nhóm đã xử lý ra sao?
- **[Trả lời ngắn]:** Nhận biết khi Train Loss giảm liên tục nhưng Validation Loss bắt đầu tăng ngược lại. Nhóm xử lý bằng cách: dùng Dropout (0.1), Weight Decay trong AdamW (0.01), giới hạn 2-3 epochs và lưu checkpoint có Validation Loss thấp nhất.
- **[Trả lời mở rộng]:** Trong `train_bert.py`, chúng em theo dõi cả Train Loss và Validation Loss sau mỗi epoch. Nhờ cơ chế `load_best_model_at_end=True`, mô hình cuối cùng được chọn là mô hình tại thời điểm tổng quát hóa tốt nhất, tránh hoàn toàn sai lầm của notebook cũ khi đánh giá mô hình ở epoch 100 bị overfit.

---

### Câu 16: Nếu một bài đánh giá có độ dài vượt quá `max_length = 128` (hoặc 256) thì điều gì xảy ra?
- **[Trả lời ngắn]:** Văn bản sẽ bị cắt cụt (Truncation), các token vượt quá giới hạn sẽ bị bỏ qua và không tham gia vào quá trình tính toán Attention.
- **[Trả lời mở rộng]:** Phân tích thống kê EDA của nhóm cho thấy hơn 90% số bài review khách sạn có độ dài dưới 128 từ và hơn 97% dưới 256 từ. Việc chọn `max_length` hợp lý giúp tiết kiệm bộ nhớ GPU bậc hai ($O(N^2)$ của ma trận Attention) mà vẫn giữ được thông tin trọng tâm của phần lớn nhận xét.

---

### Câu 17: Cơ chế Self-Attention tính toán độ tương đồng giữa các từ như thế nào?
- **[Trả lời ngắn]:** Dựa trên tích vô hướng (Dot-product) giữa vector Query của từ này và vector Key của từ khác, chia cho $\sqrt{d_k}$ và chuẩn hóa qua hàm Softmax.
- **[Trả lời mở rộng]:** Công thức $\text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right)$. Nếu hai từ có liên quan chặt chẽ về mặt ngữ nghĩa hoặc cú pháp, tích vô hướng của chúng sẽ có giá trị dương lớn, dẫn đến trọng số Softmax cao, khiến vector Value của từ đó đóng góp nhiều vào biểu diễn tổng hợp của từ hiện tại.

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

### Câu 21: Nhóm đã thực hiện phân tích lỗi (Error Analysis) như thế nào?
- **[Trả lời ngắn]:** Nhóm trích xuất các ca dự đoán sai trên Test set, phân loại chúng theo các nhóm nguyên nhân ngôn ngữ cụ thể như: câu vừa khen vừa chê, câu phủ định tinh vi, câu mỉa mai và nhãn bị nhiễu.
- **[Trả lời mở rộng]:** Trong tài liệu `04_error_analysis.md`, chúng em khảo sát chi tiết 20 ca lỗi tiêu biểu. Kết quả cho thấy nguyên nhân phổ biến nhất chiếm hơn 45% ca lỗi là dạng câu "Mixed Sentiment" (khách khen vị trí nhưng chê vệ sinh), nơi mà nhãn gán tổng thể phụ thuộc vào cảm tính chủ quan của người đánh giá.

---

### Câu 22: Ứng dụng Demo Streamlit hoạt động như thế nào?
- **[Trả lời ngắn]:** Demo nạp mô hình BERT đã fine-tune từ thư mục artifacts, nhận văn bản từ người dùng, chạy qua pipeline tokenization, tính toán xác suất và hiển thị trực quan kết quả kèm mức độ tin cậy.
- **[Trả lời mở rộng]:** Ứng dụng cung cấp các câu test mẫu thể hiện các trường hợp phức tạp (như đảo ngữ, phủ định kép). Ngoài nhãn Positive/Negative, giao diện còn hiển thị bảng bẻ từ WordPiece để người xem thấy rõ cách BERT phân tích các token và các subword `##`.

---

### Câu 23: Làm thế nào để đảm bảo tính tái lập (Reproducibility) của toàn bộ project?
- **[Trả lời ngắn]:** Bằng cách cố định random seed = 42 ở mọi cấp độ (Python random, NumPy, PyTorch, Scikit-learn) và ghi lại toàn bộ siêu tham số vào file JSON.
- **[Trả lời mở rộng]:** Chúng em thiết lập `torch.manual_seed(42)`, `np.random.seed(42)`, cố định seed trong `StratifiedShuffleSplit` và lưu toàn bộ thông số phiên bản thư viện vào `requirements.txt`. Bất kỳ ai clone project và chạy lại lệnh đều sẽ thu được đúng các con số thực nghiệm như trong báo cáo.

---

### Câu 24: Dự án tuân thủ quy trình `AI Project Cycle` của môn học như thế nào?
- **[Trả lời ngắn]:** Đồ án thực hiện đầy đủ 6 bước chuẩn: Xác định bài toán (Scope) $\rightarrow$ Xử lý dữ liệu (Data & EDA) $\rightarrow$ Xây dựng Baseline & BERT (Models) $\rightarrow$ Đóng gói Demo (Deployment) $\rightarrow$ Đánh giá & Giám sát (Monitoring) $\rightarrow$ Phân tích lỗi & Đề xuất (Feedback).
- **[Trả lời mở rộng]:** Chúng em bám sát nguyên tắc *"Start from simple to more complex"* của Slide 9: Bắt đầu từ TF-IDF + Logistic Regression trước khi chuyển sang BERT; đồng thời tuân thủ Slide 5 và 7 về kiểm tra dữ liệu, làm sạch đúng cách và không để rò rỉ dữ liệu.

---

### Câu 25: Điểm khác biệt lớn nhất giữa đồ án của nhóm và các bài demo sao chép trên mạng là gì?
- **[Trả lời ngắn]:** Tính trung thực học thuật, việc audit và chỉ ra nguyên nhân thất bại của code cũ trong tài liệu môn học, phân tích lỗi định tính chuyên sâu và quy trình kiểm chứng thực nghiệm độc lập 100%.
- **[Trả lời mở rộng]:** Nhóm không chỉ chạy theo một tutorial có sẵn mà đã nghiên cứu kỹ tài liệu bài giảng, phát hiện ra lỗi mâu thuẫn bảng từ vựng và freeze model trong `DL_Model.ipynb`. Mọi con số trong bài thuyết trình đều được xuất tự động từ quá trình chạy mã nguồn thực tế và được lưu vết trong thư mục artifacts.
