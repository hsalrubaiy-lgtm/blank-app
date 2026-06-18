import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# إعداد واجهة "دايموند" الفخمة والألوان (الأسود والذهبي)
st.set_page_config(page_title="شركة دايموند لتجارة السيارات", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: #ffffff; }
    h1, h2, h3, h4 { color: #e2c275 !important; font-family: 'Cairo', sans-serif; text-align: right; }
    .stButton>button { background-color: #e2c275; color: black; font-weight: bold; width: 100%; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #b89149; color: white; }
    div[data-testid="metric-container"] { background-color: #1a1a1a; border: 1px solid #e2c275; padding: 20px; border-radius: 12px; text-align: center; }
    div[data-testid="metric-container"] label { color: #e2c275 !important; font-size: 20px !important; }
    .rtl-text { text-align: right; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# تهيئة البيانات في المتصفح
if 'diamond_ledger' not in st.session_state:
    st.session_state.diamond_ledger = pd.DataFrame(columns=["التاريخ", "البيان / الوصف", "التصنيف الرئيسي", "نوع الحركة", "المبلغ (د.ع)"])

if 'diamond_debts' not in st.session_state:
    st.session_state.diamond_debts = pd.DataFrame(columns=["الزبون/المطلوب", "نوع الدين", "المبلغ الكلي (د.ع)", "المسدد (د.ع)", "المتبقي (د.ع)", "الحالة"])

# عنوان النظام الفخم
st.markdown('<h1 class="rtl-text">💎 شركة دايموند لتجارة السيارات</h1>', unsafe_allow_html=True)
st.markdown('<p class="rtl-text" style="color:#888;">النظام الحسابي الفخم والمطور لإدارة الأرباح والمصاريف بالدينار العراقي</p>', unsafe_allow_html=True)
st.markdown("---")

# الحسابات الإجمالية لتعرض بالخانات الفوق (الأرباح والمصاريف ليفوق)
df = st.session_state.diamond_ledger
total_revenue = df[df["التصنيف الرئيسي"] == "أرباح (إيرادات)"]["المبلغ (د.ع)"].sum()
total_expenses = df[df["التصنيف الرئيسي"].str.contains("مصاريف", na=False)]["المبلغ (د.ع)"].sum()
net_profit = total_revenue - total_expenses

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="💰 إجمالي الأرباح والواردات", value=f"{total_revenue:,.0f} د.ع")
with col_m2:
    st.metric(label="📉 إجمالي كافة المصاريف", value=f"{total_expenses:,.0f} د.ع")
with col_m3:
    st.metric(label="🟩 صافي الأرباح الحقيقية", value=f"{net_profit:,.0f} د.ع")

st.markdown("---")

# تنظيم بقية الأقسام في تبويبات أسفل الخلاصة
tab1, tab2, tab3, tab4 = st.tabs(["📝 تسجيل حركة", "📉 الرسوم البيانية", "🤝 الديون والأقساط", "📋 التفاصيل والتصدير"])

with tab1:
    st.markdown('<h3 class="rtl-text">💵 إضافة عملية جديدة</h3>', unsafe_allow_html=True)
    with st.form("diamond_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            main_cat = st.selectbox("التصنيف الرئيسي", ["أرباح (إيرادات)", "مصاريف ثابتة", "مصاريف متغيرة"])
            if main_cat == "أرباح (إيرادات)":
                sub_cat = st.selectbox("نوع الحركة", ["بيع سيارة", "عمولة/دلالية", "أرباح صيانة/تجهيز", "إيرادات أخرى"])
            elif main_cat == "مصاريف ثابتة":
                sub_cat = st.selectbox("نوع الحركة", ["إيجار المعرض", "رواتب الموظفين", "مولدة/كهرباء", "إنترنت ومياه"])
            else:
                sub_cat = st.selectbox("نوع الحركة", ["تجهيز/تعديل سيارات", "إعلانات وتمويل", "ضيافة ومصاريف يومية", "أخرى"])
        with col2:
            date_val = st.date_input("التاريخ", datetime.now())
            amount_val = st.number_input("المبلغ (د.ع)", min_value=0, step=250000)
            desc_val = st.text_input("البيان / الوصف (مثال: أرباح تاهو 2024)")
        
        submit_btn = st.form_submit_button("💾 حفظ العملية")
        if submit_btn and amount_val > 0:
            new_row = pd.DataFrame([{"التاريخ": date_val.strftime("%Y-%m-%d"), "البيان / الوصف": desc_val, "التصنيف الرئيسي": main_cat, "نوع الحركة": sub_cat, "المبلغ (د.ع)": amount_val}])
            st.session_state.diamond_ledger = pd.concat([st.session_state.diamond_ledger, new_row], ignore_index=True)
            st.success("✅ تم حفظ العملية وتحديث الخانات الفوق فوراً!")
            st.rerun()

with tab2:
    st.markdown('<h3 class="rtl-text">📊 التحليل البياني</h3>', unsafe_allow_html=True)
    if not df.empty:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig1 = px.pie(df, values='المبلغ (د.ع)', names='التصنيف الرئيسي', title="نسبة الواردات للمصاريف", color_discrete_sequence=['#e2c275', '#ff4d4d', '#3498db'])
            st.plotly_chart(fig1, use_container_width=True)
        with col_g2:
            fig2 = px.bar(df, x='نوع الحركة', y='المبلغ (د.ع)', color='التصنيف الرئيسي', title="المبالغ بالتفصيل")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("💡 سجل بعض العمليات أولاً لعرض المخططات.")

with tab3:
    st.markdown('<h3 class="rtl-text">🤝 الديون والأقساط</h3>', unsafe_allow_html=True)
    with st.form("debt_form", clear_on_submit=True):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            debtor_name = st.text_input("اسم الزبون / الجهة")
            debt_type = st.selectbox("نوع الدين", ["لنا (قسط على زبون)", "علينا (مطلوبين لشخص/معرض)"])
        with col_d2:
            total_debt = st.number_input("المبلغ الكلي (د.ع)", min_value=0, step=500000)
            paid_debt = st.number_input("المسدد حالياً (د.ع)", min_value=0, step=500000)
        
        if st.form_submit_button("➕ تسجيل الدين"):
            rem = total_debt - paid_debt
            stat = "تم السداد" if rem <= 0 else "متبقي"
            new_debt = pd.DataFrame([{"الزبون/المطلوب": debtor_name, "نوع الدين": debt_type, "المبلغ الكلي (د.ع)": total_debt, "المسدد (د.ع)": paid_debt, "المتبقي (د.ع)": rem, "الحالة": stat}])
            st.session_state.diamond_debts = pd.concat([st.session_state.diamond_debts, new_debt], ignore_index=True)
            st.success("✅ تم الحفظ.")
            st.rerun()
    st.dataframe(st.session_state.diamond_debts, use_container_width=True)

with tab4:
    st.markdown('<h3 class="rtl-text">📋 جدول التفاصيل وتصدير التقرير</h3>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    # ميزة التصدير الخاصة (الخلاصة فوق والجدول جوة)
    if not df.empty:
        report_text = f"--- تقرير شركة دايموند المالي ---\n\n"
        report_text += f"إجمالي الأرباح والواردات: {total_revenue:,.0f} د.ع\n"
        report_text += f"إجمالي كافة المصاريف: {total_expenses:,.0f} د.ع\n"
        report_text += f"صافي الأرباح الحقيقية: {net_profit:,.0f} د.ع\n"
        report_text += f"=========================================\n\n"
        report_text += "تفاصيل العمليات والسجلات اليومية:\n"
        report_text += df.to_string(index=False)
        
        st.download_button(
            label="📥 تحميل وحفظ كملف (خلاصة ليفوق والتفاصيل جوة)",
            data=report_text,
            file_name=f"Diamond_Financial_Report_{datetime.now().strftime('%Y-%m-%d')}.txt",
            mime="text/plain"
        )
    
    if st.button("🗑️ مسح وتصفير كافة الحسابات"):
        st.session_state.diamond_ledger = pd.DataFrame(columns=["التاريخ", "البيان / الوصف", "التصنيف الرئيسي", "نوع الحركة", "المبلغ (د.ع)"])
        st.session_state.diamond_debts = pd.DataFrame(columns=["الزبون/المطلوب", "نوع الدين", "المبلغ الكلي (د.ع)", "المسدد (د.ع)", "المتبقي (د.ع)", "الحالة"])
        st.rerun()
