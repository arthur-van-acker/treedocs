def open_workspace(app_window):
    from tkinter import filedialog
    folder = filedialog.askdirectory(title="Select Workspace Folder")
    if folder:
        from logic.workspace import WorkspaceConfig
        WorkspaceConfig.save(folder)
        # Rebuild workspace pane
        app_window.workspace_pane.destroy()
        from ui import WorkspacePane
        app_window.workspace_pane = WorkspacePane(app_window.main_content)
        app_window.workspace_pane.pack(side="left", fill="y")
        app_window.workspace_pane.configure(width=300)
        app_window.workspace_pane.pack_propagate(False)
        # Re-pack editor and preview panes to ensure order
        if hasattr(app_window, 'editor_pane'):
            app_window.editor_pane.pack_forget()
            app_window.editor_pane.pack(side="left", fill="y")
        if hasattr(app_window, 'preview_pane'):
            app_window.preview_pane.pack_forget()
            app_window.preview_pane.pack(side="left", fill="y")
