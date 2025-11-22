import tkinter as tk

class ContextMenus:
    def __init__(self, parent, open_workspace_cb, create_txt_cb, create_md_cb, open_selected_cb, edit_file_cb, rename_cb, delete_cb):
        # Workspace context menu
        self.workspace_context_menu = tk.Menu(parent, tearoff=0)
        self.workspace_context_menu.add_command(label="Open in Explorer", command=open_workspace_cb)
        self.workspace_context_menu.add_command(label="Create .txt file", command=create_txt_cb)
        self.workspace_context_menu.add_command(label="Create .md file", command=create_md_cb)

        # File context menu
        self.file_context_menu = tk.Menu(parent, tearoff=0)
        self.file_context_menu.add_command(label="Edit", command=edit_file_cb)
        self.file_context_menu.add_command(label="Open in Explorer", command=open_selected_cb)
        self.file_context_menu.add_command(label="Rename", command=rename_cb)
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="Delete", command=delete_cb)

        # Folder context menu
        self.folder_context_menu = tk.Menu(parent, tearoff=0)
        self.folder_context_menu.add_command(label="Open in Explorer", command=open_selected_cb)
        self.folder_context_menu.add_command(label="Rename", command=rename_cb)
        self.folder_context_menu.add_separator()
        self.folder_context_menu.add_command(label="Delete", command=delete_cb)
