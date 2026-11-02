import os
import shutil
import time
import requests
import streamlit as st
from dotenv import load_dotenv

# تحميل المتغيرات المحلية (في اللابتوب)
load_dotenv()

# هندسة جلب الأسرار: البحث في اللابتوب أولاً، ثم في سحابة Streamlit
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)

ACCESS_TOKEN = get_secret('META_ACCESS_TOKEN')
IG_USER_ID = get_secret('IG_USER_ID')
FB_PAGE_TOKEN = get_secret('FB_PAGE_TOKEN')
FB_PAGE_ID = get_secret('FB_PAGE_ID')

# رابط تطبيقك الأساسي على Streamlit
APP_URL = "https://khaledflowapp.streamlit.app"

def upload_to_cloud_buffer(file_path):
    print("☁️ Uploading video to raw bot-friendly host (Catbox.moe)...")
    url = "https://catbox.moe/user/api.php"
    
    try:
        with open(file_path, 'rb') as f:
            payload = {'reqtype': 'fileupload'}
            files = {'fileToUpload': f}
            res = requests.post(url, data=payload, files=files)
        
        # Catbox يرجع الرابط المباشر كنص عادي (Text)
        if res.status_code == 200 and "catbox.moe" in res.text:
            direct_url = res.text.strip()
            print(f"✅ Pure Raw Cloud link secured: {direct_url}")
            return direct_url
        else:
            print(f"❌ Catbox upload failed: {res.text}")
            return None
    except Exception as e:
        print(f"❌ Cloud connection error: {e}")
        return None

def publish_to_instagram(video_url, caption):
    import streamlit as st
    if not IG_USER_ID or not ACCESS_TOKEN:
        st.error("❌ Fatal Error: IG_USER_ID or META_ACCESS_TOKEN is missing in secrets!")
        return False
        
    print("🚀 [Instagram] Connecting to Meta API...")
    container_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
    payload = {
        'video_url': video_url,
        'caption': caption,
        'media_type': 'REELS',
        'share_to_feed': 'true',
        'access_token': ACCESS_TOKEN
    }
    res = requests.post(container_url, data=payload).json()
    
    if 'id' not in res:
        st.error(f"⛔ رفض من ميتا (Instagram API Error): {res}")
        return False
        
    creation_id = res['id']
    print("⏳ [Instagram] Meta is processing the video (Please wait)...")
    status_url = f"https://graph.facebook.com/v18.0/{creation_id}?fields=status_code&access_token={ACCESS_TOKEN}"
    
    while True:
        time.sleep(5)
        status_res = requests.get(status_url).json()
        status = status_res.get('status_code')
        if status == 'FINISHED': break
        if status == 'ERROR':
            st.error(f"⛔ خطأ أثناء المعالجة (Processing Error): {status_res}")
            return False
            
    pub_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"
    pub_res = requests.post(pub_url, data={'creation_id': creation_id, 'access_token': ACCESS_TOKEN}).json()
    
    if 'id' in pub_res:
        return True
    else:
        st.error(f"⛔ خطأ النشر النهائي: {pub_res}")
        return False

def publish_to_facebook(video_url, description):
    if not FB_PAGE_ID or not FB_PAGE_TOKEN:
        print("❌ Fatal Error: FB_PAGE_ID or FB_PAGE_TOKEN is missing!")
        return False
        
    print("📘 [Facebook] Connecting to Facebook Graph API...")
    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/videos"
    payload = {
        'file_url': video_url,
        'description': description,
        'access_token': FB_PAGE_TOKEN
    }
    try:
        res = requests.post(url, data=payload).json()
        if 'id' in res:
            print(f"✅ [Facebook] Successfully published to Khalid Logic! (Video ID: {res['id']})")
            return True
        else:
            print(f"❌ [Facebook] Publish failed: {res}")
            return False
    except Exception as e:
        print(f"❌ [Facebook] Fatal connection error: {e}")
        return False