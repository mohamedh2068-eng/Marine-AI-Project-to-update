import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعدادات الحماية والـ UI
st.set_page_config(page_title="M.AFixly Pro | Marine AI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #fbbf24; }
    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 30px; border-radius: 20px; border: 1px solid #334155; text-align: center; margin-bottom: 25px;
    }
    </style>
    <meta name="google" content="notranslate">
    """, unsafe_allow_html=True)

# 2. الهيدر (تحت إشراف أ.د/ حسين المصري)
st.markdown(f"""
    <div class="header-card">
        <h1 style='color: #fbbf24; margin:0;'>M.AFixly: Marine AI Platform</h1>
        <p style='color: white;'>جامعة شرق بورسعيد التكنولوجية | الطالب: محمد أشرف حسين</p>
        <p style='color: #fbbf24; font-weight: bold;'>تحت إشراف: أ.د/ حسين المصري</p>
    </div>
    """, unsafe_allow_html=True)

# 3. لوحة التحكم
with st.sidebar:
    st.header("⚙️ Configuration")
    d_m = st.slider("Propeller Diameter (m)", 0.5, 8.0, 3.0)
    v_k = st.slider("Speed (Knots)", 5, 60, 25)
    blades = st.select_slider("Number of Blades", options=[3, 4, 5, 6])
    st.info("AI Predictor Active")

# 4. التبويبات (إضافة الـ 3D هنا)
tab1, tab2, tab3 = st.tabs(["📊 Performance", "🎮 3D Simulation", "🤖 CNC Data"])

with tab1:
    eff = 0.84 - (v_k * 0.003)
    thrust = (d_m**2) * (v_k**1.2) * 0.4
    c1, c2, c3 = st.columns(3)
    c1.metric("Efficiency (η)", f"{eff*100:.1f}%")
    c2.metric("Thrust", f"{thrust:.2f} kN")
    c3.metric("Cavitation", "SAFE" if v_k < 35 else "RISK")
    
    # الرسم البياني
    j = np.linspace(0.1, 1.2, 30)
    kt = 0.5 - 0.3 * j
    fig = go.Figure(go.Scatter(x=j, y=kt, line=dict(color='#fbbf24', width=3)))
    fig.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 🧊 Interactive Propeller Model")
    # محاكي 3D مطور ومستقر جداً
    st.components.v1.html(f"""
    <div id="3d-area" style="width:100%; height:400px; background:#000; border-radius:15px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/400, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias: true, alpha: true}});
        renderer.setSize(document.getElementById('3d-area').clientWidth, 400);
        document.getElementById('3d-area').appendChild(renderer.domElement);

        const group = new THREE.Group();
        const mat = new THREE.MeshPhongMaterial({{ color: 0xfbbf24, shininess: 100 }});
        
        // رسم الريش ديناميكياً
        for(let i=0; i<{blades}; i++) {{
            const geom = new THREE.TorusGeometry(1.2, 0.3, 16, 100);
            const blade = new THREE.Mesh(geom, mat);
            blade.rotation.y = (i * Math.PI * 2) / {blades};
            group.add(blade);
        }}
        scene.add(group);
        
        const light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(5, 5, 5);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));
        camera.position.z = 5;

        function animate() {{
            requestAnimationFrame(animate);
            group.rotation.z += 0.02;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """, height=420)

with tab3:
    st.code(f"G01 X{d_m*10} Y0 Z-5 F200 \n(Generated for {blades} Blades)", language="gcode")

st.caption("M.AFixly System © 2026")
