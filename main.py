import tkinter as tk
from tkinter import ttk
from models import TodoModel
from views import TodoView
from controllers import TodoController
import os

class DesktopTodoApp:
    def __init__(self, master):
        self.master = master
        master.title("Desktop Todo")
        master.geometry("400x500")
        master.overrideredirect(True)  # 无边框
        master.attributes("-topmost", True) # 置顶
        master.attributes("-alpha", 0.9) # 透明度

        self.offset_x = 0
        self.offset_y = 0

        # 允许窗口拖动
        master.bind("<Button-1>", self.start_move)
        master.bind("<B1-Motion>", self.on_move)

        # Model, View, Controller setup
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        self.model = TodoModel(data_file=os.path.join(data_dir, "tasks.json"))
        self.view = TodoView(master)
        self.controller = TodoController(master, self.model, self.view, master.quit)

        # Theme setup
        self.style = ttk.Style()
        self.current_theme = "light"
        self.set_theme("light")

        # Context Menu for window controls
        self.context_menu = tk.Menu(master, tearoff=0)
        self.context_menu.add_command(label="置顶", command=self.toggle_topmost)
        self.context_menu.add_command(label="透明度 +", command=self.increase_alpha)
        self.context_menu.add_command(label="透明度 -", command=self.decrease_alpha)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="切换主题", command=self.toggle_theme)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="退出", command=master.quit)

        master.bind("<Button-3>", self.show_context_menu) # Right-click for context menu

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_move(self, event):
        x = self.master.winfo_x() + event.x - self.offset_x
        y = self.master.winfo_y() + event.y - self.offset_y
        self.master.geometry(f"+{x}+{y}")

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def toggle_topmost(self):
        current_topmost = self.master.attributes("-topmost")
        self.master.attributes("-topmost", not current_topmost)

    def increase_alpha(self):
        current_alpha = self.master.attributes("-alpha")
        if current_alpha < 1.0:
            new_alpha = min(1.0, current_alpha + 0.1)
            self.master.attributes("-alpha", new_alpha)

    def decrease_alpha(self):
        current_alpha = self.master.attributes("-alpha")
        if current_alpha > 0.4: # Minimum transparency level
            new_alpha = max(0.4, current_alpha - 0.1)
            self.master.attributes("-alpha", new_alpha)

    def set_theme(self, theme_name):
        if theme_name == "light":
            self.style.theme_use("clam") # A modern-looking theme
            self.style.configure("TFrame", background="#ADD8E6") # Light Blue
            self.style.configure("TButton", background="#FFA07A", foreground="#191970") # Orange button, Dark Blue text
            self.style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#000000") # White entry, Black text
            self.master.config(bg="#E0FFFF") # Light Cyan
            self.view.input_frame.config(bg="#ADD8E6") # Light Blue
            self.view.action_frame.config(bg="#ADD8E6") # Light Blue
            self.view.task_list.config(bg="#FFFFFF", fg="#36454F", selectbackground="#90EE90", selectforeground="#000000") # White list, Dark Grey text, Light Green selection
        elif theme_name == "dark":
            self.style.theme_use("clam")
            self.style.configure("TFrame", background="#6A0DAD") # Dark Orchid
            self.style.configure("TButton", background="#FFD700", foreground="#000000") # Gold button, Black text
            self.style.configure("TEntry", fieldbackground="#36454F", foreground="#FFFFFF") # Dark Grey entry, White text
            self.master.config(bg="#4B0082") # Indigo
            self.view.input_frame.config(bg="#6A0DAD") # Dark Orchid
            self.view.action_frame.config(bg="#6A0DAD") # Dark Orchid
            self.view.task_list.config(bg="#36454F", fg="#D3D3D3", selectbackground="#008080", selectforeground="#FFFFFF") # Dark Grey list, Light Grey text, Teal selection
        self.current_theme = theme_name

    def toggle_theme(self):
        if self.current_theme == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopTodoApp(root)
    root.mainloop()
