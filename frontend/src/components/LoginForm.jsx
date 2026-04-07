import { useState } from "react"
import { login, register } from "../api"

export default function LoginForm({ onAuth }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)

  async function handleLogin() {
    try {
      await login(username, password)
      onAuth()
    } catch {
      setError("Invalid credentials")
    }
  }

  async function handleRegister() {
    try {
      await register(username, password)
      onAuth()
    } catch {
      setError("Registration failed")
    }
  }

  return (
    <div>
      <h2>Bible</h2>
      {error && <p>{error}</p>}
      <input
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleRegister}>Register</button>
    </div>
  )
}
