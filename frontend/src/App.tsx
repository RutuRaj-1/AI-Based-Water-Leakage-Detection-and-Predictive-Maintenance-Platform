/**
 * App.tsx — Pune Water Network AI
 *
 * Foundation stage: minimal application shell.
 * This is only a placeholder to confirm the React application starts.
 * No real dashboard, GIS map, charts, or authentication is implemented here.
 *
 * Future: Replace with React Router <RouterProvider> and full application layout.
 */

import './App.css'

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-badge">Foundation · Stage 1</div>
        <h1 className="app-title">
          <span className="title-accent">Pune</span> Water Network AI
        </h1>
        <p className="app-subtitle">
          AI-Based Water Distribution Network Leakage Detection<br />
          &amp; Predictive Asset Management Platform
        </p>
      </header>

      <main className="app-main">
        <div className="status-grid">
          <StatusCard
            icon="🟢"
            title="Frontend"
            status="Running"
            note="Vite + React + TypeScript"
          />
          <StatusCard
            icon="⚙️"
            title="Backend"
            status="See setup guide"
            note="FastAPI — run uvicorn separately"
          />
          <StatusCard
            icon="🗄️"
            title="Database"
            status="Not connected"
            note="PostgreSQL/PostGIS — start with docker compose"
          />
          <StatusCard
            icon="🤖"
            title="AI/ML"
            status="Planned"
            note="Anomaly detection · Health scoring · Risk prediction"
          />
        </div>

        <div className="info-box">
          <p>
            This is the <strong>foundation scaffold</strong>. The complete product
            — hydraulic simulation, GIS dashboard, anomaly detection, pipeline health
            scoring, and maintenance prioritisation — will be built in subsequent stages.
          </p>
          <p>
            See <code>docs/architecture.md</code> for the planned system design
            and <code>docs/setup-guide.md</code> to start all services.
          </p>
        </div>

        <div className="team-section">
          <h2>Team</h2>
          <div className="team-grid">
            <TeamMember name="Ruturaj" role="Team Lead · DB · Integration" />
            <TeamMember name="Sanskar" role="Backend · Simulation" />
            <TeamMember name="Shardul" role="Backend · AI/ML" />
            <TeamMember name="Bhargavi" role="Frontend · GIS Dashboard" />
          </div>
        </div>
      </main>

      <footer className="app-footer">
        Pune Water Network AI · v0.1.0 · Foundation Stage
      </footer>
    </div>
  )
}

interface StatusCardProps {
  icon: string
  title: string
  status: string
  note: string
}

function StatusCard({ icon, title, status, note }: StatusCardProps) {
  return (
    <div className="status-card">
      <div className="status-icon">{icon}</div>
      <div className="status-title">{title}</div>
      <div className="status-value">{status}</div>
      <div className="status-note">{note}</div>
    </div>
  )
}

interface TeamMemberProps {
  name: string
  role: string
}

function TeamMember({ name, role }: TeamMemberProps) {
  return (
    <div className="team-member">
      <div className="member-avatar">{name[0]}</div>
      <div>
        <div className="member-name">{name}</div>
        <div className="member-role">{role}</div>
      </div>
    </div>
  )
}

export default App
