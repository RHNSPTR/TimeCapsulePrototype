import streamlit as st
import time
import os
import base64

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Time Capsule AI",
    page_icon="🕰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

VIDEO_FOLDER = "generated_videos"

# =========================================================
# SESSION STATE
# =========================================================
if "generated" not in st.session_state:
    st.session_state.generated = False
if "video_path" not in st.session_state:
    st.session_state.video_path = None

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* ---------- FONT ---------- */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, .hero-title {
    font-family: 'Space Grotesk', sans-serif;
}

/* ---------- HIDE STREAMLIT DEFAULT CHROME ---------- */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ---------- AURORA BACKGROUND ---------- */
.stApp {
    background: #0b0c14;
    background-image:
        radial-gradient(at 15% 20%, rgba(124, 58, 237, 0.35) 0px, transparent 50%),
        radial-gradient(at 85% 10%, rgba(56, 189, 248, 0.30) 0px, transparent 50%),
        radial-gradient(at 50% 80%, rgba(236, 72, 153, 0.25) 0px, transparent 50%),
        radial-gradient(at 90% 90%, rgba(16, 185, 129, 0.20) 0px, transparent 50%);
    background-attachment: fixed;
    animation: auroraShift 18s ease-in-out infinite alternate;
}

@keyframes auroraShift {
    0%   { filter: hue-rotate(0deg) brightness(1); }
    50%  { filter: hue-rotate(15deg) brightness(1.05); }
    100% { filter: hue-rotate(-10deg) brightness(1); }
}

/* ---------- HERO SECTION ---------- */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 2rem 1rem;
}
.hero-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: #c9c9e8;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    line-height: 1.1;
    margin: 0.4rem 0 1rem 0;
    background: linear-gradient(90deg, #ffffff 0%, #b9b6ff 45%, #7dd3fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.08rem;
    color: #a3a3c2;
    max-width: 620px;
    margin: 0 auto;
    font-weight: 300;
    line-height: 1.6;
}
.hero-divider {
    width: 100%;
    height: 1px;
    margin: 2.2rem 0 2rem 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
}

/* ---------- GLASS CARD ---------- */
.glass-card {
    background: rgba(255, 255, 255, 0.045);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 20px;
    padding: 1.6rem 1.6rem 1.8rem 1.6rem;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    height: 100%;
    margin-bottom: 1.2rem;
}
.card-label {
    font-size: 0.72rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #8b8bb8;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #f2f2fb;
    margin-bottom: 1rem;
}

/* ---------- FILE UPLOADER OVERRIDE (drag & drop look) ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(167, 139, 250, 0.45) !important;
    border-radius: 16px !important;
    transition: all 0.25s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(167, 139, 250, 0.9) !important;
    background: rgba(167, 139, 250, 0.06) !important;
}
[data-testid="stFileUploader"] section {
    background: transparent !important;
}
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span {
    color: #a3a3c2 !important;
}

/* ---------- PREVIEW IMAGE ---------- */
.preview-frame {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.12);
    margin-top: 0.8rem;
}
.preview-frame img {
    width: 100%;
    display: block;
}

/* ---------- TIMELINE ---------- */
.timeline-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 8px 0;
    font-size: 0.92rem;
    color: #6f6f95;
    transition: all 0.3s ease;
}
.timeline-item.active {
    color: #f2f2fb;
}
.timeline-dot {
    width: 20px;
    height: 20px;
    min-width: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    border: 1.5px solid rgba(255,255,255,0.18);
    color: #6f6f95;
    background: rgba(255,255,255,0.03);
}
.timeline-item.active .timeline-dot {
    background: linear-gradient(135deg, #7c3aed, #38bdf8);
    border-color: transparent;
    color: white;
    box-shadow: 0 0 14px rgba(124,58,237,0.55);
}

/* ---------- GENERATE BUTTON ---------- */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed 0%, #6366f1 50%, #38bdf8 100%);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    box-shadow: 0 6px 22px rgba(124, 58, 237, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(56, 189, 248, 0.4);
    color: white;
    border: none;
}
div.stButton > button:active {
    transform: translateY(0px);
}

/* ---------- STATUS PILL ---------- */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34d399;
}
.status-pulse {
    width: 7px; height: 7px; border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px #34d399;
    animation: pulse 1.4s infinite;
}
@keyframes pulse {
    0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; }
}

/* ---------- SECTION TITLE ---------- */
.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f2f2fb;
    margin: 2.4rem 0 0.3rem 0;
    text-align: center;
}
.section-sub {
    text-align: center;
    color: #8b8bb8;
    font-size: 0.92rem;
    margin-bottom: 1.6rem;
}

/* ---------- VIDEO FRAME ---------- */
.video-frame {
    border-radius: 22px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 14px 50px rgba(0,0,0,0.5);
    padding: 10px;
    background: rgba(255,255,255,0.03);
}

/* ---------- STAT CARDS ---------- */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 1.6rem;
}
.stat-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 1.1rem 1rem;
    text-align: center;
    backdrop-filter: blur(14px);
}
.stat-icon { font-size: 1.3rem; margin-bottom: 0.3rem; }
.stat-label {
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b8bb8;
    margin-bottom: 0.2rem;
}
.stat-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: #f2f2fb;
}

