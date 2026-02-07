import streamlit as st
import streamlit_shadcn_ui as ui
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/")

st.set_page_config(page_title="Documents", page_icon="📄")
st.title("📄 Document Management")

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

st.subheader("📤 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    if st.button("Upload and Ingest"):
        with st.spinner("Uploading and ingesting document..."):
            res = upload_document(uploaded_file)

            if res is None:
                pass  # Error already shown by upload_document
            elif res.status_code == 200:
                st.success("✅ Document uploaded successfully")
            else:
                st.error("❌ Failed to upload document")

st.divider()

st.subheader("📄 Available Documents")

with st.spinner("Fetching documents..."):
    documents = fetch_documents()

if not documents:
    st.info("No documents available.")
else:
    for doc in documents:
        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"📄 **{doc}**")

        with col2:
            if st.button(
                "❌ Delete",
                key=f"delete_{doc}",
                type="tertiary",
            ):
                with st.spinner("Deleting document..."):
                    res = delete_document(doc)

                    if res.status_code == 200:
                        st.success(f"✅ {doc} deleted")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete document")