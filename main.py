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
            self.style.theme_use("clam")
            self.style.configure("TFrame", background="#F7F8FA")
            self.style.configure("TButton", background="#4263FF", foreground="white")
            self.style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#4E5969")
            self.master.config(bg="#FFFFFF")
            self.view.input_frame.config(bg="#F7F8FA")
            self.view.action_frame.config(bg="#F7F8FA")
            self.view.canvas.config(bg="#FFFFFF")
            self.view.colors['main_bg'] = '#FFFFFF'
            self.view.colors['top_bg'] = '#F7F8FA'
            self.view.colors['normal_text'] = '#4E5969'
            self.view.colors['completed_text'] = '#A0AABC'
        elif theme_name == "dark":
            self.style.theme_use("clam")
            self.style.configure("TFrame", background="#2A2D34")
            self.style.configure("TButton", background="#4263FF", foreground="white")
            self.style.configure("TEntry", fieldbackground="#36454F", foreground="#D3D3D3")
            self.master.config(bg="#1A1D21")
            self.view.input_frame.config(bg="#2A2D34")
            self.view.action_frame.config(bg="#2A2D34")
            self.view.canvas.config(bg="#1A1D21")
            self.view.colors['main_bg'] = '#1A1D21'
            self.view.colors['top_bg'] = '#2A2D34'
            self.view.colors['normal_text'] = '#D3D3D3'
            self.view.colors['completed_text'] = '#6B7280'
        self.current_theme = theme_name
        self.view.redraw_tasks()

    def toggle_theme(self):
        if self.current_theme == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopTodoApp(root)
    root.mainloop()
