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
            self.tree.tag_configure('workspace_bold', font=("Consolas", 10, 'bold'))
            self.tree.item(root_node, tags=('workspace_bold',))
            populate_tree(self.tree, folder, root_node)
        else:
            self.tree.insert("", "end", text="No workspace folder found")

        # Bind selection event to open file in editor if file is selected
        def on_select(_event):
            selected = self.tree.selection()
            if selected:
                node_id = selected[0]
                values = self.tree.item(node_id, 'values')
                if values and len(values) > 0:
                    path = values[0]
                    import os
                    if os.path.isfile(path):
                        # Find the AppWindow instance and call open_file_in_editor
                        app = self.winfo_toplevel()
                        if hasattr(app, 'open_file_in_editor'):
                            app.open_file_in_editor(path)
        self.tree.bind('<<TreeviewSelect>>', on_select)