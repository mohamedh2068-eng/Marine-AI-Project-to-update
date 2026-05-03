import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import random

# ================= PAGE =================
st.set_page_config(page_title="AI Marine Twin FINAL BOSS", layout="wide")

st.title("⚓ AI Marine Propeller Final Boss System")
st.markdown("### 👨‍💻 Mohamed Ashraf Hussein Desouky")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #020617, #000);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ================= BASE DATA =================
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

# ================= INPUT =================
diameter = st.slider("Diameter", 0.5, 10.0, 2.0)
speed = st.slider("Speed", 5, 50, 20)
blades = st.selectbox("Blades", [3,4,5,6])
pitch = st.slider("Pitch", 0.1, 3.0, 1.2)
rpm = st.slider("RPM", 100, 3000, 1500)

inp = scaler.transform([[diameter, speed, blades, rpm]])
eff = model.predict(inp)[0]

st.metric("⚡ Efficiency Score", f"{eff*100:.2f}%")

# ================= GENETIC OPTIMIZATION =================
st.subheader("🧬 AI Optimization Engine")

def fitness(x):
    d, s, b, r = x
    return model.predict(scaler.transform([[d,s,b,r]]))[0]

def random_design():
    return [
        random.uniform(0.5,5),
        random.uniform(5,50),
        random.choice([3,4,5,6]),
        random.uniform(500,2500)
    ]

population = [random_design() for _ in range(20)]

for _ in range(10):
    population = sorted(population, key=fitness, reverse=True)
    best = population[:5]

    new_pop = best.copy()
    while len(new_pop) < 20:
        p1, p2 = random.sample(best, 2)
        child = [
            (p1[0]+p2[0])/2,
            (p1[1]+p2[1])/2,
            random.choice([p1[2], p2[2]]),
            (p1[3]+p2[3])/2
        ]
        new_pop.append(child)

    population = new_pop

best_design = population[0]

st.success("🏆 Best AI Design Found")
st.write(f"Diameter: {best_design[0]:.2f}")
st.write(f"Speed: {best_design[1]:.2f}")
st.write(f"Blades: {best_design[2]}")
st.write(f"RPM: {best_design[3]:.0f}")

# ================= 3D MODEL =================
st.subheader("🧊 Advanced Propeller Model")

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

# ================= FLOW FIELD =================
st.subheader("🌊 Advanced Flow Simulation")

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

# ================= SYNTHETIC DATA =================
st.subheader("🖼️ AI Synthetic Vision Engine")

mode = st.selectbox("Simulation Mode", ["Cavitation", "Pressure Field", "Wake Turbulence"])

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
st.markdown("### 🚀 FINAL BOSS SYSTEM COMPLETED")
st.markdown("👨‍💻 Designed by: Mohamed Ashraf Hussein Desouky")
