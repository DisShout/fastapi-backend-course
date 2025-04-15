from fastapi import FastAPI
from enum import Enum
import json
import os

class StatusTask(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"

def generate_new_id(tasks: list) -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


FILE_PATH = "tasks.json"

def read_tasks_from_file()  -> list:
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        return [] 
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def write_tasks_to_file(tasks: list) -> None:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


app = FastAPI()

@app.get("/tasks")
def get_tasks() -> list:
    return read_tasks_from_file()

@app.post("/tasks")
def create_task(task: str, status: StatusTask = StatusTask.NEW) -> dict:
    tasks = read_tasks_from_file()

    new_id = generate_new_id(tasks)
    new_task = {'id': new_id,'task': task, 'status': status.value}
    tasks.append(new_task)

    write_tasks_to_file(tasks)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, up_task: str|None = None, up_status: StatusTask|None = None) -> dict:
    tasks = read_tasks_from_file()

    for task in tasks:
        if task['id'] == task_id:
            if up_task is not None:
                task['task'] = up_task
            if up_status is not None:
                task['status'] = up_status.value

            write_tasks_to_file(tasks)        
            return task
        
    raise ValueError('Задачи с таким id не существует')
        

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    tasks = read_tasks_from_file()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)       
            write_tasks_to_file(tasks)
            return {"message": "Задача удалена", "id": task_id}
        
    raise ValueError('Задачи с таким id не существует')       
