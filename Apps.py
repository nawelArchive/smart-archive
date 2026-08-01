import streamlit as st
import os
import csv
import pandas as pd
from PIL import Image
from io import BytesIO
import re

def save_archive(archive_file, metadata):
    # Save the file
    archive_path = os.path.join('uploaded_archive', archive_file.name)
    archive_file.save(archive_path)

    # Save the metadata to a CSV file
    metadata_path = os.path.join('metadata', f'{metadata["name"]}.csv')
    with open(metadata_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'section', 'date', 'keywords'])
        writer.writerow([metadata['name'], metadata['section'], metadata['date'], metadata['keywords']])

def process_archive(archive_file):
    # Process the file here
    # You can extract text, keywords, etc. from the file
    # and return the metadata as a dictionary
    metadata = {}
    if archive_file.type == 'application/pdf':
        # Extract text from PDF
        with open(archive_file.name, 'rb') as file:
            pdf = PdfFileReader(file)
            text = pdf.getPage(0).extractText()
        # Extract keywords from text
        keywords = re.findall(r'\b\w+\b', text)
        metadata['keywords'] = ' '.join(keywords)
    elif archive_file.type == 'image/jpeg':
        # Extract text from JPEG
        with open(archive_file.name, 'rb') as file:
            image = Image.open(file)
            text = image.text
        # Extract keywords from text
        keywords = re.findall(r'\b\w+\b', text)
        metadata['keywords'] = ' '.join(keywords)
    else:
        metadata['keywords'] = ''
    return {
        'name': archive_file.name,
        'section': st.session_state['section'],
        'date': st.session_state['date'],
        'keywords': metadata['keywords']
    }

def main():
    st.title('Document Indexing App')

    # Sidebar
    st.sidebar.header('Navigation')
    st.sidebar.markdown('### 1. Main Menu')
    with st.sidebar.expander('Go to Main Menu'):
        st.markdown('''
            - [ ] Home
            - [ ] About
            - [ ] Contact Us
        ''')

    st.sidebar.markdown('### 2. Document Processing')
    with st.sidebar.expander('Upload a Document'):
        st.markdown('''
            - [ ] Upload a PDF or JPEG file
            - [ ] Enter the section, date, and keywords for the document
            - [ ] Click "Save" to save the document and its metadata
        ''')

    st.sidebar.markdown('### 3. Document Search')
    with st.sidebar.expander('Search for a Document'):
        st.markdown('''
            - [ ] Enter keywords to search for documents
            - [ ] Click "Search" to find documents that match the keywords
        ''')

    # Main content
    st.header('Document Indexing App')

    # Upload a document
    if not os.path.exists('uploaded_archive'):
        os.makedirs('uploaded_archive')
    metadata_dir = 'metadata'    
    if  not os.path.exists('metadata_dir'):
        os.makedirs('metadata_dir')
    if 'uploaded_archives' not in st.session_state:
        st.session_state['uploaded_archives'] = []
    if 'section' not in st.session_state:
        st.session_state['section'] = ''
    if 'date' not in st.session_state:
        st.session_state['date'] = ''
    if 'search_keywords' not in st.session_state:
        st.session_state['search_keywords'] = ''
    if 'search_results' not in st.session_state:
        st.session_state['search_results'] = []
    if 'searched' not in st.session_state:
        st.session_state['searched'] = False
    if 'searching' not in st.session_state:
        st.session_state['searching'] = False
        st.title("نظام الأرشيف الذكي 📂")

if __name__ == "__main__":
    main()
    import streamlit as st
    from pypdf import PdfReader
    import os

    # أو المجلد لحفظ الملفات مؤقتاً إذا لم يكن موجوداً
    if not os.path.exists("metadata"):
        os.makedirs("metadata")

    # --- القائمة الجانبية (Sidebar) ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("اختر الصفحة:", ["1. Main Menu", "2. Upload a Document", "3. Document Search"])

    # --- الصفحة الأولى: القائمة الرئيسية ---
    if page == "1. Main Menu":
        st.title("نظام الأرشيف الذكي 📁")
        st.write("مرحباً بك في نظام رقمنة وإدارة الوثائق.")

    # --- الصفحة الثانية: رفع ومعالجة الوثائق ---
    elif page == "2. Upload a Document":
        st.title("معالجة ورقمنة الوثائق 📄")
        st.subheader("1. رفع ملف الـ PDF")
        
        uploaded_file = st.file_uploader("اختر ملف PDF لرقمنته", type=["pdf"])

        if uploaded_file is not None:
            st.success("✅ تم رفع الملف بنجاح في الذاكرة المؤقتة!")
            from pypdf import PdfReader
    
            reader = PdfReader(uploaded_file)
            num_pages = len(reader.pages)
            st.write(f"📄 عدد صفحات الملف: {num_pages}")
    
            st.subheader("📝 البيانات والنصوص المستخرجة من الملف:")
    
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    st.markdown(f"**--- الصفحة {page_num + 1} ---**")
                    st.write(text)

 
            st.text_area("المحتوى المقروء من الملف:", value=text, height=300)
            
            # حقول إدخال البيانات الوصفية (Metadata)
            st.subheader("3. البيانات الوصفية للوثيقة")
            doc_name = st.text_input("اسم الوثيقة:", value=uploaded_file.name)
            section = st.selectbox("القسم:", ["المالية", "الموارد البشرية", "الأرشيف العام", "أخرى"])
            keywords = st.text_area("الكلمات المفتاحية (لفصلها استخدم فاصلة ,):")
            
            if st.button("حفظ الوثيقة مبدئياً"):
                st.balloons()
                st.success(f"🎉 رائع! تم محاكاة حفظ الوثيقة '{doc_name}' بنجاح!")

    # --- الصفحة الثالثة: البحث ---
    elif page == "3. Document Search":
        st.title("البحث في الأرشيف 🔍")
        st.text_input("أدخل كلمات مفتاحية للبحث:")



