from youtube_uploader import upload_video_to_youtube

print("بدء اختبار الرفع المعزول نحو خوادم يوتيوب...")

# نقوم باستدعاء دالة الرفع وتمرير اسم الملف لها
# لاحظ أننا نرفع الفيديو كـ 'private' لكي لا يظهر للمشتركين في قناتك
video_id = upload_video_to_youtube(
    file_path="test_video.mp4",
    title="تجربة خالد الأولى عبر API",
    description="هذا الفيديو تم رفعه تلقائياً بواسطة سكربت Python محلي.",
    category_id="22", # 22 تعني قسم People & Blogs
    privacy_status="private" 
)

if video_id:
    print(f"🎉 نجاح مبهر! يمكنك مشاهدة الفيديو الآن عبر الرابط التالي:")
    print(f"https://www.youtube.com/watch?v={video_id}")
else:
    print("❌ فشل اختبار الرفع.")