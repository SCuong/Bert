# 01. Material Audit: Toàn Diện Tài Liệu & Phân Tích Mã Nguồn Cũ

**Người thực hiện:** AI/ML Engineer  
**Môn học:** Trí tuệ Nhân tạo (Artificial Intelligence)  
**Ngày thực hiện:** 20/09/2026  
**Mục tiêu:** Khảo sát, audit toàn bộ tài liệu giảng viên cung cấp, đối chiếu với tiêu chuẩn học thuật và chỉ ra những điểm cần kế thừa cũng như những sai sót kỹ thuật trong code cũ.

---

## 1. Cây tài liệu liên quan trong Workspace

```text
<repository-root>/
├── Bài giảng/
│   ├── AI Project Cycle.pptx              # [CỐT LÕI] Quy trình chuẩn của một dự án AI
│   ├── Bai 1_ Gioithieu.pptx              # Giới thiệu môn học AI
│   ├── Bai 2_3_ Timkiemmu_2022.pptx       # Thuật toán tìm kiếm mù (BFS, DFS, UCS)
│   ├── Bai 4_5_Timkiemcothongtin_2022.pptx# Tìm kiếm có thông tin (A*, Greedy)
│   ├── Bai 6-7_ Timkiemcodoithu_2022.pptx # Tìm kiếm có đối thủ (Minimax, Alpha-Beta)
│   ├── Bai 8-9_ML-Linear Regression.pptx  # Hồi quy tuyến tính
│   ├── Pre_Bai _8_9.pdf                  # Tài liệu bổ trợ Regression
│   ├── Bài 10-11_ - Perceptron_2022.pptx  # Mạng Perceptron một lớp
│   ├── Bai 12-13_ ML- Logistic regression # Hồi quy Logistic cho phân loại
│   ├── Bai 14-15 Neural Network.pptx      # Mạng nơ-ron truyền thẳng (MLP, Backprop)
│   ├── Bai 16_ K means Clustering_.pptx   # Phân cụm K-Means
│   └── AI.Code/
│       ├── NLP_Demo/
│       │   ├── dts_20k_raw.csv            # [DATA GỐC] 20,000 review khách sạn thô
│       │   ├── dts_20k_preprocessed.csv   # Data sau tiền xử lý của sinh viên cũ
│       │   ├── Preprocessing_and_Visualizing.ipynb # Notebook tiền xử lý & EDA cũ
│       │   ├── NaiveBayesClassifier.ipynb # Notebook code Naive Bayes thủ công
│       │   └── DL_Model.ipynb             # [QUAN TRỌNG] Code Deep Learning (NNLM, BiLSTM, BERT)
│       └── [Các script ML/Search khác]    # Peceptron.py, Alpha_beta.py, Kmean...
└── Báo cáo bài tập lớn/
    ├── Baocaogamecaro.pptx                # Báo cáo mẫu nhóm trước (Caro Minimax)
    ├── CaroAI/                            # Source code Java của dự án Caro
    ├── Transformer.pptx                   # [CỐT LÕI] Slide bài giảng Transformer
    └── Transformer.pdf                    # Bản PDF xuất từ Transformer.pptx
```

---

## 2. Mục đích sử dụng của từng tài liệu chính

| Tài liệu | Định dạng | Mục đích chính trong đồ án |
| :--- | :---: | :--- |
| `AI Project Cycle.pptx` | PPTX | **Kim chỉ nam về phương pháp luận**: Định hình 6 giai đoạn (Scope -> Data -> Models -> Deployment -> Maintenance -> Feedback). Quy định nguyên tắc *"Start from simple to more complex models"* (phải có Baseline trước khi dùng mô hình phức tạp). |
| `Transformer.pptx` / `.pdf` | PPTX/PDF | **Cơ sở lý thuyết**: Giải thích cội nguồn Transformer (Vaswani et al., 2017), sự vượt trội so với RNN/LSTM (triệt tiêu Vanishing Gradient, tính toán song song), cơ chế Self-Attention, Multi-head Attention, Positional Encoding, Encoder-Decoder. |
| `dts_20k_raw.csv` | CSV | **Tập dữ liệu chính thức**: 20,000 dòng đánh giá khách sạn bằng tiếng Anh, nhãn 0/1 cân bằng hoàn hảo (10,000/10,000). |
| `Preprocessing_and_Visualizing.ipynb` | IPYNB | **Quy trình tiền xử lý cũ**: Chứa các bước loại bỏ HTML, URL, dấu câu, stopwords NLTK và lemmatization. Cần audit để chỉ ra lỗi phá vỡ ngữ nghĩa. |
| `DL_Model.ipynb` | IPYNB | **Mã nguồn mô hình sâu cũ**: Triển khai NNLM (Google Embedding), BiLSTM và mô hình BERT (dùng TensorFlow Hub). Chứa các lỗi kỹ thuật lớn dẫn đến kết quả BERT thấp. |
| `Baocaogamecaro.pptx` | PPTX | **Tham chiếu kỳ vọng thuyết trình**: Hiểu phong cách chấm điểm, cấu trúc slide, mức độ chi tiết mà giảng viên yêu cầu ở các nhóm sinh viên. |

