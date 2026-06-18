import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد واجهة "دايموند" الفخمة
st.set_page_config(page_title="شركة دايموند لتجارة السيارات", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: #ffffff; }
    h1, h2, h3, h4 { color: #e2c275 !important; font-family: 'Cairo', sans-serif; text-align: right; }
    .stButton>button { background-color: #e2c275; color: black; font-weight: bold; width: 100%; border-radius: 8px; border: none; }
    div[data-testid="metric-container"] { background-color: #1a1a1a; border: 1px solid #e2c275; padding: 20px; border-radius: 12px; text-align: center; }
    div[data-testid="metric-container"] label { color: #e2c275 !important; font-size: 20px !important; }
    .rtl-text { text-align: right; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

if 'diamond_ledger' not in st.session_state:
    st.session_state.diamond_ledger = pd.DataFrame(columns=["التاريخ", "البيان / الوصف", "التصنيف الرئيسي", "نوع الحركة", "المبلغ (د.ع)"])

st.markdown('<h1 class="rtl-text">💎 شركة دايموند لتجارة السيارات</h1>', unsafe_allow_html=True)
st.markdown("---")

# الحسابات
df = st.session_state.diamond_ledger
total_revenue = df[df["التصنيف الرئيسي"] == "أرباح (إيرادات)"]["المبلغ (د.ع)"].sum() if not df.empty else 0
total_expenses = df[df["التصنيف الرئيسي"].str.contains("مصاريف", na=False)]["المبلغ (د.ع)"].sum() if not df.empty else 0
net_profit = total_revenue - total_expenses

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="💰 إجمالي الأرباح", value=f"{total_revenue:,.0f} د.ع")
with col_m2:
    st.metric(label="📉 إجمالي المصاريف", value=f"{total_expenses:,.0f} د.ع")
with col_m3:
    st.metric(label="🟩 صافي الأرباح", value=f"{net_profit:,.0f} د.ع")

st.markdown("---")

# الإضافة
with st.form("diamond_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        main_cat = st.selectbox("التصنيف الرئيسي", ["أرباح (إيرادات)", "مصاريف ثابتة", "مصاريف متغيرة"])
        sub_cat = st.text_input("نوع الحركة")
    with col2:
        date_val = st.date_input("التاريخ", datetime.now())
        amount_val = st.number_input("المبلغ (د.ع)", min_value=0, step=250000)
    desc_val = st.text_input("البيان / الوصف")
    if st.form_submit_button("💾 حفظ العملية"):
        new_row = pd.DataFrame([{"التاريخ": str(date_val), "البيان / الوصف": desc_val, "التصنيف الرئيسي": main_cat, "نوع الحركة": sub_cat, "المبلغ (د.ع)": amount_val}])
        st.session_state.diamond_ledger = pd.concat([st.session_state.diamond_ledger, new_row], ignore_index=True)
        st.rerun()

st.dataframe(df, use_container_width=True)
