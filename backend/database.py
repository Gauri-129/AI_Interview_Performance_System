import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "interview.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            target_role TEXT,
            experience TEXT,
            skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            overall_score REAL DEFAULT 0,
            technical_score REAL DEFAULT 0,
            communication_score REAL DEFAULT 0,
            confidence_score REAL DEFAULT 0,
            answer_quality_score REAL DEFAULT 0,
            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":

    init_database()

    print("Database created successfully!")
    print(f"Database location: {DB_PATH}")
