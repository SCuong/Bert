# Cẩm Nang Học Tập: 25 Khái Niệm Cốt Lõi Về BERT & Xử Lý Ngôn Ngữ Tự Nhiên

**Dành cho sinh viên bảo vệ đồ án Trí tuệ Nhân tạo (AI)**  
**Đề tài:** Ứng dụng BERT trong phân loại cảm xúc đánh giá khách sạn  

---

### 1. Xử lý Ngôn ngữ Tự nhiên (NLP - Natural Language Processing) là gì?
NLP là một nhánh liên ngành của Trí tuệ nhân tạo (AI) và Ngôn ngữ học, tập trung vào việc nghiên cứu và phát triển các thuật toán giúp máy tính có khả năng "đọc", "hiểu", "suy luận" và "sinh ra" ngôn ngữ của con người một cách tự nhiên. Thách thức lớn nhất của NLP là tính đa nghĩa (ambiguity), ngữ cảnh văn hóa, tiếng lóng, ngữ pháp phi cấu trúc và các sắc thái cảm xúc phức tạp (mỉa mai, ẩn dụ).

---

### 2. Transformer giải quyết vấn đề cốt tử nào của RNN và LSTM?
Trước năm 2017, các mô hình tuần tự như Recurrent Neural Networks (RNN) và Long Short-Term Memory (LSTM) là tiêu chuẩn cho NLP. Tuy nhiên, chúng có 2 nhược điểm lớn:
1. **Xử lý tuần tự (Sequential Recurrence Bottleneck):** Để tính toán trạng thái ẩn của từ thứ $t$, mô hình bắt buộc phải đợi trạng thái ẩn của từ thứ $t-1$. Điều này khiến RNN/LSTM không thể song song hóa quá trình tính toán theo chiều dài chuỗi, dẫn đến tốc độ huấn luyện chậm trên các tập dữ liệu lớn.
2. **Suy giảm thông tin ngữ cảnh xa (Vanishing Gradient / Information Bottleneck):** Mặc dù LSTM đã cải tiến với cơ chế cổng (Gates) để lưu trữ thông tin dài hạn, nhưng qua các bước lan truyền tuần tự dài, việc nắm bắt và duy trì sự phụ thuộc giữa các từ cách xa nhau vẫn gặp khó khăn thực tế đáng kể.

**Giải pháp của Transformer (Vaswani et al., 2017):** Loại bỏ hoàn toàn bước đệ quy tuần tự, thay thế bằng cơ chế **Self-Attention**. Nhờ đó, trong một tầng tính toán, mô hình xử lý song song đồng thời mọi token trên toàn bộ chiều dài chuỗi và kết nối trực tiếp bất kỳ cặp từ nào trong câu với độ dài đường dẫn thông tin không đổi $\mathcal{O}(1)$.

---

### 3. Encoder và Decoder trong kiến trúc Transformer gốc khác nhau ra sao?
Kiến trúc Transformer nguyên bản gồm hai khối lớn:
- **Encoder (Bộ mã hóa):** Nhận chuỗi văn bản đầu vào và nén nó thành các vector biểu diễn ngữ cảnh đa chiều (Contextualized Representations). Encoder nhìn được toàn bộ ngữ cảnh hai chiều (cả từ phía trước và phía sau).
- **Decoder (Bộ giải mã):** Nhận biểu diễn từ Encoder và tự hồi quy (Autoregressive) sinh ra từng từ của chuỗi đầu ra. Decoder sử dụng **Masked Self-Attention** để ngăn không cho mô hình nhìn thấy các từ trong tương lai khi đang sinh từ hiện tại.
- **Ứng dụng:** Encoder-Decoder phù hợp cho bài toán dịch máy (Machine Translation) hoặc tóm tắt văn bản (Summarization).

---

### 4. BERT sử dụng thành phần nào của Transformer?
**BERT chỉ sử dụng phần ENCODER** của Transformer (xếp chồng nhiều khối Transformer Encoder lên nhau). 
- Vì bài toán của BERT là hiểu ngôn ngữ (Language Understanding), trích xuất đặc trưng ngữ nghĩa và phân loại, chứ không phải bài toán sinh văn bản tuần tự (như GPT dùng Decoder).
- Nhờ chỉ dùng Encoder, BERT có thể nhìn được ngữ cảnh **hai chiều thực sự (Deeply Bidirectional)** ở mọi tầng.

---

