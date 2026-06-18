import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد واجهة "دايموند" الفخمة
st.set_page_config(page_title="Diamond Co. System", page_icon="💎", layout="wide")

# CSS لتغيير الألوان للذهبي والأسود
st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: #ffffff; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #e2c275; padding: 20px; border-radius: 15px; }
    div[data-testid="metric-container"] label { color: #e2c275 !important; font-size: 20px !important; }
    .stButton>button { background-color: #e2c275; color: black; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("💎 نظام شركة دايموند المطور")

# ... (باقي كود الحسابات مالتك) ...

# --- إضافة ميزة التصدير اللي طلبتها ---
st.markdown("---")
st.subheader("📤 تصدير التقارير المالية")

if not st.session_state.diamond_ledger.empty:
    # إنشاء ملف نصي أو Excel بترتيب خاص
    df = st.session_state.diamond_ledger
    rev = df[df["التصنيف الرئيسي"] == "أرباح (إيرادات)"]["المبلغ (د.ع)"].sum()
    exp = df[df["التصنيف الرئيسي"].str.contains("مصاريف")]["المبلغ (د.ع)"].sum()
    
    # تنسيق التقرير: الأرقام فوق، الجدول جوة
    report_text = f"--- تقرير شركة دايموند المالي ---\n"
    report_text += f"إجمالي الأرباح: {rev:,.0f} د.ع\n"
    report_text += f"إجمالي المصاريف: {exp:,.0f} د.ع\n"
    report_text += f"صافي الربح: {rev-exp:,.0f} د.ع\n"
    report_text += f"----------------------------\n\n"
    report_text += "التفاصيل:\n"
    report_text += df.to_string(index=False)
    
    st.download_button(
        label="📥 تحميل التقرير (خلاصة + تفاصيل)",
        data=report_text,
        file_name=f"Diamond_Report_{datetime.now().strftime('%Y-%m-%d')}.txt",
        mime="text/plain"
    )

اللصق الكود، اضغط **Commit**، وحدث صفحة السيستم. راح تشوف الواجهة تغيرت وصار عندك زر تحميل يرتّب البيانات مثل ما طلبت بالظبط! بشرني شلون طلع عندك؟ 💎🚀
