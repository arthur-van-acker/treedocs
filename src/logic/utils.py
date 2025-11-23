import os
import sys

def normalize_path(path):
    """Normalize a filesystem path for the current OS."""
    return os.path.normpath(path)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', relative_path)
