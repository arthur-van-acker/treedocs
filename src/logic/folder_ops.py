from logic.workspace import get_last_selected_folder, WorkspaceConfig
from logic import normalize_path

def open_relevant_folder():
    folder_path = get_last_selected_folder()
    print(f"Last selected folder: {folder_path}")
    if not folder_path or not os.path.isdir(folder_path):
        folder_path = get_last_selected_folder()
        if not folder_path or not os.path.isdir(folder_path):
            folder = WorkspaceConfig.load()
            folder_path = normalize_path(folder) if folder else None
    if folder_path and os.path.isdir(folder_path):
        open_folder(folder_path)
    else:
        print("No valid folder found to open.")
import os

def open_folder(path):
    try:
        os.startfile(path)
    except Exception as e:
        print(f"Failed to open folder: {e}")
