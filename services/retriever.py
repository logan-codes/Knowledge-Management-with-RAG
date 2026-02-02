from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from google import genai
from dotenv import load_dotenv
import os
import asyncio

class retriever:
    def __init__(self):
        self.embed=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        self.vector_store=Chroma(
            collection_name="documents_collection",
            embedding_function=self.embed,
            persist_directory="./db/chroma_db"
        )

        load_dotenv()
        self.GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
        if self.GEMINI_API_KEY is None:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    def retrieve_chunks(self,query:str):
        retrieved_chunks = self.vector_store.similarity_search(query,k=5)
        return retrieved_chunks
    
    async def query_transformer(self,query:str):
        gemini_client= genai.Client(api_key=self.GEMINI_API_KEY)
        prompt=f"Split this question into smaller parts: {query}"
        chat= gemini_client.aio.chats.create(model="gemini-2.5-flash")
        response= await chat.send_message(prompt)
        gemini_client.close()
        return response.text


async def main():
    retriever_instance = retriever()
    # results = retriever_instance.retrieve_chunks("Sample query")
    # print(results)
    transformed_response = await retriever_instance.query_transformer("Sample query")
    print(transformed_response)

if __name__ == "__main__":
    asyncio.run(main())