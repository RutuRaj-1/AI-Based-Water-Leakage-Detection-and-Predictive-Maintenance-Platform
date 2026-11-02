/**
 * App.tsx — Pune Water Network AI
 *
 * Dedicated multi-page routing configuration:
 * - /             → Overview (3-column layout: health score, central map, alerts summary, telemetry KPIs)
 * - /network-map  → Dedicated expanded GIS water distribution network map
 * - /alerts       → Anomaly & leak alerts feed with severity filtering and asset diagnostics
 * - /maintenance  → Predictive maintenance work orders with priority scoring and asset profiles
 */

import { BrowserRouter, MemoryRouter, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'
import { OverviewPage } from './pages/OverviewPage'
import { NetworkMapPage } from './pages/NetworkMapPage'
import { AlertsPage } from './pages/AlertsPage'
import { MaintenancePage } from './pages/MaintenancePage'
import { DashboardDataProvider } from './context/DashboardDataProvider'

export interface AppProps {
  initialEntries?: string[]
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<OverviewPage />} />
      <Route path="/network-map" element={<NetworkMapPage />} />
      <Route path="/alerts" element={<AlertsPage />} />
      <Route path="/maintenance" element={<MaintenancePage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

// Background polling is disabled under test so suites stay deterministic.
const POLL_MS = import.meta.env.MODE === 'test' ? 0 : 3000

export function App({ initialEntries }: AppProps = {}) {
  const routes =
    initialEntries && initialEntries.length > 0 ? (
      <MemoryRouter initialEntries={initialEntries}>
        <AppRoutes />
      </MemoryRouter>
    ) : (
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    )

  return <DashboardDataProvider pollMs={POLL_MS}>{routes}</DashboardDataProvider>
}

export default App
