import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="Knowledge Management RAG",
    page_icon="🧠",
    layout="wide"
)

load_css()

# Hero Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h1 class="gradient-text" style="font-size: 3rem; margin-bottom: 10px;">Knowledge Management</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #b0b0b0; margin-top: 0;">Your Second Brain, Supercharged by AI</h3>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="padding: 24px; background: rgba(67, 97, 238, 0.08); border-radius: 16px; border-left: 6px solid #4361EE; margin-top: 20px;">
            <p style="font-size: 1.15rem; margin: 0; line-height: 1.6; color: #e0e0e0;">
                Welcome to your local-first <strong>RAG System</strong>. 
                Seamlessly upload documents, index them with advanced semantic search, and chat with your data using 
                state-of-the-art AI models. Secure, private, and powerful.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Statistic / Quick Action Placeholder
    st.markdown("""
        <div class="custom-card" style="text-align: center; display: flex; flex-direction: column; justify-content: center; height: 100%; border: 1px solid rgba(67, 97, 238, 0.3); background: rgba(67, 97, 238, 0.05);">
            <div style="font-size: 3.5rem; margin-bottom: 10px; filter: drop-shadow(0 0 20px rgba(67, 97, 238, 0.4));">🚀</div>
            <h3 style="margin-top: 5px; font-weight: 800; color: #fff;">Get Started</h3>
            <p style="color: #bbb; margin-bottom: 15px; font-size: 0.9rem;">Upload your first document to unlock the power of AI.</p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Documents.py", label="Start Uploading", icon="📂", use_container_width=True)

st.divider()

# Key Features Section
st.markdown('<h2 style="text-align: center; margin-bottom: 40px;">✨ Powerful Features</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

def feature_card(icon, title, points, color_accent):
    points_html = "".join([f"<li style='margin-bottom: 8px;'>{p}</li>" for p in points])
    return f"""
    <div class="custom-card" style="border-top: 4px solid {color_accent};">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">{icon}</div>
        <div class="card-title" style="background: {color_accent}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</div>
        <div class="card-text">
            <ul style="padding-left: 20px; margin-top: 0;">
                {points_html}
            </ul>
        </div>
    </div>
    """

with col1:
    st.markdown(feature_card(
        "📄", 
        "Smart Ingestion", 
        [
            "<strong>Docling Parsing:</strong> High-fidelity PDF processing.",
            "<strong>Async Processing:</strong> Non-blocking uploads.",
            "<strong>Status Tracking:</strong> Real-time updates."
        ],
        "linear-gradient(90deg, #4CC9F0, #4361EE)" # Blue Cyan Gradient
    ), unsafe_allow_html=True)

with col2:
    st.markdown(feature_card(
        "🧠", 
        "Intelligent Retrieval", 
        [
            "<strong>Semantic Search:</strong> Deep meaning extraction.",
            "<strong>Local Vector DB:</strong> Private ChromaDB storage.",
            "<strong>Query Expansion:</strong> Enhanced recall."
        ],
        "linear-gradient(90deg, #7209B7, #F72585)" # Purple Pink Gradient
    ), unsafe_allow_html=True)

with col3:
    st.markdown(feature_card(
        "💬", 
        "Context-Aware Chat", 
        [
            "<strong>Gemini Powered:</strong> Advanced reasoning.",
            "<strong>History Aware:</strong> Fluid conversations.",
            "<strong>Citations:</strong> (Coming Soon) Fact-checking."
        ],
        "linear-gradient(90deg, #FF9E00, #FF0054)" # Orange Red Gradient
    ), unsafe_allow_html=True)

st.divider()


# How It Works / Getting Started
st.markdown('<h2 style="margin-bottom: 30px;">🚀 How It Works</h2>', unsafe_allow_html=True)

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("""
        <div class="custom-card" style="text-align: center; border: 1px solid rgba(76, 201, 240, 0.2);">
            <div style="font-size: 2rem; color: #4CC9F0; font-weight: 800; margin-bottom: 10px;">01</div>
            <h4>Upload</h4>
            <p style="color: #aaa; margin-bottom: 15px;">Go to <strong>Documents</strong> and upload your files.</p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Documents.py", label="Go to Documents", icon="📂", use_container_width=True)

with step2:
    st.markdown("""
        <div class="custom-card" style="text-align: center; border: 1px solid rgba(114, 9, 183, 0.2);">
            <div style="font-size: 2rem; color: #7209B7; font-weight: 800; margin-bottom: 10px;">02</div>
            <h4>Process</h4>
            <p style="color: #aaa;">The system parses, embeds, and indexes your content automatically.</p>
        </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
        <div class="custom-card" style="text-align: center; border: 1px solid rgba(247, 37, 133, 0.2);">
            <div style="font-size: 2rem; color: #F72585; font-weight: 800; margin-bottom: 10px;">03</div>
            <h4>Chat</h4>
            <p style="color: #aaa;">Ask anything. Get instant answers grounded in your data.</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Tech Stack Footer
with st.expander("🛠️ Under the Hood"):
    st.markdown("""
    <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 15px;">🐍</span>
            <div>
                <strong style="color: #4361EE;">Backend:</strong> FastAPI (Python)
            </div>
        </li>
        <li style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 15px;">🎨</span>
            <div>
                <strong style="color: #F72585;">Frontend:</strong> Streamlit
            </div>
        </li>
        <li style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 15px;">🧠</span>
            <div>
                <strong style="color: #4CC9F0;">AI Model:</strong> Google Gemini 2.5 Flash
            </div>
        </li>
        <li style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 15px;">🗄️</span>
            <div>
                <strong style="color: #7209B7;">Vector DB:</strong> ChromaDB (Local)
            </div>
        </li>
        <li style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 15px;">📄</span>
            <div>
                <strong style="color: #FF9E00;">Parser:</strong> Docling
            </div>
        </li>
    </ul>
    """, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; margin-top: 50px; color: #666;'>Built with ❤️ by Logan | version 2.1.0</div>", unsafe_allow_html=True)
