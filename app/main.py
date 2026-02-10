from fastapi import FastAPI, UploadFile, Request, HTTPException,BackgroundTasks, File, Depends
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from functools import lru_cache 
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import shutil
from services.document_ingester import Ingester
from services.retriever import Retriever
from services.generation import Generation
from services.database import Database
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import time
import logging
import json

# --- Structured Logging Setup ---
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if hasattr(record, "extra"):
            log_record.update(record.extra)
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
#--- Lifecycle Management ---
database = Database()
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    logger.info("Database connection established.")
    load_dotenv()
    ingest_uploaded_docs()
    yield
    database.disconnect()
    logger.info("Database connection closed. Application shutdown complete.")
    logger.info("Application has been stopped.")

# --- FastAPI App ---
app = FastAPI(lifespan=lifespan)

# --- Middleware for Request Logging ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path}",
        extra={"extra": {"method": request.method, "path": request.url.path, "status_code": response.status_code, "duration_ms": round(process_time, 2)}}
    )
    return response

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected internal server error occurred."}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

# --- Dependency Injection ---
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@lru_cache()
def get_ingester():
    return Ingester(embedding_model=embed_model)

@lru_cache()
def get_retriever():
    return Retriever(embedding_model=embed_model)

@lru_cache()
def get_generator():
    return Generation()

# --- Background Tasks ---
def ingest_documents(path:str):
    ingester=get_ingester()
    logger.info(f"Starting document ingestion for {path}", extra={"extra": {"document_path": path}})
    ingester.ingest_documents(path)
    logger.info(f"Document ingestion completed for {path}", extra={"extra": {"document_path": path}})
    database.update_document_status(path, "ingested")
    logger.info(f"Document status updated to 'ingested' for {path}", extra={"extra": {"document_path": path}})

def ingest_uploaded_docs():
    to_be_ingested = database.list_documents()
    for doc in to_be_ingested:
        if doc[1] == "uploaded":
            ingest_documents(doc[3])
            logger.info(f"Background ingestion completed for {doc[3]}", extra={"extra": {"document_path": doc[3]}})

# --- API Endpoints ---
@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/document")
async def upload_file(background_tasks: BackgroundTasks,file:UploadFile=File(...) ):
    upload_dir = os.path.join(os.getenv("DATA_DIR"), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    safe_filename = secure_filename(file.filename)
    file_path = os.path.join(upload_dir, f"{os.path.splitext(safe_filename)[0]}_{int(time.time())}{os.path.splitext(safe_filename)[1]}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    database.add_document(filename=safe_filename, path=file_path)
    logger.info(f"Uploading file: {file.filename}", extra={"extra": {"original_filename": file.filename, "safe_path": file_path}})
    background_tasks.add_task(ingest_documents, path=file_path)
    return {"filename": file.filename, "message": "File uploaded successfully."}

@app.get("/documents")
def list_documents():
    documents = database.list_documents()
    logger.info("Fetched document list", extra={"extra": {"document_count": len(documents)}})
    return {"documents": documents}

class DeleteRequest(BaseModel):
    source: str

@app.delete("/document")
def clear_document(payload: DeleteRequest, ingester: Ingester = Depends(get_ingester)):
    logger.info(f"Deleting document: {payload.source}")
    message = ingester.delete_document(payload.source)
    logger.info(f"Vector deletion completed for: {payload.source,message}")
    db_msg=database.delete_document(payload.source)
    logger.info(f"Document deletion completed for: {payload.source}")
    return {"message": message, "db_msg": db_msg}

class ChatRequest(BaseModel):
    question: str
    history: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, retriever: Retriever = Depends(get_retriever), generator: Generation = Depends(get_generator)):
    logger.info(f"Chat request received", extra={"extra": {"question_length": len(request.question)}})
    retrieval_data = retriever.retrieve_context(request.question)
    response = generator.generate_response(request.question, retrieval_data["context"], request.history)
    return {"response": response, "citations": retrieval_data["citations"]}
