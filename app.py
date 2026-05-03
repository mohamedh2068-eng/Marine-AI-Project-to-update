import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ================= PAGE =================
st.set_page_config(page_title="M.AFixly", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.main {
    background: linear-gradient(180deg, #020617, #020617);
    color: white;
}
.hero {
    padding:50px;
    border-radius:20px;
    text-align:center;
    background: linear-gradient(135deg, rgba(0,234,255,0.1), rgba(2,6,23,0.9));
    box-shadow: 0 0 50px rgba(0,234,255,0.2);
}
.title {
    font-size:40px;
    color:#00eaff;
    font-weight:bold;
}
.subtitle {
    color:#94a3b8;
    font-size:20px;
}
.box {
    padding:12px 20px;
    border-radius:10px;
    border:1px solid #00eaff;
    margin:5px;
}
button {
    background: linear-gradient(90deg,#00eaff,#0ea5e9) !important;
    color:black !important;
    font-weight:bold !important;
    border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="hero">
<div class="title">جامعة شرق بورسعيد التكنولوجية</div>
<div class="subtitle">تكنولوجيا تشغيل وصيانة السفن</div>
<br>
<div class="subtitle">نظام الذكاء الاصطناعي لتصميم وتصنيع الرفاصات البحرية (CNC)</div>
<br>

<div style="display:flex; justify-content:center; gap:15px; flex-wrap:wrap;">
<div class="box">👨‍💻 إعداد: <b>محمد أشرف حسين دسوقي</b></div>
<div class="box">🎓 إشراف: <b>أ.د / حسين المصري</b></div>
</div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")

    d_input = st.number_input("Diameter (m)", 0.5, 10.0, 1.5)
    v_input = st.slider("Speed (knots)", 5, 50, 15)
    blades = st.selectbox("Blades", [3,4,5,6])
    pitch = st.slider("Pitch", 0.1, 2.0, 0.8)

    st.button("🔍 Scan Vessel")
    st.button("⚙ Send to CNC")

# ================= AI =================
X = np.array([[1.5,15,4],[2.0,20,5],[1.2,10,3]])
y = np.array([0.72,0.70,0.78])

model = LinearRegression().fit(X,y)
eff = model.predict([[d_input,v_input,blades]])[0]

# ================= TABS =================
tab1, tab2 = st.tabs(["📊 Data", "🧊 3D Model"])

# ================= DATA =================
with tab1:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Diameter", f"{d_input} m")
    c2.metric("Pitch", f"{pitch}")
    c3.metric("Blades", blades)
    c4.metric("Efficiency", f"{eff*100:.1f}%")

# ================= 3D =================
with tab2:

    st.markdown("### ⚓ AI Generated Propeller")

    theta = np.linspace(0, 2*np.pi, 80)
    r = np.linspace(0.2, 1, 80)
    theta, r = np.meshgrid(theta, r)

    twist = r * 2

    x = r * np.cos(theta + twist)
    y = r * np.sin(theta + twist)
    z = pitch * np.sin(3*theta)*(1-r)

    fig = go.Figure()

    colorscale = [[0, "#00eaff"], [1, "#2563eb"]]

    for i in range(blades):
        angle = i * 2*np.pi/blades
        xr = x*np.cos(angle) - y*np.sin(angle)
        yr = x*np.sin(angle) + y*np.cos(angle)

        fig.add_trace(go.Surface(
            x=xr, y=yr, z=z,
            colorscale=colorscale,
            showscale=False
        ))

    # HUB
    z_h = np.linspace(-0.5,0.5,20)
    th = np.linspace(0,2*np.pi,20)
    th,z_h = np.meshgrid(th,z_h)

    xh = 0.2*np.cos(th)
    yh = 0.2*np.sin(th)

    fig.add_trace(go.Surface(
        x=xh,y=yh,z=z_h,
        colorscale=[[0,"#aaa"],[1,"#fff"]],
        showscale=False
    ))

    fig.update_layout(
        template="plotly_dark",
        height=600,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= FOOTER =================
st.markdown("""
<hr>
<p style='text-align:center;color:gray;'>
© 2026 M.AFixly | Mohamed Ashraf
</p>
""", unsafe_allow_html=True)
