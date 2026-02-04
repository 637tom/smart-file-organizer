from pathlib import Path
from ai_module import describe_file

def inspect_file(file_path : Path):
    if not file_path.exists():
        print("File not found")
        return
    print(f"Filename: {file_path.name}")
    print(f"Suffix: {file_path.suffix}")
    print(f"Parent: {file_path.parent}")
    print(f"Size: {file_path.stat().st_size}")
    print(f"Created: {file_path.stat().st_ctime}")
    print(f"Modified: {file_path.stat().st_mtime}")
    print(f"Description: {describe_file(file_path)}")
