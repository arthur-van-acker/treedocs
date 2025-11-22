from tkinter import filedialog

class Dialogs:
    @staticmethod
    def select_folder():
        return filedialog.askdirectory(title="Select Workspace Folder")
