import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import json
from ui.app_window import AppWindow

class TreeDocsApp(ctk.CTk):
	CONFIG_PATH = os.path.expanduser(r"C:\Users\Arthur\.treedocs\config.json")

	def __init__(self):
		super().__init__()
		self.title("TreeDocs")
		self.geometry("2500x1250+10+10")
		self.iconbitmap(os.path.join(os.path.dirname(__file__), "assets", "favicon.ico"))

		# PanedWindow for resizable panes
		self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=8, bg="#e0e0e0")
		self.paned_window.pack(fill="both", expand=True)

		# Left pane for folder contents (min width 500px)
		self.left_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
		self.left_frame.pack_propagate(False)
		self.left_frame.configure(width=300)
		self.paned_window.add(self.left_frame, minsize=300)
		self.folder_label_var = tk.StringVar()
		self.folder_label = tk.Label(self.left_frame, textvariable=self.folder_label_var, bg="#f5f5f5", anchor="w", font=("Segoe UI", 12, "bold"))
		self.folder_label.pack(fill="x", padx=10, pady=(10,0))
		self.button_frame = tk.Frame(self.left_frame, bg="#f5f5f5")
		self.button_frame.pack(fill="x", padx=10, pady=(2,0))
		# + and - buttons removed, but button_frame remains for layout
		from tkinter import ttk
		self.folder_tree = ttk.Treeview(self.left_frame)
		self.folder_tree.pack(fill="both", expand=True, padx=10, pady=(2,10))

	

		# Load folder icon
		try:
			from PIL import Image, ImageTk
			folder_icon_path = os.path.join(os.path.dirname(__file__), "assets", "folder.png")
			if os.path.exists(folder_icon_path):
				folder_img = Image.open(folder_icon_path).resize((16, 16))
				self.folder_icon = ImageTk.PhotoImage(folder_img)
			else:
				self.folder_icon = None
		except Exception:
			self.folder_icon = None

		# Context menu for creating files
		self.left_context_menu = tk.Menu(self.left_frame, tearoff=0)
		self.left_context_menu.add_command(label="New .txt file", command=self.create_txt_file)
		self.left_context_menu.add_command(label="New .md file", command=self.create_md_file)
		self.left_context_menu.add_command(label="New folder", command=self.create_folder)
		self.left_frame.bind("<Button-3>", self.show_left_context_menu)

		self.file_context_menu = tk.Menu(self.left_frame, tearoff=0)
		self.file_context_menu.add_command(label="Rename", command=self.rename_selected_file)
		self.file_context_menu.add_command(label="Delete", command=self.delete_selected_file)
		self.folder_tree.bind("<Button-3>", self.show_tree_context_menu)

		self.current_folder = None
		self.load_workspace_from_config()

		# Center and right panes (equal initial size, resizable)
		self.center_frame = ctk.CTkFrame(self.paned_window, fg_color="#ffffff")
		self.right_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
		self.paned_window.add(self.center_frame, minsize=100, width=1000)
		self.paned_window.add(self.right_frame, minsize=100, width=1000)

		# Menu bar (move after UI setup)
		menubar = tk.Menu(self)
		file_menu = tk.Menu(menubar, tearoff=0)
		file_menu.add_command(label="Open workspace ...", command=lambda: self.open_workspace())
		menubar.add_cascade(label="File", menu=file_menu)
		menubar.add_cascade(label="Edit")
		menubar.add_cascade(label="Settings")
		menubar.add_cascade(label="Help")
		self.config(menu=menubar)

from ui.app_window import AppWindow

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()