### 5. Tokenization là gì?
Máy tính không thể hiểu trực tiếp các ký tự chữ cái mà chỉ làm việc với các ma trận số. **Tokenization** là quá trình phân tách một văn bản thô (chuỗi ký tự) thành các đơn vị ngữ nghĩa nhỏ hơn gọi là **Tokens** (có thể là từ, từ con hoặc ký tự), sau đó ánh xạ mỗi token thành một số nguyên duy nhất (Token ID) dựa trên bảng từ vựng (Vocabulary).

---

### 6. WordPiece / Subword Tokenization giải quyết vấn đề gì?
- Nếu tách theo **từ nguyên vẹn (Word-level):** Bảng từ vựng sẽ khổng lồ (hàng triệu từ), và gặp vấn đề lớn với các từ chưa từng thấy trong từ điển (**Out-of-Vocabulary - OOV**).
- Nếu tách theo **ký tự (Character-level):** Bảng từ vựng rất nhỏ, không bị OOV, nhưng chuỗi đầu vào bị quá dài và mất đi ngữ nghĩa của cả từ.
- **WordPiece (Subword Tokenization của BERT):** Dung hòa cả hai. Các từ phổ biến được giữ nguyên (ví dụ: `"hotel"` -> `hotel`). Các từ hiếm hoặc từ ghép phức tạp sẽ được bẻ nhỏ thành các từ con với tiền tố `##` biểu thị phần tiếp nối (ví dụ: `"unaffordable"` -> `["un", "##afford", "##able"]`). Bảng từ vựng của BERT chỉ cần ~30,522 tokens nhưng có thể biểu diễn gần như mọi từ trong tiếng Anh mà không bao giờ gặp lỗi OOV.

---

### 7. Token đặc biệt `[CLS]` dùng để làm gì?
- `[CLS]` (viết tắt của *Classification*) là token đặc biệt luôn được chèn vào vị trí đầu tiên ($index = 0$) của mọi chuỗi đầu vào trong BERT.
- Vì cơ chế Self-Attention cho phép `[CLS]` kết nối và tổng hợp thông tin từ tất cả các token khác trong câu, vector đầu ra tại vị trí `[CLS]` sau lớp Transformer cuối cùng được xem là **vector đại diện cô đọng cho toàn bộ ngữ nghĩa của câu**.
- Trong các bài toán phân loại chuỗi (Sequence Classification), ta gắn một lớp phân loại (Linear Classifier) ngay phía trên vector `[CLS]` này.

---

### 8. Token đặc biệt `[SEP]` dùng để làm gì?
- `[SEP]` (viết tắt của *Separator*) là token dùng để phân tách:
  1. Phân tách phần kết thúc của một câu.
  2. Phân tách hai câu độc lập khi đưa vào BERT (ví dụ: Cặp câu hỏi - trả lời trong bài toán QA, hoặc Cặp Tiền đề - Giả thuyết trong bài toán NLI).

---

### 9. Cơ chế Attention (Cơ chế chú ý) là gì?
Attention là cơ chế mô phỏng sự tập trung thị giác của con người: khi nhìn vào một bức tranh hay đọc một đoạn văn, bộ não không xử lý toàn bộ thông tin với trọng số đồng đều, mà tập trung cao độ vào những chi tiết quan trọng nhất. Trong NLP, Attention cho phép mô hình gán một trọng số (Attention Weight từ 0 đến 1) thể hiện mức độ liên quan giữa một từ với tất cả các từ còn lại trong ngữ cảnh.

---

### 10. Self-Attention (Tự chú ý) là gì?
Self-Attention là cơ chế Attention được áp dụng **nội bộ trong chính cùng một chuỗi văn bản**. Nó giúp từng từ trong câu tự liên kết và "hỏi" các từ khác xung quanh để xác định xem từ nào đóng vai trò quan trọng trong việc làm rõ nghĩa của nó.
- *Ví dụ:* Trong câu `"The hotel had a great pool, but it was too cold."`, từ `"it"` liên kết mạnh nhất với từ `"pool"` chứ không phải `"hotel"`. Self-Attention giúp mô hình học được mối liên kết này.

---

