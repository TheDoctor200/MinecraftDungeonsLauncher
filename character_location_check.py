import os
import subprocess
import ctypes
import sys

def hide_console():
    """Hides the console window (Works for Windows only)."""
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def check_and_open_directory():
    """Checks if the directory exists and opens it in Explorer if found."""
    user_home = os.path.expanduser("~")
    path = os.path.join(user_home, "Saved Games", "Mojang Studios", "Dungeons")

    if os.path.exists(path):
        usernames = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        subprocess.run(["explorer", path], check=True, shell=True)
    else:
        pass  # No output since the console is hidden

if __name__ == "__main__":
    hide_console()  # Hide the console before executing
    check_and_open_directory()
