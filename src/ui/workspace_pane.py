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
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        if folder:
            root_node = self.tree.insert("", "end", text=f"Workspace: {workspace_name}", open=True)
            self.tree.tag_configure('workspace_bold', font=('TkDefaultFont', 10, 'bold'))
            self.tree.item(root_node, tags=('workspace_bold',))
            self._populate_tree(folder, root_node)
        else:
            self.tree.insert("", "end", text="No workspace folder found")

    def _populate_tree(self, folder, parent="", prefix=""):
        try:
            entries = os.listdir(folder)
            entries.sort()
            for i, entry in enumerate(entries):
                path = os.path.join(folder, entry)
                is_last = (i == len(entries) - 1)
                ascii_prefix = prefix + ("└ " if is_last else "├ ")
                display_text = ascii_prefix + ("[" + entry + "]" if os.path.isdir(path) else entry)
                node = self.tree.insert(parent, "end", text=display_text, open=False)
                if os.path.isdir(path):
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    self._populate_tree(path, node, new_prefix)
        except Exception as e:
            self.tree.insert(parent, "end", text=f"Error: {e}")
