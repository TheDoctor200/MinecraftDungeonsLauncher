import os
import subprocess
import json

def check_and_open_directory():
    # Only open the mods folder specified in settings.json
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            mods_folder = data.get("mods_folder", "")
    except Exception:
        mods_folder = ""

    if mods_folder and os.path.isdir(mods_folder):
        try:
            subprocess.Popen(["explorer", mods_folder], shell=False)
            return
        except Exception as ex:
            print(f"Failed to open directory: {ex}")
    else:
        print("No valid mods folder set in settings.json. Trying fallback.")

    # Fallback to previously hardcoded default
    targets = [r"C:\Users\m_web\AppData\Local\Mojang\products\dungeons\dungeons\Dungeons\Content\Paks"]

    for path in targets:
        if path and os.path.exists(path) and os.path.isdir(path):
            try:
                subprocess.Popen(["explorer", path], shell=False)
                return
            except Exception as ex:
                print(f"Failed to open directory: {ex}")
    print("No valid directory found to open.")

def main():
    check_and_open_directory()

if __name__ == "__main__":
    main()

