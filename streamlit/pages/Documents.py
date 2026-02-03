import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/")


st.set_page_config(page_title="Upload File", page_icon="📤")
st.title("📤 Upload Document")

uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    with st.spinner("Uploading and ingesting file..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(API_URL+"upload", files=files)

        if response.status_code == 200:
            st.success("File uploaded and ingested successfully.")
            st.json(response.json())
        else:
            st.error("⚠️ Failed to upload the file.")
