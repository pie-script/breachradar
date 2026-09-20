export default function KpiRow({ stats }) {
  const {
    total = 0,
    actionable = 0,
    critical = 0,
    high = 0,
    noise_pct = 0,
    false_positive = 0,
    posture_score = 100,
  } = stats || {}

  return (
    <div className="kpi-grid">
      {/* 1. Total Recon Exposures */}
      <div className="kpi-card">
        <div className="kpi-top">
          <span className="kpi-label">Total Exposures Indexed</span>
          <span className="kpi-badge badge-blue">Passive OSINT</span>
        </div>
        <div className="kpi-value-row">
          <div className="kpi-value">{total}</div>
          {/* Embedded SVG Wave Chart (Image 1 & 2 Style) */}
          <svg className="sparkline-svg" viewBox="0 0 90 35" fill="none">
            <path
              d="M0 25 C20 10, 40 30, 60 12 C75 0, 85 18, 90 8"
              stroke="#3b82f6"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
            <path
              d="M0 25 C20 10, 40 30, 60 12 C75 0, 85 18, 90 8 L90 35 L0 35 Z"
              fill="url(#blueGrad)"
              opacity="0.15"
            />
            <defs>
              <linearGradient id="blueGrad" x1="0" y1="0" x2="0" y2="1">
                <stop stopColor="#3b82f6" />
                <stop offset="1" stopColor="#ffffff" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div className="kpi-footer-note">
          <span style={{ color: '#2563eb', fontWeight: 700 }}>Google Dork Recon</span>
          <span>· Cache indexed</span>
        </div>
      </div>

      {/* 2. Actionable Risks (Critical & High) */}
      <div className="kpi-card">
        <div className="kpi-top">
          <span className="kpi-label">Actionable Exposures</span>
          <span className="kpi-badge badge-red">{critical} Critical · {high} High</span>
        </div>
        <div className="kpi-value-row">
          <div className="kpi-value" style={{ color: actionable > 0 ? '#dc2626' : '#0f172a' }}>
            {actionable}
          </div>
          {/* Mini Bar Indicator (Image 1 Payments style) */}
          <svg className="sparkline-svg" viewBox="0 0 90 35" fill="none">
            <rect x="5" y="18" width="12" height="17" rx="3" fill="#fecaca" />
            <rect x="23" y="10" width="12" height="25" rx="3" fill="#f87171" />
            <rect x="41" y="4" width="12" height="31" rx="3" fill="#ef4444" />
            <rect x="59" y="14" width="12" height="21" rx="3" fill="#dc2626" />
            <rect x="77" y="8" width="12" height="27" rx="3" fill="#b91c1c" />
          </svg>
        </div>
        <div className="kpi-footer-note">
          <span style={{ color: '#dc2626', fontWeight: 700 }}>Immediate Attention</span>
          <span>· Verified leaks</span>
        </div>
      </div>

      {/* 3. Noise Elimination / False Positives */}
      <div className="kpi-card">
        <div className="kpi-top">
          <span className="kpi-label">Noise Reduction Ratio</span>
          <span className="kpi-badge badge-green">Gemini AI Filter</span>
        </div>
        <div className="kpi-value-row">
          <div className="kpi-value">{noise_pct}%</div>
          {/* Smooth Sine Wave Sparkline (Image 2 style) */}
          <svg className="sparkline-svg" viewBox="0 0 90 35" fill="none">
            <path
              d="M0 18 Q 22 4, 45 18 T 90 18"
              stroke="#10b981"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
            <circle cx="45" cy="18" r="3.5" fill="#10b981" />
          </svg>
        </div>
        <div className="kpi-footer-note">
          <span style={{ color: '#059669', fontWeight: 700 }}>{false_positive} Benign Filtered</span>
          <span>· Clean telemetry</span>
        </div>
      </div>

      {/* 4. Posture Health Index */}
      <div className="kpi-card">
        <div className="kpi-top">
          <span className="kpi-label">Security Posture Index</span>
          <span className={`kpi-badge ${posture_score >= 80 ? 'badge-green' : posture_score >= 50 ? 'badge-orange' : 'badge-red'}`}>
            {posture_score >= 80 ? 'Good Standing' : posture_score >= 50 ? 'Medium Risk' : 'Urgent Risk'}
          </span>
        </div>
        <div className="kpi-value-row">
          <div className="kpi-value">
            {posture_score}
            <span style={{ fontSize: '15px', color: '#94a3b8', fontWeight: 500 }}>/100</span>
          </div>
          {/* Mini Radial Indicator */}
          <svg width="40" height="40" viewBox="0 0 40 40">
            <circle cx="20" cy="20" r="15" fill="none" stroke="#e2e8f0" strokeWidth="4" />
            <circle
              cx="20"
              cy="20"
              r="15"
              fill="none"
              stroke={posture_score >= 80 ? '#10b981' : posture_score >= 50 ? '#f97316' : '#ef4444'}
              strokeWidth="4"
              strokeDasharray={94.2}
              strokeDashoffset={94.2 - (94.2 * posture_score) / 100}
              strokeLinecap="round"
              transform="rotate(-90 20 20)"
            />
          </svg>
        </div>
        <div className="kpi-footer-note">
          <span>Target Attack Surface Score</span>
        </div>
      </div>
    </div>
  )
}
