"""
generate_presentation.py - Tự động tạo slide PowerPoint học thuật chuẩn mực (15 slides).
Sử dụng python-pptx, thiết kế trang nhã, tối giản chữ, nhúng biểu đồ thực nghiệm.

Tính năng bảo vệ tính trung thực (Integrity Guard):
- Nếu chưa có metrics thực tế từ thực nghiệm, bắt buộc phải truyền cờ `--draft` để tạo bản DRAFT.
- Nếu không có cờ `--draft` mà thiếu metrics, script sẽ FAIL FAST, ngăn chặn việc tạo deck giả mạo.
"""

import os
import sys
import json
import argparse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Import cấu hình tập trung
from src.config import (
    MODEL_NAME,
    MAX_LENGTH,
    RANDOM_SEED,
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
    PROJECT_ROOT,
    FIGURES_DIR,
    BASELINE_METRICS_PATH,
    BERT_METRICS_PATH
)

def create_presentation(is_draft=False):
    # Guard kiểm tra tính trung thực của thực nghiệm
    has_baseline_metrics = os.path.exists(BASELINE_METRICS_PATH)
    has_bert_metrics = os.path.exists(BERT_METRICS_PATH)

    if not (has_baseline_metrics and has_bert_metrics) and not is_draft:
        raise RuntimeError(
            "FAIL FAST GUARD: Không tìm thấy kết quả thực nghiệm thực tế tại "
            f"'{BASELINE_METRICS_PATH}' hoặc '{BERT_METRICS_PATH}'.\n"
            "Bài thuyết trình chính thức chỉ được phép tạo sau khi đã hoàn tất huấn luyện và đánh giá thực tế.\n"
            "Để tạo bản nháp kiểm tra định dạng (DRAFT), vui lòng chạy lại với cờ: python presentation/generate_presentation.py --draft"
        )

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Widescreen standard
    blank_layout = prs.slide_layouts[6]

    # Bảng màu học thuật trang nhã
    NAVY = RGBColor(26, 54, 93)       # #1A365D
    STEEL = RGBColor(43, 108, 176)    # #2B6CB0
    CHARCOAL = RGBColor(45, 55, 72)   # #2D3748
    MUTED = RGBColor(113, 128, 150)   # #718096
    BG_BOX = RGBColor(247, 250, 252)  # #F7FAFC
    BORDER_COLOR = RGBColor(226, 232, 240) # #E2E8F0
    WHITE = RGBColor(255, 255, 255)
    DRAFT_RED = RGBColor(197, 48, 48)

    baseline_metrics = {}
    bert_metrics = {}
    if has_baseline_metrics:
        with open(BASELINE_METRICS_PATH, "r", encoding="utf-8") as f:
            baseline_metrics = json.load(f)
    if has_bert_metrics:
        with open(BERT_METRICS_PATH, "r", encoding="utf-8") as f:
            bert_metrics = json.load(f)

    def add_header(slide, title_text, subtitle_text=""):
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.font.name = "Arial"

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(12)
            p2.font.color.rgb = MUTED
            p2.font.name = "Arial"
            p2.space_before = Pt(4)

        if is_draft:
            p_draft = tf.add_paragraph()
            p_draft.text = "[DRAFT — PRE-EXPERIMENT CHECKPOINT / SỐ LIỆU CHƯA QUA HUẤN LUYỆN THỰC TẾ]"
            p_draft.font.size = Pt(10)
            p_draft.font.bold = True
            p_draft.font.color.rgb = DRAFT_RED
            p_draft.space_before = Pt(2)

    def add_card(slide, left, top, width, height, title="", body="", bg=BG_BOX, border=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg
        shape.line.color.rgb = border
        shape.line.width = Pt(1)

        if title or body:
            tf = shape.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.25)
            tf.margin_top = Inches(0.25)
            tf.margin_right = Inches(0.25)
            tf.margin_bottom = Inches(0.25)

            if title:
                p = tf.paragraphs[0]
                p.text = title
                p.font.size = Pt(15)
                p.font.bold = True
                p.font.color.rgb = NAVY
                p.font.name = "Arial"

            if body:
                p_body = tf.add_paragraph() if title else tf.paragraphs[0]
                p_body.text = body
                p_body.font.size = Pt(12)
                p_body.font.color.rgb = CHARCOAL
                p_body.font.name = "Arial"
                p_body.space_before = Pt(6)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(245, 247, 250)
    bg1.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "ĐỒ ÁN MÔN HỌC: TRÍ TUỆ NHÂN TẠO"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = STEEL
    p.font.name = "Arial"

    p = tf1.add_paragraph()
    p.text = "Ứng Dụng BERT Trong Phân Loại Cảm Xúc Đánh Giá Khách Sạn"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.font.name = "Arial"
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Fine-Tuning BERT for Hotel Review Sentiment Classification"
    p.font.size = Pt(18)
    p.font.color.rgb = CHARCOAL
    p.font.name = "Arial"
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    draft_tag = " • [DRAFT / PRE-EXPERIMENT]" if is_draft else ""
    p.text = f"Quy trình chuẩn mực tuân thủ AI Project Cycle • Thực nghiệm độc lập & Tái lập 100%{draft_tag}"
    p.font.size = Pt(13)
    p.font.color.rgb = MUTED if not is_draft else DRAFT_RED
    p.font.name = "Arial"
    p.space_before = Pt(18)

    add_card(s1, Inches(1.2), Inches(5.4), Inches(10.9), Inches(1.1),
             title="Thông Tin Báo Cáo",
             body=f"Mô hình: {MODEL_NAME} | Baseline: TF-IDF + Logistic Regression | Dữ liệu: Teacher-provided dataset\nPhương pháp: Clean-Room Implementation | Tái lập: Seed={RANDOM_SEED}")

    # =========================================================================
    # SLIDE 2: Scope & Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "01. Bối Cảnh & Mục Tiêu Nghiên Cứu", "Giai đoạn 01 (Scope & Plan) theo chuẩn AI Project Cycle")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Phát Biểu Bài Toán & Bối Cảnh",
             body="• Bối cảnh: Hàng ngàn đánh giá khách sạn trực tuyến được đăng tải mỗi ngày. Việc phân loại thủ công tốn kém nhân lực và thiếu kịp thời.\n\n"
                  "• Input: Văn bản nhận xét bằng tiếng Anh của khách lưu trú.\n"
                  "• Output: Nhãn phân loại nhị phân (Positive - 1 / Negative - 0) kèm độ tin cậy.\n\n"
                  "• Các bên liên quan (Stakeholders):\n"
                  "  - Ban quản lý khách sạn: Cần phát hiện khiếu nại ngay lập tức.\n"
                  "  - Khách hàng: Mong muốn phản hồi được lắng nghe.\n"
                  "  - Kỹ sư AI: Xây dựng hệ thống chính xác, giải thích được.")

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Mục Tiêu & Tiêu Chí Đánh Giá",
             body="• Mục tiêu kỹ thuật:\n"
                  "  1. Xây dựng mô hình cơ sở TF-IDF + Logistic Regression.\n"
                  f"  2. Fine-tuning chuẩn mực mô hình {MODEL_NAME}.\n"
                  "  3. So sánh đối sánh khách quan giữa Machine Learning và Transformer.\n"
                  "  4. Phân tích định tính các ca dự đoán sai (Error Analysis).\n\n"
                  "• Tiêu chí đánh giá chất lượng:\n"
                  "  - Macro F1-Score & Accuracy trên tập Test độc lập.\n"
                  "  - Khả năng khái quát hóa, không bị overfit trên tập Train.\n"
                  "  - Tính tái lập (Reproducibility): Cố định seed 42 xuyên suốt.\n"
                  "  - Ứng dụng Demo tương tác thời gian thực bằng Streamlit.")

    # =========================================================================
    # SLIDE 3: Evolution of NLP
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "02. Tiến Hóa Kiến Trúc: Từ RNN/LSTM Đến Transformer", "Bước chuyển dịch mô hình tính toán trong Xử lý Ngôn ngữ Tự nhiên")
    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Hạn Chế Cốt Tử Của RNN & LSTM",
             body="• Tính toán tuần tự (Sequential Bottleneck):\n"
                  "  - Muốn xử lý từ thứ t phải chờ trạng thái ẩn của từ t-1.\n"
                  "  - KHÔNG THỂ tính toán song song trên GPU.\n"
                  "  - Thời gian huấn luyện lâu trên tập dữ liệu lớn.\n\n"
                  "• Suy biến Gradient (Vanishing Gradient):\n"
                  "  - Khi độ dài chuỗi tăng, thông tin đầu câu bị suy giảm.\n"
                  "  - Khó nắm bắt các phụ thuộc tầm xa (Long-range dependencies).\n\n"
                  "• Hạn chế của BiLSTM:\n"
                  "  - Ghép nối 2 mạng độc lập (trái sang + phải sang), thiếu tương tác sâu.")

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Đột Phá Của Transformer (Vaswani et al., 2017)",
             body="• Loại bỏ hoàn toàn mạng hồi quy (No Recurrence):\n"
                  "  - Xử lý toàn bộ các từ trong câu ĐỒNG THỜI.\n"
                  "  - Tận dụng tối đa sức mạnh tính toán song song của GPU.\n\n"
                  "• Cơ chế Self-Attention (Tự chú ý):\n"
                  "  - Kết nối trực tiếp mọi cặp từ trong câu với đường truyền O(1).\n"
                  "  - Triệt tiêu hoàn toàn hiện tượng suy biến gradient.\n\n"
                  "• Mã hóa vị trí (Positional Encoding):\n"
                  "  - Bổ sung thông tin trật tự từ vào không gian nhúng.\n\n"
                  "• Khả năng mở rộng (Scalability):\n"
                  "  - Đặt nền móng cho các mô hình ngôn ngữ lớn hiện đại.")

    # =========================================================================
    # SLIDE 4: BERT Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "03. Kiến Trúc BERT & Cơ Chế Multi-Head Self-Attention", "Cấu tạo toán học của mô hình Bidirectional Encoder Representations from Transformers")
    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Bản Chất Kiến Trúc BERT",
             body="• Chỉ sử dụng phần ENCODER của Transformer:\n"
                  "  - Phục vụ tác vụ thấu hiểu và biểu diễn ngữ nghĩa (Language Understanding).\n"
                  "  - Deeply Bidirectional: Tự do nhìn đồng thời cả hai chiều trái và phải.\n\n"
                  "• Cấu hình BERT-base (Devlin et al., 2018):\n"
                  "  - 12 tầng Transformer Encoder (L=12)\n"
                  "  - Kích thước ẩn H=768, 12 Attention Heads (A=12)\n"
                  "  - ~110 Triệu tham số được tiền huấn luyện trên 3.3 tỷ từ.\n\n"
                  "• Token đặc biệt:\n"
                  "  - [CLS]: Đứng đầu câu, vector đại diện phân loại.\n"
                  "  - [SEP]: Đánh dấu kết thúc câu.")

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Cơ Chế Scaled Dot-Product Attention",
             body="• Công thức cốt lõi:\n"
                  "  Attention(Q, K, V) = softmax( (Q * K^T) / sqrt(d_k) ) * V\n\n"
                  "• Bộ ba vector Query, Key, Value:\n"
                  "  - Query (Q): Câu hỏi / nhu cầu tìm kiếm của từ hiện tại.\n"
                  "  - Key (K): Nhãn nhận diện tương thích của các từ trong câu.\n"
                  "  - Value (V): Nội dung ngữ nghĩa thực sự mà từ mang theo.\n\n"
                  "• Hệ số co giãn 1/sqrt(d_k):\n"
                  "  - Ngăn tích vô hướng quá lớn làm bão hòa gradient tại Softmax.\n\n"
                  "• Multi-Head Attention (12 Heads):\n"
                  "  - Học song song nhiều mối liên kết ngữ pháp và ngữ nghĩa khác nhau.")

    # =========================================================================
    # SLIDE 5: Dataset & EDA
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "04. Phân Tích Khám Phá Dữ Liệu (Data & EDA)", "Giai đoạn 02 (Data) theo AI Project Cycle — Kiểm soát chất lượng dữ liệu")
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Đặc Tính Tập Dữ Liệu",
             body="• Nguồn dữ liệu: Teacher-provided hotel-review dataset.\n"
                  "  - Tổng quy mô ban đầu: 20,000 bài đánh giá tiếng Anh.\n"
                  "  - Cân bằng nhãn: 10,000 Positive (1) và 10,000 Negative (0).\n\n"
                  "• Audit trùng lặp & Rò rỉ (Pre-split Audit):\n"
                  "  - Kiểm tra missing values và chuỗi rỗng.\n"
                  "  - Phân tích và loại bỏ exact duplicate texts.\n"
                  "  - Loại bỏ các văn bản có nhãn xung đột (Conflicting labels).\n"
                  "  - Đảm bảo 100% không có dữ liệu trùng giữa Train và Test.\n\n"
                  "• Nhận diện đặc trưng cấu trúc:\n"
                  "  - Xuất hiện các marker phổ biến như 'No Negative' trong review tích cực.\n"
                  "  - Giữ nguyên cấu trúc tự nhiên, không xóa stopwords để bảo tồn ngữ nghĩa.")

    len_img = os.path.join(FIGURES_DIR, "token_length_distribution.png")
    if not os.path.exists(len_img):
        len_img = os.path.join(FIGURES_DIR, "length_distribution.png")

    if os.path.exists(len_img):
        s5.shapes.add_picture(len_img, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    else:
        add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                 title="Phân Bố Độ Dài Token (EDA)",
                 body="• Phương pháp đo lường:\n"
                  f"  - Sử dụng trực tiếp Tokenizer thực tế ({MODEL_NAME}).\n"
                  "  - Không suy diễn độ dài token chỉ qua số từ (word count).\n\n"
                  "• Trạng thái hiện tại:\n"
                  "  [PENDING EXPERIMENT — SẼ ĐƯỢC XUẤT SAU KHI CHẠY EDA THỰC TẾ]\n\n"
                  "• Mục tiêu phân tích:\n"
                  "  - Xác định tỷ lệ cắt cụt (truncation rate) tại ngưỡng 128 và 256.\n"
                  "  - Tối ưu hóa bộ nhớ GPU và tốc độ huấn luyện.")

    # =========================================================================
    # SLIDE 6: Project Pipeline
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "05. Quy Trình Nghiên Cứu Chuẩn Mực (Pipeline)", "Độc lập, khoa học và ngăn chặn hoàn toàn rò rỉ dữ liệu (No Data Leakage)")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
             title="1. Dữ Liệu & Phân Chia",
             body="• Tiền xử lý tối thiểu:\n"
                  "  - Xóa thẻ HTML, chuẩn hóa khoảng trắng.\n"
                  "  - GIỮ NGUYÊN stopwords & từ phủ định.\n"
                  "  - Lọc trùng lặp & xung đột trước split.\n\n"
                  f"• Stratified Split (seed={RANDOM_SEED}):\n"
                  f"  - Train Set ({int(TRAIN_RATIO*100)}%): Cập nhật tham số.\n"
                  f"  - Val Set ({int(VAL_RATIO*100)}%): Chọn checkpoint.\n"
                  f"  - Test Set ({int(TEST_RATIO*100)}%): Đánh giá độc lập 1 lần duy nhất.")

    add_card(s6, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
             title="2. Mô Hình Hóa (Modeling)",
             body="• Mô hình cơ sở (Baseline):\n"
                  "  - TF-IDF (10,000 unigram + bigram).\n"
                  "  - Logistic Regression (L-BFGS).\n\n"
                  f"• Mô hình BERT Fine-Tuning:\n"
                  f"  - {MODEL_NAME}\n"
                  "  - PyTorch Dataset thuần túy.\n"
                  "  - Optimizer: AdamW (Weight decay=0.01).\n"
                  "  - Learning Rate: 2e-5 + Linear Warmup.\n"
                  "  - 3 Epochs, load_best_model_at_end.")

    add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             title="3. Đánh Giá & Ứng Dụng",
             body="• Đánh giá toàn diện:\n"
                  "  - Accuracy, Precision, Recall, Macro F1.\n"
                  "  - Confusion Matrix.\n"
                  "  - Đối sánh trực tiếp với Baseline.\n\n"
                  "• Phân tích lỗi (Error Analysis):\n"
                  "  - Trích xuất các ca dự đoán sai.\n"
                  "  - Khảo sát định tính theo nhóm nguyên nhân.\n\n"
                  "• Triển khai (Deployment):\n"
                  "  - Demo Streamlit trực quan, thời gian thực.")

    # =========================================================================
    # SLIDE 7: Baseline Model
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "06. Mô Hình Cơ Sở (Baseline): TF-IDF + Logistic Regression", "Tuân thủ triết lý AI Project Cycle: 'Start from simple to more complex models'")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Cấu Hình & Đặc Tính Kỹ Thuật",
             body="• Mục đích Baseline:\n"
                  "  - Thiết lập chuẩn đối sánh tối thiểu.\n"
                  "  - Trả lời câu hỏi: Liệu Transformer có thực sự cần thiết so với giải pháp đơn giản?\n\n"
                  "• Kiến trúc Pipeline:\n"
                  "  - TfidfVectorizer: N-gram (1, 2), max_features = 10,000.\n"
                  "  - sublinear_tf = True: Giảm độ ảnh hưởng của từ xuất hiện quá nhiều.\n"
                  "  - LogisticRegression: C=1.0, max_iter=1000, solver='lbfgs'.\n\n"
                  "• Nhược điểm cố hữu của Túi từ (Bag-of-Words):\n"
                  "  - Không hiểu trật tự từ và các cấu trúc đảo ngữ phức tạp.")

    baseline_body = (
        f"• Đánh giá trên tập Test Set độc lập:\n\n"
        f"  - Test Accuracy:        {baseline_metrics.get('accuracy', 0.0)*100:.2f}%\n"
        f"  - Macro Precision:      {baseline_metrics.get('macro_precision', 0.0):.4f}\n"
        f"  - Macro Recall:         {baseline_metrics.get('macro_recall', 0.0):.4f}\n"
        f"  - Macro F1-Score:       {baseline_metrics.get('macro_f1', 0.0):.4f}\n"
        f"  - Thời gian huấn luyện: {baseline_metrics.get('training_time_seconds', 0.0):.2f}s\n\n"
        "• Nhận định:\n"
        "  - Thiết lập mốc đo lường chuẩn xác trước khi so sánh với BERT."
    ) if has_baseline_metrics else (
        "• Đánh giá trên tập Test Set độc lập:\n\n"
        "  - Trạng thái: [PENDING EXPERIMENT]\n"
        "  - Test Accuracy:        [Pending]\n"
        "  - Macro Precision:      [Pending]\n"
        "  - Macro Recall:         [Pending]\n"
        "  - Macro F1-Score:       [Pending]\n"
        "  - Thời gian huấn luyện: [Pending]\n\n"
        "• Mục tiêu thực nghiệm:\n"
        "  - Sẽ được tạo tự động khi chạy python src/train_baseline.py."
    )
    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Kết Quả Thực Nghiệm Baseline",
             body=baseline_body)

    # =========================================================================
    # SLIDE 8: Experimental Design & Fine-Tuning Strategy (REPLACED AS REQUESTED)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07. Thiết Kế Thực Nghiệm & Chiến Lược Fine-Tuning", "Cấu hình chuẩn mực học thuật cho mô hình BERT")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Quy Chuẩn & Lựa Chọn Mô Hình",
             body=f"• Mô hình cốt lõi: {MODEL_NAME}\n"
                  "  - 12 tầng Transformer, H=768, 12 Attention Heads (~110M tham số).\n"
                  "  - Mở khóa toàn bộ trọng số để thích ứng ngữ cảnh bài toán (True Fine-Tuning).\n\n"
                  "• Đồng bộ Tokenizer:\n"
                  "  - Sử dụng AutoTokenizer uncased đi kèm, từ điển 30,522 WordPiece tokens.\n\n"
                  f"• Độ dài chuỗi tối đa (Max Length): {MAX_LENGTH}\n"
                  "  - Căn cứ theo phân tích phân vị độ dài token từ EDA.\n\n"
                  "• Tầng phân loại (Sequence Classification Head):\n"
                  "  - Vector [CLS] (768 chiều) -> Dropout(0.1) -> Linear(768, 2) -> Softmax.")

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Chiến Lược Huấn Luyện & Tái Lập (Reproducibility)",
             body="• Bộ tối ưu hóa (Optimizer): AdamW\n"
                  "  - Decoupled Weight Decay = 0.01 để kiểm soát độ lớn trọng số.\n\n"
                  "• Tốc độ học (Learning Rate): 2e-5\n"
                  "  - Đi kèm Linear Warmup Scheduler trong 10% số bước đầu.\n\n"
                  "• Số lượng Epoch: 2 - 3 Epochs\n"
                  "  - Tránh overfitting trên tập dữ liệu đánh giá.\n\n"
                  "• Chiến lược chọn Checkpoint:\n"
                  "  - Đánh giá trên Validation Set sau mỗi epoch.\n"
                  "  - Tự động lưu và phục hồi checkpoint có Validation F1 tốt nhất.\n\n"
                  f"• Đảm bảo tái lập: Cố định seed={RANDOM_SEED} cho toàn bộ quá trình.")

    # =========================================================================
    # SLIDE 9: BERT Fine-Tuning Pipeline
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08. Triển Khai Kỹ Thuật Fine-Tuning BERT", "Độc lập, không phụ thuộc thư viện ngoài, tối ưu tài nguyên tính toán")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Kiến Trúc Triển Khai Thuần PyTorch",
             body="• PyTorch Dataset thuần túy (HotelReviewDataset):\n"
                  "  - Kế thừa trực tiếp torch.utils.data.Dataset.\n"
                  "  - Không phụ thuộc vào gói thư viện bên ngoài (datasets/arrow).\n"
                  "  - Quản lý bộ nhớ hiệu quả và tương thích trực tiếp với DataLoader.\n\n"
                  "• Pipeline suy luận (Inference Pipeline):\n"
                  "  - Tokenize văn bản đầu vào và sinh ma trận attention_mask.\n"
                  "  - Đưa qua mô hình ở chế độ eval() với torch.no_grad().\n"
                  "  - Trả về nhãn dự đoán, xác suất Softmax và danh sách token WordPiece.")

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Kiểm Soát Quá Trình Huấn Luyện",
             body="• Giám sát độ mất mát (Loss Monitoring):\n"
                  "  - Ghi nhận Train Loss và Validation Loss qua từng epoch.\n"
                  "  - Phát hiện sớm hiện tượng phân kỳ (Overfitting).\n\n"
                  "• Quản lý Artifacts:\n"
                  "  - Trọng số tốt nhất lưu tại artifacts/model/bert_best_model/.\n"
                  "  - Metrics lưu dạng JSON tại artifacts/metrics/.\n"
                  "  - Biểu đồ xuất định dạng 300 DPI tại artifacts/figures/.\n\n"
                  "• Tính độc lập Clean-Room:\n"
                  "  - Toàn bộ pipeline tự vận hành độc lập 100%.")

    # =========================================================================
    # SLIDE 10: Experimental Results Table (FIXED SIZE: 6 ROWS x 6 COLS)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09. Bảng So Sánh Kết Quả Thực Nghiệm Tổng Hợp", "Đánh giá độc lập trên cùng tập kiểm thử Test Set")

    # SỬA LỖI KÍCH THƯỚC: 1 Header + 5 Model Rows = 6 Rows!
    rows, cols = 6, 6
    left, top, width, height = Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8)
    table_shape = s10.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    headers = ["Phương Pháp / Mô Hình", "Nguồn / Phân Loại", "Accuracy", "Precision", "Recall", "Macro F1"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    base_acc_str = f"{baseline_metrics['accuracy']*100:.2f}%" if "accuracy" in baseline_metrics else "[PENDING]"
    base_prec_str = f"{baseline_metrics['macro_precision']:.4f}" if "macro_precision" in baseline_metrics else "[PENDING]"
    base_rec_str = f"{baseline_metrics['macro_recall']:.4f}" if "macro_recall" in baseline_metrics else "[PENDING]"
    base_f1_str = f"{baseline_metrics['macro_f1']:.4f}" if "macro_f1" in baseline_metrics else "[PENDING]"

    bert_acc_str = f"{bert_metrics['accuracy']*100:.2f}%" if "accuracy" in bert_metrics else "[PENDING]"
    bert_prec_str = f"{bert_metrics['macro_precision']:.4f}" if "macro_precision" in bert_metrics else "[PENDING]"
    bert_rec_str = f"{bert_metrics['macro_recall']:.4f}" if "macro_recall" in bert_metrics else "[PENDING]"
    bert_f1_str = f"{bert_metrics['macro_f1']:.4f}" if "macro_f1" in bert_metrics else "[PENDING]"

    data_rows = [
        ["TF-IDF + Logistic Regression", "Mô hình cơ sở mới (Nhóm)", base_acc_str, base_prec_str, base_rec_str, base_f1_str],
        ["NNLM (Google Embedding)", "Historical result from supplied notebook", "79.00%", "0.7900", "0.7900", "0.7900"],
        ["BiLSTM (2-layer)", "Historical result from supplied notebook", "75.00%", "0.7500", "0.7500", "0.7500"],
        ["Old 'BERT' (Reference)", "Historical result from supplied notebook", "65.20%", "0.6550", "0.6520", "0.6500"],
        ["Fine-Tuned BERT (Ours)", "Mô hình chính mới (Nhóm)", bert_acc_str, bert_prec_str, bert_rec_str, bert_f1_str]
    ]

    for i, row in enumerate(data_rows, 1):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = val
            cell.fill.solid()
            # SỬA LỖI HIGHLIGHT: i == 5 là dòng Fine-Tuned BERT (Ours)
            if i == 5:
                cell.fill.fore_color.rgb = RGBColor(235, 248, 255)
            else:
                cell.fill.fore_color.rgb = WHITE if i % 2 == 1 else BG_BOX
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                p.font.name = "Arial"
                p.font.color.rgb = NAVY if i == 5 else CHARCOAL
                if i == 5 or j == 0:
                    p.font.bold = True
                p.alignment = PP_ALIGN.LEFT if j < 2 else PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 11: Confusion Matrix
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10. Ma Trận Nhầm Lẫn & Đánh Giá Chi Tiết Từng Lớp", "So sánh độ chính xác và mức độ cân bằng nhãn trên tập kiểm thử")

    base_cm_img = os.path.join(FIGURES_DIR, "baseline_confusion_matrix.png")
    bert_cm_img = os.path.join(FIGURES_DIR, "bert_confusion_matrix.png")

    if os.path.exists(base_cm_img) and os.path.exists(bert_cm_img):
        s11.shapes.add_picture(base_cm_img, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.5))
        s11.shapes.add_picture(bert_cm_img, Inches(6.8), Inches(1.6), Inches(5.7), Inches(4.5))
    else:
        add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.5),
                 title="Baseline Confusion Matrix",
                 body="[PENDING EXPERIMENT — SẼ ĐƯỢC XUẤT SAU KHI CHẠY train_baseline.py]")
        add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(4.5),
                 title="BERT Confusion Matrix",
                 body="[PENDING EXPERIMENT — SẼ ĐƯỢC XUẤT SAU KHI CHẠY evaluate.py]")

    add_card(s11, Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.9),
             title="Nhận Xét Kỹ Thuật",
             body="• Ma trận nhầm lẫn sẽ được sinh tự động sau khi chạy train_baseline.py và evaluate.py.\n"
                  "• Cho phép so sánh trực tiếp tỷ lệ True Positives, False Positives, True Negatives và False Negatives.")

    # =========================================================================
    # SLIDE 12: Qualitative Error Analysis
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11. Khung Phân Tích Lỗi Định Tính (Error Analysis Framework)", "Phương pháp luận khảo sát định tính các ca dự đoán sai sau khi huấn luyện")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="4 Nhóm Nguyên Nhân Giả Định",
             body="• 1. Cảm xúc pha trộn (Mixed Sentiment):\n"
                  "  - Khách khen vị trí nhưng chê cách âm và vệ sinh.\n"
                  "  - Nhãn gán phụ thuộc vào trọng số cảm tính của người đánh giá.\n\n"
                  "• 2. Cấu trúc phủ định phức tạp & Đảo ngữ:\n"
                  "  - Phủ định đa tầng ('not that it wasn't clean, but...').\n\n"
                  "• 3. Châm biếm / Mỉa mai (Sarcasm):\n"
                  "  - Dùng từ tích cực mang hàm ý chê bai ('free swimming pool in leaking bathroom').\n\n"
                  "• 4. Cắt cụt (Truncation) & Nhiễu nhãn:\n"
                  "  - Review quá dài bị cắt mất đoạn kết luận quan trọng.")

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Quy Trình Trích Xuất Thực Nghiệm",
             body="• Trạng thái hiện tại: [PRE-EXPERIMENT IMPLEMENTATION CHECKPOINT]\n\n"
                  "• Quy trình trích xuất sau khi huấn luyện:\n"
                  "  1. evaluate.py tự động lọc toàn bộ mẫu label != pred trên Test Set.\n"
                  "  2. Sắp xếp theo confidence giảm dần để tìm ca lỗi phân kỳ mạnh nhất.\n"
                  "  3. Lưu danh sách 20 ca lỗi vào artifacts/metrics/error_cases.json.\n"
                  "  4. Cập nhật chi tiết từng câu văn bản vào báo cáo phân tích lỗi.")

    # =========================================================================
    # SLIDE 13: Demo Application
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12. Ứng Dụng Thực Tế: Giao Diện Trực Quan Streamlit", "Giai đoạn 04 (Deployment) theo AI Project Cycle — Kiểm thử thời gian thực")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Tính Năng Của Ứng Dụng (app/app.py)",
             body="• Giao diện Web tương tác nhẹ, mượt mà:\n"
                  "  - Nhập trực tiếp văn bản đánh giá bất kỳ.\n"
                  "  - Cung cấp sẵn các câu ví dụ mẫu thể hiện các tình huống phức tạp.\n\n"
                  "• Trực quan hóa giải thích (Explainability):\n"
                  "  - Hiển thị nhãn kết quả kèm thanh đo xác suất (Probability Gauge).\n"
                  "  - Hiển thị danh sách các tokens WordPiece của BERT ([CLS], ##tokens, [SEP]).\n\n"
                  "• So sánh tức thời đối đầu (Side-by-Side):\n"
                  "  - Đối chiếu kết quả dự đoán của Baseline vs. BERT trên cùng một màn hình.\n\n"
                  "• Cách khởi chạy: streamlit run app/app.py")

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Ý Nghĩa Thực Tiễn & Tích Hợp",
             body="• Phục vụ giám sát hệ thống (Monitoring):\n"
                  "  - Giúp quản lý khách sạn theo dõi mức độ hài lòng của khách theo thời gian thực.\n\n"
                  "• Cảnh báo sớm (Early Alert):\n"
                  "  - Tự động gắn cờ đỏ với các review tiêu cực có độ tin cậy cao để chăm sóc khách hàng kịp thời.\n\n"
                  "• Tính độc lập:\n"
                  "  - Ứng dụng load weights trực tiếp từ thư mục artifacts/model/.")

    # =========================================================================
    # SLIDE 14: Limitations & Future Work
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "13. Giới Hạn & Hướng Phát Triển Tương Lai", "Giai đoạn 05 & 06 (Maintenance & Feedback) theo AI Project Cycle")

    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Các Giới Hạn Hiện Tại",
             body="• 1. Bài toán nhị phân đơn giản hóa (Binary Limitation):\n"
                  "  - Chỉ phân loại 2 lớp 0 và 1, chưa nắm bắt được các đánh giá trung lập (3 sao / Neutral).\n\n"
                  "• 2. Giới hạn độ dài chuỗi (Truncation):\n"
                  f"  - Với max_length = {MAX_LENGTH}, các review dài bị cắt cụt phần đuôi.\n\n"
                  "• 3. Chi phí tài nguyên phần cứng:\n"
                  "  - Mô hình BERT có 110M tham số, tốc độ suy luận chậm hơn so với Logistic Regression.")

    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Hướng Phát Triển Tiếp Theo",
             body="• 1. Phân loại cảm xúc đa khía cạnh (ABSA):\n"
                  "  - Bóc tách chi tiết cảm xúc theo từng tiêu chí: Giá cả, Vệ sinh, Vị trí, Phục vụ.\n\n"
                  "• 2. Nén mô hình (Model Compression):\n"
                  "  - Áp dụng Knowledge Distillation (DistilBERT) hoặc Quantization để tăng tốc suy luận.\n\n"
                  "• 3. Tích hợp ONNX Runtime:\n"
                  "  - Tối ưu hóa suy luận phục vụ triển khai Microservices trên Cloud.")

    # =========================================================================
    # SLIDE 15: Conclusion & References
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "14. Kết Luận & Tài Liệu Tham Khảo", "Tổng kết đóng góp của đồ án môn học")

    add_card(s15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             title="Kết Luận Đồ Án",
             body="• 1. Hoàn thành trọn vẹn quy trình AI Project Cycle:\n"
                  "  - Từ Scope, Data, Baseline, BERT Fine-Tuning đến Demo và Error Analysis.\n\n"
                  "• 2. Triển khai chuẩn mực học thuật:\n"
                  "  - Pipeline Clean-Room độc lập 100%, kiểm soát rò rỉ dữ liệu và chống overfitting.\n\n"
                  "• 3. So sánh khách quan:\n"
                  "  - Đối sánh thực nghiệm giữa Machine Learning truyền thống và Transformer.\n\n"
                  "• 4. Tính tái lập 100%:\n"
                  f"  - Cố định seed={RANDOM_SEED} và tài liệu hóa toàn diện.")

    add_card(s15, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Tài Liệu Tham Khảo Chính",
             body="• [1] Vaswani et al. (2017). 'Attention Is All You Need'. NeurIPS.\n"
                  "• [2] Devlin et al. (2018). 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding'. NAACL.\n"
                  "• [3] Loshchilov & Hutter (2019). 'Decoupled Weight Decay Regularization' (AdamW). ICLR.\n"
                  "• [4] Wolf et al. (2020). 'Transformers: State-of-the-Art Natural Language Processing'. EMNLP.\n"
                  "• [5] Teacher-provided hotel-review sentiment dataset.")

    output_pptx = os.path.join(PROJECT_ROOT, "presentation", "BERT_Project.pptx")
    prs.save(output_pptx)
    status_str = "BẢN NHÁP (DRAFT)" if is_draft else "BẢN CHÍNH THỨC"
    print(f"[+] Đã tạo thành công file PowerPoint ({status_str}) tại: {output_pptx}")
    return output_pptx

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo slide PowerPoint cho đồ án BERT")
    parser.add_argument("--draft", action="store_true", help="Tạo bản nháp khi chưa có kết quả thực nghiệm thực tế")
    args = parser.parse_args()

    create_presentation(is_draft=args.draft)
