import streamlit as st
import pandas as pd
from scanner import scan_domain
from triage import triage_findings

# 1. Page Configuration
st.set_page_config(
    page_title="BreachRadar | AI Attack Surface Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling (Badges & Clean Layout)
st.markdown("""
<style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #262730;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        letter-spacing: 0.5px;
    }
    .badge-critical { background-color: #ff4b4b22; color: #ff4b4b; border: 1px solid #ff4b4b; }
    .badge-high     { background-color: #ffa50022; color: #ffa500; border: 1px solid #ffa500; }
    .badge-medium   { background-color: #ffe83822; color: #ffe838; border: 1px solid #ffe838; }
    .badge-low      { background-color: #21c35422; color: #21c354; border: 1px solid #21c354; }
    .badge-info     { background-color: #00b4d822; color: #00b4d8; border: 1px solid #00b4d8; }
    .badge-fp       { background-color: #80808022; color: #a0a0a0; border: 1px solid #808080; }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("BreachRadar")
    st.caption("AI-Powered Passive OSINT Reconnaissance")
    st.markdown("---")
    
    target_input = st.text_input(
        "Target Domain",
        value="testphp.vulnweb.com",
        placeholder="example.com"
    ).strip().lower()

    # Strip http:// or https:// if accidentally typed
    if target_input.startswith("http://"):
        target_input = target_input[7:]
    elif target_input.startswith("https://"):
        target_input = target_input[8:]
    target_input = target_input.split("/")[0]

    scan_button = st.button("🚀 Launch Passive Scan", type="primary", use_container_width=True)
    st.markdown("---")
    st.info("**Track 01: AI Agents**\n\n• Ingestion: SerpApi Google Dorks\n• Reasoning: Gemini 3.5 Flash-Lite\n• Mode: Zero-touch passive recon")

# 4. Main Panel
st.title("🛡️ Exposure Triage Dashboard")
st.markdown("Automated asset footprinting, noise-filtering, and remediation scoring.")

# Session State to hold scan data across interactions
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None
if "target_domain" not in st.session_state:
    st.session_state.target_domain = ""

if scan_button:
    if not target_input:
        st.warning("Please enter a valid target domain.")
    else:
        st.session_state.target_domain = target_input
        
        # Step A: Ingestion via SerpApi
        with st.status(f"Scanning footprint for `{target_input}`...", expanded=True) as status:
            st.write("🔍 Running automated Google Dork categories via SerpApi...")
            raw_findings = scan_domain(target_input)
            st.write(f"✅ Discovered **{len(raw_findings)}** raw index exposures.")

            if not raw_findings:
                status.update(label="Recon complete — No surface exposures indexed!", state="complete")
                st.session_state.scan_results = []
            else:
                # Step B: Gemini Autonomous Triage
                st.write("🧠 Handing off findings to Gemini for autonomous security triage...")
                triaged = triage_findings(raw_findings)
                st.session_state.scan_results = triaged
                status.update(label="Triage complete!", state="complete")

# 5. Display Results & Analytics
results = st.session_state.scan_results

if results is not None:
    if len(results) == 0:
        st.success(f"Clean report! Google search indexes returned zero exposure footprints for `{st.session_state.target_domain}`.")
    else:
        # Calculate KPI Metrics
        total_hits = len(results)
        real_risks = [r for r in results if not r.get("is_false_positive")]
        false_positives = [r for r in results if r.get("is_false_positive")]
        critical_high = [r for r in real_risks if r.get("severity") in ["Critical", "High"]]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Indexed Findings", total_hits)
        with col2:
            st.metric("Actionable Risks", len(real_risks), delta=f"{len(real_risks)} real", delta_color="inverse")
        with col3:
            st.metric("Critical / High", len(critical_high), delta=f"{len(critical_high)} urgent", delta_color="inverse")
        with col4:
            st.metric("Noise Filtered", len(false_positives), delta=f"{len(false_positives)} false alarms")

        st.markdown("---")

        # Tabbed View for Better Usability
        tab_actionable, tab_all, tab_raw = st.tabs(["🚨 Actionable Exposures", "📋 All Findings", "💾 Raw JSON"])

        def render_finding_card(item):
            sev = item.get("severity", "Low")
            is_fp = item.get("is_false_positive", False)
            badge_class = f"badge-{sev.lower()}" if not is_fp else "badge-fp"
            badge_text = f"{sev.upper()}" if not is_fp else "FALSE POSITIVE"

            with st.expander(f"[{badge_text}] {item.get('link', 'Unknown URL')}"):
                st.markdown(f"<span class='badge {badge_class}'>{badge_text}</span>", unsafe_allow_html=True)
                st.markdown(f"**Target URL:** [{item.get('link')}]({item.get('link')})")
                st.markdown(f"**Threat Assessment:**\n{item.get('risk_summary', 'No summary provided.')}")
                
                if item.get("remediation"):
                    st.info(f"**Remediation Action:**\n{item.get('remediation')}")

        with tab_actionable:
            if not real_risks:
                st.info("No actionable risks identified! All findings were classified as benign or false positives.")
            else:
                for item in real_risks:
                    render_finding_card(item)

        with tab_all:
            for item in results:
                render_finding_card(item)

        with tab_raw:
            st.json(results)
            # Export to CSV
            df = pd.DataFrame(results)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Report as CSV",
                data=csv_data,
                file_name=f"breachradar_{st.session_state.target_domain}_report.csv",
                mime="text/csv"
            )