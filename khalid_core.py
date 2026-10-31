import os
import time
import requests
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
IG_USER_ID = os.getenv('IG_USER_ID')
FB_PAGE_TOKEN = os.getenv('FB_PAGE_TOKEN')
FB_PAGE_ID = os.getenv('FB_PAGE_ID')

def upload_to_cloud_buffer(file_path):
    print("☁️ 1. Uploading video to cloud buffer for Meta...")
    url = "https://catbox.moe/user/api.php"
    data = {'reqtype': 'fileupload'}
    try:
        with open(file_path, 'rb') as f:
            files = {'fileToUpload': f}
            res = requests.post(url, data=data, files=files)
        if res.status_code == 200 and "catbox.moe" in res.text:
            direct_url = res.text.strip()
            print(f"✅ Cloud link secured: {direct_url}")
            return direct_url
        else:
            print("❌ Cloud upload failed:", res.text)
            return None
    except Exception as e:
        print(f"❌ Cloud connection error: {e}")
        return None

def publish_to_instagram(video_url, caption):
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
        print("❌ Failed to create container:", res)
        return False
        
    creation_id = res['id']
    print("⏳ [Instagram] Meta is processing the video (Please wait)...")
    status_url = f"https://graph.facebook.com/v18.0/{creation_id}?fields=status_code&access_token={ACCESS_TOKEN}"
    
    while True:
        time.sleep(5)
        status_res = requests.get(status_url).json()
        status = status_res.get('status_code')
        print(f"   - Server status: {status}")
        if status == 'FINISHED': break
        if status == 'ERROR':
            print("❌ Meta processing error:", status_res)
            return False
            
    print("🎉 Sending final publish command to Instagram...")
    pub_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"
    pub_res = requests.post(pub_url, data={'creation_id': creation_id, 'access_token': ACCESS_TOKEN}).json()
    
    if 'id' in pub_res:
        print(f"✅ Instagram publish complete! (Post ID: {pub_res['id']})")
        return True
    return False

def publish_to_facebook(video_url, description):
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
            print("❌ [Facebook] Publish failed:", res)
            return False
    except Exception as e:
        print(f"❌ [Facebook] Fatal connection error: {e}")
        return False