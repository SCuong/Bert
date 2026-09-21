"""
generate_presentation.py - Tự động tạo bài thuyết trình học thuật chuẩn mực (13 slides).
Sử dụng template mẫu DUT được cung cấp làm slide layout library & visual design system.
Thiết kế lại toàn diện (Redesign Pass):
- Nền sáng cho các slide nội dung chính, tương phản cao, chữ to rõ ràng.
- Cắt giảm văn bản mạnh tay: One slide = one message, không copy report lên slide.
- Trực quan hóa số liệu: Big numbers, comparison cards, charts, ma trận nhầm lẫn rõ nét.
- Tích hợp số liệu định lượng (JSON) và hình ảnh thực nghiệm (PNG) chính thức.
"""

import os
import sys
import io
import json
import argparse
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.config import (
    MODEL_NAME,
    MAX_LENGTH,
    RANDOM_SEED,
    PROJECT_ROOT,
    FIGURES_DIR,
    BASELINE_MODEL_PATH,
    BERT_BEST_MODEL_DIR,
    BASELINE_TEST_CM_PATH,
    BERT_TEST_CM_PATH
)

# =============================================================================
# COLOR PALETTE — THIẾT KẾ ÁNH SÁNG & TƯƠNG PHẢN CAO
# =============================================================================
NAVY = RGBColor(26, 54, 93)            # #1A365D - Màu chủ đạo DUT (Deep Navy)
STEEL = RGBColor(43, 108, 176)         # #2B6CB0 - Màu nhấn mạnh (Steel Blue)
SKY = RGBColor(49, 130, 206)           # #3182CE - Màu xanh dương sáng
CHARCOAL = RGBColor(45, 55, 72)        # #2D3748 - Màu văn bản chính (tương phản cao)
MUTED = RGBColor(113, 128, 150)        # #718096 - Màu phụ đề / footnote
WHITE = RGBColor(255, 255, 255)        # #FFFFFF - Trắng tinh khiết
BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC - Nền slide sáng (Slate 50)
CARD_BG = RGBColor(255, 255, 255)      # #FFFFFF - Nền card
BORDER_GRAY = RGBColor(226, 232, 240)  # #E2E8F0 - Viền card mềm mại
GREEN = RGBColor(39, 103, 73)          # #276749 - Xanh lá thành công
GREEN_LIGHT = RGBColor(240, 253, 244)  # #F0FDF4 - Nền xanh lá nhạt
RED = RGBColor(197, 48, 48)            # #C53030 - Đỏ cảnh báo / lỗi
RED_LIGHT = RGBColor(255, 245, 245)    # #FFF5F5 - Nền đỏ nhạt
BLUE_LIGHT = RGBColor(235, 248, 255)   # #EBF8FF - Nền xanh nhạt nổi bật

def set_text(shape, text, font_size=Pt(13), bold=False, color=CHARCOAL, align=PP_ALIGN.LEFT):
    """Thiết lập văn bản có định dạng chuẩn trong text frame của shape."""
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    tf.text = ""  # clear
    lines = text.split('\n')
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = "Arial"
        p.font.size = font_size
        p.font.bold = bold
        p.font.color.rgb = color
        p.alignment = align

def create_base_slide(prs, chapter, title, footnote="Đồ án Trí tuệ Nhân tạo — Mô hình BERT Phân loại Cảm xúc", logo_blob=None):
    """
    Tạo slide nền sáng chuẩn mực của dự án với header, footer và logo DUT.
    Khắc phục triệt để lỗi nền tối và chữ tối của deck cũ.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    
    # Xóa các placeholder mặc định
    for sp in list(slide.shapes):
        sp_elem = sp._element
        sp_elem.getparent().remove(sp_elem)
        
    # Thiết lập nền slide sáng (#F8FAFC)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_LIGHT
    
    # Header zone:
    # 1. Chapter Subtitle
    hdr_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.73), Inches(0.95))
    tf = hdr_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = chapter.upper()
    p1.font.name = "Arial"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = STEEL
    
    # 2. Main Title
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    
    # 3. Decorative Accent Bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(1.8), Inches(0.04))
    bar.fill.solid()
    bar.fill.fore_color.rgb = STEEL
    bar.line.fill.background()
    
    # Footer zone:
    # 1. Separator Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.73), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_GRAY
    line.line.fill.background()
    
    # 2. Footnote (Left)
    ftr_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(8.5), Inches(0.35))
    tf_f = ftr_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    pf = tf_f.paragraphs[0]
    pf.text = footnote
    pf.font.name = "Arial"
    pf.font.size = Pt(9)
    pf.font.color.rgb = MUTED
    
    # 3. Organization Label (Right)
    org_box = slide.shapes.add_textbox(Inches(9.3), Inches(6.98), Inches(3.23), Inches(0.35))
    tf_o = org_box.text_frame
    tf_o.word_wrap = True
    tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = tf_o.margin_bottom = 0
    po = tf_o.paragraphs[0]
    po.text = "Trường Đại học Bách Khoa – ĐHĐN"
    po.font.name = "Arial"
    po.font.size = Pt(9)
    po.font.bold = True
    po.font.color.rgb = STEEL
    po.alignment = PP_ALIGN.RIGHT
    
    # 4. DUT Logo (nếu có)
    if logo_blob:
        slide.shapes.add_picture(io.BytesIO(logo_blob), Inches(11.3), Inches(0.35), Inches(1.2), Inches(0.6))
        
    sldId = prs.slides._sldIdLst[-1]
    return slide, sldId

def add_card(slide, left, top, width, height, title="", title_bg=NAVY, body_bg=CARD_BG, border_color=BORDER_GRAY):
    """Tạo một thẻ card trực quan có tiêu đề và khung nền tương phản cao."""
    # Khung nền Card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = body_bg
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)
    
    if title:
        # Header bar của card
        title_h = Inches(0.48)
        hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, title_h)
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = title_bg
        hdr.line.fill.background()
        
        tf = hdr.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        # Text frame cho nội dung bên dưới header
        body_box = slide.shapes.add_textbox(left + Inches(0.15), top + title_h + Inches(0.1), width - Inches(0.3), height - title_h - Inches(0.2))
        return body_box
    else:
        body_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        return body_box

def add_kpi_card(slide, left, top, width, height, number_text, label_text, subtext="", num_color=STEEL, bg_color=CARD_BG):
    """Tạo thẻ hiển thị chỉ số lớn (Big Number KPI Card)."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = BORDER_GRAY
    card.line.width = Pt(1.2)
    
    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Number
    p1 = tf.paragraphs[0]
    p1.text = number_text
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = num_color
    p1.alignment = PP_ALIGN.CENTER
    
    # Label
    p2 = tf.add_paragraph()
    p2.text = label_text
    p2.font.name = "Arial"
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.alignment = PP_ALIGN.CENTER
    
    # Subtext
    if subtext:
        p3 = tf.add_paragraph()
        p3.text = subtext
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = CHARCOAL
        p3.alignment = PP_ALIGN.CENTER

