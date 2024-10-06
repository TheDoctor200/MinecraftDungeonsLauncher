import flet as ft
import subprocess
import json
import os

# Path to settings file
settings_file = "settings.js"

# Load settings from file
def load_settings():
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            # If file is empty or invalid JSON, return default settings
            print("Invalid settings file. Loading default settings.")
            return {"window_width": 800, "window_height": 600}
    else:
        # If file does not exist, return default settings
        return {"window_width": 800, "window_height": 600}

# Save settings to file
def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f)

def main(page: ft.Page):
    # Load initial settings
    settings = load_settings()

    # Update window size based on settings
    page.window_width = settings["window_width"]
    page.window_height = settings["window_height"]
    page.bgcolor = "#2E2E2E"  # Dark grey background for the whole page

    # Function to run update_app.py
    def run_update_app():
        try:
            subprocess.run(["python", "update_app.py"], check=True)
            print("Update script ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running update_app.py: {e}")

    # Function to show settings page
    def show_settings(e):
        # Sliders for window width and height
        width_slider = ft.Slider(
            value=settings["window_width"],
            min=600,
            max=1200,
            label="Width: {value}",
            on_change=lambda event: update_width(event.value)
        )
        height_slider = ft.Slider(
            value=settings["window_height"],
            min=400,
            max=800,
            label="Height: {value}",
            on_change=lambda event: update_height(event.value)
        )

        # Update window width in settings
        def update_width(value):
            settings["window_width"] = value
            page.update()

        # Update window height in settings
        def update_height(value):
            settings["window_height"] = value
            page.update()

        # Save settings and close settings page
        def close_settings_and_save():
            save_settings(settings)  # Save settings to file
            page.go("/")  # Return to main launcher page
            page.window_width = settings["window_width"]
            page.window_height = settings["window_height"]
            page.update()

        # Settings page content
        settings_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text("Adjust app window size:", size=16, color="#E0E0E0"),
                    width_slider,
                    height_slider,
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

    # Main view layout
    def main_view():
        # Sidebar content with black background and rounded corners
        sidebar = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Image(src="./assets/Glow_Squidy.gif", width=50, height=50),  # Replace with user image
                            ft.Text("TheDoctor", size=20, color="#E0E0E0", weight=ft.FontWeight.BOLD)  # Lighter grey for the username
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

        # Main content area with background image and rounded corners
        main_content = ft.Container(
            ft.Column(
                [
                    ft.Text("Minecraft Dungeons Launcher", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),  # Orange title
                    ft.Container(
                        ft.Column(
                            [
                                ft.Image(src="assets/DungeonsBG.png", width=600, height=400, border_radius=15),  # Background image with rounded corners
                                ft.Text(
                                    "An all-new action-adventure game, inspired by classic dungeon crawlers, coming to PC, Nintendo Switch, PlayStation 4, Xbox One, and Xbox Game Pass May 26.",
                                    size=16,
                                    color="#E0E0E0",  # Lighter grey for the description
                                    text_align=ft.TextAlign.CENTER  # Centered text
                                ),
                                ft.ElevatedButton("PLAY",  # Changed from "PRE-ORDER" to "PLAY"
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

    # Set the initial page view
    page.views.append(ft.View("/", [main_view()]))
    page.update()

# Running the app with the assets folder
ft.app(target=main, assets_dir="assets")





















    







