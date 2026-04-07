# BIBLE - Dynamic Scheduler

BIBLE is a personal productivity system that goes beyond a simple to-do list.
The end goal is a fully dynamic scheduler that considers your routine, orders tasks by priority and difficulty, and restructures your schedule automatically to optimize your day.

## Current Version — v1

---

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Database | SQLite |
| Frontend | React + Vite |
| Containerization | Docker |

---

## Project Structure

```
bible/
├── backend/
│   ├── main.py               — FastAPI app + all endpoints + business logic
│   ├── database.py           — SQLite connection + context manager + table init
│   ├── structs_pydantic.py   — Pydantic request/response models
│   ├── requirements.txt      — Python dependencies
│   └── Dockerfile            — Backend container definition
├── frontend/
│   ├── src/
│   │   ├── App.jsx           — Root component, state, data fetching
│   │   ├── api.js            — All fetch calls to the backend
│   │   └── components/
│   │       ├── TaskForm.jsx  — Create task form
│   │       └── TaskList.jsx  — Task list with edit, complete, delete
│   ├── .env                  — Local environment variables (gitignored)
│   ├── package.json
│   └── Dockerfile            — Frontend container definition
├── docs/
│   ├── API_DOCS.md           — Full API endpoint documentation
│   ├── DB_DOCS.md            — Database schema documentation
│   └── FRONTEND_DOCS.md      — Frontend structure and component documentation
├── data/                     — Local SQLite DB (gitignored)
├── docker-compose.yml        — Spins up the full stack
└── .gitignore
```

---

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Run the full stack

```bash
git clone https://github.com/Jvn-r/bible
cd bible
```

Create a `.env` file in the `frontend/` folder:

```
VITE_API_URL=http://localhost:8000
```

Then start everything:

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |

To stop: `Ctrl + C`, then `docker-compose down`

---

### Frontend dev workflow (active development only)

When actively working on the frontend, run it manually for hot reload instead of through Docker:

```bash
cd frontend
npm install
npm run dev
```

Keep the backend running via Docker in a separate terminal:

```bash
docker-compose up backend
```

---

## Environment Variables

### `backend/`

| Variable | Default | Description |
|---|---|---|
| `DB_PATH` | `bible.db` | Path to the SQLite database file |

Create a `.env` in `backend/` to override:
```
DB_PATH=/app/data/bible.db
```

### `frontend/`

| Variable | Default | Description |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000` | Backend API base URL |

Create a `.env` in `frontend/` to override:
```
VITE_API_URL=http://<your-ip>:8000
```

> On the Raspberry Pi, set `VITE_API_URL` to the Pi's local IP address so the frontend can reach the backend.

---

## Branches

| Branch | Purpose |
|---|---|
| `main` | Stable backend |
| `frontend` | React frontend — to-do MVP |

---

## API Overview

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive a JWT |

### Tasks (all protected — require Bearer token)
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
- [x] SQLite setup
- [x] Docker setup for full stack
- [x] React frontend — To-Do MVP (create, view, edit, complete, delete)
- [ ] Tailwind CSS styling
- [ ] Task filtering (completed, deleted, all)
- [x] Authentication
- [ ] Deploy to Raspberry Pi
- [ ] Timetable view
- [ ] Notifications
- [ ] Auto-schedule tasks into free time slots

---

## Docs

- [API Documentation](docs/API_docs.md)
- [Database Documentation](docs/DB_docs.md)
- [Frontend Documentation](docs/FRONTEND_docs.md)
