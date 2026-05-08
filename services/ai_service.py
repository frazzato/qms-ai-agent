from groq import Groq
from config.settings import GROQ_API_KEY
import json

client = Groq(api_key=GROQ_API_KEY)

# Use a stable 2026 model ID
# "llama3-8b-8192" is often restricted or deprecated in newer API versions
MODEL_NAME = "llama-3.1-8b-instant"

def ask_groq(prompt: str) -> str:
    """Return plain text response from Groq."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def ask_groq_json(prompt: str) -> dict:
    """Return JSON response from Groq using json_object mode."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        # This flag is CRITICAL for ask_groq_json to prevent formatting errors
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
