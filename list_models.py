
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    # Attempt to list models. The method might differ slightly depending on SDK version
    # Inspecting the client object or assuming standard 'models.list' structure
    print("Attempting to list models...")
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print(f"Error listing models: {e}")
