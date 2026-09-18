import DefenderShield from './DefenderShield.jsx'

export default function Hero() {
  return (
    <div className="hero-header">
      <div className="hero-tag">
        <span className="pulse-dot" />
        &nbsp; AI-Powered · Passive OSINT · Zero-Touch
      </div>
      <div className="hero-title" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <DefenderShield size={32} />
        <span>Exposure Triage Dashboard</span>
      </div>
      <div className="hero-sub">
        Automated attack surface reconnaissance — AI-powered footprinting, noise filtering, and remediation scoring
      </div>
      <div className="workflow">
        <div className="wf-node wf-serpapi">
          <span className="wf-icon">🔍</span>
          <span className="wf-text">SerpApi Search</span>
        </div>
        <span className="wf-arrow">→</span>
        <div className="wf-node">
          <span className="wf-icon">🔗</span>
          <span className="wf-text">AI Correlation</span>
        </div>
        <span className="wf-arrow">→</span>
        <div className="wf-node">
          <span className="wf-icon">🧠</span>
          <span className="wf-text">Risk Triage</span>
        </div>
        <span className="wf-arrow">→</span>
        <div className="wf-node">
          <span className="wf-icon">📋</span>
          <span className="wf-text">Prioritized Findings</span>
        </div>
      </div>
    </div>
  )
}
