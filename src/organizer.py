from pathlib import Path
from ai_module import classify_files

def create_folder(target_path: Path, category_name: str, files: list):
    print(f"Creating folder: {category_name}")
    new_folder = Path(target_path) / category_name
    new_folder.mkdir(exist_ok=True)

    for file in files:
        new_path = new_folder / file.name
        file.rename(new_path)
    
def dry_run_simulation(target_path: Path, batch_size=5):
    folder = Path(target_path)
    files_paths = []
    categories = {}
    if not folder.exists() or not folder.is_dir():
        print(f"Error: {target_path} is not a valid directory.")
        return


    for item in folder.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            files_paths.append(item)
    file_batches = []
    for i in range(0, len(files_paths), batch_size):
        file_batches.append(files_paths[i:i+batch_size])
    for i in range(len(file_batches)):
        raw_text = classify_files(file_batches[i])
        af_text = [category.strip() for category in raw_text.split(",")]
        if len(af_text) != len(file_batches[i]):
            print("Error wrong number of categories")
            return
        for j, category in enumerate(af_text):
            if category not in categories:
                categories[category] = []
            categories[category].append(file_batches[i][j]) 
    
    for category, files in categories.items():
        create_folder(target_path, category, files)

if __name__ == "__main__":
    path_to_clean = "/Users/tomek/Nsync/Test Folder"
    dry_run_simulation(path_to_clean)