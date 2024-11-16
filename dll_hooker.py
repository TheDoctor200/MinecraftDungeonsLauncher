import os
import shutil
import ctypes

def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def find_game_install_path(game_executable):
    # Get the current user's home directory
    user_home = os.path.expanduser("~")
    # Construct the specific installation path
    specific_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Binaries", "Win64")

    # Check if the game executable exists in the specific path
    game_executable_path = os.path.join(specific_path, game_executable)
    
    if os.path.exists(game_executable_path):
        return specific_path

    return None

def copy_files_to_game_folder(game_folder, files):
    for file in files:
        source_path = os.path.join(os.getcwd(), file)
        destination_path = os.path.join(game_folder, file)
        
        # Copy the file to the game folder
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied {file} to {game_folder}")
        else:
            print(f"{file} not found in the script directory.")

def main():
    hide_console()  # Hide the console window immediately when the script runs
    
    game_executable = "Dungeons-Win64-Shipping.exe"
    
    # Find the installation path of the game
    game_install_path = find_game_install_path(game_executable)

    if game_install_path:
        print(f"Game installation path found: {game_install_path}")

        # List of files to copy
        files_to_copy = ["winmm.dll", "RUNE.ini"]

        # Copy the specified files to the game's installation folder
        copy_files_to_game_folder(game_install_path, files_to_copy)
    else:
        print(f"{game_executable} not found in the specified path.")

if __name__ == "__main__":
    main()
