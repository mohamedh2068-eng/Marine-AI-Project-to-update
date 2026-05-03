import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="M.AFixly Mobile Pro", layout="wide")

# --- ستايل الموبايل ---
st.markdown("""
    <style>
    .main { background: #010409; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: #fbbf24; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚓ M.AFixly Mobile Simulation")

# --- لوحة التحكم ---
col_ctrl, col_view = st.columns([1, 2])

with col_ctrl:
    rpm = st.slider("Speed (RPM)", 0, 4000, 1500)
    blades = st.select_slider("Blades", options=[3, 4, 5])
    
    # زرار تفعيل الصوت (لازم تضغط عليه عشان المتصفح يوافق يشغل الصوت)
    if st.button("🔊 تشغيل محاكي الصوت"):
        st.write("🎵 المحرك يعمل الآن...")
        # كود لتشغيل صوت "طنين" ميكانيكي بسيط
        st.audio("https://www.soundjay.com/transportation/engine-hum-01.mp3")

# --- المحاكي الـ 4D المعدل (High Compatibility) ---
with col_view:
    st.subheader("🧊 Live 4D View")
    
    # استخدام نسخة مبسطة جداً لضمان التشغيل على أندرويد/آيفون
    st.components.v1.html(f"""
        <div id="container" style="width:100%; height:400px; background: #0d1117; border-radius: 15px;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth/400, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: false, alpha: true }}); // Antialias OFF for speed
            renderer.setSize(document.getElementById('container').clientWidth, 400);
            document.getElementById('container').appendChild(renderer.domElement);

            // إنشاء رفاص مبسط جداً (Box Blades) لضمان الحركة
            const group = new THREE.Group();
            const material = new THREE.MeshPhongMaterial({{ color: 0xfbbf24 }});
            
            for(let i=0; i<{blades}; i++) {{
                const geo = new THREE.BoxGeometry(2, 0.5, 0.1);
                const b = new THREE.Mesh(geo, material);
                b.rotation.z = (i * Math.PI * 2) / {blades};
                group.add(b);
            }}
            scene.add(group);
            scene.add(new THREE.PointLight(0xffffff, 1).position.set(5,5,5));
            camera.position.z = 5;

            function animate() {{
                requestAnimationFrame(animate);
                group.rotation.z += {rpm / 5000};
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    """, height=420)

# --- الرسم البياني للاهتزاز (ده بيشتغل على أي موبايل) ---
st.subheader("📊 Vibration Analysis")
x = np.linspace(0, 10, 100)
y = np.sin(x * (rpm/500)) 
fig = go.Figure(data=go.Scatter(x=x, y=y, line=dict(color='#fbbf24')))
fig.update_layout(template="plotly_dark", height=300)
st.plotly_chart(fig, use_container_width=True)
