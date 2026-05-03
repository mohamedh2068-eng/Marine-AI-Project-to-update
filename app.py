import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import random

# ================= PAGE =================
st.set_page_config(page_title="AI Marine Twin FINAL BOSS", layout="wide")

# ================= INTRO SCREEN =================
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:
    st.markdown("""
    <style>
    .intro {
        padding:60px;
        text-align:center;
        background: radial-gradient(circle at top, #0f172a, #020617);
        border-radius:20px;
        box-shadow: 0 0 40px rgba(0,234,255,0.2);
    }
    .title {
        font-size:42px;
        color:#00eaff;
        font-weight:bold;
    }
    .sub {
        color:#94a3b8;
        font-size:18px;
        margin-top:10px;
    }
    .box {
        margin-top:20px;
        padding:15px;
        border:1px solid #00eaff;
        border-radius:12px;
        display:inline-block;
        color:white;
        line-height:1.8;
    }
    </style>

    <div class="intro">
        <div class="title">⚓ AI Marine Propeller System</div>
        <div class="sub">Digital Twin + AI Design + Simulation Engine</div>

        <div class="box">
            👨‍💻 إعداد: <b>محمد أشرف حسين دسوقي</b><br>
            🎓 إشراف: <b>د. حسين المصري</b><br>
            🏫 الكلية: <b>جامعة شرق بورسعيد التكنولوجية</b><br>
            🧭 القسم: <b>تكنولوجيا تشغيل وصيانة السفن</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 دخول النظام"):
        st.session_state.start = True
        st.rerun()

    st.stop()

# ================= DATA + MODEL =================
X = np.array([
    [1.5, 15, 4, 1200],
    [2.0, 20, 5, 1500],
    [1.2, 10, 3, 1000],
    [3.0, 30, 6, 2000],
    [2.5, 25, 5, 1800],
])

y = np.array([0.72, 0.70, 0.78, 0.85, 0.88])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_scaled, y)

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Control Panel")

diameter = st.sidebar.slider("Diameter", 0.5, 10.0, 2.0)
speed = st.sidebar.slider("Speed", 5, 50, 20)
blades = st.sidebar.selectbox("Blades", [3,4,5,6])
pitch = st.sidebar.slider("Pitch", 0.1, 3.0, 1.2)
rpm = st.sidebar.slider("RPM", 100, 3000, 1500)

# ================= PREDICTION =================
inp = scaler.transform([[diameter, speed, blades, rpm]])
eff = model.predict(inp)[0]

st.metric("⚡ Efficiency Score", f"{eff*100:.2f}%")

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Performance",
    "🧊 3D Model",
    "🌊 Flow Simulation",
    "🖼️ AI Vision"
])

# ================= TAB 1 =================
with tab1:
    st.subheader("📊 Performance Dashboard")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Diameter", f"{diameter} m")
    c2.metric("Speed", f"{speed} knots")
    c3.metric("Blades", blades)
    c4.metric("RPM", rpm)

# ================= TAB 2 =================
with tab2:
    st.subheader("🧊 3D Propeller Model")

    theta = np.linspace(0, 2*np.pi, 100)
    r = np.linspace(0.2, 1, 100)
    theta, r = np.meshgrid(theta, r)

    twist = r * 2.5
    x = r * np.cos(theta + twist)
    y = r * np.sin(theta + twist)
    z = pitch * np.sin(4*theta)*(1-r)

    fig = go.Figure()

    for i in range(blades):
        angle = i * 2*np.pi/blades
        xr = x*np.cos(angle) - y*np.sin(angle)
        yr = x*np.sin(angle) + y*np.cos(angle)

        fig.add_trace(go.Surface(x=xr, y=yr, z=z, showscale=False))

    fig.update_layout(template="plotly_dark", height=600)
    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 3 =================
with tab3:
    st.subheader("🌊 Flow Simulation")

    n = 70
    x = np.linspace(-2,2,n)
    y = np.linspace(-2,2,n)
    X, Y = np.meshgrid(x,y)

    R = np.sqrt(X**2 + Y**2) + 0.1
    U = -Y / R + np.sin(X)
    V = X / R + np.cos(Y)

    fig2, ax = plt.subplots()
    ax.streamplot(X, Y, U, V, color=np.sqrt(U**2+V**2), cmap="plasma")
    ax.set_title("Pseudo CFD Flow Field")
    st.pyplot(fig2)

# ================= TAB 4 =================
with tab4:
    st.subheader("🖼️ AI Synthetic Vision")

    mode = st.selectbox("Mode", ["Cavitation", "Pressure Field", "Wake Turbulence"])

    size = 250
    x = np.linspace(-3,3,size)
    y = np.linspace(-3,3,size)
    X, Y = np.meshgrid(x,y)

    noise = np.random.normal(0, 0.1, (size,size))

    if mode == "Cavitation":
        Z = np.sin(X*5)*np.cos(Y*5) + noise
    elif mode == "Pressure Field":
        Z = np.exp(-(X**2 + Y**2)) + noise
    else:
        Z = np.sin(X**2 + Y**2) + np.cos(X*Y)

    fig3, ax3 = plt.subplots()
    ax3.imshow(Z, cmap="inferno")
    ax3.set_title(mode)
    st.pyplot(fig3)

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🚀 AI Marine Twin System")
st.markdown("👨‍💻 Mohamed Ashraf Hussein Desouky")
