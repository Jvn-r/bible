import sqlite3
import os
from contextlib import contextmanager

# DB file will be created in the same directory as this file
# When you point this to the Pi, just change this path to the network mount
DB_PATH = os.getenv("DB_PATH", "bible.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # this is what makes row_to_dict() work in main.py
    conn.execute("PRAGMA journal_mode=WAL")  # WAL mode = better concurrent read performance for SQLite
    return conn


@contextmanager
def get_db():
    # use this as a context manager: `with get_db() as db:`
    # handles commit and close automatically, rolls back on error
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
    # creates the tasks table if it doesn't exist yet
    # safe to call every startup — won't overwrite existing data
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
    print(f"DB initialised at: {DB_PATH}")
