import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

import streamlit as st
import pandas as pd
from collections import Counter
from html import escape
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

/* ─ Base ─ */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ─ Sidebar ─ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b12 0%, #0b0f1a 100%) !important;
    border-right: 1px solid #141c2e !important;
}
[data-testid="stSidebar"] * { color: #c9d1e0 !important; }

.sidebar-brand { display:flex;align-items:center;gap:12px;padding:4px 0 16px 0;border-bottom:1px solid #141c2e;margin-bottom:20px; }
.brand-icon { width:38px;height:38px;background:linear-gradient(135deg,#e63946,#c1121f);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 0 18px rgba(230,57,70,0.45);flex-shrink:0; }
.brand-name { font-size:20px;font-weight:800;letter-spacing:-0.5px;background:linear-gradient(90deg,#e63946,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.brand-sub { font-size:10px;color:#3a4a60 !important;letter-spacing:1px;text-transform:uppercase;margin-top:1px;font-weight:500; }

/* ─ Pipeline tracker ─ */
.pipeline-card { background:#0a0e18;border:1px solid #141c2e;border-radius:12px;padding:16px;margin-top:16px; }
.pipeline-title { font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#3a5a80 !important;font-weight:700;margin-bottom:14px; }
.pipeline-step { display:flex;align-items:center;gap:10px;padding:6px 0;font-size:12px;font-weight:500; }
.pipeline-step.pending { color:#2a3a50 !important; }
.pipeline-step.complete { color:#21c354 !important; }
.step-icon { width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0; }
.step-icon.pending { background:#0e1420;border:1px dashed #1a2a40;color:#2a3a50; }
.step-icon.complete { background:rgba(33,195,84,0.12);border:1px solid rgba(33,195,84,0.4);color:#21c354; }
.step-label { flex:1; }
.step-tag { font-size:9px;padding:1px 6px;border-radius:10px;font-weight:600;letter-spacing:0.5px; }
.step-tag.pending { background:#0e1420;color:#1a2a40; }
.step-tag.complete { background:rgba(33,195,84,0.08);color:#21c354; }

/* ─ Hero ─ */
.hero-header { background:linear-gradient(135deg,#080b12 0%,#0b1222 50%,#0e0a18 100%);border:1px solid #141c2e;border-radius:16px;padding:28px 32px 24px;margin-bottom:24px;position:relative;overflow:hidden; }
.hero-header::before { content:'';position:absolute;top:-50px;right:-50px;width:250px;height:250px;background:radial-gradient(circle,rgba(230,57,70,0.06) 0%,transparent 70%);border-radius:50%; }
.hero-header::after { content:'';position:absolute;bottom:-80px;left:20%;width:350px;height:350px;background:radial-gradient(circle,rgba(74,158,255,0.03) 0%,transparent 70%);border-radius:50%; }
.hero-tag { display:inline-flex;align-items:center;gap:5px;background:rgba(230,57,70,0.08);border:1px solid rgba(230,57,70,0.25);color:#e63946 !important;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:600;letter-spacing:0.5px;margin-bottom:12px; }
.pulse-dot { width:6px;height:6px;background:#e63946;border-radius:50%;display:inline-block;animation:pulse 2s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(230,57,70,0.6)} 70%{box-shadow:0 0 0 7px rgba(230,57,70,0)} 100%{box-shadow:0 0 0 0 rgba(230,57,70,0)} }
.hero-title { font-size:30px;font-weight:800;letter-spacing:-0.8px;margin:0 0 6px 0;background:linear-gradient(90deg,#fff 0%,#c9d1e0 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;position:relative;z-index:1; }
.hero-sub { font-size:14px;color:#3a5a80;margin:0 0 20px 0;font-weight:400;position:relative;z-index:1; }

/* ─ Workflow pipeline ─ */
.workflow { display:flex;align-items:center;justify-content:flex-start;gap:0;flex-wrap:wrap;position:relative;z-index:1; }
.wf-node { display:flex;align-items:center;gap:8px;background:#0a0e18;border:1px solid #141c2e;border-radius:10px;padding:8px 14px;transition:all 0.2s ease; }
.wf-node:hover { border-color:#1e2d45;transform:translateY(-1px); }
.wf-icon { font-size:16px;flex-shrink:0; }
.wf-text { font-size:11px;font-weight:600;color:#5a7a9a;letter-spacing:0.3px; }
.wf-arrow { color:#1a2a40;font-size:16px;margin:0 8px;font-weight:300; }
.wf-serpapi { border-color:rgba(74,158,255,0.2);background:rgba(74,158,255,0.04); }
.wf-serpapi .wf-text { color:#4a9eff; }

/* ─ Radar animation ─ */
@keyframes radarSweep { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
@keyframes radarPulse { 0%,100%{opacity:0.12;transform:scale(1)} 50%{opacity:0.28;transform:scale(1.03)} }
@keyframes breathe { 0%,100%{opacity:0.5} 50%{opacity:1} }
.radar-wrap { text-align:center;padding:40px 0 10px; }
.radar-container { position:relative;width:180px;height:180px;margin:0 auto 20px; }
.radar-ring { position:absolute;border:1px solid rgba(230,57,70,0.12);border-radius:50%; }
.radar-ring.r1 { width:180px;height:180px;top:0;left:0;animation:radarPulse 3s ease-in-out infinite; }
.radar-ring.r2 { width:120px;height:120px;top:30px;left:30px;animation:radarPulse 3s ease-in-out 0.5s infinite; }
.radar-ring.r3 { width:60px;height:60px;top:60px;left:60px;animation:radarPulse 3s ease-in-out 1s infinite; }
.radar-center { position:absolute;width:10px;height:10px;background:#e63946;border-radius:50%;top:85px;left:85px;box-shadow:0 0 14px rgba(230,57,70,0.5); }
.radar-sweep { position:absolute;width:90px;height:2px;top:90px;left:90px;transform-origin:0 0;background:linear-gradient(90deg,rgba(230,57,70,0.5),transparent);animation:radarSweep 3s linear infinite; }
.radar-label { font-size:14px;font-weight:600;color:#2a3a50;animation:breathe 3s ease-in-out infinite;margin-bottom:8px; }
.radar-sublabel { font-size:11px;color:#1a2a3a; }

/* ─ Ghost KPI ─ */
.ghost-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:560px;margin:24px auto 0; }
.ghost-card { background:transparent;border:1px dashed #141c2e;border-radius:12px;padding:16px;text-align:center;opacity:0.35; }
.ghost-label { font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#1a2a3a;font-weight:600;margin-bottom:6px; }
.ghost-value { font-size:26px;font-weight:800;color:#141c2e;font-family:'JetBrains Mono',monospace; }

/* ─ SerpApi badge ─ */
.serpapi-badge { display:inline-flex;align-items:center;gap:5px;background:rgba(74,158,255,0.06);border:1px solid rgba(74,158,255,0.15);border-radius:20px;padding:3px 10px;font-size:10px;font-weight:600;color:#4a9eff;letter-spacing:0.3px;margin-top:14px; }

/* ─ KPI Grid ─ */
.kpi-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px; }
.kpi-card { background:#080b12;border:1px solid #141c2e;border-radius:14px;padding:20px;position:relative;overflow:hidden;transition:all 0.2s ease; }
.kpi-card:hover { border-color:#1e2d45;box-shadow:0 4px 20px rgba(0,0,0,0.3);transform:translateY(-1px); }
.kpi-card::before { content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:14px 14px 0 0; }
.kpi-card.total::before  { background:linear-gradient(90deg,#4a9eff,#00d4ff); }
.kpi-card.risk::before   { background:linear-gradient(90deg,#e63946,#ff6b6b); }
.kpi-card.critical::before { background:linear-gradient(90deg,#ff4b4b,#ff8800); }
.kpi-card.noise::before  { background:linear-gradient(90deg,#21c354,#00b4d8); }
.kpi-icon { font-size:20px;margin-bottom:10px; }
.kpi-label { font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#3a5a80;font-weight:600;margin-bottom:10px; }
.kpi-value { font-size:42px;font-weight:800;letter-spacing:-2px;line-height:1;font-family:'JetBrains Mono',monospace;margin-bottom:6px; }
.kpi-card.total .kpi-value   { color:#4a9eff; }
.kpi-card.risk .kpi-value    { color:#e63946; }
.kpi-card.critical .kpi-value { color:#ff8800; }
.kpi-card.noise .kpi-value   { color:#21c354; }
.kpi-sub { font-size:10px;color:#2a3a50;font-weight:500; }
.kpi-bar { height:3px;background:#0e1420;border-radius:2px;margin-top:10px;overflow:hidden; }
.kpi-bar-fill { height:100%;border-radius:2px;transition:width 0.5s ease; }

/* ─ Severity badges ─ */
.sev-badge { display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase; }
.sev-critical { background:rgba(255,75,75,0.1);color:#ff4b4b;border:1px solid rgba(255,75,75,0.35); }
.sev-high     { background:rgba(255,136,0,0.1);color:#ff8800;border:1px solid rgba(255,136,0,0.35); }
.sev-medium   { background:rgba(255,200,0,0.1);color:#ffcc00;border:1px solid rgba(255,200,0,0.35); }
.sev-low      { background:rgba(33,195,84,0.1);color:#21c354;border:1px solid rgba(33,195,84,0.35); }
.sev-info     { background:rgba(74,158,255,0.1);color:#4a9eff;border:1px solid rgba(74,158,255,0.35); }
.sev-fp       { background:rgba(100,100,100,0.08);color:#5a6a7a;border:1px solid rgba(100,100,100,0.25); }

/* ─ Category & source pills ─ */
.cat-pill { display:inline-block;padding:3px 9px;border-radius:5px;font-size:10px;font-weight:600;letter-spacing:0.5px;background:rgba(74,158,255,0.06);color:#4a9eff;border:1px solid rgba(74,158,255,0.15);margin-right:6px; }
.src-pill { display:inline-block;padding:3px 9px;border-radius:5px;font-size:10px;font-weight:600;letter-spacing:0.5px;background:rgba(74,158,255,0.04);color:#3a6a90;border:1px solid rgba(74,158,255,0.1); }

/* ─ Finding cards ─ */
.finding-card { background:#070a10;border:1px solid #121a2a;border-radius:14px;padding:0;margin-bottom:12px;transition:all 0.2s ease;position:relative;overflow:hidden; }
.finding-card:hover { border-color:#1e2d45;box-shadow:0 4px 24px rgba(0,0,0,0.35);transform:translateY(-1px); }
.finding-card.fp { opacity:0.55; }
.finding-card .sev-bar { position:absolute;top:0;left:0;bottom:0;width:3px; }
.sev-bar-critical { background:#ff4b4b; }
.sev-bar-high     { background:#ff8800; }
.sev-bar-medium   { background:#ffcc00; }
.sev-bar-low      { background:#21c354; }
.sev-bar-info     { background:#4a9eff; }
.sev-bar-fp       { background:#2a3a4a; }
.finding-card .card-inner { padding:18px 20px 18px 22px; }
.finding-card .card-header { display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:10px;flex-wrap:wrap; }
.card-pills { display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:8px; }
.card-url { font-family:'JetBrains Mono',monospace;font-size:13px;color:#5a8ab4;word-break:break-all;flex:1; }
.card-url a { color:#5a8ab4 !important;text-decoration:none;transition:color 0.2s; }
.card-url a:hover { color:#4a9eff !important;text-decoration:underline; }
.card-section-label { font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#1e2d45;font-weight:700;margin:12px 0 5px 0; }
.card-risk-text { font-size:13px;color:#6a8aaa;line-height:1.65; }
.card-remediation { background:rgba(33,195,84,0.04);border:1px solid rgba(33,195,84,0.1);border-left:3px solid #21c354;border-radius:0 8px 8px 0;padding:10px 14px;margin-top:12px;font-size:12px;color:#5a9a6a;line-height:1.5; }
.card-query { font-family:'JetBrains Mono',monospace;font-size:10px;color:#2a3a50;background:#080c14;border:1px solid #101820;border-radius:6px;padding:6px 10px;margin-top:8px;word-break:break-all; }

/* ─ Section headers ─ */
.section-header { display:flex;align-items:center;gap:10px;margin:4px 0 16px 0;padding-bottom:12px;border-bottom:1px solid #101820; }
.section-title { font-size:16px;font-weight:700;color:#c9d1e0; }
.section-count { background:#101820;color:#4a9eff;border-radius:20px;padding:2px 10px;font-size:12px;font-weight:600; }

/* ─ Empty / All clear ─ */
.empty-state { text-align:center;padding:50px 20px;color:#1a2a3a; }
.empty-state .empty-icon { font-size:48px;margin-bottom:12px; }
.empty-state .empty-title { font-size:18px;font-weight:600;color:#2a4a60;margin-bottom:6px; }
.empty-state .empty-sub { font-size:13px;color:#1a2a3a; }
.all-clear { background:linear-gradient(135deg,rgba(33,195,84,0.04),rgba(0,180,216,0.04));border:1px solid rgba(33,195,84,0.15);border-radius:16px;padding:40px;text-align:center; }
.all-clear-icon { font-size:52px;margin-bottom:12px; }
.all-clear-title { font-size:22px;font-weight:700;color:#21c354;margin-bottom:8px; }
.all-clear-sub { font-size:14px;color:#3a6a50; }

/* ─ Executive card ─ */
.exec-card { background:linear-gradient(135deg,#070a14 0%,#080c18 100%);border:1px solid #142030;border-left:4px solid #38bdf8;border-radius:14px;padding:20px 24px;margin-bottom:20px;position:relative;overflow:hidden; }
.exec-card::before { content:'';position:absolute;top:-30px;right:-30px;width:150px;height:150px;background:radial-gradient(circle,rgba(56,189,248,0.05) 0%,transparent 70%);border-radius:50%; }
.exec-header { display:flex;align-items:center;gap:8px;margin-bottom:12px; }
.exec-label { font-size:10px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;color:#38bdf8; }
.exec-badge { display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:600;background:rgba(56,189,248,0.06);color:#38bdf8;border:1px solid rgba(56,189,248,0.2);letter-spacing:0.5px; }
.exec-text { font-size:14px;line-height:1.75;color:#7a9ab8;font-style:italic;position:relative;z-index:1; }

/* ─ Fix artifact panel ─ */
.fix-panel { background:rgba(56,189,248,0.03);border:1px solid rgba(56,189,248,0.1);border-radius:10px;padding:14px 16px;margin-top:12px; }
.fix-panel-header { display:flex;align-items:center;gap:8px;margin-bottom:10px; }
.fix-config-badge { display:inline-block;padding:3px 10px;border-radius:5px;font-size:11px;font-weight:700;background:rgba(56,189,248,0.08);color:#38bdf8;border:1px solid rgba(56,189,248,0.25);letter-spacing:0.5px; }
.fix-instructions { background:rgba(33,195,84,0.03);border-left:3px solid #21c354;border-radius:0 6px 6px 0;padding:8px 12px;margin-top:10px;font-size:12px;color:#5a9a6a;line-height:1.5; }

/* ─ Tab overrides ─ */
[data-testid="stTabs"] [data-baseweb="tab-list"] { background:transparent !important;border-bottom:1px solid #101820 !important;gap:4px !important; }
[data-testid="stTabs"] [data-baseweb="tab"] { background:transparent !important;color:#3a5a80 !important;font-size:13px !important;font-weight:500 !important;padding:8px 16px !important;border-radius:8px 8px 0 0 !important; }
[data-testid="stTabs"] [aria-selected="true"] { background:#0a0e18 !important;color:#c9d1e0 !important;border-bottom:2px solid #e63946 !important; }

/* ─ Scrollbar ─ */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#080b12; }
::-webkit-scrollbar-thumb { background:#141c2e;border-radius:3px; }

/* ─ Input ─ */
[data-testid="stTextInput"] input { background:#080b12 !important;border-color:#141c2e !important;color:#c9d1e0 !important;font-family:'JetBrains Mono',monospace !important;font-size:13px !important;border-radius:8px !important; }
[data-testid="stTextInput"] input:focus { border-color:#e63946 !important;box-shadow:0 0 0 2px rgba(230,57,70,0.12) !important; }

/* ─ Button: Glowing CTA ─ */
@keyframes glowPulse { 0%,100%{box-shadow:0 4px 16px rgba(230,57,70,0.3)} 50%{box-shadow:0 4px 28px rgba(230,57,70,0.5)} }
[data-testid="stButton"] > button[kind="primary"] { background:linear-gradient(135deg,#c1121f,#e63946) !important;border:none !important;font-weight:700 !important;letter-spacing:0.3px !important;animation:glowPulse 3s ease-in-out infinite !important;transition:all 0.2s !important; }
[data-testid="stButton"] > button[kind="primary"]:hover { box-shadow:0 6px 32px rgba(230,57,70,0.6) !important;transform:translateY(-2px) !important; }
[data-testid="stDownloadButton"] > button { background:#0a0e18 !important;border:1px solid #141c2e !important;color:#4a9eff !important;font-weight:600 !important;border-radius:8px !important; }
[data-testid="stStatus"] { background:#080b12 !important;border:1px solid #141c2e !important;border-radius:12px !important; }

/* ─ Footer ─ */
.br-footer { text-align:center;padding:32px 0 16px;margin-top:24px;border-top:1px solid #0e1420; }
.br-footer-text { font-size:11px;color:#1a2a3a;font-weight:500;letter-spacing:0.3px; }
.br-footer-text strong { color:#2a4a60; }

/* ─ Background glow ─ */
.stMainBlockContainer { background:radial-gradient(ellipse at 50% 0%,rgba(230,57,70,0.015) 0%,transparent 60%) !important; }

/* ─ Enterprise analytics layer ─ */
.analytics-shell { background:linear-gradient(145deg,#080c14,#0a101c);border:1px solid #142238;border-radius:16px;padding:20px;margin:0 0 22px;box-shadow:0 16px 50px rgba(0,0,0,.18); }
.analytics-header { display:flex;align-items:flex-start;justify-content:space-between;gap:18px;margin-bottom:18px; }
.analytics-kicker { color:#4a9eff;font-size:10px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:5px; }
.analytics-title { color:#e7eef8;font-size:20px;font-weight:750;letter-spacing:-.4px; }
.analytics-subtitle { color:#56718d;font-size:12px;margin-top:4px; }
.posture-box { min-width:175px;text-align:right; }
.posture-label { color:#5d7894;font-size:10px;text-transform:uppercase;letter-spacing:1px;font-weight:700; }
.posture-score { color:#ff8800;font:800 30px 'JetBrains Mono',monospace;line-height:1.1;margin-top:3px; }
.posture-track { height:6px;background:#111b2b;border-radius:8px;margin-top:8px;overflow:hidden; }
.posture-fill { height:100%;border-radius:8px;background:linear-gradient(90deg,#21c354,#ffcc00,#ff4b4b); }
.stat-strip { display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px; }
.mini-stat { background:#070b13;border:1px solid #142238;border-radius:10px;padding:12px 14px; }
.mini-stat-label { color:#4e6b87;font-size:9px;letter-spacing:1px;text-transform:uppercase;font-weight:700; }
.mini-stat-value { color:#d7e4f2;font:700 20px 'JetBrains Mono',monospace;margin-top:5px; }
.mini-stat-note { color:#3f5b76;font-size:10px;margin-top:3px; }
.chart-card { background:#070b13;border:1px solid #142238;border-radius:12px;padding:14px 16px;min-height:235px; }
.chart-title { color:#a9bfd4;font-size:12px;font-weight:700;margin-bottom:3px; }
.chart-caption { color:#3f5b76;font-size:10px;margin-bottom:10px; }
.insight-card { background:linear-gradient(135deg,rgba(230,57,70,.08),rgba(74,158,255,.04));border:1px solid rgba(230,57,70,.16);border-radius:11px;padding:13px 15px;margin-top:14px;color:#88a5bd;font-size:12px;line-height:1.55; }
.insight-card strong { color:#e5edf6; }
.filter-row { background:#080d17;border:1px solid #142238;border-radius:11px;padding:12px 14px;margin-bottom:15px; }

/* ─ Hero stat cards (gradient) ─ */
.hero-stat-row { display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px; }
.hero-stat-card { border-radius:14px;padding:18px 20px;position:relative;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.25); }
.hero-stat-card.urgent { background:linear-gradient(135deg,#c1121f 0%,#e63946 55%,#ff6b6b 100%); }
.hero-stat-card.quality { background:linear-gradient(135deg,#0b3d91 0%,#1e6fd9 55%,#4a9eff 100%); }
.hero-stat-icon { font-size:18px;opacity:.85;margin-bottom:6px; }
.hero-stat-label { font-size:11px;text-transform:uppercase;letter-spacing:1px;font-weight:700;color:rgba(255,255,255,.85); }
.hero-stat-value { font:800 36px 'JetBrains Mono',monospace;color:#fff;letter-spacing:-1px;margin:6px 0 4px; }
.hero-stat-sub { display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:#fff;background:rgba(255,255,255,.16);border-radius:20px;padding:3px 10px; }

/* ─ Donut chart (CSS conic-gradient) ─ */
.donut-wrap { display:flex;align-items:center;gap:20px; }
.donut-chart { width:140px;height:140px;border-radius:50%;position:relative;flex-shrink:0; }
.donut-hole { position:absolute;inset:18px;background:#070b13;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center; }
.donut-hole-value { font:800 22px 'JetBrains Mono',monospace;color:#d7e4f2;line-height:1; }
.donut-hole-label { font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#4e6b87;margin-top:3px; }
.donut-legend { display:flex;flex-direction:column;gap:8px;flex:1; }
.legend-item { display:flex;align-items:center;gap:8px;font-size:12px;color:#a9bfd4; }
.legend-dot { width:9px;height:9px;border-radius:50%;flex-shrink:0; }
.legend-count { margin-left:auto;font:700 12px 'JetBrains Mono',monospace;color:#d7e4f2; }

/* ─ Horizontal mini bars (category breakdown) ─ */
.hbar-list { display:flex;flex-direction:column;gap:10px;padding-top:2px; }
.hbar-row { display:flex;align-items:center;gap:10px; }
.hbar-label { width:112px;font-size:11px;color:#88a5bd;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0; }
.hbar-track { flex:1;height:8px;background:#111b2b;border-radius:6px;overflow:hidden; }
.hbar-fill { height:100%;border-radius:6px;background:linear-gradient(90deg,#4a9eff,#00d4ff); }
.hbar-value { width:26px;text-align:right;font:700 11px 'JetBrains Mono',monospace;color:#5d7894;flex-shrink:0; }

@media (max-width: 800px) { .stat-strip { grid-template-columns:repeat(2,1fr); } .analytics-header { flex-direction:column; } .posture-box { text-align:left; } .hero-stat-row { grid-template-columns:1fr; } }

/* ─ Premium workspace chrome ─ */
[data-testid="stAppViewContainer"] { background:#05070c !important; }
[data-testid="stHeader"] { background:rgba(5,7,12,0.86) !important; }
[data-testid="stSidebar"] { width:300px !important; }
.workspace-bar { display:flex;align-items:center;justify-content:space-between;gap:16px;margin:0 0 14px;padding:10px 14px;background:rgba(10,14,24,0.72);border:1px solid #121d30;border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,0.12); }
.workspace-context,.workspace-target { display:flex;align-items:center;gap:8px;font-size:10px;letter-spacing:1.2px;font-weight:700;color:#56718d; }
.workspace-target { letter-spacing:.4px;font-weight:500;color:#7894ae; }
.workspace-label { color:#35516c;font-size:9px;letter-spacing:1.2px;font-weight:700; }
.workspace-target code { color:#c9d1e0;background:#080c14;border:1px solid #172338;border-radius:6px;padding:5px 9px;font-family:'JetBrains Mono',monospace;font-size:11px; }
.workspace-lock { opacity:.55; }
.status-dot { width:7px;height:7px;border-radius:50%;background:#21c354;box-shadow:0 0 0 4px rgba(33,195,84,.1),0 0 12px rgba(33,195,84,.55); }
.hero-header { box-shadow:0 18px 50px rgba(0,0,0,.18); }
.kpi-card { box-shadow:inset 0 1px 0 rgba(255,255,255,.015); }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color:#dbe7f3; }
[data-testid="stExpander"] { background:#080c14 !important;border:1px solid #141c2e !important;border-radius:12px !important; }
[data-testid="stDataFrame"] { border:1px solid #141c2e;border-radius:12px;overflow:hidden; }
@media (max-width: 900px) {
  .workspace-bar { align-items:flex-start; flex-direction:column; }
  .hero-header { padding:22px 20px 20px; }
  .hero-title { font-size:25px; }
  .workflow { gap:6px; }
  .wf-arrow { margin:0 2px; }
  .kpi-grid { grid-template-columns:repeat(2,1fr); }
}
@media (max-width: 600px) {
  .kpi-grid { grid-template-columns:1fr; }
  .workflow { display:grid; grid-template-columns:1fr; }
  .wf-arrow { display:none; }
  .wf-node { justify-content:center; }
}

</style>
""", unsafe_allow_html=True)


# ── Constants & Helpers ───────────────────────────────────────────────────────
SEV_ICONS = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢", "Informational": "🔵"}
SEV_CLASS = {"Critical": "sev-critical", "High": "sev-high", "Medium": "sev-medium", "Low": "sev-low", "Informational": "sev-info"}
SEV_BAR = {"Critical": "sev-bar-critical", "High": "sev-bar-high", "Medium": "sev-bar-medium", "Low": "sev-bar-low", "Informational": "sev-bar-info"}


def sev_badge(severity, is_fp=False):
    if is_fp:
        return "<span class='sev-badge sev-fp'>◇ FALSE POSITIVE</span>"
    icon = SEV_ICONS.get(severity, "⚪")
    cls = SEV_CLASS.get(severity, "sev-info")
    return f"<span class='sev-badge {cls}'>{icon} {severity.upper()}</span>"


def render_finding_card(item, show_patch_button=False):
    sev = item.get("severity", "Informational")
    is_fp = item.get("is_false_positive", False)
    link = str(item.get("link", "#"))
    cat = str(item.get("category", ""))
    risk = str(item.get("risk_summary", "No assessment available."))
    remed = str(item.get("remediation", ""))
    query = str(item.get("query_used", ""))
    safe_link = escape(link, quote=True)
    safe_cat = escape(cat)
    safe_risk = escape(risk)
    safe_remed = escape(remed)
    safe_query = escape(query)

    fp_class = " fp" if is_fp else ""
    bar_cls = "sev-bar-fp" if is_fp else SEV_BAR.get(sev, "sev-bar-info")

    pills = ""
    if cat:
        pills += f"<span class='cat-pill'>📂 {safe_cat}</span>"
    pills += "<span class='src-pill'>🔍 SerpApi</span>"

    remed_html = f"<div class='card-remediation'>🔧 <strong>Fix:</strong> {safe_remed}</div>" if remed else ""
    query_html = f"<div class='card-section-label'>Dork Query</div><div class='card-query'>{safe_query}</div>" if query else ""

    st.markdown(f"""
    <div class='finding-card{fp_class}'>
        <div class='sev-bar {bar_cls}'></div>
        <div class='card-inner'>
            <div class='card-header'>
                <div>
                    <div class='card-pills'>{pills}</div>
                    <div class='card-url'><a href='{safe_link}' target='_blank' rel='noopener noreferrer'>{safe_link}</a></div>
                </div>
                {sev_badge(sev, is_fp)}
            </div>
            <div class='card-section-label'>Threat Assessment</div>
            <div class='card-risk-text'>{safe_risk}</div>
            {remed_html}
            {query_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fix Artifact button (real exposures only)
    if show_patch_button and not is_fp:
        btn_key = f"btn_patch_{link}"
        cached = st.session_state.patches.get(link)
        if cached:
            _render_patch_artifact(cached)
        else:
            if st.button("⚡ Generate Fix Artifact", key=btn_key):
                with st.spinner("Compiling hardening rules..."):
                    patch = generate_remediation_patch(link, risk)
                    st.session_state.patches[link] = patch
                _render_patch_artifact(patch)


def _render_patch_artifact(patch):
    config_type = patch.get("config_type", "Config")
    snippet = patch.get("code_snippet", "")
    instructions = patch.get("instructions", "")
    lang_map = {"nginx": "nginx", "apache": "apacheconf", "robots": "text", "cloudflare": "javascript"}
    lang = next((v for k, v in lang_map.items() if k in config_type.lower()), "bash")
    st.markdown(f"""
    <div class='fix-panel'>
        <div class='fix-panel-header'>
            <span style='font-size:14px;'>🛠️</span>
            <span class='fix-config-badge'>{config_type}</span>
            <span style='font-size:11px;color:#2a3a50;font-weight:500;'>Hardening Artifact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.code(snippet, language=lang)
    if instructions:
        st.markdown(f"<div class='fix-instructions'>📌 {instructions}</div>", unsafe_allow_html=True)


def render_sidebar_pipeline(is_complete):
    stages = [
        ("🔍", "SerpApi Google Dork Search"),
        ("🔗", "Result Correlation"),
        ("🧠", "Gemini AI Triage"),
        ("📊", "Risk Prioritization"),
        ("📋", "Report Generation"),
    ]
    html = "<div class='pipeline-card'><div class='pipeline-title'>AI Scan Pipeline</div>"
    for icon, label in stages:
        if is_complete:
            html += f"<div class='pipeline-step complete'><div class='step-icon complete'>✓</div><span class='step-label'>{label}</span><span class='step-tag complete'>Done</span></div>"
        else:
            html += f"<div class='pipeline-step pending'><div class='step-icon pending'>{icon}</div><span class='step-label'>{label}</span><span class='step-tag pending'>Pending</span></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def enrich_results(triage_results, raw_findings):
    """Merge category, query_used, source from raw findings into triage results."""
    raw_lookup = {}
    for rf in raw_findings:
        key = rf.get("link", "")
        if key:
            raw_lookup[key] = rf
    enriched = []
    for item in triage_results:
        merged = dict(item)
        raw = raw_lookup.get(item.get("link", ""), {})
        merged.setdefault("category", raw.get("category", ""))
        merged.setdefault("query_used", raw.get("query_used", ""))
        merged.setdefault("source", raw.get("source", ""))
        enriched.append(merged)
    return enriched



def render_analytics(enriched, domain):
    """Render an executive-friendly security posture overview for demos and operations."""
    total = len(enriched)
    actionable = [x for x in enriched if not x.get("is_false_positive")]
    critical = sum(x.get("severity") == "Critical" for x in actionable)
    high = sum(x.get("severity") == "High" for x in actionable)
    medium = sum(x.get("severity") == "Medium" for x in actionable)
    low = sum(x.get("severity") == "Low" for x in actionable)
    informational = sum(x.get("severity") == "Informational" for x in enriched)
    false_positive = sum(x.get("is_false_positive", False) for x in enriched)
    # Weighted posture score: higher means healthier.
    exposure_points = critical * 30 + high * 18 + medium * 9 + low * 3
    posture = max(0, min(100, 100 - exposure_points))
    posture_color = '#21c354' if posture >= 80 else '#ffcc00' if posture >= 55 else '#ff8800' if posture >= 30 else '#ff4b4b'
    categories = Counter((x.get("category") or "Uncategorized") for x in enriched)
    top_category = categories.most_common(1)[0][0] if categories else "None"
    noise_pct = round((false_positive / max(total, 1)) * 100)
    risk_message = "No urgent exposure signals detected in this scan." if not actionable else f"{critical + high} urgent finding(s) require prioritization, led by {top_category}."

    st.markdown(f"""
    <div class='analytics-shell'>
      <div class='analytics-header'>
        <div><div class='analytics-kicker'>Executive security overview</div><div class='analytics-title'>Risk posture for {escape(domain)}</div><div class='analytics-subtitle'>A decision-ready view of the passive attack-surface assessment</div></div>
        <div class='posture-box'><div class='posture-label'>Security posture score</div><div class='posture-score' style='color:{posture_color}'>{posture}<span style='font-size:14px;color:#58738e'> / 100</span></div><div class='posture-track'><div class='posture-fill' style='width:{posture}%;background:{posture_color}'></div></div></div>
      </div>

      <div class='hero-stat-row'>
        <div class='hero-stat-card urgent'>
          <div class='hero-stat-icon'>⚠️</div>
          <div class='hero-stat-label'>Urgent Queue</div>
          <div class='hero-stat-value'>{critical + high:02d}</div>
          <div class='hero-stat-sub'>🔴 Critical + High severity</div>
        </div>
        <div class='hero-stat-card quality'>
          <div class='hero-stat-icon'>✅</div>
          <div class='hero-stat-label'>Signal Quality</div>
          <div class='hero-stat-value'>{noise_pct}%</div>
          <div class='hero-stat-sub'>🧠 AI-filtered noise</div>
        </div>
      </div>

      <div class='stat-strip'>
        <div class='mini-stat'><div class='mini-stat-label'>Exposure candidates</div><div class='mini-stat-value'>{total}</div><div class='mini-stat-note'>indexed by OSINT</div></div>
        <div class='mini-stat'><div class='mini-stat-label'>Confirmed risks</div><div class='mini-stat-value' style='color:#ff6b6b'>{len(actionable)}</div><div class='mini-stat-note'>AI-triaged actions</div></div>
        <div class='mini-stat'><div class='mini-stat-label'>Urgent queue</div><div class='mini-stat-value' style='color:#ff8800'>{critical + high}</div><div class='mini-stat-note'>critical + high</div></div>
        <div class='mini-stat'><div class='mini-stat-label'>Signal quality</div><div class='mini-stat-value' style='color:#21c354'>{noise_pct}%</div><div class='mini-stat-note'>noise filtered</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sev_segments = [
            ("Critical", critical, "#ff4b4b"), ("High", high, "#ff8800"),
            ("Medium", medium, "#ffcc00"), ("Low", low, "#21c354"),
            ("Informational", informational, "#4a9eff"),
        ]
        sev_total = sum(v for _, v, _ in sev_segments) or 1
        cum = 0.0
        stops = []
        for _, val, color in sev_segments:
            if val <= 0:
                continue
            start = cum / sev_total * 360
            cum += val
            end = cum / sev_total * 360
            stops.append(f"{color} {start:.1f}deg {end:.1f}deg")
        gradient = f"conic-gradient({', '.join(stops)})" if stops else "conic-gradient(#141c2e 0deg 360deg)"
        legend_html = "".join(
            f"<div class='legend-item'><span class='legend-dot' style='background:{color};'></span>{name}<span class='legend-count'>{val}</span></div>"
            for name, val, color in sev_segments
        )
        st.markdown(f"""
        <div class='chart-card'>
            <div class='chart-title'>Severity distribution</div>
            <div class='chart-caption'>AI classification across indexed findings</div>
            <div class='donut-wrap'>
                <div class='donut-chart' style='background:{gradient};'>
                    <div class='donut-hole'><div class='donut-hole-value'>{sev_total}</div><div class='donut-hole-label'>Findings</div></div>
                </div>
                <div class='donut-legend'>{legend_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        cat_items = categories.most_common()
        max_cat = max((v for _, v in cat_items), default=1) or 1
        bars_html = "".join(
            f"<div class='hbar-row'><div class='hbar-label'>{escape(name)}</div>"
            f"<div class='hbar-track'><div class='hbar-fill' style='width:{int(val / max_cat * 100)}%;'></div></div>"
            f"<div class='hbar-value'>{val}</div></div>"
            for name, val in cat_items
        ) or "<div class='hbar-row'><div class='hbar-label'>No categories</div></div>"
        st.markdown(f"""
        <div class='chart-card'>
            <div class='chart-title'>Exposure categories</div>
            <div class='chart-caption'>Where the attack surface is showing signals</div>
            <div class='hbar-list'>{bars_html}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'>💡 <strong>Analyst insight:</strong> {escape(risk_message)} Use the Actionable Findings queue below to generate remediation artifacts and prepare the remediation plan.</div>", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────────
for _key, _default in [
    ("scan_results", None),
    ("target_domain", ""),
    ("executive_summary", ""),
    ("patches", {}),
    ("raw_findings", []),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default


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

    is_complete = st.session_state.scan_results is not None
    render_sidebar_pipeline(is_complete)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("🔒 Passive recon only — no active probing. Zero-touch OSINT.")


# ── Workspace context ─────────────────────────────────────────────────────────
active_target = st.session_state.target_domain or "No target selected"
st.markdown(f"""
<div class='workspace-bar'>
    <div class='workspace-context'><span class='status-dot'></span><span>PASSIVE RECON WORKSPACE</span></div>
    <div class='workspace-target'><span class='workspace-label'>TARGET</span><code>{escape(active_target)}</code><span class='workspace-lock'>🔒</span></div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""

<div class='hero-header'>
    <div class='hero-tag'><span class='pulse-dot'></span>&nbsp; AI-Powered · Passive OSINT · Zero-Touch</div>
    <div class='hero-title'>🛡️ Exposure Triage Dashboard</div>
    <div class='hero-sub'>Automated attack surface reconnaissance — AI-powered footprinting, noise filtering, and remediation scoring</div>
    <div class='workflow'>
        <div class='wf-node wf-serpapi'><span class='wf-icon'>🔍</span><span class='wf-text'>SerpApi Search</span></div>
        <span class='wf-arrow'>→</span>
        <div class='wf-node'><span class='wf-icon'>🔗</span><span class='wf-text'>AI Correlation</span></div>
        <span class='wf-arrow'>→</span>
        <div class='wf-node'><span class='wf-icon'>🧠</span><span class='wf-text'>Risk Triage</span></div>
        <span class='wf-arrow'>→</span>
        <div class='wf-node'><span class='wf-icon'>📋</span><span class='wf-text'>Prioritized Findings</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Scan Execution ────────────────────────────────────────────────────────────
if scan_button:
    if not target_input:
        st.warning("⚠️ Please enter a valid target domain.")
    else:
        st.session_state.target_domain = target_input
        st.session_state.scan_results = None
        st.session_state.executive_summary = ""
        st.session_state.patches = {}
        st.session_state.raw_findings = []

        with st.status(f"🔍 Scanning attack surface for `{target_input}`...", expanded=True) as status:
            st.write("📡 **Stage 1/5** — Executing Google Dork categories via SerpApi...")
            raw_findings = scan_domain(target_input)
            st.session_state.raw_findings = raw_findings
            st.write(f"✅ Collected **{len(raw_findings)}** raw exposure candidates via SerpApi.")

            if not raw_findings:
                status.update(label="✅ Recon complete — Surface is clean!", state="complete")
                st.session_state.scan_results = []
            else:
                st.write("🔗 **Stage 2/5** — Correlating search results across dork categories...")
                st.write("🧠 **Stage 3/5** — Routing findings to Gemini AI for security triage...")
                triaged = triage_findings(raw_findings)
                st.session_state.scan_results = triaged

                st.write("📊 **Stage 4/5** — Prioritizing risks and scoring severity...")
                st.write("📋 **Stage 5/5** — Generating executive threat briefing...")
                st.session_state.executive_summary = generate_executive_summary(target_input, triaged)
                status.update(label=f"✅ Pipeline complete — {len(triaged)} findings analysed!", state="complete")


# ── Results ───────────────────────────────────────────────────────────────────
results = st.session_state.scan_results

if results is None:
    # Radar idle state with ghost KPI cards
    st.markdown("""
    <div class='radar-wrap'>
        <div class='radar-container'>
            <div class='radar-ring r1'></div>
            <div class='radar-ring r2'></div>
            <div class='radar-ring r3'></div>
            <div class='radar-center'></div>
            <div class='radar-sweep'></div>
        </div>
        <div class='radar-label'>Awaiting Target</div>
        <div class='radar-sublabel'>Enter a domain in the sidebar and launch a passive scan</div>
        <div class='ghost-grid'>
            <div class='ghost-card'>
                <div class='ghost-label'>Assets Indexed</div>
                <div class='ghost-value'>—</div>
            </div>
            <div class='ghost-card'>
                <div class='ghost-label'>Exposures Found</div>
                <div class='ghost-value'>—</div>
            </div>
            <div class='ghost-card'>
                <div class='ghost-label'>Risk Score</div>
                <div class='ghost-value'>—</div>
            </div>
        </div>
        <div class='serpapi-badge'>🔍 Powered by SerpApi Search Intelligence · Gemini AI</div>
    </div>
    """, unsafe_allow_html=True)

elif len(results) == 0:
    domain = st.session_state.target_domain
    st.markdown(f"""
    <div class='all-clear'>
        <div class='all-clear-icon'>✅</div>
        <div class='all-clear-title'>No Exposures Detected</div>
        <div class='all-clear-sub'>Google returned zero footprints for <code>{domain}</code>.<br>No leaked configs, admin portals, or sensitive files found.</div>
        <div class='serpapi-badge' style='margin-top:20px;'>🔍 Scanned via SerpApi · 5 dork categories · Zero exposures</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Enrich triage results with raw finding data (category, query_used)
    enriched = enrich_results(results, st.session_state.raw_findings)

    total_hits = len(enriched)
    real_risks = [r for r in enriched if not r.get("is_false_positive")]
    false_pos = [r for r in enriched if r.get("is_false_positive")]
    critical_hi = [r for r in real_risks if r.get("severity") in ("Critical", "High")]
    risk_pct = int((len(real_risks) / max(total_hits, 1)) * 100)

    # ── Executive analytics dashboard ──────────────────────────────────────
    render_analytics(enriched, st.session_state.target_domain)

    # ── Finding filters ────────────────────────────────────────────────────
    st.markdown("<div class='filter-row'>", unsafe_allow_html=True)
    filter_a, filter_b, filter_c = st.columns([1, 1, 1])
    with filter_a:
        severity_filter = st.multiselect("Severity", ["Critical", "High", "Medium", "Low", "Informational"], default=["Critical", "High", "Medium", "Low", "Informational"])
    with filter_b:
        category_options = sorted(set((x.get("category") or "Uncategorized") for x in enriched))
        category_filter = st.multiselect("Category", category_options, default=category_options)
    with filter_c:
        show_noise = st.checkbox("Include AI-filtered noise", value=False)
    st.markdown("</div>", unsafe_allow_html=True)
    visible = [x for x in enriched if x.get("severity", "Informational") in severity_filter and (x.get("category") or "Uncategorized") in category_filter and (show_noise or not x.get("is_false_positive"))]
    visible_real = [x for x in visible if not x.get("is_false_positive")]

    # ── Executive CISO Summary Card ───────────────────────────────────────
    exec_summary = st.session_state.executive_summary
    if exec_summary:
        domain_display = escape(st.session_state.target_domain)
        safe_summary = escape(exec_summary)
        st.markdown(f"""
        <div class='exec-card'>
            <div class='exec-header'>
                <span style='font-size:18px;'>🧠</span>
                <span class='exec-label'>AI Executive Threat Briefing</span>
                <span class='exec-badge'>&#x25cf; CISO · {domain_display}</span>
            </div>
            <div class='exec-text'>{safe_summary}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class='kpi-grid'>
        <div class='kpi-card total'>
            <div class='kpi-icon'>📡</div>
            <div class='kpi-label'>Total Findings</div>
            <div class='kpi-value'>{total_hits:02d}</div>
            <div class='kpi-sub'>via SerpApi Google Dorks</div>
        </div>
        <div class='kpi-card risk'>
            <div class='kpi-icon'>⚠️</div>
            <div class='kpi-label'>Actionable Risks</div>
            <div class='kpi-value'>{len(real_risks):02d}</div>
            <div class='kpi-sub'>Confirmed exposures</div>
            <div class='kpi-bar'><div class='kpi-bar-fill' style='width:{risk_pct}%;background:linear-gradient(90deg,#e63946,#ff6b6b);'></div></div>
        </div>
        <div class='kpi-card critical'>
            <div class='kpi-icon'>🔴</div>
            <div class='kpi-label'>Critical / High</div>
            <div class='kpi-value'>{len(critical_hi):02d}</div>
            <div class='kpi-sub'>Urgent attention needed</div>
        </div>
        <div class='kpi-card noise'>
            <div class='kpi-icon'>✅</div>
            <div class='kpi-label'>Noise Filtered</div>
            <div class='kpi-value'>{len(false_pos):02d}</div>
            <div class='kpi-sub'>AI-identified false positives</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab_action, tab_all, tab_raw = st.tabs([
        f"🚨  Actionable  ({len(visible_real)})",
        f"📋  All Findings  ({len(visible)})",
        "💾  Raw JSON & Export"
    ])

    with tab_action:
        if not visible_real:
            st.markdown("<div class='empty-state'><div class='empty-icon'>🎉</div><div class='empty-title'>No Actionable Risks</div><div class='empty-sub'>All findings were classified as false positives or informational.</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='section-header'><span class='section-title'>Confirmed Exposures</span><span class='section-count'>{len(visible_real)} findings</span></div>", unsafe_allow_html=True)
            for item in visible_real:
                render_finding_card(item, show_patch_button=True)

    with tab_all:
        st.markdown(f"<div class='section-header'><span class='section-title'>All Indexed Findings</span><span class='section-count'>{total_hits} total</span></div>", unsafe_allow_html=True)
        for item in visible:
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


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='br-footer'>
    <div class='br-footer-text'>
        Built with <strong>SerpApi</strong> Search Intelligence · <strong>Gemini AI</strong> · Streamlit
    </div>
</div>
""", unsafe_allow_html=True)