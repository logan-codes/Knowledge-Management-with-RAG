import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/chat")

def show():
    st.set_page_config(page_title="Chat App", page_icon="💬")
    st.title("💬 Chat Interface")

    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"You said: {prompt}"

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=30
                )

                if res.status_code == 200:
                    reply = res.json()["response"]
                else:
                    reply = "⚠️ Backend error"

                st.markdown(reply)

