import streamlit as st
import os
import time
import json
import textwrap

# ==========================================
# 0. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="KhalidFlow | Control Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    publish_to_facebook,
)
from youtube_uploader import upload_video_to_youtube


# ==========================================
# 2. SESSION MANAGEMENT
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "welcome"


def enter_dashboard():
    st.session_state.page = "dashboard"


def logout():
    st.session_state.page = "welcome"


# ==========================================
# 3. HTML HELPER
#    dedent prevents HTML from being rendered
#    as a Markdown code block.
# ==========================================
def render_html(content):
    """Render trusted app-owned HTML/CSS without Markdown code-block parsing.

    Requires Streamlit 1.33.0 or newer (st.html).
    """
    st.html(textwrap.dedent(content).strip())


# ==========================================
# 4. PREMIUM RESPONSIVE DESIGN SYSTEM
# ==========================================
render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #070B12;
    --surface: #0D1623;
    --surface-2: #111E2D;
    --line: rgba(148, 163, 184, .15);
    --text: #F1F5F9;
    --muted: #8B9AAF;
    --cyan: #38BDF8;
    --green: #10B981;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    color: var(--text);
    background:
        radial-gradient(ellipse at 8% 0%, rgba(16,185,129,.12), transparent 32%),
        radial-gradient(ellipse at 92% 8%, rgba(56,189,248,.12), transparent 34%),
        linear-gradient(180deg, #080E17 0%, #070B12 55%, #080F18 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { right: 1rem; }

.block-container {
    max-width: 1160px;
    padding: 1.6rem 2rem 3rem;
}

h1, h2, h3, h4 { color: #F8FAFC !important; }
p, label, .stMarkdown { color: #D4DCE7; }

/* Brand */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2px 0 30px;
}
.brand-mark {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    color: #04111A;
    font-size: 24px;
    font-weight: 900;
    background: linear-gradient(135deg, #67E8F9, #10B981);
    box-shadow: 0 0 28px rgba(16,185,129,.22);
}
.brand-name {
    color: #F8FAFC;
    font-size: 19px;
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: 1.2px;
}
.brand-sub {
    color: #718198;
    font-size: 9px;
    margin-top: 5px;
    letter-spacing: 3px;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: clamp(55px, 10vh, 105px) 18px 52px;
    border: 1px solid rgba(148,163,184,.12);
    border-radius: 28px;
    background:
        radial-gradient(circle at 50% 0%, rgba(56,189,248,.12), transparent 48%),
        linear-gradient(145deg, rgba(16,29,44,.82), rgba(8,15,25,.78));
    box-shadow: 0 25px 90px rgba(0,0,0,.22);
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 13px;
    border: 1px solid rgba(16,185,129,.28);
    border-radius: 999px;
    background: rgba(16,185,129,.08);
    color: #6EE7B7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
}
.hero-title {
    margin: 24px 0 0;
    font-size: clamp(2.5rem, 8vw, 6rem);
    line-height: 1;
    font-weight: 900;
    letter-spacing: clamp(-4px, -.5vw, -1px);
    background: linear-gradient(105deg, #F8FAFC 8%, #7DD3FC 48%, #34D399 90%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-tagline {
    color: #A5B4C7;
    font-size: clamp(10px, 1.6vw, 13px);
    font-weight: 700;
    letter-spacing: clamp(2px, .8vw, 6px);
    margin-top: 19px;
}
.hero-copy {
    max-width: 570px;
    margin: 22px auto 0;
    color: #91A0B4;
    font-size: 13px;
    line-height: 1.9;
}

/* Dashboard headings */
.page-title {
    color: #F8FAFC;
    font-size: clamp(25px, 4vw, 34px);
    font-weight: 900;
    letter-spacing: -1.2px;
    margin: 0;
}
.page-subtitle {
    color: #8493A8;
    font-size: 12px;
    margin-top: 7px;
}
.online {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #6EE7B7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    padding: 9px 12px;
    border: 1px solid rgba(16,185,129,.22);
    border-radius: 999px;
    background: rgba(16,185,129,.07);
}
.online-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 12px #10B981;
}

/* Streamlit bordered containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--line) !important;
    border-radius: 19px !important;
    background: linear-gradient(145deg, rgba(17,30,45,.92), rgba(10,18,29,.94)) !important;
    box-shadow: 0 14px 40px rgba(0,0,0,.16);
}

/* Section labels */
.section-kicker {
    color: #67D5F5;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 7px;
}
.section-note {
    color: #8190A5;
    font-size: 11px;
    margin-bottom: 16px;
}

/* Platform cards */
.platform-icon {
    font-size: 27px;
    margin-bottom: 6px;
}
.platform-name {
    color: #F1F5F9;
    font-size: 14px;
    font-weight: 800;
}
.platform-note {
    color: #8190A5;
    font-size: 10px;
    margin-top: 4px;
}

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: #091321 !important;
    color: #F8FAFC !important;
    border: 1px solid #29394D !important;
    border-radius: 11px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,.12) !important;
}
[data-baseweb="select"] > div {
    background: #091321 !important;
    border-color: #29394D !important;
    border-radius: 11px !important;
    color: #F8FAFC !important;
}
[data-testid="stFileUploader"] {
    background: rgba(8,19,33,.72);
    border: 1px dashed #3A5068;
    border-radius: 13px;
    padding: 8px;
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    width: 100%;
    min-height: 47px;
    border-radius: 12px;
    border: 1px solid rgba(56,189,248,.35);
    background: linear-gradient(110deg, #10283A, #10352E);
    color: #EAFBFF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .5px;
    transition: all .2s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    border-color: #34D399;
    color: #FFFFFF;
    background: linear-gradient(110deg, #075985, #047857);
    box-shadow: 0 0 24px rgba(16,185,129,.18);
    transform: translateY(-1px);
}
.stButton > button:focus, .stFormSubmitButton > button:focus {
    box-shadow: 0 0 0 2px rgba(56,189,248,.2);
}

/* Toggles and captions */
[data-testid="stToggle"] label { color: #E2E8F0 !important; }
.stCaption, [data-testid="stCaptionContainer"] { color: #8291A5 !important; }

/* Footer */
.app-footer {
    text-align: center;
    color: #536278;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 30px 0 8px;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem .85rem 2.5rem;
    }
    .brand { margin-bottom: 20px; }
    .hero {
        padding: 58px 14px 36px;
        border-radius: 20px;
    }
    .hero-title { letter-spacing: -2px; }
    .hero-tagline { letter-spacing: 2px; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
    }
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 10px !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        width: 100% !important;
    }
    .stButton > button, .stFormSubmitButton > button {
        min-height: 49px;
    }
}
</style>
""")


# ==========================================
# 5. SHARED UI COMPONENTS
# ==========================================
def render_brand():
    render_html("""
    <div class="brand">
        <div class="brand-mark">⚡</div>
        <div>
            <div class="brand-name">KHALIDFLOW</div>
            <div class="brand-sub">AUTOMATION SYSTEM</div>
        </div>
    </div>
    """)


def render_footer():
    render_html("""
    <div class="app-footer">
        KHALIDFLOW · ONE VIDEO. EVERYWHERE. · 2026
    </div>
    """)


# ==========================================
# 6. WELCOME / LANDING PAGE
# ==========================================
if st.session_state.page == "welcome":

    render_brand()

    render_html("""
    <div class="hero">
        <div class="hero-pill">
            <span>●</span> CONTENT DISTRIBUTION SYSTEM
        </div>

        <h1 class="hero-title">KHALIDFLOW</h1>

        <div class="hero-tagline">
            ONE VIDEO. EVERYWHERE.
        </div>

        <div class="hero-copy">
            Your content. Your platforms. One workflow.
            Publish your videos across Instagram, Facebook and YouTube
            from one streamlined control center.
        </div>
    </div>
    """)

    st.markdown("")
    left, center, right = st.columns([1, 1.5, 1])

    with center:
        st.button(
            "OPEN CONTROL CENTER  →",
            on_click=enter_dashboard,
            use_container_width=True,
        )

    render_html("""
    <div style="text-align:center;color:#718198;font-size:10px;
                letter-spacing:2px;margin-top:20px;">
        INSTAGRAM &nbsp; · &nbsp; FACEBOOK &nbsp; · &nbsp; YOUTUBE
    </div>
    """)

    render_footer()


# ==========================================
# 7. COMMAND CENTER / DASHBOARD
# ==========================================
elif st.session_state.page == "dashboard":

    render_brand()

    top_left, top_right = st.columns([3, 1])

    with top_left:
        render_html("""
        <div>
            <div class="page-title">Command Center</div>
            <div class="page-subtitle">
                Prepare, configure and distribute your content.
            </div>
        </div>
        """)

    with top_right:
        render_html("""
        <div style="display:flex;justify-content:flex-end;padding:5px 0 10px;">
            <div class="online">
                <span class="online-dot"></span> SYSTEM ONLINE
            </div>
        </div>
        """)
        st.button("← HOME", on_click=logout)

    st.markdown("")

    # --------------------------------------
    # CORE PAYLOAD
    # --------------------------------------
    with st.container(border=True):

        render_html("""
        <div class="section-kicker">01 / CORE PAYLOAD</div>
        <div class="section-note">
            Add your video and prepare the caption for publishing.
        </div>
        """)

        col1, col2 = st.columns([1.35, 1])

        with col1:
            global_caption = st.text_area(
                "Global Caption / Description",
                height=155,
                placeholder="Write your caption or video description...",
            )

        with col2:
            uploaded_video = st.file_uploader(
                "Upload Target Video",
                type=["mp4"],
                help="Select the MP4 video you want to publish.",
            )

            if uploaded_video:
                st.success(f"Video ready: {uploaded_video.name}")
                st.caption(
                    f"File size: {uploaded_video.size / (1024 * 1024):.1f} MB"
                )

    st.markdown("")

    # --------------------------------------
    # TARGET ENDPOINTS
    # --------------------------------------
    with st.container(border=True):

        render_html("""
        <div class="section-kicker">02 / TARGET ENDPOINTS</div>
        <div class="section-note">
            Choose where your video should be published.
        </div>
        """)

        col_ig, col_fb, col_yt = st.columns(3)

        with col_ig:
            with st.container(border=True):
                render_html("""
                <div class="platform-icon">📱</div>
                <div class="platform-name">Instagram</div>
                <div class="platform-note">REELS DISTRIBUTION</div>
                """)
                target_ig = st.toggle("Enable Instagram", value=True)

        with col_fb:
            with st.container(border=True):
                render_html("""
                <div class="platform-icon">📘</div>
                <div class="platform-name">Facebook</div>
                <div class="platform-note">PAGE DISTRIBUTION</div>
                """)
                target_fb = st.toggle("Enable Facebook", value=True)

        with col_yt:
            with st.container(border=True):
                render_html("""
                <div class="platform-icon">📺</div>
                <div class="platform-name">YouTube</div>
                <div class="platform-note">VIDEO DISTRIBUTION</div>
                """)
                target_yt = st.toggle("Enable YouTube", value=False)

        # Keep original YouTube variable names and behavior.
        if target_yt:
            st.markdown("---")

            render_html("""
            <div class="section-kicker">YOUTUBE CONFIGURATION</div>
            """)

            yt_col1, yt_col2 = st.columns([2, 1])

            with yt_col1:
                yt_title = st.text_input(
                    "YouTube Video Title",
                    placeholder="Enter your video title...",
                )

            with yt_col2:
                yt_privacy = st.selectbox(
                    "Privacy Level",
                    ["private", "unlisted", "public"],
                    index=0,
                )

    st.markdown("")

    # --------------------------------------
    # DEPLOYMENT ENGINE
    # --------------------------------------
    render_html("""
    <div class="section-kicker">03 / DEPLOYMENT ENGINE</div>
    <div class="section-note">
        Check your selections, then launch the publishing pipeline.
    </div>
    """)

    if st.button(
        "🚀  EXECUTE GLOBAL DEPLOYMENT",
        use_container_width=True,
    ):

        if not uploaded_video:
            st.error("❌ Video attachment is required.")

        elif not global_caption.strip():
            st.error("❌ Global caption is required.")

        elif not (target_ig or target_fb or target_yt):
            st.error("❌ Enable at least one platform.")

        elif target_yt and not yt_title.strip():
            st.error("❌ YouTube requires a title.")

        else:
            target_filename = "test_video.mp4"

            with open(target_filename, "wb") as f:
                f.write(uploaded_video.getbuffer())

            try:
                with st.status(
                    "Executing OMNI-Channel Pipeline...",
                    expanded=True,
                ) as status:

                    need_meta = target_ig or target_fb

                    if need_meta:
                        st.write("☁️ Preparing cloud link for Meta...")

                        video_url = upload_to_cloud_buffer(target_filename)

                        if video_url:
                            st.write(f"🔗 Direct link ready: `{video_url}`")

                            if target_fb:
                                st.write("📘 Uploading to Facebook Page...")

                                if publish_to_facebook(video_url, global_caption):
                                    st.success(
                                        "✅ [Facebook] Published successfully."
                                    )
                                else:
                                    st.error("❌ [Facebook] Publish failed.")

                            if target_ig:
                                st.write("📱 Uploading to Instagram Reels...")

                                if publish_to_instagram(video_url, global_caption):
                                    st.success(
                                        "✅ [Instagram] Published successfully."
                                    )
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
                                privacy_status=yt_privacy,
                            )

                            if video_id:
                                st.success(
                                    f"✅ [YouTube] Published successfully (ID: {video_id})"
                                )
                            else:
                                st.error("❌ [YouTube] Publish failed.")

                        except Exception as e:
                            st.error(f"❌ [YouTube] Error: {e}")

                    status.update(
                        label="System: Deployment Completed",
                        state="complete",
                        expanded=False,
                    )

            except Exception as e:
                st.error(f"❌ Deployment pipeline error: {e}")

            finally:
                if os.path.exists(target_filename):
                    os.remove(target_filename)

    render_footer()
