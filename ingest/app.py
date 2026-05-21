from fastapi import FastAPI, UploadFile, File
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import uuid

load_dotenv(dotenv_path="../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Ingest API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    filename = file.filename

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO documents (id, title, status) VALUES (:id, :title, :status)"),
            {"id": doc_id, "title": filename, "status": "pending"}
        )
        conn.commit()

    return {"document_id": doc_id, "title": filename, "status": "pending"}