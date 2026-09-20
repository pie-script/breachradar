import DefenderShield from './DefenderShield.jsx'

export default function IdleState({ onSelectTarget }) {
  const suggestions = [
    'testphp.vulnweb.com',
    'juice-shop.herokuapp.com',
    'example.com',
  ]

  return (
    <div className="idle-container">
      <div className="idle-radar-box">
        <div className="idle-radar-ring ring-outer" />
        <div className="idle-radar-ring ring-mid" />
        <div className="idle-radar-ring ring-inner" />
        <div className="idle-core-icon">
          <DefenderShield size={24} glow={false} />
        </div>
      </div>

      <h2 className="idle-title">Zero-Touch Attack Surface Intelligence</h2>
      <p className="idle-desc">
        Launch passive reconnaissance to index exposures, leaked credentials, sensitive endpoints, and configuration files via Google Dork intelligence.
      </p>

      <div style={{ marginBottom: '12px', fontSize: '12px', fontWeight: 700, color: '#64748b', textTransform: 'uppercase', letterSpacing: '1px' }}>
        Sample Targets:
      </div>
      <div className="quick-targets">
        {suggestions.map((target) => (
          <button
            key={target}
            type="button"
            className="target-pill"
            onClick={() => onSelectTarget(target)}
          >
            ⚡ {target}
          </button>
        ))}
      </div>
    </div>
  )
}
