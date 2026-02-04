import os
from pathlib import Path
from organizer import FileOrganizer
from file_inspect import inspect_file

def main():
    if not os.path.exists(".env"):
        print("Error: no .env file found")
        return

    print("Type 'help' for list of commands")

    default_path = Path.home()

    while True:
        command = input(">>> ").lower()
        if command == "help":
            print("Commands:")
            print("organize - organize files")
            print("inspect - inspect file")
            print("exit - close program")
        elif command == "exit":
            print("Exiting...")
            return
        elif command == "organize":
            path = input(f"Enter path to organize (default: {default_path}): ")
            if path == "":
                path = default_path
            organizer = FileOrganizer(Path(path))
            organizer.organize()
        elif command == "inspect":
            path = input(f"Enter path to inspect (default: {default_path}): ")
            if path == "":
                path = default_path
            inspect_file(Path(path))
        else:
            print("Unknown command. Type 'help' for list of commands")


if __name__ == "__main__":
    main()