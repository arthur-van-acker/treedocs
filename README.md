# TreeDocs

A minimal workspace file explorer and editor built with Python and customtkinter.

## Features
- Select a workspace folder
- View folder contents in a resizable left pane
- Right-click to create .txt or .md files
- Modular codebase with clear separation of UI and logic

## Project Structure
```
TreeDocs/
│
├── src/
│   ├── main.py                # Entry point, app initialization
│   ├── ui/
│   │   ├── app_window.py      # Main window and layout logic
│   │   ├── folder_tree.py     # Folder tree view logic
│   │   ├── menu_bar.py        # Menu bar setup
│   │   └── dialogs.py         # Dialogs (file/folder selection, etc.)
│   ├── logic/
│   │   ├── workspace.py       # Workspace config/load/save logic
│   │   ├── file_ops.py        # File/folder operations
│   │   └── icons.py           # Icon loading and management
│   └── assets/
│       └── ...                # Images, icons, etc.
│
├── tests/
│   └── ...                    # Unit tests for logic modules
│
├── README.md
├── LICENSE
└── requirements.txt           # Python dependencies
```

## Requirements
- Python 3.8+
- customtkinter

## Usage
1. Install dependencies:
   ```sh
   pip install customtkinter
   ```
2. Run the app:
   ```sh
   python src/main.py
   ```

## License
MIT
