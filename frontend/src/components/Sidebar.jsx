import DefenderShield from './DefenderShield.jsx'

const STAGES = [
  { icon: '🔍', label: 'SerpApi Google Dork Search' },
  { icon: '🔗', label: 'Result Correlation' },
  { icon: '🧠', label: 'Gemini AI Triage' },
  { icon: '📊', label: 'Risk Prioritization' },
  { icon: '📋', label: 'Report Generation' },
]

export default function Sidebar({ domain, setDomain, onScan, loading, isComplete, error }) {
  const handleSubmit = (e) => {
    e.preventDefault()
    onScan()
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">
          <DefenderShield size={24} glow={false} />
        </div>
        <div>
          <div className="brand-name">BreachRadar</div>
          <div className="brand-sub">Attack Surface Intelligence</div>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <label className="field-label" htmlFor="target-domain">Target Domain</label>
        <input
          id="target-domain"
          className="domain-input"
          type="text"
          placeholder="example.com"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          disabled={loading}
        />
        <button className="scan-btn" type="submit" disabled={loading}>
          {loading ? 'Scanning…' : '⚡ Launch Passive Scan'}
        </button>
        {error && <div className="field-error">⚠️ {error}</div>}
      </form>

      <div className="pipeline-card">
        <div className="pipeline-title">AI Scan Pipeline</div>
        {STAGES.map((stage, i) => {
          const state = isComplete ? 'complete' : loading ? 'active' : 'pending'
          const tag = isComplete ? 'Done' : loading ? 'Running' : 'Pending'
          return (
            <div key={i} className={`pipeline-step ${state}`}>
              <div className={`step-icon ${state}`}>{state === 'complete' ? '✓' : stage.icon}</div>
              <span className="step-label">{stage.label}</span>
              <span className={`step-tag ${state}`}>{tag}</span>
            </div>
          )
        })}
      </div>

      <div className="sidebar-note">🔒 Passive recon only — no active probing. Zero-touch OSINT.</div>
    </aside>
  )
}
