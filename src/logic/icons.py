import os
from PIL import Image, ImageTk

class Icons:
    @staticmethod
    def load_folder_icon():
        folder_icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "folder.png")
        if os.path.exists(folder_icon_path):
            folder_img = Image.open(folder_icon_path).resize((16, 16))
            return ImageTk.PhotoImage(folder_img)
        return None
