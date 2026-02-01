import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from PIL import Image
from pypdf import PdfReader
from docx import Document

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def classify_file(file_path: Path):
    suf = file_path.suffix.lower()
    instruction = """TASK: Analyze the file and return a specific category name.
RULES:
1. For PHOTOS: Describe the subject (e.g., VACATION, PORTRAITS, FOOD).
2. For DOCUMENTS: Identify the context (e.g., UNIVERSITY, INVOICES, WORK).
3. For PROGRAMMING: Identify the language or project (e.g., PYTHON, JAVASCRIPT).
4. Return ONLY 1-2 words as the folder name.
5. No special characters or dots."""
    contents = [instruction]

    try:
        if suf == ".jpg" or suf == ".png":
            contents.append(Image.open(file_path))
        elif suf == ".pdf":
            reader = PdfReader(file_path)
            text = reader.pages[0].extract_text()[:2000]
            contents.append(text)
        elif suf == ".docx":
            contents.append(Document(file_path))
        elif suf in ['.txt', '.py', '.md']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                contents.append(f"Text Content: {f.read(2000)}")
        
        contents.append(f"Filename: {file_path.name}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        print(response.text)
        return response.text.strip().upper()

    except Exception as e:
        print(f"ANALYSIS ERROR for {file_path.name}: {e}")
        return "UNCATEGORIZED"

if __name__ == "__main__":
    classify_file(Path('/Users/tomek/Nsync/ss/Screenshot 2024-11-11 at 15.50.42.png'))