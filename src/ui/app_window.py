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

        # PanedWindow for resizable panes
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=8, bg="#e0e0e0")
        self.paned_window.pack(fill="both", expand=True)

        # Left pane for folder contents (min width 500px)
        self.left_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=300)
        self.paned_window.add(self.left_frame, minsize=300)
        self.folder_label_var = tk.StringVar()
        self.folder_label = tk.Label(self.left_frame, textvariable=self.folder_label_var, bg="#f5f5f5", anchor="w", font=("Segoe UI", 12, "bold"))
        self.folder_label.pack(fill="x", padx=10, pady=(10,0))
        self.button_frame = tk.Frame(self.left_frame, bg="#f5f5f5")
        self.button_frame.pack(fill="x", padx=10, pady=(2,0))
        # + and - buttons removed, but button_frame remains for layout
        self.folder_tree = ttk.Treeview(self.left_frame)
        self.folder_tree.pack(fill="both", expand=True, padx=10, pady=(2,10))

        # Center and right panes (equal initial size, resizable)
        self.center_frame = ctk.CTkFrame(self.paned_window, fg_color="#ffffff")
        self.right_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
        self.paned_window.add(self.center_frame, minsize=100, width=1000)
        self.paned_window.add(self.right_frame, minsize=100, width=1000)

        # Menu bar setup
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open workspace ...", command=self.open_workspace)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit")
        menubar.add_cascade(label="Settings")
        menubar.add_cascade(label="Help")
        self.config(menu=menubar)

        # Context menu for creating files
        self.left_context_menu = tk.Menu(self.left_frame, tearoff=0)
        self.left_context_menu.add_command(label="New .txt file", command=self.create_txt_file)
        self.left_context_menu.add_command(label="New .md file", command=self.create_md_file)
        self.left_context_menu.add_command(label="New folder", command=self.create_folder)
        self.left_context_menu.add_separator()
        self.left_context_menu.add_command(label="Open explorer", command=lambda: self.open_explorer_workspace())
        self.left_frame.bind("<Button-3>", self.show_left_context_menu)

        self.file_context_menu = tk.Menu(self.left_frame, tearoff=0)
        self.file_context_menu.add_command(label="New .txt file", command=lambda: self.create_txt_file(in_selected_folder=True))
        self.file_context_menu.add_command(label="New .md file", command=lambda: self.create_md_file(in_selected_folder=True))
        self.file_context_menu.add_command(label="New folder", command=lambda: self.create_folder(in_selected_folder=True))
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="Open explorer", command=self.open_explorer_selected)
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="Rename", command=self.rename_selected_file)
        self.file_context_menu.add_command(label="Delete", command=self.delete_selected_file)
        self.folder_tree.bind("<Button-3>", self.show_tree_context_menu)

        # Load workspace on startup
        self.load_workspace_from_config()
    def open_explorer_workspace(self):
        import subprocess
        import platform
        folder = getattr(self, 'current_folder', None)
        # Normalize path for Windows
        if folder and platform.system() == "Windows":
            folder = os.path.normpath(folder)
        print(f"[DEBUG] Open workspace explorer path: {folder}")  # Debug output
        if folder and os.path.exists(folder):
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{folder}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        else:
            tk.messagebox.showerror("Error", f"Workspace path does not exist: {folder}")

    def open_explorer_selected(self):
        import subprocess
        import platform
        selected = self.folder_tree.selection()
        # Always fallback to workspace root if nothing is selected
        target_path = self.current_folder
        if selected:
            item = selected[0]
            if hasattr(self, '_item_to_path') and item in self._item_to_path:
                target_path = self._item_to_path[item]
        # Normalize path for Windows
        if target_path and platform.system() == "Windows":
            target_path = os.path.normpath(target_path)
        print(f"[DEBUG] Open explorer path: {target_path}")  # Debug output
        if target_path and os.path.exists(target_path):
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{target_path}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", target_path])
            else:
                subprocess.Popen(["xdg-open", target_path])
        else:
            tk.messagebox.showerror("Error", f"Path does not exist: {target_path}")

        self.current_folder = None
        self.load_workspace_from_config()

    def open_workspace(self):
        from ui.dialogs import Dialogs
        from logic.workspace import WorkspaceConfig
        folder_selected = Dialogs.select_folder()
        if folder_selected:
            WorkspaceConfig.save(folder_selected)
            self.show_folder_contents(folder_selected)

    def show_left_context_menu(self, event):
        # TODO: Use logic to determine current folder
        self.left_context_menu.tk_popup(event.x_root, event.y_root)

    def show_tree_context_menu(self, event):
        # TODO: Use logic to determine selected file/folder
        item_id = self.folder_tree.identify_row(event.y)
        if item_id:
            self.folder_tree.selection_set(item_id)
            self.file_context_menu.tk_popup(event.x_root, event.y_root)
        else:
            self.left_context_menu.tk_popup(event.x_root, event.y_root)

    def create_txt_file(self, in_selected_folder=False):
        from logic.file_ops import FileOps
        import tkinter.simpledialog
        target_folder = self.current_folder
        if in_selected_folder:
            selected = self.folder_tree.selection()
            if selected:
                item = selected[0]
                name = self.folder_tree.item(item, "text").strip()
                path = os.path.join(self.current_folder, name)
                if os.path.isdir(path):
                    target_folder = path
        if not target_folder:
            return
        filename = tkinter.simpledialog.askstring("New .txt file", "Enter file name:", parent=self)
        if filename:
            if not filename.endswith(".txt"):
                filename += ".txt"
            file_path = os.path.join(target_folder, filename)
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("")
                self.show_folder_contents(self.current_folder)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to create file: {e}")

    def create_md_file(self, in_selected_folder=False):
        from logic.file_ops import FileOps
        import tkinter.simpledialog
        target_folder = self.current_folder
        if in_selected_folder:
            selected = self.folder_tree.selection()
            if selected:
                item = selected[0]
                name = self.folder_tree.item(item, "text").strip()
                path = os.path.join(self.current_folder, name)
                if os.path.isdir(path):
                    target_folder = path
        if not target_folder:
            return
        filename = tkinter.simpledialog.askstring("New .md file", "Enter file name:", parent=self)
        if filename:
            if not filename.endswith(".md"):
                filename += ".md"
            file_path = os.path.join(target_folder, filename)
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("")
                self.show_folder_contents(self.current_folder)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to create file: {e}")

    def create_folder(self, in_selected_folder=False):
        from logic.file_ops import FileOps
        import tkinter.simpledialog
        target_folder = self.current_folder
        if in_selected_folder:
            selected = self.folder_tree.selection()
            if selected:
                item = selected[0]
                name = self.folder_tree.item(item, "text").strip()
                path = os.path.join(self.current_folder, name)
                if os.path.isdir(path):
                    target_folder = path
        if not target_folder:
            return
        foldername = tkinter.simpledialog.askstring("New folder", "Enter folder name:", parent=self)
        if foldername:
            folder_path = os.path.join(target_folder, foldername)
            if FileOps.create_folder(folder_path):
                self.show_folder_contents(self.current_folder)
            else:
                tk.messagebox.showerror("Error", "Failed to create folder.")

    def rename_selected_file(self):
        from logic.file_ops import FileOps
        import tkinter.simpledialog
        selected = self.folder_tree.selection()
        if not selected:
            return
        item = selected[0]
        old_name = self.folder_tree.item(item, "text").strip()
        old_path = os.path.join(self.current_folder, old_name)
        new_name = tkinter.simpledialog.askstring("Rename", f"Enter new name for '{old_name}':", parent=self)
        if new_name and new_name != old_name:
            new_path = os.path.join(self.current_folder, new_name)
            try:
                os.rename(old_path, new_path)
                self.show_folder_contents(self.current_folder)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to rename: {e}")

    def delete_selected_file(self):
        from logic.file_ops import FileOps
        import shutil
        selected = self.folder_tree.selection()
        if not selected:
            return
        item = selected[0]
        name = self.folder_tree.item(item, "text").strip()
        path = os.path.join(self.current_folder, name)
        confirm = tk.messagebox.askyesno("Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.show_folder_contents(self.current_folder)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to delete: {e}")

    def load_workspace_from_config(self):
        from logic.workspace import WorkspaceConfig
        folder = WorkspaceConfig.load()
        if folder:
            self.show_folder_contents(folder)

    def show_folder_contents(self, folder):
        import os
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
            try:
                items = sorted(os.listdir(path))
                dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
                files = [item for item in items if not os.path.isdir(os.path.join(path, item))]
                indent = "    " * level
                for d in dirs:
                    abs_path = os.path.join(path, d)
                    display_text = f"{indent}{d}"
                    node_id = self.folder_tree.insert(parent, "end", text=display_text, image=self.folder_icon if self.folder_icon else "", open=False)
                    self._item_to_path[node_id] = abs_path
                    insert_items(abs_path, node_id, level + 1)
                for f in files:
                    abs_path = os.path.join(path, f)
                    display_text = f"{indent}{f}"
                    node_id = self.folder_tree.insert(parent, "end", text=display_text, open=False)
                    self._item_to_path[node_id] = abs_path
            except Exception as e:
                print(f"Failed to list folder tree: {e}")
        insert_items(folder, "", 0)
        # Restore expanded state by path
        for item, path in getattr(self, '_item_to_path', {}).items():
            if path in expanded_paths:
                self.folder_tree.item(item, open=True)

    def _insert_tree_items(self, path, parent, level=0):
        import os
        try:
            items = sorted(os.listdir(path))
            dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
            files = [item for item in items if not os.path.isdir(os.path.join(path, item))]
            indent = "    " * level
            for d in dirs:
                abs_path = os.path.join(path, d)
                display_text = f"{indent}{d}"
                node_id = self.folder_tree.insert(parent, "end", text=display_text, image=self.folder_icon if self.folder_icon else "", open=False)
                self._insert_tree_items(abs_path, node_id, level + 1)
            for f in files:
                display_text = f"{indent}{f}"
                self.folder_tree.insert(parent, "end", text=display_text, open=False)
        except Exception as e:
            print(f"Failed to list folder tree: {e}")
