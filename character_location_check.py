import os
import subprocess

def check_and_open_directory():
    user_home = os.path.expanduser("~")
    path = os.path.join(user_home, "Saved Games", "Mojang Studios", "Dungeons")
    
    if os.path.exists(path):
        print(f"Directory exists: {path}")
        usernames = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        print("Usernames found:", usernames)
        subprocess.run(["explorer", path], check=True)
    else:
        print("Directory does not exist.")

check_and_open_directory()
