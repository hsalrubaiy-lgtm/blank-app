import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد واجهة "دايموند"
st.set_page_config(page_title="شركة دايموند", page_icon="💎", layout="wide")

if 'diamond_ledger' not in st.session_state:
    st.session_state.diamond_ledger = pd.DataFrame(columns=["التاريخ", "البيان", "التصنيف", "المبلغ"])

st.title("💎 شركة دايموند لتجارة السيارات")

# القسم الخاص بإضافة البيانات
with st.form("my_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("التاريخ")
        cat = st.selectbox("التصنيف", ["أرباح", "مصاريف"])
    with col2:
        desc = st.text_input("البيان")
        amount = st.number_input("المبلغ", min_value=0)
    
    if st.form_submit_button("حفظ"):
        new_row = pd.DataFrame([{"التاريخ": date, "البيان": desc, "التصنيف": cat, "المبلغ": amount}])
        st.session_state.diamond_ledger = pd.concat([st.session_state.diamond_ledger, new_row], ignore_index=True)
        st.rerun()

st.dataframe(st.session_state.diamond_ledger)
