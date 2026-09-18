from httpx import Response
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TRIAGE_PROMPT = """
You are a senior Application Security and OSINT analyst specializing in exposed asset triage.
Analyze the provided list of search findings obtained via Google Dorking.

For each finding:
1. Determine if it is a REAL EXPOSURE or a FALSE POSITIVE:
   - Mark as False Positive (`true`) if the result is general documentation, an educational tutorial, a news article, or an intentional public disclosure.
   - Mark as Real Exposure (`false`) if the link exposes active administrative interfaces, environment files, backups, database credentials, or private internal docs.
2. Assign a severity rating: "Critical", "High", "Medium", "Low", or "Informational".
3. Write a 1-sentence risk summary describing the potential threat.
4. Write a 1-sentence actionable remediation step (e.g., web server block rule, file permission adjustment, or robots.txt/Google Search Console removal).

Output strictly a valid JSON array of objects with no markdown formatting, backticks, or extra text.
Schema:
[
  {
    "link": "exact url string",
    "is_false_positive": boolean,
    "severity": "Critical" | "High" | "Medium" | "Low" | "Informational",
    "risk_summary": "string",
    "remediation": "string"
  }
]
"""

def triage_findings(findings : list):
    if not findings:
        return []

    findings_str = json.dumps(findings,indent=2)
    user_content=f"Findings to evaluate :\n{findings_str}"

    response= client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[TRIAGE_PROMPT,user_content],
        config=type.GenerateContentConfig(
            response_mime_type="application/json",
            temparature=0.2
        )
    )
    
    return json.loads(response.text)