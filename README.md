# Knowledge Management with RAG

This project is an RAG (Retrieval Augmented Genration) implementation to mangage your private or personal information base.

## Planned Features

- [ ] Ability to upload and manage files such as pdf, jpg, docx, xls, ppt, etc.(just the basic)
- [ ] Chat interface to tap into the vector db and answer user queries using Gemini API
- [ ] Ability to remove files
- [ ] Multiple chat history

# Tech stack

- Streamlit
- Langchain
- Chromadb
- Docling
- Fastapi

# Project Structure

└── 📁db
        └── 📁chroma_db
        └── 📁uploads
└── 📁services
    ├── document_ingester.py
    ├── generation.py
    ├── retriever.py
└── 📁streamlit
    ├── homepage.py
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt