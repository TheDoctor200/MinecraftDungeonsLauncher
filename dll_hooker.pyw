import os
import shutil
import ctypes
import sys
import json
import subprocess

CANDIDATE_EXE_NAMES = ("Dungeons-Win64-Shipping.exe", "MinecraftDungeons.exe")

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

def first_matching_exe(folder: str):
    try:
        for name in os.listdir(folder):
            if name.lower().endswith(".exe") and ("dungeons" in name.lower() or name in CANDIDATE_EXE_NAMES):
                return name
    except Exception:
        pass
    return None

def resolve_from_custom(custom_path: str):
    if not custom_path:
        return None, None
    p = os.path.expandvars(os.path.expanduser(custom_path))
    if os.path.isfile(p) and p.lower().endswith(".exe"):
        return os.path.dirname(p), os.path.basename(p)
    if os.path.isdir(p):
        for rel in ["", os.path.join("Dungeons","Binaries","Win64"), os.path.join("Binaries","Win64"), "Win64", "Dungeons"]:
            folder = os.path.join(p, rel) if rel else p
            exe = first_matching_exe(folder)
            if exe:
                return folder, exe
        # Last resort: recursive search
        for root, _dirs, files in os.walk(p):
            for name in files:
                if name.lower().endswith(".exe") and ("dungeons" in name.lower() or name in CANDIDATE_EXE_NAMES):
                    return root, name
    return None, None

def find_game_install_path_and_exe():
    """Finds the install path and the dungeons exe in it."""
    # Try custom path (file or folder)
    custom_path = load_custom_game_path()
    install, exe = resolve_from_custom(custom_path)
    if install and exe:
        return install, exe

    # Try default path
    user_home = os.path.expanduser("~")
    specific_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Binaries", "Win64")
    install, exe = resolve_from_custom(specific_path)
    if install and exe:
        return install, exe

    return None, None

def copy_files_to_game_folder(game_folder, files):
    """Copies specified files to the game folder silently."""
    for file in files:
        source_path = os.path.join(os.getcwd(), file)
        destination_path = os.path.join(game_folder, file)
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)

def start_game(game_executable, game_install_path):
    """Starts the game executable from the given path, hiding the console."""
    exe_path = os.path.join(game_install_path, game_executable)
    if os.path.isfile(exe_path):
        hide_console()
        subprocess.Popen(exe_path, shell=True)
    else:
        print(f"Error: {game_executable} not found in {game_install_path}")

def main():
    hide_console()  # Hide console immediately

    game_install_path, game_executable = find_game_install_path_and_exe()

    if game_install_path and game_executable:
        files_to_copy = ["winmm.dll", "RUNE.ini"]
        copy_files_to_game_folder(game_install_path, files_to_copy)
        start_game(game_executable, game_install_path)
    else:
        print("Error: No dungeons executable found in default or custom path")

if __name__ == "__main__":
    main()
