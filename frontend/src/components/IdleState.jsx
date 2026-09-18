export default function IdleState() {
  return (
    <div className="radar-wrap">
      <div className="radar-container">
        <div className="radar-ring r1" />
        <div className="radar-ring r2" />
        <div className="radar-ring r3" />
        <div className="radar-center" />
        <div className="radar-sweep" />
      </div>
      <div className="radar-label">Awaiting Target</div>
      <div className="radar-sublabel">Enter a domain in the sidebar and launch a passive scan</div>
      <div className="ghost-grid">
        <div className="ghost-card">
          <div className="ghost-label">Assets Indexed</div>
          <div className="ghost-value">—</div>
        </div>
        <div className="ghost-card">
          <div className="ghost-label">Exposures Found</div>
          <div className="ghost-value">—</div>
        </div>
        <div className="ghost-card">
          <div className="ghost-label">Risk Score</div>
          <div className="ghost-value">—</div>
        </div>
      </div>
      <div className="serpapi-badge">🔍 Powered by SerpApi Search Intelligence · Gemini AI</div>
    </div>
  )
}
