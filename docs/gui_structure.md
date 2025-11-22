# TreeDocs GUI Implementation Guide

This guide explains the structure and best practices for implementing the GUI in TreeDocs. It is designed to help you understand the separation of concerns, how widgets are organized, and how to extend the interface with new elements.

## Overview

TreeDocs uses a modular approach for its GUI, with each widget or component defined in its own file. This ensures maintainability, clarity, and ease of extension. The main window (`app_window.py`) acts as the central hub, importing and assembling all UI components.

## Separation of Concerns

- **Each widget/component is in its own file**: For example, the folder tree, menu bar, dialogs, and context menus are all defined separately in the `ui/` directory.
- **Logic and UI are separated**: Business logic (file operations, workspace management, etc.) resides in the `logic/` directory, while UI code is in `ui/`.
- **Assets are stored in a dedicated folder**: Images, icons, and other static files are kept in `assets/`.

## File Structure

```
src/
  ui/
    app_window.py        # Main application window
    menu_bar.py          # Menu bar widget
    folder_tree.py       # Folder tree widget
    dialogs.py           # Dialog windows
    context_menus.py     # Context menu widgets
    ...                  # Other UI components
  logic/
    file_ops.py          # File operations logic
    workspace.py         # Workspace management
    ...                  # Other logic modules
  assets/
    ...                  # Images, icons, etc.
```

## How Widgets Are Imported

The main window (`app_window.py`) imports each widget as needed:

```python
from .menu_bar import MenuBar
from .folder_tree import FolderTree
from .dialogs import Dialogs
# ...other imports
```

Each widget is then instantiated and added to the main window layout. This keeps the main window file clean and focused on layout and orchestration.

## Adding a New UI Element

1. **Create a new file in `ui/`**: For example, `my_widget.py`.
2. **Define your widget class**: Inherit from the appropriate base class (e.g., `tk.Frame` or `customtkinter.CTkFrame`).
3. **Implement the widget's logic and UI**: Keep it self-contained.
4. **Import your widget in `app_window.py`**:
   ```python
   from .my_widget import MyWidget
   ```
5. **Instantiate and add to the layout**: Place your widget in the desired location in the main window.

### Example: Adding a Status Bar

1. Create `status_bar.py` in `ui/`:
   ```python
   import customtkinter as ctk

   class StatusBar(ctk.CTkFrame):
       def __init__(self, master, **kwargs):
           super().__init__(master, **kwargs)
           self.label = ctk.CTkLabel(self, text="Ready")
           self.label.pack()
   ```
2. Import and add to `app_window.py`:
   ```python
   from .status_bar import StatusBar
   # ...
   self.status_bar = StatusBar(self)
   self.status_bar.pack(side="bottom", fill="x")
   ```

## Tips for Extending the GUI

- **Keep widgets self-contained**: Each widget should manage its own state and events as much as possible.
- **Use clear naming conventions**: Name files and classes after their purpose (e.g., `FolderTree`, `MenuBar`).
- **Document your code**: Add docstrings and comments for clarity.
- **Reuse components**: If a widget can be reused, make it generic and configurable.
- **Test new elements independently**: Before integrating, test widgets in isolation.

## Summary

- Modular design: Each widget in its own file
- Separation of logic and UI
- Easy to add new elements
- Main window orchestrates all components

By following these practices, you can maintain a clean, scalable, and easy-to-extend GUI for TreeDocs.
