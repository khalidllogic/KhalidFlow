import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# الصلاحية المطلوبة: السماح برفع وإدارة الفيديوهات على يوتيوب
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube():
    creds = None
    
    # 1. التحقق مما إذا كان هناك رمز دخول (token) محفوظ مسبقاً من عملية تسجيل دخول سابقة
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # 2. إذا لم يكن هناك رموز صالحة، نطلب من المستخدم تسجيل الدخول
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # تجديد الرمز إذا انتهت صلاحيته
            creds.refresh(Request())
        else:
            # فتح المتصفح لتسجيل الدخول لأول مرة باستخدام ملف الأسرار
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 3. حفظ الرمز الجديد في ملف token.json لاستخدامه لاحقاً
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    print("✅ تمت المصادقة بنجاح مع حساب YouTube!")
    return creds

# هذا الجزء يقوم بتشغيل الدالة فوراً عندما ننفذ هذا الملف من الـ Terminal
if __name__ == '__main__':
    print("جاري بدء الاتصال بخوادم Google...")
    authenticate_youtube()