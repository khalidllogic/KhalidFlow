import streamlit as st
import os
import time

# 0. Cloud Matrix JSON Reconstructor
import json
if "YOUTUBE_CLIENT_SECRET" in st.secrets and not os.path.exists("client_secret.json"):
    with open("client_secret.json", "w", encoding="utf-8") as f:
        f.write(st.secrets["YOUTUBE_CLIENT_SECRET"])

if "YOUTUBE_TOKEN" in st.secrets and not os.path.exists("token.json"):
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(st.secrets["YOUTUBE_TOKEN"])

from khalid_core import upload_to_cloud_buffer, publish_to_instagram, publish_to_facebook
from youtube_uploader import upload_video_to_youtube

# Page Config MUST be first
st.set_page_config(page_title="KhalidFlow | Matrix", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# 1. إدارة الجلسة للتبديل بين الصفحات
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

def enter_dashboard():
    st.session_state.page = 'dashboard'

# 2. حقن CSS عميق - نمط Glassmorphism & Cyberpunk
st.markdown("""
    <style>
    /* استدعاء خط مستقبلي من جوجل */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700;900&display=swap');
    
    * { font-family: 'Space Grotesk', sans-serif !important; }
    
    /* إخفاء هوية Streamlit بالكامل */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* خلفية الفضاء العميق مع إضاءات نيون مشعة */
    .stApp {
        background-color: #030712;
        background-image: 
            radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
        color: #f3f4f6;
    }

    /* نص الشاشة الترحيبية - أنيميشن يلمع */
    .hero-title {
        font-size: 7rem; font-weight: 900; text-align: center; margin-bottom: -15px;
        background: linear-gradient(to right, #38BDF8, #10B981, #38BDF8);
        background-size: 200% auto;
        color: #000;
        background-clip: text; text-fill-color: transparent;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    .hero-subtitle {
        text-align: center; color: #94a3b8; font-size: 1.5rem; letter-spacing: 12px; margin-bottom: 60px;
    }

    /* حاويات الزجاج الشفاف (Glassmorphism) */
    .glass-panel { 
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-panel:hover {
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
    }

    /* زر الإطلاق المستقبلي */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 1.2rem; font-weight: 900;
        background: linear-gradient(90deg, #0f172a, #1e293b);
        color: #38bdf8; border: 1px solid #38bdf8; 
        padding: 16px; text-transform: uppercase; letter-spacing: 3px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover { 
        background: linear-gradient(90deg, #38bdf8, #10b981);
        color: #030712; border: 1px solid transparent;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.6);
        transform: scale(1.02);
    }

    /* تعديل حقول الإدخال لتندمج مع الزجاج */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 📺 الشاشة الترحيبية (Landing Page)
# ==========================================
if st.session_state.page == 'welcome':
    st.markdown("<div style='margin-top: 18vh;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>KHALID FLOW</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>SYSTEM INITIALIZATION</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.button("INITIATE UPLINK ⚡", on_click=enter_dashboard)


# ==========================================
# ⚙️ لوحة التحكم (Command Center)
# ==========================================
elif st.session_state.page == 'dashboard':
    st.markdown("<h2 style='text-align: center; font-weight: 900; letter-spacing: 2px;'>⚡ COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 30px;'>Secure Payload Distribution Matrix</p>", unsafe_allow_html=True)
    
    # قسم البيانات (محاط بحاوية زجاجية)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #38bdf8; margin-bottom: 20px;'>1. CORE PAYLOAD</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        global_caption = st.text_area("Global Caption / Description", height=130)
    with col2:
        uploaded_video = st.file_uploader("Upload Target Video", type=["mp4"])
    st.markdown('</div>', unsafe_allow_html=True)

    # قسم المنصات (محاط بحاوية زجاجية)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #10b981; margin-bottom: 20px;'>2. TARGET ENDPOINTS</h4>", unsafe_allow_html=True)
    col_ig, col_fb, col_yt = st.columns(3)
    with col_ig:
        target_ig = st.toggle("📱 Instagram Reels", value=True)
    with col_fb:
        target_fb = st.toggle("📘 Facebook Page", value=True)
    with col_yt:
        target_yt = st.toggle("📺 YouTube", value=False)
        if target_yt:
            yt_title = st.text_input("YouTube Video Title")
            yt_privacy = st.selectbox("Privacy Level", ["private", "unlisted", "public"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # محرك النشر الأساسي (لم يمس)
    if st.button("🚀 EXECUTE GLOBAL DEPLOYMENT"):
        if not uploaded_video: st.error("❌ Video attachment is required.")
        elif not global_caption: st.error("❌ Global caption is required.")
        elif not (target_ig or target_fb or target_yt): st.error("❌ Enable at least one platform.")
        elif target_yt and not yt_title: st.error("❌ YouTube requires a title.")
        else:
            target_filename = "test_video.mp4"
            with open(target_filename, "wb") as f:
                f.write(uploaded_video.getbuffer())
            
            with st.status("Executing OMNI-Channel Pipeline...", expanded=True) as status:
                need_meta = target_ig or target_fb
                
                if need_meta:
                    st.write("☁️ Preparing cloud link for Meta...")
                    video_url = upload_to_cloud_buffer(target_filename)
                    
                    if video_url:
                        st.write(f"🔗 Direct link ready: `{video_url}`")
                        
                        if target_fb:
                            st.write("📘 Uploading to Facebook Page...")
                            if publish_to_facebook(video_url, global_caption):
                                st.success("✅ [Facebook] Published successfully.")
                            else:
                                st.error("❌ [Facebook] Publish failed.")
                                
                        if target_ig:
                            st.write("📱 Uploading to Instagram Reels...")
                            if publish_to_instagram(video_url, global_caption):
                                st.success("✅ [Instagram] Published successfully.")
                            else:
                                st.error("❌ [Instagram] Publish failed.")
                    else:
                        st.error("❌ Failed to generate cloud link.")
                
                if target_yt:
                    st.write("📺 Uploading to YouTube...")
                    try:
                        video_id = upload_video_to_youtube(
                            file_path=target_filename, 
                            title=yt_title, 
                            description=global_caption, 
                            category_id="28", 
                            privacy_status=yt_privacy
                        )
                        if video_id:
                            st.success(f"✅ [YouTube] Published successfully (ID: {video_id})")
                        else:
                            st.error("❌ [YouTube] Publish failed.")
                    except Exception as e:
                        st.error(f"❌ [YouTube] Error: {e}")
                
                status.update(label="System: Deployment Completed", state="complete", expanded=False)
            
            if os.path.exists(target_filename):
                os.remove(target_filename)