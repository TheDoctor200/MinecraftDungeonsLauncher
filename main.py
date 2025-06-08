import flet as ft
import subprocess
import os
import json

SETTINGS_FILE = "settings.json"
GAME_PATH_FILE = "game_path.json"
RUNE_INI_FILE = "RUNE.ini"
INFOS_FILE = "infos.txt"


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

    # Read infos.txt content at startup
    try:
        with open(INFOS_FILE, "r", encoding="utf-8") as f:
            faq_content = f.read()
    except Exception:
        faq_content = "FAQ file not found."

    faq_text_control = ft.Text(
        faq_content,
        selectable=True,
        size=16,
        color=ft.Colors.WHITE,  # Use Colors enum (not colors)
        font_family="Segoe UI",
        opacity=1.0,
    )

    faq_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("FAQ", weight=ft.FontWeight.BOLD, size=24),
        content=faq_text_control,
        actions=[ft.TextButton("Close", on_click=lambda e: page.close(faq_dialog))],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="rgba(30,32,40,0.92)",  # Less transparent, more solid dark background
        elevation=16,                   # Softer shadow
        surface_tint_color=None,        # Remove tint for clarity
        shadow_color="#00000088",       # Subtle shadow
        # border_radius=24,             # Still not supported
        on_dismiss=None,
    )

    def show_faq(e=None):
        page.dialog = faq_dialog
        page.open(faq_dialog)

    # --- Button Actions ---
    def run_dll_hooker(e=None):
        try:
            subprocess.Popen(["python", "dll_hooker.py"])
        except Exception as ex:
            print(f"Error running dll_hooker.py: {ex}")

    def run_dll_unhooker(e=None):
        try:
            subprocess.Popen(["python", "dll_unhooker.py"])
        except Exception as ex:
            print(f"Error running dll_unhooker.py: {ex}")

    def run_charloc(e=None):
        try:
            subprocess.Popen(["python", "character_location_check.py"])
        except Exception as ex:
            print(f"Error running character_location_check.py: {ex}")

    def run_modloc(e=None):
        try:
            subprocess.Popen(["python", "mod_location_check.py"])
        except Exception as ex:
            print(f"Error running mod_location_check.py: {ex}")

    def run_start_game(e=None):
        try:
            custom_path = load_game_path()
            if custom_path and os.path.exists(custom_path):
                subprocess.Popen([custom_path])
            else:
                subprocess.Popen(["python", "dll_unhooker.py"])
        except Exception as ex:
            print(f"Error starting game: {ex}")

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

    # --- Sidebar ---
    def sidebar(on_nav):
        return ft.Container(
            ft.Column(
                [
                    # Removed avatar_default.png
                    ft.Container(
                        ft.Text(player_name, size=20, color="#fff", weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=4,
                    ),
                    ft.Container(
                        ft.Divider(height=24, color="#23272F"),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=8,
                        blur=8,
                        padding=2,
                    ),
                    # TextButtons with icon on the right, each in a mica container
                    ft.Container(
                        ft.TextButton(
                            content=ft.Row([
                                ft.Text("Online", size=15, color="#18e2d5", font_family="Segoe UI"),
                                ft.Icon(ft.Icons.PLAY_ARROW, color="#18e2d5", size=22),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                            style=ft.ButtonStyle(
                                bgcolor={"": "transparent"},
                                shape={"": ft.RoundedRectangleBorder(radius=12)},
                                padding={"": 10},
                            ),
                            on_click=lambda e: on_nav("play"),
                        ),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=2,
                    ),
                    ft.Container(
                        ft.TextButton(
                            content=ft.Row([
                                ft.Text("Offline", size=15, color="#4CAF50", font_family="Segoe UI"),
                                ft.Icon(ft.Icons.OFFLINE_BOLT, color="#4CAF50", size=22),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                            style=ft.ButtonStyle(
                                bgcolor={"": "transparent"},
                                shape={"": ft.RoundedRectangleBorder(radius=12)},
                                padding={"": 10},
                            ),
                            on_click=lambda e: on_nav("offline"),
                        ),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=2,
                    ),
                    ft.Container(
                        ft.TextButton(
                            content=ft.Row([
                                ft.Text("Character", size=15, color="#2196F3", font_family="Segoe UI"),
                                ft.Icon(ft.Icons.FOLDER_OPEN, color="#2196F3", size=22),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                            style=ft.ButtonStyle(
                                bgcolor={"": "transparent"},
                                shape={"": ft.RoundedRectangleBorder(radius=12)},
                                padding={"": 10},
                            ),
                            on_click=lambda e: on_nav("charloc"),
                        ),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=2,
                    ),
                    ft.Container(
                        ft.TextButton(
                            content=ft.Row([
                                ft.Text("Mods", size=15, color="#2196F3", font_family="Segoe UI"),
                                ft.Icon(ft.Icons.EXTENSION, color="#2196F3", size=22),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                            style=ft.ButtonStyle(
                                bgcolor={"": "transparent"},
                                shape={"": ft.RoundedRectangleBorder(radius=12)},
                                padding={"": 10},
                            ),
                            on_click=lambda e: on_nav("modloc"),
                        ),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=2,
                    ),
                    ft.Container(
                        ft.TextButton(
                            content=ft.Row([
                                ft.Text("FAQ", size=15, color="#18e2d5", font_family="Segoe UI"),
                                ft.Icon(ft.Icons.HELP_OUTLINE, color="#18e2d5", size=22),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                            style=ft.ButtonStyle(
                                bgcolor={"": "transparent"},
                                shape={"": ft.RoundedRectangleBorder(radius=12)},
                                padding={"": 10},
                            ),
                            on_click=show_faq,
                        ),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=2,
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Image(src="assets/favicon.png", width=32, height=32),
                                ft.Text("v1.3", size=14, color="#B0B8C1", weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor="rgba(255,255,255,0.10)",
                        border_radius=12,
                        blur=8,
                        padding=4,
                    ),
                    ft.Container(height=16)
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            ),
            width=140,
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
            ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            ft.Text(
                                "Minecraft Dungeons Launcher",
                                size=38,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                                font_family="Segoe UI",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            bgcolor="rgba(255,255,255,0.10)",
                            border_radius=12,
                            blur=8,
                            padding=8,
                        ),
                        ft.Container(
                            ft.Image(
                                src="assets/DungeonsBG.gif",
                                width=900,  # Shrink width
                                height=340, # Slightly taller
                                fit=ft.ImageFit.CONTAIN,
                                border_radius=24,
                            ),
                            bgcolor="rgba(255,255,255,0.10)",
                            border_radius=18,
                            blur=8,
                            padding=ft.padding.only(left=48, right=48, top=0, bottom=0),  # Shrink left/right padding
                            margin=ft.margin.only(top=16, bottom=16),  # Expand mica to top/bottom
                        ),
                        ft.Container(
                            ft.Text(
                                "A modern launcher for Minecraft Dungeons.\nPlay online, offline, manage mods, and more.",
                                size=18, color="#B0B8C1", text_align=ft.TextAlign.CENTER, font_family="Segoe UI",
                            ),
                            bgcolor="rgba(255,255,255,0.10)",
                            border_radius=12,
                            blur=8,
                            padding=8,
                        ),
                    ],
                    spacing=22,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                bgcolor="rgba(35,39,47,0.92)",
                padding=32,
                border_radius=32,
                shadow=ft.BoxShadow(
                    color="#00000088",
                    blur_radius=24,
                    offset=ft.Offset(0, 8),
                ),
                expand=True,
            ),
            expand=True,
        )

    # --- Layout Refresh ---
    def refresh_layout():
        # Add background gif as first control, then overlay the UI
        page.controls.clear()
        page.add(
            ft.Stack(
                [
                    ft.Container(
                        content=ft.Image(
                            src="assets/BG_Launcher.gif",
                            fit=ft.ImageFit.COVER,
                            opacity=0.18,
                            expand=True,
                        ),
                        expand=True,
                        bgcolor="rgba(255,255,255,0.13)",
                        blur=8,
                    ),
                    # Place Glow Squid gif above mica layer
                    ft.Container(
                        ft.Image(
                            src="assets/Glow_Squidy.gif",
                            width=72,
                            height=72,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        left=32,
                        top=40,
                        width=72,
                        height=72,
                        bgcolor=None,
                        border_radius=36,
                        alignment=ft.alignment.top_left,
                        z_index=2,  # Ensure above mica
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
