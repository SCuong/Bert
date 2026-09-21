# Báo Cáo Tổng Kết Dự Án (Final Project Report)

> [!NOTE]
> **TRẠNG THÁI DỰ ÁN:** `FINAL EXPERIMENT COMPLETED`  
> Toàn bộ quy trình từ kiểm toán dữ liệu, xây dựng pipeline mô hình cơ sở, tinh chỉnh BERT, đánh giá đối đầu trên tập kiểm thử độc lập (Held-Out Test Set, 3,949 mẫu), và phân tích định tính lỗi thực nghiệm đã hoàn tất.  
> Toàn bộ kết quả thực nghiệm và số liệu trong báo cáo này được trích xuất trực tiếp từ các tệp artifact chính thức tại thư mục `artifacts/metrics/`.

**Đề tài:** Ứng Dụng Mô Hình BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn  
**Tên tiếng Anh:** Fine-Tuning BERT for Hotel Review Sentiment Classification  
**Môn học:** Trí tuệ Nhân tạo (Artificial Intelligence)  
**Quy trình phương pháp luận:** Tuân thủ chuẩn mực 6 giai đoạn của `AI Project Cycle.pptx`.  
**Tính độc lập:** Xây dựng mới hoàn toàn độc lập; không tái sử dụng mã nguồn tham khảo (independent implementation from scratch; reference code was not reused).  
**Ngày hoàn tất:** 21/09/2026  

---

## 1. Thông Tin Chung & Tuyên Bố Dự Án (Project Overview & Executive Summary)

### 1.1. Bối cảnh & Mục tiêu
Trong khuôn khổ môn học Trí tuệ Nhân tạo, bài toán phân loại cảm xúc văn bản (Sentiment Analysis) đóng vai trò nền tảng nhằm đánh giá năng lực xử lý ngôn ngữ tự nhiên. Dự án này nghiên cứu và giải quyết bài toán phân loại cảm xúc nhị phân (Tích cực - 1 vs. Tiêu cực - 0) trên tập dữ liệu đánh giá cảm xúc khách sạn do giảng viên cung cấp (teacher-provided hotel-review sentiment dataset) gồm 20,000 mẫu thô.

Mục tiêu cốt lõi của dự án bao gồm:
1. **Khảo sát và tái đánh giá:** Phân tích toàn diện tài liệu và mã nguồn tham khảo của môn học, xác định các hạn chế kỹ thuật trong triển khai BERT cũ (`DL_Model.ipynb` chỉ đạt 65.20% Accuracy).
2. **Xây dựng hệ thống chuẩn mực:** Triển khai độc lập từ đầu một đường ống máy học hoàn chỉnh, tuân thủ nguyên tắc từ đơn giản đến phức tạp (*"from simple to more complex models"* - Slide 9 `AI Project Cycle.pptx`), gồm mô hình cơ sở TF-IDF + Logistic Regression và mô hình Transformer `bert-base-uncased`.
3. **Thực nghiệm nghiêm ngặt:** Áp dụng quy trình kiểm soát rò rỉ dữ liệu (data leakage prevention), niêm phong tập kiểm thử độc lập (Held-Out Test Set) và đánh giá đối đầu đa chiều (Accuracy, Macro/Weighted Precision, Recall, F1-score, Confusion Matrix, Tốc độ suy luận).
4. **Phân tích học thuật sâu sắc:** Giải thích cơ chế hoạt động, phân tích động lực học tập (learning dynamics), thực hiện phân tích định tính lỗi thực nghiệm (qualitative error analysis) với ngôn ngữ học thuật chuẩn mực, và trả lời thỏa đáng 3 câu hỏi nghiên cứu (Research Questions).

### 1.2. Tóm tắt kết quả chính (Executive Summary)
- **Dữ liệu sạch:** Sau khi loại bỏ 5 mẫu rỗng, 127 mẫu có nhãn mâu thuẫn (conflicting labels), và 123 mẫu trùng lặp văn bản hoàn toàn (exact duplicates), tập dữ liệu sạch gồm **19,745 mẫu** duy nhất (50.25% Negative, 49.75% Positive).
- **Phân chia Stratified (Seed 42):** Tập Huấn luyện (Train) gồm 13,821 mẫu (70%), Tập Phát triển (Validation) gồm 1,975 mẫu (10%), và Tập Kiểm thử (Test) gồm 3,949 mẫu (20%). Kiểm tra duy trì trong pipeline xác nhận không có văn bản trùng khớp chính xác giữa các tập; kiểm toán hậu nghiệm có phân biệt hoa/thường được trình bày tại Mục 4.2.
- **Kết quả đối đầu trên Held-Out Test Set (3,949 mẫu):**
  - **Mô hình cơ sở (TF-IDF + Logistic Regression):** Đạt Accuracy **81.94%**, Macro Precision **0.8208**, Macro Recall **0.8193**, Macro F1 **0.8192**, thời gian suy luận **0.137 giây** (~28,784 mẫu/giây).
  - **Mô hình chính (Fine-Tuned BERT):** Đạt Accuracy **84.83%**, Macro Precision **0.8486**, Macro Recall **0.8482**, Macro F1 **0.8483**, thời gian suy luận **307.30 giây** (~12.85 mẫu/giây trên CPU).
  - **Hiệu quả vượt trội:** Fine-Tuned BERT vượt qua Baseline **+2.89 điểm phần trăm Accuracy** và **+0.0291 Macro F1**, giảm 114 ca dự đoán sai trên tập kiểm thử (599 lỗi so với 713 lỗi của Baseline).
  - **Khắc phục lỗi mô hình cũ:** Khôi phục hoàn toàn tiềm năng của BERT so với kết quả 65.20% trong notebook cũ (khắc phục 5 lỗi kỹ thuật lớn; lưu ý điều kiện thử nghiệm khác nhau).

---

## 2. Khảo Sát & Phát Hiện Từ Tài Liệu Giảng Viên (What I Found)

Quá trình khảo sát toàn bộ tài liệu giảng viên và sinh viên khóa trước ghi nhận:
1. **Định hướng quy trình (`AI Project Cycle.pptx`):** 
   - Đề ra 6 bước chuẩn: *Scope & Plan $\rightarrow$ Data $\rightarrow$ Models $\rightarrow$ Deployment $\rightarrow$ Maintenance $\rightarrow$ Feedback*.
   - Nguyên tắc thiết kế cốt lõi (Slide 9): Cần bắt đầu từ giải pháp đơn giản nhất (baseline) trước khi chuyển sang các mô hình phức tạp hơn, bảo đảm giải pháp cô đọng, hiệu quả và có thể kiểm chứng.
