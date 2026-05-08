from services.ai_service import ask_groq_json

def generate_training_module(filename: str):
    prompt = f"""
    You are a Senior QMS Trainer specializing in AS9100.

    Create a training module for the document titled: {filename}.

    You MUST return ONLY a valid JSON object.
    No explanations. No markdown. No commentary. No extra text.

    The JSON MUST have exactly these keys:
    "summary": "A detailed 3–5 sentence summary of the document.",
    "importance": "A 2–3 sentence explanation of why this document matters for AS9100 compliance.",
    "trap": "A realistic audit trap or common nonconformity related to this document.",
    "question": "A clear multiple-choice question that tests understanding of the document.",
    "options": [
        "A full-sentence option A",
        "A full-sentence option B",
        "A full-sentence option C",
        "A full-sentence option D"
    ],
    "answer": "The correct option letter (A, B, C, or D)."

    Requirements:
    - All fields must contain meaningful, complete content.
    - Options must be distinct and realistic.
    - The question must be directly related to the document.
    - The answer must match one of the options.

    Respond with STRICT JSON ONLY.
    """
    return ask_groq_json(prompt)
