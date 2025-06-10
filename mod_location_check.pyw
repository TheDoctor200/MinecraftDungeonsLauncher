import os
import subprocess
import json

def check_and_open_directory():
    default_path = r"C:\Users\m_web\AppData\Local\Mojang\products\dungeons\dungeons\Dungeons\Content\Paks"
    path = default_path
    if os.path.exists(path) and os.path.isdir(path):
        try:
            subprocess.Popen(["explorer", path], shell=False)
        except Exception as ex:
            print(f"Failed to open directory: {ex}")
    else:
        # Try to get path from game_path.json
        try:
            with open("game_path.json", "r") as f:
                data = json.load(f)
                exe_path = data.get("game_path", "")
                if exe_path:
                    # Try to get the directory of the exe and open its parent Content\Paks if possible
                    exe_dir = os.path.dirname(exe_path)
                    # Try to find Content\Paks relative to exe_dir
                    candidate = os.path.join(exe_dir, "Content", "Paks")
                    if os.path.exists(candidate) and os.path.isdir(candidate):
                        subprocess.Popen(["explorer", candidate], shell=False)
                        return
                    # Otherwise, just open the exe directory
                    subprocess.Popen(["explorer", exe_dir], shell=False)
                else:
                    print("No game_path found in game_path.json")
        except Exception as ex:
            print(f"Directory does not exist: {path} and failed to use game_path.json: {ex}")

def main():
    check_and_open_directory()

if __name__ == "__main__":
    main()