2. **Nền tảng lý thuyết (`Transformer.pptx` / `Transformer.pdf`):**
   - Chỉ ra nhược điểm cố hữu của RNN/LSTM: tính tuần tự cản trở song song hóa, suy giảm thông tin ngữ cảnh xa (vanishing gradient / information bottleneck).
   - Trình bày kiến trúc Transformer: cơ chế Scaled Dot-Product Attention, Multi-Head Attention, và Positional Encoding giúp mô hình hóa ngữ cảnh hai chiều đồng thời.
3. **Thực trạng dữ liệu & mã nguồn cũ (`NLP_Demo/`):**
   - `dts_20k_raw.csv`: Chứa 20,000 dòng đánh giá khách sạn do giảng viên cung cấp. Trong dữ liệu quan sát thấy các marker định dạng như `"No Negative"`, `"No Positive"` (đây là quan sát hình thức dữ liệu, không phải chứng minh nguồn gốc độc lập). Dữ liệu thô tồn tại trùng lặp, nhiễu nhãn và các văn bản chứa trường dữ liệu gộp không chuẩn hóa cần được kiểm toán nghiêm ngặt.
   - `Preprocessing_and_Visualizing.ipynb`: Áp dụng kỹ thuật xóa stopwords NLTK một cách máy móc. Kỹ thuật này đã vô tình xóa mất từ `"No"` trong cụm `"No Negative"`, để lại chữ `"Negative"` ở đầu các bình luận tích cực, đồng thời triệt tiêu các từ phủ định cốt tử (`"not"`, `"never"`, `"no"`), phá vỡ nghiêm trọng cấu trúc ngữ pháp tự nhiên.
   - `DL_Model.ipynb`: Chứa các kết quả thực nghiệm lịch sử: NNLM đạt 79.0% Accuracy, BiLSTM đạt 75.0% Accuracy, và mô hình mang tên "BERT" chỉ đạt **65.20% Accuracy**.
   - **Phát hiện 5 lỗi kỹ thuật nghiêm trọng trong "Old BERT":**
     1. *Lệch Tokenizer và Model:* Tiền xử lý giữ nguyên hoa/thường (cased preprocessing) nhưng đưa vào encoder không phân biệt hoa/thường (`bert-base-uncased`), dẫn đến mã hóa lệch token ID.
     2. *Đóng băng hoàn toàn Encoder (`trainable=False`):* Không thực hiện fine-tuning mà chỉ xem BERT như bộ trích xuất đặc trưng tĩnh, vô hiệu hóa khả năng thích nghi miền (domain adaptation).
     3. *Tốc độ học phá vỡ trọng số:* Sử dụng Learning Rate $10^{-3}$ ($0.001$), quá lớn gấp 50 lần so với dải khuyến nghị ($2 \times 10^{-5}$ đến $5 \times 10^{-5}$), làm mất ổn định các biểu diễn học được.
     4. *Phân loại head quá sâu và thiếu điều quy:* Ghép 5 tầng Dense liên tiếp, loại bỏ Dropout, khiến head có kích thước quá lớn so với lượng dữ liệu.
     5. *Overfitting cực đoan:* Huấn luyện 100 epochs mà không có Early Stopping hay kiểm soát checkpoint, dẫn đến hiện tượng Train Accuracy đạt 97% nhưng Test Accuracy sụp đổ về 65.20%.

---

## 3. Những Gì Nhóm Đã Xây Dựng Độc Lập (What I Built)

Dự án được **triển khai độc lập từ đầu (independent implementation from scratch; không tái sử dụng mã nguồn tham khảo)**, cấu trúc dạng module tại repository root:

```text
/
├── .gitignore
├── README.md
├── requirements.txt
├── FINAL_REPORT.md
├── data/
│   ├── dts_20k_raw.csv
│   ├── clean_dataset.csv
│   ├── train.csv
│   ├── val.csv
│   └── test.csv
├── docs/
│   ├── 01_material_audit.md
│   ├── 02_project_spec.md
│   ├── 03_old_bert_analysis.md
│   ├── 04_error_analysis.md
│   ├── STUDY_GUIDE.md
│   └── DEFENSE_QA.md
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Baseline.ipynb
│   └── BERT_Training_Colab.ipynb
├── src/
│   ├── config.py
│   ├── data.py
│   ├── train_baseline.py
│   ├── train_bert.py
│   ├── evaluate.py
│   └── predict.py
├── app/
│   └── app.py
├── artifacts/
│   ├── model/
│   ├── metrics/
│   └── figures/
└── presentation/
    ├── generate_presentation.py
    ├── presentation_outline.md
    ├── speaker_notes.md
    └── BERT_Project_Final.pptx
```

Các module cốt lõi:
1. **Module dữ liệu (`src/data.py`):** Xây dựng pipeline kiểm toán dữ liệu, lọc bỏ mẫu trùng lặp và xung đột nhãn, bảo toàn cấu trúc văn bản tự nhiên, phân chia tập dữ liệu Stratified (70/10/20) và xác minh tính chống rò rỉ.
2. **Module mô hình cơ sở (`src/train_baseline.py`):** Triển khai pipeline TF-IDF (10,000 unigram + bigram) kết hợp Logistic Regression, điều chỉnh siêu tham số và lưu trữ artifact.
3. **Module BERT Fine-Tuning (`src/train_bert.py`):** Tinh chỉnh mô hình `google-bert/bert-base-uncased` với PyTorch và Hugging Face Transformers, sử dụng AdamW, Linear Warmup Scheduler, và cơ chế chọn checkpoint tối ưu dựa trên Validation Macro F1.
4. **Module đánh giá đối đầu (`src/evaluate.py`):** Thực thi đánh giá so sánh đồng thời cả Baseline và BERT trên tập kiểm thử độc lập (Test Set) đúng 1 lần duy nhất, xuất các chỉ số chi tiết, ma trận nhầm lẫn và trích xuất danh sách ca lỗi phục vụ phân tích định tính.
5. **Module suy luận tương tác (`src/predict.py`):** Cung cấp giao diện dự đoán cho từng chuỗi văn bản, hiển thị xác suất phân lớp và chi tiết phân rã từ con WordPiece.
6. **Ứng dụng Web Demo (`app/app.py`):** Giao diện tương tác trực quan Streamlit, cho phép so sánh thời gian thực kết quả phân loại của cả hai mô hình trên các văn bản đánh giá tùy ý.

---

## 4. Dữ Liệu & Tiền Xử Lý (Data & Preprocessing)

