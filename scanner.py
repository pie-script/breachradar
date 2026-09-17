import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
DORK_CATEGORIES = {
    "Exposed Configs & Secrets": "(ext:env OR ext:yml OR ext:yaml) (DB_PASSWORD OR secret OR auth)",
    "Database Backups": "(ext:sql OR ext:bak OR ext:dmp OR ext:backup)",
    "Exposed Admin Portals": "(inurl:login OR inurl:admin OR inurl:dashboard)",
    "Sensitive Files & Logs": "ext:log (error OR password OR exception)",
    "Sensitive Documents": 'filetype:pdf ("confidential" OR "internal use only")',
}

def scan_domain(target_domain):

    all_findings=[]
    for category, dork in DORK_CATEGORIES.items():
        query = f"site:{target_domain} {dork}"
    
        params={
            "engine": "google",
            "q" : query,
            "num":5,
            "api_key":SERPAPI_API_KEY
        }
    
        try:
            search = GoogleSearch(params)
            results= search.get_dict()
            organic_results=results.get('organic_results', [])
            for item in organic_results:
                findings={
                    "category":category,
                    "title" : item.get('title'),
                    "link":item.get('link'),
                    "snippet":item.get('snippet'),
                    "source":item.get('source'),
                    "date" : item.get('date'),
                    "query_used":query

                }
                all_findings.append(findings)
        except Exception as e:
            print(f"Error Scanning the categories : {category} {e}")

    return all_findings