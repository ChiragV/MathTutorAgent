import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load variables from .env
load_dotenv()

# Verify the key was loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY not found. Check your .env file.")
    exit()

print("Key found! Testing connection...")

try:
    # 2. Initialize the client
    client = OpenAI(api_key=api_key)

    # Get the model from .env, or use a default
    model_name = os.getenv("OPENAI_MODEL", "gpt-5.5")

    # 3. Make a simple test request
    response = client.responses.create(
        model=model_name,
        input="Hello! This is a test. Please reply with exactly 'Connection successful!'"
    )

    print("\n✅ Success!")
    print("OpenAI says:", response.output_text)

except Exception as e:
    print("\n❌ Error connecting to OpenAI API:")
    print(e)