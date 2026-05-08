from models import TodoModel
from views import TodoView

class TodoController:
    def __init__(self, master, model: TodoModel, view: TodoView, quit_app_callback):
        self.master = master
        self.model = model
        self.view = view

        self.view.set_callbacks(
            self.add_task,
            self.complete_task,
            self.delete_task,
            self.clear_completed_tasks,
            self.edit_task,
            quit_app_callback
        )
        self.refresh_task_list()

    def add_task(self):
        description = self.view.get_new_task_description()
        if description:
            self.model.add_task(description)
            self.view.clear_new_task_input()
            self.refresh_task_list()

    def complete_task(self):
        selected_index = self.view.get_selected_task_index()
        if selected_index is not None:
            task_to_complete = self.model.get_all_tasks()[selected_index]
            self.model.update_task(task_to_complete.task_id, new_completed=not task_to_complete.completed)
            self.refresh_task_list()

    def delete_task(self):
        selected_index = self.view.get_selected_task_index()
        if selected_index is not None:
            task_to_delete = self.model.get_all_tasks()[selected_index]
            self.model.delete_task(task_to_delete.task_id)
            self.refresh_task_list()

    def edit_task(self):
        selected_index = self.view.get_selected_task_index()
        if selected_index is not None:
            task_to_edit = self.model.get_all_tasks()[selected_index]
            current_description = task_to_edit.description
            new_description = self.view.show_edit_dialog(current_description)
            if new_description and new_description != current_description:
                self.model.update_task(task_to_edit.task_id, new_description=new_description)
                self.refresh_task_list()

    def clear_completed_tasks(self):
        self.model.clear_completed_tasks()
        self.refresh_task_list()

    def refresh_task_list(self):
        tasks = self.model.get_all_tasks()
        self.view.display_tasks(tasks)
