import DefenderShield from './DefenderShield.jsx'

const STAGES = [
  'SerpApi Google Dork',
  'AI Correlation',
  'Gemini Risk Triage',
  'Prioritization',
  'Report Ready',
]

export default function Sidebar({ activeTab, setActiveTab, actionableCount = 0, totalCount = 0, loading, isComplete }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-badge">
          <DefenderShield size={22} glow={false} />
        </div>
        <div>
          <div className="brand-title">BreachRadar</div>
          <div className="brand-subtitle">Attack Surface AI</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-title">Operations</div>
        
        <button
          type="button"
          className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <span className="nav-icon">📊</span>
          <span>Dashboard</span>
        </button>

        <button
          type="button"
          className={`nav-item ${activeTab === 'actionable' ? 'active' : ''}`}
          onClick={() => setActiveTab('actionable')}
        >
          <span className="nav-icon">🚨</span>
          <span>Actionable Risks</span>
          {actionableCount > 0 && <span className="nav-badge">{actionableCount}</span>}
        </button>

        <button
          type="button"
          className={`nav-item ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          <span className="nav-icon">📋</span>
          <span>All Findings</span>
          {totalCount > 0 && (
            <span style={{ marginLeft: 'auto', fontSize: '11px', color: '#64748b', fontWeight: 600 }}>
              {totalCount}
            </span>
          )}
        </button>

        <button
          type="button"
          className={`nav-item ${activeTab === 'raw' ? 'active' : ''}`}
          onClick={() => setActiveTab('raw')}
        >
          <span className="nav-icon">📦</span>
          <span>Raw Telemetry</span>
        </button>
      </nav>

      <div className="sidebar-pipeline">
        <div className="pipeline-header">
          <span>AI Scan Pipeline</span>
          <span>{isComplete ? '100%' : loading ? 'Active' : 'Idle'}</span>
        </div>
        {STAGES.map((step, idx) => {
          const isDone = isComplete
          const isActive = loading && idx === 2
          return (
            <div
              key={step}
              className={`pipeline-item ${isDone ? 'done' : isActive ? 'active' : ''}`}
            >
              <span className="pipeline-dot" />
              <span>{step}</span>
            </div>
          )
        })}
      </div>
    </aside>
  )
}
