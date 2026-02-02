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

def classify_files(files):
    instruction = """TASK: Analyze the provided files in the exact order they are given.
OUTPUT: Return pairs in format CATEGORY|DESCRIPTION, separated by '^'.
RULES:
1. One CATEGORY|DESCRIPTION pair per file.
2. For PHOTOS: Identify the subject (e.g., VACATION, PORTRAITS, FOOD).
3. For PROGRAMMING: Identify the language or project (e.g., PYTHON, JAVASCRIPT).
4. For DOCUMENTS: Identify the context (e.g., UNIVERSITY, INVOICES, WORK).
5. DESCRIPTION: Brief summary of content (max 12 words).
6. Use '|' to separate CATEGORY from DESCRIPTION.
7. Use '^' to separate results for different files.
8. Format example: VACATION|Sunset in Rome^INVOICES|Gas bill Jan 2024^PYTHON|Sorting script
9. No other text, no explanations, no headers."""
    contents = [instruction]
    for i, file_path in enumerate(files):
        suf = file_path.suffix.lower()
        contents.append(f"--- FILE {i+1}: {file_path.name} ---")
        try:
            if suf == ".jpg" or suf == ".png":
                im = Image.open(file_path)
                im.thumbnail((512, 512))
                contents.append(im)
            elif suf == ".pdf":
                reader = PdfReader(file_path)
                text = reader.pages[0].extract_text()[:1500]
                contents.append(text)
            elif suf == ".docx":
                d = Document(file_path)
                text = "\n".join([p.text for p in d.paragraphs])
                text = text[:1500]
                contents.append(text)
            elif suf in ['.txt', '.py', '.md', '.json', '.js', '.html', '.css', '.cpp', '.cs', '.java', '.rb', '.php', '.go', '.rs', '.swift', '.kt', '.kts', '.ts', '.tsx', '.jsx', '.scss', '.sass', '.less', '.styl', '.stylus', '.sass', '.less', '.styl', '.stylus']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    contents.append(f.read(1500))
        except Exception as e:
            print(f"ANALYSIS ERROR for {file_path.name}: {e}")
            contents.append("UNCATEGORIZED")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents
        )
        return response.text.strip().lower()

    except Exception as e:
        print(f"ANALYSIS ERROR for {file_path.name}: {e}")
        return "UNCATEGORIZED"