def create_presentation(output_path=None):
    """Hàm tạo bài thuyết trình học thuật 13 slides tinh gọn, trực quan, nền sáng."""
    template_path = os.path.join(PROJECT_ROOT, "Template-DUT-Total - Copy (1).pptx")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Không tìm thấy template tại {template_path}")
        
    if output_path is None:
        output_path = os.path.join(PROJECT_ROOT, "presentation", "BERT_Project_Final.pptx")
        
    prs = Presentation(template_path)
    
    # Trích xuất logo DUT từ Slide 4 của template để dùng lại
    logo_blob = None
    try:
        s4_orig = prs.slides[4]
        for sp in s4_orig.shapes:
            if sp.shape_type == 13 and sp.width < Inches(3):  # DUT logo
                logo_blob = sp.image.blob
                break
    except Exception:
        pass
        
    # Lưu lại Slide 0 (Cover) và Slide 14 (Thank You)
    cover_slide = prs.slides[0]
    cover_sldId = prs.slides._sldIdLst[0]
    thankyou_slide = prs.slides[14]
    thankyou_sldId = prs.slides._sldIdLst[14]
    
    # ==========================================================
    # SLIDE 1: Cover (Dark theme từ template)
    # ==========================================================
    set_text(
        cover_slide.shapes[1],
        "NGHIÊN CỨU VÀ ỨNG DỤNG MÔ HÌNH BERT\nCHO BÀI TOÁN PHÂN LOẠI CẢM XÚC ĐÁNH GIÁ KHÁCH SẠN",
        font_size=Pt(24), bold=True, color=WHITE
    )
    set_text(
        cover_slide.shapes[2],
        "Học phần: Trí tuệ Nhân tạo (Artificial Intelligence)\n"
        "Giảng viên hướng dẫn: TS. Huỳnh Hữu Hưng\n"
        "Sinh viên thực hiện: [Họ và tên sinh viên / Nhóm thực hiện]\n"
        "Đơn vị: Trường Đại học Bách Khoa – Đại học Đà Nẵng\n"
        "Tháng 09/2026",
        font_size=Pt(13), bold=False, color=RGBColor(226, 232, 240)
    )
    
    # ==========================================================
    # SLIDE 2: Problem & Objective (Light theme)
    # ==========================================================
    s2, s2_sldId = create_base_slide(prs, "Chương 1: Tổng quan", "BỐI CẢNH BÀI TOÁN & MỤC TIÊU NGHIÊN CỨU", logo_blob=logo_blob)
    
    # Card 1: Problem
    b1 = add_card(s2, Inches(0.8), Inches(1.55), Inches(5.65), Inches(5.0), title="THÁCH THỨC BÀI TOÁN (PROBLEM)", title_bg=STEEL)
    tf1 = b1.text_frame
    tf1.word_wrap = True
    bullets_p = [
        ("Phân loại cảm xúc trực tuyến:", " Nhu cầu tự động hóa phân tích hàng ngàn đánh giá khách sạn để nâng cao chất lượng dịch vụ lưu trú."),
        ("Ngữ cảnh phức tạp:", " Ngôn ngữ đánh giá chứa nhiều câu đa ý, cảm xúc hỗn hợp (mixed sentiment) và cấu trúc phủ định tinh vi."),
        ("Hạn chế mô hình cũ:", " Mô hình truyền thống (BoW/TF-IDF) bỏ qua trật tự từ; mô hình tuần tự (RNN/LSTM) gặp điểm nghẽn tính toán và suy giảm ngữ cảnh xa.")
    ]
    for i, (bld, txt) in enumerate(bullets_p):
        p = tf1.paragraphs[0] if i == 0 else tf1.add_paragraph()
        p.space_after = Pt(14)
        run1 = p.add_run(); run1.text = "• " + bld; run1.font.bold = True; run1.font.size = Pt(13); run1.font.color.rgb = NAVY
        run2 = p.add_run(); run2.text = txt; run2.font.bold = False; run2.font.size = Pt(13); run2.font.color.rgb = CHARCOAL
        
    # Card 2: Objective
    b2 = add_card(s2, Inches(6.85), Inches(1.55), Inches(5.65), Inches(5.0), title="MỤC TIÊU & ĐÓNG GÓP (OBJECTIVE)", title_bg=NAVY)
    tf2 = b2.text_frame
    tf2.word_wrap = True
    bullets_o = [
        ("Quy trình chuẩn mực khép kín:", " Triển khai đầy đủ 6 giai đoạn AI Project Cycle; kiểm toán exact-match trước split và case-normalized hậu nghiệm."),
        ("Thực nghiệm đối chứng công bằng:", " Huấn luyện mô hình cơ sở TF-IDF + Logistic Regression và Fine-tuning BERT (bert-base-uncased) trên cùng dữ liệu chuẩn."),
        ("Đánh giá khách quan & Triển khai:", " Đóng băng và kiểm thử trên Held-Out Test Set (3,949 mẫu); phân tích định tính ca lỗi và đóng gói Web UI Streamlit.")
    ]
    for i, (bld, txt) in enumerate(bullets_o):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.space_after = Pt(14)
        run1 = p.add_run(); run1.text = "• " + bld; run1.font.bold = True; run1.font.size = Pt(13); run1.font.color.rgb = NAVY
        run2 = p.add_run(); run2.text = txt; run2.font.bold = False; run2.font.size = Pt(13); run2.font.color.rgb = CHARCOAL
        
    # ==========================================================
    # SLIDE 3: Methodology / AI Project Cycle (Light theme)
    # ==========================================================
    s3, s3_sldId = create_base_slide(prs, "Chương 2: Phương pháp luận", "QUY TRÌNH NGHIÊN CỨU CHUẨN MỰC (AI PROJECT CYCLE)", logo_blob=logo_blob)
    
    # 7 Process Steps
    steps = [
        ("01", "Data Audit", "Loại bỏ 255 mẫu\nlỗi & trùng lặp"),
        ("02", "Token EDA", "Phân tích độ dài,\nchọn MAX_LEN=128"),
        ("03", "Data Split", "Stratified 70/10/20\nvới seed 42 cố định"),
        ("04", "Baseline", "TF-IDF (10k feats)\n+ Logistic Regr"),
        ("05", "BERT Train", "Full fine-tuning,\nchọn checkpoint F1"),
        ("06", "Frozen Test", "Đánh giá 1 lần duy nhất\ntrên 3,949 mẫu"),
        ("07", "Error & Demo", "Kiểm toán 20 ca lỗi;\nWeb UI Streamlit")
    ]
    
    step_w = Inches(1.52)
    step_gap = Inches(0.18)
    start_x = Inches(0.8)
    
    for i, (num, title_s, desc_s) in enumerate(steps):
        cur_x = start_x + i * (step_w + step_gap)
        # Card step
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cur_x, Inches(1.8), step_w, Inches(3.6))
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE
        c.line.color.rgb = STEEL if i in [3, 4, 5] else BORDER_GRAY
        c.line.width = Pt(1.5 if i in [3, 4, 5] else 1.0)
        
        # Number badge
        badge = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cur_x, Inches(1.8), step_w, Inches(0.65))
        badge.fill.solid()
        badge.fill.fore_color.rgb = NAVY if i in [3, 4, 5] else STEEL
        badge.line.fill.background()
        tf_b = badge.text_frame
        p = tf_b.paragraphs[0]
        p.text = num
        p.font.name = "Arial"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
        
        # Text box in card
        tb = s3.shapes.add_textbox(cur_x + Inches(0.08), Inches(2.55), step_w - Inches(0.16), Inches(2.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_s
        p1.font.name = "Arial"; p1.font.size = Pt(12); p1.font.bold = True; p1.font.color.rgb = NAVY
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = desc_s
        p2.font.name = "Arial"; p2.font.size = Pt(10); p2.font.color.rgb = CHARCOAL
        p2.alignment = PP_ALIGN.CENTER
        
    # Callout bottom
    callout = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.73), Inches(0.95))
    callout.fill.solid(); callout.fill.fore_color.rgb = BLUE_LIGHT
    callout.line.color.rgb = STEEL; callout.line.width = Pt(1.2)
    set_text(
        callout,
        "Nguyên tắc cốt lõi: Xây dựng độc lập từ đầu (from scratch) • Kiểm soát giao thoa dữ liệu • "
        "Đóng băng siêu tham số trước khi mở niêm phong tập kiểm thử (Held-Out Test Set).",
        font_size=Pt(12), bold=True, color=NAVY, align=PP_ALIGN.CENTER
    )
    
    # ==========================================================
    # SLIDE 4: Dataset & Data Audit (Light theme)
    # ==========================================================
    s4, s4_sldId = create_base_slide(prs, "Chương 2: Dữ liệu & Phương pháp", "TẬP DỮ LIỆU & KẾT QUẢ KIỂM TOÁN CHỐNG RÒ RỈ", logo_blob=logo_blob)
    
    add_kpi_card(
        s4, Inches(0.8), Inches(1.6), Inches(5.65), Inches(2.2),
        "20,000", "MẪU DỮ LIỆU THÔ BAN ĐẦU",
        "Tập dữ liệu đánh giá khách sạn tiếng Anh do GV cung cấp;\nchứa các định dạng đặc thù ('No Negative', 'No Positive').",
        num_color=NAVY
    )
    add_kpi_card(
        s4, Inches(6.85), Inches(1.6), Inches(5.65), Inches(2.2),
        "255", "MẪU LỖI ĐÃ LOẠI BỎ (DATA AUDIT)",
        "Loại bỏ 5 mẫu rỗng, 127 mẫu nhãn xung đột (từ 20 văn bản)\nvà 123 mẫu trùng lặp tuyệt đối trước khi phân chia.",
        num_color=RED, bg_color=RED_LIGHT
    )
    add_kpi_card(
        s4, Inches(0.8), Inches(4.1), Inches(5.65), Inches(2.3),
        "19,745", "TẬP DỮ LIỆU SẠCH DUY NHẤT",
        "Cân bằng lớp lý tưởng: 9,921 Tiêu cực (50.25%) và 9,824 Tích cực (49.75%).\nBảo đảm tính đại diện khách quan cho bài toán.",
        num_color=GREEN, bg_color=GREEN_LIGHT
    )
    add_kpi_card(
        s4, Inches(6.85), Inches(4.1), Inches(5.65), Inches(2.3),
        "70% / 10% / 20%", "STRATIFIED SPLIT (SEED 42)",
        "Train: 13,821 | Validation: 1,975 | Test: 3,949\nExact overlap: 0; post-hoc casefold audit: 3 / 10 / 2 cặp.",
        num_color=STEEL
    )
    
    # ==========================================================
    # SLIDE 5: EDA & MAX_LENGTH Decision (Light theme)
    # ==========================================================
    s5, s5_sldId = create_base_slide(prs, "Chương 2: Dữ liệu & Phương pháp", "PHÂN BỐ ĐỘ DÀI TOKEN & QUYẾT ĐỊNH MAX_LENGTH", logo_blob=logo_blob)
    
    # Chart image (Left)
    token_fig = os.path.join(FIGURES_DIR, "token_length_distribution.png")
    if os.path.exists(token_fig):
        s5.shapes.add_picture(token_fig, Inches(0.8), Inches(1.6), Inches(5.7), Inches(4.7))
        
    # Callout Cards (Right)
    add_kpi_card(
        s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(1.45),
        "p95 = 121 | p99 = 168", "PHÂN VỊ ĐỘ DÀI TOKEN BERT",
        "Trung vị: 30 tokens | Trung bình: 42.33 tokens. Đại đa số đánh giá có độ dài ngắn và súc tích.",
        num_color=NAVY
    )
    add_kpi_card(
        s5, Inches(6.8), Inches(3.2), Inches(5.7), Inches(1.45),
        "Tỷ lệ > 128: chỉ 3.93%", "ĐỘ BAO PHỦ NGỮ CẢNH",
        "Trong Train + Validation, 3.93% văn bản (620 mẫu) vượt 128 tokens; 96.07% không vượt ngưỡng.",
        num_color=STEEL
    )
    
    dec_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.8), Inches(5.7), Inches(1.5))
    dec_card.fill.solid(); dec_card.fill.fore_color.rgb = GREEN_LIGHT
    dec_card.line.color.rgb = GREEN; dec_card.line.width = Pt(1.5)
    set_text(
        dec_card,
        "QUYẾT ĐỊNH CẤU HÌNH: MAX_LENGTH = 128\n"
        "• Giảm 4x kích thước ma trận Attention O(L^2) và bộ nhớ kích hoạt so với ngưỡng 256.\n"
        "• Cân đối tối ưu giữa việc giữ trọn vẹn ngữ cảnh và khả năng huấn luyện ổn định trên CPU.",
        font_size=Pt(11), bold=False, color=CHARCOAL
    )
    
    # ==========================================================
    # SLIDE 6: Baseline vs BERT Setup (Light theme)
    # ==========================================================
    s6, s6_sldId = create_base_slide(prs, "Chương 2: Dữ liệu & Phương pháp", "THIẾT LẬP THỰC NGHIỆM ĐỐI CHỨNG: BASELINE VS BERT", logo_blob=logo_blob)
    
    # Left Card: Baseline
    c_base = add_card(s6, Inches(0.8), Inches(1.55), Inches(5.65), Inches(5.0), title="MÔ HÌNH CƠ SỞ (BASELINE)", title_bg=STEEL)
    tf_b = c_base.text_frame
    tf_b.word_wrap = True
    bullets_base = [
        ("Đặc trưng:", " TF-IDF (Unigrams + Bigrams), từ điển max_features = 10,000."),
        ("Biến đổi tần suất:", " sublinear_tf = True (1 + log(tf)) hạn chế ảnh hưởng của từ xuất hiện quá nhiều."),
        ("Bộ phân loại:", " Logistic Regression với chuẩn hóa L2 (Ridge), C = 1.0, solver lbfgs."),
        ("Vai trò phương pháp:", " Tạo mốc đối chứng chuẩn mực theo nguyên tắc 'Start simple to complex models'."),
        ("Đặc tính vận hành:", " Huấn luyện cực nhanh (0.68s), suy luận ~28,700 mẫu/giây trên CPU.")
    ]
    for i, (bld, txt) in enumerate(bullets_base):
        p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = txt; r2.font.bold = False; r2.font.size = Pt(12); r2.font.color.rgb = CHARCOAL
        
    # Right Card: BERT
    c_bert = add_card(s6, Inches(6.85), Inches(1.55), Inches(5.65), Inches(5.0), title="MÔ HÌNH CHÍNH (FINE-TUNED BERT)", title_bg=NAVY)
    tf_bt = c_bert.text_frame
    tf_bt.word_wrap = True
    bullets_bert = [
        ("Mô hình gốc:", " google-bert/bert-base-uncased (110M tham số, 12 layers, 12 heads)."),
        ("Cơ chế huấn luyện:", " Full Fine-Tuning toàn bộ 110M tham số của Transformer Encoder."),
        ("Siêu tham số tối ưu:", " AdamW, lr = 2e-5, warmup ratio = 0.1, weight decay = 0.01."),
        ("Batch size & Epoch:", " Batch size = 16, số epoch = 3 (2,592 steps), MAX_LENGTH = 128."),
        ("Tiêu chí Checkpoint:", " Tự động lưu checkpoint có Validation Macro F1 cao nhất (Epoch 3).")
    ]
    for i, (bld, txt) in enumerate(bullets_bert):
        p = tf_bt.paragraphs[0] if i == 0 else tf_bt.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = txt; r2.font.bold = False; r2.font.size = Pt(12); r2.font.color.rgb = CHARCOAL
        
    # ==========================================================
    # SLIDE 7: BERT Training Dynamics & Checkpoint (Light theme)
    # ==========================================================
    s7, s7_sldId = create_base_slide(prs, "Chương 3: Kết quả thực nghiệm", "QUÁ TRÌNH HUẤN LUYỆN BERT & ĐỘNG LỰC HỌC TẬP", logo_blob=logo_blob)
    
    # Training History Chart (Left)
    train_fig = os.path.join(FIGURES_DIR, "training_history.png")
    if os.path.exists(train_fig):
        s7.shapes.add_picture(train_fig, Inches(0.8), Inches(1.6), Inches(5.7), Inches(4.7))
        
    # Summary Cards (Right)
    b_dyn = add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.6), title="TIẾN TRÌNH 3 EPOCHS TRÊN CPU", title_bg=STEEL)
    tf_d = b_dyn.text_frame
    tf_d.word_wrap = True
    bullets_dyn = [
        "Môi trường: PyTorch CPU (2.14.0+cpu) | Tổng thời gian: ~4.34 giờ (15,617s)",
        "Epoch 1: Train Loss (step avg) = 0.4385 | Val Acc = 83.14% | Val F1 = 0.8310",
        "Epoch 2: Train Loss (step avg) = 0.2877 | Val Acc = 83.90% | Val F1 = 0.8387",
        "Epoch 3: Train Loss (step avg) = 0.2022 | Val Acc = 83.90% | Val F1 = 0.8389 (Đỉnh)",
        "Trainer aggregate training loss toàn bộ quá trình: 0.3071"
    ]
    for i, b_txt in enumerate(bullets_dyn):
        p = tf_d.paragraphs[0] if i == 0 else tf_d.add_paragraph()
        p.space_after = Pt(4)
        p.text = "• " + b_txt
        p.font.name = "Arial"; p.font.size = Pt(11); p.font.color.rgb = CHARCOAL
        if "Đỉnh" in b_txt:
            p.font.bold = True
            p.font.color.rgb = GREEN
            
    b_chk = add_card(s7, Inches(6.8), Inches(4.35), Inches(5.7), Inches(2.0), title="LỰA CHỌN CHECKPOINT & GIẢI THÍCH LOSS", title_bg=NAVY)
    tf_c = b_chk.text_frame
    tf_c.word_wrap = True
    bullets_chk = [
        "Checkpoint được chọn: checkpoint-2592 (cuối Epoch 3, đạt đỉnh Validation Macro F1 = 83.89%).",
        "Hiện tượng Val Loss: Cross-entropy (-log p) phạt nặng độ tự tin ở một số ít mẫu biên mơ hồ khiến loss tăng nhẹ, trong khi phân loại nhãn cứng vẫn đạt hiệu năng đỉnh cao nhất."
    ]
    for i, b_txt in enumerate(bullets_chk):
        p = tf_c.paragraphs[0] if i == 0 else tf_c.add_paragraph()
        p.space_after = Pt(6)
        p.text = "• " + b_txt
        p.font.name = "Arial"; p.font.size = Pt(11); p.font.color.rgb = CHARCOAL
        
    # ==========================================================
    # SLIDE 8: Final Test Results (Light theme - MAIN RESULT SLIDE!)
    # ==========================================================
    s8, s8_sldId = create_base_slide(
        prs, "Chương 3: Kết quả thực nghiệm", "KẾT QUẢ SO SÁNH ĐỐI ĐẦU TRÊN HELD-OUT TEST SET (3,949 MẪU)",
        footnote="Đánh giá độc lập trên tập Held-Out Test Set 3,949 mẫu sau khi đóng băng hoàn toàn tham số mô hình.",
        logo_blob=logo_blob
    )
    
    # 3 Main KPI Cards
    # Card 1: Baseline
    c1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(3.65), Inches(3.7))
    c1.fill.solid(); c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = BORDER_GRAY; c1.line.width = Pt(1.5)
    
    h1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(3.65), Inches(0.55))
    h1.fill.solid(); h1.fill.fore_color.rgb = STEEL; h1.line.fill.background()
    set_text(h1, "BASELINE (TF-IDF + LR)", font_size=Pt(13), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    tb1 = s8.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(3.45), Inches(2.9))
    tf1 = tb1.text_frame; tf1.word_wrap = True
    set_text(
        tb1,
        "Accuracy:\n81.94%\n\n"
        "Macro F1-Score:\n0.8192\n\n"
        "Macro P / R: 0.8208 / 0.8193\n"
        "Tốc độ: 28,784 mẫu/giây (0.137s)",
        font_size=Pt(12), color=CHARCOAL, align=PP_ALIGN.CENTER
    )
    # Format numbers inside tb1
    tf1.paragraphs[1].font.size = Pt(26); tf1.paragraphs[1].font.bold = True; tf1.paragraphs[1].font.color.rgb = NAVY
    tf1.paragraphs[3].font.size = Pt(22); tf1.paragraphs[3].font.bold = True; tf1.paragraphs[3].font.color.rgb = STEEL
    
    # Card 2: BERT
    c2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.55), Inches(3.65), Inches(3.7))
    c2.fill.solid(); c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = GREEN; c2.line.width = Pt(2.0)
    
    h2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.55), Inches(3.65), Inches(0.55))
    h2.fill.solid(); h2.fill.fore_color.rgb = NAVY; h2.line.fill.background()
    set_text(h2, "FINE-TUNED BERT (CHÍNH)", font_size=Pt(13), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    tb2 = s8.shapes.add_textbox(Inches(4.9), Inches(2.2), Inches(3.45), Inches(2.9))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    set_text(
        tb2,
        "Accuracy:\n84.83%\n\n"
        "Macro F1-Score:\n0.8483\n\n"
        "Macro P / R: 0.8486 / 0.8482\n"
        "Tốc độ: 12.85 mẫu/giây (307.3s)",
        font_size=Pt(12), color=CHARCOAL, align=PP_ALIGN.CENTER
    )
    tf2.paragraphs[1].font.size = Pt(26); tf2.paragraphs[1].font.bold = True; tf2.paragraphs[1].font.color.rgb = GREEN
    tf2.paragraphs[3].font.size = Pt(22); tf2.paragraphs[3].font.bold = True; tf2.paragraphs[3].font.color.rgb = GREEN
    
    # Card 3: Delta
    c3 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.55), Inches(3.73), Inches(3.7))
    c3.fill.solid(); c3.fill.fore_color.rgb = GREEN_LIGHT
    c3.line.color.rgb = GREEN; c3.line.width = Pt(1.5)
    
    h3 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.55), Inches(3.73), Inches(0.55))
    h3.fill.solid(); h3.fill.fore_color.rgb = GREEN; h3.line.fill.background()
    set_text(h3, "MỨC CẢI THIỆN ĐỐI CHỨNG (Δ)", font_size=Pt(13), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    
    tb3 = s8.shapes.add_textbox(Inches(8.9), Inches(2.2), Inches(3.53), Inches(2.9))
    tf3 = tb3.text_frame; tf3.word_wrap = True
    set_text(
        tb3,
        "Accuracy Cải Thiện:\n+2.89 percentage points\n\n"
        "Macro F1 Cải Thiện:\n+0.0291 (+2.91%)\n\n"
        "Giảm 114 ca dự đoán sai (-16.0%)\n"
        "Đánh đổi: Thời gian suy luận lớn hơn",
        font_size=Pt(12), color=CHARCOAL, align=PP_ALIGN.CENTER
    )
    tf3.paragraphs[1].font.size = Pt(20); tf3.paragraphs[1].font.bold = True; tf3.paragraphs[1].font.color.rgb = GREEN
    tf3.paragraphs[3].font.size = Pt(20); tf3.paragraphs[3].font.bold = True; tf3.paragraphs[3].font.color.rgb = GREEN
    
    # Bottom Banner
    banner = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.45), Inches(11.73), Inches(1.2))
    banner.fill.solid(); banner.fill.fore_color.rgb = BLUE_LIGHT
    banner.line.color.rgb = STEEL; banner.line.width = Pt(1.2)
    set_text(
        banner,
        "• Minh chứng khoa học thực chất: BERT vượt trội Baseline toàn diện trên cả 5 chỉ số phân loại (+2.89 percentage points Accuracy, +0.0291 Macro F1).\n"
        "• Tính nhất quán giữa các tập: Chỉ số Validation Macro F1 (83.89%) và Test Macro F1 (84.83%) sát nhau, nhất quán với hiệu năng quan sát được trên cả hai tập held-out (Validation and Test metrics are close, consistent with similar observed performance across the two held-out splits).\n"
        "• Đánh đổi kỹ thuật: Nâng cao độ chính xác và giảm 114 ca lỗi (-16.0%) đi kèm chi phí tính toán và độ trễ suy luận lớn hơn trên CPU (12.85 mẫu/s vs 28,784 mẫu/s).",
        font_size=Pt(11), bold=False, color=NAVY
    )
    
    # ==========================================================
    # SLIDE 9: Confusion Matrix Comparison (Light theme)
    # ==========================================================
    s9, s9_sldId = create_base_slide(prs, "Chương 3: Kết quả thực nghiệm", "SO SÁNH MA TRẬN NHẦM LẪN TRÊN TẬP TEST (3,949 MẪU)", logo_blob=logo_blob)
    
    base_cm = BASELINE_TEST_CM_PATH
    bert_cm = BERT_TEST_CM_PATH
    if os.path.exists(base_cm):
        s9.shapes.add_picture(base_cm, Inches(0.8), Inches(1.55), Inches(5.65), Inches(3.5))
    if os.path.exists(bert_cm):
        s9.shapes.add_picture(bert_cm, Inches(6.85), Inches(1.55), Inches(5.65), Inches(3.5))
        
    lbl1 = s9.shapes.add_textbox(Inches(0.8), Inches(5.15), Inches(5.65), Inches(0.35))
    set_text(lbl1, "Baseline: TN=1,691 | FP=293 | FN=420 | TP=1,545 (Tổng lỗi: 713 ca / 18.06%)", font_size=Pt(10), bold=True, color=STEEL, align=PP_ALIGN.CENTER)
    
    lbl2 = s9.shapes.add_textbox(Inches(6.85), Inches(5.15), Inches(5.65), Inches(0.35))
    set_text(lbl2, "BERT: TN=1,711 | FP=273 | FN=326 | TP=1,639 (Tổng lỗi: 599 ca / 15.17%)", font_size=Pt(10), bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    
    # 2 Takeaway Cards
    t1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.6), Inches(5.65), Inches(1.1))
    t1.fill.solid(); t1.fill.fore_color.rgb = WHITE; t1.line.color.rgb = GREEN; t1.line.width = Pt(1.2)
    set_text(
        t1,
        "GIẢM MẠNH FALSE NEGATIVES (BỎ SÓT TÍCH CỰC):\n"
        "BERT giảm 94 ca FN (từ 420 xuống 326 ca, giảm 22.38%), nhận diện chính xác thêm 94 đánh giá tích cực so với Baseline.",
        font_size=Pt(11), bold=False, color=CHARCOAL
    )
    t1.text_frame.paragraphs[0].font.bold = True; t1.text_frame.paragraphs[0].font.color.rgb = GREEN
    
    t2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(5.6), Inches(5.65), Inches(1.1))
    t2.fill.solid(); t2.fill.fore_color.rgb = WHITE; t2.line.color.rgb = STEEL; t2.line.width = Pt(1.2)
    set_text(
        t2,
        "GIẢM ĐỒNG THỜI CẢ FP VÀ FN TRÊN TOÀN BỘ TẬP TEST:\n"
        "BERT giảm 20 ca FP và 94 ca FN (tổng giảm 114 ca lỗi, -16.0%), cải thiện đồng bộ cả Precision (+2.78%) và Recall (+2.89%).",
        font_size=Pt(11), bold=False, color=CHARCOAL
    )
    t2.text_frame.paragraphs[0].font.bold = True; t2.text_frame.paragraphs[0].font.color.rgb = STEEL
    
    # ==========================================================
    # SLIDE 10: Qualitative Error Analysis (Light theme)
    # ==========================================================
    s10, s10_sldId = create_base_slide(
        prs, "Chương 3: Kết quả thực nghiệm", "PHÂN TÍCH LỖI ĐỊNH TÍNH TRÊN MẪU 20 CA TỰ TIN NHẤT",
        footnote="* Thống kê chỉ áp dụng trong phạm vi 20 ca lỗi có độ tự tin cao nhất được kiểm toán (within the 20 selected highest-confidence errors), không suy rộng cho toàn bộ 599 ca lỗi của BERT.",
        logo_blob=logo_blob
    )
    
    # 4 Cards (2x2 Grid)
    cards_data = [
        (Inches(0.8), Inches(1.55), "01. CẢM XÚC HỖN HỢP (MIXED SENTIMENT) — 15/20 CA", STEEL,
         "• 15/20 mẫu kiểm toán chứa đồng thời mệnh đề khen và chê (ví dụ: 'phòng rộng nhưng phục vụ tệ').\n"
         "• Nhãn nhị phân đơn lẻ (0 hoặc 1) gặp khó khăn khi đại diện đầy đủ văn bản đa chiều cảm xúc."),
        (Inches(6.85), Inches(1.55), "02. MƠ HỒ NHÃN / KHẢ NĂNG NHIỄU NHÃN (POSSIBLE LABEL AMBIGUITY / NOISE) — 8/20 CA", NAVY,
         "• 8/20 mẫu bộc lộ mâu thuẫn rõ rệt giữa nhãn ground-truth và ngữ nghĩa bề mặt văn bản.\n"
         "• Dự đoán của mô hình thể hiện sự nhất quán với ngữ nghĩa bài viết hơn là nhãn được gán trong dữ liệu."),
        (Inches(0.8), Inches(4.15), "03. PHỦ ĐỊNH / NHƯỢNG BỘ & TEMPLATE MARKERS — 8 & 6 CA", NAVY,
         "• 8/20 ca chứa cấu trúc phủ định hoặc nhượng bộ ('not bad', 'didn't like').\n"
         "• 6/20 ca mang dấu vết biểu mẫu ghép chuỗi đặc thù ('No Positive', 'No Negative', 'nothing')."),
        (Inches(6.85), Inches(4.15), "04. KIỂM TOÁN CẮT CỤT CHUỖI (TRUNCATION AUDIT) — 0/20 CA", GREEN,
         "• 0/20 selected highest-confidence error cases exceeded MAX_LENGTH=128 (độ dài thực tế 6–126 tokens).\n"
         "• Quan sát này chỉ áp dụng cho 20 ca được kiểm toán, không suy rộng cho toàn bộ lỗi.")
    ]
    
    for l, t, title_c, hdr_c, body_c in cards_data:
        box = add_card(s10, l, t, Inches(5.65), Inches(2.35), title=title_c, title_bg=hdr_c)
        set_text(box, body_c, font_size=Pt(11), color=CHARCOAL)
        
    # ==========================================================
    # SLIDE 11: Real-Time Streamlit Demo (Light theme)
    # ==========================================================
    s11, s11_sldId = create_base_slide(prs, "Chương 4: Đóng gói & Triển khai", "ỨNG DỤNG TƯƠNG TÁC THỜI GIAN THỰC (STREAMLIT DEMO)", logo_blob=logo_blob)
    
    # Left: Mockup UI Card
    mock = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(6.2), Inches(5.0))
    mock.fill.solid(); mock.fill.fore_color.rgb = WHITE
    mock.line.color.rgb = STEEL; mock.line.width = Pt(1.5)
    
    mock_hdr = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(6.2), Inches(0.48))
    mock_hdr.fill.solid(); mock_hdr.fill.fore_color.rgb = NAVY; mock_hdr.line.fill.background()
    set_text(mock_hdr, "GIAO DIỆN ỨNG DỤNG WEB (STREAMLIT UI — app/app.py)", font_size=Pt(12), bold=True, color=WHITE)
    
    mock_tb = s11.shapes.add_textbox(Inches(0.95), Inches(2.15), Inches(5.9), Inches(4.2))
    set_text(
        mock_tb,
        "Ví dụ minh họa giao diện (không phải benchmark đóng băng):\n"
        "\"The room was a bit small, but the location was great and breakfast was delicious!\"\n\n"
        "Ứng dụng hiển thị khi chạy:\n"
        "• Nhãn dự đoán và độ tin cậy của BERT cùng Baseline.\n"
        "• Danh sách token WordPiece của văn bản đầu vào.\n"
        "• Độ trễ suy luận đo trực tiếp, phụ thuộc phần cứng và môi trường.",
        font_size=Pt(11), color=CHARCOAL
    )
    # Format runs
    tf_m = mock_tb.text_frame
    tf_m.paragraphs[0].font.bold = True; tf_m.paragraphs[0].font.color.rgb = NAVY
    tf_m.paragraphs[1].font.italic = True
    tf_m.paragraphs[2].font.bold = True; tf_m.paragraphs[2].font.color.rgb = STEEL
    tf_m.paragraphs[3].font.color.rgb = GREEN; tf_m.paragraphs[3].font.bold = True
    tf_m.paragraphs[4].font.color.rgb = RED
    tf_m.paragraphs[5].font.bold = True; tf_m.paragraphs[5].font.color.rgb = NAVY
    tf_m.paragraphs[6].font.name = "Courier New"; tf_m.paragraphs[6].font.size = Pt(9.5)
    
    # Right: 3 Feature Cards
    f_cards = [
        ("TRIỂN KHAI CỤC BỘ KHÉP KÍN",
         "• Nạp tự động trọng số đã đóng băng từ artifacts/model/bert_best_model/.\n"
         "• Đo lường và hiển thị độ trễ suy luận thời gian thực (Inference Latency ms)."),
        ("SO SÁNH ĐỐI ĐẦU SONG SONG",
         "• Cho phép thử nghiệm trực tiếp khả năng nắm bắt ngữ cảnh câu giữa TF-IDF và Transformer trên cùng một văn bản đầu vào."),
        ("TRỰC QUAN HÓA CƠ CHẾ BERT",
         "• Hiển thị danh sách token WordPiece (##), minh họa trực quan cơ chế tách từ và biểu diễn vector cho người sử dụng.")
    ]
    for idx, (f_title, f_body) in enumerate(f_cards):
        top_pos = Inches(1.55) + idx * Inches(1.7)
        c_box = add_card(s11, Inches(7.3), top_pos, Inches(5.2), Inches(1.55), title=f_title, title_bg=STEEL if idx > 0 else NAVY)
        set_text(c_box, f_body, font_size=Pt(11), color=CHARCOAL)
        
    # ==========================================================
    # SLIDE 12: Limitations & Future Work (Light theme)
    # ==========================================================
    s12, s12_sldId = create_base_slide(prs, "Chương 4: Kết luận & Đánh giá", "HẠN CHẾ CỦA NGHIÊN CỨU & HƯỚNG PHÁT TRIỂN (LIMITATIONS & FUTURE WORK)", logo_blob=logo_blob)
    
    # Left Card: Limitations
    box_lim = add_card(s12, Inches(0.8), Inches(1.55), Inches(5.65), Inches(4.15), title="HẠN CHẾ HIỆN TẠI (LIMITATIONS)", title_bg=STEEL)
    tf_l = box_lim.text_frame
    tf_l.word_wrap = True
    bullets_lim = [
        ("Phân loại nhị phân (Binary sentiment only):", " Hiện tại chỉ phân loại 2 lớp (Tích cực / Tiêu cực), chưa xử lý lớp trung lập (3 sao / Neutral) hoặc cảm xúc nhiều mức độ."),
        ("Phạm vi kiểm toán lỗi (Selected qualitative analysis):", " Chỉ tập trung kiểm toán 20 ca lỗi có độ tự tin cao nhất (highest-confidence errors), không suy rộng cho toàn bộ 599 ca lỗi của BERT."),
        ("Chi phí suy luận trên CPU (BERT CPU inference cost):", " Tốc độ ~12.85 mẫu/s (307.3s cho 3,949 mẫu) chậm hơn nhiều so với mô hình cơ sở (~28,784 mẫu/s) khi triển khai thực tế."),
        ("Cắt cụt độ dài token (Sequence truncation):", " 3.93% văn bản trong tập Train + Validation (620 mẫu) vượt quá ngưỡng MAX_LENGTH=128.")
    ]
    for i, (bld, txt) in enumerate(bullets_lim):
        p = tf_l.paragraphs[0] if i == 0 else tf_l.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = txt; r2.font.bold = False; r2.font.size = Pt(11); r2.font.color.rgb = CHARCOAL
        
    # Right Card: Future Work
    box_fut = add_card(s12, Inches(6.85), Inches(1.55), Inches(5.65), Inches(4.15), title="HƯỚNG PHÁT TRIỂN TƯƠNG LAI (FUTURE WORK)", title_bg=NAVY)
    tf_f = box_fut.text_frame
    tf_f.word_wrap = True
    bullets_fut = [
        ("Phân tích cảm xúc theo khía cạnh (ABSA):", " Nhận diện cụ thể cảm xúc khách hàng theo từng thực thể dịch vụ (vị trí, phòng ốc, vệ sinh, giá cả, phục vụ)."),
        ("Tối ưu hóa & nén mô hình (Efficient/distilled models):", " Triển khai các mô hình nhỏ gọn hơn (DistilBERT, TinyBERT) hoặc lượng tử hóa kết hợp ONNX Runtime / TensorRT để tăng tốc độ suy luận."),
        ("Mở rộng đa ngữ & Tiếng Việt (Vietnamese / multilingual extension):", " Huấn luyện và đánh giá trên các mô hình tiếng Việt chuyên biệt (PhoBERT, ViBERT) hoặc đa ngữ (mBERT, XLM-RoBERTa).")
    ]
    for i, (bld, txt) in enumerate(bullets_fut):
        p = tf_f.paragraphs[0] if i == 0 else tf_f.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run(); r1.text = "• " + bld; r1.font.bold = True; r1.font.size = Pt(11.5); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = txt; r2.font.bold = False; r2.font.size = Pt(11.5); r2.font.color.rgb = CHARCOAL
        
    # Bottom Banner: 3 Core Takeaways
    ban_tak = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.85), Inches(11.73), Inches(0.85))
    ban_tak.fill.solid(); ban_tak.fill.fore_color.rgb = BLUE_LIGHT
    ban_tak.line.color.rgb = STEEL; ban_tak.line.width = Pt(1.2)
    set_text(
        ban_tak,
        "3 KẾT LUẬN CỐT LÕI: (1) Kiểm soát và báo cáo minh bạch giao thoa dữ liệu • (2) BERT vượt Baseline +2.89 percentage points Acc, +0.0291 Macro F1 • (3) Mẫu lỗi thường liên quan cảm xúc pha trộn và khả năng mơ hồ nhãn.",
        font_size=Pt(11), bold=True, color=NAVY, align=PP_ALIGN.CENTER
    )
    
    # ==========================================================
    # SLIDE 13: Conclusion & Q&A (Dark theme từ template Slide 14)
    # ==========================================================
    set_text(thankyou_slide.shapes[0], "TRÂN TRỌNG CẢM ƠN!", font_size=Pt(36), bold=True, color=WHITE)
    
    qa_box = thankyou_slide.shapes.add_textbox(Inches(5.8), Inches(1.8), Inches(7.0), Inches(4.2))
    set_text(
        qa_box,
        "ĐỀ TÀI: NGHIÊN CỨU VÀ ỨNG DỤNG MÔ HÌNH BERT\n"
        "CHO BÀI TOÁN PHÂN LOẠI CẢM XÚC ĐÁNH GIÁ KHÁCH SẠN\n\n"
        "Học phần: Trí tuệ Nhân tạo (Artificial Intelligence)\n"
        "Giảng viên hướng dẫn: TS. Huỳnh Hữu Hưng\n"
        "Sinh viên thực hiện: [Họ và tên sinh viên / Nhóm thực hiện]\n"
        "Đơn vị: Trường Đại học Bách Khoa – Đại học Đà Nẵng\n\n"
        "XIN KÍNH MỜI QUÝ THẦY CÔ VÀ HỘI ĐỒNG ĐẶT CÂU HỎI!\n(PHIÊN HỎI & ĐÁP — Q&A)",
        font_size=Pt(13.5), bold=True, color=WHITE
    )
    
    # ==========================================================
    # LƯU VÀ TÁI CẤU TRÚC DANH SÁCH SLIDE (13 SLIDES)
    # ==========================================================
    # Danh sách thứ tự: cover, s2..s12, thankyou
    desired_sldIds = [
        cover_sldId, s2_sldId, s3_sldId, s4_sldId, s5_sldId,
        s6_sldId, s7_sldId, s8_sldId, s9_sldId, s10_sldId,
        s11_sldId, s12_sldId, thankyou_sldId
    ]
    
    sldIdLst = prs.slides._sldIdLst
    desired_ids = {elem.id for elem in desired_sldIds}
    for elem in list(sldIdLst):
        if elem.id not in desired_ids:
            prs.part.drop_rel(elem.rId)
            sldIdLst.remove(elem)
    for elem in list(sldIdLst):
        sldIdLst.remove(elem)
    for elem in desired_sldIds:
        sldIdLst.append(elem)
        
    prs.save(output_path)
    print(f" Đã tạo thành công bài thuyết trình REDESIGNED 13 slides tại: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo PowerPoint theo DUT-style template supplied for this project")
    parser.add_argument("--output", type=str, default=None, help="Đường dẫn file pptx đầu ra")
    args = parser.parse_args()
    
    create_presentation(output_path=args.output)
