# 🧠 Knowledge Management RAG System

A powerful, local-first Retrieval-Augmented Generation (RAG) system designed to manage your personal knowledge base. Built with a modern client-server architecture, it allows you to upload documents, persist them in a vector database, and chat with your data using Google's Gemini models.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-0.1-green)

## ✨ Key Features

-   **📄 Document Ingestion**: Seamlessly upload PDF, DOCX, and TXT files.
-   **🤖 Advanced Parsing**: Powered by [Docling](https://github.com/DS4SD/docling) for high-fidelity document parsing and chunking.
-   **🧠 Smart Retrieval**: Uses `sentence-transformers/all-MiniLM-L6-v2` embeddings stored in a local ChromaDB instance.
-   **💬 Context-Aware Chat**: Chat interface powered by Google Gemini 2.5 Flash Lite for fast, accurate responses based on your data.
-   **⚡ High Performance**: Optimized architecture with model caching (LRU) to prevent redundant reloading.
-   **🧹 Management**: View and delete uploaded documents directly from the UI.

## 🛠️ Architecture

The project follows a clean segregation of duties:

```
/
├── 📁 app/                 # FastAPI Backend
│   ├── main.py             # API Entry point & Dependency Injection
│   └── 📁 services/        # Core Business Logic
│       ├── document_ingester.py  # Docling + ChromaDB ingestion
│       ├── retriever.py          # Semantic Search Logic
│       └── generation.py         # Gemini LLM Interface
├── 📁 ui/                  # Streamlit Frontend
│   ├── Home.py             # Landing Page
│   └── 📁 pages/           # Chat & Document Management Modules
├── 📁 data/                # Persistent Storage
│   ├── 📁 chroma_db/       # Vector Database
│   └── 📁 uploads/         # Raw Files
└── requirements.txt        # Dependencies
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.10 or higher
-   A Google AI Studio API Key

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/rag-knowledge-management.git
    cd rag-knowledge-management
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    API_URL=http://localhost:8000/
    ```

### Running the Application

You will need two terminal windows:

**Terminal 1: Backend (API)**
```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2: Frontend (UI)**
```bash
streamlit run ui/Home.py
```

## 📚 Usage Guide

1.  **Upload Info**: Go to the **Documents** page. Upload your PDFs or text files. The system will parse and vectorise them automatically.
2.  **Verify**: Check the file list to ensure your documents are indexed.
3.  **Chat**: Switch to the **Chat** page. Ask questions like "Summarize the document I just uploaded" or specific details contained in your files.

## 🔮 Roadmap

-   [ ] Multiple chat history
-   [ ] Docker & Docker Compose support

---
*Built with ❤️ by logan*