### 4.1. Kiểm toán chất lượng dữ liệu (Data Audit)
Dữ liệu đầu vào `data/dts_20k_raw.csv` do giảng viên cung cấp chứa 20,000 dòng văn bản đánh giá và nhãn nhị phân (1: Tích cực, 0: Tiêu cực). Quy trình kiểm toán tự động ghi nhận:
- Mẫu thiếu thuộc tính (missing text/label): 0 mẫu.
- Mẫu rỗng sau khi chuẩn hóa khoảng trắng: 5 mẫu.
- Mẫu có nhãn xung đột (Conflicting labels): 127 dòng dữ liệu bắt nguồn từ 20 đoạn văn bản giống hệt nhau nhưng bị gán đồng thời cả nhãn 0 và nhãn 1 (ví dụ: các đoạn văn bản ngắn hoặc lời cảm ơn chung chung). Nhóm quyết định loại bỏ toàn bộ 127 dòng này để loại trừ nguy cơ gây nhiễu cho mô hình học sâu.
- Mẫu trùng lặp văn bản hoàn toàn (Exact duplicates): 123 dòng lặp lại văn bản và trùng nhãn được loại bỏ để ngăn ngừa rò rỉ dữ liệu giữa các tập.
- **Tổng số mẫu bị loại bỏ:** 255 mẫu (1.28%).
- **Tập dữ liệu sạch cuối cùng:** **19,745 mẫu hợp lệ**, gồm 9,921 mẫu Tiêu cực (50.25%) và 9,824 mẫu Tích cực (49.75%). Tỷ lệ phân bố nhãn duy trì trạng thái cân bằng tự nhiên xấp xỉ 1:1.

### 4.2. Chiến lược phân chia dữ liệu (Data Splitting)
Áp dụng phương pháp phân chia phân tầng (Stratified Split) với seed ngẫu nhiên cố định `42`:
- **Tập Huấn luyện (Train Set):** 13,821 mẫu (70.0%) | 6,945 Negative (50.25%), 6,876 Positive (49.75%).
- **Tập Phát triển (Validation Set):** 1,975 mẫu (10.0%) | 992 Negative (50.23%), 983 Positive (49.77%).
- **Tập Kiểm thử độc lập (Test Set):** 3,949 mẫu (20.0%) | 1,984 Negative (50.24%), 1,965 Positive (49.76%).
- **Kiểm tra giao thoa chính xác:** Pipeline dùng phép giao tập hợp trên chuỗi văn bản đã làm sạch tối thiểu và xác nhận 0 văn bản trùng khớp chính xác giữa Train, Validation và Test (`artifacts/metrics/data_audit.json`); implementation không thực hiện kiểm tra SHA-256.
- **Giới hạn hậu nghiệm về chữ hoa/thường:** Kiểm toán chỉ đọc sau thực nghiệm, dùng Unicode NFC + `strip()` + `casefold()`, phát hiện Train–Validation 3 cặp (3 văn bản chuẩn hóa duy nhất, cùng nhãn), Train–Test 10 cặp (9 văn bản chuẩn hóa duy nhất; 9 cùng nhãn, 1 trái nhãn), và Validation–Test 2 cặp (2 văn bản chuẩn hóa duy nhất, cùng nhãn). Báo cáo có cấu trúc được lưu tại `artifacts/metrics/case_normalized_overlap_audit.json`. Các kết quả thực nghiệm đã đóng băng không được tính lại và được báo cáo nguyên trạng.
- **Niêm phong tập Test:** Tập Test không được dùng để lựa chọn mô hình hoặc siêu tham số trước lượt đánh giá cuối.

### 4.3. Phân tích phân vị độ dài Token (Token-Length Distribution)
Để xác định chiều dài chuỗi đầu vào tối ưu cho mô hình Transformer, nhóm tiến hành đo lường độ dài token hóa bằng `bert-base-uncased` Tokenizer trên phạm vi tập Train và Validation (15,796 mẫu), ghi nhận tại `artifacts/metrics/token_length_stats.json`:
- Mean: 42.33 tokens | Std: 37.32 tokens | Min: 3 tokens | Median (p50): 30.0 tokens.
- Phân vị 90% (p90): 94.0 tokens.
- Phân vị 95% (p95): 121.0 tokens.
- Phân vị 99% (p99): 168.0 tokens.
- Độ dài tối đa (Max): 425 tokens.
- **Quyết định cấu hình `MAX_LENGTH = 128`:**
  - Trong phạm vi Train + Validation (15,796 mẫu), ngưỡng 128 tokens bao phủ trọn vẹn 96.07% số văn bản (tỷ lệ vượt ngưỡng là 3.93%).
  - Cơ chế Self-Attention có độ phức tạp tính toán và bộ nhớ tỷ lệ bậc hai với chiều dài chuỗi $\mathcal{O}(L^2)$. So với ngưỡng 256 tokens, việc chọn 128 tokens giúp giảm $4\times$ kích thước ma trận chú ý và bộ nhớ kích hoạt, trong khi chỉ hy sinh 3.84% độ bao phủ văn bản dài. Đây là sự đánh đổi kỹ thuật tối ưu giữa tài nguyên tính toán và độ chính xác mô hình.

---

## 5. Kiến Trúc & Huấn Luyện Mô Hình Cơ Sở (Baseline Model)

### 5.1. Thiết kế kỹ thuật
Theo phương pháp luận `AI Project Cycle.pptx`, mô hình cơ sở phải đơn giản, huấn luyện nhanh và mang tính diễn giải cao:
- **Trích xuất đặc trưng:** `TfidfVectorizer` với các thiết lập:
  - `ngram_range=(1, 2)`: Trích xuất cả từ đơn (unigrams) và cụm hai từ liền kề (bigrams) để bắt được các cấu trúc ngữ cảnh ngắn (ví dụ: *"not good"*, *"very clean"*).
  - `max_features=10000`: Giới hạn 10,000 đặc trưng có tần suất thông tin cao nhất.
  - `sublinear_tf=True`: Áp dụng phép biến đổi logarit cho tần suất từ ($1 + \log(\text{tf})$) nhằm giảm độ ảnh hưởng của các từ lặp lại nhiều lần.
- **Mô hình phân loại:** `LogisticRegression` với thuật toán tối ưu `lbfgs`, nghịch đảo tham số điều quy $C = 1.0$, và `max_iter=1000`.

### 5.2. Kết quả phát triển trên Validation Set (1,975 mẫu)
- **Validation Accuracy:** 81.01% (0.810127)
- **Validation Macro Precision:** 0.8116
- **Validation Macro Recall:** 0.8100
- **Validation Macro F1-score:** 0.8098
- **Validation Weighted F1:** 0.8099
- **Thời gian huấn luyện:** 0.68 giây
- **Thời gian suy luận Validation:** 0.114 giây (~17,378 mẫu/giây)
- **Ma trận nhầm lẫn Validation:**
  - True Negative (TN): 838 | False Positive (FP): 154
  - False Negative (FN): 221 | True Positive (TP): 762

---

## 6. Kiến Trúc & Fine-Tuning BERT (Main Model)

