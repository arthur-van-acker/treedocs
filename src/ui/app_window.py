
from logic import resource_path
import customtkinter as ctk
import os
import tkinter as tk
from ui import MenuBar, ToolBar, WorkspacePane, EditorPane, PreviewPane


class AppWindow(ctk.CTk):
    # ...existing code...
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("1900x1250")
        self.resizable(False, False)
        # Variables to track pane visibility
        self.editor_pane_var = tk.BooleanVar(value=True)
        self.preview_pane_var = tk.BooleanVar(value=True)
        # Set favicon (window icon)
        icon_path = resource_path("assets/favicon.ico")
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

        # Add tool bar below menu bar
        assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
        self.tool_bar = ToolBar(self, assets_path)
        self.tool_bar.pack(side="top", fill="x")

        # Main content area with three panes
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="top", fill="both", expand=True)

        # Workspace pane (left)
        self.workspace_pane = WorkspacePane(self.main_content)
        self.workspace_pane.pack(side="left", fill="y")
        self.workspace_pane.configure(width=300)
        self.workspace_pane.pack_propagate(False)

        # Editor pane (middle)
        self.editor_pane = EditorPane(self.main_content)
        self.editor_pane.pack(side="left", fill="y")
        self.editor_pane.configure(width=800)
        self.editor_pane.pack_propagate(False)

        # Preview pane (right)
        self.preview_pane = PreviewPane(self.main_content)
        self.preview_pane.pack(side="left", fill="y")
        self.preview_pane.configure(width=800)
        self.preview_pane.pack_propagate(False)

        # Add menu bar (after panes are created)
        self.menu_bar = MenuBar(self)

    def toggle_editor_pane(self):
        if self.editor_pane_var.get():
            self.editor_pane.pack(side="left", fill="y")
        else:
            self.editor_pane.pack_forget()
        self.update_mainwindow_width()

    def toggle_preview_pane(self):
        if self.preview_pane_var.get():
            self.preview_pane.pack(side="left", fill="y")
        else:
            self.preview_pane.pack_forget()
        self.update_mainwindow_width()

    def update_mainwindow_width(self):
        width = 300 # workspace pane always visible
        if self.editor_pane_var.get():
            width += 800
        if self.preview_pane_var.get():
            width += 800
        self.geometry(f"{width}x1250")