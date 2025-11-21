import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os

class TreeDocsApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("TreeDocs")
		self.geometry("2500x1250+10+10")
		self.iconbitmap(os.path.join(os.path.dirname(__file__), "assets", "favicon.ico"))

		# Menu bar
		menubar = tk.Menu(self)
		file_menu = tk.Menu(menubar, tearoff=0)
		file_menu.add_command(label="Open workspace ...", command=self.open_workspace)
		menubar.add_cascade(label="File", menu=file_menu)
		menubar.add_cascade(label="Edit")
		menubar.add_cascade(label="Settings")
		menubar.add_cascade(label="Help")
		self.config(menu=menubar)

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
		self.left_frame.bind("<Button-3>", self.show_left_context_menu)
		self.folder_listbox.bind("<Button-3>", self.show_left_context_menu)

		self.current_folder = None

		# Center and right panes
		self.center_frame = ctk.CTkFrame(self.paned_window, fg_color="#ffffff")
		self.paned_window.add(self.center_frame)
		self.right_frame = ctk.CTkFrame(self.paned_window, fg_color="#f5f5f5")
		self.paned_window.add(self.right_frame)

	def open_workspace(self):
		folder_selected = filedialog.askdirectory(title="Select Workspace Folder")
		if folder_selected:
			self.show_folder_contents(folder_selected)

	def show_folder_contents(self, folder):
		self.current_folder = folder
		self.folder_label_var.set(f"Workspace: {os.path.basename(folder)}")
		self.folder_listbox.delete(0, tk.END)
		for item in os.listdir(folder):
			self.folder_listbox.insert(tk.END, item)

	def show_left_context_menu(self, event):
		if self.current_folder:
			self.left_context_menu.tk_popup(event.x_root, event.y_root)

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
