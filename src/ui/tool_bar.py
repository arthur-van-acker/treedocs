from ui import ToolTip
import customtkinter as ctk
from PIL import Image
import os
from logic import normalize_path

class ToolBar(ctk.CTkFrame):
    def __init__(self, master, assets_path, **kwargs):
        super().__init__(master, **kwargs)
        self.assets_path = assets_path
        self._app_window = master.master if hasattr(master, 'master') else master  # Get AppWindow instance
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
        # Try to get selected folder from WorkspacePane's treeview
        try:
            workspace_pane = getattr(self._app_window, 'workspace_pane', None)
            if workspace_pane is not None:
                tree = getattr(workspace_pane, 'tree', None)
                if tree is not None:
                    selected = tree.selection()
                    if selected:
                        node_id = selected[0]
                        # Get actual path from node values
                        values = tree.item(node_id, 'values')
                        if values and len(values) > 0:
                            folder_path = normalize_path(values[0])
                            if os.path.isdir(folder_path):
                                os.startfile(folder_path)
                                return
        except Exception as e:
            print(f"Failed to open selected folder: {e}")
        # Fallback: open workspace folder
        try:
            from logic.workspace import WorkspaceConfig
            folder = WorkspaceConfig.load()
            folder = normalize_path(folder) if folder else folder
            if folder and os.path.isdir(folder):
                os.startfile(folder)
            else:
                print("No valid workspace folder found.")
        except Exception as e:
            print(f"Failed to open workspace folder: {e}")
