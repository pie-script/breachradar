import { useState } from 'react'

export default function TopNav({
  domain,
  setDomain,
  onScan,
  loading,
  targetScanned,
  scansHistory = [],
  onSelectStoredTarget,
  onOpenPortfolio,
}) {
  const [localInput, setLocalInput] = useState(domain || 'testphp.vulnweb.com')
  const [dropdownOpen, setDropdownOpen] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!localInput.trim()) return
    setDomain(localInput.trim())
    onScan(localInput.trim())
  }

  return (
    <header className="top-nav">
      <form className="nav-search-bar" onSubmit={handleSubmit}>
        <span className="search-icon">🔍</span>
        <input
          type="text"
          className="search-input"
          placeholder="Enter target domain (e.g. testphp.vulnweb.com)"
          value={localInput}
          onChange={(e) => setLocalInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="scan-submit-btn" disabled={loading}>
          {loading ? 'Scanning…' : '⚡ Run Scan'}
        </button>
      </form>

      <div className="top-nav-actions">
        {/* Scanned Targets Switcher Dropdown */}
        {scansHistory.length > 0 && (
          <div className="target-switcher-wrapper">
            <button
              type="button"
              className="target-switcher-btn"
              onClick={() => setDropdownOpen(!dropdownOpen)}
            >
              <span>🌐 Targets ({scansHistory.length})</span>
              <span style={{ fontSize: '10px' }}>▼</span>
            </button>

            {dropdownOpen && (
              <div className="target-dropdown-menu">
                <div className="dropdown-header-label">Switch Monitored Target</div>
                {scansHistory.map((scan) => {
                  const score = scan.stats?.posture_score || 100
                  const isCur = scan.domain === targetScanned
                  return (
                    <button
                      key={scan.domain}
                      type="button"
                      className={`dropdown-target-item ${isCur ? 'active' : ''}`}
                      onClick={() => {
                        setDropdownOpen(false)
                        setLocalInput(scan.domain)
                        setDomain(scan.domain)
                        onSelectStoredTarget(scan.domain)
                      }}
                    >
                      <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '170px' }}>
                        {scan.domain}
                      </span>
                      <span
                        className={`status-pill ${score >= 80 ? 'pill-low' : score >= 50 ? 'pill-medium' : 'pill-critical'}`}
                        style={{ fontSize: '10px', padding: '1px 6px' }}
                      >
                        {score}%
                      </span>
                    </button>
                  )
                })}

                <div style={{ borderTop: '1px solid #f1f5f9', marginTop: '4px', paddingTop: '4px' }}>
                  <button
                    type="button"
                    className="dropdown-target-item"
                    style={{ color: '#2563eb', fontWeight: 700 }}
                    onClick={() => {
                      setDropdownOpen(false)
                      onOpenPortfolio()
                    }}
                  >
                    <span>📊 View Portfolio Overview</span>
                    <span>→</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="recon-status-badge">
          <span className="status-beacon" />
          <span>Passive Recon</span>
        </div>

        {targetScanned && (
          <div style={{ fontSize: '12px', color: '#64748b', fontWeight: 600 }}>
            Target: <code style={{ color: '#0f172a', background: '#f1f5f9', padding: '3px 8px', borderRadius: '4px' }}>{targetScanned}</code>
          </div>
        )}

        <div className="top-avatar" title="Security Operations">
          🛡️
        </div>
      </div>
    </header>
  )
}
