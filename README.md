# Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn
### Fine-Tuning BERT for Hotel Review Sentiment Classification

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Transformers-5.17.0-yellow.svg)](https://huggingface.co/)
[![FastAPI](https://img.shields.io/badge/Demo-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

Đồ án môn học **Trí Tuệ Nhân Tạo (Artificial Intelligence)**. Dự án fine-tune BERT để phân loại đánh giá khách sạn **bằng tiếng Anh** thành Positive (1) hoặc Negative (0), đồng thời so sánh với baseline TF-IDF + Logistic Regression.

## Tổng quan

- **Mô hình chính:** fine-tuned `bert-base-uncased` (PyTorch + Hugging Face Transformers).
- **Baseline:** TF-IDF (10,000 unigram + bigram) + Logistic Regression.
- **Dữ liệu:** hotel-review sentiment dataset do giảng viên cung cấp; sau làm sạch còn **19,745** mẫu duy nhất, chia stratified với seed 42: Train **13,821**, Validation **1,975**, Test **3,949**.
- **Triển khai chuẩn:** `src/`; web demo FastAPI tái sử dụng trực tiếp `src.predict.predict_bert`.

## Kết quả chính thức

Các giá trị dưới đây là kết quả đã đóng băng trên cùng held-out Test Set (**3,949** mẫu). Nguồn đối chiếu chuẩn là `artifacts/metrics/`.

| Mô hình / Phương pháp | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Thời gian suy luận | Tốc độ suy luận |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | 81.94% | 0.8208 | 0.8193 | 0.8192 | 0.8192 | **0.137 s** | **28,784 mẫu/s** |
| **Fine-Tuned BERT (`bert-base-uncased`)** | **84.83%** | **0.8486** | **0.8482** | **0.8483** | **0.8483** | 307.30 s | 12.85 mẫu/s |
| **Cải thiện (BERT − Baseline)** | **+2.89 điểm phần trăm** | **+0.0278** | **+0.0289** | **+0.0291** | **+0.0291** | *+307.16 s* | *-28,771 mẫu/s* |

Các kết quả NNLM, BiLSTM và BERT cũ chỉ là tham chiếu lịch sử; xem [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md).

## Chạy web demo

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Mở `http://127.0.0.1:8000`. Endpoint `POST /api/predict` gọi canonical inference trong `src.predict.predict_bert`.

> [!NOTE]
> Dữ liệu thô và trọng số model được giữ cục bộ, không đưa vào Git. Đặt artifact model đã huấn luyện tại `artifacts/model/` trước khi chạy inference.

## Cấu trúc repository

```text
.
├── app/                    # FastAPI demo: backend, template, CSS, JavaScript
├── artifacts/
│   ├── metrics/            # Frozen metrics, error analysis, token statistics
│   ├── figures/            # EDA, confusion matrices, training history
│   └── model/              # Trọng số đã huấn luyện (local, gitignored)
├── data/                   # Ghi chú dữ liệu; raw CSV giữ cục bộ
├── docs/                   # Đặc tả, phân tích lỗi, lịch sử, hướng dẫn và Q&A
├── notebooks/              # Notebook historical/exploratory
├── presentation/           # Slide, outline và speaker notes
├── src/                    # Canonical training, evaluation và inference pipeline
├── FINAL_REPORT.md         # Báo cáo học thuật đầy đủ
└── requirements.txt
```

## Canonical sources và artifacts

- `src/` là implementation được duy trì cho data processing, training, evaluation và prediction.
- `artifacts/metrics/` là nguồn bằng chứng định lượng đã đóng băng; không thay thế số liệu trong các tệp này bằng kết quả chạy lại.
- `notebooks/` là tài liệu historical/exploratory, không thay thế pipeline trong `src/`.
- Hướng dẫn chạy lại từng bước pipeline nằm tại [`docs/02_project_spec.md`](docs/02_project_spec.md).

## Giới hạn chính

- Model hiện chỉ được huấn luyện cho **đánh giá khách sạn bằng tiếng Anh**; không hỗ trợ suy luận tiếng Việt.
- Đây là bộ phân loại cảm xúc nhị phân tổng thể; đánh giá mixed hoặc ambiguous có thể khó hơn. Xem [`docs/04_error_analysis.md`](docs/04_error_analysis.md).
- Kết quả Test Set là frozen results; giao diện demo không retrain hoặc reevaluate model.

## Tài liệu bổ sung

- [`FINAL_REPORT.md`](FINAL_REPORT.md): báo cáo học thuật đầy đủ.
- [`docs/02_project_spec.md`](docs/02_project_spec.md): đặc tả và quy trình dự án.
- [`docs/03_old_bert_analysis.md`](docs/03_old_bert_analysis.md): phân tích chi tiết các triển khai lịch sử.
- [`docs/04_error_analysis.md`](docs/04_error_analysis.md): phân tích 20 ca lỗi.
- [`docs/DEFENSE_QA.md`](docs/DEFENSE_QA.md): câu hỏi và trả lời phản biện.
- [`presentation/BERT_Project_Final.pptx`](presentation/BERT_Project_Final.pptx): slide trình bày cuối cùng.
