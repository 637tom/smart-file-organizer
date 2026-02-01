import os
from google import genai
from dotenv import load_dotenv

# Load configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

print("Starting connection test...")

try:
    # Execute test request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="System check: respond with 'Ready'"
    )
    
    # Output results
    print("--- CONNECTION TEST ---")
    print(f"Status: SUCCESS")
    print(f"Model output: {response.text.strip()}")
    print("--- END ---")

except Exception as e:
    print("--- CONNECTION TEST ---")
    print(f"Status: FAILED")
    print(f"Error details: {e}")
    print("--- END ---")