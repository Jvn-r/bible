from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title : str
    description : str | None = None
    start_time: datetime
    end_time: datetime | None = None
    duration: int | None = None
    priority : str
    difficulty : str
    deadline : datetime | None = None
    is_completed : bool = False
    is_deleted : bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration: int | None = None
    priority: str | None = None
    difficulty: str | None = None
    deadline: datetime | None = None
    is_completed: bool | None = None
    is_deleted: bool | None = None

class Task(BaseModel):
    id: str
    user_id: str
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    duration: int 
    priority: str
    difficulty: str
    deadline: datetime | None
    is_completed: bool = False
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
