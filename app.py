import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Cinematic Theme Configuration ---
st.set_page_config(page_title="M.AFixly | Industrial Twin", layout="wide")

st.markdown("""
    <style>
    .main { background: #010409; color: #e6edf3; }
    .stMetric { border-radius: 12px; background: #0d1117; border-top: 4px solid #fbbf24; }
    .status-box { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div style="text-align: center; padding: 25px; border-bottom: 1px solid #30363d;">
        <h1 style="color: #fbbf24; font-size: 3em; margin: 0;">M.AFIXLY: QUANTUM PROPULSION</h1>
        <p style="color: #8b949e; letter-spacing: 3px;">ADVANCED AI VIBRATION & DESIGN ENGINE</p>
        <div style="display: flex; justify-content: center; gap: 40px; margin-top: 15px;">
            <span>👨‍💻 Eng: <b>Mohamed Ashraf</b></span>
            <span>🏫 Dept: <b>Ship Maintenance & Ops</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Pro Side Panel ---
with st.sidebar:
    st.header("💎 Premium Controls")
    design_type = st.radio("Blade Geometry", ["Standard (Kaplan)", "High Skew (Silent)", "Symmetric"])
    diameter = st.slider("Propeller Diameter (m)", 0.5, 12.0, 5.5)
    rpm = st.slider("Rotational Speed (RPM)", 0, 5000, 1800)
    fluid_density = st.select_slider("Fluid Density", options=[1000, 1025, 1030], value=1025)
    
    st.divider()
    st.write("🔧 **CNC Pathing:** Auto-Sync Enabled")
    st.write("📡 **AI Diagnostics:** Real-time Monitoring")

# --- AI & Physics Core (Vibration & Acoustics) ---
def compute_quantum_metrics(d, r, b_type):
    # حساب التردد والاهتزازات
    frequency = (rpm / 60) * 4 # Blade passing frequency
    vibration_level = (rpm**1.5 * d) / 1000000
    
    # الكفاءة بناءً على نوع التصميم
    eff_map = {"Standard (Kaplan)": 0.78, "High Skew (Silent)": 0.84, "Symmetric": 0.72}
    efficiency = eff_map[b_type] - (rpm * 0.00002)
    
    return round(efficiency*100, 1), round(vibration_level, 2), round(frequency, 1)

eff, vib, freq = compute_quantum_metrics(diameter, rpm, design_type)

# --- Dashboard Layout ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Efficiency", f"{eff}%")
col2.metric("Vibration (G)", vib)
col3.metric("Pass Frequency", f"{freq} Hz")
col4.metric("AI Prediction", "STABLE" if vib < 0.5 else "CRITICAL", delta_color="inverse")

# --- Interactive 3D & Vibration Radar ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown("### 🧊 4D Digital Twin Simulation")
    # المحاكي المتحرك مع تأثير "الإضاءة الديناميكية"
    st.components.v1.html(f"""
        <div id="sim" style="width:100%; height:550px; background: radial-gradient(circle, #1e293b 0%, #010409 100%); border-radius: 20px;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 550, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(document.getElementById('sim').clientWidth, 550);
            document.getElementById('sim').appendChild(renderer.domElement);

            const group = new THREE.Group();
            const material = new THREE.MeshStandardMaterial({{ 
                color: { '0xff3333' if vib > 0.5 else '0xfbbf24' }, 
                metalness: 1, roughness: 0.2 
            }});
            
            // رسم رفاص بشكل حقيقي (Fan Shape)
            const hub = new THREE.Mesh(new THREE.SphereGeometry(0.6, 32, 32), material);
            group.add(hub);
            
            for(let i=0; i<4; i++) {{
                const bladeGeom = new THREE.TorusKnotGeometry(1.2, 0.4, 64, 8, 2, 3);
                const blade = new THREE.Mesh(bladeGeom, material);
                blade.rotation.z = (i * Math.PI * 2) / 4;
                blade.scale.set({diameter/5}, {diameter/5}, 0.2);
                group.add(blade);
            }}
            
            scene.add(group);
            scene.add(new THREE.PointLight(0xffffff, 2, 50).position.set(5,5,5));
            scene.add(new THREE.AmbientLight(0x404040, 2));
            camera.position.z = 5;

            function animate() {{
                requestAnimationFrame(animate);
                // سرعة الدوران والاهتزاز مربوطة بالـ RPM
                group.rotation.z += {rpm / 10000};
                if({vib} > 0.5) {{
                    group.position.x = Math.sin(Date.now() * 0.05) * 0.05; // تأثير الاهتزاز
                }}
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    """, height=570)

with c_right:
    st.markdown("### 📡 Acoustic Signature")
    # رسم بياني للموجات الصوتية (Mock Sound Wave)
    x = np.linspace(0, 10, 100)
    y = np.sin(x * freq * 0.1) * vib
    fig_sound = go.Figure(data=go.Scatter(x=x, y=y, line=dict(color='#fbbf24', width=3)))
    fig_sound.update_layout(template="plotly_dark", height=250, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
    st.plotly_chart(fig_sound, use_container_width=True)
    
    st.markdown("### 🛠️ CNC Tool Path")
    st.code(f"G01 X{diameter*10} Z-5\nF{rpm/10}\nM03 S{rpm}", language="gcode")

# --- AI Diagnostics Report ---
st.markdown("""<div class="status-box">""", unsafe_allow_html=True)
st.subheader("🤖 AI Technical Diagnosis")
if vib > 0.5:
    st.error(f"CRITICAL VIBRATION: {vib}G detected at {rpm} RPM. Structural fatigue risk is high.")
else:
    st.success("STABLE OPERATION: Harmonics are within safe limits. Optimal efficiency achieved.")
st.markdown("</div>", unsafe_allow_html=True)
