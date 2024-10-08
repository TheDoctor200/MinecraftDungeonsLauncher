import flet as ft
import subprocess
import os
import threading
import time

# Path to RUNE.ini
rune_ini_file = "./RUNE.ini"  # Path to RUNE.ini in the app's folder

def main(page: ft.Page):
    page.bgcolor = "#2E2E2E"  # Dark grey background for the whole page

    # Background images list
    background_images = [
        "./assets/DungeonsBG.png",
        "./assets/mvc1minecraft-1635640703.png",  
        "./assets/wp5929735.png",
        "./assets/wp5929830.png"
        "./assets/wp6369300.png"
    ]
    
    current_image_index = 0  # Index to keep track of the current image

    # Function to change the background image
    def change_background_image():
        nonlocal current_image_index
        current_image_index = (current_image_index + 1) % len(background_images)
        background_image.source = background_images[current_image_index]
        page.update()

    # Function to run update_app.py
    def run_update_app(event):
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
        def save_player_name(event):
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
        # Sidebar content with black background and rounded corners
        sidebar = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Image(src="./assets/Glow_Squidy.gif", width=50, height=50),  # Replace with user image
                            ft.Text("Player Name", size=20, color="#E0E0E0", weight=ft.FontWeight.BOLD)  # Placeholder for the player's name
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Divider(color="#424242"),  # Divider in dark grey for contrast
                    ft.Text("Minecraft Dungeons", size=24, weight=ft.FontWeight.BOLD, color="#E0E0E0"),  # Lighter grey for title
                    ft.TextButton("Spielen", on_click=lambda e: print("Spielen clicked"),
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
                    ft.TextButton("FAQ", on_click=lambda e: print("FAQ clicked"),
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#FF9800"  # Orange button
                                  )),
                    ft.Divider(color="#424242"),  # Divider in dark grey for contrast
                    ft.TextButton("Einstellungen", on_click=show_settings,  # Show settings page when clicked
                                  style=ft.ButtonStyle(
                                      color="#E0E0E0",
                                      shape=ft.RoundedRectangleBorder(radius=8),
                                      bgcolor="#9E9E9E"  # Grey button
                                  )),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            bgcolor="#000000",  # Black background for sidebar
            padding=15,
            border_radius=15,  # Rounded corners for the sidebar
            width=220,  # Define width for better layout
        )

        # Background image placeholder
        global background_image  # Declare background_image as global
        background_image = ft.Image(src=background_images[current_image_index], width=600, height=400, border_radius=15)  # Initial background image

        # Main content area with background image and rounded corners
        main_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Minecraft Dungeons Launcher", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Container(
                        ft.Column(
                            [
                                background_image,  # Display the current background image
                                ft.Text(
                                    "An all-new action-adventure game, inspired by classic dungeon crawlers, coming to PC, Nintendo Switch, PlayStation 4, Xbox One, and Xbox Game Pass May 26.",
                                    size=16,
                                    color="#E0E0E0",  # Lighter grey for the description
                                    text_align=ft.TextAlign.CENTER  # Centered text
                                ),
                                ft.ElevatedButton("PLAY",  
                                                  on_click=lambda e: print("Play clicked"),
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
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            expand=True  # Make the main content area expand to fill the rest of the space
        )

        # Return the main view with sidebar and main content
        return ft.Row(
            [
                sidebar,  # Sidebar with rounded corners and improved colors
                ft.VerticalDivider(width=1, color="#757575"),  # Grey divider
                main_content,  # Main content with improved layout and design
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True  # Ensure the row expands to the full page width
        )

    # Function to start background image rotation
    def start_background_rotation():
        while True:
            change_background_image()
            time.sleep(5)  # Change the image every 5 seconds

    # Set the initial page view
    page.views.append(ft.View("/", [main_view()]))
    page.update()

    # Start background rotation in a separate thread
    threading.Thread(target=start_background_rotation, daemon=True).start()

# Running the app with the assets folder
ft.app(target=main, assets_dir="assets")



































    







