import webbrowser
import ctypes
import time
import requests
import json
import sys
import os

# Lightweight result object for integration with the Flet app
class UpdateResult:
    def __init__(self, status: str, current_version: str = None, latest_version: str = None, message: str = None, release_url: str = None):
        self.status = status  # one of: 'update_available', 'up_to_date', 'error'
        self.current_version = current_version
        self.latest_version = latest_version
        self.message = message
        self.release_url = release_url

# Constants
GITHUB_API_URL = "https://api.github.com/repos/TheDoctor200/MinecraftDungeonsLauncher/releases/latest"
RELEASE_PAGE_URL = "https://github.com/TheDoctor200/MinecraftDungeonsLauncher/releases"
CURRENT_VERSION_FILE = "version.txt"  # Path to your app version file

# Utility to display message boxes
def show_message_box(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)  # 0x40 = INFO_ICON, 0x1 = OK_BUTTON

# Function to get current version from the local version file
def get_current_version(version_file: str = CURRENT_VERSION_FILE):
    try:
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as vf:
                return vf.read().strip()
        else:
            print("Version file not found. Ensure the version.txt file exists.")
            return None  # No version file found
    except Exception as e:
        print(f"Error reading current version: {e}")
        return None

# Function to check for the latest version on GitHub
def get_latest_version():
    try:
        headers = {"Accept": "application/vnd.github+json"}
        response = requests.get(GITHUB_API_URL, timeout=10, headers=headers)
        if response.status_code == 200:
            release_info = json.loads(response.text)
            if "tag_name" in release_info:
                return release_info["tag_name"]
            else:
                print("No 'tag_name' found in the GitHub API response. Please check the API structure.")
                return None
        else:
            print(f"Failed to get latest version. HTTP Status code: {response.status_code}")
            return None
    except requests.ConnectionError:
        print("Failed to connect to GitHub API. Please check your internet connection.")
        return None
    except requests.Timeout:
        print("Request to GitHub API timed out.")
        return None

def _normalize_version(v: str) -> str:
    """Normalize version by stripping common prefixes/spaces."""
    if v is None:
        return None
    v = v.strip()
    if v.lower().startswith('v'):
        v = v[1:]
    return v

def _version_key(v: str):
    """Convert version string into a tuple for comparison. Falls back to string if not purely numeric."""
    v = _normalize_version(v) or ""
    parts = []
    for p in v.replace('-', '.').split('.'):
        if p.isdigit():
            parts.append(int(p))
        else:
            # split numeric+alpha like 'rc1'
            num = ''
            alpha = ''
            for ch in p:
                if ch.isdigit() and alpha == '':
                    num += ch
                else:
                    alpha += ch
            parts.append(int(num) if num else 0)
            if alpha:
                parts.append(alpha)
    return tuple(parts) if parts else (0,)

# Function to check if update is needed
def check_for_updates():
    """Backward-compatible tuple API: (update_needed, latest_version)
    Returns:
        (True, latest) if update available
        (False, None) if up to date
        (None, None) on error
    """
    res = check_for_updates_result()
    if res.status == 'update_available':
        return True, res.latest_version
    if res.status == 'up_to_date':
        return False, None
    return None, None

def check_for_updates_result() -> UpdateResult:
    """Rich API for integrations: returns UpdateResult."""
    current_version = get_current_version()
    if current_version is None:
        return UpdateResult('error', current_version=None, message='Current version not found')

    latest_version = get_latest_version()
    if latest_version is None:
        return UpdateResult('error', current_version=current_version, message='Failed to retrieve latest version')

    cv = _normalize_version(current_version)
    lv = _normalize_version(latest_version)
    try:
        is_newer = _version_key(lv) > _version_key(cv)
    except Exception:
        # Fallback to strict string inequality
        is_newer = lv != cv

    if is_newer:
        msg = f"A new version {latest_version} is available. You are currently using {current_version}."
        return UpdateResult('update_available', current_version=current_version, latest_version=latest_version, message=msg, release_url=RELEASE_PAGE_URL)
    else:
        msg = "You are already using the latest version of the app."
        return UpdateResult('up_to_date', current_version=current_version, latest_version=latest_version, message=msg, release_url=RELEASE_PAGE_URL)

# Main update function
def main():
    # Checking for updates using the rich API
    result = check_for_updates_result()

    if result.status == 'update_available':
        show_message_box(
            "Update Available",
            result.message or f"A new version {result.latest_version} is available."
        )
        if result.release_url:
            webbrowser.open(result.release_url)
        time.sleep(2)
    elif result.status == 'up_to_date':
        show_message_box(
            "No Updates Available",
            result.message or "You are already using the latest version of the app."
        )
    else:
        show_message_box(
            "Update Check Failed",
            result.message or "Unable to check for updates at this time. Please try again later."
        )
    sys.exit()

if __name__ == "__main__":

    # Hiding the console window
    SW_HIDE = 0
    GetConsoleWindow = ctypes.windll.kernel32.GetConsoleWindow
    ShowWindow = ctypes.windll.user32.ShowWindow
    ShowWindow(GetConsoleWindow(), SW_HIDE)
    
    main()