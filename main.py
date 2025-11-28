import os
import shutil
import datetime
import json



# folder_path = input('Enter the path to the folder you want to organize: ')

# folder_path = folder_path.strip()


# print('organizing folder:', folder_path)

# #getting only the files. no folder
# all_items = os.listdir(folder_path)
# files = [f  for f in all_items if os.path.isfile(os.path.join(folder_path, f))]

# print(f'Found {len(files)} files to process.')

# file_types = {
#     'images': ['.jpg', 'jpeg', '.png', '.gif'],
#     'videos': ['.mp4', '.mkv', '.avi'],
#     'Audio': ['.mp3', '.wav'],
#     'documents': ['.txt', 'docx', '.pdf', '.xlsx'],
#     'archives': ['.zip', '.rar', '.tar', '.7z'],
#     'Installers': ['.exe', '.msi', '.dmg']
# }

# def get_category(file_path):
#     filename = os.path.basename(file_path)#extract just the file name

#     _,ext = os.path.splitext(filename)#split 'filename' and extention
#     ext = ext.lower()

#     for category, extentions in file_types.items():
#         if ext in extentions:
#             return category #thia will run if matches
#     return 'others'#run if nothing matches
    
# for file in files:
#     file_path = os.path.join(folder_path, file)
#     category = get_category(file_path)
    
#     category_folder = os.path.join(folder_path, category)
    
#     #crerate a folder if it dosn't exist
#     if not os.path.exists(category_folder):
#         os.makedirs(category_folder)
#         print(f'created folder: {category_folder}')

#         #move file
#     new_path = os.path.join(category_folder, file)
#     # where to move it to
#     if not os.path.exists(new_path):

#         shutil.move(file_path, new_path)
#     else:
#         print(f'file already exists: {new_path}')
#         print(f'moved: {file} --> {category} ')

    





# This create json for undoing. like unorganize the files after organizing

# --- Define file type categories ---
file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.csv'],
    'codes': ['.py', '.js', '.css', '.html', '.xml', '.c', 'json'],
    'Archives': ['.zip', '.rar', '.tar', '.7z'],
    'Installers': ['.exe', '.msi', '.dmg']
}

# --- Ask user for folder path ---
folder_path = input("Enter the full path to the folder you want to organize:\n").strip()

if not os.path.exists(folder_path):
    print("❌ Error: That folder does not exist.")
    exit()

# --- Setup paths for logging and undo ---
log_file = os.path.join(folder_path, 'organize_log.txt')
undo_file = os.path.join(folder_path, 'undo_map.json')
undo_map = {}

# --- Function to get file category ---
def get_category(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for category, extensions in file_types.items():
        if ext in extensions:
            return category
    return 'Others'

# --- Step 1: List all visible files ---
files = [f for f in os.listdir(folder_path)
         if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith('.') and not f.endswith(('.log', '.json'))]

# --- Step 2: Process files ---
with open(log_file, 'a') as log:
    log.write(f"\n--- Run at {datetime.datetime.now()} ---\n")

    for file in files:
        file_path = os.path.join(folder_path, file)
        category = get_category(file_path)
        category_folder = os.path.join(folder_path, category)

        # Create destination folder if needed
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
            log.write(f"📁 Created: {category_folder}\n")

        new_path = os.path.join(category_folder, file)

        if not os.path.exists(new_path):
            shutil.move(file_path, new_path)
            undo_map[file] = file_path  # Save original location
            log.write(f"✅ Moved: {file} → {category}/\n")
        else:
            log.write(f"⚠️ Skipped (already exists): {file}\n")

# Save undo mapping
with open(undo_file, 'w') as undo_json:
    json.dump(undo_map, undo_json)

print("✅ Organizing complete. Actions logged.")




#=========================== UNDO ==============================

# --- Ask user for the folder where undo_map.json is located ---
folder_path = input("Enter the path to the folder where 'undo_map.json' is stored:\n").strip()
undo_file = os.path.join(folder_path, 'undo_map.json')

if not os.path.isfile(undo_file):
    print("❌ undo_map.json not found at that location.")
    exit()

# --- Load the undo map ---
with open(undo_file, 'r') as f:
    undo_map = json.load(f)

# --- Loop through files and move them back to original location ---
restored_count = 0

for file_name, original_path in undo_map.items():
    # Find the current path (search all subfolders)
    found = False
    for root, _, files in os.walk(folder_path):
        if file_name in files:
            current_path = os.path.join(root, file_name)
            try:
                shutil.move(current_path, original_path)
                print(f"🔁 Restored: {file_name} → {original_path}")
                restored_count += 1
                found = True
                break
            except Exception as e:
                print(f"❌ Error restoring {file_name}: {e}")
    if not found:
        print(f"⚠️ Not found: {file_name} (may already be restored or missing)")

print(f"\n✅ Undo complete: {restored_count} files restored.")