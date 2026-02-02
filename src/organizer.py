from pathlib import Path
from ai_module import classify_files

def dry_run_simulation(target_path, batch_size=5):
    folder = Path(target_path)
    files_paths = []
    categories = {}
    if not folder.exists() or not folder.is_dir():
        print(f"BŁĄD: Ścieżka {target_path} nie jest poprawnym folderem.")
        return


    for item in folder.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            files_paths.append(item)
    file_batches = []
    for i in range(0, len(files_paths), batch_size):
        file_batches.append(files_paths[i:i+batch_size])
    for i in range(len(file_batches)):
        for j in range(len(file_batches[i])):
            print(file_batches[i][j].name)
        print(classify_files(file_batches[i]))
if __name__ == "__main__":
    path_to_clean = "/Users/tomek/Nsync/ss"
    dry_run_simulation(path_to_clean)