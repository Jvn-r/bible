# BIBLE v1 — Frontend Documentation

> Stack: React + Vite | Version: 1.0
> Dev server: `http://localhost:5173`
> Connects to backend at: `http://localhost:8000` (configurable via `.env`)

---

## Overview

The frontend is a React app built with Vite. It provides a to-do list UI that talks to the FastAPI backend. The current MVP supports creating, viewing, editing, completing, and deleting tasks.

---

## File Structure
```
frontend/
├── src/
│   ├── App.jsx           — Root component. Owns all state, auth flag, data fetching.
│   ├── api.js            — All fetch calls + token management.
│   └── components/
│       ├── LoginForm.jsx — Username/password form. Handles login and register.
│       ├── TaskForm.jsx  — Form for creating new tasks.
│       └── TaskList.jsx  — Renders the task list with inline editing.
├── .env                  — Environment variables (gitignored)
├── index.html
├── package.json
└── Dockerfile
```

---

## How it connects to the backend

All API calls go through `src/api.js`. The base URL is read from the `VITE_API_URL` environment variable, falling back to `http://localhost:8000` if not set.

```js
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"
```

This means you never hardcode URLs in components — always import from `api.js`. If the backend URL ever changes, you only update it in one place (`.env`).

### `.env` setup

Create a `.env` file in the `frontend/` folder:

```
VITE_API_URL=http://localhost:8000
```

On the Raspberry Pi, change this to the Pi's local IP:

```
VITE_API_URL=http://<pi-ip>:8000
```

> Any Vite environment variable must be prefixed with `VITE_` to be accessible in the app via `import.meta.env`.

---

## `api.js` — API layer

All backend communication lives here. Token is stored in a module-level variable
and attached to every request automatically.

| Function | Method | Endpoint | Description |
|---|---|---|---|
| `login(username, password)` | `POST` | `/auth/login` | Login, stores token |
| `register(username, password)` | `POST` | `/auth/register` | Register, stores token |
| `getTasks()` | `GET` | `/tasks/` | Fetch active tasks |
| `createTask(task)` | `POST` | `/tasks/` | Create a new task |
| `completeTask(id)` | `PATCH` | `/tasks/{id}/complete` | Mark complete |
| `deleteTask(id)` | `DELETE` | `/tasks/{id}` | Soft delete |
| `updateTask(id, data)` | `PUT` | `/tasks/{id}` | Update task fields |

**Token management:** `login()` and `register()` store the JWT automatically via `setToken()`.
All task functions call `authHeaders()` internally — components never touch the token directly.

**Note:** token is in-memory only. Refreshing the page logs the user out. Persistence via
localStorage is a planned future improvement.

---

## Components

### `App.jsx`

Root of the app. Owns all state including auth.

- `authed` boolean — false by default, flipped to true after successful login or register
- If `authed` is false → renders `LoginForm`
- If `authed` is true → renders task UI and fetches tasks
- `useEffect` only runs `fetchTasks()` when `authed` is true

---

### `LoginForm.jsx`

Shown when the user is not authenticated. Manages its own username, password, and error state.

**Props:**
| Prop | Type | Description |
|---|---|---|
| `onAuth` | function | Called after successful login or register — flips `authed` in `App` |

Both Login and Register buttons are present. On success, `onAuth()` is called.
On failure, a local error message is shown.

---

### `TaskForm.jsx`

A controlled form for creating new tasks. Manages its own local state for each field using `useState`. On submit, calls `onTaskCreated` (passed from `App`) with the form data, then resets all fields.

**Fields:**
| Field | Input type | Notes |
|---|---|---|
| Title | text | Required |
| Start time | datetime-local | Required. Converted to ISO string on submit. |
| Duration | number | Required. In minutes. |
| Priority | select | `low`, `moderate`, `high` |
| Difficulty | select | `low`, `moderate`, `high` |

**Props:**
| Prop | Type | Description |
|---|---|---|
| `onTaskCreated` | function | Called with form data object on submit |

---

### `TaskList.jsx`

Renders the list of tasks. Handles inline editing — when a user clicks Edit on a task, that row switches into an editable state with inputs pre-filled with the current values. Clicking Save calls `onEdit`, clicking Cancel reverts.

Editing state is managed locally inside `TaskList` using `editingId` (which task is being edited) and `editData` (the current values of the edit form).

**Editable fields:** title, priority, difficulty, duration.

**Display format per task:**
```
{title} · {priority} priority · {start_time} · {duration} mins  [Edit] [Complete] [Delete]
```

**Props:**
| Prop | Type | Description |
|---|---|---|
| `tasks` | array | List of task objects from the backend |
| `onComplete` | function | Called with task `id` when Complete is clicked |
| `onDelete` | function | Called with task `id` when Delete is clicked |
| `onEdit` | function | Called with `(id, updatedData)` when Save is clicked |

---

## Running locally

### With Docker (recommended)

```bash
docker-compose up --build
```

Frontend available at `http://localhost:5173`.

### Manually (for active frontend development)

```bash
cd frontend
npm install
npm run dev
```

Run the backend separately:

```bash
docker-compose up backend
```

Hot reload is active — changes to any file in `src/` update the browser instantly without a refresh.

---

## Notes for teammates

- **Never call `fetch` directly in a component.** Always add a function to `api.js` and import it. Keeps all backend communication in one place.
- **State lives in `App.jsx`.** Components are mostly stateless — they receive data as props and call handler functions. The exception is `TaskList`, which manages its own local editing state.
- **Re-fetching after mutations.** After any create/edit/delete/complete, `App` calls `fetchTasks()` again to sync with the backend. This is simple and reliable for now — can be optimised later with optimistic updates if needed.
- **CORS is wide open on the backend** (`allow_origins=["*"]`). This is fine for local dev but needs to be locked down before any public deployment.
- **Token lives in `api.js`, not in components.** Never import or manipulate the token
  outside of `api.js`. Use `login()` and `register()` — they handle storage automatically.
- **Refreshing logs you out.** Token is in-memory only by design for now.
