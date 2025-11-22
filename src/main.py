import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import json

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
	def open_workspace(self):
		folder_selected = filedialog.askdirectory(title="Select Workspace Folder")
		if folder_selected:
			self.save_workspace_to_config(folder_selected)
			self.show_folder_contents(folder_selected)

		# PanedWindow for resizable panes
		self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=8, bg="#e0e0e0")
		self.paned_window.pack(fill="both", expand=True)

		# Left pane for folder contents (min width 500px)
		self.left_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
		self.left_frame.pack_propagate(False)
		self.left_frame.configure(width=500)
		self.paned_window.add(self.left_frame, minsize=500)
		self.folder_label_var = tk.StringVar()
		self.folder_label = tk.Label(self.left_frame, textvariable=self.folder_label_var, bg="#f5f5f5", anchor="w", font=("Segoe UI", 12, "bold"))
		self.folder_label.pack(fill="x", padx=10, pady=(10,0))
		self.folder_listbox = tk.Listbox(self.left_frame, bg="#f5f5f5", border=0)
		self.folder_listbox.pack(fill="both", expand=True, padx=10, pady=(2,10))

		# Context menu for creating files
		self.left_context_menu = tk.Menu(self.left_frame, tearoff=0)
		self.left_context_menu.add_command(label="New .txt file", command=self.create_txt_file)
		self.left_context_menu.add_command(label="New .md file", command=self.create_md_file)
		self.left_context_menu.add_command(label="New folder", command=self.create_folder)
		self.left_frame.bind("<Button-3>", self.show_left_context_menu)
		self.folder_listbox.bind("<Button-3>", self.show_left_context_menu)

		self.current_folder = None
		self.load_workspace_from_config()

		# Center and right panes
		self.center_frame = ctk.CTkFrame(self.paned_window, fg_color="#ffffff")
		self.paned_window.add(self.center_frame)
		self.right_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
		self.paned_window.add(self.right_frame)

	def load_workspace_from_config(self):
		try:
			if os.path.exists(self.CONFIG_PATH):
				with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
					config = json.load(f)
				folder = config.get("workspace_folder")
				if folder and os.path.isdir(folder):
					self.show_folder_contents(folder)
		except Exception as e:
			print(f"Failed to load workspace config: {e}")

	def create_folder(self):
		if self.current_folder:
			folder_name = filedialog.asksaveasfilename(initialdir=self.current_folder, title="Create Folder", defaultextension="", filetypes=[("All Files", "*")])
			if folder_name:
				# Remove file extension if any, and create folder
				folder_name = os.path.splitext(folder_name)[0]
				try:
					os.makedirs(folder_name, exist_ok=True)
					self.show_folder_contents(self.current_folder)
				except Exception as e:
					print(f"Failed to create folder: {e}")

	def save_workspace_to_config(self, folder):
		try:
			os.makedirs(os.path.dirname(self.CONFIG_PATH), exist_ok=True)
			with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
				json.dump({"workspace_folder": folder}, f)
		except Exception as e:
			print(f"Failed to save workspace config: {e}")

	def show_folder_contents(self, folder):
		self.current_folder = folder
		self.folder_label_var.set(f"Workspace: {os.path.basename(folder)}")
		self.folder_tree.delete(*self.folder_tree.get_children())
		self._insert_tree_items(folder, "")

	def _insert_tree_items(self, path, parent, prefix=""):
		try:
			items = sorted(os.listdir(path))
			dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
			files = [item for item in items if not os.path.isdir(os.path.join(path, item))]
			# Always show directories, even if empty
			for idx, d in enumerate(dirs):
				abs_path = os.path.join(path, d)
				# ASCII tree connection
				connector = "├── " if idx < len(dirs) - 1 or files else "└── "
				display_text = f"{prefix}{connector}{d}"
				node_id = self.folder_tree.insert(parent, "end", text=display_text, image=self.folder_icon if self.folder_icon else "", open=False)
				# For children, add vertical bar if not last
				child_prefix = prefix + ("│   " if idx < len(dirs) - 1 or files else "    ")
				self._insert_tree_items(abs_path, node_id, child_prefix)
			for f_idx, f in enumerate(files):
				connector = "└── " if f_idx == len(files) - 1 else "├── "
				display_text = f"{prefix}{connector}{f}"
				self.folder_tree.insert(parent, "end", text=display_text, open=False)
		except Exception as e:
			print(f"Failed to list folder tree: {e}")

	def show_left_context_menu(self, event):
		if self.current_folder:
			self.left_context_menu.tk_popup(event.x_root, event.y_root)

	def show_tree_context_menu(self, event):
		item_id = self.folder_tree.identify_row(event.y)
		if item_id:
			self.folder_tree.selection_set(item_id)
			self.file_context_menu.tk_popup(event.x_root, event.y_root)
		else:
			self.left_context_menu.tk_popup(event.x_root, event.y_root)
	def get_selected_file_path(self):
		item_id = self.folder_tree.selection()[0]
		parts = []
		while item_id:
			parts.insert(0, self.folder_tree.item(item_id, "text"))
			item_id = self.folder_tree.parent(item_id)
		return os.path.join(self.current_folder, *parts) if parts else None

	def rename_selected_file(self):
		old_path = self.get_selected_file_path()
		if old_path and os.path.exists(old_path):
			import tkinter.simpledialog
			# Create a custom Toplevel for the dialog to set icon
			dialog = tk.Toplevel(self)
			dialog.withdraw()
			icon_path = os.path.join(os.path.dirname(__file__), "assets", "favicon.ico")
			try:
				dialog.iconbitmap(icon_path)
			except Exception:
				pass
			new_name = tkinter.simpledialog.askstring("Rename", f"Rename '{os.path.basename(old_path)}' to:", initialvalue=os.path.basename(old_path), parent=dialog)
			dialog.destroy()
			if new_name:
				new_path = os.path.join(os.path.dirname(old_path), new_name)
				try:
					os.rename(old_path, new_path)
					self.show_folder_contents(self.current_folder)
				except Exception as e:
					print(f"Failed to rename: {e}")

	def delete_selected_file(self):
		path = self.get_selected_file_path()
		if path and os.path.exists(path):
			import shutil
			try:
				if os.path.isdir(path):
					shutil.rmtree(path)
				else:
					os.remove(path)
				self.show_folder_contents(self.current_folder)
			except Exception as e:
				print(f"Failed to delete: {e}")

	def create_txt_file(self):
		if self.current_folder:
			filename = filedialog.asksaveasfilename(initialdir=self.current_folder, title="Create .txt file", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
			if filename:
				with open(filename, "w", encoding="utf-8") as f:
					f.write("")
				self.show_folder_contents(self.current_folder)

	def create_md_file(self):
		if self.current_folder:
			filename = filedialog.asksaveasfilename(initialdir=self.current_folder, title="Create .md file", defaultextension=".md", filetypes=[("Markdown files", "*.md")])
			if filename:
				with open(filename, "w", encoding="utf-8") as f:
					f.write("")
				self.show_folder_contents(self.current_folder)

if __name__ == "__main__":
	app = TreeDocsApp()
	app.mainloop()
