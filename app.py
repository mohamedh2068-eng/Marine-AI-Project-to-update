import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="M.AFixly - Marine AI Pro", layout="wide")

# =========================
# CSS احترافي
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
}
.header-box {
    text-align:center;
    padding:30px;
    border-radius:20px;
    background: linear-gradient(135deg, #1e293b, #020617);
    box-shadow: 0 0 30px rgba(251,191,36,0.2);
    margin-bottom:20px;
}
.stMetric {
    backdrop-filter: blur(12px);
    background: rgba(30,41,59,0.6);
    border-radius:15px;
    padding:20px;
    border:1px solid rgba(255,255,255,0.1);
}
button {
    border-radius:10px !important;
    background: linear-gradient(90deg,#fbbf24,#f59e0b) !important;
    color:black !important;
    font-weight:bold !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div class="header-box">
    <h1 style='color:#fbbf24;'>⚓ M.AFixly Marine AI System</h1>
    <p style='color:#94a3b8;'>AI + Hydrodynamics + CNC Integration</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("⚙️ Inputs")

    d_input = st.number_input("Diameter (m)", 0.5, 15.0, 2.5)
    v_input = st.slider("Speed (knots)", 5, 60, 22)
    blades = st.select_slider("Blades", options=[3, 4, 5, 6])
    pitch = st.slider("Blade Pitch", 0.1, 2.0, 1.0)

    ship_type = st.selectbox("Ship Type", ["Cargo", "Tanker", "Passenger"])

# =========================
# AI Model
# =========================
X = np.array([
    [2.5, 22, 4],
    [3.0, 25, 5],
    [2.0, 18, 3],
    [2.8, 30, 4]
])
y = np.array([0.75, 0.72, 0.80, 0.70])

model = LinearRegression().fit(X, y)
eff = model.predict([[d_input, v_input, blades]])[0]

# =========================
# حسابات
# =========================
v_ms = v_input * 0.5144
thrust = (d_input**2) * (v_ms**2) * 0.55

# =========================
# Tabs
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Performance", "🧊 3D Model", "📋 Report"])

# =========================
# TAB 1
# =========================
with tab1:

    col1, col2, col3 = st.columns(3)
    col1.metric("Efficiency", f"{eff*100:.2f}%")
    col2.metric("Thrust", f"{thrust:.2f} kN")
    col3.metric("Efficiency Gap", f"{(0.9-eff)*100:.2f}%")

    if v_input > 35:
        st.error("⚠ High Cavitation Risk")
    elif v_input > 28:
        st.warning("⚠ Moderate Risk")
    else:
        st.success("✅ Safe Operation")

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/Ship_propeller.jpg",
        caption="Real Marine Propeller"
    )

    st.subheader("Performance Curve")

    j = np.linspace(0.1, 1.0, 20)
    kt = 0.5 - 0.4 * j

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=j, y=kt, mode='lines+markers'))
    fig.update_layout(template="plotly_dark", height=400)

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2 (3D واقعي)
# =========================
with tab2:

    st.subheader("⚓ Realistic 3D Propeller")

    theta = np.linspace(0, 2*np.pi, 50)
    radius = np.linspace(0.2, 1, 50)
    theta, radius = np.meshgrid(theta, radius)

    twist = radius * 2

    x = radius * np.cos(theta + twist)
    y = radius * np.sin(theta + twist)
    z = pitch * np.sin(3 * theta) * (1 - radius)

    fig = go.Figure()

    # لون معدني
    colorscale = [[0, "#999"], [1, "#fbbf24"]]

    # الريشة الأساسية
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=colorscale, showscale=False))

    # باقي الريش
    for i in range(blades):
        angle = (i * 2 * np.pi) / blades
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)

        fig.add_trace(go.Surface(
            x=x_rot, y=y_rot, z=z,
            colorscale=colorscale,
            showscale=False
        ))

    # الهَب (المحور)
    z_hub = np.linspace(-0.5, 0.5, 20)
    theta_hub = np.linspace(0, 2*np.pi, 20)
    theta_hub, z_hub = np.meshgrid(theta_hub, z_hub)

    x_hub = 0.2 * np.cos(theta_hub)
    y_hub = 0.2 * np.sin(theta_hub)

    fig.add_trace(go.Surface(
        x=x_hub, y=y_hub, z=z_hub,
        colorscale=colorscale,
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

# =========================
# TAB 3
# =========================
with tab3:

    st.subheader("📋 Project Report")

    st.write(f"""
    **Ship Type:** {ship_type}  
    **Diameter:** {d_input} m  
    **Speed:** {v_input} knots  
    **Blades:** {blades}  

    ---
    **Efficiency:** {eff:.2f}  
    **Thrust:** {thrust:.2f} kN  
    """)

    if st.button("Export Report"):
        with open("report.txt", "w") as f:
            f.write(f"""
M.AFixly Report

Ship Type: {ship_type}
Diameter: {d_input}
Speed: {v_input}
Blades: {blades}

Efficiency: {eff}
Thrust: {thrust}
""")
        st.success("Report Saved Successfully!")

# =========================
# Footer
# =========================
st.markdown("""
<hr>
<p style='text-align:center;color:gray;'>© 2026 M.AFixly Marine Systems</p>
""", unsafe_allow_html=True)
