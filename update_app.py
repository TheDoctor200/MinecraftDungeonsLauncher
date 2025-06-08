import flet as ft
import requests
import json
import webbrowser
import os

GITHUB_API_URL = "https://api.github.com/repos/TheDoctor200/MinecraftDungeonsLauncher/releases/latest"
RELEASE_PAGE_URL = "https://github.com/TheDoctor200/MinecraftDungeonsLauncher/releases"
CURRENT_VERSION_FILE = "version.txt"

def get_current_version():
    try:
        if os.path.exists(CURRENT_VERSION_FILE):
            with open(CURRENT_VERSION_FILE, 'r') as version_file:
                return version_file.read().strip()
        return None
    except Exception:
        return None

def get_latest_version():
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)
        if response.status_code == 200:
            release_info = json.loads(response.text)
            return release_info.get("tag_name")
    except (requests.ConnectionError, requests.Timeout):
        return None
    return None

def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()
    if not current_version or not latest_version:
        return None, None
    return (current_version != latest_version, latest_version if current_version != latest_version else None)

def main(page: ft.Page):
    page.title = "Update Checker"
    page.window_width = 400
    page.window_height = 200
    page.window_resizable = False

    def show_dialog(title, message, show_yes_no=False, on_yes=None):
        actions = []
        if show_yes_no:
            actions.append(ft.TextButton("Yes", on_click=lambda e: (on_yes() if on_yes else None, close_dialog())))
            actions.append(ft.TextButton("No", on_click=lambda e: close_dialog()))
        else:
            actions.append(ft.TextButton("OK", on_click=lambda e: close_dialog()))
        dialog = ft.AlertDialog(
            title=ft.Text(title, size=22, weight=ft.FontWeight.BOLD),
            content=ft.Text(message, size=16),
            actions=actions,
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog():
        if page.dialog:
            page.dialog.open = False
            page.update()

    update_needed, latest_version = check_for_updates()

    if update_needed is True:
        def open_release():
            webbrowser.open(RELEASE_PAGE_URL)
        show_dialog(
            "Update Available",
            f"A new version {latest_version} is available. Do you want to open the download page?",
            show_yes_no=True,
            on_yes=open_release
        )
    elif update_needed is False:
        show_dialog("No Updates Available", "You are already using the latest version.")
    else:
        show_dialog("Update Check Failed", "Unable to check for updates at this time.")

ft.app(target=main)