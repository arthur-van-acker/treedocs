
from logic import resource_path
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
import sys
from ui import MenuBar, ToolBar, WorkspacePane, EditorPane, PreviewPane


class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("2500x1250+10+10")
        # Set favicon (window icon)
        icon_path = resource_path("assets/favicon.ico")
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

        # Add menu bar
        self.menu_bar = MenuBar(self)
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
        self.editor_pane.pack(side="left", fill="both", expand=True)

        # Preview pane (right)
        self.preview_pane = PreviewPane(self.main_content)
        self.preview_pane.pack(side="left", fill="y")