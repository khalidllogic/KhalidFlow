import streamlit as st

# إعداد عنوان الصفحة ورمز التبويب
st.set_page_config(page_title="KhalidFlow", page_icon="🚀", layout="centered")

# عنوان التطبيق الرئيسي
st.title("🚀 KhalidFlow")
st.subheader("Multi-Platform Video Publisher")

st.divider() # خط فاصل

# واجهة بسيطة لاختيار الفيديوهات وكتابة التفاصيل (MVP)
st.write("### 1. تفاصيل الفيديو")
video_title = st.text_input("عنوان الفيديو (Title)")
video_desc = st.text_area("وصف الفيديو (Description)")
uploaded_video = st.file_uploader("اختر ملف الفيديو", type=['mp4', 'mov'])

st.write("### 2. المنصات المستهدفة")
col1, col2, col3 = st.columns(3)
with col1:
    to_youtube = st.checkbox("YouTube Shorts")
with col2:
    to_instagram = st.checkbox("Instagram Reels")
with col3:
    to_facebook = st.checkbox("Facebook Reels")

st.divider()

# زر النشر (لا يفعل شيئاً الآن)
if st.button("بدء النشر", type="primary"):
    if not uploaded_video:
        st.error("الرجاء اختيار ملف فيديو أولاً.")
    elif not video_title:
        st.warning("الرجاء كتابة عنوان للفيديو.")
    elif not (to_youtube or to_instagram or to_facebook):
        st.warning("الرجاء اختيار منصة واحدة على الأقل.")
    else:
        st.info("جاري تجهيز النظام للنشر... (لم نبرمج التكامل بعد!)")