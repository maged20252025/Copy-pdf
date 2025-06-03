
import streamlit as st
import zipfile
import io
import tempfile
import os

st.set_page_config(page_title="📁 استخراج ملفات الطعون", layout="centered")
st.title("📦 استخراج ملفات الطعون بناءً على ملف أرقام")

# خيار رفع الملفات
upload_option = st.radio("اختر طريقة رفع الملفات:", ["📤 رفع ملفات PDF مباشرة", "🗂️ رفع ملف مضغوط ZIP يحتوي على PDF"])

uploaded_files = []
if upload_option == "📤 رفع ملفات PDF مباشرة":
    uploaded_files = st.file_uploader("📥 ارفع مجموعة من ملفات PDF", type=["pdf"], accept_multiple_files=True)
elif upload_option == "🗂️ رفع ملف مضغوط ZIP يحتوي على PDF":
    uploaded_zip = st.file_uploader("📦 ارفع ملف ZIP", type=["zip"])
    if uploaded_zip:
        temp_dir = tempfile.TemporaryDirectory()
        zip_path = os.path.join(temp_dir.name, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir.name)

        for filename in os.listdir(temp_dir.name):
            if filename.endswith(".pdf"):
                filepath = os.path.join(temp_dir.name, filename)
                with open(filepath, "rb") as f:
                    uploaded_files.append({"name": filename, "data": f.read()})

# رفع ملف TXT يحتوي على أرقام الطعون
uploaded_ids_file = st.file_uploader("📄 ارفع ملف TXT يحتوي على أرقام الطعون", type=["txt"])

if uploaded_files and uploaded_ids_file:
    content = uploaded_ids_file.read().decode("utf-8")
    raw_numbers = content.replace(",", "\n").splitlines()
    search_numbers = [num.strip() for num in raw_numbers if num.strip().isdigit()]

    matched_files = []
    for file in uploaded_files:
        fname = file.name if hasattr(file, "name") else file["name"]
        for num in search_numbers:
            if num in fname:
                matched_files.append(file)
                break

    if matched_files:
        st.success(f"✅ تم العثور على {len(matched_files)} ملف مطابق.")

        # إنشاء ملف ZIP للتحميل
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_out:
            for file in matched_files:
                if hasattr(file, "read"):  # من uploader
                    zip_out.writestr(file.name, file.read())
                else:  # من zip
                    zip_out.writestr(file["name"], file["data"])
        zip_buffer.seek(0)

        st.download_button(
            label="📥 تنزيل الملفات المطابقة (ZIP)",
            data=zip_buffer,
            file_name="الطعون_المختارة.zip",
            mime="application/zip"
        )
    else:
        st.warning("❌ لم يتم العثور على ملفات تطابق الأرقام المدخلة.")
