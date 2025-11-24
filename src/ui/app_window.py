
from logic import resource_path
import customtkinter as ctk
import os
import tkinter as tk
from ui import MenuBar, ToolBar, WorkspacePane, EditorPane, PreviewPane
from ui_events import on_save


class AppWindow(ctk.CTk):
    def save_file_in_editor(self):
        on_save(self)

    def open_file_in_editor(self, file_path):
        if hasattr(self.editor_pane, 'load_file'):
            self.editor_pane.load_file(file_path)

    # ...existing code...
    def __init__(self):
        super().__init__()
        self.title("TreeDocs")
        self.geometry("1900x1250")
        self.resizable(False, False)
        # Variables to track pane visibility
        self.editor_pane_var = tk.BooleanVar(value=True)
        self.preview_pane_var = tk.BooleanVar(value=True)
        # Font size state for panes
        self.pane_font_size = 12
        # Set favicon (window icon)
        icon_path = resource_path("assets/favicon.ico")
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

        # Add tool bar below menu bar
        assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
        self.tool_bar = ToolBar(self, assets_path)
        self.tool_bar.pack(side="top", fill="x")

        # Main content area with three panes
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="top", fill="both", expand=True)

        # Workspace pane (left)
        self.workspace_pane = WorkspacePane(self.main_content)
        self.workspace_pane.pack(side="left", fill="y")
        self.workspace_pane.configure(width=300)
        self.workspace_pane.pack_propagate(False)

        # Editor pane (middle)
        self.editor_pane = EditorPane(self.main_content)
        self.editor_pane.pack(side="left", fill="y")
        self.editor_pane.configure(width=800)
        self.editor_pane.pack_propagate(False)

        # Preview pane (right)
        self.preview_pane = PreviewPane(self.main_content)
        self.preview_pane.pack(side="left", fill="y")
        self.preview_pane.configure(width=800)
        self.preview_pane.pack_propagate(False)

        # Live preview: bind text change event
        # Debounced live preview update for CEF browser
        self._preview_update_after_id = None
        def debounced_preview_update(event=None):
            if self._preview_update_after_id:
                self.editor_pane.text_widget.after_cancel(self._preview_update_after_id)
            def update():
                label_text = self.editor_pane.label.cget("text")
                if label_text.endswith('.md'):
                    content = self.editor_pane.text_widget.get("1.0", "end-1c")
                    self.preview_pane.load_markdown_content(content)
                self.editor_pane.text_widget.edit_modified(False)
            self._preview_update_after_id = self.editor_pane.text_widget.after(500, update)
        self.editor_pane.text_widget.bind("<<Modified>>", debounced_preview_update)

        # Add menu bar (after panes are created)
        self.menu_bar = MenuBar(self)
        # Connect zoom actions
        self.menu_bar.set_zoom_handlers(self.zoom_in, self.zoom_out)
    def set_pane_font_size(self, size):
        size = max(8, min(24, size))
        self.pane_font_size = size
        # Update EditorPane font
        if hasattr(self.editor_pane, 'label'):
            self.editor_pane.label.configure(font=("Consolas", size))
        if hasattr(self.editor_pane, 'text_widget'):
            self.editor_pane.text_widget.configure(font=("Consolas", size))
        # Update PreviewPane font
        if hasattr(self.preview_pane, 'label'):
            self.preview_pane.label.configure(font=("Consolas", size))
    def zoom_in(self):
        self.set_pane_font_size(self.pane_font_size + 2)

    def zoom_out(self):
        self.set_pane_font_size(self.pane_font_size - 2)

    def toggle_editor_pane(self):
        if self.editor_pane_var.get():
            self.editor_pane.pack(side="left", fill="y")
        else:
            self.editor_pane.pack_forget()
        self.update_mainwindow_width()

    def toggle_preview_pane(self):
        if self.preview_pane_var.get():
            self.preview_pane.pack(side="left", fill="y")
        else:
            self.preview_pane.pack_forget()
        self.update_mainwindow_width()

    def update_mainwindow_width(self):
        width = 300 # workspace pane always visible
        if self.editor_pane_var.get():
            width += 800
        if self.preview_pane_var.get():
            width += 800
        self.geometry(f"{width}x1250")