import customtkinter as ctk

class EditorPane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=800, **kwargs)
        self.inner_frame = ctk.CTkFrame(self, fg_color="white", border_width=1, border_color="black")
        self.inner_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.label = ctk.CTkLabel(self.inner_frame, text="Editor Pane", font=("Consolas", 12))
        self.label.pack(padx=10, pady=10)
        # Add a text widget for editing
        self.text_widget = ctk.CTkTextbox(self.inner_frame, font=("Consolas", 12), width=780, height=600)
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        # Set tab size to 4 spaces
        def insert_tab(event):
            self.text_widget.insert("insert", "    ")
            return "break"
        self.text_widget.bind("<Tab>", insert_tab)

    def load_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", content)
            self.label.configure(text=f"Editor Pane - {file_path}")
        except Exception as e:
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", f"Error loading file: {e}")
            self.label.configure(text="Editor Pane")
