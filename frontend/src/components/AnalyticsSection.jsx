export default function AnalyticsSection({ stats, executiveSummary, domain }) {
  if (!stats) return null

  const {
    total = 0,
    critical = 0,
    high = 0,
    medium = 0,
    low = 0,
    informational = 0,
    posture_score = 100,
    categories = [],
  } = stats

  const circumference = 2 * Math.PI * 65 // ~408.4
  const strokeDashoffset = circumference - (circumference * posture_score) / 100

  const postureColor =
    posture_score >= 80 ? '#10b981' : posture_score >= 50 ? '#f97316' : '#ef4444'

  return (
    <>
      {/* CISO Executive Briefing Banner */}
      {executiveSummary && (
        <div className="briefing-card">
          <div className="briefing-header">
            <span className="briefing-badge">● CISO Threat Briefing</span>
            <span style={{ fontSize: '12px', color: '#64748b', fontWeight: 600 }}>
              Target: <strong style={{ color: '#0f172a' }}>{domain}</strong>
            </span>
          </div>
          <div className="briefing-text">{executiveSummary}</div>
        </div>
      )}

      <div className="middle-grid">
        {/* Left: Exposure Vectors & Severity Breakdown */}
        <div className="surface-card">
          <div className="card-title-row">
            <div>
              <div className="card-heading">Exposure Attack Vectors</div>
              <div className="card-subheading">Breakdown of passive intelligence hits by category</div>
            </div>
            <div style={{ display: 'flex', gap: '6px' }}>
              <span className="status-pill pill-critical">{critical} Crit</span>
              <span className="status-pill pill-high">{high} High</span>
              <span className="status-pill pill-medium">{medium} Med</span>
              <span className="status-pill pill-low">{low} Low</span>
            </div>
          </div>

          <div className="hbar-container">
            {categories.length === 0 ? (
              <div style={{ color: '#94a3b8', fontSize: '13px', padding: '20px 0' }}>
                No category breakdown available.
              </div>
            ) : (
              categories.slice(0, 5).map((cat, idx) => {
                const pct = Math.round((cat.count / Math.max(total, 1)) * 100)
                const colors = ['#3b82f6', '#06b6d4', '#8b5cf6', '#f59e0b', '#10b981']
                const barColor = colors[idx % colors.length]
                return (
                  <div key={cat.name} className="hbar-item">
                    <div className="hbar-meta">
                      <span>{cat.name}</span>
                      <span>
                        <strong>{cat.count}</strong> <span style={{ color: '#94a3b8' }}>({pct}%)</span>
                      </span>
                    </div>
                    <div className="hbar-bar-bg">
                      <div
                        className="hbar-bar-fill"
                        style={{ width: `${pct}%`, background: barColor }}
                      />
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>

        {/* Right: Security Posture Radial Gauge (Image 2 & 4 style) */}
        <div className="surface-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <div className="card-title-row" style={{ width: '100%' }}>
            <div>
              <div className="card-heading">Domain Posture Rating</div>
              <div className="card-subheading">Computed health index</div>
            </div>
          </div>

          <div className="radial-gauge-container">
            <svg className="radial-svg" viewBox="0 0 160 160">
              {/* Outer track */}
              <circle
                cx="80"
                cy="80"
                r="65"
                fill="none"
                stroke="#f1f5f9"
                strokeWidth="12"
              />
              {/* Progress ring */}
              <circle
                cx="80"
                cy="80"
                r="65"
                fill="none"
                stroke={postureColor}
                strokeWidth="12"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                transform="rotate(-90 80 80)"
                style={{ transition: 'stroke-dashoffset 0.6s ease' }}
              />
              {/* Inner subtle concentric accent (Image 4 style) */}
              <circle
                cx="80"
                cy="80"
                r="50"
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="1.5"
                strokeDasharray="4 4"
              />
              {/* Center value */}
              <text x="80" y="78" textAnchor="middle" className="radial-score-text">
                {posture_score}%
              </text>
              <text x="80" y="98" textAnchor="middle" className="radial-label-text">
                HEALTH INDEX
              </text>
            </svg>

            <div
              className="posture-status-tag"
              style={{
                background: posture_score >= 80 ? '#ecfdf5' : posture_score >= 50 ? '#fff7ed' : '#fef2f2',
                color: posture_score >= 80 ? '#047857' : posture_score >= 50 ? '#c2410c' : '#dc2626',
                border: `1px solid ${posture_score >= 80 ? '#a7f3d0' : posture_score >= 50 ? '#fed7aa' : '#fecaca'}`,
              }}
            >
              {posture_score >= 80 ? '✓ High Security Resilience' : posture_score >= 50 ? '⚠️ Moderate Exposure Risk' : '🚨 Severe Exposure Alert'}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
