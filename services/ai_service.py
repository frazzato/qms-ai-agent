from groq import Groq
from config.settings import GROQ_API_KEY
import json

client = Groq(api_key=GROQ_API_KEY)

def ask_groq(prompt: str) -> str:
    """Return plain text response from Groq Llama 3."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def ask_groq_json(prompt: str) -> dict:
    """Return JSON response from Groq Llama 3."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
