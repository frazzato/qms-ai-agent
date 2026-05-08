import google.generativeai as genai
from config.settings import API_KEY, GEMINI_MODEL
from config.safety import SAFETY_SETTINGS

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    safety_settings=SAFETY_SETTINGS
)
