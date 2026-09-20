"""
app.py - Giao diện Web tương tác phân loại cảm xúc đánh giá khách sạn bằng Streamlit.
Phục vụ thuyết trình & kiểm thử trực tiếp trước Hội đồng Giảng viên.
Cách chạy: streamlit run app/app.py
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Thiết lập đường dẫn import
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from src.predict import predict_baseline, predict_bert

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="BERT Hotel Review Sentiment Analysis",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header & Tiêu đề
st.title("🏨 Phân Loại Cảm Xúc Đánh Giá Khách Sạn")
st.markdown("""
**Đồ Án Môn Học:** Trí Tuệ Nhân Tạo (Artificial Intelligence)  
**Mô hình cốt lõi:** `google-bert/bert-base-uncased` (Fine-tuned) | **Baseline:** TF-IDF + Logistic Regression  
*Quy trình chuẩn mực tuân thủ `AI Project Cycle.pptx`*
""")
st.divider()

# Sidebar: Thông tin hệ thống & Mô tả
with st.sidebar:
    st.header("⚙️ Cấu Hình & Thông Tin")
    st.markdown("""
    **Bộ dữ liệu:** 20,000 Hotel Reviews (`dts_20k_raw.csv`)  
    **Tác vụ:** Phân loại cảm xúc nhị phân:
    - **Positive (1):** Hài lòng
    - **Negative (0):** Không hài lòng
    """)
    st.markdown("---")
    st.subheader("💡 Mẹo kiểm thử trước Hội đồng:")
    st.info("""
    1. **Thử câu phủ định kép:**  
       `"Not bad at all, quite comfortable."`  
    2. **Thử câu có từ 'No Negative':**  
       `"No Negative. Clean room, friendly staff."`  
    3. **Thử câu mỉa mai (Sarcasm):**  
       `"Thank you for the free swimming pool in our leaking bathroom!"`
    """)
    st.markdown("---")
    st.caption("AI Project Cycle | Đại học Bách Khoa / CNTT")

# Các câu ví dụ mẫu phong phú
SAMPLE_REVIEWS = {
    "-- Chọn một đánh giá mẫu để kiểm thử nhanh --": "",
    "1. Tích cực rõ ràng (Clear Positive)": "A very comfortable bed, clean room and a very good breakfast. The best hotel I have ever stayed in!",
    "2. Tiêu cực rõ ràng (Clear Negative)": "Terrible experience. The air conditioner was broken, the bathroom was dirty, and the staff was extremely rude.",
    "3. Phủ định tinh vi (Subtle Negation)": "Lower price but not bad service at all. Clean room and decent breakfast.",
    "4. Cảm xúc pha trộn (Mixed Sentiment)": "The location is fantastic right near the subway, but the noise from outside was unbearable and the room was tiny.",
    "5. Châm biếm (Sarcasm)": "Thank you for giving us a free indoor swimming pool in our leaking bathroom. Absolutely unforgettable!",
    "6. Dữ liệu Booking.com đặc trưng ('No Negative')": "No Negative A very pleasant stay with wonderful hospitality and spacious room."
}

# Khu vực nhập liệu
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📝 Nhập Đánh Giá Khách Sạn (English Review)")
    selected_sample = st.selectbox("Chọn ví dụ mẫu:", list(SAMPLE_REVIEWS.keys()))
    
    default_text = SAMPLE_REVIEWS[selected_sample] if selected_sample != "-- Chọn một đánh giá mẫu để kiểm thử nhanh --" else ""
    user_review = st.text_area(
        "Nhập hoặc chỉnh sửa văn bản đánh giá:",
        value=default_text,
        height=140,
        placeholder="Ví dụ: The room was great, but the air conditioner was a bit noisy..."
    )
    
    predict_btn = st.button("🚀 Phân Tích Cảm Xúc (Analyze Sentiment)", type="primary", use_container_width=True)

with col_right:
    st.subheader("📊 Kết Quả So Sánh Nhanh")
    
    if predict_btn and user_review.strip():
        # Dự đoán Baseline
        res_baseline = None
        try:
            res_baseline = predict_baseline(user_review.strip())
        except Exception as e:
            st.warning(f"Chưa nạp được Baseline: {e}")
            
        # Dự đoán BERT
        res_bert = None
        try:
            res_bert = predict_bert(user_review.strip())
        except Exception as e:
            st.info(f"Mô hình BERT đang ở trạng thái huấn luyện hoặc chưa lưu weights: {e}")
            
        # Hiển thị kết quả BERT
        if res_bert is not None:
            st.markdown("### 🤖 Mô hình BERT (bert-base-uncased)")
            is_pos = res_bert["label"] == "Positive"
            badge_color = "#2ecc71" if is_pos else "#e74c3c"
            badge_icon = "😊 TÍCH CỰC (POSITIVE)" if is_pos else "😠 TIÊU CỰC (NEGATIVE)"
            
            st.markdown(
                f"""
                <div style="background-color: {badge_color}20; border-left: 6px solid {badge_color}; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
                    <h3 style="color: {badge_color}; margin: 0;">{badge_icon}</h3>
                    <p style="margin: 4px 0 0 0; font-size: 15px;">Độ tin cậy (Confidence): <b>{res_bert['confidence']*100:.2f}%</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Thanh đo xác suất
            prob_df = pd.DataFrame({
                "Cảm xúc": ["Tiêu cực (Negative)", "Tích cực (Positive)"],
                "Xác suất": [res_bert["prob_negative"], res_bert["prob_positive"]]
            })
            st.bar_chart(prob_df.set_index("Cảm xúc"), color="#3498db")
            
        # Hiển thị kết quả Baseline
        if res_baseline is not None:
            st.markdown("### 📈 Mô hình Baseline (TF-IDF + Logistic Regression)")
            is_base_pos = res_baseline["label"] == "Positive"
            base_color = "#27ae60" if is_base_pos else "#c0392b"
            base_icon = "Positive" if is_base_pos else "Negative"
            st.write(f"Dự đoán: **{base_icon}** (Độ tin cậy: **{res_baseline['confidence']*100:.2f}%**)")
            st.caption(f"Xác suất: Negative = {res_baseline['prob_negative']:.3f} | Positive = {res_baseline['prob_positive']:.3f}")
            
    elif predict_btn and not user_review.strip():
        st.warning("⚠️ Vui lòng nhập văn bản hoặc chọn một ví dụ mẫu trước khi phân tích!")

# Khu vực hiển thị chi tiết Tokenization của BERT
if predict_btn and user_review.strip() and 'res_bert' in locals() and res_bert is not None:
    st.divider()
    st.subheader("🔍 Chi Tiết Bẻ Từ WordPiece của BERT (Explainability)")
    st.markdown("""
    Cơ chế **WordPiece Tokenization** giúp BERT giải quyết triệt để vấn đề từ ngoài từ điển (OOV).  
    Các token bắt đầu bằng `##` thể hiện phần tiếp nối của một từ phức tạp. `[CLS]` đại diện cho phân loại cả câu, `[SEP]` đánh dấu kết thúc câu.
    """)
    
    tokens = res_bert.get("tokens", [])
    if tokens:
        # Hiển thị các badges tokens
        tokens_html = " ".join([
            f"<span style='background-color: #ecf0f1; color: #2c3e50; padding: 4px 8px; border-radius: 4px; margin: 3px; display: inline-block; font-family: monospace;'>{t}</span>"
            for t in tokens
        ])
        st.markdown(tokens_html, unsafe_allow_html=True)
