from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4, UUID

app = FastAPI()

class User(BaseModel):
    username: str
    email: str
    password: str
class Task(BaseModel):
    title: str
    description: str
    status: str

users = {}
tasks = {}

# Registro de Usuarios
@app.post("/register/")
def register_user(user: User):
    user_id = uuid4()
    users[user_id] = user
    return {"message": "User registered successfully", "user_id": str(user_id)}

# Obtener Datos de Usuario
@app.get("/user/{user_id}/")
def get_user(user_id: UUID):
    if user_id in users:
        return users[user_id]
    raise HTTPException(status_code=404, detail="User not found")

# Crear Tareas
@app.post("/tasks/create/")
def create_task(task: Task, user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    task_id = uuid4()
    tasks[task_id] = {**task.dict(), "user_id": user_id}
    return {"message": "Task created successfully", "task_id": str(task_id)}

# Listar Tareas por Usuario
@app.get("/tasks/{user_id}/")
def get_tasks_by_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user_tasks = [task for task_id, task in tasks.items() if task["user_id"] == user_id]
    return user_tasks
