import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from scanner import scan_domain
from triage import triage_findings

if __name__ == "__main__":
    target = "testphp.vulnweb.com"
    print(f"[*] Starting scan for target: {target}...")
    
    # 1. Reconnaissance
    raw_findings = scan_domain(target)
    len_raw_findings = len(raw_findings)
    print(f"[+] Total raw exposures found: {len_raw_findings}")

    # Guard clause: stop if nothing was found
    if len_raw_findings == 0:
        print("[-] No findings discovered.")
        exit()

    # 2. AI Triage & Analysis
    print("[*] Running AI triage on raw findings...")
    triage_results = triage_findings(raw_findings)

    # 3. Report Output
    print("\n" + "=" * 60)
    print(f"TRIAGE AUDIT REPORT: {target.upper()}")
    print("=" * 60 + "\n")

    for item in triage_results:
        print(f"Severity:          {item.get('severity')}")
        print(f"Link:              {item.get('link')}")
        print(f"Is False Positive: {item.get('is_false_positive')}")
        print(f"Risk Summary:      {item.get('risk_summary')}")
        print(f"Remediation:       {item.get('remediation')}")
        print("-" * 60)