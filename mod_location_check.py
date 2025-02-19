import os
import subprocess

def check_and_open_directory():
    user_home = os.path.expanduser("~")
    path = os.path.join(user_home, "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Content", "Paks")
    
    if os.path.exists(path):
        print(f"Directory exists: {path}")
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        print("Files found:", files)
        subprocess.run(["explorer", path], check=True)
    else:
        print("Directory does not exist.")

check_and_open_directory()
