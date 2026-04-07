from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from structs_pydantic import TaskCreate, TaskUpdate, Task, RegisterRequest, LoginRequest, TokenResponse
from database import get_db, init_db
from datetime import datetime, timedelta
from dateutil.parser import parse
from auth import get_current_user, hash_password, verify_password, create_access_token
import uuid

app = FastAPI(
    title="Bible v1",
    version="1.0"
)

# runs once on startup to create tables if they don't exist
@app.on_event("startup")
async def startup():
    init_db()

# CORS - open for now, lock down to your domain later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Working", "version": "1.0"}


def normalize_times(start_time, end_time, duration):
    if end_time is None and duration is None:
        raise HTTPException(
            status_code=400,
            detail="Must provide either end_time or duration"
        )

    if duration is not None and end_time is None:
        end_time = start_time + timedelta(minutes=duration)
    elif end_time is not None and duration is None:
        duration = int((end_time - start_time).total_seconds() / 60)

    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")

    return end_time, duration


def row_to_dict(row) -> dict:
    # sqlite3 rows are index-based by default, this converts them to dicts
    return dict(row)

@app.post("/auth/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest):
    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (body.username,)
        ).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

        user_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        db.execute(
            "INSERT INTO users (id, username, hashed_password, created_at) VALUES (?,?,?,?)",
            (user_id, body.username, hash_password(body.password), now)
        )

    token = create_access_token(user_id)
    return TokenResponse(access_token=token)



@app.post("/auth/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as db:
        row = db.execute(
            "SELECT id, hashed_password FROM users WHERE username = ?", (form_data.username,)
        ).fetchone() 

    if not row or not verify_password(form_data.password, row["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(row["id"])
    return TokenResponse(access_token=token)


@app.post("/tasks/", status_code=201, response_model=Task)
async def add_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    end_time, duration = normalize_times(task.start_time, task.end_time, task.duration)

    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    with get_db() as db:
        db.execute(
            """
            INSERT INTO tasks (
                id, user_id, title, description, start_time, end_time,
                duration, priority, difficulty, deadline,
                is_completed, is_deleted, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                current_user,
                task.title,
                task.description,
                task.start_time.isoformat(),
                end_time.isoformat(),
                duration,
                task.priority,
                task.difficulty,
                task.deadline.isoformat() if task.deadline else None,
                task.is_completed,
                task.is_deleted,
                now,
                now,
            )
        )
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    return row_to_dict(row)


@app.get("/tasks/")
async def get_tasks(
    current_user: str = Depends(get_current_user),
    completed: bool | None = None,
    deleted: bool | None = None,
    all: bool = False
):
    query = "SELECT * FROM tasks WHERE user_id = ?"
    params: list = [current_user]

    if not all:
        if completed is None and deleted is None:
            query += " AND is_completed = 0 AND is_deleted = 0"
        else:
            if completed is not None:
                query += " AND is_completed = ?"
                params.append(completed)
            if deleted is not None:
                query += " AND is_deleted = ?"
                params.append(deleted)

    with get_db() as db:
        rows = db.execute(query, params).fetchall()

    return [row_to_dict(r) for r in rows]


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: str, current_user: str = Depends(get_current_user)):
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"couldn't find task: {task_id}")
    if row["user_id"] != current_user:
        raise HTTPException(status_code=403, detail="Not authorised")

    return row_to_dict(row)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: str = Depends(get_current_user)):
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"couldn't find task: {task_id}")
        if row["user_id"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorised")

        db.execute(
            "UPDATE tasks SET is_deleted = 1, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), task_id)
        )

    return {"message": f"task: {task_id} deleted successfully"}


@app.patch("/tasks/{task_id}/undelete", response_model=Task)
async def undelete_task(task_id: str, current_user: str = Depends(get_current_user)):
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"couldn't find task: {task_id}")
        if row["user_id"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorised")
        if not row_to_dict(row)["is_deleted"]:
            raise HTTPException(status_code=400, detail="task is not deleted")

        db.execute(
            "UPDATE tasks SET is_deleted = 0, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), task_id)
        )
        updated = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    return row_to_dict(updated)


@app.patch("/tasks/{task_id}/complete", response_model=Task)
async def mark_as_complete(task_id: str, current_user: str = Depends(get_current_user)):
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"couldn't find task: {task_id}")
        if row["user_id"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorised")
        if row_to_dict(row)["is_deleted"]:
            raise HTTPException(status_code=400, detail="cannot complete a deleted task")

        db.execute(
            "UPDATE tasks SET is_completed = 1, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), task_id)
        )
        updated = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    return row_to_dict(updated)


@app.patch("/tasks/{task_id}/incomplete", response_model=Task)
async def mark_as_incomplete(task_id: str, current_user: str = Depends(get_current_user)):
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"couldn't find task: {task_id}")
        if row["user_id"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorised")
        if row_to_dict(row)["is_deleted"]:
            raise HTTPException(status_code=400, detail="cannot mark incomplete a deleted task")

        db.execute(
            "UPDATE tasks SET is_completed = 0, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), task_id)
        )
        updated = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    return row_to_dict(updated)


def convert_str_to_datetime(value):
    if isinstance(value, str):
        return parse(value)
    return value


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate, current_user: str = Depends(get_current_user)):
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        if row["user_id"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorised")

        existing_task = row_to_dict(row)

        if existing_task["is_deleted"]:
            raise HTTPException(status_code=400, detail="Cannot update a deleted task")

        new_data = task_update.model_dump(exclude_unset=True)

        if "start_time" in new_data or "end_time" in new_data or "duration" in new_data:
            new_start = convert_str_to_datetime(new_data.get("start_time") or existing_task["start_time"])
            new_end = convert_str_to_datetime(new_data.get("end_time") or existing_task["end_time"]) if new_data.get("end_time") or existing_task["end_time"] else None
            new_duration = new_data.get("duration")

            new_end, new_duration = normalize_times(new_start, new_end, new_duration)

            new_data["start_time"] = new_start.isoformat()
            new_data["end_time"] = new_end.isoformat()
            new_data["duration"] = new_duration

        new_data["updated_at"] = datetime.now().isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in new_data)
        values = list(new_data.values()) + [task_id]

        db.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
        updated = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    return row_to_dict(updated)

 
