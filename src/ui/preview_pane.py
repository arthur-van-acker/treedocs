import customtkinter as ctk

class PreviewPane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=800, **kwargs)
        # Add a white background frame with padding
        self.inner_frame = ctk.CTkFrame(self, fg_color="white", border_width=1, border_color="black")
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)
        # Add preview-specific widgets to inner_frame
        self.label = ctk.CTkLabel(self.inner_frame, text="Preview Pane")
        self.label.pack(padx=10, pady=10)
