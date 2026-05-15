from groq import Groq
from config.settings import GROQ_API_KEY
import json

client = Groq(api_key=GROQ_API_KEY)

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
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# ─────────────────────────────────────
# NEW: Audit Agent Functions
# ─────────────────────────────────────

def analyze_gaps(doc_text: str, standard: str = "AS9100 Rev D") -> str:
    prompt = f"""You are an expert {standard} and ISO 9001:2015 QMS auditor.

Analyze the following document text and identify:

1. **Covered Clauses** — list each {standard} clause that IS addressed
2. **Missing Clauses** — list each clause that SHOULD be addressed but is NOT found
3. **Weak Areas** — clauses mentioned but lacking sufficient detail
4. **Risk Level** — rate each gap as HIGH / MEDIUM / LOW risk
5. **Recommendations** — specific actions to close each gap

Format with clear sections and tables where appropriate.

DOCUMENT TEXT:
{doc_text[:8000]}
"""
    return ask_groq(prompt)


def generate_capa(finding: str, clause: str = "") -> str:
    prompt = f"""You are an AS9100 Rev D / ISO 9001:2015 CAPA specialist.

Given this audit finding, generate a complete CAPA report:

FINDING: {finding}
{'RELATED CLAUSE: ' + clause if clause else ''}

Include:
1. **Root Cause Analysis** — use 5-Why method
2. **Immediate Containment Action**
3. **Corrective Action** — eliminate the root cause
4. **Preventive Action** — prevent recurrence
5. **Verification Method** — how to confirm effectiveness
6. **Target Completion Date** — realistic timeline
7. **Risk Assessment** — before and after CAPA

Format as a structured report ready for QMS records.
"""
    return ask_groq(prompt)


def generate_checklist(clause: str, process_area: str = "") -> str:
    prompt = f"""You are an AS9100 Rev D / ISO 9001:2015 lead auditor.

Generate a detailed internal audit checklist for:
CLAUSE: {clause}
{'PROCESS AREA: ' + process_area if process_area else ''}

For each checklist item include:
- Question to ask
- What objective evidence to look for
- Reference to specific sub-clause
- Pass/Fail criteria

Format as a numbered checklist ready for use in an internal audit.
"""
    return ask_groq(prompt)


def assess_risk(process: str, context: str = "") -> str:
    prompt = f"""You are an AS9100 Rev D risk management specialist.

Perform a risk assessment for:
PROCESS: {process}
{'CONTEXT: ' + context if context else ''}

Provide:
1. **Risk Identification** — list potential risks (minimum 5)
2. **Risk Matrix** — Likelihood (1-5) x Severity (1-5) = Risk Score
3. **Risk Classification** — LOW (1-8) / MEDIUM (9-15) / HIGH (16-25)
4. **Mitigation Actions** — for each MEDIUM and HIGH risk
5. **Monitoring Plan** — how to track risk levels

Format as a table-based risk register.
"""
    return ask_groq(prompt)
