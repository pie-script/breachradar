import streamlit as st
import pandas as pd
from scanner import scan_domain
from triage import triage_findings, generate_executive_summary, generate_remediation_patch

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BreachRadar | AI Attack Surface Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: '"'"'Inter'"'"', sans-serif; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0d14 0%, #0d1120 100%) !important;
    border-right: 1px solid #1a2035 !important;
}
[data-testid="stSidebar"] * { color: #c9d1e0 !important; }

.sidebar-brand { display:flex;align-items:center;gap:12px;padding:4px 0 16px 0;border-bottom:1px solid #1a2035;margin-bottom:20px; }
.brand-icon { width:38px;height:38px;background:linear-gradient(135deg,#e63946,#c1121f);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 0 18px rgba(230,57,70,0.45);flex-shrink:0; }
.brand-name { font-size:20px;font-weight:800;letter-spacing:-0.5px;background:linear-gradient(90deg,#e63946,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.brand-sub { font-size:10px;color:#4a5568 !important;letter-spacing:1px;text-transform:uppercase;margin-top:1px;font-weight:500; }

.pipeline-card { background:#0f1520;border:1px solid #1e2d45;border-radius:10px;padding:14px;margin-top:16px; }
.pipeline-title { font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#4a6fa5 !important;font-weight:700;margin-bottom:10px; }
.pipeline-step { display:flex;align-items:center;gap:8px;padding:5px 0;font-size:12px;color:#7a8fa8 !important; }
.pipeline-dot { width:7px;height:7px;border-radius:50%;flex-shrink:0; }
.dot-green  { background:#21c354;box-shadow:0 0 6px #21c354aa; }
.dot-blue   { background:#4a9eff;box-shadow:0 0 6px #4a9effaa; }
.dot-purple { background:#a855f7;box-shadow:0 0 6px #a855f7aa; }

.hero-header { background:linear-gradient(135deg,#0a0d14 0%,#0d1829 50%,#100a1a 100%);border:1px solid #1a2540;border-radius:16px;padding:28px 32px;margin-bottom:24px;position:relative;overflow:hidden; }
.hero-header::before { content:'';position:absolute;top:-40px;right:-40px;width:200px;height:200px;background:radial-gradient(circle,rgba(230,57,70,0.08) 0%,transparent 70%);border-radius:50%; }
.hero-title { font-size:30px;font-weight:800;letter-spacing:-0.8px;margin:0 0 6px 0;background:linear-gradient(90deg,#ffffff 0%,#c9d1e0 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.hero-sub { font-size:14px;color:#4a6fa5;margin:0;font-weight:400; }
.hero-tag { display:inline-flex;align-items:center;gap:5px;background:rgba(230,57,70,0.1);border:1px solid rgba(230,57,70,0.3);color:#e63946 !important;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:600;letter-spacing:0.5px;margin-bottom:12px; }
.pulse-dot { width:6px;height:6px;background:#e63946;border-radius:50%;display:inline-block;box-shadow:0 0 0 0 rgba(230,57,70,0.6);animation:pulse 2s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(230,57,70,0.6)} 70%{box-shadow:0 0 0 7px rgba(230,57,70,0)} 100%{box-shadow:0 0 0 0 rgba(230,57,70,0)} }

.kpi-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px; }
.kpi-card { background:#0a0d14;border:1px solid #1a2035;border-radius:12px;padding:18px 20px;position:relative;overflow:hidden; }
.kpi-card::before { content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:12px 12px 0 0; }
.kpi-card.total::before  { background:linear-gradient(90deg,#4a9eff,#00d4ff); }
.kpi-card.risk::before   { background:linear-gradient(90deg,#e63946,#ff6b6b); }
.kpi-card.critical::before { background:linear-gradient(90deg,#ff4b4b,#ff8800); }
.kpi-card.noise::before  { background:linear-gradient(90deg,#21c354,#00b4d8); }
.kpi-label { font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#4a6fa5;font-weight:600;margin-bottom:10px; }
.kpi-value { font-size:40px;font-weight:800;letter-spacing:-2px;line-height:1;font-family:"JetBrains Mono",monospace;margin-bottom:6px; }
.kpi-card.total .kpi-value   { color:#4a9eff; }
.kpi-card.risk .kpi-value    { color:#e63946; }
.kpi-card.critical .kpi-value { color:#ff8800; }
.kpi-card.noise .kpi-value   { color:#21c354; }
.kpi-sub { font-size:11px;color:#3a4a5a;font-weight:500; }

.sev-badge { display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase; }
.sev-critical { background:rgba(255,75,75,0.12);color:#ff4b4b;border:1px solid rgba(255,75,75,0.4); }
.sev-high     { background:rgba(255,136,0,0.12);color:#ff8800;border:1px solid rgba(255,136,0,0.4); }
.sev-medium   { background:rgba(255,200,0,0.12);color:#ffcc00;border:1px solid rgba(255,200,0,0.4); }
.sev-low      { background:rgba(33,195,84,0.12);color:#21c354;border:1px solid rgba(33,195,84,0.4); }
.sev-info     { background:rgba(74,158,255,0.12);color:#4a9eff;border:1px solid rgba(74,158,255,0.4); }
.sev-fp       { background:rgba(100,100,100,0.1);color:#6a7a8a;border:1px solid rgba(100,100,100,0.3); }

.cat-pill { display:inline-block;padding:3px 9px;border-radius:5px;font-size:10px;font-weight:600;letter-spacing:0.5px;background:rgba(74,158,255,0.08);color:#4a9eff;border:1px solid rgba(74,158,255,0.2);margin-bottom:10px; }

.finding-card { background:#080b12;border:1px solid #151c2e;border-radius:12px;padding:18px 20px;margin-bottom:12px;transition:border-color 0.2s,box-shadow 0.2s;position:relative;overflow:hidden; }
.finding-card:hover { border-color:#2a3a5a;box-shadow:0 4px 24px rgba(0,0,0,0.4); }
.finding-card.fp { opacity:0.6; }
.finding-card .card-header { display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:10px;flex-wrap:wrap; }
.card-url { font-family:"JetBrains Mono",monospace;font-size:13px;color:#7aa2d4;word-break:break-all;flex:1; }
.card-url a { color:#7aa2d4 !important;text-decoration:none; }
.card-url a:hover { color:#4a9eff !important;text-decoration:underline; }
.card-section-label { font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#2a3a5a;font-weight:700;margin:12px 0 5px 0; }
.card-risk-text { font-size:13px;color:#8899aa;line-height:1.6; }
.card-remediation { background:rgba(33,195,84,0.05);border:1px solid rgba(33,195,84,0.15);border-left:3px solid #21c354;border-radius:0 8px 8px 0;padding:10px 14px;margin-top:12px;font-size:13px;color:#7aad7a;line-height:1.5; }

.section-header { display:flex;align-items:center;gap:10px;margin:4px 0 16px 0;padding-bottom:12px;border-bottom:1px solid #101825; }
.section-title { font-size:16px;font-weight:700;color:#c9d1e0; }
.section-count { background:#1a2540;color:#4a9eff;border-radius:20px;padding:2px 10px;font-size:12px;font-weight:600; }

.empty-state { text-align:center;padding:50px 20px;color:#2a3a5a; }
.empty-state .empty-icon { font-size:48px;margin-bottom:12px; }
.empty-state .empty-title { font-size:18px;font-weight:600;color:#3a5a7a;margin-bottom:6px; }
.empty-state .empty-sub { font-size:13px;color:#1a2a3a; }

.all-clear { background:linear-gradient(135deg,rgba(33,195,84,0.05),rgba(0,180,216,0.05));border:1px solid rgba(33,195,84,0.2);border-radius:14px;padding:32px;text-align:center; }
.all-clear-icon { font-size:52px;margin-bottom:12px; }
.all-clear-title { font-size:22px;font-weight:700;color:#21c354;margin-bottom:8px; }
.all-clear-sub { font-size:14px;color:#4a7a5a; }

[data-testid="stTabs"] [data-baseweb="tab-list"] { background:transparent !important;border-bottom:1px solid #101825 !important;gap:4px !important; }
[data-testid="stTabs"] [data-baseweb="tab"] { background:transparent !important;color:#4a6fa5 !important;font-size:13px !important;font-weight:500 !important;padding:8px 16px !important;border-radius:8px 8px 0 0 !important; }
[data-testid="stTabs"] [aria-selected="true"] { background:#0f1824 !important;color:#c9d1e0 !important;border-bottom:2px solid #e63946 !important; }

::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#0a0d14; }
::-webkit-scrollbar-thumb { background:#1a2540;border-radius:3px; }

[data-testid="stTextInput"] input { background:#0a0d14 !important;border-color:#1a2540 !important;color:#c9d1e0 !important;font-family:"JetBrains Mono",monospace !important;font-size:13px !important; }
[data-testid="stTextInput"] input:focus { border-color:#e63946 !important;box-shadow:0 0 0 2px rgba(230,57,70,0.15) !important; }

[data-testid="stButton"] > button[kind="primary"] { background:linear-gradient(135deg,#c1121f,#e63946) !important;border:none !important;font-weight:700 !important;letter-spacing:0.3px !important;box-shadow:0 4px 16px rgba(230,57,70,0.35) !important;transition:all 0.2s !important; }
[data-testid="stButton"] > button[kind="primary"]:hover { box-shadow:0 6px 24px rgba(230,57,70,0.55) !important;transform:translateY(-1px) !important; }

[data-testid="stDownloadButton"] > button { background:#0f1824 !important;border:1px solid #1a2540 !important;color:#4a9eff !important;font-weight:600 !important; }
[data-testid="stStatus"] { background:#0a0d14 !important;border:1px solid #1a2540 !important;border-radius:10px !important; }

/* ─ Executive summary card ─ */
.exec-card {
    background: linear-gradient(135deg, #07111e 0%, #0a0d1a 100%);
    border: 1px solid #1e3a5a;
    border-left: 4px solid #38bdf8;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.exec-card::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(56,189,248,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.exec-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}
.exec-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    color: #38bdf8;
}
.exec-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    background: rgba(56,189,248,0.08);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.25);
    letter-spacing: 0.5px;
}
.exec-text {
    font-size: 14px;
    line-height: 1.75;
    color: #9bb5cc;
    font-style: italic;
}

/* ─ Fix artifact panel ─ */
.fix-panel {
    background: rgba(56,189,248,0.03);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 12px;
}
.fix-panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}
.fix-config-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
    background: rgba(56,189,248,0.1);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.3);
    letter-spacing: 0.5px;
}
.fix-instructions {
    background: rgba(33,195,84,0.04);
    border-left: 3px solid #21c354;
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin-top: 10px;
    font-size: 12px;
    color: #6aaa7a;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

SEV_ICONS = {"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢","Informational":"🔵"}
SEV_CLASS  = {"Critical":"sev-critical","High":"sev-high","Medium":"sev-medium","Low":"sev-low","Informational":"sev-info"}

def sev_badge(severity, is_fp=False):
    if is_fp:
        return "<span class='sev-badge sev-fp'>◇ FALSE POSITIVE</span>"
    icon = SEV_ICONS.get(severity, "⚪")
    cls  = SEV_CLASS.get(severity, "sev-info")
    return f"<span class='sev-badge {cls}'>{icon} {severity.upper()}</span>"

def render_finding_card(item, show_patch_button=False):
    sev   = item.get("severity", "Informational")
    is_fp = item.get("is_false_positive", False)
    link  = item.get("link", "#")
    cat   = item.get("category", "")
    risk  = item.get("risk_summary", "No assessment available.")
    remed = item.get("remediation", "")
    fp_class  = " fp" if is_fp else ""
    cat_html  = f"<span class='cat-pill'>📂 {cat}</span>" if cat else ""
    remed_html= f"<div class='card-remediation'>🔧 <strong>Fix:</strong> {remed}</div>" if remed else ""

    st.markdown(f"""
    <div class='finding-card{fp_class}'>
        <div class='card-header'>
            <div>
                {cat_html}
                <div class='card-url'><a href='{link}' target='_blank'>{link}</a></div>
            </div>
            {sev_badge(sev, is_fp)}
        </div>
        <div class='card-section-label'>Threat Assessment</div>
        <div class='card-risk-text'>{risk}</div>
        {remed_html}
    </div>
    """, unsafe_allow_html=True)

    # ── Fix Artifact button (only for real exposures) ──────────────────────────
    if show_patch_button and not is_fp:
        btn_key = f"btn_patch_{link}"
        cached  = st.session_state.patches.get(link)

        if cached:
            # Already generated — render cached artifact
            _render_patch_artifact(cached)
        else:
            if st.button("⚡ Generate Fix Artifact", key=btn_key):
                with st.spinner("Compiling hardening rules..."):
                    patch = generate_remediation_patch(link, risk)
                    st.session_state.patches[link] = patch
                _render_patch_artifact(patch)


def _render_patch_artifact(patch: dict):
    """Render a generated DevSecOps fix artifact panel."""
    config_type = patch.get("config_type", "Config")
    snippet     = patch.get("code_snippet", "")
    instructions= patch.get("instructions", "")

    # Pick syntax lang based on config type
    lang_map = {
        "nginx": "nginx", "apache": "apacheconf",
        "robots": "text",  "cloudflare": "javascript",
    }
    lang = next((v for k, v in lang_map.items() if k in config_type.lower()), "bash")

    st.markdown(f"""
    <div class='fix-panel'>
        <div class='fix-panel-header'>
            <span style='font-size:14px;'>🛠️</span>
            <span class='fix-config-badge'>{config_type}</span>
            <span style='font-size:11px;color:#3a5a7a;font-weight:500;'>Hardening Artifact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.code(snippet, language=lang)
    if instructions:
        st.markdown(f"<div class='fix-instructions'>📌 {instructions}</div>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None
if "target_domain" not in st.session_state:
    st.session_state.target_domain = ""
if "executive_summary" not in st.session_state:
    st.session_state.executive_summary = ""
if "patches" not in st.session_state:
    st.session_state.patches = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div class='brand-icon'>🛡️</div>
        <div>
            <div class='brand-name'>BreachRadar</div>
            <div class='brand-sub'>Attack Surface Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    target_input = st.text_input(
        "TARGET DOMAIN",
        value="testphp.vulnweb.com",
        placeholder="example.com"
    ).strip().lower()

    for prefix in ("https://", "http://"):
        if target_input.startswith(prefix):
            target_input = target_input[len(prefix):]
    target_input = target_input.split("/")[0]

    scan_button = st.button("⚡  Launch Passive Scan", type="primary", use_container_width=True)

    st.markdown("""
    <div class='pipeline-card'>
        <div class='pipeline-title'>Scan Pipeline</div>
        <div class='pipeline-step'><div class='pipeline-dot dot-green'></div>SerpApi Google Dork Ingestion</div>
        <div class='pipeline-step'><div class='pipeline-dot dot-blue'></div>Gemini AI Security Triage</div>
        <div class='pipeline-step'><div class='pipeline-dot dot-purple'></div>Risk Scoring &amp; Remediation</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("🔒 Passive recon only — no active probing.")

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div class='hero-tag'><span class='pulse-dot'></span>&nbsp; AI-Powered · Passive OSINT · Zero-Touch</div>
    <div class='hero-title'>🛡️ Exposure Triage Dashboard</div>
    <div class='hero-sub'>Automated attack surface reconnaissance — footprinting, noise-filtering, and AI-generated remediation scoring</div>
</div>
""", unsafe_allow_html=True)

# ── Scan execution ────────────────────────────────────────────────────────────
if scan_button:
    if not target_input:
        st.warning("⚠️ Please enter a valid target domain.")
    else:
        st.session_state.target_domain = target_input
        st.session_state.scan_results  = None
        st.session_state.executive_summary = ""
        st.session_state.patches = {}
        with st.status(f"🔍 Scanning attack surface for `{target_input}`...", expanded=True) as status:
            st.write("📡 Executing 5 Google Dork categories via SerpApi...")
            raw_findings = scan_domain(target_input)
            st.write(f"✅ Collected **{len(raw_findings)}** raw exposure candidates.")
            if not raw_findings:
                status.update(label="✅ Recon complete — Surface is clean!", state="complete")
                st.session_state.scan_results = []
            else:
                st.write("🧠 Routing findings to Gemini for autonomous security triage...")
                triaged = triage_findings(raw_findings)
                st.session_state.scan_results = triaged
                st.write("📋 Compiling executive threat briefing...")
                st.session_state.executive_summary = generate_executive_summary(target_input, triaged)
                status.update(label=f"✅ Triage complete — {len(triaged)} findings analysed!", state="complete")

# ── Results ───────────────────────────────────────────────────────────────────
results = st.session_state.scan_results

if results is None:
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-icon'>🎯</div>
        <div class='empty-title'>Ready to Scan</div>
        <div class='empty-sub'>Enter a target domain in the sidebar and click <strong>Launch Passive Scan</strong><br>to start automated OSINT reconnaissance.</div>
    </div>
    """, unsafe_allow_html=True)

elif len(results) == 0:
    domain = st.session_state.target_domain
    st.markdown(f"""
    <div class='all-clear'>
        <div class='all-clear-icon'>✅</div>
        <div class='all-clear-title'>No Exposures Detected</div>
        <div class='all-clear-sub'>Google returned zero footprints for <code>{domain}</code>. No leaked configs, admin portals, or sensitive files found.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    total_hits  = len(results)
    real_risks  = [r for r in results if not r.get("is_false_positive")]
    false_pos   = [r for r in results if r.get("is_false_positive")]
    critical_hi = [r for r in real_risks if r.get("severity") in ("Critical", "High")]

    # ── Executive CISO Summary Card ─────────────────────────────────────────
    exec_summary = st.session_state.executive_summary
    if exec_summary:
        domain_display = st.session_state.target_domain
        st.markdown(f"""
        <div class='exec-card'>
            <div class='exec-header'>
                <span style='font-size:18px;'>🧠</span>
                <span class='exec-label'>AI Executive Threat Briefing</span>
                <span class='exec-badge'>&#x25cf; CISO · {domain_display}</span>
            </div>
            <div class='exec-text'>{exec_summary}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='kpi-grid'>
        <div class='kpi-card total'>
            <div class='kpi-label'>Total Findings</div>
            <div class='kpi-value'>{total_hits:02d}</div>
            <div class='kpi-sub'>Raw indexed results</div>
        </div>
        <div class='kpi-card risk'>
            <div class='kpi-label'>Actionable Risks</div>
            <div class='kpi-value'>{len(real_risks):02d}</div>
            <div class='kpi-sub'>Confirmed exposures</div>
        </div>
        <div class='kpi-card critical'>
            <div class='kpi-label'>Critical / High</div>
            <div class='kpi-value'>{len(critical_hi):02d}</div>
            <div class='kpi-sub'>Urgent attention needed</div>
        </div>
        <div class='kpi-card noise'>
            <div class='kpi-label'>Noise Filtered</div>
            <div class='kpi-value'>{len(false_pos):02d}</div>
            <div class='kpi-sub'>False positives removed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_action, tab_all, tab_raw = st.tabs([
        f"🚨  Actionable  ({len(real_risks)})",
        f"📋  All Findings  ({total_hits})",
        "💾  Raw JSON & Export"
    ])

    with tab_action:
        if not real_risks:
            st.markdown("<div class='empty-state'><div class='empty-icon'>🎉</div><div class='empty-title'>No Actionable Risks</div><div class='empty-sub'>All findings were classified as false positives or informational only.</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='section-header'><span class='section-title'>Confirmed Exposures</span><span class='section-count'>{len(real_risks)} findings</span></div>", unsafe_allow_html=True)
            for item in real_risks:
                render_finding_card(item, show_patch_button=True)

    with tab_all:
        st.markdown(f"<div class='section-header'><span class='section-title'>All Indexed Findings</span><span class='section-count'>{total_hits} total</span></div>", unsafe_allow_html=True)
        for item in results:
            render_finding_card(item)

    with tab_raw:
        col_json, col_export = st.columns([3, 1])
        with col_json:
            st.json(results)
        with col_export:
            st.markdown("<br>", unsafe_allow_html=True)
            df = pd.DataFrame(results)
            st.download_button(
                label="📥  Export CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"breachradar_{st.session_state.target_domain}_report.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption(f"**Target:** `{st.session_state.target_domain}`  \n**Findings:** {total_hits}  \n**Risks:** {len(real_risks)}")
