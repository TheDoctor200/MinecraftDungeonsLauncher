import flet as ft
import subprocess
import os
import json

SETTINGS_FILE = "settings.json"
GAME_PATH_FILE = "game_path.json"
RUNE_INI_FILE = "RUNE.ini"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"app_scale": 1.0, "player_name": "Player"}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def load_game_path():
    try:
        with open(GAME_PATH_FILE, "r") as f:
            return json.load(f).get("game_path", "")
    except Exception:
        return ""

def save_game_path(game_path):
    with open(GAME_PATH_FILE, "w") as f:
        json.dump({"game_path": game_path}, f)

def update_rune_ini(player_name):
    if os.path.exists(RUNE_INI_FILE):
        with open(RUNE_INI_FILE, "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("UserName="):
                lines[i] = f"UserName={player_name}\n"
        with open(RUNE_INI_FILE, "w") as f:
            f.writelines(lines)

def main(page: ft.Page):
    page.title = "Minecraft Dungeons Launcher"
    page.window_width = 1100
    page.window_height = 700
    page.window_resizable = False
    page.bgcolor = "#15181e"
    page.fonts = {"Segoe UI": "assets/SegoeUI.ttf"}

    settings = load_settings()
    player_name = settings.get("player_name", "Player")
    page.scale = settings.get("app_scale", 1.0)

    # --- Button Actions ---
    def run_dll_hooker(e=None):
        try:
            subprocess.Popen(["python", "dll_hooker.pyw"])
        except Exception as ex:
            print(f"Error running dll_hooker.pyw: {ex}")

    def run_dll_unhooker(e=None):
        try:
            subprocess.Popen(["python", "dll_unhooker.pyw"])
        except Exception as ex:
            print(f"Error running dll_unhooker.pyw: {ex}")

    def run_charloc(e=None):
        try:
            subprocess.Popen(["python", "character_location_check.pyw"])
        except Exception as ex:
            print(f"Error running character_location_check.pyw: {ex}")

    def run_modloc(e=None):
        try:
            subprocess.Popen(["python", "mod_location_check.pyw"])
        except Exception as ex:
            print(f"Error running mod_location_check.pyw: {ex}")

    def run_start_game(e=None):
        try:
            custom_path = load_game_path()
            if custom_path and os.path.exists(custom_path):
                subprocess.Popen([custom_path])
            else:
                subprocess.Popen(["python", "start_game.pyw"])
        except Exception as ex:
            print(f"Error starting game: {ex}")

    # --- Modal Dialogs ---
    def show_settings_dialog(e=None):
        name_input = ft.TextField(
            value=player_name,
            label="Player Name",
            width=320,
            border_radius=8,
            border_color="#424242",
            focused_border_color="#FF5722",
            content_padding=10,
        )
        game_path_input = ft.TextField(
            value=load_game_path(),
            label="Custom Game Path (optional)",
            width=320,
            border_radius=8,
            border_color="#424242",
            focused_border_color="#FF5722",
            content_padding=10,
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Settings", size=28, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    name_input,
                    game_path_input,
                    ft.Text("Only set custom path if the game doesn't launch normally.", size=12, color="#808080", italic=True),
                ],
                spacing=16,
            ),
            actions=[
                ft.TextButton("Save", on_click=lambda e: save_and_close_settings(dialog, name_input, game_path_input)),
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
            ],
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def save_and_close_settings(dialog, name_input, game_path_input):
        nonlocal player_name
        player_name = name_input.value
        settings["player_name"] = player_name
        save_settings(settings)
        update_rune_ini(player_name)
        save_game_path(game_path_input.value.strip())
        dialog.open = False
        page.update()
        refresh_layout()

    def show_faq_dialog(e=None):
        try:
            with open("infos.txt", "r", encoding="utf-8") as f:
                faq_content = f.read()
        except Exception as ex:
            faq_content = f"FAQ file not found.\n{ex}"
        dialog = ft.AlertDialog(
            title=ft.Text("FAQ", size=28, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                ft.ListView(
                    controls=[
                        ft.Text(faq_content, size=16, selectable=True, font_family="Segoe UI"),
                    ],
                    width=600,
                    height=400,
                    padding=0,
                    auto_scroll=False,
                ),
                width=600,
                height=400,
                bgcolor="#23272F",
                border_radius=8,
                padding=16,
                expand=False,
            ),
            actions=[ft.TextButton("Close", on_click=lambda e: close_dialog(dialog))],
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # --- Navigation Handler ---
    def on_nav(action):
        if action == "play":
            run_start_game()
        elif action == "offline":
            run_dll_hooker()
        elif action == "charloc":
            run_charloc()
        elif action == "modloc":
            run_modloc()
        elif action == "faq":
            show_faq_dialog()
        elif action == "settings":
            show_settings_dialog()

    # --- Sidebar ---
    def sidebar(on_nav):
        return ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Image(
                            src="assets/avatar_default.png",
                            width=72, height=72, border_radius=36, fit=ft.ImageFit.COVER,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=24, bottom=12),
                    ),
                    ft.Text(player_name, size=20, color="#fff", weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
                    ft.Divider(height=24, color="#23272F"),
                    ft.IconButton(icon=ft.Icons.PLAY_ARROW, icon_color="#18e2d5", tooltip="Play Online", on_click=lambda e: on_nav("play")),
                    ft.IconButton(icon=ft.Icons.OFFLINE_BOLT, icon_color="#4CAF50", tooltip="Offline Play", on_click=lambda e: on_nav("offline")),
                    ft.IconButton(icon=ft.Icons.FOLDER_OPEN, icon_color="#2196F3", tooltip="Character Location", on_click=lambda e: on_nav("charloc")),
                    ft.IconButton(icon=ft.Icons.EXTENSION, icon_color="#2196F3", tooltip="Mods Location", on_click=lambda e: on_nav("modloc")),
                    ft.IconButton(icon=ft.Icons.HELP_OUTLINE, icon_color="#FF9800", tooltip="FAQ", on_click=lambda e: on_nav("faq")),
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color="#9E9E9E", tooltip="Settings", on_click=lambda e: on_nav("settings")),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.Image(src="assets/favicon.png", width=32, height=32),
                            ft.Text("v1.3", size=14, color="#B0B8C1", weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=16)
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            ),
            width=90,
            bgcolor="rgba(35,39,47,0.98)",
            border_radius=ft.border_radius.only(top_left=0, top_right=24, bottom_left=0, bottom_right=24),
            shadow=ft.BoxShadow(
                color="#00000066",
                blur_radius=18,
                offset=ft.Offset(0, 6),
            ),
            padding=ft.padding.only(top=0, left=0, right=0, bottom=0),
        )

    # --- Main Content ---
    def main_content():
        return ft.Container(
            ft.Column(
                [
                    ft.Image(
                        src="assets/launcher_hero.gif",  # Use a GIF if you want animation
                        width=540, height=200, fit=ft.ImageFit.CONTAIN, border_radius=18,
                    ),
                    ft.Text(
                        "Minecraft Dungeons Launcher",
                        size=38, weight=ft.FontWeight.BOLD, color="#fff", font_family="Segoe UI",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "A modern launcher for Minecraft Dungeons.\nPlay online, offline, manage mods, and more.",
                        size=18, color="#B0B8C1", text_align=ft.TextAlign.CENTER, font_family="Segoe UI",
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "PLAY ONLINE",
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=lambda e: run_dll_unhooker(e),
                                bgcolor="#FF5722",
                                color="#fff",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(horizontal=32, vertical=14),
                                    elevation=6,
                                ),
                            ),
                            ft.ElevatedButton(
                                "OFFLINE PLAY",
                                icon=ft.Icons.OFFLINE_BOLT,
                                on_click=lambda e: run_dll_hooker(e),
                                bgcolor="#4CAF50",
                                color="#fff",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(horizontal=32, vertical=14),
                                    elevation=6,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=24,
                    ),
                ],
                spacing=28,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor="rgba(35,39,47,0.92)",
            padding=48,
            border_radius=32,
            shadow=ft.BoxShadow(
                color="#00000088",
                blur_radius=24,
                offset=ft.Offset(0, 8),
            ),
            expand=True,
        )

    # --- Layout Refresh ---
    def refresh_layout():
        # Add background image as first control, then overlay the UI
        page.controls.clear()
        page.add(
            ft.Stack(
                [
                    ft.Image(
                        src="assets/launcher_bg.jpg",
                        width=page.window_width,
                        height=page.window_height,
                        fit=ft.ImageFit.COVER,
                        opacity=0.18,
                        left=0, top=0, right=0, bottom=0, expand=True,
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                sidebar(on_nav),
                                ft.Container(width=24),
                                main_content(),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )
        page.update()

    refresh_layout()

ft.app(target=main, assets_dir="assets")
