import tkinter as tk

class MenuBar:
    def __init__(self, parent):
        menubar = tk.Menu(parent)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open...")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        workspaces_menu = tk.Menu(menubar, tearoff=0)
        workspaces_menu.add_command(label="Open Workspace...")
        workspaces_menu.add_command(label="Close Workspace")
        menubar.add_cascade(label="Workspaces", menu=workspaces_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Zoom In")
        view_menu.add_command(label="Zoom Out")
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help Topics")
        help_menu.add_command(label="About TreeDocs")
        menubar.add_cascade(label="Help", menu=help_menu)

        parent.config(menu=menubar)
