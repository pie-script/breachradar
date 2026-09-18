from scanner import scan_domain
from triage import triage_findings

if __name__=="__main__" :
    
    target="testphp.vulnweb.com"
    raw_findings=scan_domain(target)
    len_raw_findings=len(raw_findings)
    triage_results=triage_findings(raw_findings)

    if len_raw_findings == 0:
        print("No findings")
        exit()

    for item in triage_results:
        print(f"Severity :{item.get("severity")}")
        print(f"Link : {item.get("link")}")
        print(f"Is False Positive : {item.get("is_false_positive")}")
        print(f"Risk Summary : {item.get("risk_summary")}")
        print(f"Remediation : {item.get("remediation")}")
        print("-"*60)
      

