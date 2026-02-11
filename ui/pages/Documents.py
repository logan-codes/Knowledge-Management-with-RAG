import streamlit as st
import requests
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_css

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/")

st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")
load_css()

st.markdown('<h1 class="gradient-text">📄 Document Management</h1>', unsafe_allow_html=True)

def fetch_documents():
    try:
        res = requests.get(API_URL + "documents")
        if res.status_code == 200:
            return res.json().get("documents", [])
    except Exception:
        st.error("Failed to fetch documents from the server.")
    return []

def upload_document(file):
    files = {"file": (file.name, file.getvalue(), file.type)}
    try:
        res=requests.post(API_URL + "document", files=files)
    except requests.exceptions.RequestException:
        st.error("⚠️ Could not connect to the backend. Please try again later.")
        return None
    return res

def delete_document(name):
    try:
        res=requests.delete(API_URL + f"document", json={"source": name})
    except requests.exceptions.RequestException:
        st.error("⚠️ Could not connect to the backend. Please try again later.")
        return None
    return res

# Upload Section
st.subheader("📤 Upload Document")
st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.2); margin-bottom: 20px;">
        <p style="margin: 0; color: #aaa;">Supported formats: PDF, DOCX, TXT</p>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["pdf", "docx", "txt"],
    label_visibility="collapsed"
)

if uploaded_file:
    if st.button("Upload and Ingest", type="primary"):
        with st.spinner("Uploading and ingesting document..."):
            res = upload_document(uploaded_file)

            if res is None:
                pass  # Error already shown by upload_document
            elif res.status_code == 200:
                st.success("✅ Document uploaded successfully")
            else:
                st.error("❌ Failed to upload document")

st.divider()

# Documents List
st.subheader("📄 Available Documents")

search_col, _ = st.columns([1, 1])
with search_col:
    search_query = st.text_input(   
        "",
        placeholder="🔍 Search documents...",
        label_visibility="collapsed"
    )

with st.spinner("Fetching documents..."):
    documents = fetch_documents()

if search_query:
    documents = [
        doc for doc in documents
        if search_query.lower() in doc[0].lower()
    ]

if not documents:
    st.info("No documents available.")
else:
    # Header
    st.markdown("""
        <div style="display: flex; font-weight: bold; color: #e0e0e0; padding: 10px 0; border-bottom: 2px solid rgba(67, 97, 238, 0.5); background: rgba(0,0,0,0.2); margin-bottom: 10px;">
            <div style="flex: 3; padding-left: 10px;">Filename</div>
            <div style="flex: 2;">Status</div>
            <div style="flex: 2;">Uploaded At</div>
            <div style="flex: 1; text-align: right; padding-right: 10px;">Actions</div>
        </div>
    """, unsafe_allow_html=True)

    for idx, doc in enumerate(documents):
        filename, status, timestamp, path = doc
        
        status_class = "status-ingested" if status == "ingested" else "status-pending"
        status_display = f"✅ {status.capitalize()}" if status == "ingested" else f"⏳ {status.capitalize()}"

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"<div style='padding-top: 5px; padding-left: 10px;'>{filename}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<span class='status-badge {status_class}'>{status_display}</span>", unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"<div style='padding-top: 5px; color: #aaa;'>{timestamp}</div>", unsafe_allow_html=True)
            
        with col4:
            if st.button("🗑️", key=f"delete_{idx}", help="Delete Document"):
                with st.spinner("Deleting..."):
                    res = delete_document(path)
                    if res and res.status_code == 200:
                        st.success(f"Deleted {filename}")
                        st.rerun()
                    else:
                        st.error("Failed to delete")
        
        st.markdown("<hr style='margin: 5px 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
