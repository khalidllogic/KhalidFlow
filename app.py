import streamlit as st
import os
import time
import json
import hmac

# ==========================================
# 0. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="KhalidFlow | Control System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. CLOUD MATRIX JSON RECONSTRUCTOR
# ==========================================
if "YOUTUBE_CLIENT_SECRET" in st.secrets and not os.path.exists("client_secret.json"):
    with open("client_secret.json", "w", encoding="utf-8") as f:
        f.write(st.secrets["YOUTUBE_CLIENT_SECRET"])

if "YOUTUBE_TOKEN" in st.secrets and not os.path.exists("token.json"):
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(st.secrets["YOUTUBE_TOKEN"])

from khalid_core import (
    upload_to_cloud_buffer,
    publish_to_instagram,
    publish_to_facebook
)

from youtube_uploader import upload_video_to_youtube


# ==========================================
# 2. SESSION MANAGEMENT
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def enter_dashboard():
    st.session_state.page = "login"


def authenticate():
    entered_password = st.session_state.get("login_password", "")

    if "DASHBOARD_PASSWORD" not in st.secrets:
        st.session_state.login_error = "Access password is not configured."
        return

    correct_password = str(st.secrets["DASHBOARD_PASSWORD"])

    if hmac.compare_digest(entered_password, correct_password):
        st.session_state.authenticated = True
        st.session_state.page = "dashboard"
        st.session_state.login_error = ""
        st.session_state.login_password = ""
    else:
        st.session_state.login_error = "Invalid access credentials."


def logout():
    st.session_state.authenticated = False
    st.session_state.page = "welcome"
    st.session_state.login_password = ""


# ==========================================
# 3. PREMIUM DESIGN SYSTEM
# ==========================================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #070B12;
    --surface: #0E1622;
    --surface-light: #131F2E;
    --border: rgba(148, 163, 184, 0.13);
    --text: #F1F5F9;
    --muted: #8493A8;
    --cyan: #38BDF8;
    --green: #10B981;
}

* {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(16,185,129,.10), transparent 35%),
        radial-gradient(ellipse at 90% 10%, rgba(56,189,248,.10), transparent 35%),
        #070B12;
    color: var(--text);
}

[data-testid="stHeader"],
#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* ---------- TYPOGRAPHY ---------- */

h1, h2, h3, h4 {
    color: #F8FAFC !important;
    letter-spacing: -0.7px;
}

p, label {
    color: #CBD5E1;
}

.muted-text {
    color: var(--muted);
    font-size: 0.9rem;
}

/* ---------- BRAND ---------- */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 25px;
}

