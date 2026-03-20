import { useState } from "react"

function TaskForm({ onTaskCreated }) {
  const [title, setTitle] = useState("")
  const [priority, setPriority] = useState("moderate")
  const [difficulty, setDifficulty] = useState("moderate")
  const [startTime, setStartTime] = useState("")
  const [duration, setDuration] = useState("")

  function handleSubmit(e) {
    e.preventDefault()
    if (!title || !startTime || !duration) return

    onTaskCreated({
      title,
      priority,
      difficulty,
      start_time: new Date(startTime).toISOString(),
      duration: parseInt(duration)
    })

    setTitle("")
    setStartTime("")
    setDuration("")
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Task title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <input
        type="datetime-local"
        value={startTime}
        onChange={e => setStartTime(e.target.value)}
      />
      <input
        type="number"
        placeholder="Duration (minutes)"
        value={duration}
        onChange={e => setDuration(e.target.value)}
      />
      <select value={priority} onChange={e => setPriority(e.target.value)}>
        <option value="low">Low priority</option>
        <option value="moderate">Moderate priority</option>
        <option value="high">High priority</option>
      </select>
      <select value={difficulty} onChange={e => setDifficulty(e.target.value)}>
        <option value="low">Low difficulty</option>
        <option value="moderate">Moderate difficulty</option>
        <option value="high">High difficulty</option>
      </select>
      <button type="submit">Add Task</button>
    </form>
  )
}

export default TaskForm