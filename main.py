from fastapi import FastAPI, UploadFile, File
import shutil
from services.document_ingester import Ingester
from services.retriever import Retriever
from services.generation import Generation
from pydantic import BaseModel
import os

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/document")
async def upload_file(file:UploadFile=File(...)):
    os.makedirs("db/uploads", exist_ok=True)

    file_path = f"db/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    ingester= Ingester()
    ingester.ingest_documents(file_path)
    return {"filename": file.filename, "message": "File uploaded and ingested successfully."}

@app.get("/documents")
def list_documents():
    ingester = Ingester()
    documents = ingester.list_documents()
    return {"documents": documents}

class DeleteRequest(BaseModel):
    source: str

@app.delete("/document")
def clear_document(payload: DeleteRequest):
    ingester = Ingester()
    message = ingester.delete_document(payload.source)
    return {"message": message}

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):

    retriever = Retriever()
    generator = Generation()

    context = retriever.retrieve_context(request.question)
    response = generator.generate_response(request.question, context)

    return {"response": response}