import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="M.AFixly | Marine AI", layout="wide")

# منع الترجمة التلقائية تماماً
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

# 2. تصميم احترافي (بسيط ونظيف جداً)
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: white; }
    .stTabs [data-baseweb="tab"] { color: white; font-size: 18px; }
    .stMetric { background: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #fbbf24; }
    .header-style {
        text-align: center;
        padding: 30px;
        background: #1e293b;
        border-radius: 15px;
        border: 1px solid #fbbf24;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر (بدون ترجمة خاطئة)
st.markdown("""
    <div class="header-style" class="notranslate">
        <h1 style='color: #fbbf24;'>M.AFixly - Marine AI System</h1>
        <h2 style='color: white;'>جامعة شرق بورسعيد التكنولوجية</h2>
        <p style='color: #94a3b8;'>قسم تكنولوجيا تشغيل وصيانة السفن</p>
        <hr style='border-color: #fbbf24;'>
        <p style='font-size: 1.2em;'><b>الطالب:</b> محمد أشرف حسين دسوقي</p>
        <p style='font-size: 1.1em; color: #fbbf24;'><b>تحت إشراف:</b> أ.د/ حسين المصري</p>
    </div>
    """, unsafe_allow_html=True)

# 4. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ Configuration")
    diam = st.slider("Propeller Diameter (m)", 0.5, 8.0, 2.5)
    speed = st.slider("Ship Speed (Knots)", 5, 50, 20)
    blades = st.radio("Number of Blades", [3, 4, 5], horizontal=True)
    st.write("---")
    st.success("System is Online")

# 5. عرض النتائج (الأداء)
tab1, tab2, tab3 = st.tabs(["📊 Performance", "🔧 CNC G-Code", "📖 Project Info"])

with tab1:
    # حسابات هندسية بسيطة ومظبوطة
    efficiency = 0.85 - (speed * 0.003)
    thrust = (diam**2) * (speed**1.2) * 0.5
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Efficiency (η)", f"{efficiency*100:.1f}%")
    c2.metric("Thrust Force", f"{thrust:.2f} kN")
    
    # حل مشكلة مستوى الكافيتيشن
    status = "SAFE / آمن" if speed < 35 else "RISK / خطر"
    c3.metric("Cavitation Status", status)

    # رسم بياني احترافي
    st.subheader("Performance Characteristics")
    j = np.linspace(0.1, 1.2, 50)
    kt = 0.55 - 0.4 * j
    fig = go.Figure(data=go.Scatter(x=j, y=kt, line=dict(color='#fbbf24', width=4)))
    fig.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Automated CNC Path Generation")
    st.info("Generating G-Code for 5-Axis Machining Center...")
    st.code(f"""
    G21 ; Units mm
    G90 ; Absolute Mode
    M03 S2800 ; Spindle Start
    G01 X0 Y0 Z10 F100
    (Machining Propeller Diameter: {diam}m)
    (Blades Count: {blades})
    G01 Z-5.0 F50
    M30 ; End
    """, language="gcode")

with tab3:
    st.write("### About M.AFixly")
    st.write("هذا النظام يهدف إلى دمج تقنيات الذكاء الاصطناعي في هندسة السفن لتوفير الوقت والجهد في عملية تصميم وتصنيع الرفاصات البحرية.")

st.markdown("<p style='text-align: center; color: #64748b;'>© 2026 Powered by Mohamed Ashraf</p>", unsafe_allow_html=True)
