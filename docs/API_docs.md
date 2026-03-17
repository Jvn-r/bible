# Bible v1 — Backend Documentation

> Stack: FastAPI + SQLite | Version: 1.0 Base URL (local): `http://localhost:8000` Base URL (Docker): `http://localhost:8000` Interactive docs: `http://localhost:8000/docs`

---
## File Structure
```
bible/
├──backend/
|	├── main.py             — FastAPI app, all endpoints, business logic
|	├── database.py         — SQLite connection, context manager,table initializer 
|	├── structs_pydantic.py — Pydantic models (request/response shapes)
|	├── requirements.txt    — Python dependencies
|	└── Dockerfile          — Container definition
└──data/
	└──bible.db
```
---
## Pydantic Models (`structs_pydantic.py`)

Pydantic models define the shape of data coming in and going out of the API. FastAPI uses these to automatically validate requests and serialize responses. Think of them as contracts between the frontend and the backend.
Theyre basically just structs 

---
### `TaskCreate` Model : used when creating a task (POST body)

| Field          | Type               | Required | Default | Notes                                |
| -------------- | ------------------ | -------- | ------- | ------------------------------------ |
| `title`        | `str`              | Y        | ---     | Task name                            |
| `description`  | `str \| None`      | N        | `None`  | Optional details                     |
| `start_time`   | `datetime`         | Y        | ---     | ISO format                           |
| `end_time`     | `datetime \| None` | N        | `None`  | Provide this OR duration             |
| `duration`     | `int \| None`      | N        | `None`  | In minutes. Provide this OR end_time |
| `priority`     | `str`              | Y        | ---     | `"low"`, `"moderate"`, `"high"`      |
| `difficulty`   | `str`              | Y        | ---     | `"low"`, `"moderate"`, `"high"`      |
| `deadline`     | `datetime \| None` | N        | `None`  | Optional hard deadline               |
| `is_completed` | `bool`             | N        | `false` | Usually left as default on create    |
| `is_deleted`   | `bool`             | N        | `false` | Usually left as default on create    |

> **Rule:** You must provide either `end_time` or `duration`. Not both, not neither. If you provide `duration`, `end_time` is calculated automatically. If you provide `end_time`, `duration` is calculated automatically.

---
### `TaskUpdate` Model - used when updating a task (PUT body)

All fields are optional. Only send what you want to change.

|Field|Type|
|---|---|
|`title`|`str \| None`|
|`description`|`str \| None`|
|`start_time`|`datetime \| None`|
|`end_time`|`datetime \| None`|
|`duration`|`int \| None`|
|`priority`|`str \| None`|
|`difficulty`|`str \| None`|
|`deadline`|`datetime \| None`|
|`is_completed`|`bool \| None`|
|`is_deleted`|`bool \| None`|

> If you change `start_time`, `end_time`, or `duration`, all three are recalculated automatically.

---
### `Task` Model - the full task object returned by the API (response shape)

|Field|Type|Notes|
|---|---|---|
|`id`|`str`|UUID, generated on creation|
|`user_id`|`str`|Currently hardcoded `"default_user"` — will be real user ID after auth|
|`title`|`str`||
|`description`|`str \| None`||
|`start_time`|`datetime`||
|`end_time`|`datetime`||
|`duration`|`int`|In minutes|
|`priority`|`str`||
|`difficulty`|`str`||
|`deadline`|`datetime \| None`||
|`is_completed`|`bool`||
|`is_deleted`|`bool`||
|`created_at`|`datetime`|Set on creation, never changes|
|`updated_at`|`datetime`|Updated on every write operation|

---
## API Endpoints (`main.py`)

---
### `GET /`

Health check. Confirms the server is running.

**Response**

```json
{
  "message": "Working",
  "version": "1.0"
}
```

---
### `POST /tasks/`

Create a new task.
**Status:** `201 Created` **Request body:** `TaskCreate` **Response:** `Task
`
**Example request**

```json
{
  "title": "Study for exam",
  "priority": "high",
  "difficulty": "moderate",
  "start_time": "2025-11-22T09:00:00",
  "duration": 90
}
```

**Example response**

```json
{
  "id": "3f7a9c12-...",
  "user_id": "default_user",
  "title": "Study for exam",
  "description": null,
  "start_time": "2025-11-22T09:00:00",
  "end_time": "2025-11-22T10:30:00",
  "duration": 90,
  "priority": "high",
  "difficulty": "moderate",
  "deadline": null,
  "is_completed": false,
  "is_deleted": false,
  "created_at": "2025-11-22T08:55:00",
  "updated_at": "2025-11-22T08:55:00"
}
```

