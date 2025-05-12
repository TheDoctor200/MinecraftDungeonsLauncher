import os
import subprocess
import json

def load_custom_game_path():
    try:
        with open("game_path.json", "r") as f:
            data = json.load(f)
            return data.get("game_path", "")
    except (FileNotFoundError, json.JSONDecodeError):
        return ""

# Get the current user's home directory
user_home = os.path.expanduser("~")

# Construct the expected path
game_path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons",
                         "dungeons", "Dungeons", "Binaries", "Win64")

# The executable file
exe_file = "Dungeons-Win64-Shipping.exe"
exe_path = os.path.join(game_path, exe_file)

# Check if the file exists and run it, if not try custom path
if os.path.isfile(exe_path):
    print(f"Starting {exe_file}...")
    subprocess.Popen(exe_path, shell=True)
else:
    # Try custom path from json
    custom_path = load_custom_game_path()
    if custom_path and os.path.isfile(os.path.join(custom_path, exe_file)):
        custom_exe_path = os.path.join(custom_path, exe_file)
        print(f"Starting {exe_file} from custom path...")
        subprocess.Popen(custom_exe_path, shell=True)
    else:
        print(f"Error: {exe_file} not found in default or custom path")