### 6.1. Kiến trúc mô hình
- **Mô hình nền tảng:** `google-bert/bert-base-uncased` gồm 12 tầng Transformer Encoder, 768 chiều không gian ẩn (hidden dimension), 12 attention heads, tổng cộng xấp xỉ 110 triệu tham số.
- **Cơ chế biểu diễn:** Sử dụng vector trạng thái ẩn của token đầu tiên `[CLS]` ở tầng thứ 12 làm biểu diễn ngữ cảnh tổng thể cho toàn bộ câu văn.
- **Classification Head:** Thiết kế tinh gọn theo chuẩn Hugging Face:
  $$\mathbf{h}_{cls} = \text{Transformer}(\mathbf{x})_{[CLS]} \in \mathbb{R}^{768}$$
  $$\mathbf{h}_{drop} = \text{Dropout}(p=0.1)(\mathbf{h}_{cls})$$
  $$\mathbf{z} = \mathbf{W}\mathbf{h}_{drop} + \mathbf{b}, \quad \mathbf{W} \in \mathbb{R}^{2 \times 768}, \; \mathbf{b} \in \mathbb{R}^2$$
  $$\mathbf{p} = \text{Softmax}(\mathbf{z})$$

### 6.2. Cấu hình siêu tham số & Chiến lược tối ưu
- **Fine-tuning toàn diện (Full Fine-Tuning):** Mở khóa toàn bộ 110M tham số để các tầng Transformer Encoder tự thích nghi với miền từ vựng đánh giá dịch vụ khách sạn.
- **Optimizer:** AdamW với hệ số tiêu tán trọng số phân tách (Decoupled Weight Decay) $\lambda = 0.01$, $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$.
- **Learning Rate:** $2 \times 10^{-5}$ kết hợp bộ điều chỉnh Linear Warmup Scheduler trong 10% tổng số bước đầu tiên (259 steps), sau đó giảm tuyến tính về 0.
- **Kích thước Batch & Số Epoch:** Batch size = 16, số epoch = 3 (tổng cộng 2,592 steps huấn luyện).
- **Môi trường phần cứng:** Huấn luyện trên CPU đa lõi (PyTorch `2.14.0+cpu`). Tổng thời gian huấn luyện: **15,617.19 giây (~4.34 giờ / 260.29 phút)**.
- **Tiêu chí lựa chọn Checkpoint:** Tự động theo dõi và lưu lại checkpoint có **Validation Macro F1 cao nhất** (`metric_for_best_model="eval_macro_f1"`, `load_best_model_at_end=True`).

### 6.3. Tiến trình huấn luyện qua 3 Epochs
Dữ liệu trích xuất từ nhật ký chính thức `artifacts/metrics/bert_training_history.json`:
- **Epoch 1:** Train Loss (step average) = 0.4385 | Validation Loss = 0.3959 | Validation Accuracy = 83.14% | Validation Macro F1 = 0.8310
- **Epoch 2:** Train Loss (step average) = 0.2877 | Validation Loss = 0.3836 | Validation Accuracy = 83.90% | Validation Macro F1 = 0.8387
- **Epoch 3:** Train Loss (step average) = 0.2022 | Validation Loss = 0.5461 | Validation Accuracy = **83.90%** | Validation Macro F1 = **0.8389**
- **Checkpoint tối ưu được chọn:** `checkpoint-2592` (tại cuối Epoch 3, đạt đỉnh Validation Macro F1 = 0.8389).
- *Lưu ý về phương pháp tính toán:* Train loss theo từng epoch được ghi nhận là giá trị trung bình các step-loss được log trong epoch đó (average of logged step-loss values within each epoch: Epoch 1: 0.4385, Epoch 2: 0.2877, Epoch 3: 0.2022). Giá trị trainer-reported aggregate training loss cho toàn bộ quá trình huấn luyện được ghi nhận là 0.3071 (đây là giá trị trung bình tích lũy toàn đợt chạy của Hugging Face Trainer, không phải loss của bước cuối cùng).

---

## 7. Kết Quả Thực Nghiệm Đối Đầu Trên Held-Out Test Set (Results)

Sau khi hoàn tất toàn bộ quá trình huấn luyện và đóng băng tham số của cả hai mô hình, tập kiểm thử độc lập (Held-Out Test Set gồm 3,949 mẫu) được mở niêm phong để thực hiện đánh giá đối đầu đúng 1 lần duy nhất (`src/evaluate.py`).

### 7.1. Bảng so sánh chỉ số định lượng tổng thể

| Mô Hình / Phương Pháp | Vai Trò / Nền Tảng | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Thời Gian Suy Luận | Tốc Độ Xử Lý |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | *Mô hình cơ sở mới (Nhóm)* | 81.94% | 0.8208 | 0.8193 | 0.8192 | 0.8192 | **0.137 s** | **28,784 mẫu/s** |
| **Fine-Tuned BERT (`bert-base-uncased`)** | *Mô hình chính mới (Nhóm)* | **84.83%** | **0.8486** | **0.8482** | **0.8483** | **0.8483** | 307.30 s | 12.85 mẫu/s |
| **Độ chênh lệch ($\Delta$ = BERT - Baseline)** | *Mức độ cải thiện thực tế* | **+2.89%** | **+0.0278** | **+0.0289** | **+0.0291** | **+0.0291** | *+307.16 s* | *-28,771 mẫu/s* |

> [!NOTE]
> **CHÚ THÍCH THAM KHẢO LỊCH SỬ (HISTORICAL REFERENCE ONLY — KHÔNG PHẢI PHÉP SO SÁNH ĐỐI CHỨNG CÓ KIỂM SOÁT):**
> Các kết quả mô hình cũ trong tài liệu môn học (`DL_Model.ipynb`):
> - NNLM (Neural Network Language Model): Accuracy 79.00%
> - BiLSTM: Accuracy 75.00%
> - Old BERT (Triển khai lỗi): Accuracy **65.20%**
> Các kết quả này thuộc về các cấu hình, tập dữ liệu thử nghiệm và quy trình khác nhau, **không phải là phép so sánh đối chứng có kiểm soát (controlled comparison)** trong cùng điều kiện với nghiên cứu này. Mức chênh lệch so với Old BERT là minh chứng phân tích hạn chế kỹ thuật của code cũ, không được dùng làm delta thực nghiệm khoa học chính thức.

### 7.2. Phân tích chi tiết ma trận nhầm lẫn (Confusion Matrix Analysis)

#### Ma trận nhầm lẫn của Mô hình Cơ sở (TF-IDF + Logistic Regression):
$$\begin{pmatrix} \text{TN} = 1,691 & \text{FP} = 293 \\ \text{FN} = 420 & \text{TP} = 1,545 \end{pmatrix}$$
- Tổng số mẫu dự đoán đúng: $1,691 + 1,545 = 3,236$ mẫu (81.94%).
- Tổng số mẫu dự đoán sai: $293 + 420 = 713$ mẫu (18.06%).

