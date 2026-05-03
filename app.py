import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# ================= PAGE =================
st.set_page_config(page_title="AI Marine Twin", layout="wide")

# ================= INTRO SCREEN =================
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:

    st.markdown("""
    <style>
    .hero {
        text-align:center;
        padding:60px;
        border-radius:25px;
        background: linear-gradient(135deg, #0f172a, #020617);
        box-shadow: 0 0 60px rgba(0,234,255,0.25);
    }

    .title {
        font-size:48px;
        color:#00eaff;
        font-weight:800;
        margin-bottom:10px;
    }

    .sub {
        color:#94a3b8;
        font-size:18px;
        margin-bottom:20px;
    }

    .card {
        display:inline-block;
        padding:20px;
        border-radius:15px;
        border:1px solid #00eaff;
        color:white;
        line-height:1.8;
        background: rgba(255,255,255,0.03);
    }
    </style>

    <div class="hero">
        <div class="title">⚓ AI Marine Propeller System</div>
        <div class="sub">Digital Twin • CFD Simulation • AI Engineering Design</div>

        <img src="https://images.unsplash.com/photo-1548574505-5e239809ee19"
             style="width:80%; border-radius:15px; margin-bottom:20px;">

        <div class="card">
            👨‍💻 <b>محمد أشرف حسين دسوقي</b><br>
            🎓 إشراف: د. حسين المصري<br>
            🏫 جامعة شرق بورسعيد التكنولوجية<br>
            🧭 تكنولوجيا تشغيل وصيانة السفن
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 دخول النظام"):
        st.session_state.start = True
        st.rerun()

    st.stop()

# ================= AI MODEL =================
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

st.metric("⚡ Efficiency", f"{eff*100:.2f}%")

# ================= TABS =================
tab1, tab2, tab3 = st.tabs([
    "📊 Data",
    "🧊 3D Animation",
    "🌊 Flow Simulation"
])

# ================= TAB 1 =================
with tab1:
    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Efficiency", f"{eff*100:.2f}%")
    c2.metric("Diameter", f"{diameter} m")
    c3.metric("Speed", f"{speed} knots")
    c4.metric("RPM", rpm)

# ================= TAB 2 (ANIMATED 3D) =================
with tab2:
    st.subheader("🧊 Real-Time Animated Propeller")

    theta = np.linspace(0, 2*np.pi, 120)
    r = np.linspace(0.2, 1.2, 120)
    theta, r = np.meshgrid(theta, r)

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    blade = np.sin(theta * 2) * (1 - r)
    z = 0.25 * blade

    speed_ctrl = st.slider("Rotation Speed", 0.0, 5.0, 1.5)

    fig = go.Figure()

    for i in range(blades):

        base_angle = i * 2*np.pi/blades

        # static blade shape
        xr = x*np.cos(base_angle) - y*np.sin(base_angle)
        yr = x*np.sin(base_angle) + y*np.cos(base_angle)

        # animation rotation effect
        rot = speed_ctrl

        x_final = xr*np.cos(rot) - yr*np.sin(rot)
        y_final = xr*np.sin(rot) + yr*np.cos(rot)

        fig.add_trace(go.Surface(
            x=x_final,
            y=y_final,
            z=z,
            colorscale="Turbo",
            showscale=False,
            opacity=0.95
        ))

    # water surface
    wx = np.linspace(-2,2,30)
    wy = np.linspace(-2,2,30)
    WX, WY = np.meshgrid(wx,wy)
    WZ = np.zeros_like(WX) - 0.4

    fig.add_trace(go.Surface(
        x=WX, y=WY, z=WZ,
        colorscale=[[0,"#0ea5e9"],[1,"#0369a1"]],
        opacity=0.5,
        showscale=False
    ))

    fig.update_layout(
        template="plotly_dark",
        height=650,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        )
    )

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

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🚀 AI Marine Twin System")
st.markdown("👨‍💻 Mohamed Ashraf Hussein Desouky")
