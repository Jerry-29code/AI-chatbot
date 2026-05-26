from fastapi import FastAPI, UploadFile, File
from sqlalchemy import create_engine, text as sql_text
from dotenv import load_dotenv
import os
import uuid

load_dotenv(dotenv_path="../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

app = FastAPI()

def chunk_text(text, chunk_size=750, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

@app.get("/")
def read_root():
    return {"message": "Ingest API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    filename = file.filename
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    chunks = chunk_text(text)

    with engine.connect() as conn:
        conn.execute(
            sql_text("INSERT INTO documents (id, title, status) VALUES (:id, :title, :status)"),
            {"id": doc_id, "title": filename, "status": "processing"}
        )
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            conn.execute(
                sql_text("INSERT INTO chunks (id, document_id, content, chunk_index) VALUES (:id, :doc_id, :content, :index)"),
                {"id": chunk_id, "doc_id": doc_id, "content": chunk, "index": i}
            )
        conn.execute(
            sql_text("UPDATE documents SET status='ready' WHERE id=:id"),
            {"id": doc_id}
        )
        conn.commit()

    return {"document_id": doc_id, "title": filename, "chunks": len(chunks), "status": "ready"}

@app.get("/search")
def search_chunks(q: str):
    with engine.connect() as conn:
        results = conn.execute(
            sql_text("SELECT content FROM chunks WHERE content ILIKE :query LIMIT 5"),
            {"query": f"%{q}%"}
        ).fetchall()
    return {"results": [r[0] for r in results]}