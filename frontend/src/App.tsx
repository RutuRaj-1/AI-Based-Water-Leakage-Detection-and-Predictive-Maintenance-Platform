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

export function App({ initialEntries }: AppProps = {}) {
  if (initialEntries && initialEntries.length > 0) {
    return (
      <MemoryRouter initialEntries={initialEntries}>
        <AppRoutes />
      </MemoryRouter>
    )
  }

  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  )
}

export default App
