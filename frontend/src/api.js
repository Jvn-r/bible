const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export async function getTasks() {
  const res = await fetch(`${BASE_URL}/tasks/`)
  return res.json()
}

export async function createTask(task) {
  const res = await fetch(`${BASE_URL}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task)
  })
  return res.json()
}

export async function completeTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}/complete`, { method: "PATCH" })
  return res.json()
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, { method: "DELETE" })
  return res.json()
}

export async function updateTask(id, data) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  return res.json()
}