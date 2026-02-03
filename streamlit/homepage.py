import streamlit as st
import pages.chat as chat
import pages.upload as upload

st.title("Multipage App")

# Add a sidebar for navigation
page = st.sidebar.selectbox("Select a page:", ["Chat", "Upload"])

if page == "Chat":
    chat.show()
elif page == "Upload":
    upload.show()
