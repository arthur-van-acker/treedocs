import customtkinter as ctk

class PreviewPane(ctk.CTkFrame):
    def load_markdown_content(self, content: str) -> None:
        import os
        import markdown2
        from cefpython3 import cefpython as cef
        html = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables', 'strike', 'task_list', 'cuddled-lists', 'metadata', 'code-friendly', 'footnotes', 'header-ids', 'toc', 'github-markdown-css'])
        css_path = os.path.join(os.path.dirname(__file__), '../assets/markdown_preview.css')
        try:
            with open(css_path, 'r', encoding='utf-8') as css_file:
                css = css_file.read()
            style_tag = f'<style>{css}</style>'
            html = style_tag + html
        except Exception:
            pass
        # Only update if content changed
        if not hasattr(self, '_last_html') or self._last_html != html:
            self._last_html = html
            # Create or update CEF browser widget
            if not hasattr(self, 'cef_browser'):
                # Destroy previous widget if exists
                if hasattr(self, 'preview_widget'):
                    self.preview_widget.destroy()
                self.inner_frame.pack_forget()
                self.native_frame.pack_forget()
                # Initialize CEF if not already done
                if not cef.GetApp():
                    cef.Initialize()
                # Create a Tkinter frame for CEF browser
                import tkinter as tk
                self.cef_frame = tk.Frame(self)
                self.cef_frame.pack(fill='both', expand=True, padx=5, pady=5)
                window_info = cef.WindowInfo()
                window_info.SetAsChild(self.cef_frame.winfo_id(), [0, 0, 780, 600])
                self.cef_browser = cef.CreateBrowserSync(window_info, url='data:text/html,' + html)
            else:
                self.cef_browser.LoadUrl('data:text/html,' + html)
    def __init__(self, master, **kwargs):
        super().__init__(master, width=800, **kwargs)
        # Add a white background frame with padding
        import tkinter as tk
        self.native_frame = tk.Frame(self)
        self.inner_frame = ctk.CTkFrame(self, fg_color='#f6f8fa', border_width=1, border_color='#d0d7de')
        self.inner_frame.pack(fill='both', expand=True, padx=5, pady=5)
        # Add preview-specific widgets to inner_frame
        self.label = ctk.CTkLabel(
            self.inner_frame,
            text='Preview',
            font=('Consolas', 13, 'bold'),
            text_color='#24292f',
            fg_color='#f6f8fa',
            anchor='w'
        )
        self.label.pack(fill='x', padx=10, pady=(10, 0))

    def load_file_content(self, file_path: str) -> None:
        print(f'[PreviewPane] load_file_content called for: {file_path}')
        import os
        try:
            ext = os.path.splitext(file_path)[1].lower()
            print(f'[PreviewPane] file extension: {ext}')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f'[PreviewPane] file read successfully')
            self.label.configure(text=f'Preview - {file_path}')
            self.inner_frame.configure(fg_color='white')
            if hasattr(self, 'preview_widget'):
                self.preview_widget.destroy()
            # Hide native_frame by default
            self.native_frame.pack_forget()
            self.inner_frame.pack(fill='both', expand=True, padx=5, pady=5)
            import customtkinter as ctk
            if ext == '.txt':
                print(f'[PreviewPane] displaying as plain text')
                self.preview_widget = ctk.CTkTextbox(
                    self.inner_frame,
                    font=('Consolas', 12),
                    width=780,
                    height=600,
                    fg_color='#f6f8fa',
                    text_color='#24292f',
                    border_color='#d0d7de',
                    border_width=1
                )
                self.preview_widget.insert('1.0', content)
                self.preview_widget.configure(state='disabled')
                self.preview_widget.bind('<Key>', lambda e: 'break')
                self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
            elif ext == '.md':
                print(f'[PreviewPane] displaying as markdown')
                try:
                    import markdown2
                    html = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables', 'strike', 'task_list', 'cuddled-lists', 'metadata', 'code-friendly', 'footnotes', 'header-ids', 'toc', 'github-markdown-css'])
                    print(f'[PreviewPane] markdown2 conversion successful')
                    # Inject custom CSS
                    css_path = os.path.join(os.path.dirname(__file__), '../assets/markdown_preview.css')
                    try:
                        with open(css_path, 'r', encoding='utf-8') as css_file:
                            css = css_file.read()
                        style_tag = f'<style>{css}</style>'
                        html = style_tag + html
                        print(f'[PreviewPane] Custom CSS injected')
                    except Exception as css_error:
                        print(f'[PreviewPane] Could not load custom CSS: {css_error}')
                except ImportError:
                    html = '<b>Error:</b> markdown2 is not installed.'
                    print(f'[PreviewPane] markdown2 not installed')
                # Try to render HTML using tkinterweb
                try:
                    from tkinterweb import HtmlFrame
                    if hasattr(self, 'preview_widget'):
                        self.preview_widget.destroy()
                    print(f'[PreviewPane] creating HtmlFrame (tkinterweb)')
                    # Hide customtkinter preview pane and show native_frame
                    self.inner_frame.pack_forget()
                    self.native_frame.pack(fill='both', expand=True, padx=5, pady=5)
                    self.preview_widget = HtmlFrame(self.native_frame)
                    self.preview_widget.load_html(html)
                    self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
                    print(f'[PreviewPane] HtmlFrame (tkinterweb) displayed')
                except Exception as web_error:
                    print(f'[PreviewPane] HtmlFrame (tkinterweb) error: {web_error}\nFalling back to textbox preview.')
                    self.native_frame.pack_forget()
                    self.inner_frame.pack(fill='both', expand=True, padx=5, pady=5)
                    self.preview_widget = ctk.CTkTextbox(
                        self.inner_frame,
                        font=('Consolas', 12),
                        width=780,
                        height=600,
                        fg_color='#f6f8fa',
                        text_color='#24292f',
                        border_color='#d0d7de',
                        border_width=1
                    )
                    self.preview_widget.insert('1.0', html)
                    self.preview_widget.configure(state='disabled')
                    self.preview_widget.bind('<Key>', lambda e: 'break')
                    self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
            else:
                print(f'[PreviewPane] displaying unsupported file type')
                msg = f'Preview not available for this file type: {ext}'
                self.preview_widget = ctk.CTkTextbox(
                    self.inner_frame,
                    font=('Consolas', 12, 'italic'),
                    width=780,
                    height=100,
                    fg_color='#f6f8fa',
                    text_color='#6e7781',
                    border_color='#d0d7de',
                    border_width=1
                )
                self.preview_widget.insert('1.0', msg)
                self.preview_widget.configure(state='disabled')
                self.preview_widget.bind('<Key>', lambda e: 'break')
                self.preview_widget.pack(fill='x', padx=10, pady=10)
            print(f'[PreviewPane] load_file_content completed')
        except Exception as e:
            print(f'[PreviewPane] Error loading file: {e}')
            self.label.configure(text='Preview Pane')
            if hasattr(self, 'preview_widget'):
                self.preview_widget.destroy()
            import customtkinter as ctk
            self.preview_widget = ctk.CTkTextbox(self.inner_frame, font=('Consolas', 12), width=780, height=600)
            self.preview_widget.insert('1.0', f'Error loading file: {e}')
            self.preview_widget.configure(state='disabled')
            self.preview_widget.pack(fill='both', expand=True, padx=10, pady=10)
            print(f'[PreviewPane] load_file_content error handled')
