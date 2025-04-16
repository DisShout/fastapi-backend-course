import requests
from enum import Enum


class StatusTask(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class JsonBinStorage:
    def __init__(self, api_key: str, bin_id: str):
        self.api_key = api_key
        self.bin_id = bin_id
        self.url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"
        self.headers = {
            "X-Master-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _read(self) -> list[dict]:
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.json()["record"]

    def _write(self, tasks: list[dict]) -> None:
        response = requests.put(self.url, headers=self.headers, json=tasks)
        response.raise_for_status()

    def _find_task_index(self, tasks: list[dict], task_id: int) -> int | None:
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                return index
        return None

    def get_all(self) -> list[dict]:
        tasks = self._read()
        return tasks

    def create(self, task_text: str, status: StatusTask = StatusTask.NEW) -> dict:
        tasks = self._read()
        new_id = max([x["id"] for x in tasks], default=0) + 1
        new_task = {"id": new_id, "task": task_text, "status": status.value}
        tasks.append(new_task)
        self._write(tasks)
        return new_task

    def update(
        self, task_id: int, text_task: str = None, status: StatusTask | None = None
    ) -> dict:
        tasks = self._read()
        index = self._find_task_index(tasks, task_id)
        if index is None:
            raise ValueError("Задача не найдена")
        if text_task is not None:
            tasks[index]["task"] = text_task
        if status is not None:
            tasks[index]["status"] = status.value

        self._write(tasks)
        return tasks[index]

    def delete(self, task_id: int) -> dict:
        tasks = self._read()
        index = self._find_task_index(tasks, task_id)
        if index is None:
            raise ValueError("Задача не найдена")

        tasks.remove(tasks[index])
        self._write(tasks)
        return {"message": "Задача удалена", "id": task_id}
