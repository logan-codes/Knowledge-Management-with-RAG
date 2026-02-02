from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


class retriever:
    def __init__(self):
        self.embed=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        self.vector_store=Chroma(
            collection_name="documents_collection",
            embedding_function=self.embed,
            persist_directory="./db/chroma_db"
        )

    def retrieve_chunks(self,query:str):
        retrieved_chunks = self.vector_store.similarity_search(query,k=5)
        return retrieved_chunks

if __name__ == "__main__":
    retriever_instance = retriever()
    results = retriever_instance.retrieve_chunks("Sample query")
    print(results)