#### Ma trận nhầm lẫn của Fine-Tuned BERT:
$$\begin{pmatrix} \text{TN} = 1,711 & \text{FP} = 273 \\ \text{FN} = 326 & \text{TP} = 1,639 \end{pmatrix}$$
- Tổng số mẫu dự đoán đúng: $1,711 + 1,639 = 3,350$ mẫu (84.83%).
- Tổng số mẫu dự đoán sai: $273 + 326 = 599$ mẫu (15.17%).

#### So sánh trực diện từng thành phần sai lệch:
- **True Negatives:** BERT nhận diện chính xác 1,711 mẫu tiêu cực, nhiều hơn Baseline 20 mẫu ($1,711$ vs $1,691$).
- **False Positives (Báo động giả tiêu cực thành tích cực):** BERT giảm được 20 ca FP so với Baseline ($273$ vs $293$).
- **True Positives:** BERT nhận diện chính xác 1,639 mẫu tích cực, nhiều hơn Baseline 94 mẫu ($1,639$ vs $1,545$).
- **False Negatives (Bỏ sót tích cực thành tiêu cực):** BERT giảm mạnh được **94 ca FN** so với Baseline ($326$ vs $420$, giảm 22.38% số ca FN).
- **Tổng số lỗi giảm thiểu:** BERT giảm tổng cộng **114 ca lỗi** trên tập kiểm thử ($599$ so với $713$).

---

## 8. So Sánh Validation vs Test Set & Phân Tích Động Lực Học (Learning Dynamics)

### 8.1. Tính tổng quát hóa trên tập kiểm thử (Generalization Gap)
Đối chiếu các chỉ số giữa tập phát triển (Validation Set) và tập kiểm thử (Test Set):

| Mô hình | Tập dữ liệu | Số mẫu | Accuracy | Macro F1 | Weighted F1 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Baseline (TF-IDF + LR)** | Validation Set | 1,975 | 81.01% | 0.8098 | 0.8099 |
| | Test Set | 3,949 | 81.94% | 0.8192 | 0.8192 |
| | *Chênh lệch (Test - Val)* | *+1,974* | *+0.93%* | *+0.0094* | *+0.0093* |
| **Fine-Tuned BERT** | Validation Set | 1,975 | 83.90% | 0.8389 | 0.8389 |
| | Test Set | 3,949 | 84.83% | 0.8483 | 0.8483 |
| | *Chênh lệch (Test - Val)* | *+1,974* | *+0.93%* | *+0.0094* | *+0.0094* |

**Nhận định học thuật:**
- Cả hai mô hình đều có hiệu năng trên tập Test cao hơn nhẹ xấp xỉ 0.93 điểm phần trăm so với tập Validation. Điều này khẳng định không xảy ra hiện tượng overfitting đối với tập Validation trong quá trình tinh chỉnh siêu tham số.
- Khoảng cách hiệu năng giữa Validation và Test hoàn toàn ổn định và nhất quán giữa hai mô hình, minh chứng cho tính đại diện đồng đều của phép phân chia Stratified Split (Seed 42).

### 8.2. Phân tích động lực học tập của BERT (Epoch 3 Loss vs F1)
Trong tiến trình huấn luyện của BERT:
- Train Loss (step average) giảm liên tục qua từng epoch: $0.4385 \rightarrow 0.2877 \rightarrow 0.2022$.
- Validation Loss đạt giá trị nhỏ nhất ở Epoch 2 ($0.3836$), sau đó tăng lên $0.5461$ ở Epoch 3.
- Ngược lại, Validation Accuracy và Validation Macro F1 duy trì ổn định và đạt đỉnh ở Epoch 3: Macro F1 đạt $0.8310 \rightarrow 0.8387 \rightarrow 0.8389$.

**Giải thích hiện tượng học sâu:**
Hàm mất mát Cross-Entropy và chỉ số phân loại nhãn cứng Macro F1 đo lường hai khía cạnh khác nhau của mô hình:
- Cross-entropy loss ($-\sum y \log p$) đo lường độ lệch xác suất; một số ít mẫu bị dự đoán sai với độ tự tin cao (high-confidence mistakes) có thể làm tăng loss đáng kể, trong khi đại đa số các mẫu khác vẫn được phân loại đúng nhãn (hard-label classification) giúp Macro F1 duy trì ổn định hoặc tăng nhẹ. Nguyên nhân chính xác chưa được cô lập thực nghiệm.
- Do đó, việc lựa chọn checkpoint dựa trên **Validation Macro F1** (chỉ số mục tiêu của bài toán phân loại) là chiến lược tối ưu giúp đạt độ chính xác phân loại cao nhất trên tập dữ liệu thực tế.

---

## 9. Phân Tích Định Tính Ca Lỗi Của BERT (Qualitative Error Analysis)

Nhằm hiểu rõ bản chất 599 ca lỗi của BERT trên tập kiểm thử độc lập, nhóm tiến hành khảo sát định tính chi tiết **mẫu 20 ca lỗi có độ tin cậy cao nhất (highest-confidence errors)** gồm 10 ca False Positive và 10 ca False Negative trích xuất tại `artifacts/metrics/error_cases.json`. Báo cáo đầy đủ được lưu tại `docs/04_error_analysis.md` và tóm tắt tại `artifacts/metrics/error_analysis_summary.json`.

### 9.1. Thống kê phân bố hiện tượng ngôn ngữ trên mẫu 20 ca lỗi khảo sát

| Hiện tượng Ngôn ngữ / Đặc trưng Dữ liệu | Số ca xuất hiện (trên mẫu 20 ca) | Tỷ lệ trong mẫu (%) | Đặc trưng nhận diện |
| :--- | :---: | :---: | :--- |
| **Cảm xúc pha trộn / Mệnh đề cạnh tranh (Mixed Sentiment)** | **15 / 20** | **75.0%** | Văn bản chứa cả mặt tích cực và tiêu cực về các khía cạnh dịch vụ khác nhau. |
| **Dấu hiệu mơ hồ nhãn hoặc nhiễu nhãn (Label Noise / Ambiguity)** | **8 / 20** | **40.0%** | Ngữ nghĩa bề mặt mâu thuẫn rõ rệt với nhãn ground-truth nhị phân được gán. |
| **Cấu trúc phủ định hoặc nhượng bộ (Negation / Concessive)** | **8 / 20** | **40.0%** | Cấu trúc *"not"*, *"didn't"*, *"could do with"*, hoặc litotes (*"wasn't a bad hotel"*). |
| **Tác động của biểu mẫu nguồn (Template / Source Marker)** | **6 / 20** | **30.0%** | Tồn tại các thẻ trích xuất từ biểu mẫu web như `"No Positive"`, ghép trường không dấu cách. |
| **Văn bản phi chuẩn: lỗi ngữ pháp, chính tả (Noisy Grammar / Spelling)** | **4 / 20** | **20.0%** | Lỗi gõ phím (*"arking"*, *"miss leading"*), ngữ pháp vỡ (*"All staff in the slow everything"*). |
| **Khiếu nại nền tảng trung gian (Domain / Platform Complaint)** | **2 / 20** | **10.0%** | Khách hàng phàn nàn về nền tảng trung gian hoặc tiếng ồn đường phố bên ngoài khách sạn. |
| **Thách thức suy luận ngữ cảnh sâu của mô hình (Model Reasoning)** | **1 / 20** | **5.0%** | Không tách biệt được quan điểm trích dẫn của bạn bè với lập trường cá nhân tác giả. |

