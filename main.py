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


def   _game_path(game_path):
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
    page.window_width = 1920
    page.window_height = 1080
    page.window_resizable = False
    page.bgcolor = "transparent"
    page.fonts = {"Segoe UI": "assets/SegoeUI.ttf"}
    page.padding = 0  # Remove all padding to avoid black edges

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
                    ft.Text(player_name, size=20, color="#fff", weight=ft.FontWeight.BOLD, font_family="Segoe UI"),
                    ft.Divider(height=24, color=ft.Colors.WHITE),
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
                    # --- New Update App Button ---
                    ft.TextButton(
                        content=ft.Row([
                            ft.Text("Update App", size=15, color="#FFC107", font_family="Segoe UI"),
                            ft.Icon(ft.Icons.SYSTEM_UPDATE, color="#FFC107", size=22),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                        style=ft.ButtonStyle(
                            bgcolor={"": "transparent"},
                            shape={"": ft.RoundedRectangleBorder(radius=12)},
                            padding={"": 10},
                        ),
                        on_click=lambda e: subprocess.Popen(["python", "update_app.py"]),
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.Image(src="assets/favicon.png", width=32, height=32),
                            ft.Text("v1.35", size=14, color="#B0B8C1", weight=ft.FontWeight.BOLD),
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
            width=140,
            bgcolor="rgba(35,39,47,0.98)",
            border_radius=ft.border_radius.only(top_left=0, top_right=24, bottom_left=0, bottom_right=24),
            shadow=ft.BoxShadow(
                color="#00000066",
                blur_radius=18,
                offset=ft.Offset(0, 6),
            ),
            # Add top padding to move all buttons down
            padding=ft.padding.only(top=88, left=0, right=0, bottom=0),
        )

    # --- Main Content ---
    def main_content():
        # Add stateful controls for game path and player name
        game_path_field = ft.TextField(
            label="Game Executable Path",
            value=load_game_path(),
            width=340,  # Smaller width
            text_align=ft.TextAlign.CENTER,
            border_radius=10,  # Slightly smaller radius
            bgcolor="transparent",
            color=ft.Colors.WHITE,
            border_color="#18e2d5",
            cursor_color=ft.Colors.WHITE,
            selection_color="#18e2d5",
            hint_style=ft.TextStyle(color=ft.Colors.WHITE),
        )
        # Load player name directly from RUNE.ini
        def load_player_name_from_rune():
            if os.path.exists(RUNE_INI_FILE):
                with open(RUNE_INI_FILE, "r") as f:
                    for line in f:
                        if line.startswith("UserName="):
                            return line.strip().split("=", 1)[-1]
            return "Player"
        player_name_field = ft.TextField(
            label="Player Name (RUNE.ini)",
            value=load_player_name_from_rune(),
            width=340,  # Smaller width
            text_align=ft.TextAlign.CENTER,
            border_radius=10,
            bgcolor="transparent",
            color=ft.Colors.WHITE,
            border_color="#18e2d5",
            cursor_color=ft.Colors.WHITE,
            selection_color="#18e2d5",
            hint_style=ft.TextStyle(color=ft.Colors.WHITE),
        )

        def save_settings_fields(e):
            # Only update the corresponding files
            save_game_path(game_path_field.value)
            update_rune_ini(player_name_field.value)
            page.snack_bar = ft.SnackBar(ft.Text("Settings saved!"), bgcolor="#23272F")
            page.snack_bar.open = True
            page.update()

        save_btn = ft.ElevatedButton(
            "Save",
            icon=ft.Icons.SAVE,
            bgcolor="transparent",  # Remove turquoise, let blur show through
            color=ft.Colors.WHITE,
            on_click=save_settings_fields,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=12)},
                padding={"": 16},
            ),
        )

        # Add blur effect inside the text fields and save button using decoration
        def blurred_input(field):
            return ft.Container(
                field,
                bgcolor="rgba(35,39,47,0.92)",
                blur=ft.Blur(sigma_x=3, sigma_y=3),
                border_radius=10,
                padding=6,
                expand=False,
            )

        def blurred_button(button):
            return ft.Container(
                button,
                bgcolor="rgba(35,39,47,0.92)",
                blur=ft.Blur(sigma_x=3, sigma_y=3),
                border_radius=10,
                padding=6,
                expand=False,
            )

        return ft.Container(
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
                        margin=ft.margin.only(top=16),
                    ),
                    ft.Image(
                        src="assets/DungeonsBG.gif",
                        width=750,
                        height=250,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=24,
                    ),
                    # --- Side by side title and subtitle ---
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "A modern launcher for Minecraft Dungeons.",
                                    size=18,
                                    color=ft.Colors.WHITE,
                                    font_family="Segoe UI",
                                    text_align=ft.TextAlign.LEFT,
                                ),
                                ft.Text(
                                    "Play online, offline, manage mods, and more.",
                                    size=18,
                                    color=ft.Colors.WHITE,
                                    font_family="Segoe UI",
                                    text_align=ft.TextAlign.LEFT,
                                ),
                            ],
                            spacing=8,  # Normal/small space between texts
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=0, bottom=0),
                    ),
                    # --- New selection bars and save button ---
                    ft.Container(
                        ft.Column(
                            [
                                blurred_input(game_path_field),
                                blurred_input(player_name_field),
                                blurred_button(save_btn),
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=20, bottom=0),
                    ),
                ],
                spacing=24,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor="rgba(35,39,47,0.92)",
            padding=ft.padding.only(top=0, left=24, right=24, bottom=24),
            border_radius=32,
            expand=True,
        )

    def refresh_layout():
        # Responsive background image: always fully visible, fills window, never cropped or zoomed in
        page.controls.clear()
        page.add(
            ft.Stack(
                [
                    ft.Image(
                        src="assets/BG_Launcher.gif",
                        expand=True,
                        fit=ft.ImageFit.FIT_HEIGHT,  # Ensures full height is visible, less cropping of bottom/middle
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        left=0,
                        top=0,
                    ),
                    ft.Container(
                        bgcolor="rgba(21,24,30,0.20)",
                        blur=ft.Blur(sigma_x=4, sigma_y=4),
                        expand=True,
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
                    ft.Image(
                        src="assets/Glow_Squidy.gif",
                        width=72,
                        height=72,
                        fit=ft.ImageFit.CONTAIN,
                        left=32,
                        top=40,
                    ),
                ],
                expand=True,
            )
        )
        page.update()

    refresh_layout()

ft.app(target=main, assets_dir="assets")
