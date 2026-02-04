from pathlib import Path
from ai_module import find_best_file

def batch(files_paths: list, batch_size: int):
        file_batches = []
        for i in range(0, len(files_paths), batch_size):
            file_batches.append(files_paths[i:i+batch_size])
        return file_batches

def find_file(target_path : Path, query : str):
    if not target_path.exists():
        print("Folder not found")
        return None

    files_paths = []
    for item in target_path.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            files_paths.append(item)
    if len(files_paths) == 0:
        return "No files in folder found"
    best = files_paths[0]
    files_paths = files_paths[1:]
    file_batches = batch(files_paths, 4) 
    for i in range(len(file_batches)):
        curr_batch = file_batches[i]
        curr_batch.append(best)
        print(f"\r Analyzing file {i*4+1} of {len(files_paths)}", end="")
        curr = find_best_file(curr_batch, query)
        if curr is None:
            print("Error")
            return None
        best = curr
    return best
        

    