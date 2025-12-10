import os
import shutil
import logging
from datetime import datetime

SOURCE_FOLDER = r"C:\Users\Priyanka\Downloads" 
DRY_RUN = False  
LOG_FILE = "file_organizer.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
def get_destination_folder(extension):
    if not extension:
        return "Others"
    return extension[1:].upper()  # remove dot & uppercase (e.g., "jpg" -> JPG)

def handle_collision(dest_path):
    base, ext = os.path.splitext(dest_path)
    counter = 1

    while os.path.exists(dest_path):
        dest_path = f"{base}({counter}){ext}"
        counter += 1

    return dest_path

def organize_files():
    print("\nStarting File Organizer...\n")

    for filename in os.listdir(SOURCE_FOLDER):
        file_path = os.path.join(SOURCE_FOLDER, filename)

        if os.path.isdir(file_path):
            continue

        _, extension = os.path.splitext(filename)
        folder_name = get_destination_folder(extension)

        dest_folder = os.path.join(SOURCE_FOLDER, folder_name)
        os.makedirs(dest_folder, exist_ok=True)

        dest_path = os.path.join(dest_folder, filename)
        dest_path = handle_collision(dest_path)

        if DRY_RUN:
            print(f"[DRY RUN] Would move: {file_path} -> {dest_path}")
            continue

        shutil.move(file_path, dest_path)
        print(f"Moved: {filename} -> {folder_name}")
        logging.info(f"MOVED: {file_path} -> {dest_path}")

    print("\nFile organization completed!")
    if DRY_RUN:
        print("No files were moved (dry-run mode).")
    print(f"Log saved to: {LOG_FILE}")
	
if __name__ == "__main__":
    organize_files()