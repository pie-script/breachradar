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