import streamlit as st

st.set_page_config(
    page_title="Knowledge Management RAG",
    page_icon="🧠",
    layout="wide"
)

# Hero Section
st.title("🧠 Knowledge Management System")
st.markdown("""
    ### Your Personal AI-Powered Knowledge Base
    
    Welcome to a local-first Retrieval-Augmented Generation (RAG) system designed to help you 
    **organize**, **search**, and **chat** with your documents. Powered by advanced AI models, 
    this tool transforms your static files into an interactive knowledge engine.
""")

st.divider()

# Key Features Section
st.header("✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📄 Smart Ingestion")
    st.markdown("""
    - **Advanced Parsing**: Uses [Docling](https://github.com/DS4SD/docling) for high-fidelity PDF & document processing.
    - **Async Processing**: Upload large files without blocking the UI.
    - **State Management**: Track document status from upload to full indexing.
    """)

with col2:
    st.subheader("🤖 Intelligent Retrieval")
    st.markdown("""
    - **Semantic Search**: Powered by `all-MiniLM-L6-v2` embeddings.
    - **Vector Database**: Fast and scalable storage using ChromaDB (local) or Qdrant.
    - **Query Expansion**: Generates multiple perspectives for better recall.
    """)

with col3:
    st.subheader("💬 Context-Aware Chat")
    st.markdown("""
    - **Gemini Powered**: Uses Google's Gemini 2.5 Flash Lite for accurate reasoning.
    - **History Aware**: Remembers conversation context for fluid interaction.
    - **Source Citations**: Know exactly where the answer came from (Coming Soon).
    """)

st.divider()

# How It Works / Getting Started
st.header("🚀 Getting Started")

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("#### 1. Upload Documents")
    st.info("Go to the **Documents** page and upload your PDFs, DOCX, or TXT files.")

with step2:
    st.markdown("#### 2. Process & Index")
    st.warning("The system automatically processes files in the background. Watch the status change to 'Ingested'.")

with step3:
    st.markdown("#### 3. Chat with Data")
    st.success("Switch to the **Chat** page and ask questions about your knowledge base.")

st.divider()

# Tech Stack Footer
with st.expander("🛠️ Under the Hood"):
    st.markdown("""
    This project is built with a modern, robust tech stack:
    - **Backend**: FastAPI (Python)
    - **Frontend**: Streamlit
    - **LLM**: Google Gemini 1.5 Flash
    - **Embeddings**: HuggingFace (`sentence-transformers`)
    - **Vector Store**: ChromaDB / SQLite
    - **Parsing**: Docling
    """)

st.markdown("---")
st.caption("Built with ❤️ by Logan | version 2.0.0")
