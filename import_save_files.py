import os
import shutil

def find_numbered_folder(base_path):
    # Iterate through all entries in the base path
    for entry in os.listdir(base_path):
        entry_path = os.path.join(base_path, entry)

        # Check if entry is a directory and if its name is composed only of digits
        if os.path.isdir(entry_path) and entry.isdigit():
            return entry_path  # Return the first found numbered folder
    return None  # No numbered folder found

def copy_files(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy all files and directories from the source to the destination
    for item in os.listdir(source_folder):
        src_item = os.path.join(source_folder, item)
        dest_item = os.path.join(destination_folder, item)

        if os.path.isdir(src_item):
            shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
        else:
            shutil.copy2(src_item, dest_item)

        print(f"Copied {item} to {destination_folder}")

def main():
    user_home = os.path.expanduser("~")
    source_base_path = os.path.join(user_home, "Saved Games", "Mojang Studios", "Dungeons")
    destination_folder = os.path.join(user_home, "Saved Games", "Mojang Studios", "Dungeons", "2000000000000000")

    # Find the first numbered folder
    source_folder = find_numbered_folder(source_base_path)

    if source_folder:
        print(f"Found source folder: {source_folder}")
        # Copy files from the source folder to the destination folder
        copy_files(source_folder, destination_folder)
    else:
        print("No numbered folder found in the source directory.")

if __name__ == "__main__":
    main()

