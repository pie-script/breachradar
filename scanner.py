import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
params ={
    "q":"cofee",
    "api_key": SERPAPI_API_KEY
}