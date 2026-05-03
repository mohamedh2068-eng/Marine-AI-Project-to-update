import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="M.AFixly - Marine AI Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS احترافي (Glass UI)
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
}
.block-container {
    padding-top: 2rem;
}
.stMetric {
    background: rgba(30, 41, 59, 0.7);
    padding: 15px;
    border-radius: 12px;
    border-bottom: 3px solid #fbbf24;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.header-box {
    text-align: center;
    padding: 25px;
    background: linear-gradient(90deg, #1e293b, #020617);
    border-radius: 15px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div class="header-box">
    <h1 style='color:#fbbf24;'>M.AFixly: Marine AI & Propeller System</h1>
    <p style='color:#94a3b8;'>AI + Hydrodynamics + CNC Integration</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("⚙️ Engineering Inputs")

    d_input = st.number_input("Diameter (m)", 0.5, 15.0, 2.5)
    v_input = st.slider("Speed (knots)", 5, 60, 22)
    blades = st.select_slider("Blades", options=[3, 4, 5, 6])

    ship_type = st.selectbox("Ship Type", ["Cargo", "Tanker", "Passenger"])

    material = st.selectbox("Material", [
        "Nickel-Alu Bronze",
        "Stainless Steel 316L",
        "Manganese Bronze"
    ])

# =========================
# AI Model (ML حقيقي)
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
tab1, tab2, tab3 = st.tabs([
    "📊 Performance",
    "🧊 3D Model",
    "📋 Report"
])

# =========================
# TAB 1
# =========================
with tab1:

    col1, col2, col3 = st.columns(3)

    col1.metric("Efficiency", f"{eff*100:.2f}%")
    col2.metric("Thrust", f"{thrust:.2f} kN")
    col3.metric("Efficiency Gap", f"{(0.9-eff)*100:.2f}%")

    # Alerts
    if v_input > 35:
        st.error("⚠ High Cavitation Risk")
    elif v_input > 28:
        st.warning("⚠ Moderate Risk")
    else:
        st.success("✅ Safe Operation")

    # صورة حقيقية
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/Ship_propeller.jpg",
        caption="Real Marine Propeller"
    )

    # منحنى الأداء
    st.subheader("Performance Curve")

    j = np.linspace(0.1, 1.0, 20)
    kt = 0.5 - 0.4 * j

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=j, y=kt, mode='lines+markers'))

    fig.update_layout(template="plotly_dark", height=400)

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2 (3D احترافي)
# =========================
with tab2:

    st.subheader("3D Propeller Simulation")

    theta = np.linspace(0, 2*np.pi, 100)
    z = np.linspace(-1, 1, 100)
    theta, z = np.meshgrid(theta, z)

    r = 1 + 0.3 * np.sin(blades * theta)

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])

    fig.update_layout(template="plotly_dark", height=500)

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:

    st.subheader("Project Report")

    st.write(f"""
    **Ship Type:** {ship_type}  
    **Material:** {material}  
    **Diameter:** {d_input} m  
    **Speed:** {v_input} knots  
    **Blades:** {blades}  

    ---
    **Efficiency:** {eff:.2f}  
    **Thrust:** {thrust:.2f} kN  
    """)

    # Export
    if st.button("Export Report"):
        with open("report.txt", "w") as f:
            f.write(f"""
M.AFixly Report

Ship Type: {ship_type}
Material: {material}
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
<p style='text-align:center;color:gray;'>
© 2026 M.AFixly Marine Systems
</p>
""", unsafe_allow_html=True)
