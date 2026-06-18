import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الواجهة لتكون مناسبة للموبايل واللغة العربية
st.set_page_config(page_title="شركة دايموند لتجارة السيارات", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    body, div, p, h1, h2, h3, h4, span, input, label, select { text-align: right; direction: rtl; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { width: 100%; background-color: #008080; color: white; border-radius: 8px; font-weight: bold; height: 45px; }
    .metric-box { padding: 15px; border-radius: 10px; background-color: #1e1e1e; color: white; border-right: 5px solid #008080; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 شركة دايموند لتجارة السيارات")
st.write("النظام الحسابي الذكي لإدارة الأرباح والمصاريف بالدينار العراقي")
st.write("---")

if 'diamond_ledger' not in st.session_state:
    st.session_state.diamond_ledger = pd.DataFrame(columns=["التاريخ", "البيان / الوصف", "التصنيف الرئيسي", "نوع الحركة", "المبلغ (د.ع)"])

df = st.session_state.diamond_ledger

st.subheader("📊 الموقف المالي الحالي (الخلاصة)")
total_earnings = df[df["التصنيف الرئيسي"] == "أرباح (إيرادات)"]["المبلغ (د.ع)"].sum()
total_expenses = df[df["التصنيف الرئيسي"] != "أرباح (إيرادات)"]["المبلغ (د.ع)"].sum()
net_profit = total_earnings - total_expenses

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='metric-box'><h4>💰 إجمالي الأرباح</h4><h2>{total_earnings:,.0f} د.ع</h2></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='metric-box'><h4>📉 إجمالي المصاريف</h4><h2>{total_expenses:,.0f} د.ع</h2></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='metric-box'><h4>🟩 صافي الربح</h4><h2>{net_profit:,.0f} د.ع</h2></div>", unsafe_allow_html=True)

st.write("---")
st.subheader("➕ تسجيل حركة مالية جديدة")

with st.form("diamond_form", clear_on_submit=True):
    date_val = st.date_input("التاريخ", datetime.now())
    main_cat = st.selectbox("التصنيف الرئيسي", ["أرباح (إيرادات)", "مصاريف ثابتة", "مصاريف متحركة"])
    sub_cat = st.text_input("نوع الحركة / التفصيل", placeholder="مثال: ارباح سيارات، ايجار، رواتب")
    amount_val = st.number_input("المبلغ بالدينار العراقي (د.ع)", min_value=0, step=25000)
    desc_val = st.text_input("البيان / الوصف التوضيحي")
    
    submit = st.form_submit_button("📥 حفظ الحركة وتحديث الحسابات")
    if submit and amount_val > 0:
        new_data = pd.DataFrame([{"التاريخ": date_val.strftime('%Y-%m-%d'), "البيان / الوصف": desc_val, "التصنيف الرئيسي": main_cat, "نوع الحركة": sub_cat, "المبلغ (د.ع)": amount_val}])
        st.session_state.diamond_ledger = pd.concat([st.session_state.diamond_ledger, new_data], ignore_index=True)
        st.success("✅ تم الحفظ بنجاح!")
        st.rerun()

st.write("---")
st.subheader("📜 سجل الحركات المكتملة")
if not df.empty:
    st.dataframe(df.iloc[::-1], use_container_width=True)
else:
    st.info("السجل فارغ حالياً.")
