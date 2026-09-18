export default function WorkspaceBar({ domain }) {
  return (
    <div className="workspace-bar">
      <div className="workspace-context">
        <span className="status-dot" />
        <span>PASSIVE RECON WORKSPACE</span>
      </div>
      <div className="workspace-target">
        <span className="workspace-label">TARGET</span>
        <code>{domain || 'No target selected'}</code>
        <span>🔒</span>
      </div>
    </div>
  )
}
