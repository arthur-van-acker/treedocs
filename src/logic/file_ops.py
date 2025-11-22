import os

class FileOps:
    @staticmethod
    def create_folder(path):
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create folder: {e}")
            return False
    # ...other file operations...
