import streamlit as st
import os

from khalid_core import upload_to_cloud_buffer, publish_to_instagram, publish_to_facebook
from youtube_uploader import upload_video_to_youtube

st.set_page_config(page_title="KhalidFlow | Unified Matrix", page_icon="⚙️", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stButton>button {
        width: 100%; border-radius: 6px; font-size: 18px; font-weight: bold;
        background-color: #0F172A; color: #38BDF8; border: 1px solid #1E293B; padding: 12px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1E293B; border: 1px solid #38BDF8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.2); }
    .platform-container { background-color: #0f111a; padding: 15px; border-radius: 8px; border: 1px solid #1e2130; margin-bottom: 15px; height: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ KhalidFlow | OMNI-Channel Deployment")
st.markdown("**Centralized Payload Distribution (Instagram, Facebook & YouTube)**")
st.divider()

st.header("1. Core Payload")
col1, col2 = st.columns([2, 1])

with col1:
    global_caption = st.text_area("Global Caption / Description", height=150)
with col2:
    uploaded_video = st.file_uploader("Upload Video (.mp4)", type=["mp4"])

st.divider()

st.header("2. Target Endpoints")
col_ig, col_fb, col_yt = st.columns(3)

with col_ig:
    st.markdown('<div class="platform-container">', unsafe_allow_html=True)
    target_ig = st.toggle("📱 Instagram Reels", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_fb:
    st.markdown('<div class="platform-container">', unsafe_allow_html=True)
    target_fb = st.toggle("📘 Facebook Page", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_yt:
    st.markdown('<div class="platform-container">', unsafe_allow_html=True)
    target_yt = st.toggle("📺 YouTube", value=False)
    if target_yt:
        yt_title = st.text_input("Video Title (Required for YouTube)")
        yt_privacy = st.selectbox("Privacy", ["private", "unlisted", "public"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

if st.button("🚀 Execute Global Deployment"):
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