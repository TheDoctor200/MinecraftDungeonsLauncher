import os
import subprocess

# Get the current user's home directory
user_home = os.path.expanduser("~")

# Construct the expected path
game_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons",
                         "dungeons", "Dungeons", "Binaries", "Win64")

# The executable file
exe_file = "Dungeons-Win64-Shipping.exe"
exe_path = os.path.join(game_path, exe_file)

# Check if the file exists and run it
if os.path.isfile(exe_path):
    print(f"Starting {exe_file}...")
    subprocess.Popen(exe_path, shell=True)
else:
    print(f"Error: {exe_file} not found in {game_path}")
