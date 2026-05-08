import google.generativeai as genai
from config.settings import API_KEY, GEMINI_MODEL
from config.safety import SAFETY_SETTINGS

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    safety_settings=SAFETY_SETTINGS
)

def ask_gemini(prompt: str) -> str:
    response = model.generate_content([prompt])
    return response.text

def ask_gemini_json(prompt: str) -> dict:
    response = model.generate_content([prompt])
    text = response.text.strip().replace("```json", "").replace("```", "")
    import json
    return json.loads(text)