### 11. Bộ ba vector Query (Q), Key (K), Value (V) được tính như thế nào?
Với mỗi từ (đã nhúng thành vector $x$), ta nhân $x$ với 3 ma trận trọng số có thể học được $W^Q, W^K, W^V$ để tạo ra 3 vector:
1. **Query ($Q$):** Đóng vai trò là "câu hỏi" hoặc "yêu cầu tìm kiếm" của từ hiện tại.
2. **Key ($K$):** Đóng vai trò là "nhãn" hoặc "từ khóa chỉ mục" của các từ trong câu để khớp với Query.
3. **Value ($V$):** Đóng vai trò là "nội dung ngữ nghĩa thực sự" mà từ đó mang theo.

Công thức tính toán Attention:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$
Trong đó:
- $Q K^T$ là tích vô hướng đo độ tương đồng giữa câu hỏi và từ khóa.
- $\sqrt{d_k}$ là hệ số co giãn (scaling factor) nhằm ngăn tích vô hướng quá lớn làm tràn gradient ở hàm softmax.
- $\text{softmax}(\cdot)$ biến các điểm số thành trọng số phân bố xác suất có tổng bằng 1.
- Nhân với $V$ để lấy tổng có trọng số của các vector nội dung.

---

### 12. Multi-Head Attention (Chú ý đa đầu) mang lại lợi ích gì?
Thay vì chỉ tính một ma trận Attention duy nhất, Multi-Head Attention chia $Q, K, V$ thành $h$ phần độc lập (trong BERT-base là $h = 12$ heads) và tính Attention song song trên từng head.
- **Lợi ích:** Mỗi head có thể chuyên môn hóa để chú ý vào một khía cạnh ngôn ngữ khác nhau:
  - Head 1 chú ý vào mối quan hệ cú pháp (Chủ ngữ - Vị ngữ).
  - Head 2 chú ý vào đại từ thay thế (pronoun coreference).
  - Head 3 chú ý vào cụm từ phủ định ("not", "never").
  Sau đó, kết quả từ 12 heads được ghép (concatenate) lại và chiếu qua ma trận tuyến tính $W^O$.

---

### 13. Positional Information (Thông tin vị trí) và Positional Embeddings
Vì Self-Attention xử lý tất cả các token trong một tầng đồng thời mà không dùng bước tuần tự, bản thân phép tính tích vô hướng là bất biến với hoán vị (Permutation Invariant). Nghĩa là câu `"Hotel is good, not bad"` và câu `"Hotel is bad, not good"` sẽ có tập vector đầu vào giống hệt nhau nếu không có thông tin vị trí.
- **Giải pháp:** BERT cộng thêm một vector **Positional Embedding** vào mỗi vector từ đầu vào. Nhờ đó, mô hình biết chính xác từ nào đứng ở vị trí số 0, số 1, số 2... và hiểu được trật tự cú pháp của câu.

---

### 14. Ngữ cảnh hai chiều (Bidirectional Context) thực sự của BERT là gì?
- Các mô hình ngôn ngữ cổ điển như N-gram hoặc LSTM một chiều chỉ nhìn được từ trái qua phải (Left-to-Right).
- BiLSTM tuy có 2 chiều nhưng thực chất là ghép nối độc lập (concatenate) một mạng chạy từ trái sang và một mạng chạy từ phải sang, không có sự tương tác qua lại ở các tầng sâu.
- **BERT là Deeply Bidirectional:** Ở mọi tầng Transformer, cơ chế Self-Attention cho phép mỗi từ nhìn thấy đồng thời cả các từ bên trái và bên phải trong cùng một không gian biểu diễn chung.

---

### 15. Giai đoạn Tiền huấn luyện (Pre-training) của BERT diễn ra như thế nào?
BERT được các kỹ sư Google huấn luyện trên một kho dữ liệu khổng lồ (Toronto BookCorpus 800 triệu từ + Wikipedia tiếng Anh 2,500 triệu từ) theo phương pháp **Tự giám sát (Self-Supervised Learning)** mà không cần con người gán nhãn thủ công. Mô hình học cấu trúc ngữ pháp và tri thức thông qua 2 nhiệm vụ: MLM và NSP.

---

### 16. Nhiệm vụ Masked Language Modeling (MLM) là gì?
- Trong câu đầu vào, 15% số token được chọn ngẫu nhiên.
  - 80% trong số đó được thay bằng token đặc biệt `[MASK]`.
  - 10% được thay bằng một từ ngẫu nhiên khác.
  - 10% được giữ nguyên.
