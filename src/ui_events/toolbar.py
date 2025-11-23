def on_save(app_window):
    if hasattr(app_window, 'editor_pane') and hasattr(app_window.editor_pane, 'save_file'):
        app_window.editor_pane.save_file()

def on_new_file():
    print("New File button clicked")
