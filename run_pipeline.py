from scanner import scan_domain
from triage import triage_findings

if __name__=="__main__" :
    
    target="testphp.vulnweb.com"
    raw_findings=scan_domain(target)
    len_raw_findings=len(raw_findings)
    
    if len_raw_findings == 0:
        print("No findings")
        exit()
    for item in raw_findings:
        print(f"Severity: {item['severity']}")
        print(f"Link: {item['link']}")
        print(f"Title: {item['title']}")
        print(f"Snippet: {item['snippet']}")
        print(f"Source: {item['source']}")
        print(f"Date: {item['date']}")
        print(f"Query used: {item['query_used']}")
        print("-" * 60) 

