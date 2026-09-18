export default function AnalyticsDashboard({ stats, domain }) {
  if (!stats) return null

  const {
    total = 0,
    actionable = 0,
    critical = 0,
    high = 0,
    medium = 0,
    low = 0,
    informational = 0,
    false_positive = 0,
    posture_score = 100,
    noise_pct = 0,
    categories = [],
    top_category = 'None',
  } = stats

  const postureColor =
    posture_score >= 80 ? 'var(--green)' : posture_score >= 50 ? 'var(--yellow)' : 'var(--crit)'

  return (
    <div className="analytics-shell">
      <div className="analytics-header">
        <div>
          <div className="analytics-kicker">Autonomous Exposure Analysis</div>
          <div className="analytics-title">Security Posture & Risk Dynamics</div>
          <div className="analytics-subtitle">
            Passive attack surface footprinting across search engine intelligence caches
          </div>
        </div>
        <div className="posture-box">
          <div className="posture-label">Domain Posture Index</div>
          <div className="posture-score" style={{ color: postureColor }}>
            {posture_score}
            <small>/100</small>
          </div>
          <div className="posture-track">
            <div
              className="posture-fill"
              style={{ width: `${posture_score}%`, background: postureColor }}
            />
          </div>
        </div>
      </div>

      <div className="hero-stat-row">
        <div className="hero-stat-card urgent">
          <div className="hero-stat-icon">🚨</div>
          <div className="hero-stat-label">Actionable Exposures</div>
          <div className="hero-stat-value">{actionable}</div>
          <div className="hero-stat-sub">
            <span>●</span> Requires active triage & remediation
          </div>
        </div>

        <div className="hero-stat-card quality">
          <div className="hero-stat-icon">🛡️</div>
          <div className="hero-stat-label">Noise Reduction & Filtering</div>
          <div className="hero-stat-value">{noise_pct}%</div>
          <div className="hero-stat-sub">
            <span>✓</span> {false_positive} benign dork results eliminated
          </div>
        </div>
      </div>

      <div className="stat-strip">
        <div className="mini-stat">
          <div className="mini-stat-label">Critical Findings</div>
          <div className="mini-stat-value" style={{ color: 'var(--crit)' }}>{critical}</div>
          <div className="mini-stat-note">Immediate breach risk</div>
        </div>
        <div className="mini-stat">
          <div className="mini-stat-label">High Severity</div>
          <div className="mini-stat-value" style={{ color: 'var(--orange)' }}>{high}</div>
          <div className="mini-stat-note">Sensitive assets/configs</div>
        </div>
        <div className="mini-stat">
          <div className="mini-stat-label">Medium Severity</div>
          <div className="mini-stat-value" style={{ color: 'var(--yellow)' }}>{medium}</div>
          <div className="mini-stat-note">Info leakage & internals</div>
        </div>
        <div className="mini-stat">
          <div className="mini-stat-label">Low & Info</div>
          <div className="mini-stat-value" style={{ color: 'var(--blue)' }}>{low + informational}</div>
          <div className="mini-stat-note">Public footprint</div>
        </div>
      </div>

      <div className="chart-row" style={{ marginTop: '16px' }}>
        <div className="chart-card">
          <div className="chart-title">Severity Distribution</div>
          <div className="chart-caption">Proportion of verified exposures across severity tiers</div>
          <div className="donut-wrap">
            <div className="donut-chart" style={{
              background: `conic-gradient(
                var(--crit) 0% ${(critical / Math.max(total, 1)) * 100}%,
                var(--orange) ${(critical / Math.max(total, 1)) * 100}% ${((critical + high) / Math.max(total, 1)) * 100}%,
                var(--yellow) ${((critical + high) / Math.max(total, 1)) * 100}% ${((critical + high + medium) / Math.max(total, 1)) * 100}%,
                var(--blue) ${((critical + high + medium) / Math.max(total, 1)) * 100}% 100%
              )`
            }}>
              <div className="donut-hole">
                <div className="donut-hole-value">{total}</div>
                <div className="donut-hole-label">Total</div>
              </div>
            </div>
            <div className="donut-legend">
              <div className="legend-item">
                <span className="legend-dot" style={{ background: 'var(--crit)' }} />
                <span>Critical</span>
                <span className="legend-count">{critical}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot" style={{ background: 'var(--orange)' }} />
                <span>High</span>
                <span className="legend-count">{high}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot" style={{ background: 'var(--yellow)' }} />
                <span>Medium</span>
                <span className="legend-count">{medium}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot" style={{ background: 'var(--blue)' }} />
                <span>Low & Info</span>
                <span className="legend-count">{low + informational}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-title">Top Exposure Categories</div>
          <div className="chart-caption">Primary attack vectors identified by reconnaissance dorks</div>
          <div className="hbar-list">
            {categories.slice(0, 5).map((cat) => {
              const pct = Math.round((cat.count / Math.max(total, 1)) * 100)
              return (
                <div key={cat.name} className="hbar-row">
                  <div className="hbar-label" title={cat.name}>{cat.name}</div>
                  <div className="hbar-track">
                    <div className="hbar-fill" style={{ width: `${pct}%` }} />
                  </div>
                  <div className="hbar-value">{cat.count}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
