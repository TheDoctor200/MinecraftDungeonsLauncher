import os
import sys
import json
import ctypes
import subprocess
import time
import stat

CANDIDATE_EXE_NAMES = ("Dungeons-Win64-Shipping.exe", "Dungeons.exe")

def hide_console():
    if sys.platform == "win32":
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

def default_win64_dir():
    # C:\Users\<user>\AppData\Local\Mojang\products\dungeons\dungeons\Dungeons\Binaries\Win64
    user_home = os.path.expanduser("~")
    return os.path.join(
        user_home,
        "AppData", "Local", "Mojang", "products", "dungeons", "dungeons", "Dungeons", "Binaries", "Win64"
    )

def load_game_path():
    try:
        with open("game_path.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("game_path", "") or ""
    except Exception:
        return ""

def first_matching_exe(folder: str):
    try:
        for name in CANDIDATE_EXE_NAMES:
            p = os.path.join(folder, name)
            if os.path.isfile(p):
                return name
        # Fallback: any exe with 'dungeons' in name
        for name in os.listdir(folder):
            if name.lower().endswith(".exe") and "dungeons" in name.lower():
                return name
    except Exception:
        pass
    return None

def resolve_from_custom(custom_path: str):
    if not custom_path:
        return None, None
    p = os.path.expandvars(os.path.expanduser(custom_path))
    # If user provided the exe directly
    if os.path.isfile(p) and p.lower().endswith(".exe"):
        return os.path.dirname(p), os.path.basename(p)
    # If user provided a folder, try common subfolders
    if os.path.isdir(p):
        candidates = [
            p,
            os.path.join(p, "Dungeons", "Binaries", "Win64"),
            os.path.join(p, "Binaries", "Win64"),
            os.path.join(p, "Win64"),
            os.path.join(p, "Dungeons"),
        ]
        for folder in candidates:
            exe = first_matching_exe(folder)
            if exe:
                return folder, exe
        # Last resort: recursive search (bounded)
        for root, _dirs, files in os.walk(p):
            for name in files:
                if name.lower().endswith(".exe") and ("dungeons" in name.lower() or name in CANDIDATE_EXE_NAMES):
                    return root, name
    return None, None

def resolve_install_dir_and_exe():
    # 1) Default path for current user
    win64 = default_win64_dir()
    if os.path.isdir(win64):
        exe = first_matching_exe(win64)
        if exe:
            return win64, exe
    # 2) From game_path.json (file or folder)
    custom = load_game_path()
    folder, exe = resolve_from_custom(custom)
    if folder and exe:
        return folder, exe
    return None, None

def force_delete_file(path: str):
    """Force delete without admin by clearing attributes, trying os.remove, cmd del /f, rename+delete, schedule on reboot."""
    if not os.path.exists(path):
        return

    FILE_ATTRIBUTE_NORMAL = 0x80

    def clear_attrs(p: str):
        try:
            ctypes.windll.kernel32.SetFileAttributesW(ctypes.c_wchar_p(p), FILE_ATTRIBUTE_NORMAL)
        except Exception:
            try:
                subprocess.run(["cmd", "/c", f'attrib -r -s -h "{p}"'], check=False, capture_output=True)
            except Exception:
                pass
        try:
            os.chmod(p, stat.S_IWRITE | stat.S_IREAD)
        except Exception:
            pass

    def cmd_force_del(p: str) -> bool:
        try:
            subprocess.run(["cmd", "/c", f'del /f /q "{p}"'], check=False, capture_output=True)
            return not os.path.exists(p)
        except Exception:
            return False

    def schedule_delete_on_reboot(p: str):
        try:
            MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004
            ctypes.windll.kernel32.MoveFileExW(ctypes.c_wchar_p(p), None, MOVEFILE_DELAY_UNTIL_REBOOT)
        except Exception:
            pass

    # Try direct delete
    try:
        clear_attrs(path)
        os.remove(path)
        return
    except Exception:
        pass

    # Try command forced delete
    if cmd_force_del(path):
        return

    # Retry with rename fallback
    for i in range(6):
        try:
            time.sleep(0.2)
            if not os.path.exists(path):
                return
            clear_attrs(path)
            if cmd_force_del(path):
                return
            # rename then delete
            tmp = f"{path}.delete.{os.getpid()}.{i}"
            try:
                os.replace(path, tmp)
                clear_attrs(tmp)
                try:
                    os.remove(tmp)
                    return
                except Exception:
                    if cmd_force_del(tmp):
                        return
                    schedule_delete_on_reboot(tmp)
                    return
            except Exception:
                continue
        except Exception:
            continue

    # Final fallback
    if os.path.exists(path):
        schedule_delete_on_reboot(path)

def unhook_and_launch():
    folder, exe = resolve_install_dir_and_exe()
    if not folder or not exe:
        print("Error: Could not resolve game folder or executable.")
        return
    # Remove winmm.dll if present
    winmm_path = os.path.join(folder, "winmm.dll")
    force_delete_file(winmm_path)
    # Small delay for filesystem settle
    time.sleep(0.25)
    # Launch game
    exe_path = os.path.join(folder, exe)
    if os.path.isfile(exe_path):
        try:
            hide_console()
            subprocess.Popen(exe_path, shell=True)
        except Exception as ex:
            print(f"Failed to launch {exe_path}: {ex}")
    else:
        print(f"Executable not found: {exe_path}")

def main():
    hide_console()
    unhook_and_launch()

if __name__ == "__main__":
    main()
