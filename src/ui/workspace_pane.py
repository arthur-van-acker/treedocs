import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from logic import WorkspaceConfig
import os

class WorkspacePane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=300, **kwargs)
        folder = WorkspaceConfig.load()
        workspace_name = os.path.basename(folder) if folder else "(none)"
        self.workspace_label = ctk.CTkLabel(self, text=f"Workspace: {workspace_name}", anchor="w")
        self.workspace_label.pack(fill="x", padx=5, pady=(5,0))

        # Treeview for workspace folder
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        if folder:
            self._populate_tree(folder)
        else:
            self.tree.insert("", "end", text="No workspace folder found")

    def _populate_tree(self, folder, parent=""):
        try:
            for entry in os.listdir(folder):
                path = os.path.join(folder, entry)
                node = self.tree.insert(parent, "end", text=entry, open=False)
                if os.path.isdir(path):
                    self._populate_tree(path, node)
        except Exception as e:
            self.tree.insert(parent, "end", text=f"Error: {e}")
