import customtkinter as ctk
from PIL import Image
import os

class ToolBar(ctk.CTkFrame):
    def __init__(self, master, assets_path, **kwargs):
        super().__init__(master, **kwargs)
        self.assets_path = assets_path
        self._create_widgets()

    def _create_widgets(self):
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

    def _on_save(self):
        # Placeholder for save functionality
        print("Save button clicked")
