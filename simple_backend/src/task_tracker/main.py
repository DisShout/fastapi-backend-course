from fastapi import FastAPI
from task_storage import TaskStorage, StatusTask


app = FastAPI()
storage = TaskStorage()


@app.get("/tasks")
def get_tasks() -> list:
    return storage.get_all()


@app.post("/tasks")
def create_task(task_text: str, status: StatusTask = StatusTask.NEW) -> dict:
    return storage.create(task_text, status)


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int, task_text: str | None = None, status: StatusTask | None = None
) -> dict:
    return storage.update(task_id, task_text, status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    return storage.delete(task_id)