---

## 3. Workflow giảng viên đang giảng dạy

Theo slide `AI Project Cycle.pptx`, giảng viên định hướng quy trình kỹ thuật gồm 6 bước:
1. **Scope & Plan**: Xác định bài toán (Problem), bên liên quan (Stakeholders), mục tiêu (Goals/Objectives), chỉ số đo lường (Success metrics/KPIs).
2. **Data**:
   - Thu thập & tổ chức dữ liệu.
   - Làm sạch dữ liệu (Cleaning) & tiền xử lý (Preprocessing).
   - Phân tích khám phá (EDA - Exploratory Data Analysis) để tìm insights.
3. **Models**:
   - Khảo sát các giải pháp hiện hành.
   - Bắt đầu từ mô hình đơn giản (Baseline) đến mô hình phức tạp.
   - Đánh giá kết quả trên các metrics chuẩn.
   - Tối ưu và tinh chỉnh mô hình (Fine-tuning).
4. **Deployment & Integration**: Đưa mô hình vào ứng dụng thực tế (Demo UI), kiểm thử hệ thống.
5. **Monitoring & Maintenance**: Giám sát hiệu năng, phát hiện lỗi, cập nhật dữ liệu.
6. **Feedback**: Thu thập phản hồi từ người dùng/stakeholders để lặp lại chu trình cải tiến.

---

## 4. Phân tích chi tiết mã nguồn NLP hiện tại

### 4.1. Tiền xử lý (`Preprocessing_and_Visualizing.ipynb`)
- Đọc `dts_20k_raw.csv`.
- Thống kê độ dài từ: Hàm `wl(text)` đếm số từ thông qua `len(text.split(" "))`.
- Xóa URL: `re.sub(r'http\S+', '', text)`.
- Xóa HTML tags: `re.sub(r'<.*?>', '', text)`.
- Xóa dấu câu: `text.translate(str.maketrans('', '', string.punctuation))`.
- Xóa Stopwords: Sử dụng NLTK `stopwords.words()`.
- Lemmatization: Khởi tạo `WordNetLemmatizer()`, gọi `lemmatizer.lemmatize(text)` trên toàn bộ chuỗi văn bản.
- Lưu kết quả ra `dts_20k_preprocessed.csv`.

### 4.2. Huấn luyện mô hình sâu (`DL_Model.ipynb`)
Notebook triển khai 3 mô hình trên tập `dts_20k_preprocessed.csv`:
1. **Google Embedding (NNLM-en-dim50)**:
   - Sử dụng `hub.KerasLayer('https://tfhub.dev/google/nnlm-en-dim50/2')`.
   - Lớp Dense ẩn: Dense(128, relu) -> Dense(64, relu) -> Dense(32, relu) -> Dense(16, relu) -> Dense(1, sigmoid).
   - Optimizer Adam (lr=0.001), 10 epochs.
2. **Traditional BiLSTM**:
   - Tokenizer Keras với vocab size thực tế, padding post maxlen=250.
   - Embedding(dim=60) -> 2 tầng Bidirectional(LSTM(60)) -> GlobalAveragePooling1D -> Dense(500) -> Dense(200) -> Dense(100) -> Dense(50) -> Dense(1, sigmoid).
   - Optimizer Adam (lr=0.001), 50 epochs.
3. **Mô hình "BERT" cũ**:
   - Preprocessing layer: `hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3')`.
   - Encoder layer: `hub.KerasLayer('https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/2', trainable=False)`.
   - Classifier head: Dense(400) -> Dense(200) -> Dense(100) -> Dense(50) -> Dense(25) -> Dense(1, sigmoid).
   - Optimizer Adam (lr=0.001), 100 epochs.

---

## 5. Các metrics ghi nhận trong notebook cũ (Test Set: 2,000 mẫu)

| Mô hình | Accuracy | Precision (0 / 1) | Recall (0 / 1) | F1-score (0 / 1) | Ghi chú |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **NNLM (Google Embedding)** | **79.0%** | 0.78 / 0.80 | 0.82 / 0.76 | 0.80 / 0.78 | 10 epochs |
| **BiLSTM** | **75.0%** | 0.76 / 0.74 | 0.74 / 0.76 | 0.75 / 0.75 | 50 epochs (1,987 mẫu test) |
| **"BERT" (TF Hub cũ)** | **65.2%** | 0.66 / 0.65 | 0.65 / 0.66 | 0.65 / 0.65 | 100 epochs, train acc=97.1%, test loss=2.61 |

*Nguồn trích xuất trực tiếp: Cell 22, Cell 33, Cell 46 của `DL_Model.ipynb`.*

---

## 6. Điểm tốt trong tài liệu & mã nguồn cũ

