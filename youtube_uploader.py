import os
import socket
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# ضبط وقت الانتظار لمنع مشاكل انقطاع الشبكة
socket.setdefaulttimeout(300)

def get_authenticated_service():
    """التحقق من وجود التصريح وبناء قناة اتصال مع يوتيوب"""
    if not os.path.exists('token.json'):
        raise FileNotFoundError("ملف token.json مفقود. يجب إنهاء المصادقة أولاً.")
    
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
    return build('youtube', 'v3', credentials=creds)

def upload_video_to_youtube(file_path, title, description, category_id="22", privacy_status="private"):
    """
    رفع الفيديو إلى يوتيوب مع حماية ضد التكرار ومعالجة أخطاء الشبكة.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ملف الفيديو غير موجود في المسار: {file_path}")

    youtube = get_authenticated_service()

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    print(f"جاري رفع الفيديو: {title}...")
    
    # محاولة رفع آمنة بدون num_retries العشوائي لتجنب التكرار، مع التعامل مع الاستثناءات
    try:
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"نسبة الرفع: {int(status.progress() * 100)}%")
                
        print(f"✅ تم الرفع بنجاح! معرف الفيديو: {response['id']}")
        return response['id']
        
    except HttpError as e:
        print(f"❌ خطأ من خوادم Google أثناء الرفع: {e}")
        return None
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع في الشبكة: {e}")
        return None

if __name__ == '__main__':
    print("هذا الملف عبارة عن وحدة برمجية (Module) ولا يجب تشغيله مباشرة إلا للاختبار.")