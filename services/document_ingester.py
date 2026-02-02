from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from pathlib import Path

class Ingester:
    def __init__(self):
        self.embedding_model= HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store= Chroma(
            collection_name="documents_collection",
            embedding_function=self.embedding_model,
            persist_directory="./db/chroma_db"
        )

        self.converter= DocumentConverter()
        self.chunker= HybridChunker(max_tokens=400, overlap=50)

    def ingest_documents(self,documents_path):
        source_path = Path(documents_path)
        converted=self.converter.convert(source=source_path).document
        chunks= self.chunker.chunk(dl_doc=converted)
        lc_docs= [Document(page_content=chunk.text) for chunk in chunks]
        self.vector_store.add_documents(lc_docs)
        

if __name__ == "__main__":
    ingester = Ingester()
    ingester.ingest_documents("E:/Coding/AIMl/Rag/docs/test_doc/sample.pdf")
    print("Document ingestion completed.")