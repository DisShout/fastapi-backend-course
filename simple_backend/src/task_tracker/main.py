from fastapi import FastAPI
from pydantic import BaseModel

from jsonbin_storage import JsonBinStorage, StatusTask
from config import settings


app = FastAPI()
storage = JsonBinStorage(api_key=settings.api_key, bin_id=settings.bin_id)


class TaskCreate(BaseModel):
    task_text: str
    status: StatusTask = StatusTask.NEW


class TaskUpdate(BaseModel):
    task_text: str | None = None
    status: StatusTask | None = None


class TaskResponse(BaseModel):
    id: int
    task: str
    status: StatusTask


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks() -> list:
    return storage.get_all()


@app.post("/tasks", response_model=TaskResponse)
def create_task(data: TaskCreate):
    return storage.create(data.task_text, data.status)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate):
    return storage.update(task_id, data.task_text, data.status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return storage.delete(task_id)
