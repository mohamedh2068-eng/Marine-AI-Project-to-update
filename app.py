import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعدادات الصفحة الأساسية وقفل الترجمة
st.set_page_config(page_title="M.AFixly Marine AI", layout="wide")

st.markdown("""
    <style>
    /* منع الترجمة التلقائية */
    * { font-family: 'Arial', sans-serif; }
    .main { background-color: #0e1117; }
    .stMetric { background: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #fbbf24; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .header-box {
        background: #1a1c24;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #fbbf24;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    <meta name="google" content="notranslate">
    """, unsafe_allow_html=True)

# 2. الهيدر الرسمي (نصوص ثابتة)
st.markdown("""
    <div class="header-box">
        <h1 style='color: #fbbf24; margin:0;'>M.AFixly: Marine AI Platform</h1>
        <h3 style='color: white; margin:5px;'>جامعة شرق بورسعيد التكنولوجية</h3>
        <p style='color: #888;'>إعداد الطالب: محمد أشرف حسين دسوقي</p>
        <p style='color: #fbbf24; font-weight: bold;'>تحت إشراف: أ.د/ حسين المصري</p>
    </div>
    """, unsafe_allow_html=True)

# 3. تقسيم الشاشة (Sidebar & Main)
with st.sidebar:
    st.header("⚙️ Design Inputs")
    d_m = st.slider("Diameter (m)", 0.5, 7.0, 2.5)
    v_k = st.slider("Speed (Knots)", 5, 50, 20)
    b_n = st.selectbox("Blades", [3, 4, 5])
    st.write("---")
    st.info("System Status: Operational")

# 4. الحسابات والنتائج
tab1, tab2 = st.tabs(["📊 Performance Analysis", "🤖 Manufacturing (CNC)"])

with tab1:
    # معادلات هندسية مبسطة
    eff = 0.85 - (v_k * 0.003)
    thrust = (d_m**2) * (v_k**1.3) * 0.45
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Efficiency (η)", f"{eff*100:.1f}%")
    c2.metric("Thrust (kN)", f"{thrust:.2f}")
    
    # حل مشكلة الكافيتيشن نهائياً
    c_label = "SAFE (آمن)" if v_k < 35 else "RISK (خطر)"
    c3.metric("Cavitation", c_label)

    # رسم بياني احترافي بـ Plotly (ثابت ومستقر)
    x = np.linspace(0.1, 1.2, 30)
    y = 0.5 - 0.3 * x
    fig = go.Figure(data=go.Scatter(x=x, y=y, line=dict(color='#fbbf24', width=3)))
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### CNC G-Code Generator")
    st.code(f"""
    (M.AFixly G-Code)
    G21 ; mm units
    G90 ; absolute
    M03 S2600 ; spindle on
    G01 X0 Y0 Z10 F200
    (Propeller D: {d_m}m | Blades: {b_n})
    M30 ; end
    """, language="gcode")

st.markdown("---")
st.caption("Developed by Mohamed Ashraf © 2026")
