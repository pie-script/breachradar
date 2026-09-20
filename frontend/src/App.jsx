import { useState, useEffect, useMemo } from 'react'
import Sidebar from './components/Sidebar.jsx'
import TopNav from './components/TopNav.jsx'
import KpiRow from './components/KpiRow.jsx'
import AnalyticsSection from './components/AnalyticsSection.jsx'
import FindingsTable from './components/FindingsTable.jsx'
import PortfolioAnalytics from './components/PortfolioAnalytics.jsx'
import IdleState from './components/IdleState.jsx'
import { scanDomain, generatePatch } from './api.js'

const STORAGE_KEY = 'breachradar_scans_v1'

export default function App() {
  const [domain, setDomain] = useState('testphp.vulnweb.com')
  const [loading, setLoading] = useState(false)
  const [scanData, setScanData] = useState(null)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard') // 'dashboard' | 'portfolio' | 'actionable' | 'all' | 'raw'
  const [scansHistory, setScansHistory] = useState([])

  // Load stored scans from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved)
        if (Array.isArray(parsed) && parsed.length > 0) {
          setScansHistory(parsed)
          // Default to the most recent scan
          setScanData(parsed[0])
          setDomain(parsed[0].domain)
        }
      }
    } catch (e) {
      console.error('Failed to load scan history:', e)
    }
  }, [])

  // Persist scans to localStorage
  const saveScanToHistory = (newScan) => {
    setScansHistory((prev) => {
      const filtered = prev.filter((s) => s.domain.toLowerCase() !== newScan.domain.toLowerCase())
      const updated = [{ ...newScan, scannedAt: new Date().toISOString() }, ...filtered]
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch (e) {
        console.error('Failed to persist scan history:', e)
      }
      return updated
    })
  }

  const handleDeleteDomain = (targetDomain) => {
    setScansHistory((prev) => {
      const updated = prev.filter((s) => s.domain.toLowerCase() !== targetDomain.toLowerCase())
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch (e) {
        console.error('Failed to save after deletion:', e)
      }
      if (scanData?.domain?.toLowerCase() === targetDomain.toLowerCase()) {
        if (updated.length > 0) {
          setScanData(updated[0])
          setDomain(updated[0].domain)
        } else {
          setScanData(null)
        }
      }
      return updated
    })
  }

  const handleSelectStoredDomain = (targetDomain) => {
    const match = scansHistory.find((s) => s.domain.toLowerCase() === targetDomain.toLowerCase())
    if (match) {
      setScanData(match)
      setDomain(match.domain)
      setActiveTab('dashboard')
    }
  }

  const handleScan = async (targetDomain) => {
    const target = targetDomain || domain
    if (!target.trim()) {
      setError('Please enter a target domain.')
      return
    }
    setError(null)
    setLoading(true)
    try {
      const data = await scanDomain(target.trim())
      setScanData(data)
      saveScanToHistory(data)
      setActiveTab('dashboard')
    } catch (err) {
      setError(err.message || 'Failed to scan target domain. Make sure the backend server is running.')
    } finally {
      setLoading(false)
    }
  }

  const handlePatch = async (link, riskSummary) => {
    return await generatePatch(link, riskSummary)
  }

  const results = scanData?.results || []
  const stats = scanData?.stats || null
  const actionableCount = useMemo(() => {
    return results.filter((r) => !r.is_false_positive).length
  }, [results])

  return (
    <div className="app-layout">
      {/* 1. Left Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        actionableCount={actionableCount}
        totalCount={results.length}
        portfolioCount={scansHistory.length}
        loading={loading}
        isComplete={Boolean(scanData)}
      />

      {/* 2. Main Body Area */}
      <div className="main-wrapper">
        <TopNav
          domain={domain}
          setDomain={setDomain}
          onScan={handleScan}
          loading={loading}
          targetScanned={scanData?.domain}
          scansHistory={scansHistory}
          onSelectStoredTarget={handleSelectStoredDomain}
          onOpenPortfolio={() => setActiveTab('portfolio')}
        />

        <main className="content-body">
          {error && (
            <div style={{
              background: '#fef2f2',
              border: '1px solid #fecaca',
              color: '#dc2626',
              padding: '12px 16px',
              borderRadius: '8px',
              fontSize: '13px',
              fontWeight: 600,
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}>
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* VIEW: Portfolio Overview across all monitored domains */}
          {activeTab === 'portfolio' ? (
            <PortfolioAnalytics
              scansHistory={scansHistory}
              onSelectDomain={handleSelectStoredDomain}
              onDeleteDomain={handleDeleteDomain}
            />
          ) : !scanData ? (
            <IdleState onSelectTarget={(target) => {
              setDomain(target)
              handleScan(target)
            }} />
          ) : (
            <>
              {/* Top KPI Metric Cards (Image 1 & 2 Style) */}
              <KpiRow stats={stats} />

              {/* Middle Section: Posture Radial Gauge + Categories + CISO Briefing */}
              {activeTab === 'dashboard' && (
                <AnalyticsSection
                  stats={stats}
                  executiveSummary={scanData.executive_summary}
                  domain={scanData.domain}
                />
              )}

              {/* Data Table View (Active in Dashboard, Actionable, or All tabs) */}
              {(activeTab === 'dashboard' || activeTab === 'actionable' || activeTab === 'all') && (
                <FindingsTable
                  results={activeTab === 'actionable' ? results.filter((r) => !r.is_false_positive) : results}
                  domain={scanData.domain}
                  onPatch={handlePatch}
                />
              )}

              {/* Raw Telemetry Tab */}
              {activeTab === 'raw' && (
                <div className="surface-card">
                  <div className="card-title-row">
                    <div>
                      <div className="card-heading">Raw Intelligence Telemetry</div>
                      <div className="card-subheading">Full JSON payload for {scanData.domain}</div>
                    </div>
                  </div>
                  <pre style={{
                    background: '#0f172a',
                    color: '#e2e8f0',
                    padding: '16px',
                    borderRadius: '8px',
                    fontFamily: 'JetBrains Mono, monospace',
                    fontSize: '12px',
                    maxHeight: '500px',
                    overflow: 'auto',
                    whiteSpace: 'pre-wrap',
                  }}>
                    {JSON.stringify(scanData, null, 2)}
                  </pre>
                </div>
              )}
            </>
          )}

          <footer className="footer-bar">
            Powered by <strong>SerpApi Intelligence</strong> · <strong>Google Gemini AI</strong> · React & FastAPI
          </footer>
        </main>
      </div>
    </div>
  )
}