.brand-icon {
    width: 43px;
    height: 43px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    color: #07111A;
    background: linear-gradient(135deg, #38BDF8, #10B981);
    box-shadow: 0 0 25px rgba(16,185,129,.22);
}

.brand-name {
    font-size: 21px;
    font-weight: 900;
    letter-spacing: -1px;
    color: #F8FAFC;
}

.brand-caption {
    font-size: 9px;
    color: #64748B;
    letter-spacing: 3px;
}

/* ---------- HERO ---------- */

.hero-wrapper {
    text-align: center;
    padding: 100px 15px 65px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 15px;
    border: 1px solid rgba(16,185,129,.25);
    border-radius: 30px;
    background: rgba(16,185,129,.07);
    color: #34D399;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 25px;
}

.hero-title {
    font-size: clamp(2.8rem, 8vw, 6.5rem);
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: -5px;
    background: linear-gradient(110deg, #F8FAFC 10%, #38BDF8 48%, #10B981 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: clamp(11px, 2vw, 15px);
    letter-spacing: clamp(3px, 1vw, 7px);
    margin-top: 22px;
}

.hero-description {
    max-width: 530px;
    margin: 25px auto;
    color: #8493A8;
    font-size: 14px;
    line-height: 1.9;
}

/* ---------- PANELS ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(19,31,46,.88),
        rgba(10,17,28,.94)
    );
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    box-shadow: 0 15px 45px rgba(0,0,0,.18);
}

/* ---------- BUTTONS ---------- */

.stButton > button {
    width: 100%;
    min-height: 49px;
    border-radius: 12px;
    border: 1px solid rgba(56,189,248,.35);
    background: linear-gradient(110deg, #0F2535, #12352F);
    color: #E0F2FE;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: .5px;
    transition: all .25s ease;
}

.stButton > button:hover {
    border-color: #10B981;
    background: linear-gradient(110deg, #0E7490, #047857);
    color: white;
    box-shadow: 0 0 25px rgba(16,185,129,.20);
    transform: translateY(-2px);
}

.stButton > button:focus {
    box-shadow: 0 0 0 2px rgba(56,189,248,.25);
}

/* ---------- INPUTS ---------- */

.stTextInput input,
.stTextArea textarea {
    background: #0A1220 !important;
    color: #F8FAFC !important;
    border: 1px solid #253449 !important;
    border-radius: 11px !important;
    min-height: 45px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,.12) !important;
}

[data-baseweb="select"] > div {
    background: #0A1220 !important;
    border-color: #253449 !important;
    border-radius: 11px !important;
}

[data-testid="stFileUploader"] {
    background: rgba(10,18,32,.7);
    border: 1px dashed #334155;
    border-radius: 13px;
    padding: 8px;
}

/* ---------- TOGGLES ---------- */

[data-testid="stToggle"] {
    padding: 8px 0;
}

/* ---------- SECTION HEADERS ---------- */

.section-heading {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #38BDF8;
    margin-bottom: 5px;
}

.section-description {
    color: #64748B;
    font-size: 12px;
    margin-bottom: 18px;
}

/* ---------- STATUS ---------- */

.system-status {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #34D399;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 10px #10B981;
}

/* ---------- LOGIN ---------- */

.login-icon {
    width: 65px;
    height: 65px;
    border-radius: 20px;
    margin: 0 auto 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    background: linear-gradient(135deg, #123B48, #123B30);
    border: 1px solid rgba(56,189,248,.2);
}

/* ---------- FOOTER ---------- */

.custom-footer {
    text-align: center;
    color: #475569;
    font-size: 10px;
    letter-spacing: 2px;
    padding: 30px 0 10px;
}

/* ---------- MOBILE RESPONSIVE ---------- */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem .85rem 3rem;
    }

    .hero-wrapper {
        padding: 75px 5px 35px;
    }

    .hero-title {
        letter-spacing: -2px;
    }

    .hero-subtitle {
        letter-spacing: 3px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
    }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 12px !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        width: 100% !important;
    }

    .stButton > button {
        min-height: 50px;
        font-size: 12px;
    }

    .stTextArea textarea {
        min-height: 120px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. REUSABLE BRAND HEADER
# ==========================================
def render_brand():
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">⚡</div>
        <div>
            <div class="brand-name">KHALIDFLOW</div>
            <div class="brand-caption">AUTOMATION SYSTEM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="custom-footer">
        KHALIDFLOW · BUILT FOR AUTOMATION · 2026
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 5. WELCOME PAGE
# ==========================================
if st.session_state.page == "welcome":

    render_brand()

    st.markdown("""
    <div class="hero-wrapper">

        <div class="hero-badge">
            ● SYSTEM READY · VERSION 2.0
        </div>

        <h1 class="hero-title">KHALIDFLOW</h1>

        <div class="hero-subtitle">
            ONE VIDEO. EVERYWHERE.
        </div>

        <div class="hero-description">
            A unified content distribution platform.
            Upload once and publish your content across
            multiple social media platforms through one
            intelligent control center.
        </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.button(
            "ACCESS CONTROL CENTER  →",
            on_click=enter_dashboard,
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:#64748B;font-size:11px;">
        INSTAGRAM &nbsp; · &nbsp; FACEBOOK &nbsp; · &nbsp; YOUTUBE
    </div>
    """, unsafe_allow_html=True)

    render_footer()


# ==========================================
# 6. SECURE LOGIN PAGE
# ==========================================
elif st.session_state.page == "login":

    render_brand()

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.3, 1])

    with center:

        with st.container(border=True):

            st.markdown("""
            <div style="text-align:center;padding:12px 0 20px;">

                <div class="login-icon">🔐</div>

                <h2 style="font-size:25px;margin-bottom:5px;">
                    Secure Access
                </h2>

                <p style="color:#8493A8;font-size:12px;">
                    Authentication required to continue
                </p>

                <div class="system-status" style="justify-content:center;">
                    <span class="status-dot"></span>
                    PROTECTED ENVIRONMENT
                </div>

            </div>
            """, unsafe_allow_html=True)

            with st.form("secure_login_form"):

                st.text_input(
                    "ACCESS PASSWORD",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )

                st.form_submit_button(
                    "UNLOCK CONTROL CENTER  →",
                    on_click=authenticate,
                    use_container_width=True
                )

            if st.session_state.get("login_error"):
                st.error(st.session_state.login_error)

            st.markdown("""
            <p style="text-align:center;color:#64748B;font-size:10px;">
                AUTHORIZED ACCESS ONLY
            </p>
            """, unsafe_allow_html=True)

    back_col1, back_col2, back_col3 = st.columns([1, 1.3, 1])

    with back_col2:
        st.button(
            "← BACK TO HOME",
            on_click=logout,
            use_container_width=True
        )

    render_footer()


# ==========================================
# 7. COMMAND CENTER
# ==========================================
elif st.session_state.page == "dashboard":

    # Security guard
    if not st.session_state.authenticated:
        st.session_state.page = "login"
        st.rerun()

    render_brand()

    # Dashboard top bar
    top_left, top_right = st.columns([3, 1])

    with top_left:
        st.markdown("""
        <div style="padding:8px 0;">
            <div style="font-size:25px;font-weight:900;color:#F8FAFC;">
                Command Center
            </div>
            <div style="color:#8493A8;font-size:12px;margin-top:5px;">
                Manage your global content distribution
            </div>
        </div>
        """, unsafe_allow_html=True)

    with top_right:
        st.markdown("""
        <div style="padding:12px 0;text-align:right;">
            <div class="system-status" style="justify-content:flex-end;">
                <span class="status-dot"></span>
                SYSTEM ONLINE
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.button("LOG OUT ↗", on_click=logout)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # CORE PAYLOAD
    # --------------------------------------
    with st.container(border=True):

        st.markdown("""
        <div class="section-heading">
            01 / CORE PAYLOAD
        </div>
        <div class="section-description">
            Configure the content you want to distribute.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1.4, 1])

        with col1:
            global_caption = st.text_area(
                "Global Caption / Description",
                height=160,
                placeholder="Write your content description here..."
            )

        with col2:
            uploaded_video = st.file_uploader(
                "Upload Target Video",
                type=["mp4"]
            )

            if uploaded_video:
                st.success("Video successfully attached.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # TARGET ENDPOINTS
    # --------------------------------------
    with st.container(border=True):

        st.markdown("""
        <div class="section-heading">
            02 / TARGET ENDPOINTS
        </div>
        <div class="section-description">
            Select the platforms where your content will be published.
        </div>
        """, unsafe_allow_html=True)

        col_ig, col_fb, col_yt = st.columns(3)

        with col_ig:
            with st.container(border=True):
                st.markdown("### 📱")
                st.markdown("**Instagram**")
                st.caption("Reels Distribution")

                target_ig = st.toggle(
                    "Enable Instagram",
                    value=True
                )

        with col_fb:
            with st.container(border=True):
                st.markdown("### 📘")
                st.markdown("**Facebook**")
                st.caption("Page Distribution")

                target_fb = st.toggle(
                    "Enable Facebook",
                    value=True
                )

        with col_yt:
            with st.container(border=True):
                st.markdown("### 📺")
                st.markdown("**YouTube**")
                st.caption("Video Distribution")

                target_yt = st.toggle(
                    "Enable YouTube",
                    value=False
                )

        # YouTube settings
        if target_yt:

            st.markdown("---")

            st.markdown("""
            <div class="section-heading">
                YOUTUBE CONFIGURATION
            </div>
            """, unsafe_allow_html=True)

            yt_col1, yt_col2 = st.columns([2, 1])

            with yt_col1:
                yt_title = st.text_input(
                    "YouTube Video Title",
                    placeholder="Enter video title..."
                )

            with yt_col2:
                yt_privacy = st.selectbox(
                    "Privacy Level",
                    ["private", "unlisted", "public"],
                    index=0
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # DEPLOYMENT ENGINE
    # --------------------------------------
    st.markdown("""
    <div class="section-heading">
        03 / DEPLOYMENT ENGINE
    </div>
    <div class="section-description">
        Review your settings and execute the publishing pipeline.
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🚀  EXECUTE GLOBAL DEPLOYMENT",
        use_container_width=True
    ):

        if not uploaded_video:
            st.error("❌ Video attachment is required.")

        elif not global_caption:
            st.error("❌ Global caption is required.")

        elif not (target_ig or target_fb or target_yt):
            st.error("❌ Enable at least one platform.")

        elif target_yt and not yt_title:
            st.error("❌ YouTube requires a title.")

        else:

            target_filename = "test_video.mp4"

            with open(target_filename, "wb") as f:
                f.write(uploaded_video.getbuffer())

            try:

                with st.status(
                    "Executing OMNI-Channel Pipeline...",
                    expanded=True
                ) as status:

                    need_meta = target_ig or target_fb

                    if need_meta:

                        st.write("☁️ Preparing cloud link for Meta...")

                        video_url = upload_to_cloud_buffer(
                            target_filename
                        )

                        if video_url:

                            st.write(
                                f"🔗 Direct link ready: `{video_url}`"
                            )

                            if target_fb:

                                st.write(
                                    "📘 Uploading to Facebook Page..."
                                )

                                if publish_to_facebook(
                                    video_url,
                                    global_caption
                                ):
                                    st.success(
                                        "✅ [Facebook] Published successfully."
                                    )
                                else:
                                    st.error(
                                        "❌ [Facebook] Publish failed."
                                    )

                            if target_ig:

                                st.write(
                                    "📱 Uploading to Instagram Reels..."
                                )

                                if publish_to_instagram(
                                    video_url,
                                    global_caption
                                ):
                                    st.success(
                                        "✅ [Instagram] Published successfully."
                                    )
                                else:
                                    st.error(
                                        "❌ [Instagram] Publish failed."
                                    )

                        else:

                            st.error(
                                "❌ Failed to generate cloud link."
                            )

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

                                st.success(
                                    f"✅ [YouTube] Published successfully (ID: {video_id})"
                                )

                            else:

                                st.error(
                                    "❌ [YouTube] Publish failed."
                                )

                        except Exception as e:

                            st.error(
                                f"❌ [YouTube] Error: {e}"
                            )

                    status.update(
                        label="System: Deployment Completed",
                        state="complete",
                        expanded=False
                    )

            except Exception as e:

                st.error(f"❌ Deployment pipeline error: {e}")

            finally:

                if os.path.exists(target_filename):
                    os.remove(target_filename)

    render_footer()