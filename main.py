import flet as ft
import subprocess
import os

# Path to RUNE.ini
rune_ini_file = "./RUNE.ini"  # Path to RUNE.ini in the app's folder

def main(page: ft.Page):
    page.bgcolor = "#2E2E2E"  # Dark grey background for the whole page

    # Function to run update_app.py
    def run_update_app():
        try:
            subprocess.run(["python", "update_app.py"], check=True)
            print("Update script ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running update_app.py: {e}")

    # Update RUNE.ini file with the player's name
    def update_rune_ini(player_name):
        if os.path.exists(rune_ini_file):
            with open(rune_ini_file, "r") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith("UserName="):
                    lines[i] = f"UserName={player_name}\n"
            with open(rune_ini_file, "w") as f:
                f.writelines(lines)
            print(f"Updated RUNE.ini with new player name: {player_name}")
        else:
            print(f"Error: {rune_ini_file} not found.")

    # Function to show settings page
    def show_settings(e):
        # Text field for player name
        name_input = ft.TextField(
            label="Player Name",
            width=300,
            bgcolor="#FFFFFF"  # White background for input field
        )

        # Save and update the player name in RUNE.ini
        def save_player_name():
            player_name = name_input.value
            update_rune_ini(player_name)  # Update RUNE.ini with the player name
            page.go("/")  # Return to main launcher page
            page.update()

        # Settings page content
        settings_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text("Enter your player name:", size=16, color="#E0E0E0"),
                    name_input,
                    ft.ElevatedButton(
                        "Update App",
                        on_click=run_update_app,
                        bgcolor="#FF5722",
                        color="#FFFFFF"
                    ),
                    ft.ElevatedButton(
                        "Save & Close",
                        on_click=save_player_name,
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
        page.views.clear()
        page.views.append(ft.View("/settings", [settings_content]))
        page.update()

    # Main view layout
    def main_view():
        sidebar = ft.Container(
            ft.Column(
                [
                    ft.Text("Minecraft Dungeons Launcher", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.TextButton("Einstellungen", on_click=show_settings,
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#9E9E9E"
                                  )),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            bgcolor="#000000",  # Black background for sidebar
            padding=15,
            border_radius=15,
            width=220,  # Define width for better layout
        )

        main_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Welcome to Minecraft Dungeons!", size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.ElevatedButton("PLAY",
                                      on_click=lambda e: print("Play clicked"),
                                      bgcolor="#FF5722",
                                      color="#FFFFFF")
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            expand=True  # Make the main content area expand to fill the rest of the space
        )

        return ft.Row(
            [
                sidebar,
                main_content,
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True  # Ensure the row expands to the full page width
        )

    # Set the initial page view
    page.views.append(ft.View("/", [main_view()]))
    page.update()

# Running the app with the assets folder
ft.app(target=main, assets_dir="assets")































    







