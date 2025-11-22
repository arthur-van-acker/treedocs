
from logic.utils import resource_path
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
import sys
from ui import MenuBar, ToolBar


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