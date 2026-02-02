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

def classify_files(files : list, existing_categories : list):
    if len(existing_categories) > 0:
        existing_categories = ", ".join(existing_categories)
    else:
        existing_categories = "None you have to create new categories"

    # Optimized promt for gemini 2.0 flash
    instruction = f"""ROLE: Senior Content Analyst & Organizer.
TASK: Deeply analyze content of {len(files)} files and categorize them precisely.

CONTEXT - EXISTING CATEGORIES: [{existing_categories}]

BEST FIT PROTOCOL (Follow strictly):
1. CONTENT FIRST: Analyze what the file *contains*, not just its format. A photo of a document is a DOCUMENT, not just PHOTOS.
2. SPECIFIC OVER GENERIC: Avoid dumping distinct content into generic buckets like 'SCREENSHOTS' or 'MISC'.
   - BAD: A screenshot of stock charts -> CATEGORY: SCREENSHOTS
   - GOOD: A screenshot of stock charts -> CATEGORY: TRADING or FINANCE
3. REUSE vs. CREATE:
   - Check the EXISTING CATEGORIES list first. If a category fits the content well, USE IT.
   - If the content is significantly different from existing categories, CREATE A NEW, SPECIFIC ONE. Do not be afraid to create new categories for distinct topics.

RULES:
1. OUTPUT FORMAT: Exactly {len(files)} pairs in format: CATEGORY|DESCRIPTION
2. SEPARATOR: Use '^' between pairs. No '^' at the end.
3. CATEGORY NAMES: Single word, UPPERCASE, use underscores for spaces (e.g., WEB_DEV, UNIVERSITY_MATH).
4. DESCRIPTION: Max 10 words summary.

EXAMPLE BEHAVIOR:
(Input: image of python code, image of a cat, pdf invoice)
(Existing buckets: PHOTOS)
OUTPUT: PYTHON|Script with sorting algorithms^PHOTOS|A cute tabby cat^INVOICES|Electricity bill Jan 2024
*(Notice: It reused PHOTOS for the cat, but created PYTHON and INVOICES because they were specific distinct content)*"""


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
            elif suf in ['.txt', '.py', '.md', '.json', '.js', '.html', '.css', '.cpp', '.cs', '.java', '.rb', '.php', '.go', '.rs', '.swift', '.kt', '.kts', '.ts', '.tsx', '.jsx', '.scss', '.sass', '.less', '.styl', '.stylus', '.sass', '.less', '.styl', '.stylus', '.in', '.out']:
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
