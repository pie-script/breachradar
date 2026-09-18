"""
BreachRadar API
────────────────
Thin FastAPI layer around your existing scanner.py / triage.py modules.
Drop your existing scanner.py and triage.py into this backend/ folder —
the imports below assume the same function signatures your Streamlit
app already used, so no changes should be needed there.
"""
from collections import Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scanner import scan_domain
from triage import triage_findings, generate_executive_summary, generate_remediation_patch

app = FastAPI(title="BreachRadar API", version="1.0.0")

# Allow the Vite dev server (and any other origin you deploy the frontend to)
# to call this API. Tighten this list before shipping to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / response models ───────────────────────────────────────────────
class ScanRequest(BaseModel):
    domain: str


class PatchRequest(BaseModel):
    link: str
    risk_summary: str = ""


# ── Helpers (ported straight from app.py) ───────────────────────────────────
def _clean_domain(raw: str) -> str:
    d = raw.strip().lower()
    for prefix in ("https://", "http://"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d.split("/")[0]


def _enrich_results(triage_results, raw_findings):
    """Merge category, query_used, source from raw findings into triage results."""
    raw_lookup = {rf.get("link", ""): rf for rf in raw_findings if rf.get("link")}
    enriched = []
    for item in triage_results:
        merged = dict(item)
        raw = raw_lookup.get(item.get("link", ""), {})
        merged.setdefault("category", raw.get("category", ""))
        merged.setdefault("query_used", raw.get("query_used", ""))
        merged.setdefault("source", raw.get("source", ""))
        enriched.append(merged)
    return enriched


def _compute_stats(enriched):
    """Same posture-score / severity-mix math the Streamlit dashboard used,
    now computed once on the server so the frontend just renders numbers."""
    total = len(enriched)
    actionable = [x for x in enriched if not x.get("is_false_positive")]
    critical = sum(x.get("severity") == "Critical" for x in actionable)
    high = sum(x.get("severity") == "High" for x in actionable)
    medium = sum(x.get("severity") == "Medium" for x in actionable)
    low = sum(x.get("severity") == "Low" for x in actionable)
    informational = sum(x.get("severity") == "Informational" for x in enriched)
    false_positive = sum(x.get("is_false_positive", False) for x in enriched)

    exposure_points = critical * 30 + high * 18 + medium * 9 + low * 3
    posture_score = max(0, min(100, 100 - exposure_points))

    categories = Counter((x.get("category") or "Uncategorized") for x in enriched)
    top_category = categories.most_common(1)[0][0] if categories else "None"

    return {
        "total": total,
        "actionable": len(actionable),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "informational": informational,
        "false_positive": false_positive,
        "posture_score": posture_score,
        "noise_pct": round((false_positive / max(total, 1)) * 100),
        "categories": [{"name": k, "count": v} for k, v in categories.most_common()],
        "top_category": top_category,
    }


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/scan")
def scan(req: ScanRequest):
    domain = _clean_domain(req.domain)
    if not domain:
        raise HTTPException(status_code=400, detail="A valid target domain is required.")

    raw_findings = scan_domain(domain)

    if not raw_findings:
        return {
            "domain": domain,
            "raw_findings": [],
            "results": [],
            "executive_summary": "",
            "stats": _compute_stats([]),
        }

    triaged = triage_findings(raw_findings)
    enriched = _enrich_results(triaged, raw_findings)
    summary = generate_executive_summary(domain, triaged)

    return {
        "domain": domain,
        "raw_findings": raw_findings,
        "results": enriched,
        "executive_summary": summary,
        "stats": _compute_stats(enriched),
    }


@app.post("/api/patch")
def patch(req: PatchRequest):
    if not req.link:
        raise HTTPException(status_code=400, detail="link is required.")
    return generate_remediation_patch(req.link, req.risk_summary)
