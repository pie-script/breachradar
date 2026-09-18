const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export function scanDomain(domain) {
  return fetch(`${API_BASE}/api/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain }),
  }).then(handle)
}

export function generatePatch(link, riskSummary) {
  return fetch(`${API_BASE}/api/patch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ link, risk_summary: riskSummary }),
  }).then(handle)
}

/** Client-side CSV export — no backend round trip needed for this. */
export function downloadResultsCsv(results, domain) {
  if (!results.length) return
  const headers = Object.keys(results[0])
  const escapeCell = (v) => {
    const s = v === null || v === undefined ? '' : String(v)
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
  }
  const rows = [
    headers.join(','),
    ...results.map((r) => headers.map((h) => escapeCell(r[h])).join(',')),
  ]
  const blob = new Blob([rows.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `breachradar_${domain}_report.csv`
  a.click()
  URL.revokeObjectURL(url)
}
