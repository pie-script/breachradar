export default function ExecutiveSummary({ summary, domain }) {
  if (!summary) return null

  return (
    <div className="exec-card">
      <div className="exec-header">
        <span className="exec-label">Executive Threat Briefing</span>
        <span className="exec-badge">● CISO · {domain}</span>
      </div>
      <div className="exec-text">{summary}</div>
    </div>
  )
}
