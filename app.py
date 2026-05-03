import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# ================= PAGE =================
st.set_page_config(page_title="AI Marine Twin", layout="wide")

# ================= INTRO (CLEAN & PROFESSIONAL) =================
st.title("⚓ AI Marine Propeller System")

st.image(
    "https://images.unsplash.com/photo-1548574505-5e239809ee19",
    use_container_width=True
)

st.markdown("""
### 👨‍💻 محمد أشرف حسين دسوقي  
### 🎓 إشراف: د. حسين المصري  
### 🏫 جامعة شرق بورسعيد التكنولوجية  
### 🧭 تكنولوجيا تشغيل وصيانة السفن  
""")

st.markdown("---")

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

inp = scaler.transform([[diameter, speed, blades, rpm]])
eff = model.predict(inp)[0]

st.metric("⚡ Efficiency", f"{eff*100:.2f}%")

# ================= TABS =================
tab1, tab2, tab3 = st.tabs([
    "📊 Data",
    "🔄 Propeller Motion",
    "🌊 Flow"
])

# ================= TAB 1 =================
with tab1:
    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Efficiency", f"{eff*100:.2f}%")
    c2.metric("Diameter", f"{diameter} m")
    c3.metric("Speed", f"{speed} knots")
    c4.metric("RPM", rpm)

# ================= TAB 2 (REAL MOTION SIMULATION) =================
with tab2:
    st.subheader("🔄 Realistic Propeller Motion (Simulation)")

    speed_ctrl = st.slider("Rotation Speed Control", 0.1, 5.0, 1.5)

    fig = go.Figure()

    # WATER SURFACE
    wx = np.linspace(-2,2,25)
    wy = np.linspace(-2,2,25)
    WX, WY = np.meshgrid(wx,wy)
    WZ = np.zeros_like(WX) - 0.5

    fig.add_trace(go.Surface(
        x=WX,
        y=WY,
        z=WZ,
        colorscale=[[0,"#0ea5e9"],[1,"#075985"]],
        opacity=0.5,
        showscale=False
    ))

    # PROPELLER MOTION (REALISTIC LOOPED CURVE)
    t = np.linspace(0, 2*np.pi, 200)

    for i in range(blades):

        base_angle = i * (2*np.pi/blades) + speed_ctrl

        # realistic blade shape (simple engineering curve)
        x = np.cos(t) * (1 - t/(2*np.pi))
        y = np.sin(t) * (1 - t/(2*np.pi))
        z = 0.2 * np.sin(2*t)

        # rotation
        xr = x*np.cos(base_angle) - y*np.sin(base_angle)
        yr = x*np.sin(base_angle) + y*np.cos(base_angle)

        fig.add_trace(go.Scatter3d(
            x=xr,
            y=yr,
            z=z,
            mode='lines',
            line=dict(color="#00eaff", width=6)
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
    st.subheader("🌊 Flow Field Simulation")

    n = 70
    x = np.linspace(-2,2,n)
    y = np.linspace(-2,2,n)
    X, Y = np.meshgrid(x,y)

    R = np.sqrt(X**2 + Y**2) + 0.1
    U = -Y / R + np.sin(X)
    V = X / R + np.cos(Y)

    fig2, ax = plt.subplots()
    ax.streamplot(X, Y, U, V, color=np.sqrt(U**2+V**2), cmap="plasma")
    ax.set_title("Water Flow Simulation")
    st.pyplot(fig2)

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🚀 AI Marine Twin System")
st.markdown("👨‍💻 Mohamed Ashraf Hussein Desouky")