/* ---------- FOOTER ---------- */
.footer-wrap {
    text-align: center;
    margin-top: 3.5rem;
    padding-top: 1.8rem;
    border-top: 1px solid rgba(255,255,255,0.08);
    color: #6f6f95;
    font-size: 0.85rem;
    line-height: 1.9;
}
.footer-wrap b { color: #a3a3c2; }

/* ---------- RESPONSIVE ---------- */
@media (max-width: 768px) {
    .hero-title { font-size: 2.1rem; }
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    st.info("Tampilan antarmuka untuk proyek Time Capsule. Pemrosesan video asli dilakukan secara terpisah melalui Google AI Studio.")
    st.markdown("---")
    st.write("📁 **Direktori Output:**")
    st.code(f"{VIDEO_FOLDER}/")
    st.markdown("---")
    if st.button("🔄 Reset Sesi"):
        st.session_state.generated = False
        st.session_state.video_path = None
        st.rerun()

# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🕰️ AI Video Generation Prototype</div>
    <div class="hero-title">Time Capsule AI</div>
    <div class="hero-sub">
        Transform a single portrait into a cinematic journey through time —
        powered by Google AI Studio.
    </div>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# =========================================================
# UPLOAD + AI PROCESSING SECTION
# =========================================================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Step 01</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📤 Upload Portrait</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Seret & lepas foto Anda di sini, atau klik untuk memilih",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.markdown('<div class="preview-frame">', unsafe_allow_html=True)
        st.image(uploaded_file, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(f"📎 {uploaded_file.name}")
    else:
        st.caption("Format didukung: JPG, JPEG, PNG")

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Step 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🤖 AI Processing</div>', unsafe_allow_html=True)

    timeline_steps = [
        "Upload Image",
        "Analyze Portrait",
        "Generate Prompt",
        "Google AI Studio",
        "Render Video",
        "Complete"
    ]

    timeline_placeholder = st.empty()

    def render_timeline(active_index=-1):
        """active_index = -1 artinya belum ada yang aktif."""
        html = ""
        for i, step in enumerate(timeline_steps):
            is_active = i <= active_index
            cls = "timeline-item active" if is_active else "timeline-item"
            icon = "✓" if i < active_index else ("●" if i == active_index else "")
            html += f"""
            <div class="{cls}">
                <div class="timeline-dot">{icon}</div>
                <div>{step}</div>
            </div>
            """
        timeline_placeholder.markdown(html, unsafe_allow_html=True)

    render_timeline(-1)

    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("✨ Generate Cinematic Video", type="primary", disabled=(uploaded_file is None))

    status_placeholder = st.empty()
    if not st.session_state.generated:
        status_placeholder.markdown(
            '<span class="status-pill">⏳ Menunggu input</span>', unsafe_allow_html=True
        )
    else:
        status_placeholder.markdown(
            '<span class="status-pill"><span class="status-pulse"></span> Completed</span>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PROSES GENERATE (SIMULASI)
# =========================================================
if generate_clicked and uploaded_file is not None:
    for i in range(len(timeline_steps)):
        render_timeline(i)
        status_placeholder.markdown(
            f'<span class="status-pill"><span class="status-pulse"></span> {timeline_steps[i]}...</span>',
            unsafe_allow_html=True
        )
        time.sleep(0.9 if i < len(timeline_steps) - 1 else 0.4)

    render_timeline(len(timeline_steps))
    status_placeholder.markdown(
        '<span class="status-pill"><span class="status-pulse"></span> Completed</span>',
        unsafe_allow_html=True
    )

    # Cek video di folder output
    if os.path.exists(VIDEO_FOLDER):
        videos = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(('.mp4', '.mov', '.avi'))]
        if videos:
            st.session_state.video_path = os.path.join(VIDEO_FOLDER, videos[0])
            st.session_state.generated = True
        else:
            st.session_state.generated = False
            st.warning(f"Belum ada file video di dalam folder `{VIDEO_FOLDER}`. Silakan masukkan hasil video dari AI Studio ke folder tersebut terlebih dahulu.")
    else:
        st.session_state.generated = False
        st.error(f"Folder `{VIDEO_FOLDER}` tidak ditemukan. Pastikan Anda berada di direktori yang benar saat menjalankan Streamlit.")

    st.rerun()

# =========================================================
# VIDEO OUTPUT SECTION
# =========================================================
if st.session_state.generated and st.session_state.video_path:
    st.markdown('<div class="section-title">🎬 Generated Time Capsule</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Hasil video Anda siap ditonton</div>', unsafe_allow_html=True)

    st.markdown('<div class="video-frame">', unsafe_allow_html=True)
    st.video(st.session_state.video_path)
    st.markdown('</div>', unsafe_allow_html=True)

    # Stat cards
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-icon">🧠</div>
            <div class="stat-label">AI Engine</div>
            <div class="stat-value">Google AI Studio</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-label">Status</div>
            <div class="stat-value">Completed</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📁</div>
            <div class="stat-label">Output</div>
            <div class="stat-value">{VIDEO_FOLDER}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🎞️</div>
            <div class="stat-label">Resolution</div>
            <div class="stat-value">HD Video</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-wrap">
    Powered by <b>Google AI Studio</b><br>
    Time Capsule Prototype — <b>Universitas Mercu Buana</b>
</div>
""", unsafe_allow_html=True)