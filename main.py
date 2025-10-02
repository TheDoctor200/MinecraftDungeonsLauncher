import sys
import flet as ft
import subprocess
import json
import os
from typing import Optional

# Ensure local directory is importable for .pyw modules
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
except Exception:
    BASE_DIR = os.getcwd()

def _load_module_from_file(mod_name: str, file_name: str):
    try:
        path = os.path.join(BASE_DIR, file_name)
        if not os.path.exists(path):
            return None
        import importlib.util
        spec = importlib.util.spec_from_file_location(mod_name, path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    except Exception:
        return None
    return None

# Local helpers (import if available; otherwise keep subprocess fallback)
try:
    import update_app as updater
except Exception:
    updater = _load_module_from_file("update_app", "update_app.pyw")
try:
    import character_location_check as char_loc
except Exception:
    char_loc = _load_module_from_file("character_location_check", "character_location_check.pyw")
try:
    import mod_location_check as mod_loc
except Exception:
    mod_loc = _load_module_from_file("mod_location_check", "mod_location_check.pyw")
try:
    import dll_hooker as dll_hook
except Exception:
    dll_hook = _load_module_from_file("dll_hooker", "dll_hooker.pyw")
try:
    import dll_unhooker as dll_unhook
except Exception:
    dll_unhook = _load_module_from_file("dll_unhooker", "dll_unhooker.pyw")

# --- Flet compatibility shims (support older/newer APIs) ---
COLORS = getattr(ft, "colors", None) or getattr(ft, "Colors", None)
ICONS = getattr(ft, "icons", None) or getattr(ft, "Icons", None)
BLUR = getattr(ft, "Blur", None)
BLUR_TILE_MODE = getattr(ft, "BlurTileMode", None)

def col(name: str, default: str = "#FFFFFF"):
    """Get a color constant from Flet colors/Colors with fallback.
    Tries UPPER then lower case attribute; falls back to provided default string.
    """
    if COLORS is None:
        return default
    return getattr(COLORS, name, getattr(COLORS, name.lower(), default))

# --- Theme (Minecraft launcher-inspired) ---
ACCENT = "#3C8527"  # Minecraft green
ACCENT_TEXT = "#FFFFFF"

# --- Constants ---
SETTINGS_FILE = "settings.json"
GAME_PATH_FILE = "game_path.json"
RUNE_INI_FILE = "RUNE.ini"
INFOS_FILE = "infos.txt"
VERSION_FILE = "version.txt"
MODS_PATH_KEY = "mods_folder"

# --- Helper Functions ---

def load_json_file(file_path, default_data):
    """Loads data from a JSON file, returning default data on failure."""
    if not os.path.exists(file_path):
        return default_data
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default_data

def save_json_file(file_path, data):
    """Saves data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError:
        # Handle save errors if necessary
        pass

def load_settings():
    """Loads application settings."""
    # Add mods_folder with default empty string
    return load_json_file(SETTINGS_FILE, {"player_name": "Player", "app_scale": 1.0, MODS_PATH_KEY: ""})

def save_settings(settings):
    """Saves application settings."""
    save_json_file(SETTINGS_FILE, settings)

def load_game_path():
    """Loads the game path."""
    data = load_json_file(GAME_PATH_FILE, {"game_path": ""})
    return data.get("game_path", "")

def save_game_path(game_path):
    """Saves the game path."""
    save_json_file(GAME_PATH_FILE, {"game_path": game_path})

def get_app_version():
    """Reads the version from version.txt."""
    if not os.path.exists(VERSION_FILE):
        return "v1.35"
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except IOError:
        return "v1.35"

def update_rune_ini(player_name: str):
    """Updates UserName in RUNE.ini under [Settings]. Creates it if missing."""
    try:
        lines = []
        if os.path.exists(RUNE_INI_FILE):
            # Read with tolerant decoding in case of non-UTF8 chars
            with open(RUNE_INI_FILE, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        else:
            # Initialize file with Settings section if missing
            lines = ["[Settings]\n"]

        found_username = False
        settings_index = None
        for idx, line in enumerate(lines):
            s = line.strip()
            if s.lower() == "[settings]":
                settings_index = idx
            # Replace any existing UserName entry (case-insensitive, tolerate spaces)
            if s.lower().startswith("username"):
                eq_pos = line.find("=")
                prefix = line[: eq_pos + 1] if eq_pos != -1 else "UserName="
                # Preserve any spacing after '='
                suffix_space = ""
                if eq_pos != -1 and eq_pos + 1 < len(line) and line[eq_pos + 1] == " ":
                    suffix_space = " "
                lines[idx] = f"{prefix}{suffix_space}{player_name}\n"
                found_username = True
                break

        if not found_username:
            # Insert UserName after [Settings] if present, else add a [Settings] header
            insert_at = None
            if settings_index is not None:
                insert_at = settings_index + 1
            else:
                lines.append("[Settings]\n")
                insert_at = len(lines)
            lines.insert(insert_at, f"UserName={player_name}\n")

        with open(RUNE_INI_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except IOError:
        # Silently ignore write errors per original behavior
        pass

def run_script(script_name):
    """Runs an external Python script."""
    try:
        subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), script_name])
    except Exception:
        pass

def read_game_exe_dir() -> Optional[str]:
    try:
        with open(GAME_PATH_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            gp = data.get("game_path", "")
            if gp:
                exe_dir = os.path.dirname(gp)
                if os.path.isdir(exe_dir):
                    return exe_dir
    except Exception:
        return None
    return None

# --- Main Application Class ---

class MinecraftDungeonsLauncher:
    def __init__(self, page: ft.Page):
        self.page = page
        self.settings = load_settings()
        self.game_path = load_game_path()
        self.player_name = self.settings.get("player_name", "Player")
        self.mods_folder = self.settings.get(MODS_PATH_KEY, "")
        # Use non-generic Ref for wider compatibility with older Flet versions
        self.is_online = ft.Ref()

        # Initialize page settings
        self.page.title = "Minecraft Dungeons Launcher"
        self.page.window_width = 1280
        self.page.window_height = 720
        self.page.window_resizable = False
        # Use a transparent background if supported; fallback to None
        self.page.bgcolor = None
        self.page.fonts = {"Segoe UI": "assets/SegoeUI.ttf"}
        self.page.padding = 0
        self.page.window_frameless = True
        self.page.window_title_bar_hidden = True
        self.page.window_title_bar_buttons_hidden = True

    def build(self):
        # --- UI Controls ---
        self.game_path_field = ft.TextField(
            value=self.game_path,
            label="Game Path (folder or exe)",
            width=400,
            border_color="#18e2d5",
        )
        self.player_name_field = ft.TextField(
            value=self.player_name,
            label="Player Name",
            width=400,
            border_color="#18e2d5",
        )
        self.mods_folder_field = ft.TextField(
            value=self.mods_folder,
            label="Mods Folder Path",
            width=400,
            border_color="#18e2d5",
            hint_text="e.g. C:\\Games\\MinecraftDungeons\\Content\\Paks\\~mods",
        )

        # --- Views ---
        self.main_view = self._create_main_view()
        self.settings_view = self._create_settings_view()

        # --- Main Layout ---
        self.view_fader = ft.AnimatedSwitcher(
            content=self.main_view,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=100,
        )

        return ft.Stack(
            [
                ft.Image(
                    src="assets/BG_Launcher.gif",
                    width=self.page.window_width,
                    height=self.page.window_height,
                    fit=ft.ImageFit.COVER,
                ),
                # Blur overlay (if supported); otherwise acts as a transparent overlay
                ft.Container(
                    width=self.page.window_width,
                    height=self.page.window_height,
                    blur=BLUR(6, 6, getattr(BLUR_TILE_MODE, "MIRROR", None)) if BLUR else None,
                ),
                # Top-left animated glow
                ft.Image(
                    src="assets/Glow_Squidy.gif",
                    width=96,
                    height=96,
                    top=40,
                    left=10,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Column(
                    [
                        ft.WindowDragArea(
                            ft.Container(height=30), expand=True
                        ),
                        ft.Container(
                            content=self.view_fader,
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    get_app_version(),
                    bottom=10,
                    right=15,
                    size=12,
                    color=col("WHITE54", "#FFFFFF"),
                ),
            ]
        )

    def _create_main_view(self):
        """Creates the main view with the launch button and actions."""
        return ft.Container(
            ft.Column(
                [
                    ft.Image(
                        src="assets/Minecraft_Dungeons_Ultimate_Edition.png",
                        width=500,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.ElevatedButton(
                        "Launch Game",
                        icon=ICONS.PLAY_ARROW if hasattr(ICONS, "PLAY_ARROW") else "play_arrow",
                        on_click=self._launch_game,
                        width=250,
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            bgcolor=ACCENT,
                            color=ACCENT_TEXT,
                        ),
                    ),
                    ft.Row(
                        [
                            ft.Text("Offline"),
                            ft.Switch(ref=self.is_online, value=True, on_change=self._toggle_online),
                            ft.Text("Online"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=20),
                    # Simple action bar without background
                    ft.Row(
                        [
                            self._create_action_button(ICONS.FOLDER_OPEN if hasattr(ICONS, "FOLDER_OPEN") else "folder_open", "Character", self._open_character_dir),
                            self._create_action_button(ICONS.EXTENSION if hasattr(ICONS, "EXTENSION") else "extension", "Mods", self._show_mod_manager),
                            self._create_action_button(ICONS.HELP_OUTLINE if hasattr(ICONS, "HELP_OUTLINE") else "help_outline", "FAQ", self._show_faq),
                            self._create_action_button(ICONS.SETTINGS if hasattr(ICONS, "SETTINGS") else "settings", "Settings", self._show_settings),
                            self._create_action_button(ICONS.SYSTEM_UPDATE if hasattr(ICONS, "SYSTEM_UPDATE") else "system_update", "Update", self._check_updates_ui),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=28,
                    ),
                    # Decorative bar removed as requested
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
        )

    def _create_settings_view(self):
        """Creates the settings view."""
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD),
                    self.game_path_field,
                    self.player_name_field,
                    self.mods_folder_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Save", icon=ICONS.SAVE if hasattr(ICONS, "SAVE") else "save", on_click=self._save_and_close_settings, bgcolor=ACCENT, color=ACCENT_TEXT),
                            ft.OutlinedButton("Back", icon=ICONS.ARROW_BACK if hasattr(ICONS, "ARROW_BACK") else "arrow_back", on_click=self._show_main),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
        )

    def _create_action_button(self, icon, tooltip, on_click):
        """Helper to create consistent icon buttons."""
        return ft.IconButton(icon=icon, tooltip=tooltip, on_click=on_click, icon_size=28)

    # --- Event Handlers ---

    def _launch_game(self, e):
        """Handler for the launch game button."""
        if self.is_online.current.value:
            # Online mode uses dll_unhooker
            if dll_unhook is not None:
                try:
                    dll_unhook.main()
                except Exception:
                    run_script("dll_unhooker.pyw")
            else:
                run_script("dll_unhooker.pyw")
        else:
            # Offline mode uses dll_hooker
            if dll_hook is not None:
                try:
                    dll_hook.main()
                except Exception:
                    run_script("dll_hooker.pyw")
            else:
                run_script("dll_hooker.pyw")
        # Hooker scripts are responsible for starting the game
        return

    def _open_character_dir(self, e):
        if char_loc is not None and hasattr(char_loc, "check_and_open_directory"):
            try:
                char_loc.check_and_open_directory()
                # Only call fallback if import failed, not on exception
                return
            except Exception:
                # Do not fallback here, as the imported function may have already opened the folder
                return
        run_script("character_location_check.pyw")

    def _open_mods_dir(self, e):
        if mod_loc is not None and hasattr(mod_loc, "check_and_open_directory"):
            try:
                mod_loc.check_and_open_directory()
                return
            except Exception:
                pass
        run_script("mod_location_check.pyw")

    # --- Mod Manager ---
    def _show_mod_manager(self, e):
        mods_dir = self.settings.get(MODS_PATH_KEY, "")
        if not mods_dir or not os.path.isdir(mods_dir):
            self._show_info_dialog(
                "Mods Folder Not Set",
                "Please specify your mods folder path in Settings first (e.g. Content\\Paks\\~mods)."
            )
            return

        list_view = ft.ListView(expand=1, spacing=6, padding=0)

        def refresh_list():
            list_view.controls.clear()
            mods = self._scan_mods(mods_dir)
            if not mods:
                list_view.controls.append(ft.Text("No mods found in this folder.", color=col("WHITE70", "#DDDDDD")))
            else:
                for m in mods:
                    name_text = ft.Text(m["name"], color=ACCENT_TEXT if m["enabled"] else col("WHITE70", "#DDDDDD"))

                    def make_toggle(path, name_label):
                        def _on_change(ev):
                            try:
                                new_path = self._rename_mod(path, ev.control.value)
                                refresh_list()
                                self.page.update()
                            except Exception as ex:
                                self._show_error_dialog(f"Failed to toggle '{os.path.basename(path)}': {ex}")
                        return _on_change

                    switch = ft.Switch(value=m["enabled"], on_change=make_toggle(m["path"], name_text))
                    # Move filename slightly to the right of the switch
                    row = ft.Row(
                        [
                            switch,
                            ft.Container(content=name_text, padding=ft.padding.only(left=12)),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=8,
                    )
                    list_view.controls.append(row)
            self.page.update()

        def open_folder(_):
            try:
                os.startfile(mods_dir)
            except Exception:
                pass

        def open_curseforge(_):
            try:
                import webbrowser
                webbrowser.open("https://www.curseforge.com/minecraft-dungeons")
            except Exception:
                pass

        def open_nexus(_):
            try:
                import webbrowser
                webbrowser.open("https://www.nexusmods.com/minecraftdungeons/mods")
            except Exception:
                pass

        refresh_btn = ft.TextButton("Refresh", on_click=lambda _: refresh_list(), style=ft.ButtonStyle(color=ACCENT))
        open_btn = ft.TextButton("Open Folder", on_click=open_folder, style=ft.ButtonStyle(color=ACCENT))
        curse_btn = ft.TextButton("Browse CurseForge", on_click=open_curseforge, style=ft.ButtonStyle(color=ACCENT))
        nexus_btn = ft.TextButton("Browse NexusMods", on_click=open_nexus, style=ft.ButtonStyle(color=ACCENT))

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Mod Manager"),
            content=ft.Container(width=520, height=320, content=list_view),
            actions=[curse_btn, nexus_btn, open_btn, refresh_btn, ft.TextButton("Close", on_click=lambda _: self.page.close(dlg), style=ft.ButtonStyle(color=ACCENT))],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        refresh_list()
        self.page.open(dlg)

    def _scan_mods(self, mods_dir: str):
        """Return a list of mods with enabled state. Considers *.pak and *.pak.disabled files."""
        items = []
        try:
            for entry in os.listdir(mods_dir):
                full = os.path.join(mods_dir, entry)
                if not os.path.isfile(full):
                    continue
                low = entry.lower()
                if low.endswith(".pak"):
                    items.append({"path": full, "name": entry, "enabled": True})
                elif low.endswith(".pak.disabled") or low.endswith(".disabled"):
                    # Normalize name display without .disabled suffix
                    base = entry[:-9] if low.endswith(".disabled") else entry
                    items.append({"path": full, "name": base, "enabled": False})
        except Exception:
            pass
        # Sort by name
        items.sort(key=lambda x: x["name"].lower())
        return items

    def _rename_mod(self, path: str, enable: bool) -> str:
        """Enable/disable a mod by renaming extension. Returns new path."""
        folder = os.path.dirname(path)
        name = os.path.basename(path)
        low = name.lower()
        if enable:
            # Remove .disabled suffix if present
            if low.endswith(".disabled"):
                new_name = name[: -len(".disabled")]
            else:
                new_name = name
            # Ensure endswith .pak
            if not new_name.lower().endswith(".pak"):
                # If original was something else.disabled, convert to .pak
                root, _ext = os.path.splitext(new_name)
                new_name = root + ".pak"
        else:
            # Append .disabled if not already
            if not low.endswith(".disabled"):
                new_name = name + ".disabled"
            else:
                new_name = name

        src = path
        dest = os.path.join(folder, new_name)
        if os.path.abspath(src) == os.path.abspath(dest):
            return src
        dest = self._unique_dest_path(dest)
        os.replace(src, dest)
        return dest

    def _unique_dest_path(self, dest: str) -> str:
        """If dest exists, add numeric suffix before extension to avoid overwrite."""
        if not os.path.exists(dest):
            return dest
        base = os.path.basename(dest)
        folder = os.path.dirname(dest)
        stem, ext = os.path.splitext(base)
        i = 1
        while True:
            candidate = os.path.join(folder, f"{stem}.{i}{ext}")
            if not os.path.exists(candidate):
                return candidate
            i += 1

    def _check_updates_ui(self, e):
        """Check for updates and show result in a dialog; fallback to running the script if module import failed."""
        if updater is None:
            run_script("update_app.pyw")
            return
        try:
            result = updater.check_for_updates_result()
            if result.status == 'update_available':
                def open_release(_):
                    try:
                        import webbrowser
                        if result.release_url:
                            webbrowser.open(result.release_url)
                    finally:
                        self.page.close(dlg)
                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Update Available"),
                    content=ft.Text(result.message or "A new version is available."),
                    actions=[
                        ft.TextButton("Open Releases", on_click=open_release, style=ft.ButtonStyle(color=ACCENT)),
                        ft.TextButton("Close", on_click=lambda _: self.page.close(dlg), style=ft.ButtonStyle(color=ACCENT)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                self.page.open(dlg)
            elif result.status == 'up_to_date':
                self._show_info_dialog("No Updates Available", result.message or "You are already using the latest version.")
            else:
                self._show_error_dialog(result.message or "Unable to check for updates.")
        except Exception as ex:
            self._show_error_dialog(f"Update check failed: {ex}")

    def _toggle_online(self, e):
        """Handles the online/offline toggle."""
        # This can be used for future logic if needed
        pass

    def _show_settings(self, e):
        """Switches to the settings view."""
        self.view_fader.content = self.settings_view
        self.page.update()

    def _show_main(self, e):
        """Switches back to the main view."""
        self.view_fader.content = self.main_view
        self.page.update()

    def _save_and_close_settings(self, e):
        """Saves settings and returns to the main view."""
        self.game_path = self.game_path_field.value
        self.player_name = self.player_name_field.value
        self.mods_folder = self.mods_folder_field.value

        save_game_path(self.game_path)
        self.settings["player_name"] = self.player_name
        self.settings[MODS_PATH_KEY] = self.mods_folder
        save_settings(self.settings)
        update_rune_ini(self.player_name)

        self._show_main(e)

    def _show_faq(self, e):
        """Displays the FAQ dialog."""
        try:
            with open(INFOS_FILE, "r", encoding="utf-8") as f:
                faq_content = f.read()
        except IOError:
            faq_content = "FAQ file (infos.txt) not found."

        faq_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("FAQ"),
            content=ft.Text(faq_content, selectable=True),
            actions=[ft.TextButton("Close", on_click=lambda _: self.page.close(faq_dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(faq_dialog)

    def _show_error_dialog(self, message):
        """Displays an error dialog."""
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda _: self.page.close(error_dialog), style=ft.ButtonStyle(color=ACCENT))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(error_dialog)

    def _show_info_dialog(self, title: str, message: str):
        info_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda _: self.page.close(info_dialog), style=ft.ButtonStyle(color=ACCENT))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(info_dialog)

def main(page: ft.Page):
    page.title = "Minecraft Dungeons Launcher"
    page.window_width = 1280
    page.window_height = 720
    page.window_resizable = False
    # Avoid colors API differences across Flet versions
    page.bgcolor = None
    page.fonts = {"Segoe UI": "assets/SegoeUI.ttf"}
    page.padding = 0
    page.window_frameless = True
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    
    launcher = MinecraftDungeonsLauncher(page)
    # Add the built UI control instead of the class itself (not a Flet Control)
    page.add(launcher.build())
    page.update()
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
