import customtkinter as ctk
import tkinter as tk

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("2500x1250+10+10")
        # ...additional window setup...
