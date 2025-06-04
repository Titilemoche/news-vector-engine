# pipeline/llm_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API (tu dois avoir ta clé API dans une variable d'environnement GEMINI_API_KEY)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback or error if GEMINI_API_KEY is not found, Google's library will also check GOOGLE_API_KEY
    # but we make it explicit that we are looking for GEMINI_API_KEY from .env
    print("Error: GEMINI_API_KEY not found in .env file or environment variables.")
    # Optionally, you could raise an exception here or let genai.configure fail if it also doesn't find GOOGLE_API_KEY
    # For now, we'll let genai.configure try its defaults if GEMINI_API_KEY is missing.
    # The Google library itself will raise an error if no key is found (either via configure or GOOGLE_API_KEY env var).
    pass # Let genai.configure handle the missing key if GEMINI_API_KEY is not set

genai.configure(api_key=api_key) # Pass the loaded key, or None if not found (Google lib will then check GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def call_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()