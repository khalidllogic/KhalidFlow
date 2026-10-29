import streamlit as st
import os
from youtube_uploader import upload_video_to_youtube

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="KhalidFlow", page_icon="🌊", layout="centered")

st.title("🌊 KhalidFlow")
st.subheader("منصة النشر الموحدة للفيديو (إصدار يوتيوب)")
st.markdown("---")

# 2. واجهة إدخال البيانات
st.header("1. تفاصيل الفيديو")
video_title = st.text_input("عنوان الفيديو", placeholder="اكتب عنواناً جذاباً...")
video_description = st.text_area("وصف الفيديو", placeholder="اكتب وصفاً تفصيلياً...")
# جعلنا الخيار الافتراضي 'private' لحماية تجاربك
privacy_status = st.selectbox("حالة الخصوصية", ["private", "unlisted", "public"], index=0) 

st.header("2. رفع الملف")
uploaded_file = st.file_uploader("اختر ملف الفيديو (MP4)", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file) # معاينة الفيديو قبل الرفع

st.markdown("---")

# 3. زر النشر ومنطق التشغيل
if st.button("🚀 نشر الفيديو إلى YouTube"):
    if not video_title:
        st.error("❌ يرجى كتابة عنوان الفيديو أولاً.")
    elif uploaded_file is None:
        st.error("❌ يرجى اختيار ملف الفيديو أولاً.")
    else:
        with st.spinner("جاري معالجة ورفع الفيديو إلى يوتيوب، يرجى الانتظار..."):
            # هندسة الذاكرة: حفظ الملف المرفوع مؤقتاً ليقرأه YouTube API
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # استدعاء وحدة الرفع (Backend)
            video_id = upload_video_to_youtube(
                file_path=temp_file_path,
                title=video_title,
                description=video_description,
                privacy_status=privacy_status
            )
            
            # التنظيف الذاتي: حذف الملف المؤقت بعد إتمام الرفع
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            # عرض النتيجة للمستخدم
            if video_id:
                st.success("🎉 تم النشر بنجاح!")
                st.markdown(f"[🔗 اضغط هنا لمشاهدة الفيديو على YouTube](https://www.youtube.com/watch?v={video_id})")
                st.balloons()
            else:
                st.error("❌ حدث خطأ أثناء الرفع. راجع الـ Terminal للتفاصيل.")