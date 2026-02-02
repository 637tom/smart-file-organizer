from pathlib import Path
from ai_module import classify_files

class FileOrganizer:
    def __init__(self, target_path: Path):
        self.target_path = target_path
        if not self.target_path.exists() or not self.target_path.is_dir():
            raise ValueError(f"Error: {self.target_path} is not a directory.")
        self.history = []
    
    def create_folder(self, category_name: str, files: list):
        print(f"Creating folder: {category_name}")
        new_folder = Path(self.target_path) / category_name
        new_folder.mkdir(exist_ok=True)

        for file in files:
            new_path = new_folder / file.name
            file.rename(new_path)
            self.history.append((new_path, file))
            
    @staticmethod
    def batch(files_paths: list, batch_size: int):
        file_batches = []
        for i in range(0, len(files_paths), batch_size):
            file_batches.append(files_paths[i:i+batch_size])
        return file_batches

    def dry_run_simulation(self, batch_size=5):
        folder = Path(self.target_path)
        files_paths = []
        categories = {}

        for item in folder.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                files_paths.append(item)

        file_batches = self.batch(files_paths, batch_size)

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
            self.create_folder(category, files)

if __name__ == "__main__":
    path_to_clean = "/Users/tomek/Nsync/Test Folder"
    try:
        organizer = FileOrganizer(Path(path_to_clean))
        organizer.dry_run_simulation()
    except Exception as e:
        print(e)