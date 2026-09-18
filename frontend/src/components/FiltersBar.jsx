export default function FiltersBar({
  severityFilter,
  setSeverityFilter,
  categoryFilter,
  setCategoryFilter,
  showNoise,
  setShowNoise,
  categories,
}) {
  const severities = ['All', 'Critical', 'High', 'Medium', 'Low', 'Informational']

  return (
    <div className="filter-row">
      <div className="filter-group">
        <label>Filter by Severity</label>
        <div className="pill-select">
          {severities.map((s) => (
            <button
              key={s}
              type="button"
              className={`pill-toggle ${severityFilter === s ? 'active' : ''}`}
              onClick={() => setSeverityFilter(s)}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-group">
        <label>Filter by Exposure Type</label>
        <div className="pill-select">
          <button
            type="button"
            className={`pill-toggle ${categoryFilter === 'All' ? 'active' : ''}`}
            onClick={() => setCategoryFilter('All')}
          >
            All
          </button>
          {categories.map((c) => (
            <button
              key={c.name}
              type="button"
              className={`pill-toggle ${categoryFilter === c.name ? 'active' : ''}`}
              onClick={() => setCategoryFilter(c.name)}
            >
              {c.name} ({c.count})
            </button>
          ))}
        </div>
      </div>

      <div className="noise-toggle">
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={showNoise}
            onChange={(e) => setShowNoise(e.target.checked)}
          />
          <span>Include Benign / Noise</span>
        </label>
      </div>
    </div>
  )
}
