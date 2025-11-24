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
        import os
        try:
            ext = os.path.splitext(file_path)[1].lower()
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.label.configure(text=f'Preview - {file_path}')
            self.inner_frame.configure(fg_color='white')
            if hasattr(self, 'preview_widget'):
                self.preview_widget.destroy()
            import customtkinter as ctk
            if ext == '.txt':
                # Display plain text in a read-only textbox
                self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=600)
                self.preview_widget.insert('1.0', content)
                self.preview_widget.configure(state='disabled')
                self.preview_widget.bind('<Key>', lambda e: 'break')
                self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
            elif ext == '.md':
                # Convert markdown to HTML using markdown2 (GitHub-flavored)
                try:
                    import markdown2
                    html = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables', 'strike', 'task_list', 'cuddled-lists', 'metadata', 'code-friendly', 'footnotes', 'header-ids', 'toc', 'github-markdown-css'])
                except ImportError:
                    html = '<b>Error:</b> markdown2 is not installed.'
                # Render HTML in the preview pane using tkinterhtml
                try:
                    from tkinterhtml import HtmlFrame
                    if hasattr(self, 'preview_widget'):
                        self.preview_widget.destroy()
                    # Create HtmlFrame for HTML rendering
                    self.preview_widget = HtmlFrame(self.inner_frame, horizontal_scrollbar='auto')
                    self.preview_widget.set_content(html)
                    self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
                    # Make HtmlFrame strictly read-only (disable selection and editing)
                    self.preview_widget.bind('<Key>', lambda e: 'break')
                    self.preview_widget.bind('<Button-3>', lambda e: 'break')
                except ImportError:
                    # Fallback: show HTML as text if tkinterhtml is not installed
                    self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=600)
                    self.preview_widget.insert('1.0', html)
                    self.preview_widget.configure(state='disabled')
                    self.preview_widget.bind('<Key>', lambda e: 'break')
                    self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
            else:
                # Display a message for unsupported file types
                msg = f'Preview not available for this file type: {ext}'
                self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=100)
                self.preview_widget.insert('1.0', msg)
                self.preview_widget.configure(state='disabled')
                self.preview_widget.bind('<Key>', lambda e: 'break')
                self.preview_widget.pack(fill='x', padx=10, pady=10)
        except Exception as e:
            self.label.configure(text='Preview Pane')
            if hasattr(self, 'preview_widget'):
                self.preview_widget.destroy()
            import customtkinter as ctk
            self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=600)
            self.preview_widget.insert('1.0', f'Error loading file: {e}')
            self.preview_widget.configure(state='disabled')
            self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
