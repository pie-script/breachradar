import os
from pathlib import Path
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load from repo root or backend folder
env_root = Path(__file__).resolve().parent.parent / ".env"
env_backend = Path(__file__).resolve().parent.parent / "backend" / ".env"
if env_root.exists():
    load_dotenv(env_root)
elif env_backend.exists():
    load_dotenv(env_backend)
else:
    load_dotenv()

api_key = os.getenv("SERPAPI_API_KEY")

if not api_key:
    print("[!] Error: SERPAPI_API_KEY not found in .env file.")
    exit(1)

print("[*] Testing connection to SerpApi...")

params = {
    "engine": "google",
    "q": "site:example.com",
    "num": 2,
    "api_key": api_key
}

try:
    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])
    
    print("[+] Connection successful!")
    print(f"[+] Retrieved {len(organic)} sample results:")
    for res in organic:
        print(f"  - {res.get('title')} ({res.get('link')})")

except Exception as e:
    print(f"[!] API call failed: {e}")