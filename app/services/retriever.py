from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

class Retriever:
    def __init__(self, embedding_model:HuggingFaceEmbeddings=None):
        self.embed= embedding_model if embedding_model else HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        load_dotenv()
        self.DATA_DIR = os.getenv("DATA_DIR")
        self.vector_store=Chroma(
            collection_name="documents_collection",
            embedding_function=self.embed,
            persist_directory=os.path.join(self.DATA_DIR,"chroma_db")
        )

        self.GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
        if self.GEMINI_API_KEY is None:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    def _retrieve_chunks(self,query:str):
        retrieved_chunks = self.vector_store.similarity_search(query,k=3)
        return retrieved_chunks
    
    def _query_transformer(self,query:str):
        template= """You are an AI language model assistant. Your task is to generate three 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",temperature=0.7)
        chain= (prompt 
                | llm
                | StrOutputParser()
                | (lambda x: x.strip().split("\n"))  # Split the output into a list of questions
        )
        response= chain.invoke({"question": query})
        return response

    def retrieve_context(self, query: str):
        transformed_queries = self._query_transformer(query)
        all_retrieved_chunks = []
        for tq in transformed_queries:
            chunks = self._retrieve_chunks(tq)
            for chunk in chunks:
                if chunk.page_content not in [c.page_content for c in all_retrieved_chunks]:
                    all_retrieved_chunks.append(chunk)
            
        context = ""
        citations = []
        for idx, doc in enumerate(all_retrieved_chunks):
            source = os.path.basename(doc.metadata.get("source", "Unknown"))
            context += (f"Context {idx+1} (Source: {source}):\n{doc.page_content}\n{'-'*50}\n")
            if source not in citations:
                citations.append(source)
                
        return {"context": context, "citations": citations}

if __name__ == "__main__":
    retriever_instance = Retriever()
    # results = retriever_instance.retrieve_chunks("Sample query")
    # print(results)
    # transformed_response = retriever_instance.query_transformer("tell me about the history of AI and its applications in healthcare and finance")
    # print(transformed_response)
    context = retriever_instance.retrieve_context("how does the ocr work in docling?")
    print(context)