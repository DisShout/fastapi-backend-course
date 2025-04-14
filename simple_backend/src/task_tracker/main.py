from fastapi import FastAPI
from enum import Enum

class Status_task(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"



app = FastAPI()

tasks = []

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: str, status: Status_task = Status_task.NEW):
    task_id_counter = len(tasks)+1
    new_task = {'id': task_id_counter,'task': task, 'status': status.value}
    tasks.append(new_task)
    

@app.put("/tasks/{task_id}")
def update_task(task_id: int, up_task: str = None, up_status: Status_task = None):
    for task in tasks:
        if task['id'] == task_id:
            if up_task is not None:
                task['task'] = up_task
            if up_status is not None:
                task['status'] = up_status.value        
            return task
    raise ValueError('Задачи с таким id не существует')
        

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            
