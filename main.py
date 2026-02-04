from fastapi import FastAPI, UploadFile, File, Depends
from functools import lru_cache 
import shutil
from services.document_ingester import Ingester
from services.retriever import Retriever
from services.generation import Generation
from pydantic import BaseModel
import os

app = FastAPI()

@lru_cache()
def get_ingester():
    return Ingester()
@lru_cache()
def get_retriever():
    return Retriever()
@lru_cache()
def get_generator():
    return Generation()

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/document")
async def upload_file(file:UploadFile=File(...), ingester: Ingester = Depends(get_ingester)):
    os.makedirs("db/uploads", exist_ok=True)

    file_path = f"db/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    ingester.ingest_documents(file_path)
    return {"filename": file.filename, "message": "File uploaded and ingested successfully."}

@app.get("/documents")
def list_documents(ingester: Ingester = Depends(get_ingester)):
    documents = ingester.list_documents()
    return {"documents": documents}

class DeleteRequest(BaseModel):
    source: str

@app.delete("/document")
def clear_document(payload: DeleteRequest,ingester: Ingester = Depends(get_ingester)):
    message = ingester.delete_document(payload.source)
    return {"message": message}

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, retriever: Retriever = Depends(get_retriever), generator: Generation = Depends(get_generator)):

    context = retriever.retrieve_context(request.question)
    response = generator.generate_response(request.question, context)

    return {"response": response}