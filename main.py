import flet as ft
import subprocess
import os

# Path to RUNE.ini
rune_ini_file = "./RUNE.ini"

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
    page.bgcolor = "#2E2E2E"  # Dark grey background for the whole page

    # Function to run update_app.py
    def run_update_app():
        try:
            subprocess.run(["python", "update_app.py"], check=True)
            print("Update script ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running update_app.py: {e}")

    # Function to run the game exe
    def start_game(e):
        try:
            exe_path = os.path.expandvars(r"%LOCALAPPDATA%\Mojang\products\dungeons\dungeons\Dungeons.exe")
            subprocess.Popen(exe_path)
        except Exception as e:
            print(f"Error starting the game: {e}")

    # Function to run dll_hooker.py
    def run_dll_hooker():
        try:
            subprocess.run(["python", "dll_hooker.py"], check=True)
            print("dll_hooker.py ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running dll_hooker.py: {e}")

    # Function to run dll_unhooker.py
    def run_dll_unhooker():
        try:
            subprocess.run(["python", "dll_unhooker.py"], check=True)
            print("dll_unhooker.py ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running dll_unhooker.py: {e}")

    # Function to show settings page
    def show_settings(e):
        # Text field for player name
        name_input = ft.TextField(
            value="TheDoctor",  # Default player name
            label="Player Name",
            on_change=lambda event: update_player_name(event.control.value),  # Accessing the value correctly
            width=300
        )

        # Update player name in settings
        def update_player_name(value):
            # Update RUNE.ini immediately when the user types
            update_rune_ini(value)

        # Save settings and close the app
        def close_settings_and_save():
            page.window_close()  # Close the entire app

        # Settings page content
        settings_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text("Enter your player name:", size=16, color="#E0E0E0"),
                    name_input,
                    ft.ElevatedButton(
                        "Update App",
                        on_click=lambda e: run_update_app(),
                        bgcolor="#FF5722",
                        color="#FFFFFF"
                    ),
                    ft.ElevatedButton(
                        "Save & Close",
                        on_click=lambda e: close_settings_and_save(),
                        bgcolor="#4CAF50",
                        color="#FFFFFF"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor="#3E3E3E",  # Dark grey background
            padding=30,
            border_radius=15,  # Rounded corners
            expand=True  # Expand to fill the page
        )

        # Navigate to the settings page
        page.go("/settings")
        # Clear existing page content and add the settings content
        page.views.clear()
        page.views.append(ft.View("/", [main_view()]))
        page.views.append(ft.View("/settings", [settings_content]))
        page.update()

    # Function to display README.md in a transparent window
    def show_readme(e):
        try:
            with open("infos.txt", "r") as f:
                readme_content = f.read()

            dialog = ft.AlertDialog(
                title=ft.Text("Infos", size=24),
                content=ft.Text(readme_content),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog(dialog))  # Call close_dialog
                ],
                modal=True,
                shape=ft.RoundedRectangleBorder(radius=10),
            )

            page.dialog = dialog  # Set the dialog to the page dialog
            dialog.open = True  # Open the dialog
            page.update()  # Update the page to reflect changes

        except Exception as e:
            print(f"Error opening README.md: {e}")

    # Helper function to close the dialog
    def close_dialog(dialog):
        dialog.open = False  # Set the open property to False to close the dialog
        page.update()  # Update the page to reflect the changes

    # Main view layout
    def main_view():
        # Sidebar content with black background and rounded corners
        sidebar = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Image(src="./assets/Glow_Squidy.gif", width=50, height=50),  # User image
                            ft.Text("TheDoctor", size=20, color="#E0E0E0", weight=ft.FontWeight.BOLD)  # Default Player's name
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Divider(color="#424242"),  # Divider in dark grey for contrast
                    ft.Text("Minecraft Dungeons", size=24, weight=ft.FontWeight.BOLD, color="#E0E0E0"),  # Title
                    ft.TextButton("Start Game", on_click=start_game,  # Launch Dungeons.exe
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#00BCD4"  # Cyan button
                                  )),
                    ft.TextButton("Offline Play", on_click=lambda e: run_dll_hooker(),  # Launch dll_hooker.py
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",  # Light grey text
                                      shape=ft.RoundedRectangleBorder(radius=8),  # Rounded corners
                                      bgcolor="#4CAF50"  # Green button
                                  )),
                    ft.TextButton("Beta", on_click=lambda e: print("Beta clicked"),
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#2196F3"  # Blue button
                                  )),
                    ft.TextButton("FAQ", on_click=show_readme,  # Show README in a new dialog
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#FF9800"  # Orange button
                                  )),
                    ft.Divider(color="#424242"),  # Divider in dark grey for contrast
                    ft.TextButton("Settings", on_click=show_settings,  # Show settings page
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#9E9E9E"  # Grey button
                                  )),
                    ft.Container(expand=True),  # Push the version info to the bottom
                    ft.Row(  # App version and image at the bottom-left of the sidebar
                        [
                            ft.Image(src="./assets/favicon.png", width=40, height=40),  # Version icon
                            ft.Text("Version 1.25", size=16, color="#E0E0E0"),  # Version text
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True  # Ensure that the sidebar takes full vertical space
            ),
            bgcolor="#000000",  # Black background for sidebar
            padding=15,
            border_radius=15,  # Rounded corners for the sidebar
            width=220,  # Define width for better layout
        )

        # Main content area with background image
        main_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Minecraft Dungeons Launcher", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),  # Title
                    ft.Image(src="assets/DungeonsBG.gif", width=600, height=400, border_radius=15),  # GIF Background
                    ft.Text(
                        "An all-new action-adventure game, inspired by classic dungeon crawlers, now available on PC, Nintendo, Xbox Gamepass and on Steam.",
                        size=16,
                        color="#E0E0E0",  # Description
                        text_align=ft.TextAlign.CENTER  # Centered text
                    ),
                    ft.ElevatedButton("PLAY ONLINE",  # Play button
                                      on_click=lambda e: run_dll_unhooker(),  # Launch dll_unhooker.py
                                      bgcolor="#FF5722",  # Dark orange button
                                      color="#FFFFFF",  # White text
                                      style=ft.ButtonStyle(
                                          shape=ft.RoundedRectangleBorder(radius=10),  # Rounded button
                                          padding=ft.padding.symmetric(horizontal=20, vertical=10)  # Add padding to the button
                                      )
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#3E3E3E",  # Dark grey background for the content area
            padding=30,
            border_radius=15,  # Rounded corners for the content container
        )

        # Return the main view with sidebar and main content
        return ft.Row(
            [
                sidebar,  # Sidebar
                ft.VerticalDivider(width=1, color="#757575"),  # Grey divider
                main_content,  # Main content
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True  # Ensure the row expands to the full page width
        )

    # Set the main view when the app starts
    page.views.append(ft.View("/", [main_view()]))  # Main view with sidebar and content
    page.update()

# Run the app
ft.app(target=main, assets_dir="assets")
















































    







