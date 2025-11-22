import customtkinter as ctk

class WorkspacePane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=300, **kwargs)
        # Add workspace-specific widgets here
        self.label = ctk.CTkLabel(self, text="Workspace Pane")
        self.label.pack(padx=10, pady=10)
