import os
import ctypes
import sys
import json
import subprocess

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

def find_game_executable_in_folder(folder):
    """Finds the first .exe in the folder with 'dungeons' in its name (case-insensitive)."""
    for file in os.listdir(folder):
        if file.lower().endswith(".exe") and "dungeons" in file.lower():
            return file
    return None

def find_game_install_path_and_exe():
    """Finds the install path and the dungeons exe in it."""
    # Try custom path from json first
    custom_path = load_custom_game_path()
    if custom_path and os.path.isdir(custom_path):
        exe = find_game_executable_in_folder(custom_path)
        if exe:
            return custom_path, exe

    # Try default path
    user_home = os.path.expanduser("~")
    specific_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Binaries", "Win64")
    if os.path.isdir(specific_path):
        exe = find_game_executable_in_folder(specific_path)
        if exe:
            return specific_path, exe

    return None, None

def remove_files_from_game_folder(game_folder, files):
    """Removes specified files from the game folder silently."""
    for file in files:
        file_path = os.path.join(game_folder, file)
        if os.path.exists(file_path):
            os.remove(file_path)

def start_game(game_executable, game_install_path):
    """Starts the game executable from the given path, hiding the console."""
    exe_path = os.path.join(game_install_path, game_executable)
    if os.path.isfile(exe_path):
        # Hide the console before starting the game
        hide_console()
        subprocess.Popen(exe_path, shell=True)
    else:
        print(f"Error: {game_executable} not found in {game_install_path}")

def main():
    hide_console()  # Hide console immediately

    game_install_path, game_executable = find_game_install_path_and_exe()

    if game_install_path and game_executable:
        files_to_remove = ["winmm.dll", "RUNE.ini"]
        remove_files_from_game_folder(game_install_path, files_to_remove)
        start_game(game_executable, game_install_path)
    else:
        print("Error: No dungeons executable found in default or custom path")

if __name__ == "__main__":
    main()

