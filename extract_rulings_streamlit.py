import streamlit as st
import zipfile
import io

st.set_page_config(page_title="📁 ملفات الطعون دفعة واحدة", layout="centered")
st.title("📦 استخراج ملفات الطعون بناءً على ملف أرقام")

# رفع ملفات PDF
uploaded_files = st.file_uploader("📤 ارفع مجموعة من ملفات PDF", type="pdf", accept_multiple_files=True)

# رفع ملف يحتوي على أرقام الطعون (واحد في كل سطر أو مفصولة بفاصلة)
uploaded_ids_file = st.file_uploader("📄 ارفع ملف TXT يحتوي على أرقام الطعون", type=["txt"])

if uploaded_files and uploaded_ids_file:
    content = uploaded_ids_file.read().decode("utf-8")
    # دعم الفصل بفواصل أو أسطر
    raw_numbers = content.replace(",", "\n").splitlines()
    search_numbers = [num.strip() for num in raw_numbers if num.strip().isdigit()]

    matched_files = []
    for file in uploaded_files:
        for num in search_numbers:
            if num in file.name:
                matched_files.append(file)
                break

    if matched_files:
        st.success(f"✅ تم العثور على {len(matched_files)} ملف يطابق الأرقام في الملف.")

        # تجهيز ملف zip في الذاكرة
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in matched_files:
                zip_file.writestr(file.name, file.read())

        zip_buffer.seek(0)

        # زر تنزيل الكل
        st.download_button(
            label="📥 تنزيل كل الملفات المطابقة كملف ZIP",
            data=zip_buffer,
            file_name="الطعون_المختارة.zip",
            mime="application/zip"
        )
    else:
        st.warning("❌ لم يتم العثور على ملفات مطابقة.")
