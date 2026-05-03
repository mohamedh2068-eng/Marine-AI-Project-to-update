import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import random

# ================= PAGE =================
st.set_page_config(page_title="AI Marine Pro System", layout="wide")

# ================= INTRO =================
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:

    st.title("🚢 AI Marine Propeller Optimization PRO")

    st.image(
        "https://images.unsplash.com/photo-1548574505-5e239809ee19",
        use_container_width=True
    )

    st.markdown("""
    ### 👨‍🎓 محمد أشرف حسين دسوقي  
    ### 🏫 جامعة شرق بورسعيد التكنولوجية  
    ### 🧭 قسم تكنولوجيا تشغيل وصيانة السفن  
    ### 🎓 إشراف: د. حسين المصري  
    """)

    if st.button("🚀 Enter AI System"):
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

model = RandomForestRegressor(n_estimators=400, random_state=42)
model.fit(X_scaled, y)

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Control Panel")

speed = st.sidebar.slider("Ship Speed", 5, 50, 20)
blades = st.sidebar.selectbox("Blades", [3,4,5,6])
diameter = st.sidebar.slider("Diameter", 0.5, 10.0, 2.0)
rpm = st.sidebar.slider("RPM", 100, 3000, 1500)

# ================= GENERATE 10 DESIGNS =================
st.header("🧠 AI Multi-Design Optimization Engine")

designs = []

for i in range(10):

    d = diameter + random.uniform(-0.5, 0.5)
    s = speed + random.uniform(-7, 7)
    b = blades
    r = rpm + random.randint(-300, 300)

    inp = scaler.transform([[d, s, b, r]])
    eff = model.predict(inp)[0]

    score = eff * 0.6 + (1 - abs(s-20)/50)*0.2 + (d/10)*0.2

    designs.append({
        "id": i,
        "diameter": d,
        "speed": s,
        "blades": b,
        "rpm": r,
        "eff": eff,
        "score": score
    })

best = max(designs, key=lambda x: x["score"])

st.success("🏆 Best AI-Optimized Design Selected")

col1, col2, col3 = st.columns(3)

col1.metric("Efficiency", f"{best['eff']*100:.2f}%")
col2.metric("Score", f"{best['score']:.3f}")
col3.metric("RPM", best["rpm"])

# ================= COMPARISON TABLE =================
st.subheader("📊 AI Design Comparison")

for d in designs:
    st.write(f"Design {d['id']} → Efficiency: {d['eff']*100:.2f}% | Score: {d['score']:.3f}")

# ================= 3D =================
st.header("🧊 Advanced 3D Visualization")

theta = np.linspace(0, 2*np.pi, 120)
r = np.linspace(0.2, 1.2, 120)
theta, r = np.meshgrid(theta, r)

fig = go.Figure()

for i in range(best["blades"]):

    angle = i * 2*np.pi/best["blades"]

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    blade = np.sin(theta * 2) * (1 - r)
    z = 0.3 * blade

    xr = x*np.cos(angle) - y*np.sin(angle)
    yr = x*np.sin(angle) + y*np.cos(angle)

    fig.add_trace(go.Surface(
        x=xr,
        y=yr,
        z=z,
        colorscale="Turbo",
        showscale=False,
        opacity=0.9
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

# ================= FLOW =================
st.header("🌊 Flow Field Simulation")

n = 60
x = np.linspace(-2,2,n)
y = np.linspace(-2,2,n)
X, Y = np.meshgrid(x,y)

R = np.sqrt(X**2 + Y**2) + 0.1
U = -Y / R + np.sin(X)
V = X / R + np.cos(Y)

fig2, ax = plt.subplots()
ax.streamplot(X, Y, U, V, color=np.sqrt(U**2+V**2), cmap="plasma")
ax.set_title("Hydrodynamic Flow Field")
st.pyplot(fig2)

# ================= REPORT =================
st.header("📄 AI Report Summary")

st.code(f"""
AI MARINE OPTIMIZATION REPORT

Best Design ID: {best['id']}
Efficiency: {best['eff']*100:.2f}%
Score: {best['score']:.3f}

Parameters:
- Diameter: {best['diameter']:.2f}
- Speed: {best['speed']:.2f}
- Blades: {best['blades']}
- RPM: {best['rpm']}

Conclusion:
AI selected optimal marine propeller configuration
based on multi-variable engineering analysis.
""")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🚀 AI Marine Engineering Pro System")
st.markdown("👨‍💻 Mohamed Ashraf Hussein Desouky")
