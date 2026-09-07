from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from database import get_connection, init_database


app = FastAPI(
    title="AI Interview Performance System",
    description="Backend API for AI Interview Performance System",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://gauri-129.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_database()


class Candidate(BaseModel):
    name: str
    email: str
    target_role: Optional[str] = ""
    experience: Optional[str] = ""
    skills: Optional[str] = ""


@app.get("/")
def home():
    return {
        "success": True,
        "message": "AI Interview Performance System backend is running"
    }


@app.post("/candidates")
def create_candidate(candidate: Candidate):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO candidates
            (name, email, target_role, experience, skills)
            VALUES (?, ?, ?, ?, ?)
        """, (
            candidate.name,
            candidate.email,
            candidate.target_role,
            candidate.experience,
            candidate.skills
        ))

        connection.commit()

        candidate_id = cursor.lastrowid

        return {
            "success": True,
            "candidate_id": candidate_id,
            "message": "Candidate saved successfully"
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }

    finally:

        connection.close()


@app.get("/candidates")
def get_candidates():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM candidates
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]
