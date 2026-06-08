import os
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = FastAPI(title="Chayan Tracker")

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "tracker")
DB_USER = os.getenv("DB_USER", "chayan")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )

class Note(BaseModel):
    title: str
    content: str

@app.on_event("startup")
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Chayan Tracker v1.0"}

@app.post("/api/notes")
def create_note(note: Note):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id, created_at",
        (note.title, note.content)
    )
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result

@app.get("/api/notes")
def list_notes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY created_at DESC LIMIT 50")
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return notes
