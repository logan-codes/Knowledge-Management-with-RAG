import streamlit as st
import os

def load_css(file_name="style.css"):
    """
    Loads a CSS file from the same directory as this script.
    """
    css_file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
