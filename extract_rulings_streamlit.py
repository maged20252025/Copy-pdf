
import streamlit as st
import zipfile
import io

st.set_page_config(page_title="📁 البحث عن ملفات طعن", layout="centered")
st.title("📦 البحث وتنزيل ملفات الطعون دفعة واحدة")

# رفع الملفات
uploaded_files = st.file_uploader("📤 ارفع مجموعة من ملفات PDF", type="pdf", accept_multiple_files=True)

# إدخال أرقام الطعون
search_input = st.text_input("🔎 أدخل أرقام الطعون (افصل بينها بفاصلة)", placeholder="مثال: 30492, 30501, 30777")

if uploaded_files and search_input:
    search_numbers = [num.strip() for num in search_input.split(",") if num.strip().isdigit()]
    matched_files = []

    for file in uploaded_files:
        for num in search_numbers:
            if num in file.name:
                matched_files.append(file)
                break

    if matched_files:
        st.success(f"✅ تم العثور على {len(matched_files)} ملف يطابق الأرقام المدخلة.")

        # تجهيز ملف zip في الذاكرة
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in matched_files:
                zip_file.writestr(file.name, file.read())

        zip_buffer.seek(0)

        # زر تنزيل الكل
        st.download_button(
            label="📥 تنزيل كل الملفات دفعة واحدة (ZIP)",
            data=zip_buffer,
            file_name="الطعون_المختارة.zip",
            mime="application/zip"
        )
    else:
        st.warning("❌ لم يتم العثور على أي ملف يطابق الأرقام المدخلة.")
