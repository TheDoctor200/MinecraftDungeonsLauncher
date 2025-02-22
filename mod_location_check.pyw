import os
import subprocess
import ctypes
import sys

def hide_console():
    """Hides the console window (Windows only)."""
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def check_and_open_directory():
    """Checks if the directory exists and opens it in Explorer if found, silently."""
    user_home = os.path.expanduser("~")
    path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Content", "Paks")
    
    if os.path.exists(path):
        subprocess.run(["explorer", path], check=True, shell=True)

def main():
    hide_console()  # Hide console immediately
    check_and_open_directory()

if __name__ == "__main__":
    main()

