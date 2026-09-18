import { useState, useMemo } from 'react'
import Sidebar from './components/Sidebar.jsx'
import WorkspaceBar from './components/WorkspaceBar.jsx'
import Hero from './components/Hero.jsx'
import IdleState from './components/IdleState.jsx'
import AnalyticsDashboard from './components/AnalyticsDashboard.jsx'
import ExecutiveSummary from './components/ExecutiveSummary.jsx'
import FiltersBar from './components/FiltersBar.jsx'
import ResultsTabs from './components/ResultsTabs.jsx'
import { scanDomain, generatePatch } from './api.js'

export default function App() {
  const [domain, setDomain] = useState('testphp.vulnweb.com')
  const [loading, setLoading] = useState(false)
  const [scanData, setScanData] = useState(null)
  const [error, setError] = useState(null)

  const [severityFilter, setSeverityFilter] = useState('All')
  const [categoryFilter, setCategoryFilter] = useState('All')
  const [showNoise, setShowNoise] = useState(false)

  const handleScan = async () => {
    if (!domain.trim()) {
      setError('Please enter a target domain.')
      return
    }
    setError(null)
    setLoading(true)
    try {
      const data = await scanDomain(domain.trim())
      setScanData(data)
    } catch (err) {
      setError(err.message || 'Failed to scan target domain.')
    } finally {
      setLoading(false)
    }
  }

  const handlePatch = async (link, riskSummary) => {
    return await generatePatch(link, riskSummary)
  }

  const results = scanData?.results || []
  const stats = scanData?.stats || null

  const actionableResults = useMemo(() => {
    return results.filter((r) => !r.is_false_positive)
  }, [results])

  const visibleResults = useMemo(() => {
    return results.filter((item) => {
      if (!showNoise && item.is_false_positive) return false
      if (severityFilter !== 'All' && item.severity !== severityFilter) return false
      if (categoryFilter !== 'All' && item.category !== categoryFilter) return false
      return true
    })
  }, [results, severityFilter, categoryFilter, showNoise])

  const visibleActionable = useMemo(() => {
    return visibleResults.filter((r) => !r.is_false_positive)
  }, [visibleResults])

  return (
    <div className="app-shell">
      <Sidebar
        domain={domain}
        setDomain={setDomain}
        onScan={handleScan}
        loading={loading}
        isComplete={Boolean(scanData)}
        error={error}
      />

      <main className="main-col">
        <WorkspaceBar domain={scanData?.domain || domain} />
        <Hero />

        {!scanData ? (
          <IdleState />
        ) : (
          <>
            <AnalyticsDashboard stats={stats} domain={scanData.domain} />
            <ExecutiveSummary summary={scanData.executive_summary} domain={scanData.domain} />
            <FiltersBar
              severityFilter={severityFilter}
              setSeverityFilter={setSeverityFilter}
              categoryFilter={categoryFilter}
              setCategoryFilter={setCategoryFilter}
              showNoise={showNoise}
              setShowNoise={setShowNoise}
              categories={stats?.categories || []}
            />
            <ResultsTabs
              results={results}
              actionableResults={actionableResults}
              visibleResults={visibleResults}
              visibleActionable={visibleActionable}
              rawFindings={scanData.raw_findings}
              domain={scanData.domain}
              onPatch={handlePatch}
            />
          </>
        )}

        <footer className="br-footer">
          <div className="br-footer-text">
            Built with <strong>SerpApi</strong> Search Intelligence · <strong>Gemini AI</strong> · React & FastAPI
          </div>
        </footer>
      </main>
    </div>
  )
}
