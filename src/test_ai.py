import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        # Próbujemy najbezpieczniejszego modelu
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Say 'Connection OK'"
        )
        print(f"STATUS: {response.text}")
    except Exception as e:
        print(f"!!! ERROR: {e}")

if __name__ == "__main__":
    test_connection()