**Errors**

| Code  | Reason                                     |
| ----- | ------------------------------------------ |
| `400` | Neither `end_time` nor `duration` provided |
| `400` | `end_time` is before `start_time`          |

---
### `GET /tasks/`

Get a list of tasks. By default returns only active (not completed, not deleted) tasks.

**Query parameters**

|Param|Type|Default|Description|
|---|---|---|---|
|`user_id`|`str`|`"default_user"`|Filter by user|
|`completed`|`bool \| None`|`None`|Filter by completion status|
|`deleted`|`bool \| None`|`None`|Filter by deletion status|
|`all`|`bool`|`false`|If true, return everything regardless of status|

**Default behaviour (no params):** returns tasks where `is_completed = false` AND `is_deleted = false`

**Examples**

```
GET /tasks/                          → active tasks only
GET /tasks/?completed=true           → completed tasks only
GET /tasks/?deleted=true             → deleted tasks only
GET /tasks/?all=true                 → every task in the DB
GET /tasks/?completed=true&deleted=false → completed but not deleted
```
**Response:** array of `Task`

---
### `GET /tasks/{task_id}`

Get a single task by its ID.
**Path param:** `task_id` — UUID string

**Response:** `Task`

**Errors**

|Code|Reason|
|---|---|
|`404`|Task not found|

---
### `DELETE /tasks/{task_id}`

[Soft delete]([[API docs#Soft Deletes]]) a task. Sets `is_deleted = true`. Does not remove from DB.
**Path param:** `task_id` — UUID string

**Response**

```json
{ "message": "task: <id> deleted successfully" }
```

**Errors**

|Code|Reason|
|---|---|
|`404`|Task not found|

---
### `PATCH /tasks/{task_id}/undelete`

Undo a [Soft delete]([[API docs#Soft Deletes]]). Sets `is_deleted = false`.
**Path param:** `task_id` — UUID string

**Response:** `Task`

**Errors**

|Code|Reason|
|---|---|
|`404`|Task not found|
|`400`|Task is not deleted|

---
### `PATCH /tasks/{task_id}/complete`

Mark a task as completed. Sets `is_completed = true`.
**Path param:** `task_id` — UUID string

**Response:** `Task`

**Errors**

| Code  | Reason                                           |
| ----- | ------------------------------------------------ |
| `404` | Task not found                                   |
| `400` | Task is deleted — cannot complete a deleted task |

---
### `PATCH /tasks/{task_id}/incomplete`

Mark a completed task as incomplete. Sets `is_completed = false`.
**Path param:** `task_id` — UUID string

**Response:** `Task`

**Errors**

| Code  | Reason          |
| ----- | --------------- |
| `404` | Task not found  |
| `400` | Task is deleted |

---
### `PUT /tasks/{task_id}`

Full update on a task. Send only the fields you want to change.
**Path param:** `task_id` — UUID string **Request body:** `TaskUpdate` **Response:** `Task`

**Time recalculation rules:** If any of `start_time`, `end_time`, or `duration` are included in the update, all three are recalculated consistently. Same rules as creation apply.

**Errors**

| Code  | Reason                                         |
| ----- | ---------------------------------------------- |
| `404` | Task not found                                 |
| `400` | Task is deleted — cannot update a deleted task |
| `400` | Time validation failed                         |
| `500` | DB update failed                               |

---
## Weird Fixes Note

### `normalize_times()`

Helper function in `main.py`. Called on every create and time-related update.

- If only `duration` given -> calculates `end_time = start_time + duration`
- If only `end_time` given -> calculates `duration` from the difference
- Validates `end_time > start_time`
- Raises `HTTP 400` if neither is provided or if times are invalid

### `row_to_dict()`

SQLite rows are not dicts by default. This helper converts them so Pydantic can serialize them into the `Task` response model.

### Soft Deletes

Tasks are never hard deleted from the database. `DELETE /tasks/{id}` sets `is_deleted = 1`. `PATCH /tasks/{id}/undelete` sets it back to `0`.

This means all data is always recoverable. The default `GET /tasks/` query filters out deleted tasks automatically.

---
## Auth Note
Everything currently uses `user_id = "default_user"` hardcoded. When Auth lands, this gets replaced with the actual authenticated user's ID. Every endpoint that reads or writes tasks will need to pull `user_id` from the auth token instead. The DB schema is already ready for it — `user_id` column exists on every row.

---
## [Database Docs]([[Database docs]])
