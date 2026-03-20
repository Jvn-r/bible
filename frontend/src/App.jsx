import { useState, useEffect } from "react"
import TaskForm from "./components/TaskForm"
import TaskList from "./components/TaskList"
import { getTasks, createTask, completeTask, deleteTask, updateTask } from "./api"
function App() {
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    fetchTasks()
  }, [])

  async function fetchTasks() {
    const data = await getTasks()
    setTasks(data)
  }

  async function handleTaskCreated(taskData) {
    await createTask(taskData)
    fetchTasks()
  }

  async function handleComplete(id) {
    await completeTask(id)
    fetchTasks()
  }

  async function handleDelete(id) {
    await deleteTask(id)
    fetchTasks()
  }

  async function handleEdit(id, data) {
  await updateTask(id, data)
  fetchTasks()
}

  return (
    <div>
      <h1>Bible</h1>
      <TaskForm onTaskCreated={handleTaskCreated} />
      <TaskList
        tasks={tasks}
        onComplete={handleComplete}
        onDelete={handleDelete}
        onEdit={handleEdit}
      />
    </div>
  )
}

export default App
