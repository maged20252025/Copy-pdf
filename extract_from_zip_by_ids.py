
import streamlit as st
import zipfile
import io
import tempfile
import os

st.set_page_config(page_title="📁 استخراج ملفات الطعون من ZIP", layout="centered")
st.title("📦 استخراج ملفات الطعون بناءً على ملف أرقام (من ملف مضغوط)")

# رفع الملف المضغوط
uploaded_zip = st.file_uploader("🗂️ ارفع ملف ZIP يحتوي على ملفات PDF", type=["zip"])

# رفع ملف TXT يحتوي على أرقام الطعون
uploaded_ids_file = st.file_uploader("📄 ارفع ملف TXT يحتوي على أرقام الطعون", type=["txt"])

if uploaded_zip and uploaded_ids_file:
    # قراءة محتوى ملف الأرقام
    content = uploaded_ids_file.read().decode("utf-8")
    raw_numbers = content.replace(",", "
").splitlines()
    search_numbers = [num.strip() for num in raw_numbers if num.strip().isdigit()]

    # فك الضغط إلى مجلد مؤقت
    temp_dir = tempfile.TemporaryDirectory()
    zip_path = os.path.join(temp_dir.name, "uploaded.zip")
    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.read())

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir.name)

    # البحث عن الملفات المطابقة
    matched_files = []
    for filename in os.listdir(temp_dir.name):
        if filename.endswith(".pdf"):
            for num in search_numbers:
                if num in filename:
                    matched_files.append(filename)
                    break

    if matched_files:
        st.success(f"✅ تم العثور على {len(matched_files)} ملف مطابق داخل الملف المضغوط.")

        # إنشاء ملف ZIP جديد يحتوي على الملفات المطابقة
        output_zip = io.BytesIO()
        with zipfile.ZipFile(output_zip, "w") as zip_out:
            for filename in matched_files:
                file_path = os.path.join(temp_dir.name, filename)
                zip_out.write(file_path, arcname=filename)

        output_zip.seek(0)

        # زر التنزيل
        st.download_button(
            label="📥 تنزيل الملفات المطابقة (ZIP)",
            data=output_zip,
            file_name="الطعون_المختارة.zip",
            mime="application/zip"
        )
    else:
        st.warning("❌ لم يتم العثور على ملفات PDF تطابق الأرقام المدخلة.")
