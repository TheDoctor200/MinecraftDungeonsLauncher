import os
import shutil
import ctypes
import sys

def hide_console():
    """Hides the console window (Windows only)."""
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def find_game_install_path(game_executable):
    """Finds the installation path of the game based on the given executable."""
    user_home = os.path.expanduser("~")
    specific_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Binaries", "Win64")
    game_executable_path = os.path.join(specific_path, game_executable)

    return specific_path if os.path.exists(game_executable_path) else None

def copy_files_to_game_folder(game_folder, files):
    """Copies specified files to the game folder silently."""
    for file in files:
        source_path = os.path.join(os.getcwd(), file)
        destination_path = os.path.join(game_folder, file)

        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)

def main():
    hide_console()  # Hide console immediately

    game_executable = "Dungeons-Win64-Shipping.exe"
    game_install_path = find_game_install_path(game_executable)

    if game_install_path:
        files_to_copy = ["winmm.dll", "RUNE.ini"]
        copy_files_to_game_folder(game_install_path, files_to_copy)

if __name__ == "__main__":
    main()
