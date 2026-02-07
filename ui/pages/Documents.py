import streamlit as st
import requests
import os
import pandas as pd
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

search_query = st.text_input(   
    "",
    placeholder="🔍 Search documents"
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
    # Table header
    header_cols = st.columns([3, 2, 2, 1])
    header_cols[0].markdown("**Filename**")
    header_cols[1].markdown("**Status**")
    header_cols[2].markdown("**Uploaded At**")
    header_cols[3].markdown("**Actions**")

    st.divider()

    for idx, doc in enumerate(documents):
        filename, status, timestamp, path = doc

        cols = st.columns([3, 2, 2, 1])

        cols[0].write(filename)
        cols[1].write(status)
        cols[2].write(timestamp)

        if cols[3].button(
            "Delete",
            key=f"delete_{idx}",
            type="secondary"
        ):
            with st.spinner("Deleting document..."):
                res = delete_document(path)

                if res is None:
                    pass
                elif res.status_code == 200:
                    st.success(f"✅ Deleted `{filename}`")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete document")
