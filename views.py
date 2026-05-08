import tkinter as tk
from tkinter import ttk

class TodoView:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Input Frame (顶部输入)
        self.input_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.task_input = ttk.Entry(self.input_frame, font=("Arial", 12))
        self.task_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        # self.task_input.bind("<Return>", lambda event: self.add_task_callback()) # 绑定将在set_callbacks中完成

        self.add_button = ttk.Button(self.input_frame, text="添加") # command绑定将在set_callbacks中完成
        self.add_button.pack(side=tk.RIGHT)

        # Task List Frame (中间滚动列表)
        self.list_frame = tk.Frame(self.master)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.task_list = tk.Listbox(self.list_frame, font=("Arial", 12), selectmode=tk.SINGLE,
                                    height=15, bd=0, highlightthickness=0, relief=tk.FLAT)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.task_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=self.scrollbar.set)

        # Action Bar Frame (底部操作栏)
        self.action_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.action_frame.pack(pady=10, padx=10, fill=tk.X)

        self.complete_button = ttk.Button(self.action_frame, text="标记完成") # command绑定将在set_callbacks中完成
        self.complete_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = ttk.Button(self.action_frame, text="删除") # command绑定将在set_callbacks中完成
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_completed_button = ttk.Button(self.action_frame, text="清空已完成") # command绑定将在set_callbacks中完成
        self.clear_completed_button.pack(side=tk.RIGHT, padx=(5, 0))

        self.exit_button = ttk.Button(self.action_frame, text="退出") # command绑定将在set_callbacks中完成
        self.exit_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Callbacks (will be set by controller)
        self.add_task_callback = None
        self.complete_task_callback = None
        self.delete_task_callback = None
        self.clear_completed_callback = None
        self.edit_task_callback = None

                # self.task_list.bind("<Double-Button-1>", lambda event: self.edit_task_callback() if self.edit_task_callback else None) # 绑定将在set_callbacks中完成

    def set_callbacks(self, add_task_cb, complete_task_cb, delete_task_cb, clear_completed_cb, edit_task_cb, quit_app_cb):
        self.add_task_callback = add_task_cb
        self.complete_task_callback = complete_task_cb
        self.delete_task_callback = delete_task_cb
        self.clear_completed_callback = clear_completed_cb
        self.edit_task_callback = edit_task_cb
        self.quit_app_callback = quit_app_cb

        # Now bind the commands to the widgets
        self.task_input.bind("<Return>", lambda event: self.add_task_callback())
        self.add_button.config(command=self.add_task_callback)
        self.complete_button.config(command=self.complete_task_callback)
        self.delete_button.config(command=self.delete_task_callback)
        self.clear_completed_button.config(command=self.clear_completed_callback)
        self.exit_button.config(command=self.quit_app_callback)
        self.task_list.bind("<Double-Button-1>", lambda event: self.edit_task_callback())

    def get_new_task_description(self):
        return self.task_input.get()

    def clear_new_task_input(self):
        self.task_input.delete(0, tk.END)

    def get_selected_task_index(self):
        selected_indices = self.task_list.curselection()
        if selected_indices:
            return selected_indices[0]
        return None

    def display_tasks(self, tasks):
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(tasks):
            display_text = f"[{'✓' if task.completed else ' '}] {task.description}"
            self.task_list.insert(tk.END, display_text)
            if task.completed:
                self.task_list.itemconfig(i, fg="grey")

    def show_edit_dialog(self, current_description):
        dialog = tk.Toplevel(self.master)
        dialog.title("编辑任务")
        dialog.geometry("300x100")
        dialog.transient(self.master)  # Make dialog appear on top of main window
        dialog.grab_set()  # Modal window

        label = ttk.Label(dialog, text="新任务描述:")
        label.pack(pady=5)

        entry = ttk.Entry(dialog, width=40)
        entry.insert(0, current_description)
        entry.pack(pady=5)
        entry.focus_set()

        result = None

        def on_ok():
            nonlocal result
            result = entry.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        ok_button = ttk.Button(dialog, text="确定", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=10, pady=5)

        cancel_button = ttk.Button(dialog, text="取消", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.master.wait_window(dialog)
        return result
