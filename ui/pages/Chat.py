import streamlit as st
import requests
import os
import json
import sys
from dotenv import load_dotenv

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_css

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/")

st.set_page_config(page_title="Chat App", page_icon="💬", layout="wide")
load_css()

col_title, col_btn = st.columns([0.8, 0.2])
with col_title:
    st.markdown('<h1 class="gradient-text">💬 Chat Interface</h1>', unsafe_allow_html=True)
with col_btn:
    if st.button("Clear History", type="primary"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = None
            try:
                res = requests.post(
                    API_URL+"chat",
                    json={"question": prompt, "history": json.dumps(st.session_state.messages)}
                )
            except requests.exceptions.RequestException:
                st.error("⚠️ Could not connect to the backend. Please try again later.")
                st.stop()

            if res is None:
                st.stop()
            
            if res.status_code == 200:
                reply = res.json()["response"]
            else:
                reply = "Sorry, something went wrong. Please try again later."

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
            st.markdown(reply)

