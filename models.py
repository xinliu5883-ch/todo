import json
import os
from datetime import datetime

class Task:
    def __init__(self, description, completed=False, created_at=None, task_id=None):
        self.task_id = task_id if task_id is not None else str(int(datetime.now().timestamp() * 1000))
        self.description = description
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["description"], data["completed"], data["created_at"], data["task_id"])

class TodoModel:
    def __init__(self, data_file="data/tasks.json"):
        self.data_file = data_file
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(data) for data in tasks_data]
                except json.JSONDecodeError:
                    self.tasks = []
        else:
            self.tasks = []

    def _save_tasks(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=4)

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)
        self._save_tasks()
        return task

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self._save_tasks()

    def update_task(self, task_id, new_description=None, new_completed=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if new_description is not None:
                    task.description = new_description
                if new_completed is not None:
                    task.completed = new_completed
                self._save_tasks()
                return task
        return None

    def get_all_tasks(self):
        return self.tasks

    def clear_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task.completed]
        self._save_tasks()