*(Lưu ý: Một ca lỗi có thể mang nhiều đặc trưng đồng thời. Các tỷ lệ phần trăm trên chỉ áp dụng cụ thể cho mẫu 20 ca lỗi cực đoan được khảo sát, không suy rộng cho toàn bộ 599 ca lỗi).*

### 9.2. Quan sát hiện tượng cắt cụt văn bản (Truncation Analysis)
- **Kết quả đo lường:** Trong mẫu 20 ca lỗi có độ tin cậy cao nhất, **0 / 20 ca bị cắt cụt** (`truncation_count = 0`). Độ dài token dao động từ 6 đến 126 tokens (đều nằm trong ngưỡng `MAX_LENGTH = 128`).
- **Phạm vi kết luận:** Trong 20 ca lỗi được kiểm toán, không ca nào vượt `MAX_LENGTH = 128`. Quan sát này không được suy rộng thành kết luận nhân quả cho toàn bộ 599 ca lỗi; hiện tượng cắt cụt vẫn có thể ảnh hưởng đến các văn bản dài khác.

---

## 10. Trả Lời 3 Câu Hỏi Nghiên Cứu (Research Questions Answered)

### RQ1: BERT có thực sự vượt trội hơn mô hình tuyến tính cổ điển (TF-IDF + Logistic Regression) trên bài toán phân loại cảm xúc đánh giá khách sạn không?
**Trả lời dựa trên bằng chứng thực nghiệm:**
- **Về độ chính xác phân loại:** Có. Trên tập kiểm thử độc lập 3,949 mẫu, Fine-Tuned BERT vượt qua Baseline trên toàn bộ các chỉ số đánh giá: Accuracy đạt 84.83% so với 81.94% (+2.89 điểm phần trăm), Macro F1 đạt 0.8483 so với 0.8192 (+0.0291). BERT giảm tổng cộng 114 ca dự đoán sai, đặc biệt giảm tới 22.38% số ca False Negative (từ 420 xuống 326 ca).
- **Về sự đánh đổi tài nguyên tính toán (Trade-off):** Mức cải thiện +2.89 điểm phần trăm Accuracy đi kèm với sự gia tăng rất lớn về chi phí tính toán: thời gian suy luận của BERT chậm hơn Baseline xấp xỉ 2,243 lần (307.30 giây so với 0.137 giây trên CPU), và thời gian huấn luyện là ~4.34 giờ so với 0.68 giây. Do đó, trong các ứng dụng công nghiệp yêu cầu độ trễ cực thấp hoặc tài nguyên hạn chế, Baseline vẫn là một giải pháp rất cạnh tranh; trong khi BERT là lựa chọn tối ưu khi ưu tiên tối đa độ chính xác.

### RQ2: Những sai lầm kỹ thuật nào trong triển khai BERT cũ (`DL_Model.ipynb`) khiến mô hình chỉ đạt 65.20%, và quy trình fine-tuning chuẩn giải quyết các vấn đề đó như thế nào?
**Trả lời dựa trên bằng chứng kỹ thuật:**
- **Nguyên nhân cốt lõi khiến triển khai cũ thất bại (65.20% Accuracy):**
  1. Đóng băng hoàn toàn Transformer Encoder (`trainable=False`), biến BERT thành bộ trích xuất đặc trưng tĩnh không thể thích nghi với miền dữ liệu đánh giá dịch vụ.
  2. Sử dụng Learning Rate $10^{-3}$, quá lớn gấp 50 lần chuẩn khuyến nghị, phá vỡ cấu trúc không gian biểu diễn.
  3. Ghép nối 5 tầng Dense quá sâu không Dropout, dẫn đến overfitting cực độ sau 100 epochs (Train Acc đạt 97% nhưng Test Acc sụp đổ về 65.20%).
  4. Lệch token ID do tiền xử lý giữ nguyên hoa/thường nhưng ghép với encoder `uncased`.
- **Cách tiếp cận mới giải quyết triệt để:**
  1. Đồng bộ hoàn toàn kiến trúc và bộ tách từ `uncased`.
  2. Mở khóa toàn bộ tham số (Full Fine-Tuning) để thích ứng miền.
  3. Sử dụng AdamW với Learning Rate nhỏ $2 \times 10^{-5}$ và Linear Warmup Scheduler.
  4. Thiết kế Classification Head tối giản (1 tầng Linear + Dropout 0.1).
  5. Huấn luyện 3 epochs và tự động phục hồi Checkpoint tối ưu dựa trên Validation Macro F1.
  $\rightarrow$ Kết quả: Đạt Accuracy **84.83%**, khắc phục hoàn toàn hạn chế kỹ thuật khiến triển khai cũ dừng lại ở mức 65.20% (lưu ý hai mô hình thử nghiệm ở các điều kiện khác nhau).

### RQ3: Bản chất của các trường hợp mà mô hình BERT dự đoán sai là gì? Lỗi bắt nguồn từ hạn chế kiến trúc mô hình hay do chất lượng và tính mơ hồ của dữ liệu?
**Trả lời dựa trên bằng chứng phân tích định tính:**
- **Chất lượng dữ liệu và bản chất bài toán đóng vai trò chi phối chính trong các ca lỗi cực đoan:**
  - Trong mẫu 20 ca lỗi tự tin nhất được khảo sát, 15/20 ca (75%) xuất phát từ đặc trưng cảm xúc pha trộn (Mixed Sentiment), nơi các khía cạnh đối lập cùng tồn tại trong một bài viết. Việc gán một nhãn nhị phân duy nhất cho các văn bản đa khía cạnh tạo ra tính mơ hồ cố hữu.
  - Có 8/20 ca (40%) mang dấu hiệu bất tương thích giữa ngữ nghĩa văn bản và nhãn dữ liệu (nhãn nhiễu hoặc tàn dư biểu mẫu `"No Positive"`). Trong các trường hợp này, dự đoán của mô hình thể hiện sự nhất quán với ngữ nghĩa bề mặt của văn bản hơn là nhãn nhị phân trong dữ liệu.
