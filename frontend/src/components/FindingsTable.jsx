import { useState, useMemo } from 'react'
import { downloadResultsCsv } from '../api.js'

export default function FindingsTable({
  results = [],
  domain,
  onPatch,
}) {
  const [filterSeverity, setFilterSeverity] = useState('All')
  const [searchQuery, setSearchQuery] = useState('')
  const [includeNoise, setIncludeNoise] = useState(false)
  const [expandedPatches, setExpandedPatches] = useState({})
  const [patchLoading, setPatchLoading] = useState({})

  const severities = ['All', 'Critical', 'High', 'Medium', 'Low']

  const filtered = useMemo(() => {
    return results.filter((item) => {
      if (!includeNoise && item.is_false_positive) return false
      if (filterSeverity !== 'All' && item.severity !== filterSeverity) return false
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase()
        const link = (item.link || '').toLowerCase()
        const risk = (item.risk_summary || '').toLowerCase()
        const cat = (item.category || '').toLowerCase()
        if (!link.includes(q) && !risk.includes(q) && !cat.includes(q)) return false
      }
      return true
    })
  }, [results, filterSeverity, searchQuery, includeNoise])

  const handleGeneratePatch = async (item, idx) => {
    setPatchLoading((prev) => ({ ...prev, [idx]: true }))
    try {
      const res = await onPatch(item.link, item.risk_summary)
      setExpandedPatches((prev) => ({ ...prev, [idx]: res }))
    } catch (e) {
      console.error(e)
    } finally {
      setPatchLoading((prev) => ({ ...prev, [idx]: false }))
    }
  }

  const getPillClass = (sev, isFp) => {
    if (isFp) return 'pill-fp'
    switch ((sev || '').toLowerCase()) {
      case 'critical': return 'pill-critical'
      case 'high': return 'pill-high'
      case 'medium': return 'pill-medium'
      case 'low': return 'pill-low'
      default: return 'pill-info'
    }
  }

  return (
    <div className="table-section-card">
      <div className="table-toolbar">
        <div className="table-filter-pills">
          {severities.map((sev) => (
            <button
              key={sev}
              type="button"
              className={`pill-btn ${filterSeverity === sev ? 'active' : ''}`}
              onClick={() => setFilterSeverity(sev)}
            >
              {sev}
            </button>
          ))}
          <button
            type="button"
            className={`pill-btn ${includeNoise ? 'active' : ''}`}
            onClick={() => setIncludeNoise(!includeNoise)}
          >
            {includeNoise ? '✓ Showing Noise' : '+ Include Benign'}
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <input
            type="text"
            className="table-search-input"
            placeholder="Search URL, vulnerability, category…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />

          <button
            type="button"
            className="export-csv-btn"
            onClick={() => downloadResultsCsv(filtered, domain)}
            title="Download CSV report"
          >
            📥 Export CSV
          </button>
        </div>
      </div>

      <div className="data-table-container">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th style={{ width: '130px' }}>Severity</th>
              <th style={{ minWidth: '220px' }}>Target Resource / URL</th>
              <th style={{ width: '160px' }}>Category</th>
              <th style={{ minWidth: '260px' }}>Risk Assessment</th>
              <th style={{ width: '150px', textAlign: 'right' }}>Remediation</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '40px 16px', color: '#94a3b8' }}>
                  <div style={{ fontSize: '28px', marginBottom: '8px' }}>🛡️</div>
                  <div style={{ fontWeight: 700, color: '#0f172a' }}>No matching findings</div>
                  <div style={{ fontSize: '12px' }}>Try switching filters or include benign noise results.</div>
                </td>
              </tr>
            ) : (
              filtered.map((item, idx) => {
                const patch = expandedPatches[idx]
                const isLoading = patchLoading[idx]
                const isFp = Boolean(item.is_false_positive)
                return (
                  <tr key={idx} className={isFp ? 'is-fp' : ''}>
                    <td>
                      <span className={`status-pill ${getPillClass(item.severity, isFp)}`}>
                        {isFp ? '● False Pos' : item.severity}
                      </span>
                    </td>
                    <td>
                      <a
                        href={item.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="table-url-link"
                      >
                        <span>{item.link}</span>
                        <span style={{ fontSize: '10px' }}>↗</span>
                      </a>
                      {item.query_used && (
                        <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '3px' }}>
                          Dork: <code>{item.query_used}</code>
                        </div>
                      )}
                    </td>
                    <td>
                      <span className="category-tag">
                        {item.category || 'Information'}
                      </span>
                    </td>
                    <td>
                      <div style={{ fontSize: '13px', lineHeight: 1.5, color: '#334155' }}>
                        {item.risk_summary || 'No description available.'}
                      </div>
                      {item.remediation && (
                        <div style={{ fontSize: '12px', color: '#059669', marginTop: '4px', fontWeight: 500 }}>
                          💡 {item.remediation}
                        </div>
                      )}
                      {patch && (
                        <div className="patch-drawer">
                          <div className="patch-drawer-header">
                            <span>🛠️ {patch.config_type || 'Patch Artifact'}:</span>
                            <span style={{ color: '#0f172a' }}>{patch.filename || 'remediation.conf'}</span>
                          </div>
                          {patch.instructions && (
                            <div style={{ fontSize: '12px', color: '#334155', marginBottom: '8px' }}>
                              {patch.instructions}
                            </div>
                          )}
                          {patch.patch_content && (
                            <pre className="patch-code-box">{patch.patch_content}</pre>
                          )}
                        </div>
                      )}
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      {!isFp && !patch && (
                        <button
                          type="button"
                          className="action-fix-btn"
                          onClick={() => handleGeneratePatch(item, idx)}
                          disabled={isLoading}
                        >
                          {isLoading ? 'Generating…' : '⚡ Fix Artifact'}
                        </button>
                      )}
                      {patch && (
                        <span style={{ fontSize: '11px', color: '#10b981', fontWeight: 700 }}>
                          ✓ Ready
                        </span>
                      )}
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
