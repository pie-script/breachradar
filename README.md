# 🛡️ BreachRadar — AI Attack Surface Reconnaissance & Triage

Autonomous passive OSINT and exposure triage agent powered by **SerpApi Search Intelligence** and **Google Gemini AI**.

---

## 📁 Project Structure

```text
breachradar/
├── backend/                       # 🚀 FastAPI Backend & OSINT Intelligence Core
│   ├── main.py                    # REST API endpoints (/api/scan, /api/patch)
│   ├── scanner.py                 # SerpApi Google Dork Reconnaissance Engine
│   ├── triage.py                  # Google Gemini AI Triage & Fix Generator
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Local secrets (SERPAPI_API_KEY, GEMINI_API_KEY)
│
├── frontend/                      # ⚡ React 18 + Vite Web Dashboard
│   ├── src/
│   │   ├── components/            # UI components (DefenderShield, Hero, Cards...)
│   │   ├── api.js                 # Backend API client
│   │   ├── App.jsx                # Main dashboard application
│   │   ├── index.css              # High-contrast cybersecurity theme
│   │   └── main.jsx               # React DOM entrypoint
│   ├── index.html
│   ├── vite.config.js
│   └── package.json               # Frontend dependencies
│
├── scripts/                       # 🛠️ CLI Utilities & Test Scripts
│   ├── run_pipeline.py            # Terminal-based passive OSINT pipeline test
│   └── verify_connection.py       # SerpApi connection validator
│
├── streamlit/                     # 📊 Alternative Streamlit Python Dashboard
│   └── app.py                     # Standalone all-in-one Streamlit SOC dashboard
│
├── .gitignore                     # Git ignore rules for Python, Node, and secrets
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start

### Option A: Modern React + FastAPI Stack (Recommended)

#### 1. Start the Backend (Terminal 1)
```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
* API runs at `http://localhost:8000`.
* Interactive API Docs (Swagger UI): `http://localhost:8000/docs`.

#### 2. Start the Frontend (Terminal 2)
```powershell
cd frontend
npm install
npm run dev
```
* Web Dashboard runs at `http://localhost:5173`.

---

### Option B: Streamlit Python Dashboard

If you prefer running the single-file Streamlit dashboard:

```powershell
cd streamlit
streamlit run app.py
```
* Dashboard runs at `http://localhost:8501`.

---

### Option C: Standalone CLI Test Scripts

Run a quick passive reconnaissance scan and Gemini triage directly in your console:

```powershell
# Test SerpApi connection
python scripts/verify_connection.py

# Run end-to-end passive scan & triage against a test target
python scripts/run_pipeline.py
```

---

## 🔒 Security Notice

BreachRadar performs **passive reconnaissance only** using Google Search Intelligence via SerpApi. It executes zero active packet probing, port scanning, or intrusive testing against target servers.
