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
        self.paned_window.pack(fill="both", expand=True)

        # Left pane for folder contents (min width 500px)
        self.left_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
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
        # Step 2: Bind double-click to print selected file path
        self.folder_tree.bind('<Double-1>', self.on_treeview_double_click)

        # Center and right panes (equal initial size, resizable)
        self.center_frame = ctk.CTkFrame(self.paned_window, fg_color="#ffffff")
        self.right_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
        self.paned_window.add(self.center_frame, minsize=100, width=1000)
        self.paned_window.add(self.right_frame, minsize=100, width=1000)

        # Step 1: Add a basic tk.Text widget to center pane
        self.text_editor = tk.Text(self.center_frame)
        self.text_editor.pack(fill="both", expand=True)
        # Load save icon for Save button
        try:
            save_icon_path = resource_path("assets/save.png")
            self.save_icon = tk.PhotoImage(file=save_icon_path)
        except Exception as e:
            print(f"[DEBUG] Failed to load save icon: {e}")
            self.save_icon = None
        self.save_button = tk.Button(self.taskbar_frame, image=self.save_icon, command=self.save_file_from_editor)
        self.save_button.pack(side="left", padx=4, pady=4)
        self.current_file_path = None

        # Menu bar setup
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open workspace ...", command=self.open_workspace)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit")
        menubar.add_cascade(label="Settings")
        menubar.add_cascade(label="Help")
        self.config(menu=menubar)

        # Workspace context menu for workspace actions
        self.workspace_context_menu = tk.Menu(self.left_frame, tearoff=0)
        self.workspace_context_menu.add_command(label="Open in Explorer", command=self.open_explorer_workspace)
        self.workspace_context_menu.add_command(label="Create .txt file", command=self.create_txt_file)
        self.workspace_context_menu.add_command(label="Create .md file", command=self.create_md_file)

        # Load workspace on startup
        self.load_workspace_from_config()
        # Start auto-refresh for treeview
        self.start_auto_refresh()

    def on_treeview_double_click(self, event):
        selected = self.folder_tree.selection()
        if not selected:
            print("[DEBUG] No item selected.")
            return
        item = selected[0]
        if not hasattr(self, '_item_to_path') or item not in self._item_to_path:
            print("[DEBUG] No path mapping for item.")
            return
        file_path = self._item_to_path[item]
        print(f"[DEBUG] Double-clicked file path: {file_path}")
        # Step 3: Load file content into text editor
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"[DEBUG] Text editor widget: {self.text_editor}")
                self.text_editor.delete('1.0', tk.END)
                self.text_editor.insert(tk.END, content)
                self.current_file_path = file_path
                print(f"[DEBUG] Inserted content into text editor.")
            except Exception as e:
                print(f"[DEBUG] Failed to load file: {e}")
        else:
            print("[DEBUG] Selected item is not a file.")

    def save_file_from_editor(self):
        if not self.current_file_path:
            print("[DEBUG] No file loaded to save.")
            return
        try:
            content = self.text_editor.get('1.0', tk.END)
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[DEBUG] Saved content to {self.current_file_path}")
        except Exception as e:
            print(f"[DEBUG] Failed to save file: {e}")

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

    def show_workspace_context_menu(self, event):
        # TODO: Use logic to determine current folder
        self.workspace_context_menu.tk_popup(event.x_root, event.y_root)

    def show_tree_context_menu(self, event):
        item_id = self.folder_tree.identify_row(event.y)
        if item_id:
            self.folder_tree.selection_set(item_id)
            # Determine if selected item is file or folder
            path = self._item_to_path.get(item_id)
            if path and os.path.isdir(path):
                self.folder_context_menu.tk_popup(event.x_root, event.y_root)
            else:
                self.file_context_menu.tk_popup(event.x_root, event.y_root)
        else:
            self.workspace_context_menu.tk_popup(event.x_root, event.y_root)
    def edit_selected_file(self):
        selected = self.folder_tree.selection()
        if not selected:
            return
        item = selected[0]
        if not hasattr(self, '_item_to_path') or item not in self._item_to_path:
            return
        file_path = self._item_to_path[item]
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_editor.delete('1.0', tk.END)
                self.text_editor.insert(tk.END, content)
                self.current_file_path = file_path
            except Exception:
                pass

    def create_txt_file(self, in_selected_folder=False):
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

    def start_auto_refresh(self, interval_ms=2000):
        self._last_snapshot = self._get_folder_snapshot(self.current_folder)
        self._auto_refresh_interval = interval_ms
        self._auto_refresh()

    def _get_folder_snapshot(self, folder):
        snapshot = set()
        for root, dirs, files in os.walk(folder):
            for d in dirs:
                snapshot.add(os.path.join(root, d))
            for f in files:
                snapshot.add(os.path.join(root, f))
        return snapshot

    def _auto_refresh(self):
        if not self.current_folder:
            self.after(self._auto_refresh_interval, self._auto_refresh)
            return
        current_snapshot = self._get_folder_snapshot(self.current_folder)
        if getattr(self, '_last_snapshot', None) != current_snapshot:
            self.show_folder_contents(self.current_folder)
            self._last_snapshot = current_snapshot
        self.after(self._auto_refresh_interval, self._auto_refresh)

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
        # At the end of show_folder_contents, update snapshot
        self._last_snapshot = self._get_folder_snapshot(folder)

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
