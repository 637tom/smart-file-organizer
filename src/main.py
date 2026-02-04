import os
from pathlib import Path
from organizer import FileOrganizer
from file_inspect import inspect_file
from file_finder import find_file

def main():
    if not os.path.exists(".env"):
        print("Error: no .env file found")
        return

    print("Type 'help' for list of commands")

    default_path = Path.home()

    while True:
        command = input(">>> ").lower().strip()
        if command == "help":
            print("Commands:")
            print("organize - organize files")
            print("inspect - inspect file")
            print("exit - close program")
            print("find - find files with specific query")
        elif command == "exit":
            print("Exiting...")
            return
        elif command == "organize":
            path = input(f"Enter path to organize (default: {default_path}): ").strip()
            if path == "":
                path = default_path
            organizer = FileOrganizer(Path(path))
            organizer.organize()
        elif command == "inspect":
            path = input(f"Enter path to inspect (default: {default_path}): ").strip()
            if path == "":
                path = default_path
            inspect_file(Path(path))
        elif command == "find":
            path = input(f"Enter path to search (default: {default_path}): ").strip()
            if path == "":
                path = default_path
            query = input("Enter query: ").strip()  
            best = find_file(Path(path), query)
            if best is not None:
                print(f"\nBest matching file: {best}")
        else:
            print("Unknown command. Type 'help' for list of commands")


if __name__ == "__main__":
    main()