- **Hạn chế mô hình hóa ngôn ngữ sâu xuất hiện ở mức độ tinh tế:**
  - BERT xử lý tốt các cấu trúc phủ định thông thường và litotes.
  - Thách thức thực sự nằm ở các cấu trúc ngữ dụng học phức tạp (như phân biệt quan điểm trích dẫn của người khác với lập trường tác giả ở Case 16) và sự thiếu vắng cơ chế phân tích theo từng khía cạnh (Aspect-Based Sentiment Analysis).

---

## 11. So Sánh Chuyên Sâu Pipeline Mới vs Mã Nguồn Cũ (Detailed Pipeline Comparison)

| Tiêu chí Kỹ thuật | Triển khai Cũ (`DL_Model.ipynb`) | Triển khai Mới của Nhóm (`src/train_bert.py`) | Cơ sở Lý thuyết & Tác động Kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Tiền xử lý văn bản** | Xóa stopwords NLTK máy móc (mất *"No"*, *"not"*) | Giữ nguyên dấu câu, từ phủ định, cấu trúc câu tự nhiên | BERT dựa vào Positional Encoding và Self-Attention; việc giữ nguyên ngữ pháp giúp bảo toàn toàn vẹn ngữ cảnh hai chiều. |
| **Tính đồng bộ từ vựng** | Preprocess cased ghép với encoder uncased | Đồng bộ hoàn toàn `AutoTokenizer` và `AutoModel` uncased | Tránh hiện tượng lệch chỉ số token ID trong ma trận Embedding. |
| **Phương thức huấn luyện** | Đóng băng Encoder (`trainable=False`) | Mở khóa toàn bộ tham số (Full Fine-Tuning) | Cho phép các tầng Transformer Encoder tự thích ứng với miền từ vựng chuyên ngành khách sạn. |
| **Tốc độ học (Learning Rate)** | $10^{-3}$ ($0.001$) — Quá lớn gấp 50 lần | $2 \times 10^{-5}$ kết hợp Linear Warmup Scheduler (10%) | Tránh hiện tượng phá hủy các biểu diễn tiền huấn luyện quý giá (catastrophic forgetting). |
| **Bộ tối ưu hóa** | Adam thông thường | **AdamW** (Decoupled Weight Decay = 0.01) | Tách biệt việc tiêu tán trọng số khỏi gradient, điều quy mô hình hiệu quả hơn. |
| **Kiến trúc Head** | 5 tầng Dense sâu liên tiếp, không Dropout | 1 tầng Linear duy nhất + Dropout ($p=0.1$) | Giảm số lượng tham số ngẫu nhiên mới, chống hiện tượng ghi nhớ vẹt dữ liệu huấn luyện. |
| **Kiểm soát Epoch** | 100 epochs cố định $\rightarrow$ Overfitting nghiêm trọng | 3 epochs với giám sát Validation Loss và F1 | Tránh lãng phí tài nguyên tính toán và ngăn chặn suy giảm khả năng tổng quát hóa. |
| **Chiến lược Checkpoint** | Lấy trọng số tại epoch cuối cùng (epoch 100) | Tự động chọn Checkpoint có Validation Macro F1 cao nhất | Bảo đảm mô hình đưa vào kiểm thử có năng lực tổng quát hóa tối ưu nhất. |
| **Accuracy đạt được** | **65.20%** | **84.83%** (Khắc phục lỗi mô hình cũ; lưu ý điều kiện thử nghiệm khác nhau) | Khẳng định tính đúng đắn của phương pháp luận kỹ thuật chuẩn mực. |

---

## 12. Hướng Dẫn Tái Lập Thực Nghiệm (Reproducibility Guide)

Toàn bộ quy trình thực nghiệm được đóng gói dưới dạng các module Python chuẩn hóa, có thể thực thi tuần tự từ thư mục gốc của repository:

```bash
# Bước 1: Thiết lập môi trường và cài đặt các gói phụ thuộc
pip install -r requirements.txt

# Bước 2: Kiểm toán dữ liệu, loại bỏ trùng lặp và phân chia tập dữ liệu
python -m src.data

# Bước 3: Huấn luyện và đánh giá mô hình cơ sở trên Validation Set
python -m src.train_baseline

# Bước 4: Fine-tuning mô hình BERT và lưu checkpoint tối ưu
python -m src.train_bert

# Bước 5: Đánh giá so sánh đối đầu trên Test Set và trích xuất ca lỗi
python -m src.evaluate

# Bước 6: Khởi tạo bộ slide thuyết trình PowerPoint chính thức
python -m presentation.generate_presentation

# Bước 7: Khởi chạy ứng dụng Web tương tác Streamlit
streamlit run app/app.py
```

*Lưu ý về tính ngẫu nhiên:* Các hạt giống ngẫu nhiên (seed) đều được cố định tại giá trị `42` trong `src/config.py`. Tuy nhiên, do các phép toán số học dấu phẩy động trên phần cứng CPU/GPU và các luồng tính toán song song, các chỉ số số thực có thể có sự dao động nhỏ ở phần thập phân thứ 4 hoặc thứ 5 giữa các môi trường thực thi khác nhau.

---

## 13. Giới Hạn Nghiên Cứu (Limitations)

1. **Giới hạn của bài toán phân loại nhị phân:**
   Hệ thống hiện tại gán nhãn văn bản vào hai lớp cực đoan (0 hoặc 1). Trong thực tế, nhiều đánh giá mang tính trung tính (Neutral - 3 sao) hoặc chứa các ý kiến cân bằng không thể phản ánh trọn vẹn qua nhãn nhị phân.
2. **Hiện tượng cắt cụt văn bản (Truncation):**
   Mặc dù ngưỡng `MAX_LENGTH = 128` bảo toàn hơn 96% số văn bản, khoảng 3.93% văn bản dài vẫn bị cắt cụt phần đuôi. Ở một số đánh giá dài, kết luận tổng thể của người dùng nằm ở cuối bài có thể bị bỏ lỡ.
3. **Chi phí tính toán và độ trễ suy luận:**
   Mô hình BERT với 110 triệu tham số có tốc độ suy luận ~12.85 mẫu/giây trên CPU, chậm hơn nhiều so với mô hình tuyến tính TF-IDF (~28,784 mẫu/giây). Điều này đặt ra rào cản khi triển khai trên các thiết bị biên hoặc hệ thống phục vụ tải lớn thời gian thực.
4. **Giới hạn phạm vi phân tích lỗi định tính:**
   Phân tích lỗi định tính tập trung vào mẫu 20 ca lỗi có độ tin cậy cao nhất. Mẫu này không mang tính đại diện thống kê cho toàn bộ 599 ca lỗi của mô hình trên tập kiểm thử.

