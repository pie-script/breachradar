import { useState } from 'react'
import FindingCard from './FindingCard.jsx'
import { downloadResultsCsv } from '../api.js'

export default function ResultsTabs({
  results,
  actionableResults,
  visibleResults,
  visibleActionable,
  rawFindings,
  domain,
  onPatch,
}) {
  const [activeTab, setActiveTab] = useState('actionable')

  return (
    <div>
      <div className="tab-bar">
        <button
          type="button"
          className={`tab-btn ${activeTab === 'actionable' ? 'active' : ''}`}
          onClick={() => setActiveTab('actionable')}
        >
          🚨 Actionable Risks ({actionableResults.length})
        </button>
        <button
          type="button"
          className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          📋 All Results ({results.length})
        </button>
        <button
          type="button"
          className={`tab-btn ${activeTab === 'raw' ? 'active' : ''}`}
          onClick={() => setActiveTab('raw')}
        >
          📦 Raw Intelligence & Export
        </button>
      </div>

      {activeTab === 'actionable' && (
        <div>
          {visibleActionable.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🛡️</div>
              <div className="empty-title">No Actionable Exposures Found</div>
              <div className="empty-sub">
                Either all discovered findings were verified as false positives or no matches met the filter.
              </div>
            </div>
          ) : (
            visibleActionable.map((item, idx) => (
              <FindingCard
                key={idx}
                item={item}
                showPatchButton={true}
                onPatch={onPatch}
              />
            ))
          )}
        </div>
      )}

      {activeTab === 'all' && (
        <div>
          {visibleResults.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <div className="empty-title">No Findings Match Selected Filters</div>
              <div className="empty-sub">Adjust your severity or category filters above.</div>
            </div>
          ) : (
            visibleResults.map((item, idx) => (
              <FindingCard
                key={idx}
                item={item}
                showPatchButton={!item.is_false_positive}
                onPatch={onPatch}
              />
            ))
          )}
        </div>
      )}

      {activeTab === 'raw' && (
        <div className="export-panel">
          <pre className="raw-json">
            {JSON.stringify(results, null, 2)}
          </pre>
          <div className="export-side">
            <button
              type="button"
              className="export-btn"
              onClick={() => downloadResultsCsv(results, domain)}
            >
              📥 Download Report (CSV)
            </button>
            <div className="export-caption">
              Exports full telemetry including severity, AI risk assessment, category, and raw dork queries.
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
