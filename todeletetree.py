import os

# Dossiers à inclure (ajuste à ton besoin)
folders_to_include = ["backend", "frontend", "UIM5Stack"]
max_depth = 6  # Profondeur maximale

def print_tree(start_path, prefix='', max_depth=4, current_depth=0):
    if current_depth > max_depth:
        return
    for item in sorted(os.listdir(start_path)):
        path = os.path.join(start_path, item)
        if os.path.isdir(path):
            print(f"{prefix}📁 {item}")
            print_tree(path, prefix + '    ', max_depth, current_depth + 1)
        else:
            print(f"{prefix}📄 {item}")

base_path = os.getcwd()
for folder in folders_to_include:
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        print(f"\n🗂️ Dossier: {folder}")
        print_tree(folder_path, prefix='  ', max_depth=max_depth)
    else:
        print(f"\n⚠️ Le dossier '{folder}' n'existe pas.")
