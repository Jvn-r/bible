# BIBLE - Dynamic Scheduler

BIBLE is a personal productivity system that goes beyond a simple to-do list.
The end goal is a fully dynamic scheduler that considers your routine, orders tasks by priority and difficulty, and restructures your tasks automatically to optimize your day.
## CURRENT VERSION - v1 

---
## Current Stack
- Backend - FastAPI
- Database - SQLite
- Frontend - React
- Extras - Docker
---
## Project Structure

```
bible/
├── backend/
│   ├── main.py               — FastAPI app + all endpoints
│   ├── database.py           — SQLite connection + table init
│   ├── structs_pydantic.py   — Pydantic request/response models
│   ├── requirements.txt      — Python dependencies
│   └── Dockerfile            — Container definition
├── frontend/                 — React app (in progress)
├── docs/
│   ├── API_DOCS.md           — Full API endpoint documentation
│   └── DB_DOCS.md            — Database schema documentation
├── data/                     — Local SQLite DB (gitignored)
├── docker-compose.yml        — Spins up the full stack
└── .gitignore
```

---
## Steps to run
- Swagger docs at `http://localhost:8000/docs`
### Docker - simplest
Make sure Docker is installed, then:
```bash
git clone <repo-url>
cd bible
mkdir data
docker-compose up --build
```
### FastAPI server
```bash
cd backend
python -m venv venv
source venv/bin/activate        #Windows: venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py
```
---
## API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/tasks/` | Create a task |
| `GET` | `/tasks/` | Get tasks (filterable) |
| `GET` | `/tasks/{id}` | Get task by ID |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Soft delete a task |
| `PATCH` | `/tasks/{id}/undelete` | Undo a delete |
| `PATCH` | `/tasks/{id}/complete` | Mark as complete |
| `PATCH` | `/tasks/{id}/incomplete` | Mark as incomplete |

Full documentation in `docs/API_DOCS.md`.

---
## Planned Features
- [x] FastAPI backend with full task CRUD
- [x] SQLite migration
- [x] Docker setup
- [ ] React frontend — To-Do MVP
- [ ] Authentication
- [ ] Deploy to Raspberry Pi
- [ ] Timetable 
- [ ] Notifications
- [ ] Auto add tasks to Free time slots

---
## Docs
- [API Documentation](docs/API_DOCS.md)
- [Database Documentation](docs/DB_DOCS.md)
---
## .env
- `DB_PATH = bible.db` - path to SQLite db
- Create a `.env` file in `backend/` to override:
```
DB_PATH=/app/data/bible.db
```
---
