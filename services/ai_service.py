import google.generativeai as genai
from config.settings import API_KEY, GEMINI_MODEL

# Configure the API key
genai.configure(api_key=API_KEY)

# Initialize the model (no safety settings — required for new SDK)
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL
)

def ask_gemini(prompt: str) -> str:
    """Return plain text response from Gemini."""
    response = model.generate_content([prompt])
    return response.text

def ask_gemini_json(prompt: str) -> dict:
    """Return JSON response from Gemini."""
    response = model.generate_content([prompt])
    text = response.text.strip().replace("```json", "").replace("```", "")
    import json
    return json.loads(text)
