import os
import subprocess
import ctypes
import sys
import json

def hide_console():
    """Hides the console window (Windows only)."""
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def load_custom_game_path():
    """Loads custom game path from game_path.json if it exists."""
    try:
        with open("game_path.json", "r") as f:
            data = json.load(f)
            return data.get("game_path", "")
    except (FileNotFoundError, json.JSONDecodeError):
        return ""

def check_and_open_directory():
    """Checks if the directory exists and opens it in Explorer if found, silently."""
    # Try default path first
    user_home = os.path.expanduser("~")
    path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Content", "Paks")
    
    if not os.path.exists(path):
        # Try custom path from json
        custom_base = load_custom_game_path()
        if custom_base:
            path = os.path.join(os.path.dirname(os.path.dirname(custom_base)), "Content", "Paks")
    
    if os.path.exists(path):
        subprocess.run(["explorer", path], check=True, shell=True)

def main():
    hide_console()  # Hide console immediately
    check_and_open_directory()

if __name__ == "__main__":
    main()

