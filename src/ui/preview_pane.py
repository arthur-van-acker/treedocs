import customtkinter as ctk

class PreviewPane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=400, **kwargs)
        # Add preview-specific widgets here
        self.label = ctk.CTkLabel(self, text="Preview Pane")
        self.label.pack(padx=10, pady=10)
