import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Cashi Statement Processor", layout="centered")

st.title("📊 Cashi PDF Analyzer")
st.write("Upload your PDF statements to calculate totals.")

# اختيار نوع العملية
transaction_type = st.radio("Select Transaction Type:", ("Positive (+)", "Negative (-)"))
symbol = r'\+' if transaction_type == "Positive (+)" else '-'

# رفع الملفات
uploaded_files = st.file_uploader("Choose Cashi PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    grand_total = 0.0
    st.write("---")
    
    for i, file in enumerate(uploaded_files, 3):
        try:
            # فتح الملف من الذاكرة
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join([page.get_text() for page in doc])
            
            # حساب المبالغ
            pattern = symbol + r'\s*([\d,]+\.\d{2})'
            matches = re.findall(pattern, text)
            file_total = sum(float(m.replace(',', '')) for m in matches)
            
            # البحث عن التاريخ (نصي أو رقمي)
            date_text = re.search(r'(\d{1,2}\s+[\u0600-\u06FF]+\s+\d{4})', text)
            date_digit = re.search(r'(\d{2}-\d{2}-\d{4})', text)
            file_date = "Unknown"
            if date_text: file_date = date_text.group(1)
            elif date_digit: file_date = date_digit.group(1)
            
            # عرض النتيجة
            st.success(f"**Day ({file_date}): {file_total:,.2f}")
            grand_total += file_total
            doc.close()
        except Exception as e:
            st.error(f"Error in file {file.name}: {e}")

    st.divider()

    st.metric(label="GRAND TOTAL", value=f"{grand_total:,.2f}")
