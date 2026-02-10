from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

class Ingester:
    def __init__(self, embedding_model:HuggingFaceEmbeddings=None):
        self.embedding_model= embedding_model if embedding_model else HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        load_dotenv()
        self.DATA_DIR = os.getenv("DATA_DIR")
        self.vector_store= Chroma(
            collection_name="documents_collection",
            embedding_function=self.embedding_model,
            persist_directory=os.path.join(self.DATA_DIR,"chroma_db")
        )

        self.converter= DocumentConverter()
        self.chunker= HybridChunker(max_tokens=400, overlap=50)
        self.logger = logging.getLogger(__name__)

    def ingest_documents(self,documents_path):
        source_path = Path(documents_path)
        converted=self.converter.convert(source=source_path).document
        chunks= self.chunker.chunk(dl_doc=converted)
        lc_docs= [Document(page_content=chunk.text,metadata={"source": str(source_path.resolve())}) for chunk in chunks]
        self.logger.info(f"Ingesting {len(lc_docs)} chunks from document '{source_path}' into the vector store.")
        self.vector_store.add_documents(documents=lc_docs)
    
    def delete_document(self,source: str):
        source_path = Path(source)
        try:
            os.remove(source_path)
        except FileNotFoundError:
            self.logger.warning(f"File {source_path} not found for deletion.")
            pass  # If the file does not exist, we can ignore the error
        # Attempt to delete by the given source value and also by the resolved absolute path.
        deleted_any = False
        try:
            self.vector_store.delete(where={"source": source})
            deleted_any = True
        except Exception as e:
            self.logger.debug(f"Vector delete by provided source failed: {e}")

        try:
            abs_source = str(source_path.resolve())
            # If abs_source equals the original, this will just repeat; that's fine.
            self.vector_store.delete(where={"source": abs_source})
            deleted_any = True
        except Exception as e:
            self.logger.debug(f"Vector delete by absolute source failed: {e}")

        if not deleted_any:
            self.logger.warning(f"No vector entries deleted for source '{source}' or '{abs_source}'.")

        return f"Documents from source '{source}' have been cleared from the vector store. deleted={deleted_any}"
    
    def clear_document(self):
        return self.vector_store.reset_collection()
    
    def list_chunks(self):
        return self.vector_store.get(limit=100000,offset=0)
        

if __name__ == "__main__":
    ingester = Ingester()
    # ingester.ingest_documents("E:/Coding/AIMl/Rag/data/test_doc/sample.pdf")
    # print("Document ingestion completed.")
    ingester.delete_document("sample_1770465383.pdf")
    print("Deleted document and its chunks from the vector store.")
    ingester.clear_document()
    print("Cleared documents from the vector store.")
    print(ingester.list_chunks())