1. **Ý thức so sánh nhiều mô hình**: Nhóm sinh viên cũ đã thử nghiệm cả mô hình truyền thống (Naive Bayes), mô hình nhúng từ (NNLM), mô hình tuần tự (BiLSTM) và mô hình Transformer (BERT).
2. **Sử dụng dataset chuẩn**: Dataset 20,000 mẫu cân bằng, độ dài phong phú, rất phù hợp cho bài toán phân loại cảm xúc nhị phân.
3. **Có trực quan hóa**: Trong `DL_Model.ipynb` có vẽ biểu đồ loss và accuracy theo epoch.
4. **Slide bài giảng Transformer**: Slide `Transformer.pptx` rất trực quan, minh họa cơ chế Attention, Multi-head Attention và Positional Encoding tương đối chi tiết.

---

## 7. Các lỗi kỹ thuật & Điểm chưa hợp lý nghiêm trọng

### 7.1. Lỗi phá hủy ngữ nghĩa khi tiền xử lý cho mô hình ngôn ngữ
- **Xóa nhầm từ phủ định**: NLTK stopwords chứa `"not"`, `"no"`, `"never"`, `"without"`. Khi xóa toàn bộ stopwords, câu `"The hotel is not clean"` trở thành `"hotel clean"`, biến cảm xúc từ Tiêu cực (0) thành Tích cực (1).
- **Hỏng nhãn dữ liệu Booking.com**: Trong dataset gốc, khách hàng hài lòng thường điền mục Negative là `"No Negative"`. Khi xóa từ `"No"`, câu bắt đầu bằng từ `"negative"`, khiến review tích cực lại chứa từ "negative"!
- **Lemmatization sai cách**: Lệnh `lemmatizer.lemmatize(text)` trong NLTK nhận đầu vào là một từ đơn (token), không thể nhận cả một câu dài `text`. Lệnh này gần như không có tác dụng hoặc sinh lỗi tiềm ẩn.
- **Làm rỗng câu**: Có 113 review ngắn bị xóa sạch thành chuỗi rỗng `""` trong `dts_20k_preprocessed.csv`.

### 7.2. Các sai lầm chết người trong triển khai mô hình BERT cũ
1. **Mâu thuẫn giữa Cased Preprocessor và Uncased Encoder**:
   - Tiền xử lý dùng `bert_en_cased_preprocess/3` (giữ nguyên hoa/thường).
   - Nhưng mô hình BERT lại dùng `small_bert/bert_en_uncased_L-4_H-512_A-8/2` (toàn bộ viết thường).
   - Sự lệch bảng từ vựng (vocabulary mismatch) khiến các token bị mã hóa sai lệch nghiêm trọng.
2. **BERT bị đóng băng (`trainable=False`)**:
   - Đây KHÔNG PHẢI là fine-tuning! Toàn bộ 11.3 triệu tham số của Small BERT bị khóa cứng.
   - Mô hình chỉ đang dùng Small BERT như một feature extractor cố định, sau đó học một mạng MLP phía trên.
3. **Sử dụng Small BERT thay vì BERT-base**:
   - Mô hình được dùng là `small_bert` với 4 lớp Transformer, ẩn 512, 8 attention heads, năng lực biểu diễn kém hơn nhiều so với `bert-base-uncased` (12 lớp, ẩn 768, 12 heads, 110 triệu tham số).
4. **Tốc độ học quá lớn (`lr = 0.001`)**:
   - Tốc độ học chuẩn khi fine-tuning BERT là từ `2e-5` đến `5e-5`. Tốc độ `1e-3` cao gấp 50 lần, khiến gradient bị dao động dữ dội.
5. **Classifier Head quá sâu không có Regularization**:
   - Xếp chồng 6 tầng Dense liên tiếp (400 -> 200 -> 100 -> 50 -> 25 -> 1).
   - Tất cả các lớp Dropout đều bị comment bỏ (`# net = tf.keras.layers.Dropout(0.1)(net)`).
6. **Overfitting cực nặng sau 100 Epochs**:
   - Huấn luyện tới 100 epochs mà không có Early Stopping.
   - Kết quả: Training accuracy tăng lên **97.12%** (loss 0.076), nhưng Test accuracy tụt thảm hại xuống **65.20%** (test loss tăng vọt lên **2.6135**).
   - Không nạp lại best weights mà đánh giá trực tiếp model ở epoch 100 bị overfit hoàn toàn.

---

## 8. Điều gì có thể tái sử dụng & Điều gì KHÔNG nên sao chép

### Điều có thể tái sử dụng:
- Tệp dữ liệu gốc `dts_20k_raw.csv`.
- Tư tưởng phân chia train/val/test và so sánh với baseline.
- Khung cấu trúc thuyết trình của `AI Project Cycle.pptx` và phong cách minh họa của `Transformer.pptx`.

### Điều TUYỆT ĐỐI KHÔNG sao chép:
- **KHÔNG** dùng `dts_20k_preprocessed.csv` đã bị xóa mất từ phủ định.
- **KHÔNG** xóa stopwords vô tội vạ cho BERT. BERT cần toàn bộ ngữ cảnh tự nhiên của câu.
- **KHÔNG** đóng băng encoder (`trainable=False`) rồi gọi là fine-tuning.
- **KHÔNG** dùng learning rate 0.001 cho BERT.
- **KHÔNG** train 100 epoch với head sâu không dropout.
- **KHÔNG** để tokenizer và encoder lệch chuẩn cased/uncased.
