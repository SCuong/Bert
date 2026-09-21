# 03. Phân Tích Kỹ Thuật Mô Hình BERT Cũ Trong Tài Liệu Tham Khảo

**Tài liệu phân tích:** Notebook `Bài giảng/AI.Code/NLP_Demo/DL_Model.ipynb`  
**Đối tượng khảo sát:** Phần *"Training with BERT"* (Cell 39 đến Cell 48)  
**Mục tiêu:** Phân tích kỹ thuật khách quan, chỉ ra nguyên nhân gốc rễ (root causes) khiến mô hình BERT cũ đạt hiệu năng thấp (65.20% Test Accuracy) và đề xuất các giải pháp kỹ thuật chuẩn mực để khắc phục.

---

## 1. Trích Xuất Kiến Trúc Mô Hình BERT Cũ

Trong Cell 42 của `DL_Model.ipynb`, mô hình được định nghĩa bằng TensorFlow / Keras và TensorFlow Hub như sau:

```python
def build_classifier_model():
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
    preprocessing_layer = hub.KerasLayer(
        'https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3', 
        name='preprocessing'
    )
    encoder_inputs = preprocessing_layer(text_input)
    encoder = hub.KerasLayer(
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/2', 
        trainable=False, 
        name='BERT_encoder'
    )
    outputs = encoder(encoder_inputs)
    net = outputs['pooled_output']
    net = tf.keras.layers.Dense(400, activation='relu')(net)
    net = tf.keras.layers.Dense(200, activation='relu')(net)
    net = tf.keras.layers.Dense(100, activation='relu')(net)
    net = tf.keras.layers.Dense(50, activation='relu')(net)
    net = tf.keras.layers.Dense(25, activation='relu')(net)
    net = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(net)
    return tf.keras.Model(inputs=text_input, outputs=net)

classifier_model = build_classifier_model()
adam = Adam(learning_rate=0.001)
classifier_model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['binary_accuracy'])
history = classifier_model.fit(
    x=input_data_train, y=label_data_train, 
    epochs=100, 
    validation_data=(input_data_val, label_data_val), 
    callbacks=[callback_model]
)
```

Kết quả lưu lại tại Cell 46:
- **Test Loss:** `2.6135`
- **Test Binary Accuracy:** `0.6520` (65.20%)
- **Test F1-Score:** `0.65`

Trong khi đó, ở các cell trước trong cùng notebook:
- **NNLM (Google Embedding):** Test Accuracy = **79.0%**, F1 = 0.79.
- **BiLSTM:** Test Accuracy = **75.0%**, F1 = 0.75.

Điều này tạo ra một nghịch lý bề ngoài: *"Mô hình Transformer/BERT hiện đại lại thua kém cả BiLSTM và NNLM đơn giản"*. Tuy nhiên, phân tích kỹ thuật dưới đây chứng minh rằng nghịch lý này hoàn toàn do lỗi triển khai.

---

## 2. Các Lỗi Kỹ Thuật Nghiêm Trọng

### 2.1. Đóng băng trọng số Encoder (`trainable=False`) — Đây KHÔNG PHẢI là Fine-tuning
- Trong hàm khởi tạo, tham số `trainable=False` đã khóa cứng toàn bộ các trọng số của lớp `BERT_encoder`.
- **Hệ quả lý thuyết:** Mô hình không hề thực hiện "Fine-tuning". Nó chỉ đang thực hiện phương pháp "Feature Extraction" (trích xuất đặc trưng tĩnh). Các tầng Attention và biểu diễn ngữ cảnh của BERT hoàn toàn không thích nghi với từ vựng hay ngữ cảnh đặc thù của bài toán đánh giá khách sạn.

### 2.2. Xung đột bảng từ vựng (Cased Preprocessor ghép với Uncased Encoder)
- Tầng tiền xử lý sử dụng: `bert_en_cased_preprocess/3` (giữ nguyên chữ hoa, chữ thường, sử dụng bảng từ vựng cased gồm 28,996 token).
- Tầng encoder sử dụng: `small_bert/bert_en_uncased_L-4_H-512_A-8/2` (mô hình uncased, sử dụng bảng từ vựng uncased gồm 30,522 token).
- **Hệ quả nghiêm trọng:** ID của các token trong bảng cased không hề trùng khớp với ID trong bảng uncased! Ví dụ, token `"The"` và `"the"` có ID khác nhau hoàn toàn trong hai từ điển. Khi đưa token ID từ bộ cased vào một mô hình uncased, mô hình sẽ đọc nhầm sang các từ hoàn toàn khác hoặc gặp token `[UNK]`. Đây là một lỗi chí tử khiến thông tin ngữ nghĩa bị xáo trộn ngay từ đầu vào.

### 2.3. Sử dụng mô hình Small BERT thay vì BERT-base
- Mô hình được chọn là `small_bert/bert_en_uncased_L-4_H-512_A-8` (4 tầng Transformer, chiều ẩn $H=512$, 8 attention heads, ~11.3 triệu tham số).
- Chuẩn mực công bố trong bài báo gốc của Devlin et al. (2018) là `bert-base-uncased` (12 tầng Transformer, chiều ẩn $H=768$, 12 attention heads, 110 triệu tham số). Năng lực mô hình hóa của Small BERT thấp hơn rất nhiều so với BERT-base.

