from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from pathlib import Path
import os

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
        lc_docs= [Document(page_content=chunk.text,metadata={"source": source_path.name}) for chunk in chunks]
        self.vector_store.add_documents(documents=lc_docs)
    
    def list_documents(self):
        all_docs = Path("./db/uploads").glob("*")
        return [doc.name for doc in all_docs]
    
    def delete_document(self,source: str):
        source_path = Path(f"./db/uploads/{source}")
        os.remove(source_path)
        self.vector_store.delete(where={"source":source})
        return f"Documents from source '{source}' have been cleared from the vector store."
    
    def clear_document(self):
        return self.vector_store.reset_collection()
    
    def list_chunks(self):
        return self.vector_store.get(limit=100000,offset=0)
        

if __name__ == "__main__":
    ingester = Ingester()
    # ingester.ingest_documents("E:/Coding/AIMl/Rag/docs/test_doc/sample.pdf")
    # print("Document ingestion completed.")
    ingester.clear_document()
    print("Cleared documents from the vector store.")
    print(ingester.list_chunks())