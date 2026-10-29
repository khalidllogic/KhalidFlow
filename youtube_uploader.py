import os
import socket
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# زيادة وقت انتظار استجابة الخادم إلى 300 ثانية (5 دقائق) لتجاوز تقطعات الشبكة
socket.setdefaulttimeout(300)

def get_authenticated_service():
    """التحقق من وجود التصريح وبناء قناة اتصال مع يوتيوب"""
    if not os.path.exists('token.json'):
        raise FileNotFoundError("ملف token.json مفقود. يجب إنهاء المصادقة أولاً.")
    
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
    return build('youtube', 'v3', credentials=creds)

def upload_video_to_youtube(file_path, title, description, category_id="22", privacy_status="private"):
    """
    رفع الفيديو إلى يوتيوب.
    privacy_status: 'private', 'public', 'unlisted'
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
    try:
        # أضفنا num_retries=3 ليحاول 3 مرات تلقائياً في حال انقطاع الشبكة
        response = request.execute(num_retries=3)
        print(f"✅ تم الرفع بنجاح! معرف الفيديو: {response['id']}")
        return response['id']
    except HttpError as e:
        print(f"❌ خطأ من خوادم Google أثناء الرفع: {e}")
        return None

if __name__ == '__main__':
    print("هذا الملف عبارة عن وحدة برمجية (Module) ولا يجب تشغيله مباشرة إلا للاختبار.")