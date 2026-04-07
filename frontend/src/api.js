const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

let token = null

export function setToken(t) { token = t }
export function getToken() { return token }

function authHeaders() {
  return {
    "Content-Type": "application/json",
    ...(token ? { "Authorization": `Bearer ${token}` } : {})
  }
}

export async function login(username, password) {
  const form = new URLSearchParams()
  form.append("username", username)
  form.append("password", password)

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    body: form
  })
  if (!res.ok) throw new Error("Invalid credentials")
  const data = await res.json()
  setToken(data.access_token)
  return data
}

export async function register(username, password) {
  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
  if (!res.ok) throw new Error("Registration failed")
  const data = await res.json()
  setToken(data.access_token)
  return data
}

export async function getTasks() {
  const res = await fetch(`${BASE_URL}/tasks/`, { headers: authHeaders() })
  return res.json()
}

export async function createTask(task) {
  const res = await fetch(`${BASE_URL}/tasks/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(task)
  })
  return res.json()
}

export async function completeTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}/complete`, {
    method: "PATCH",
    headers: authHeaders()
  })
  return res.json()
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "DELETE",
    headers: authHeaders()
  })
  return res.json()
}

export async function updateTask(id, data) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(data)
  })
  return res.json()
}
