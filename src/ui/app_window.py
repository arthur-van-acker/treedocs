import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', relative_path)

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("2500x1250+10+10")
        self.iconbitmap(resource_path("assets/favicon.ico"))

        # Load folder icon
        try:
            from logic.icons import Icons
            self.folder_icon = Icons.load_folder_icon()
        except Exception:
            self.folder_icon = None

        # Taskbar frame below menu bar
        self.taskbar_frame = ctk.CTkFrame(self, fg_color="#e0e0e0")
        self.taskbar_frame.pack(fill="x")

        # Main content frame (horizontal layout)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Left pane for folder contents
        self.left_frame = ctk.CTkFrame(self.content_frame, fg_color="#f5f5f5", width=300)
        self.left_frame.pack(side="left", fill="y")
        self.folder_label_var = tk.StringVar()
        self.folder_label = ctk.CTkLabel(self.left_frame, textvariable=self.folder_label_var, anchor="w", font=("Segoe UI", 12, "bold"))
        self.folder_label.pack(fill="x", padx=10, pady=(10,0))
        self.button_frame = ctk.CTkFrame(self.left_frame, fg_color="#f5f5f5")
        self.button_frame.pack(fill="x", padx=10, pady=(2,0))
        # Replace ttk.Treeview with CTkTextbox for demonstration (CustomTkinter does not have a treeview, so use textbox or custom widget)
        self.folder_tree = ctk.CTkTextbox(self.left_frame)
        self.folder_tree.pack(fill="both", expand=True, padx=10, pady=(2,10))

        # Center pane
        self.center_frame = ctk.CTkFrame(self.content_frame, fg_color="#ffffff")
        self.center_frame.pack(side="left", fill="both", expand=True)
        self.line_numbers = ctk.CTkTextbox(self.center_frame, width=40)
        self.line_numbers.pack(side="left", fill="y")
        self.text_editor = ctk.CTkTextbox(self.center_frame)
        self.text_editor.pack(side="right", fill="both", expand=True)

        # Right pane
        self.right_frame = ctk.CTkFrame(self.content_frame, fg_color="#f5f5f5", width=300)
        self.right_frame.pack(side="left", fill="y")

        # Show initial folder contents (use current working directory)
        initial_folder = os.getcwd()
        self.show_folder_contents(initial_folder)

        # ...existing code...
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', relative_path)

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("2500x1250+10+10")
        self.iconbitmap(resource_path("assets/favicon.ico"))


        # Load folder icon
        try:
            from logic.icons import Icons
            self.folder_icon = Icons.load_folder_icon()
        except Exception:
            self.folder_icon = None

        # Taskbar frame below menu bar
        self.taskbar_frame = tk.Frame(self, bg="#e0e0e0")
        self.taskbar_frame.pack(fill="x")

        # PanedWindow for resizable panes
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=8, bg="#e0e0e0")


    # ...existing code...

    def start_auto_refresh(self, interval_ms=2000):
        from logic.file_ops import get_folder_snapshot
        self._last_snapshot = get_folder_snapshot(self.current_folder)
        self._auto_refresh_interval = interval_ms
        self._auto_refresh()

    def _auto_refresh(self):
        from logic.file_ops import get_folder_snapshot
        if not self.current_folder:
            self.after(self._auto_refresh_interval, self._auto_refresh)
            return
        current_snapshot = get_folder_snapshot(self.current_folder)
        if getattr(self, '_last_snapshot', None) != current_snapshot:
            self.show_folder_contents(self.current_folder)
            self._last_snapshot = current_snapshot
        self.after(self._auto_refresh_interval, self._auto_refresh)

    def show_folder_contents(self, folder):
        import os
        from logic.file_ops import insert_tree_items, get_folder_snapshot
        self.current_folder = folder
        self.folder_label_var.set(f"Workspace: {os.path.basename(folder)}")
        # Save expanded folder paths
        expanded_paths = set()
        def collect_expanded(item, path):
            if self.folder_tree.item(item, 'open'):
                expanded_paths.add(path)
            for child in self.folder_tree.get_children(item):
                child_name = self.folder_tree.item(child, 'text').strip()
                child_path = os.path.join(path, child_name)
                collect_expanded(child, child_path)
        for item in self.folder_tree.get_children():
            name = self.folder_tree.item(item, 'text').strip()
            collect_expanded(item, os.path.join(folder, name))
        # Clear tree
        self.folder_tree.delete(*self.folder_tree.get_children())
        # Insert tree items and keep a mapping from item to path
        self._item_to_path = {}
        def insert_items(path, parent, level=0):
            insert_tree_items(self.folder_tree, self.folder_icon, path, parent, level)
        insert_items(folder, "", 0)
        # Restore expanded state by path
        for item, path in getattr(self, '_item_to_path', {}).items():
            if path in expanded_paths:
                self.folder_tree.item(item, open=True)
        # At the end of show_folder_contents, update snapshot
        self._last_snapshot = get_folder_snapshot(folder)
