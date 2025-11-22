import os
from dotenv import load_dotenv

load_dotenv()
class FileOps:
    @staticmethod
    def create_folder(path):
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create folder: {e}")
            return False
    @staticmethod
    def rename_file(old_path, new_path):
        try:
            os.rename(old_path, new_path)
            return True
        except Exception as e:
            print(f"Failed to rename file: {e}")
            return False

    @staticmethod
    def delete_file_or_folder(path):
        import shutil
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return True
        except Exception as e:
            print(f"Failed to delete: {e}")
            return False
    # ...other file operations...
