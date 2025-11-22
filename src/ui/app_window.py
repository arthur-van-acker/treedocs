from logic.utils import resource_path
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
import sys


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