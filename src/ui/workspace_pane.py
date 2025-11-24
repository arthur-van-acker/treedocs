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
            print('[WorkspacePane] on_select called')
            try:
                selected = self.tree.selection()
                print(f'[WorkspacePane] selected: {selected}')
                if selected:
                    node_id = selected[0]
                    values = self.tree.item(node_id, 'values')
                    print(f'[WorkspacePane] node_id: {node_id}, values: {values}')
                    if values and len(values) > 0:
                        path = values[0]
                        import os
                        app = self.winfo_toplevel()
                        print(f'[WorkspacePane] path: {path}')
                        if os.path.isfile(path):
                            print(f'[WorkspacePane] path is file')
                            # Call editor pane for editing
                            if hasattr(app, 'open_file_in_editor'):
                                print(f'[WorkspacePane] calling open_file_in_editor')
                                app.open_file_in_editor(path)
                            # Call preview pane for supported files (.txt, .md)
                            ext = os.path.splitext(path)[1].lower()
                            print(f'[WorkspacePane] file extension: {ext}')
                            if ext in ['.txt', '.md'] and hasattr(app, 'preview_pane'):
                                preview_pane = getattr(app, 'preview_pane', None)
                                if hasattr(preview_pane, 'load_file_content'):
                                    print(f'[WorkspacePane] calling preview_pane.load_file_content')
                                    preview_pane.load_file_content(path)
                print('[WorkspacePane] on_select completed')
            except Exception as e:
                print(f'[WorkspacePane] Error in file selection: {e}')
                app = self.winfo_toplevel()
                if hasattr(app, 'preview_pane') and hasattr(app.preview_pane, 'load_file_content'):
                    # Show error in preview pane
                    app.preview_pane.label.configure(text='Preview Pane')
                    if hasattr(app.preview_pane, 'preview_widget'):
                        app.preview_pane.preview_widget.destroy()
                    import customtkinter as ctk
                    error_msg = (
                        'Unable to load file preview.\n\n'
                        f'Error: {e}\n\n'
                        'Please check the file path, permissions, or file format.'
                    )
                    app.preview_pane.preview_widget = ctk.CTkTextbox(
                        app.preview_pane.inner_frame,
                        font=('Consolas', 12, 'italic'),
                        width=780,
                        height=120,
                        fg_color='#fff0f0',
                        text_color='#b91c1c',
                        border_color='#d0d7de',
                        border_width=1
                    )
                    app.preview_pane.preview_widget.insert('1.0', error_msg)
                    app.preview_pane.preview_widget.configure(state='disabled')
                    app.preview_pane.preview_widget.bind('<Key>', lambda e: 'break')
                    app.preview_pane.preview_widget.pack(fill='x', padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', on_select)