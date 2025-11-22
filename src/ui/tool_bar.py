class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 40
        y = y + self.widget.winfo_rooty() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=4)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
import customtkinter as ctk
from PIL import Image
import os
import tkinter as tk

class ToolBar(ctk.CTkFrame):
    def __init__(self, master, assets_path, **kwargs):
        super().__init__(master, **kwargs)
        self.assets_path = assets_path
        self._create_widgets()

    def _create_widgets(self):
        # Save button
        save_icon_path = os.path.join(os.path.dirname(self.assets_path), "assets", "png", "22.png")
        save_img = Image.open(save_icon_path).convert("RGBA")
        save_img = save_img.resize((24, 24), Image.LANCZOS)
        self.save_icon = ctk.CTkImage(light_image=save_img, dark_image=save_img, size=(24, 24))
        self.save_btn = ctk.CTkButton(
            self,
            image=self.save_icon,
            text="",
            width=32,
            height=32,
            command=self._on_save,
            fg_color="#e0e0e0",  # light grey
            hover_color="white"  # white
        )
        self.save_btn.pack(side="left", padx=4, pady=2)
        ToolTip(self.save_btn, "Save")

        # New File button
        new_file_icon_path = os.path.join(os.path.dirname(self.assets_path), "assets", "png", "2.png")
        new_file_img = Image.open(new_file_icon_path).convert("RGBA")
        new_file_img = new_file_img.resize((24, 24), Image.LANCZOS)
        self.new_file_icon = ctk.CTkImage(light_image=new_file_img, dark_image=new_file_img, size=(24, 24))
        self.new_file_btn = ctk.CTkButton(
            self,
            image=self.new_file_icon,
            text="",
            width=32,
            height=32,
            command=self._on_new_file,
            fg_color="#e0e0e0",
            hover_color="white"
        )
        self.new_file_btn.pack(side="left", padx=4, pady=2)
        ToolTip(self.new_file_btn, "New File")

        # Open Folder button
        open_folder_icon_path = os.path.join(os.path.dirname(self.assets_path), "assets", "png", "52.png")
        open_folder_img = Image.open(open_folder_icon_path).convert("RGBA")
        open_folder_img = open_folder_img.resize((24, 24), Image.LANCZOS)
        self.open_folder_icon = ctk.CTkImage(light_image=open_folder_img, dark_image=open_folder_img, size=(24, 24))
        self.open_folder_btn = ctk.CTkButton(
            self,
            image=self.open_folder_icon,
            text="",
            width=32,
            height=32,
            command=self._on_open_folder,
            fg_color="#e0e0e0",
            hover_color="white"
        )
        self.open_folder_btn.pack(side="left", padx=4, pady=2)
        ToolTip(self.open_folder_btn, "Open Folder")

    def _on_save(self):
        # Placeholder for save functionality
        print("Save button clicked")

    def _on_new_file(self):
        # Placeholder for new file functionality
        print("New File button clicked")

    def _on_open_folder(self):
        # Placeholder for open folder functionality
        print("Open Folder button clicked")
