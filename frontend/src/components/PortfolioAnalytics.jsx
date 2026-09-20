export default function PortfolioAnalytics({
  scansHistory = [],
  onSelectDomain,
  onDeleteDomain,
}) {
  const totalDomains = scansHistory.length

  const avgPosture = totalDomains > 0
    ? Math.round(scansHistory.reduce((acc, s) => acc + (s.stats?.posture_score || 100), 0) / totalDomains)
    : 100

  const totalActionable = scansHistory.reduce((acc, s) => acc + (s.stats?.actionable || 0), 0)
  const totalNoise = scansHistory.reduce((acc, s) => acc + (s.stats?.false_positive || 0), 0)

  return (
    <div>
      {/* Portfolio Header Banner */}
      <div className="portfolio-header-card">
        <div>
          <div className="portfolio-header-title">Multi-Domain Security Portfolio</div>
          <div className="portfolio-header-sub">
            Continuous passive attack surface intelligence across all monitored digital assets
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-beacon" />
          <span style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8' }}>
            {totalDomains} Monitored {totalDomains === 1 ? 'Domain' : 'Domains'}
          </span>
        </div>
      </div>

      {/* Aggregate KPI Grid */}
      <div className="portfolio-kpi-grid">
        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Monitored Targets</span>
            <span className="kpi-badge badge-blue">Portfolio Size</span>
          </div>
          <div className="kpi-value-row">
            <div className="kpi-value">{totalDomains}</div>
            <span style={{ fontSize: '26px' }}>🌐</span>
          </div>
          <div className="kpi-footer-note">
            <span>Active footprint surveillance</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Average Posture Index</span>
            <span className={`kpi-badge ${avgPosture >= 80 ? 'badge-green' : avgPosture >= 50 ? 'badge-orange' : 'badge-red'}`}>
              {avgPosture >= 80 ? 'High Resilience' : avgPosture >= 50 ? 'Medium Risk' : 'Urgent Alert'}
            </span>
          </div>
          <div className="kpi-value-row">
            <div className="kpi-value">
              {avgPosture}
              <span style={{ fontSize: '15px', color: '#94a3b8', fontWeight: 500 }}>/100</span>
            </div>
            <svg width="40" height="40" viewBox="0 0 40 40">
              <circle cx="20" cy="20" r="15" fill="none" stroke="#e2e8f0" strokeWidth="4" />
              <circle
                cx="20"
                cy="20"
                r="15"
                fill="none"
                stroke={avgPosture >= 80 ? '#10b981' : avgPosture >= 50 ? '#f97316' : '#ef4444'}
                strokeWidth="4"
                strokeDasharray={94.2}
                strokeDashoffset={94.2 - (94.2 * avgPosture) / 100}
                strokeLinecap="round"
                transform="rotate(-90 20 20)"
              />
            </svg>
          </div>
          <div className="kpi-footer-note">
            <span>Portfolio-wide resilience score</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Total Actionable Leaks</span>
            <span className="kpi-badge badge-red">{totalActionable} Active Risks</span>
          </div>
          <div className="kpi-value-row">
            <div className="kpi-value" style={{ color: totalActionable > 0 ? '#dc2626' : '#0f172a' }}>
              {totalActionable}
            </div>
            <span style={{ fontSize: '26px' }}>🚨</span>
          </div>
          <div className="kpi-footer-note">
            <span>Requiring immediate remediation</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Total Noise Filtered</span>
            <span className="kpi-badge badge-green">AI Quality</span>
          </div>
          <div className="kpi-value-row">
            <div className="kpi-value">{totalNoise}</div>
            <span style={{ fontSize: '26px' }}>🛡️</span>
          </div>
          <div className="kpi-footer-note">
            <span>Benign dorks eliminated</span>
          </div>
        </div>
      </div>

      {/* Comparative Posture Bar Chart */}
      <div className="chart-container-card">
        <div className="card-title-row">
          <div>
            <div className="card-heading">Domain Posture Comparison</div>
            <div className="card-subheading">Side-by-side resilience scores across monitored targets</div>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <span className="status-pill pill-low">● 80-100 Strong</span>
            <span className="status-pill pill-medium">● 50-79 Medium</span>
            <span className="status-pill pill-critical">● 0-49 Urgent</span>
          </div>
        </div>

        {scansHistory.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>
            No domains scanned yet. Run scans to view comparative posture scores.
          </div>
        ) : (
          <div className="comparative-chart-bars">
            {scansHistory.map((scan) => {
              const score = scan.stats?.posture_score || 100
              const color = score >= 80 ? '#10b981' : score >= 50 ? '#f97316' : '#ef4444'
              return (
                <div key={scan.domain} className="comp-bar-col">
                  <div className="comp-bar-val" style={{ color }}>{score}%</div>
                  <div
                    className="comp-bar-fill"
                    style={{
                      height: `${Math.max(score * 1.8, 16)}px`,
                      background: color,
                    }}
                  />
                  <div className="comp-bar-label" title={scan.domain}>
                    {scan.domain}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Monitored Targets Table */}
      <div className="table-section-card">
        <div className="card-title-row">
          <div>
            <div className="card-heading">Monitored Attack Surfaces</div>
            <div className="card-subheading">All stored reconnaissance targets in local intelligence storage</div>
          </div>
        </div>

        <div className="data-table-container">
          <table className="enterprise-table">
            <thead>
              <tr>
                <th>Domain Asset</th>
                <th>Posture Index</th>
                <th>Actionable Exposures</th>
                <th>Noise Filtered</th>
                <th>Last Scanned</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {scansHistory.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '30px', color: '#94a3b8' }}>
                    No scanned targets stored. Run a scan above to add a domain.
                  </td>
                </tr>
              ) : (
                scansHistory.map((scan) => {
                  const score = scan.stats?.posture_score || 100
                  const actionable = scan.stats?.actionable || 0
                  const noise = scan.stats?.false_positive || 0
                  const scoreColor = score >= 80 ? 'pill-low' : score >= 50 ? 'pill-medium' : 'pill-critical'
                  const dateStr = scan.scannedAt
                    ? new Date(scan.scannedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    : 'Just now'

                  return (
                    <tr key={scan.domain}>
                      <td>
                        <strong style={{ color: '#0f172a', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span>🌐</span>
                          <span>{scan.domain}</span>
                        </strong>
                      </td>
                      <td>
                        <span className={`status-pill ${scoreColor}`}>
                          {score} / 100
                        </span>
                      </td>
                      <td>
                        <span style={{ fontWeight: 700, color: actionable > 0 ? '#dc2626' : '#64748b' }}>
                          {actionable} {actionable === 1 ? 'risk' : 'risks'}
                        </span>
                      </td>
                      <td>
                        <span style={{ color: '#059669', fontWeight: 600 }}>
                          {noise} benign
                        </span>
                      </td>
                      <td>
                        <span style={{ fontSize: '12px', color: '#64748b' }}>{dateStr}</span>
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        <div style={{ display: 'inline-flex', gap: '8px' }}>
                          <button
                            type="button"
                            className="action-fix-btn"
                            onClick={() => onSelectDomain(scan.domain)}
                          >
                            🔍 Deep Dive
                          </button>
                          <button
                            type="button"
                            style={{
                              background: '#fef2f2',
                              border: '1px solid #fecaca',
                              color: '#dc2626',
                              fontSize: '11.5px',
                              fontWeight: 700,
                              padding: '5px 10px',
                              borderRadius: '6px',
                              cursor: 'pointer',
                            }}
                            onClick={() => onDeleteDomain(scan.domain)}
                            title="Remove from history"
                          >
                            ✕
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
