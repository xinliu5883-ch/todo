import tkinter as tk
from tkinter import ttk

class TodoView:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.create_widgets()

    def create_widgets(self):
        self.colors = {
            'main_bg': '#FCFCFC',
            'top_bg': '#F5F1ED',
            'title_text': '#5C5248',
            'normal_text': '#857A6F',
            'completed_text': '#B8AFA5',
            'primary_button': '#A07DFF',
            'primary_button_hover': '#8C6AF3',
            'delete_button': '#FF9F9F',
            'border': '#EAE5DF',
        }

        self.master.configure(bg=self.colors['main_bg'])

        self.input_frame = tk.Frame(self.master, bg=self.colors['top_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        self.input_frame.pack(pady=10, padx=10, fill=tk.X)

        style = ttk.Style()
        style.configure("Primary.TButton", background=self.colors['primary_button'], foreground="white")
        style.map("Primary.TButton", background=[("active", self.colors['primary_button_hover'])])

        self.task_input = tk.Entry(self.input_frame, font=("Arial", 12), bg=self.colors['main_bg'], fg=self.colors['normal_text'],
                                   insertbackground=self.colors['normal_text'], relief=tk.FLAT, bd=0)
        self.task_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10), pady=8)

        self.add_button = ttk.Button(self.input_frame, text="添加", style="Primary.TButton")
        self.add_button.pack(side=tk.RIGHT, padx=(0, 10), pady=5)

        self.list_frame = tk.Frame(self.master, bg=self.colors['main_bg'])
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.list_frame, bg=self.colors['main_bg'], bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.task_list = self.canvas

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.task_items = []
        self.selected_index = None

        self.canvas.bind("<Configure>", lambda e: self.redraw_tasks())
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.action_frame = tk.Frame(self.master, bg=self.colors['top_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        self.action_frame.pack(pady=10, padx=10, fill=tk.X)

        self.complete_button = ttk.Button(self.action_frame, text="标记完成", style="Primary.TButton")
        self.complete_button.pack(side=tk.LEFT, padx=(5, 5))

        style.configure("Delete.TButton", background=self.colors['delete_button'], foreground="white")
        style.map("Delete.TButton", background=[("active", self.colors['delete_button'])])

        self.delete_button = ttk.Button(self.action_frame, text="删除", style="Delete.TButton")
        self.delete_button.pack(side=tk.LEFT, padx=(5, 5))

        self.clear_completed_button = ttk.Button(self.action_frame, text="清空已完成")
        self.clear_completed_button.pack(side=tk.RIGHT, padx=(5, 5))

        self.exit_button = ttk.Button(self.action_frame, text="退出")
        self.exit_button.pack(side=tk.RIGHT, padx=(5, 5))

        self.add_task_callback = None
        self.complete_task_callback = None
        self.delete_task_callback = None
        self.clear_completed_callback = None
        self.edit_task_callback = None

    def set_callbacks(self, add_task_cb, complete_task_cb, delete_task_cb, clear_completed_cb, edit_task_cb, quit_app_cb):
        self.add_task_callback = add_task_cb
        self.complete_task_callback = complete_task_cb
        self.delete_task_callback = delete_task_cb
        self.clear_completed_callback = clear_completed_cb
        self.edit_task_callback = edit_task_cb
        self.quit_app_callback = quit_app_cb

        self.task_input.bind("<Return>", lambda event: self.add_task_callback())
        self.add_button.config(command=self.add_task_callback)
        self.complete_button.config(command=self.complete_task_callback)
        self.delete_button.config(command=self.delete_task_callback)
        self.clear_completed_button.config(command=self.clear_completed_callback)
        self.exit_button.config(command=self.quit_app_callback)

    def get_new_task_description(self):
        return self.task_input.get()

    def clear_new_task_input(self):
        self.task_input.delete(0, tk.END)

    def get_selected_task_index(self):
        return self.selected_index

    def on_canvas_click(self, event):
        y = self.canvas.canvasy(event.y)
        line_height = 30
        index = int((y - 10) / line_height)
        if 0 <= index < len(self.task_items):
            self.selected_index = index
            self.redraw_tasks()
        else:
            self.selected_index = None

    def redraw_tasks(self):
        self.canvas.delete("all")
        self.task_items = []
        y = 10
        line_height = 30
        canvas_width = self.canvas.winfo_width() or 380

        for i, task in enumerate(self.tasks):
            if self.selected_index == i:
                self.canvas.create_rectangle(0, y - 5, canvas_width, y + line_height - 5, fill=self.colors['primary_button'], outline="")

            display_text = f"[{'✓' if task.completed else ' '}] {task.description}"

            text_color = self.colors['completed_text'] if task.completed else self.colors['normal_text']
            if self.selected_index == i:
                text_color = "white"

            text_id = self.canvas.create_text(10, y, anchor="nw", text=display_text, font=("Arial", 12), fill=text_color)

            if task.completed:
                bbox = self.canvas.bbox(text_id)
                line_id = self.canvas.create_line(bbox[0], bbox[3] - 4, bbox[2], bbox[3] - 4, fill=text_color)
            else:
                line_id = None

            self.task_items.append((text_id, line_id, y))
            y += line_height

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def display_tasks(self, tasks):
        self.tasks = tasks
        self.redraw_tasks()

    def show_edit_dialog(self, current_description):
        dialog = tk.Toplevel(self.master)
        dialog.title("编辑任务")
        dialog.geometry("300x100")
        dialog.transient(self.master)
        dialog.grab_set()

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