from fastapi import FastAPI, UploadFile, File
import shutil
from services.document_ingester import Ingester
from services.retriever import Retriever
from services.generation import Generation

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    file_path = f"db/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    ingester= Ingester()
    ingester.ingest_documents(file_path)
    return {"filename": file.filename, "message": "File uploaded and ingested successfully."}

@app.post("/chat")
async def chat_endpoint(question: str):

    retriever = Retriever()
    generator = Generation()

    context = retriever.retrieve_context(question)
    response = generator.generate_response(question, context)

    return {"response": response}