import { useState } from 'react'

export default function FindingCard({ item, showPatchButton = false, onPatch }) {
  const [patchLoading, setPatchLoading] = useState(false)
  const [patchData, setPatchData] = useState(item.patch || null)

  const sev = item.severity || 'Informational'
  const isFp = Boolean(item.is_false_positive)
  const sevKey = isFp ? 'fp' : sev.toLowerCase()

  const handleGenerate = async () => {
    if (!onPatch) return
    setPatchLoading(true)
    try {
      const res = await onPatch(item.link, item.risk_summary)
      setPatchData(res)
    } catch (e) {
      console.error(e)
    } finally {
      setPatchLoading(false)
    }
  }

  return (
    <div className={`finding-card ${isFp ? 'fp' : ''}`}>
      <div className={`sev-bar sev-bar-${sevKey}`} />
      <div className="card-inner">
        <div className="card-header">
          <div className="card-pills">
            {item.category && <span className="cat-pill">{item.category}</span>}
            <span className="src-pill">SerpApi Passive OSINT</span>
          </div>
          <span className={`sev-badge sev-${sevKey}`}>
            {isFp ? '🛡️ False Positive' : sev}
          </span>
        </div>

        <div className="card-url">
          <a href={item.link} target="_blank" rel="noopener noreferrer">
            {item.link}
          </a>
        </div>

        <div className="card-section-label">Risk Assessment</div>
        <div className="card-risk-text">{item.risk_summary || 'No risk assessment provided.'}</div>

        {item.remediation && (
          <div className="card-remediation">
            <strong>Recommended Fix:</strong> {item.remediation}
          </div>
        )}

        {item.query_used && (
          <div className="card-query">
            <strong>Dork Query:</strong> <code>{item.query_used}</code>
          </div>
        )}

        {patchData && (
          <div className="fix-panel">
            <div className="fix-panel-header">
              <span className="fix-config-badge">{patchData.config_type || 'Patch Artifact'}</span>
              <span style={{ fontSize: '11px', color: 'var(--blue)', fontWeight: 600 }}>
                Target: {patchData.filename || 'remediation.conf'}
              </span>
            </div>
            {patchData.instructions && (
              <div className="fix-instructions">{patchData.instructions}</div>
            )}
            {patchData.patch_content && (
              <pre className="fix-code">{patchData.patch_content}</pre>
            )}
          </div>
        )}
      </div>

      {showPatchButton && !isFp && !patchData && (
        <button
          className="patch-btn"
          onClick={handleGenerate}
          disabled={patchLoading}
        >
          {patchLoading ? 'Generating Fix with Gemini…' : '⚡ Generate Fix Artifact'}
        </button>
      )}
    </div>
  )
}
