import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import random

# ================= PAGE =================
st.set_page_config(page_title="Marine AI Cinema System", layout="wide")

# ================= CINEMATIC INTRO =================
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:

    st.markdown("<h1 style='text-align:center;'>⚓ Marine AI Propeller System</h1>", unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1581091215367-59ab6c0a5f7e",
        use_container_width=True
    )

    st.markdown("""
<div style='text-align:center; font-size:18px;'>
👨‍💻 محمد أشرف حسين دسوقي  
<br>
🏫 جامعة شرق بورسعيد التكنولوجية  
<br>
🧭 قسم تكنولوجيا تشغيل وصيانة السفن  
<br>
🎓 إشراف: د. حسين المصري  
</div>
""", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;color:#00e5ff;'>AI Engineering Decision & Simulation System</h3>", unsafe_allow_html=True)

    if st.button("▶ START EXPERIENCE"):
        st.session_state.start = True
        st.rerun()

    st.stop()

# ================= AI ENGINE =================
X = np.array([
    [1.5, 15, 4, 1200],
    [2.0, 20, 5, 1500],
    [1.2, 10, 3, 1000],
    [3.0, 30, 6, 2000],
    [2.5, 25, 5, 1800],
])

y = np.array([0.72, 0.70, 0.78, 0.85, 0.88])

scaler = StandardScaler()
X = scaler.fit_transform(X)

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X, y)

# ================= CONTROL =================
st.sidebar.title("⚙ Control Panel")

speed = st.sidebar.slider("Ship Speed", 5, 50, 20)
blades = st.sidebar.selectbox("Blade Count", [3,4,5,6])
diameter = st.sidebar.slider("Diameter", 0.5, 10.0, 2.0)
rpm = st.sidebar.slider("RPM", 100, 3000, 1500)

# ================= AI GENERATION =================
st.header("🧠 AI Optimization Core")

designs = []

for i in range(10):

    d = diameter + random.uniform(-0.4, 0.4)
    s = speed + random.uniform(-5, 5)
    b = blades
    r = rpm + random.randint(-200, 200)

    inp = scaler.transform([[d, s, b, r]])
    eff = model.predict(inp)[0]

    score = eff * 0.7 + (1 - abs(s-20)/50)*0.3

    designs.append({
        "id": i,
        "d": d,
        "s": s,
        "b": b,
        "r": r,
        "eff": eff,
        "score": score
    })

best = max(designs, key=lambda x: x["score"])

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

col1.metric("⚡ Efficiency", f"{best['eff']*100:.2f}%")
col2.metric("🏆 AI Score", f"{best['score']:.3f}")
col3.metric("🔄 RPM", best["r"])

# ================= CINEMATIC SIMULATION =================
st.header("🌊 Real-Time Propeller Simulation")

t = np.linspace(0, 2*np.pi, 200)

fig = go.Figure()

# WATER (smooth cinematic layer)
wx = np.linspace(-2,2,30)
wy = np.linspace(-2,2,30)
WX, WY = np.meshgrid(wx,wy)
WZ = np.sin(WX*2) * 0.05 + np.cos(WY*2)*0.05 - 0.5

fig.add_trace(go.Surface(
    x=WX,
    y=WY,
    z=WZ,
    colorscale=[[0,"#0f172a"],[1,"#0ea5e9"]],
    opacity=0.65,
    showscale=False
))

# PROPELLER MOTION
for i in range(best["b"]):

    angle = i * (2*np.pi/best["b"])

    x = np.cos(t) * (1 - t/(2*np.pi))
    y = np.sin(t) * (1 - t/(2*np.pi))
    z = 0.3 * np.sin(3*t)

    xr = x*np.cos(angle) - y*np.sin(angle)
    yr = x*np.sin(angle) + y*np.cos(angle)

    fig.add_trace(go.Scatter3d(
        x=xr,
        y=yr,
        z=z,
        mode='lines',
        line=dict(color="#00ffff", width=5)
    ))

fig.update_layout(
    template="plotly_dark",
    height=720,
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
    )
)

st.plotly_chart(fig, use_container_width=True)

# ================= REPORT =================
st.header("📄 AI Engineering Report")

st.code(f"""
MARINE AI CINEMATIC SYSTEM REPORT
----------------------------------

Best Design ID: {best['id']}

Performance:
- Efficiency: {best['eff']*100:.2f}%
- AI Score: {best['score']:.3f}

Configuration:
- Diameter: {best['d']:.2f} m
- Speed: {best['s']:.2f} knots
- Blades: {best['b']}
- RPM: {best['r']}

System Result:
✔ AI optimized marine propeller design
✔ Real-time hydrodynamic simulation
✔ Engineering decision support output

Status: CINEMATIC DEMO READY
""")

# ================= FOOTER =================
st.markdown("---")
st.markdown("<h4 style='text-align:center;'>⚓ Marine AI Cinematic System</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>👨‍💻 Mohamed Ashraf Hussein Desouky</p>", unsafe_allow_html=True)