- **Mục tiêu:** BERT phải nhìn vào các từ ngữ cảnh xung quanh để đoán đúng từ bị ẩn sau `[MASK]`. Đây chính là bài toán điền từ vào chỗ trống, buộc mô hình phải hiểu sâu sắc ngữ cảnh hai chiều.

---

### 17. Nhiệm vụ Next Sentence Prediction (NSP) trong BERT gốc là gì?
- BERT nhận vào 2 câu A và B.
  - Trong 50% trường hợp, B là câu tiếp theo thực sự của A trong văn bản (nhãn `IsNext`).
  - Trong 50% trường hợp còn lại, B là một câu ngẫu nhiên được bốc từ tài liệu khác (nhãn `NotNext`).
- **Mục tiêu:** Dự đoán xem câu B có phải là câu tiếp theo của câu A hay không. Nhiệm vụ này giúp BERT hiểu được mối quan hệ logic giữa các câu (hữu ích cho QA và suy luận logic).

---

### 18. Fine-tuning là gì và cơ chế cập nhật trọng số ra sao?
**Fine-tuning** là kỹ thuật Học chuyển giao (Transfer Learning): Ta lấy mô hình BERT đã được tiền huấn luyện (đã nắm vững ngữ pháp và ngữ nghĩa tiếng Anh), gắn thêm một tầng phân loại đơn giản (Linear Layer) lên trên token `[CLS]`, sau đó huấn luyện mô hình trên tập dữ liệu đánh giá khách sạn cụ thể.
- **Cơ chế:** Toàn bộ các trọng số của BERT và tầng phân loại mới đều được cập nhật thông qua thuật toán Backpropagation với tốc độ học nhỏ (ví dụ $2 \times 10^{-5}$).

---

### 19. Vì sao không huấn luyện BERT từ đầu (Train from Scratch) trong đồ án này?
1. **Chi phí tính toán khổng lồ:** Huấn luyện BERT-base từ đầu cần 64 chip TPU chạy liên tục trong 4 ngày, tiêu tốn hàng chục ngàn USD.
2. **Kích thước dữ liệu:** Dataset đồ án chỉ có 20,000 mẫu, hoàn toàn không đủ để học từ đầu 110 triệu tham số (sẽ bị overfitting ngay lập tức).
3. **Hiệu quả thực tế:** Nhờ Pre-training, mô hình đã hiểu sẵn tiếng Anh. Fine-tuning chỉ cần 2-3 epochs (~4.34 giờ trên CPU đa lõi trong thực nghiệm chính thức của nhóm; hoặc thực thi trên môi trường Google Colab với notebook đi kèm) là đạt độ chính xác cao.

---

### 20. Kiến trúc phân loại chuỗi (Sequence Classification Head) hoạt động ra sao?
- Đầu vào: Chuỗi văn bản qua BERT cho ra ma trận ẩn cuối cùng $H \in \mathbb{R}^{T \times 768}$.
- Vector tại vị trí `[CLS]` là $h_{\text{[CLS]}} \in \mathbb{R}^{768}$.
- Áp dụng một lớp Dropout ($p = 0.1$) để chống overfitting:
  $$\tilde{h} = \text{Dropout}(h_{\text{[CLS]}})$$
- Đưa qua lớp Linear chuyển từ 768 chiều về 2 chiều (tương ứng với 2 nhãn 0 và 1):
  $$z = W \tilde{h} + b \quad (W \in \mathbb{R}^{2 \times 768}, b \in \mathbb{R}^2)$$
- Dùng hàm Softmax để tính xác suất cho từng lớp:
  $$P(\text{Class} = k) = \frac{e^{z_k}}{\sum_{j=0}^1 e^{z_j}}$$

---

### 21. Hiện tượng Overfitting là gì và cách nhận biết / khắc phục trong BERT?
- **Hiện tượng:** Mô hình "học vẹt" và ghi nhớ máy móc các đặc trưng riêng của tập Train thay vì học quy luật tổng quát. Khi đó, loss trên tập Train liên tục giảm, accuracy trên Train đạt gần 100%, nhưng loss trên tập Validation bắt đầu tăng ngược trở lại và accuracy trên Test giảm mạnh (như trường hợp notebook cũ: train acc 97% nhưng test acc 65.20%).
- **Cách khắc phục:**
  1. Chỉ train 2-3 epochs với kiểm soát checkpoint.
  2. Dùng Weight Decay (AdamW) và Dropout.
  3. Dùng Learning Rate nhỏ ($2 \times 10^{-5}$) kết hợp Warmup Scheduler.
  4. Lưu lại checkpoint có Validation Macro F1 tốt nhất để đánh giá trên Test set.

