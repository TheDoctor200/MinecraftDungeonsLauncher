import flet as ft
import subprocess
import os
import json

# Path to RUNE.ini
rune_ini_file = "./RUNE.ini"
settings_file = "./settings.json"  # File to store settings

# Load settings from file
def load_settings():
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        # Return default settings if file not found
        return {"app_scale": 1.0}

# Save settings to file
def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f)

# Update RUNE.ini file with the player's name
def update_rune_ini(player_name):
    if os.path.exists(rune_ini_file):
        with open(rune_ini_file, "r") as f:
            lines = f.readlines()
        # Modify the UserName line in the ini file
        for i, line in enumerate(lines):
            if line.startswith("UserName="):
                lines[i] = f"UserName={player_name}\n"
        # Write the changes back to the RUNE.ini file
        with open(rune_ini_file, "w") as f:
            f.writelines(lines)
    else:
        print(f"Error: {rune_ini_file} not found.")


def main(page: ft.Page):
    # Set the app icon
    page.icon = "assets/favicon.png"  # Set the path to your favicon
    page.bgcolor = "#1C1C1C"  # Dark background for the whole page
    page.window_icon = "assets/favicon.ico"  

    player_name = "TheDoctor" # Variable to store Player Name

    # Load settings
    settings = load_settings()
    page.scale = settings.get("app_scale", 1.0)
    
    # Function to run update_app.py
    def run_update_app():
        try:
            subprocess.run(["python", "update_app.pyw"], check=True)
            print("Update script ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running update_app.pyw: {e}")

    # Function to show settings page
    def show_settings(e):
        # Text field for player name
        name_input = ft.TextField(
            value=player_name,  # Default player name
            label="Player Name",
            width=300,
            border_radius=ft.border_radius.all(5), # Rounded corners for input field
            border_color="#424242", # Dark grey border
            focused_border_color="#FF5722", # Accent color when focused
            content_padding=10, # Padding around the input text
        )

        # Save settings and return to the main app
        def close_settings_and_save(e):
            global player_name
            player_name = name_input.value  # Update the global player name
            update_rune_ini(player_name)  # Update the INI file
            page.controls[0] = main_view()  # Go back to the main view
            page.update()

        # Settings page content
        settings_content = ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Settings",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                    ft.Text(
                        "Enter your player name:", size=16, color="#E0E0E0"
                    ),
                    name_input,
                    ft.ElevatedButton(
                        "Update App",
                        on_click=lambda e: run_update_app(),
                        bgcolor="#FF5722",
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5), # Rounded corners for button
                            padding=ft.padding.symmetric(horizontal=20, vertical=10) 
                        )
                    ),
                    ft.ElevatedButton(
                        "Save & Close",
                        on_click=close_settings_and_save,
                        bgcolor="#4CAF50",
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5), # Rounded corners for button
                            padding=ft.padding.symmetric(horizontal=20, vertical=10)
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor="#3E3E3E",
            padding=30,
            border_radius=15,
            expand=True,
        )
        page.controls.clear()
        page.add(settings_content)  # Add settings content to the page
        page.update()

    # Main view layout
    def main_view():
        # Sidebar content with a dark background, rounded corners, and a subtle shadow
        sidebar = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Image(
                                src="./assets/Glow_Squidy.gif",
                                width=50,
                                height=50,
                            ),
                            ft.Text(
                                player_name,  # Use the updated player name
                                size=20,
                                color="#E0E0E0",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(color="#424242"),  # Dark grey divider
                    ft.Text(
                        "MCD Launch Options:",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#E0E0E0",
                    ),
                    ft.TextButton(
                        "Offline Play",
                        on_click=lambda e: run_dll_hooker(),
                        style=ft.ButtonStyle(
                            color="#E0E0E0",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor="#4CAF50",  # Green button
                        ),
                    ),
                    ft.TextButton(
                        "Open Character location",
                        on_click=lambda e: run_charachter_loc(),
                        style=ft.ButtonStyle(
                            color="#E0E0E0",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor="#2196F3",  # Blue button
                        ),
                    ),
                    ft.TextButton(
                        "Open Mods location",
                        on_click=lambda e: run_mods_loc(),
                        style=ft.ButtonStyle(
                            color="#E0E0E0",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor="#2196F3",  # Blue button
                        ),
                    ),                   
                    ft.TextButton(
                        "FAQ",
                        on_click=show_readme,
                        style=ft.ButtonStyle(
                            color="#E0E0E0",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor="#FF9800",  # Orange button
                        ),
                    ),
                    ft.Divider(color="#424242"),  # Dark grey divider
                    ft.TextButton(
                        "Settings",
                        on_click=show_settings,
                        style=ft.ButtonStyle(
                            color="#E0E0E0",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor="#9E9E9E",  # Grey button
                        ),
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.Image(
                                src="./assets/favicon.png", width=40, height=40
                            ),
                            ft.Text("Version 1.3", size=16, color="#E0E0E0", weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
            ),
            bgcolor="#000000",
            padding=15,
            border_radius=15,
            width=220,
            # Add a subtle shadow to the sidebar
            shadow=ft.BoxShadow(
                color=ft.Colors.BLACK,
                blur_radius=10,
                offset=ft.Offset(5, 5),
            ),
        )

        # Main content area with background image and subtle shadow
        main_content = ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Minecraft Dungeons Launcher",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                    ft.Image(
                        src="assets/DungeonsBG.gif",
                        width=600,
                        height=400,
                        border_radius=15,
                        fit=ft.ImageFit.COVER, # Make sure the image covers the entire area
                    ),
                    ft.Text(
                        "An all-new action-adventure game, inspired by classic dungeon crawlers, now available on PC, Nintendo, Xbox Gamepass and on Steam.",
                        size=16,
                        color="#E0E0E0",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton(
                        "PLAY ONLINE",
                        on_click=lambda e: run_dll_unhooker(),
                        bgcolor="#FF5722",
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.symmetric(
                                horizontal=20, vertical=10
                            ),
                        ),
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#3E3E3E",
            padding=30,
            border_radius=15,
            # Add a subtle shadow to the main content
            shadow=ft.BoxShadow(
                color=ft.Colors.BLACK,
                blur_radius=10,
                offset=ft.Offset(5, 5),
            ),
        )

        # Return the main view with sidebar and main content
        return ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1, color="#757575"),
                main_content,
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )

    # Function to run dll_hooker.py
    def run_dll_hooker():
        try:
            subprocess.run(["python", "dll_hooker.pyw"], check=True)
            print("dll_hooker.pyw ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running dll_hooker.pyw: {e}")

    # Function to run character_location_check.py
    def run_charachter_loc():
        try:
            subprocess.run(["python", "character_location_check.pyw"], check=True)
            print("character_location_check.pyw ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running character_location_check.pyw: {e}")

    # Function to run mod_location_check.py
    def run_mods_loc():
        try:
            subprocess.run(["python", "mod_location_check.pyw"], check=True)
            print("mod_location_check.pyw ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running mod_location_check.pyw: {e}")

    # Function to run dll_unhooker.py
    def run_dll_unhooker():
        try:
            subprocess.run(["python", "dll_unhooker.pyw"], check=True)
            print("dll_unhooker.pyw ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running dll_unhooker.pyw: {e}")
    
     # Function to display README.md in a transparent window
    def show_readme(e):
        try:
            with open("infos.txt", "r") as f:
                readme_content = f.read()

            dialog = ft.AlertDialog(
                title=ft.Text("Infos", size=24),
                content=ft.Text(readme_content),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog(dialog))
                ],
                modal=True,
                shape=ft.RoundedRectangleBorder(radius=10),
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        except Exception as e:
            print(f"Error opening README.md: {e}")

    # Helper function to close the dialog
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # Set the main view when the app starts
    page.add(main_view())

# Run the app
ft.app(target=main, assets_dir="assets")
