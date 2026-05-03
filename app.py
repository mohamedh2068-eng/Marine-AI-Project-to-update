import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. إعدادات الصفحة الأساسية ومنع الترجمة
st.set_page_config(
    page_title="M.AFixly | Marine AI",
    page_icon="🚢",
    layout="wide"
)

# منع ترجمة جوجل التي تسببت في ظهور كلمة "الله" و "الضرب"
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

# 2. تصميم CSS احترافي (Modern Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif; }
    .main { background-color: #0b0f19; }
    
    /* تصميم الكروت */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* الهيدر الاحترافي */
    .hero-section {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 40px;
        border-radius: 20px;
        border-bottom: 5px solid #fbbf24;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .status-safe { color: #10b981; font-weight: bold; }
    .status-risk { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. الجزء العلوي (Hero Section) مع الصور
col_logo, col_text = st.columns([1, 4])

with col_text:
    st.markdown(f"""
        <div class="hero-section">
            <h1 style='color: #fbbf24;'>نظام الذكاء الاصطناعي لتصميم الرفاصات البحرية</h1>
            <h3 style='color: #ffffff;'>M.AFixly - Smart Marine Systems</h3>
            <p style='color: #94a3b8; font-size: 1.1em;'>جامعة شرق بورسعيد التكنولوجية | تكنولوجيا تشغيل وصيانة السفن</p>
            <hr style="border-color: rgba(255,255,255,0.1)">
            <div style="display: flex; justify-content: space-around; color: #e2e8f0;">
                <span>👤 <b>الطالب:</b> محمد أشرف حسين دسوقي</span>
                <span>👨‍🏫 <b>تحت إشراف:</b> أ.د/ حسين المصري</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 4. لوحة التحكم الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=100)
    st.title("⚙️ معايير التصميم")
    d_input = st.number_input("قطر الرفاص (D) بالمتر", 0.5, 10.0, 2.8)
    v_input = st.slider("سرعة السفينة (V) عقدة", 5, 50, 25)
    blades = st.select_slider("عدد الريش", options=[3, 4, 5, 6])
    st.info("يتم تحديث النموذج الـ 3D والنتائج فورياً بناءً على المدخلات.")

# 5. منطقة العرض الرئيسية (Main Display)
tab1, tab2, tab3 = st.tabs(["📈 تحليل الأداء", "🕹️ المحاكي الـ 3D", "🛠️ أكواد الـ CNC"])

with tab1:
    # حسابات برمجية (Mechanical Logic)
    efficiency = 0.82 - (v_input * 0.002)
    thrust = (d_input**2) * (v_input**1.5) * 0.4
    
    c1, c2, c3 = st.columns(3)
    c1.metric("كفاءة الرفاص (η)", f"{efficiency*100:.1f}%")
    c2.metric("قوة الدفع (kN)", f"{thrust:.2f}")
    
    # حل مشكلة كلمة "الله" الناتجة عن الترجمة الخاطئة لـ "Status"
    cav_status = "Safe / آمن" if v_input < 32 else "Risk / خطر كافيتيشن"
    c3.metric("الحالة الهيدروديناميكية", cav_status)

    # رسم بياني تفاعلي بـ Plotly
    st.markdown("### 📊 منحنى التنبؤ بالأداء")
    x = np.linspace(0.1, 1.2, 50)
    y = 0.6 - (0.4 * x**2)
    fig = go.Figure(data=go.Scatter(x=x, y=y, line=dict(color='#fbbf24', width=4), fill='tozeroy'))
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20), height=350)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 🧊 محاكاة الرفاص ثلاثية الأبعاد")
    # أنيميشن 3D باستخدام JavaScript (تم إصلاحه ليعمل رغم الترجمة)
    st.components.v1.html(f"""
    <div id="canvas-container" style="width:100%; height:450px; background:#000; border-radius:20px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/450, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias: true, alpha: true}});
        renderer.setSize(document.getElementById('canvas-container').clientWidth, 450);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        // إنشاء شكل رفاص مبسط (TorusKnot) لتمثيل الريش
        const geometry = new THREE.TorusKnotGeometry(1.5, 0.4, 100, {blades*2});
        const material = new THREE.MeshStandardMaterial({{ 
            color: 0xfbbf24, 
            metalness: 0.9, 
            roughness: 0.1 
        }});
        const propeller = new THREE.Mesh(geometry, material);
        scene.add(propeller);

        const light = new THREE.PointLight(0xffffff, 1.5, 100);
        light.position.set(10, 10, 10);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040, 2));

        camera.position.z = 5;

        function animate() {{
            requestAnimationFrame(animate);
            propeller.rotation.z += {v_input / 100}; // السرعة تؤثر على الدوران
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """, height=470)

with tab3:
    st.markdown("### ⚙️ توليد مسار الماكينة (G-Code Generater)")
    st.code(f"""
    (M.AFixly AI Generated G-Code)
    (Design for {blades} Blades)
    G21 ; Units in mm
    G90 ; Absolute positioning
    M03 S2500 ; Spindle ON
    G01 X0 Y0 Z5 F200
    (Propeller Edge Cutting)
    G02 X{d_input*10} Y5 R{d_input}
    M30 ; End Program
    """, language="gcode")

# 6. الفوتر (Footer)
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #64748b;'>تم التطوير بواسطة م/ محمد أشرف - 2026</p>", unsafe_allow_html=True)
