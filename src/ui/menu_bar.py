import tkinter as tk

class MenuBar:
    def __init__(self, parent, open_workspace_callback):
        menubar = tk.Menu(parent)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open workspace ...", command=open_workspace_callback)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit")
        menubar.add_cascade(label="Settings")
        menubar.add_cascade(label="Help")
        parent.config(menu=menubar)
