import customtkinter as ctk
from tkinter import ttk
from logic import WorkspaceConfig
from ui_events.workspace_pane import on_tree_select, populate_tree
import os

class WorkspacePane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=300, **kwargs)
        folder = WorkspaceConfig.load()
        workspace_name = os.path.basename(folder) if folder else "(none)"
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        if folder:
            root_node = self.tree.insert("", "end", text=f"Workspace: {workspace_name}", open=True)
            self.tree.tag_configure('workspace_bold', font=('TkDefaultFont', 10, 'bold'))
            self.tree.item(root_node, tags=('workspace_bold',))
            populate_tree(self.tree, folder, root_node)
        else:
            self.tree.insert("", "end", text="No workspace folder found")

        # Bind selection event to store last selected folder
        self.tree.bind('<<TreeviewSelect>>', lambda _event: on_tree_select(self.tree))