---

### 22. Vai trò của phân chia Train, Validation và Test set
- **Train Set (70%):** Dữ liệu để mô hình tính gradient và cập nhật trọng số.
- **Validation Set (10%):** Dữ liệu độc lập dùng để theo dõi quá trình huấn luyện, tinh chỉnh siêu tham số và chọn thời điểm dừng mô hình (chọn best checkpoint).
- **Test Set (20%):** "Đề thi cuối kỳ" hoàn toàn cô lập. Chỉ được đưa ra đánh giá duy nhất một lần khi mô hình đã hoàn tất huấn luyện để đo lường năng lực thực tế trong môi trường sản phẩm. Không bao giờ được dùng Test set để chỉnh siêu tham số (chống Data Leakage).

---

### 23. Accuracy, Precision, Recall và các biến thể F1-Score khác nhau thế nào?
- **Accuracy:** Tỷ lệ số mẫu dự đoán đúng trên tổng số mẫu: $\frac{TP + TN}{TP + TN + FP + FN}$. Dễ gây đánh lừa nếu dữ liệu mất cân bằng.
- **Precision (Độ chuẩn xác):** Trong số những mẫu mô hình đoán là Tích cực, có bao nhiêu mẫu thực sự Tích cực: $\frac{TP}{TP + FP}$.
- **Recall (Độ bao phủ / Nhạy):** Trong số tất cả những mẫu thực sự Tích cực, mô hình tìm ra được bao nhiêu mẫu: $\frac{TP}{TP + FN}$.
- **F1-Score:** Trung bình điều hòa giữa Precision và Recall: $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$.
- **Các biến thể F1-Score:**
  - **Macro F1:** Tính F1 riêng cho từng lớp rồi lấy trung bình cộng không trọng số: $\frac{F_{1,\text{class 0}} + F_{1,\text{class 1}}}{2}$. Đánh giá công bằng cho mọi lớp bất kể số lượng mẫu.
  - **Weighted F1:** Tính F1 riêng cho từng lớp rồi nhân với tỷ lệ số mẫu thực tế của từng lớp.
  - **Binary F1:** Chỉ tính F1 cho lớp tích cực (Class 1).

---

### 24. Vì sao BERT vượt trội hơn TF-IDF + Logistic Regression?
- **TF-IDF + Logistic Regression:** Dựa trên giả định "Túi từ" (Bag-of-Words). Nó đếm tần suất xuất hiện của từ mà hoàn toàn không biết từ đó đứng ở đâu, bổ nghĩa cho ai, và không hiểu được các cấu trúc phủ định phức tạp. Ví dụ: câu *"Not a single complaint"* có từ *"complaint"* mang trọng số âm, TF-IDF có thể phân loại nhầm thành Tiêu cực.
- **BERT:** Hiểu được ngữ cảnh hai chiều, nhận biết được cụm *"Not a single"* bổ nghĩa và đảo ngược nghĩa của *"complaint"*, từ đó phân loại chính xác là Tích cực.

---

### 25. Những trường hợp nào mô hình BERT vẫn có thể dự đoán sai?
1. **Câu vừa khen vừa chê (Mixed Sentiment):** Khách khen phòng ốc đẹp nhưng chê đồ ăn dở và nhân viên thô lỗ. Nhãn chung phụ thuộc vào việc người đánh giá cảm thấy yếu tố nào quan trọng hơn.
2. **Châm biếm / Mỉa mai (Sarcasm):** Ví dụ *"Thank you for giving us a free indoor swimming pool in our leaking bathroom!"*.
3. **Văn bản quá dài bị cắt cụt (Truncation):** Mặc dù trong mẫu 20 ca lỗi cực đoan được khảo sát, 0/20 ca bị cắt cụt (đều $\le 126$ tokens), trên toàn bộ tập dữ liệu (với phân vị p99 là 168 tokens), việc cắt cụt tại `max_length = 128` vẫn có thể làm mất thông tin kết luận ở cuối các bài đánh giá rất dài.
4. **Nhiễu nhãn (Label Noise):** Một số người dùng chấm điểm 1 sao nhưng ghi nhận xét tích cực, hoặc ngược lại (lỗi người nhập liệu hoặc lỗi ghép trường biểu mẫu).
