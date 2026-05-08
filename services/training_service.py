from services.ai_service import ask_groq_json

def generate_training_module(filename: str):
    prompt = f"""
    You are a Senior QMS Trainer specializing in AS9100.

    Create a training module for the document titled: {filename}.

    You MUST return ONLY a valid JSON object.
    No explanations. No markdown. No commentary. No extra text.

    The JSON MUST have exactly these keys:
    "summary": "...",
    "importance": "...",
    "trap": "...",
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "..."

    Respond with STRICT JSON ONLY.
    """
    return ask_groq_json(prompt)