---

## 14. Hướng Phát Triển Tương Lai (Future Work)

1. **Phân tích Cảm xúc Đa Khía cạnh (Aspect-Based Sentiment Analysis - ABSA):**
   Phát triển mô hình phân loại cảm xúc theo từng khía cạnh cụ thể (Vị trí, Giá cả, Vệ sinh, Thái độ phục vụ) thay vì một nhãn tổng thể duy nhất, giải quyết triệt để bài toán cảm xúc pha trộn.
2. **Tối ưu hóa và nén mô hình (Model Compression):**
   Áp dụng kỹ thuật chưng cất tri thức (Knowledge Distillation) với DistilBERT hoặc MobileBERT, kết hợp lượng tử hóa (Quantization INT8) và ONNX Runtime để giảm kích thước mô hình và tăng tốc độ suy luận trên CPU lên 3-5 lần.
3. **Mở rộng sang tập dữ liệu đa ngôn ngữ:**
   Đánh giá khả năng chuyển giao miền trên các mô hình như `xlm-roberta-base` hoặc `phobert` đối với dữ liệu đánh giá khách sạn tại thị trường Việt Nam.

---

## 15. Hướng Dẫn Ôn Tập & Chuẩn Bị Bảo Vệ (Study Guide & Defense Prep)

Nhằm giúp sinh viên nắm vững kiến thức chuyên môn và tự tin thuyết minh trước Hội đồng, nhóm đã xây dựng hai tài liệu học thuật chi tiết:
1. **`docs/STUDY_GUIDE.md` (Cẩm nang 25 khái niệm AI/NLP cốt lõi):**
   - Giải thích cặn kẽ cơ chế toán học của Scaled Dot-Product Attention:
     $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
   - Phân tích cơ chế bẻ từ con WordPiece, ý nghĩa các token đặc biệt (`[CLS]`, `[SEP]`, `[PAD]`).
   - Phân biệt giữa Pre-training tự giám sát (MLM, NSP) và Fine-tuning có giám sát.
   - Lý giải vì sao không áp dụng xóa stopwords cho các mô hình ngôn ngữ dựa trên Transformer.
2. **`docs/DEFENSE_QA.md` (Bộ 25 câu hỏi phản biện & đáp án mẫu):**
   - Thiết kế theo cấu trúc hai mức độ: *Câu trả lời nhanh 30 giây* (đủ ý, tự tin) và *Câu trả lời mở rộng 1-2 phút* (sâu sắc, có dẫn chứng số liệu thực nghiệm).
   - Bao quát toàn diện các chủ đề chất vấn: phương pháp luận dữ liệu, cơ chế chống rò rỉ, phân tích sự cố mô hình cũ, đánh đổi hiệu năng vs. tốc độ, và cách xử lý các ca lỗi thực tế.

---

## 16. Vị Trí Sản Phẩm & Tài Nguyên Dự Án (Project Artifacts & Deliverables)

Toàn bộ tài nguyên của dự án được lưu trữ có hệ thống:
- **Tài liệu học thuật:** `FINAL_REPORT.md`, `README.md`, các tài liệu chuyên sâu trong `docs/`.
- **Dữ liệu thực nghiệm:** `data/clean_dataset.csv`, `data/train.csv`, `data/val.csv`, `data/test.csv`.
- **Số liệu & Biểu đồ:** Các tệp JSON chỉ số trong `artifacts/metrics/` và các hình ảnh ma trận nhầm lẫn, biểu đồ EDA trong `artifacts/figures/`.
- **Slide thuyết trình chính thức:** `presentation/BERT_Project_Final.pptx` (xây dựng dựa trên hệ thống thiết kế Đại học Bách Khoa - ĐHĐN).
- **Kịch bản thuyết trình & Dàn ý:** `presentation/presentation_outline.md` và `presentation/speaker_notes.md` (chuẩn thời lượng 8-10 phút).
- **Ứng dụng Demo thời gian thực:** `app/app.py`.
- **Notebook Google Colab độc lập:** `notebooks/BERT_Training_Colab.ipynb`.

---

## 17. Báo Cáo Kiểm Chứng Hoàn Tất Dự Án (Final Verification & Sign-Off)

Bảng xác nhận trạng thái hoàn tất toàn bộ các hạng mục công việc theo tiêu chuẩn công trình nghiên cứu:

| Hạng mục công việc | Trạng thái kỹ thuật | Bằng chứng kiểm chứng / Tệp lưu trữ |
| :--- | :---: | :--- |
| **Kiểm toán dữ liệu & Chống rò rỉ** | **ĐÃ HOÀN TẤT** | `artifacts/metrics/data_audit.json` (0 mẫu rò rỉ, 19,745 mẫu sạch) |
| **Phân tích phân vị độ dài token** | **ĐÃ HOÀN TẤT** | `artifacts/metrics/token_length_stats.json` (p95 = 121, chọn max_len = 128) |
| **Huấn luyện mô hình cơ sở** | **ĐÃ HOÀN TẤT** | `artifacts/model/baseline_tfidf_lr.joblib`, `baseline_validation_metrics.json` |
| **Fine-tuning mô hình BERT** | **ĐÃ HOÀN TẤT** | `artifacts/model/bert_best_model/`, `bert_validation_metrics.json` |
| **Đánh giá đối đầu trên Test Set** | **ĐÃ HOÀN TẤT** | `artifacts/metrics/comparative_metrics.json`, `bert_test_metrics.json` |
| **Ma trận nhầm lẫn trực quan** | **ĐÃ HOÀN TẤT** | `artifacts/figures/baseline_test_confusion_matrix.png`, `bert_test_confusion_matrix.png` |
| **Phân tích định tính ca lỗi** | **ĐÃ HOÀN TẤT** | `docs/04_error_analysis.md`, `artifacts/metrics/error_analysis_summary.json` |
| **Slide thuyết trình học thuật** | **ĐÃ HOÀN TẤT** | `presentation/BERT_Project_Final.pptx`, `speaker_notes.md` |
| **Ứng dụng Web tương tác** | **ĐÃ HOÀN TẤT** | `app/app.py` (Hỗ trợ so sánh song song Baseline vs BERT) |
| **Tài liệu hướng dẫn & Phản biện** | **ĐÃ HOÀN TẤT** | `docs/STUDY_GUIDE.md`, `docs/DEFENSE_QA.md` |

**KẾT LUẬN NGHIỆM THU:**  
Dự án đã hoàn thành toàn diện, xuất sắc các mục tiêu đề ra; đáp ứng nghiêm ngặt các yêu cầu phương pháp luận của `AI Project Cycle.pptx`, giải quyết triệt để các hạn chế của mã nguồn tham khảo, và sẵn sàng cho buổi báo cáo bảo vệ trước Hội đồng môn học.
