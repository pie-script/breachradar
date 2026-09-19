import { useState } from 'react'

export default function TopNav({ domain, setDomain, onScan, loading, targetScanned }) {
  const [localInput, setLocalInput] = useState(domain || 'testphp.vulnweb.com')

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
        <div className="recon-status-badge">
          <span className="status-beacon" />
          <span>Passive Recon Workspace</span>
        </div>

        {targetScanned && (
          <div style={{ fontSize: '12px', color: '#64748b', fontWeight: 600 }}>
            Target: <code style={{ color: '#0f172a', background: '#f1f5f9', padding: '3px 8px', borderRadius: '4px' }}>{targetScanned}</code>
          </div>
        )}

        <div className="top-avatar" title="Security Analyst">
          🛡️
        </div>
      </div>
    </header>
  )
}
