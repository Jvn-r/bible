import { useState } from "react"

function TaskList({ tasks, onComplete, onDelete, onEdit }) {
  const [editingId, setEditingId] = useState(null)
  const [editData, setEditData] = useState({})

  function startEdit(task) {
    setEditingId(task.id)
    setEditData({
      title: task.title,
      priority: task.priority,
      difficulty: task.difficulty,
      duration: task.duration,
    })
  }

  function handleSave(id) {
    onEdit(id, editData)
    setEditingId(null)
    setEditData({})
  }

  if (tasks.length === 0) {
    return <p>No tasks yet.</p>
  }

  return (
    <ul>
      {tasks.map(task => (
        <li key={task.id}>
          {editingId === task.id ? (
            <>
              <input
                value={editData.title}
                onChange={e => setEditData({ ...editData, title: e.target.value })}
              />
              <select
                value={editData.priority}
                onChange={e => setEditData({ ...editData, priority: e.target.value })}
              >
                <option value="low">Low priority</option>
                <option value="moderate">Moderate priority</option>
                <option value="high">High priority</option>
              </select>
              <select
                value={editData.difficulty}
                onChange={e => setEditData({ ...editData, difficulty: e.target.value })}
              >
                <option value="low">Low difficulty</option>
                <option value="moderate">Moderate difficulty</option>
                <option value="high">High difficulty</option>
              </select>
              <input
                type="number"
                value={editData.duration}
                onChange={e => setEditData({ ...editData, duration: parseInt(e.target.value) })}
              />
              <button onClick={() => handleSave(task.id)}>Save</button>
              <button onClick={() => setEditingId(null)}>Cancel</button>
            </>
          ) : (
            <>
              <span>{task.title}</span>
              {" · "}
              <span>{task.priority} priority</span>
              {" · "}
              <span>{new Date(task.start_time).toLocaleString()}</span>
              {" · "}
              <span>{task.duration} mins</span>
              {" "}
              <button onClick={() => startEdit(task)}>Edit</button>
              {" "}
              <button onClick={() => onComplete(task.id)}>Complete</button>
              {" "}
              <button onClick={() => onDelete(task.id)}>Delete</button>
            </>
          )}
        </li>
      ))}
    </ul>
  )
}

export default TaskList