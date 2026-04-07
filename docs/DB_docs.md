# `database.py`

## Overview
- **Engine:** SQLite
- **File location:** controlled by `DB_PATH` environment variable
- **Default (local):** `bible.db` in the same directory
- **Default (Docker):** `/app/data/bible.db`
- **WAL mode enabled:** better read performance under concurrent access

---
## Connection Pattern
All DB access goes through the `get_db()` context manager. It handles open, commit, rollback on error, and close automatically.
```python
with get_db() as db:
    db.execute("SELECT * FROM tasks")
```
Never call `get_connection()` directly in endpoints — always use `get_db()`.

---
## `init_db()`

Called once on FastAPI startup via the `@app.on_event("startup")` hook. Creates the `tasks` table if it doesn't already exist. Safe to call on every restart — will never overwrite existing data.

---
## Table: `tasks`

|Column|Type|Constraints|Description|
|---|---|---|---|
|`id`|`TEXT`|`PRIMARY KEY`|UUID generated in Python on insert|
|`user_id`|`TEXT`|`NOT NULL`|Owner of the task. Currently `"default_user"`|
|`title`|`TEXT`|`NOT NULL`|Task name|
|`description`|`TEXT`|nullable|Optional details|
|`start_time`|`TEXT`|`NOT NULL`|ISO 8601 datetime string|
|`end_time`|`TEXT`|`NOT NULL`|ISO 8601 datetime string|
|`duration`|`INTEGER`|`NOT NULL`|Duration in minutes|
|`priority`|`TEXT`|`NOT NULL`|`"low"`, `"moderate"`, `"high"`|
|`difficulty`|`TEXT`|`NOT NULL`|`"low"`, `"moderate"`, `"high"`|
|`deadline`|`TEXT`|nullable|Optional ISO 8601 datetime string|
|`is_completed`|`INTEGER`|`NOT NULL DEFAULT 0`|`0 = false`, `1 = true`|
|`is_deleted`|`INTEGER`|`NOT NULL DEFAULT 0`|`0 = false`, `1 = true` — soft delete flag|
|`created_at`|`TEXT`|`NOT NULL`|ISO 8601, set on insert, never updated|
|`updated_at`|`TEXT`|`NOT NULL`|ISO 8601, updated on every write|

> **Note:** SQLite has no native `boolean` or `datetime` types. Booleans are stored as `INTEGER` (`0`/`1`). Datetimes are stored as `TEXT` in ISO 8601 format (`2025-11-22T09:00:00`). Pydantic handles the conversion automatically on the way in and out.

### Table: `users`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID generated in Python on insert |
| `username` | TEXT | NOT NULL, UNIQUE | Login identifier |
| `hashed_password` | TEXT | NOT NULL | bcrypt hash — plaintext never stored |
| `created_at` | TEXT | NOT NULL | ISO 8601 timestamp |

---
# [API Docs]([[API docs]])
