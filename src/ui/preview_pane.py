import customtkinter as ctk

class PreviewPane(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=800, **kwargs)
        # Add a white background frame with padding
        self.inner_frame = ctk.CTkFrame(self, fg_color='white', border_width=1, border_color='black')
        self.inner_frame.pack(fill='both', expand=True, padx=5, pady=5)
        # Add preview-specific widgets to inner_frame
        self.label = ctk.CTkLabel(self.inner_frame, text='Preview', font=('Consolas', 12))
        self.label.pack(padx=10, pady=10)

    def load_file_content(self, file_path: str) -> None:
        '''
        Load and display the content of a file in the preview pane.

        Args:
            file_path (str): Path to the file to preview.
        '''
        # Placeholder: Implementation for .txt/.md/other types will be added in next steps
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.label.configure(text=f'Preview - {file_path}')
            # For now, just display the raw content in the label (will be replaced)
            self.inner_frame.configure(fg_color='white')
            if hasattr(self, 'preview_widget'):
                self.preview_widget.destroy()
            import customtkinter as ctk
            self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=600)
            self.preview_widget.insert('1.0', content)
            self.preview_widget.configure(state='disabled')
            self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
        except Exception as e:
            self.label.configure(text='Preview Pane')
            if hasattr(self, 'preview_widget'):
                self.preview_widget.destroy()
            import customtkinter as ctk
            self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=600)
            self.preview_widget.insert('1.0', f'Error loading file: {e}')
            self.preview_widget.configure(state='disabled')
            self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
