import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "bible.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    conn.execute("PRAGMA journal_mode=WAL")  # WAL mode = better concurrent read performance for SQLite
    return conn


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id           TEXT PRIMARY KEY,
                user_id      TEXT NOT NULL,
                title        TEXT NOT NULL,
                description  TEXT,
                start_time   TEXT NOT NULL,
                end_time     TEXT NOT NULL,
                duration     INTEGER NOT NULL,
                priority     TEXT NOT NULL,
                difficulty   TEXT NOT NULL,
                deadline     TEXT,
                is_completed INTEGER NOT NULL DEFAULT 0,
                is_deleted   INTEGER NOT NULL DEFAULT 0,
                created_at   TEXT NOT NULL,
                updated_at   TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              TEXT PRIMARY KEY,
                username        TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                created_at      TEXT NOT NULL
            )
        """)
    print(f"DB initialised at: {DB_PATH}")
