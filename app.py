import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- إعدادات الصفحة ---
st.set_page_config(page_title="M.AFixly | Marine Digital Twin", layout="wide")

# ستايل احترافي (Dark Navy & Gold)
st.markdown("""
    <style>
    .main { background-color: #020617; color: white; }
    .stMetric { background: #1e293b; border-radius: 10px; border-top: 4px solid #fbbf24; }
    </style>
    """, unsafe_allow_html=True)

# --- الهيدر (تحت إشراف د. حسين المصري) ---
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #fbbf24; padding: 20px; border-radius: 20px;">
        <h1 style="color: #fbbf24;">M.AFixly: AI Propeller & CNC System</h1>
        <p>جامعة شرق بورسعيد التكنولوجية | إعداد: <b>محمد أشرف حسين</b></p>
        <p>إشراف: <b>أ.د/ حسين المصري</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- لوحة التحكم (نفس فكرة الموقع اللي بعته) ---
with st.sidebar:
    st.header("🚢 تصنيف الأسطول")
    fleet_type = st.selectbox("اختار نوع السفينة", 
        ["سفن بضائع (Bulk Carrier)", "ناقلات نفط (Tankers)", "يخوت سريعة (Fast Yachts)", "غواصات (Submarines)"])
    
    st.header("📏 أبعاد الرفاص")
    diameter = st.slider("القطر (D - Meters)", 0.5, 8.0, 3.5)
    speed = st.slider("السرعة (V - Knots)", 5, 45, 18)
    blades = st.select_slider("عدد الريش (Blades)", options=[3, 4, 5, 6])
    
    st.divider()
    if st.button("🚀 توليد وتصنيع (Generate & CNC)"):
        st.toast("جاري معالجة البيانات بالذكاء الاصطناعي...")

# --- محرك الحسابات (AI Engine) ---
# حسابات تتغير بناءً على نوع السفينة
def calculate_propeller_logic(f_type, d, s, b):
    base_eff = 0.82
    if "Yachts" in f_type: base_eff = 0.88 # اليخوت أكفأ في السرعات العالية
    elif "Submarines" in f_type: base_eff = 0.78 # الغواصات تركز على الهدوء
    
    efficiency = base_eff - (s * 0.002) - (b * 0.005)
    thrust = (d**2.2) * (s**1.1) * 0.5
    return round(efficiency*100, 1), round(thrust, 2)

eff, thrust = calculate_propeller_logic(fleet_type, diameter, speed, blades)

# --- شاشة الماكينة والنتائج ---
col_stats, col_sim = st.columns([1, 2])

with col_stats:
    st.subheader("📟 CNC Status")
    st.metric("Efficiency", f"{eff}%")
    st.metric("Thrust Force", f"{thrust} kN")
    
    st.info(f"Target: {fleet_type}")
    
    # محاكاة كود الـ CNC بشكل حي
    st.markdown("**G-Code Stream:**")
    st.code(f"G01 X{diameter*10} Y0 Z-5\nG90 G21 F150\nM03 S1200\n(Blades: {blades})", language="gcode")

with col_sim:
    st.subheader("🧊 3D Digital Twin")
    
    # تحريك الرفاص (الخيار الثاني المطور)
    st.components.v1.html(f"""
        <div id="3d-div" style="width:100%; height:450px; background: #0f172a; border-radius: 15px;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 450, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(document.getElementById('3d-div').clientWidth, 450);
            document.getElementById('3d-div').appendChild(renderer.domElement);

            const group = new THREE.Group();
            // تغيير اللون بناءً على النوع (ذهبي للنحاس، فضي للاستانلس)
            const matColor = "{'#fbbf24' if 'Yachts' not in fleet_type else '#e2e8f0'}";
            const material = new THREE.MeshPhongMaterial({{ color: matColor, shininess: 100, side: THREE.DoubleSide }});
            
            for(let i=0; i<{blades}; i++) {{
                // تغيير شكل الريشة (TorusKnot كتمثيل فني للريشة)
                const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16, 1, {blades});
                const blade = new THREE.Mesh(geometry, material);
                blade.rotation.z = (i * Math.PI * 2) / {blades};
                group.add(blade);
            }}
            scene.add(group);
            scene.add(new THREE.PointLight(0xffffff, 1, 100).position.set(5,5,5) && new THREE.AmbientLight(0x404040));
            camera.position.z = 4;

            function animate() {{
                requestAnimationFrame(animate);
                group.rotation.z += {speed / 1000}; // السرعة مرتبطة بالواقع
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    """, height=470)

st.markdown("---")
st.caption("M.AFixly System v2.0 - Developed for Port Said Technological University")
