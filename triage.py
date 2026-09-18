import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        model='gemini-3.5-flash-lite',
        contents=[TRIAGE_PROMPT,user_content],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )

    return json.loads(response.text)

def generate_executive_summary(domain: str, findings: list) -> str:
    """Generates a high-level 2-3 sentence CISO risk summary of the domain posture."""
    if not findings:
        return f"Target domain `{domain}` exhibits a clean external footprint with zero indexed exposures across scanned vectors."
    
    prompt = f"""
    You are a Chief Information Security Officer (CISO) delivering an executive risk summary for domain: {domain}.
    Based on these analyzed findings:
    {json.dumps(findings, indent=2)}

    Provide a concise, professional, 2-3 sentence executive threat briefing.
    Highlight the overall security posture, most critical exposed vector (if any), and urgent organizational priority.
    Keep it strictly plaintext, direct, and authoritative with no markdown headers or bullet lists.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text.strip()
    except Exception as e:
        return f"Executive threat assessment temporarily unavailable: {e}"


def generate_remediation_patch(link: str, risk_summary: str) -> dict:
    """Generates copy-paste configuration snippets (Nginx, Apache, robots.txt) for an exposure."""
    prompt = f"""
    You are an DevSecOps engineer. Provide actionable remediation configuration snippets to fix this exposed asset:
    Target Link: {link}
    Risk Description: {risk_summary}

    Return strictly a JSON object with this schema:
    {{
      "config_type": "Nginx / Apache / robots.txt / Cloudflare Rule",
      "code_snippet": "the exact server block or rule snippet",
      "instructions": "1-2 sentence explanation of where to deploy this file"
    }}
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "config_type": "Error",
            "code_snippet": "# Unable to generate patch artifact",
            "instructions": str(e)
        }



if __name__ == "__main__":
    sample_findings = [
        {
            "category": "Exposed Configs & Secrets",
            "title": "Index of /backup",
            "link": "[http://testphp.vulnweb.com/backup/.env](http://testphp.vulnweb.com/backup/.env)",
            "snippet": "DB_PASSWORD=root_pass_2024 AWS_SECRET=AKIA...",
            "query_used": "site:testphp.vulnweb.com ext:env"
        },
        {
            "category": "Exposed Admin Portals",
            "title": "How to secure your admin panel - Security Blog",
            "link": "[https://testphp.vulnweb.com/blog/securing-admin](https://testphp.vulnweb.com/blog/securing-admin)",
            "snippet": "In this tutorial we explain why exposing /admin/login.php is dangerous.",
            "query_used": "site:testphp.vulnweb.com inurl:admin"
        }
    ]

    print("[*] Running test triage...")
    result = triage_findings(sample_findings)
    print(json.dumps(result, indent=2))