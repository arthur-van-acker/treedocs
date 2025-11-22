import os
import json

class WorkspaceConfig:
    CONFIG_PATH = os.path.expanduser(r"C:\Users\Arthur\.treedocs\config.json")

    @staticmethod
    def load():
        try:
            if os.path.exists(WorkspaceConfig.CONFIG_PATH):
                with open(WorkspaceConfig.CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                folder = config.get("workspace_folder")
                if folder and os.path.isdir(folder):
                    return folder
        except Exception as e:
            print(f"Failed to load workspace config: {e}")
        return None

    @staticmethod
    def save(folder):
        try:
            config = {"workspace_folder": folder}
            os.makedirs(os.path.dirname(WorkspaceConfig.CONFIG_PATH), exist_ok=True)
            with open(WorkspaceConfig.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Failed to save workspace config: {e}")