### 2.4. Tốc độ học (Learning Rate) quá lớn (`0.001`)
- Tốc độ học được cấu hình là `lr = 0.001` (1e-3).
- Trong các nghiên cứu chuẩn về BERT (Devlin et al., 2018; Mosbach et al., 2021), tốc độ học khuyến nghị cho fine-tuning nằm trong khoảng `2e-5` đến `5e-5`. Tốc độ học `1e-3` cao gấp **50 lần** mức khuyến nghị, khiến việc hội tụ của các trọng số bị chệch hướng nghiêm trọng.

### 2.5. Classifier Head quá sâu và thiếu Regularization
- Sau đầu ra `pooled_output` (512 chiều), tác giả xếp chồng liên tiếp 5 lớp Dense: `400 -> 200 -> 100 -> 50 -> 25 -> 1`.
- Các dòng mã Dropout đều bị chú thích bỏ (`# net = tf.keras.layers.Dropout(0.1)(net)`).
- Việc xếp chồng nhiều lớp Dense phi tuyến tính mà không có bất kỳ cơ chế điều quy nào (Dropout, Weight Decay) trên một biểu diễn cố định dẫn đến việc mạng nơ-ron ghi nhớ máy móc tập huấn luyện.

### 2.6. Huấn luyện 100 Epochs dẫn đến Overfitting trầm trọng
- Mô hình được cho chạy liên tục 100 epochs.
- Đến epoch 100:
  - Training Binary Accuracy đạt **97.12%** (loss giảm xuống **0.0764**).
  - Nhưng trên tập kiểm thử (Cell 46), Test Loss tăng vọt lên **2.6135** và Test Accuracy chỉ còn **65.20%**.
- Độ chênh lệch giữa Train Accuracy (97%) và Test Accuracy (65%) là minh chứng kinh điển cho hiện tượng **Overfitting cực độ**.
- Hơn nữa, mặc dù có khởi tạo `callback_model = ModelCheckpoint(...)`, ở Cell 46 dòng lệnh nạp lại trọng số tốt nhất đã bị comment bỏ (`# classifier_model.load_weights(...)`), khiến mô hình được đánh giá chính là trạng thái tệ nhất ở epoch 100.

---

## 3. Bảng Đối Chiếu Kỹ Thuật: Mã Cũ vs. Giải Pháp Chuẩn Mới

| Tiêu chí | Mã cũ (`DL_Model.ipynb`) | Giải pháp mới của nhóm (Fine-Tuned BERT) | Cơ sở học thuật |
| :--- | :--- | :--- | :--- |
| **Mô hình nền tảng** | Small BERT (L=4, H=512, A=8) | `google-bert/bert-base-uncased` (L=12, H=768, A=12) | Chuẩn mực Devlin et al. (2018) |
| **Tính tương thích Tokenizer** | Cased Preprocess + Uncased Model (Lệch vocab) | Đồng bộ tuyệt đối: `AutoTokenizer` đi cùng `AutoModel` | Đảm bảo đúng Token ID và đúng bảng mã |
| **Cơ chế huấn luyện** | Feature Extraction (`trainable=False`) | True Fine-tuning (Cập nhật toàn bộ các tầng Encoder) | Cho phép các tầng Attention thích ứng với dữ liệu khách sạn |
| **Tốc độ học (Learning Rate)** | `1e-3` (quá lớn) | `2e-5` kết hợp với Linear Warmup Scheduler | Khuyến nghị chuẩn mực cho AdamW |
| **Optimizer** | Adam thông thường | **AdamW** (Decoupled Weight Decay = 0.01) | Loshchilov & Hutter (2019) |
| **Classifier Head** | 5 tầng Dense liên tiếp (400->25), không Dropout | 1 tầng Linear duy nhất phía trên `[CLS]` token có Dropout = 0.1 | Kiến trúc chuẩn của Hugging Face SequenceClassification |
| **Số lượng Epoch** | 100 epochs (Overfitting) | 2 đến 3 epochs | Tránh hiện tượng catastrophic forgetting & overfitting |
| **Kiểm soát Model** | Đánh giá epoch cuối (overfit) | Lưu checkpoint theo Validation F1/Loss, load best weights | Đảm bảo mô hình đạt hiệu năng tổng quát cao nhất |

---

## 4. Kết luận rút ra cho sinh viên

Khi bảo vệ trước hội đồng giảng viên, sinh viên cần trình bày rõ ràng:
1. Con số 65.2% trong tài liệu cũ **không phản ánh năng lực thực sự của BERT**, mà là kết quả của một chuỗi sai sót kỹ thuật (mâu thuẫn bảng từ vựng, đóng băng encoder, learning rate quá cao và overfitting 100 epoch).
2. Trong thực nghiệm đã hoàn tất, pipeline fine-tuning được duy trì (Hugging Face + PyTorch, đồng bộ uncased, lr=2e-5, AdamW, 3 epochs) đạt **84.83% Test Accuracy** và **0.8483 Macro F1**. Đây là kết quả đóng băng của cấu hình hiện tại và thay thế các mức dự báo trước thực nghiệm.
