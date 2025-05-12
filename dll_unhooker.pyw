import os
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

def find_game_install_path(game_executable):
    """Finds the installation path of the game based on the given executable."""
    # Try default path first
    user_home = os.path.expanduser("~")
    specific_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Binaries", "Win64")
    game_executable_path = os.path.join(specific_path, game_executable)

    if os.path.exists(game_executable_path):
        return specific_path

    # If default path fails, try custom path from json
    custom_path = load_custom_game_path()
    if custom_path and os.path.exists(os.path.join(custom_path, game_executable)):
        return custom_path

    return None

def remove_files_from_game_folder(game_folder, files):
    """Removes specified files from the game folder silently."""
    for file in files:
        file_path = os.path.join(game_folder, file)
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    hide_console()  # Hide console immediately

    game_executable = "Dungeons-Win64-Shipping.exe"
    game_install_path = find_game_install_path(game_executable)

    if game_install_path:
        files_to_remove = ["winmm.dll", "RUNE.ini"]
        remove_files_from_game_folder(game_install_path, files_to_remove)

if __name__ == "__main__":
    main()

