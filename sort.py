import os
import shutil
import zipfile

def normalize(filename):
    return filename

def process_folder(folder_path):
    categories = ['images', 'documents', 'audio', 'video', 'archives', 'other']

    for category in categories:
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True)

    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path) and item.lower() in categories:
            continue

        if item.lower().endswith('.zip'):
            try:
                with zipfile.ZipFile(item_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(folder_path, 'archives', os.path.splitext(item)[0]))
                os.remove(item_path)
            except zipfile.BadZipFile:
                os.remove(item_path)
            continue

        _, extension = os.path.splitext(item)

        new_name = normalize(item)

        if extension[1:].lower() in ['jpeg', 'png', 'jpg', 'svg']:
            shutil.move(item_path, os.path.join(folder_path, 'images', new_name))
        elif extension[1:].lower() in ['avi', 'mp4', 'mov', 'mkv']:
            shutil.move(item_path, os.path.join(folder_path, 'video', new_name))
        elif extension[1:].lower() in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
            shutil.move(item_path, os.path.join(folder_path, 'documents', new_name))
        elif extension[1:].lower() in ['mp3', 'ogg', 'wav', 'amr']:
            shutil.move(item_path, os.path.join(folder_path, 'audio', new_name))
        elif extension[1:].lower() in ['zip', 'gz', 'tar']:
            pass
        else:
            shutil.move(item_path, os.path.join(folder_path, 'other', new_name))

def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        sys.exit(1)

    process_folder(folder_path)
    print("Sorting completed.")

if __name__ == "__main__":
    main()
