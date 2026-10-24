/**
 * App tests — verifies Pune Water Network AI routing, distinct pages, and GIS dashboard features
 */
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from '../App'

describe('Pune Water Network AI Dashboard — Routing & Distinct Pages', () => {
  it('renders the project branding and simulated data badge', () => {
    render(<App />)
    expect(screen.getByText(/Pune Water Network AI/i)).toBeInTheDocument()
    const simulatedElements = screen.getAllByText(/SIMULATED DATA/i)
    expect(simulatedElements.length).toBeGreaterThanOrEqual(1)
  })

  it('renders navigation links to all four routes', () => {
    render(<App />)
    expect(screen.getByRole('link', { name: /^Overview/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /^Network Map/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Alerts/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /^Maintenance/i })).toBeInTheDocument()
  })

  it('highlights the active navigation link based on current route', () => {
    render(<App initialEntries={['/']} />)
    const overviewLink = screen.getByRole('link', { name: /^Overview/i })
    expect(overviewLink.className).toContain('text-blue-600')
    expect(overviewLink.className).toContain('bg-white')
  })

  it('renders the Overview page with 3-column dashboard and bottom telemetry', () => {
    render(<App initialEntries={['/']} />)
    // Left panel
    expect(screen.getByText(/Asset Health & Pipeline Condition/i)).toBeInTheDocument()
    expect(screen.getAllByText(/Healthy/i).length).toBeGreaterThanOrEqual(1)
    expect(screen.getAllByText(/Critical/i).length).toBeGreaterThanOrEqual(1)

    // Center map
    expect(screen.getByText(/Pune Municipal Water Distribution/i)).toBeInTheDocument()
    expect(screen.getByText(/GIS Live/i)).toBeInTheDocument()
    expect(screen.getByText(/Pipelines \(8\)/i)).toBeInTheDocument()
    expect(screen.getByText(/Nodes \(9\)/i)).toBeInTheDocument()
    expect(screen.getAllByText(/Leaks \(3\)/i).length).toBeGreaterThanOrEqual(1)

    // Right panel
    expect(screen.getByText(/Alerts & Maintenance/i)).toBeInTheDocument()
    expect(screen.getByText(/Live Leak Anomaly Detections/i)).toBeInTheDocument()

    // Bottom panel
    expect(screen.getByText(/Simulation Engine/i)).toBeInTheDocument()
    expect(screen.getAllByText(/Composite Network Health/i).length).toBeGreaterThanOrEqual(1)
  })

  it('synchronizes asset selection between map and right panel in Overview', () => {
    render(<App initialEntries={['/']} />)
    const alertCard = screen.getByText(/Sudden Pressure Drop/i)
    fireEvent.click(alertCard)
    expect(screen.getByText(/Map Selected/i)).toBeInTheDocument()
  })

  it('renders the dedicated Network Map page at /network-map', () => {
    render(<App initialEntries={['/network-map']} />)
    expect(screen.getByText(/Pune Municipal Water Distribution Network — GIS View/i)).toBeInTheDocument()
    expect(screen.getByText(/Full GeoView/i)).toBeInTheDocument()
    expect(screen.getByText(/Pipelines \(8\)/i)).toBeInTheDocument()
    expect(screen.getByText(/Nodes \(9\)/i)).toBeInTheDocument()
    expect(screen.getByText(/Pipe Health:/i)).toBeInTheDocument()
  })

  it('renders the dedicated Alerts page at /alerts with severity filtering and details', () => {
    render(<App initialEntries={['/alerts']} />)
    expect(screen.getByRole('heading', { name: /Network Anomaly & Leak Alerts/i })).toBeInTheDocument()
    expect(screen.getByText(/All registered alerts/i)).toBeInTheDocument()
    expect(screen.getByText(/Alert Diagnostics & Inspection/i)).toBeInTheDocument()
    expect(screen.getAllByText(/Sudden Pressure Drop/i).length).toBeGreaterThanOrEqual(1)

    // Test severity filter button
    const criticalButtons = screen.getAllByRole('button', { name: /critical/i })
    expect(criticalButtons.length).toBeGreaterThanOrEqual(1)
    fireEvent.click(criticalButtons[0])
    expect(screen.getAllByText(/Sudden Pressure Drop/i).length).toBeGreaterThanOrEqual(1)
  })

  it('renders the dedicated Maintenance page at /maintenance with work orders and priority filtering', () => {
    render(<App initialEntries={['/maintenance']} />)
    expect(screen.getByRole('heading', { name: /Predictive Maintenance & Work Orders/i })).toBeInTheDocument()
    expect(screen.getByText(/Total Work Orders/i)).toBeInTheDocument()
    expect(screen.getByText(/Work Order Specification/i)).toBeInTheDocument()
    expect(screen.getAllByText(/WO-804/i).length).toBeGreaterThanOrEqual(1)
    expect(screen.getAllByText(/Emergency acoustic survey & pipe joint clamp/i).length).toBeGreaterThanOrEqual(1)

    // Test priority filter button
    const urgentButtons = screen.getAllByRole('button', { name: /urgent/i })
    expect(urgentButtons.length).toBeGreaterThanOrEqual(1)
    fireEvent.click(urgentButtons[0])
    expect(screen.getAllByText(/WO-804/i).length).toBeGreaterThanOrEqual(1)
  })

  it('navigates between routes when header links are clicked', () => {
    render(<App initialEntries={['/']} />)

    // Navigate to Alerts
    const alertsLink = screen.getByRole('link', { name: /Alerts/i })
    fireEvent.click(alertsLink)
    expect(screen.getByRole('heading', { name: /Network Anomaly & Leak Alerts/i })).toBeInTheDocument()

    // Navigate to Maintenance
    const maintenanceLink = screen.getByRole('link', { name: /^Maintenance/i })
    fireEvent.click(maintenanceLink)
    expect(screen.getByRole('heading', { name: /Predictive Maintenance & Work Orders/i })).toBeInTheDocument()

    // Navigate back to Overview
    const overviewLink = screen.getByRole('link', { name: /^Overview/i })
    fireEvent.click(overviewLink)
    expect(screen.getByText(/Asset Health & Pipeline Condition/i)).toBeInTheDocument()
  })
})
