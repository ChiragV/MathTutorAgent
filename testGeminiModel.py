import os
from dotenv import load_dotenv
from google import genai

# 1. Load the variables from your .env file
load_dotenv()

# Verify the key was loaded properly
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found. Check your .env file.")
    exit()

print("Key found! Testing connection...")

try:
    # 2. Initialize the client 
    # (It automatically detects the GEMINI_API_KEY environment variable)
    client = genai.Client()
    
    # Get the model from .env, or default to standard flash
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    # 3. Make a simple test request
    response = client.models.generate_content(
        model=model_name,
        contents="Hello! This is a test. Please reply with exactly 'Connection successful!'"
    )
    
    print("\n✅ Success!")
    print("Gemini says:", response.text)

except Exception as e:
    print("\n❌ Error connecting to Gemini API:")
    print(e)