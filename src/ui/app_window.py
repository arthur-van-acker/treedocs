import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("2500x1250+10+10")
        self.iconbitmap("src/assets/favicon.ico")

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
        self.left_frame.bind("<Button-3>", self.show_left_context_menu)

        self.file_context_menu = tk.Menu(self.left_frame, tearoff=0)
        self.file_context_menu.add_command(label="Rename", command=self.rename_selected_file)
        self.file_context_menu.add_command(label="Delete", command=self.delete_selected_file)
        self.folder_tree.bind("<Button-3>", self.show_tree_context_menu)

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

    def create_txt_file(self):
        # TODO: Implement using logic.file_ops
        pass

    def create_md_file(self):
        # TODO: Implement using logic.file_ops
        pass

    def create_folder(self):
        # TODO: Implement using logic.file_ops
        pass

    def rename_selected_file(self):
        # TODO: Implement using logic.file_ops
        pass

    def delete_selected_file(self):
        # TODO: Implement using logic.file_ops
        pass

    def load_workspace_from_config(self):
        from logic.workspace import WorkspaceConfig
        folder = WorkspaceConfig.load()
        if folder:
            self.show_folder_contents(folder)

    def show_folder_contents(self, folder):
        import os
        self.current_folder = folder
        self.folder_label_var.set(f"Workspace: {os.path.basename(folder)}")
        # Clear tree
        self.folder_tree.delete(*self.folder_tree.get_children())
        self._insert_tree_items(folder, "", 0)

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
