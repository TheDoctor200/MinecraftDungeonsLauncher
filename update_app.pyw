import webbrowser
import ctypes
import time
import requests
import json
import sys
import os

# Constants
GITHUB_API_URL = "https://api.github.com/repos/TheDoctor200/MinecraftDungeonsLauncher/releases/latest"
RELEASE_PAGE_URL = "https://github.com/TheDoctor200/MinecraftDungeonsLauncher/releases"
CURRENT_VERSION_FILE = "version.txt"  # Path to your app version file

# Utility to display message boxes in foreground
def show_message_box(title, message, buttons=0x40 | 0x1 | 0x40000):
    # Display the message box
    ctypes.windll.user32.MessageBoxW(0, message, title, buttons)

    # Get the message box window handle
    hwnd = ctypes.windll.user32.GetForegroundWindow()

    # Maximize the message box window
    ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = SW_MAXIMIZE

    # Bring the message box to the foreground
    ctypes.windll.user32.SetForegroundWindow(hwnd)

# Function to get current version from the local version file
def get_current_version():
    try:
        if os.path.exists(CURRENT_VERSION_FILE):
            with open(CURRENT_VERSION_FILE, 'r') as version_file:
                return version_file.read().strip()
        return None  # No version file found
    except Exception:
        return None

# Function to check for the latest version on GitHub
def get_latest_version():
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)  # Increased timeout to 10 seconds
        if response.status_code == 200:
            release_info = json.loads(response.text)
            return release_info.get("tag_name")
    except (requests.ConnectionError, requests.Timeout):
        return None
    return None

# Function to check if update is needed
def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()

    if not current_version or not latest_version:
        return None, None

    return (current_version != latest_version, latest_version if current_version != latest_version else None)

# Main update function
def main():
    update_needed, latest_version = check_for_updates()

    if update_needed is True:
        response = show_message_box("Update Available", f"A new version {latest_version} is available. Do you want to open the download page?", 0x40 | 0x1 | 0x2 | 0x40000)  # Yes/No Buttons
        if response == 6:  # 6 = IDYES
            webbrowser.open(RELEASE_PAGE_URL)
        
    elif update_needed is False:
        show_message_box("No Updates Available", "You are already using the latest version.")

    else:
        show_message_box("Update Check Failed", "Unable to check for updates at this time.")

    sys.exit()

if __name__ == "__main__":
    main()
