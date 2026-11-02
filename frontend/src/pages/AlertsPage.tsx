import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { DashboardLayout } from '../layouts/DashboardLayout'
import { TopNavbar } from '../components/dashboard/TopNavbar'
import { Badge } from '../components/common/Badge'
import { simulatedAlerts, criticalAssets } from '../data/dashboardData'
import type { SeverityLevel } from '../types/dashboard'

export function AlertsPage() {
  const [selectedAlertId, setSelectedAlertId] = useState<string>(simulatedAlerts[0]?.id || '')
  const [severityFilter, setSeverityFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState<string>('')

  // Filter alerts by severity and search query
  const filteredAlerts = useMemo(() => {
    return simulatedAlerts.filter((alert) => {
      const matchesSeverity =
        severityFilter === 'all' || alert.severity === severityFilter

      const matchesSearch =
        searchQuery === '' ||
        alert.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.pipelineId.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.id.toLowerCase().includes(searchQuery.toLowerCase())

      return matchesSeverity && matchesSearch
    })
  }, [severityFilter, searchQuery])

  // Current selected alert
  const selectedAlert = useMemo(() => {
    return (
      simulatedAlerts.find((a) => a.id === selectedAlertId) ||
      filteredAlerts[0] ||
      simulatedAlerts[0]
    )
  }, [selectedAlertId, filteredAlerts])

  // Matched critical asset if any
  const matchedAsset = useMemo(() => {
    if (!selectedAlert) return null
    const cleanId = selectedAlert.pipelineId.replace('Pipe ', '').trim()
    return criticalAssets.find((asset) => asset.id === cleanId)
  }, [selectedAlert])

  const countsBySeverity = useMemo(() => {
    return {
      all: simulatedAlerts.length,
      critical: simulatedAlerts.filter((a) => a.severity === 'critical').length,
      high: simulatedAlerts.filter((a) => a.severity === 'high').length,
      moderate: simulatedAlerts.filter((a) => a.severity === 'moderate').length,
      low: simulatedAlerts.filter((a) => a.severity === 'low').length,
      normal: simulatedAlerts.filter((a) => a.severity === 'normal').length,
    }
  }, [])

  return (
    <DashboardLayout topNavbar={<TopNavbar />}>
      <div className="flex flex-col gap-4 max-w-[1920px] mx-auto w-full pb-8">
        {/* Page Header */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xs">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-rose-100 text-rose-700 flex items-center justify-center font-bold">
                <svg
                  className="w-5 h-5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                  <line x1="12" y1="9" x2="12" y2="13" />
                  <line x1="12" y1="17" x2="12.01" y2="17" />
                </svg>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-lg font-bold text-slate-900 tracking-tight">
                    Network Anomaly &amp; Leak Alerts
                  </h1>
                  <Badge variant="critical" size="sm">
                    {countsBySeverity.critical + countsBySeverity.high} Urgent
                  </Badge>
                </div>
                <p className="text-xs text-slate-500">
                  Simulated anomaly detections derived from acoustic noise logs and pressure transient monitoring
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Badge variant="neutral" size="md">
              <span className="text-[11px] font-semibold text-slate-700 uppercase">
                Synthetic Feed · v0.2
              </span>
            </Badge>
            <Link
              to="/network-map"
              className="px-3 py-1.5 rounded-lg bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700 shadow-xs transition-colors flex items-center gap-1.5"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" />
                <line x1="8" y1="2" x2="8" y2="18" />
                <line x1="16" y1="6" x2="16" y2="22" />
              </svg>
              Open GIS Map
            </Link>
          </div>
        </div>

        {/* Severity Metric Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <button
            type="button"
            onClick={() => setSeverityFilter('all')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              severityFilter === 'all'
                ? 'bg-blue-50/80 border-blue-400 ring-2 ring-blue-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-slate-500 block">Total Alerts</span>
            <span className="text-2xl font-bold text-slate-900 block mt-0.5">{countsBySeverity.all}</span>
            <span className="text-[10px] text-slate-500 mt-1 block">All registered alerts</span>
          </button>

          <button
            type="button"
            onClick={() => setSeverityFilter('critical')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              severityFilter === 'critical'
                ? 'bg-rose-50 border-rose-400 ring-2 ring-rose-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-rose-600 block">Critical</span>
            <span className="text-2xl font-bold text-rose-700 block mt-0.5">{countsBySeverity.critical}</span>
            <span className="text-[10px] text-rose-600 font-medium mt-1 block">Immediate action</span>
          </button>

          <button
            type="button"
            onClick={() => setSeverityFilter('high')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              severityFilter === 'high'
                ? 'bg-amber-50 border-amber-400 ring-2 ring-amber-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-amber-600 block">High</span>
            <span className="text-2xl font-bold text-amber-700 block mt-0.5">{countsBySeverity.high}</span>
            <span className="text-[10px] text-amber-600 font-medium mt-1 block">Rapid response</span>
          </button>

          <button
            type="button"
            onClick={() => setSeverityFilter('moderate')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              severityFilter === 'moderate'
                ? 'bg-orange-50 border-orange-400 ring-2 ring-orange-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-orange-600 block">Moderate</span>
            <span className="text-2xl font-bold text-orange-700 block mt-0.5">{countsBySeverity.moderate}</span>
            <span className="text-[10px] text-slate-500 mt-1 block">Under monitoring</span>
          </button>

          <button
            type="button"
            onClick={() => setSeverityFilter('low')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              severityFilter === 'low'
                ? 'bg-sky-50 border-sky-400 ring-2 ring-sky-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-sky-600 block">Low</span>
            <span className="text-2xl font-bold text-sky-700 block mt-0.5">{countsBySeverity.low}</span>
            <span className="text-[10px] text-slate-500 mt-1 block">Minor deviation</span>
          </button>

          <button
            type="button"
            onClick={() => setSeverityFilter('normal')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              severityFilter === 'normal'
                ? 'bg-emerald-50 border-emerald-400 ring-2 ring-emerald-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-emerald-600 block">Resolved / Normal</span>
            <span className="text-2xl font-bold text-emerald-700 block mt-0.5">{countsBySeverity.normal}</span>
            <span className="text-[10px] text-emerald-600 font-medium mt-1 block">Restored</span>
          </button>
        </div>

        {/* Filter and Search Bar */}
        <div className="bg-white border border-slate-200 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 shadow-xs">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs font-semibold text-slate-600 mr-1">Severity:</span>
            {(['all', 'critical', 'high', 'moderate', 'low', 'normal'] as const).map((sev) => (
              <button
                key={sev}
                type="button"
                onClick={() => setSeverityFilter(sev)}
                className={`px-3 py-1 rounded-md text-xs font-medium capitalize transition-all cursor-pointer ${
                  severityFilter === sev
                    ? 'bg-blue-600 text-white font-semibold shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {sev === 'all' ? 'All Severities' : sev}
              </button>
            ))}
          </div>

          <div className="relative w-full sm:w-72">
            <input
              type="text"
              placeholder="Search by ID, pipe, or zone..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200 bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-400 text-slate-800 placeholder-slate-400"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1.5 text-xs text-slate-400 hover:text-slate-600"
              >
                Clear
              </button>
            )}
          </div>
        </div>

        {/* Main 2-Column Alerts Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Column 1: Alert List (7 cols) */}
          <div className="lg:col-span-7 flex flex-col gap-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                Alerts ({filteredAlerts.length})
              </span>
              <span className="text-[11px] text-slate-500">
                Select an alert card to inspect diagnostics
              </span>
            </div>

            {filteredAlerts.length === 0 ? (
              <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">
                <p className="font-medium text-sm">No alerts match the selected criteria.</p>
                <button
                  type="button"
                  onClick={() => {
                    setSeverityFilter('all')
                    setSearchQuery('')
                  }}
                  className="mt-2 text-xs text-blue-600 font-semibold hover:underline"
                >
                  Reset filters
                </button>
              </div>
            ) : (
              filteredAlerts.map((alert) => {
                const isSelected = alert.id === selectedAlert?.id
                return (
                  <div
                    key={alert.id}
                    onClick={() => setSelectedAlertId(alert.id)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        setSelectedAlertId(alert.id)
                      }
                    }}
                    className={`bg-white border rounded-xl p-4 transition-all cursor-pointer relative shadow-xs ${
                      isSelected
                        ? 'border-blue-500 ring-2 ring-blue-500/20 bg-blue-50/30'
                        : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50/50'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1.5">
                          <Badge
                            variant={alert.severity as SeverityLevel}
                            size="sm"
                            pulsing={alert.severity === 'critical'}
                          >
                            {alert.severity.toUpperCase()}
                          </Badge>
                          <span className="text-xs font-mono font-bold text-slate-700">
                            {alert.id}
                          </span>
                          <span className="text-[11px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200 capitalize">
                            {alert.status}
                          </span>
                          <span className="text-[11px] text-slate-400 ml-auto">
                            {alert.timestamp}
                          </span>
                        </div>

                        <h3 className="text-sm font-bold text-slate-900 leading-snug">
                          {alert.title}
                        </h3>

                        <div className="mt-2 grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs text-slate-600 pt-2 border-t border-slate-100">
                          <div>
                            <span className="text-slate-400 block text-[10px] uppercase font-medium">Pipeline</span>
                            <span className="font-semibold text-slate-800">{alert.pipelineId}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px] uppercase font-medium">Location</span>
                            <span className="font-medium text-slate-800">{alert.location}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px] uppercase font-medium">Estimated Loss</span>
                            <span className="font-bold text-rose-600">{alert.estimatedLoss}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>

          {/* Column 2: Selected Alert Details & Asset Info (5 cols) */}
          <div className="lg:col-span-5">
            {selectedAlert ? (
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs sticky top-20 flex flex-col gap-4">
                <div className="border-b border-slate-100 pb-3 flex items-start justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500">
                      Alert Diagnostics &amp; Inspection
                    </span>
                    <h2 className="text-base font-bold text-slate-900 mt-0.5">
                      {selectedAlert.id} · {selectedAlert.title}
                    </h2>
                  </div>
                  <Badge variant={selectedAlert.severity as SeverityLevel} size="md">
                    {selectedAlert.severity.toUpperCase()}
                  </Badge>
                </div>

                {/* Telemetry Snapshot */}
                <div className="space-y-2 text-xs">
                  <span className="text-xs font-bold text-slate-700 block uppercase tracking-wide">
                    Telemetry Observations
                  </span>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-[10px] uppercase font-semibold text-slate-500">Loss Rate</span>
                      <p className="text-sm font-bold text-rose-600 mt-0.5">{selectedAlert.estimatedLoss}</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-[10px] uppercase font-semibold text-slate-500">First Detected</span>
                      <p className="text-sm font-semibold text-slate-800 mt-0.5">{selectedAlert.timestamp}</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-[10px] uppercase font-semibold text-slate-500">DMA / Sector</span>
                      <p className="text-sm font-medium text-slate-800 mt-0.5">{selectedAlert.location}</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-[10px] uppercase font-semibold text-slate-500">AI Confidence</span>
                      <p className="text-sm font-bold text-blue-600 mt-0.5">94.8% ML Match</p>
                    </div>
                  </div>
                </div>

                {/* Associated Asset Info */}
                <div className="space-y-2 text-xs">
                  <span className="text-xs font-bold text-slate-700 block uppercase tracking-wide">
                    Associated Asset Profile
                  </span>
                  {matchedAsset ? (
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-900">{matchedAsset.name}</span>
                        <span className={`text-[11px] font-bold px-1.5 py-0.5 rounded ${
                          matchedAsset.healthScore < 30 ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                        }`}>
                          Health {matchedAsset.healthScore}%
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-x-2 gap-y-1 text-[11px] text-slate-600">
                        <div>
                          <strong className="text-slate-800">Material:</strong> {matchedAsset.material}
                        </div>
                        <div>
                          <strong className="text-slate-800">Age:</strong> {matchedAsset.ageYears} years
                        </div>
                        <div className="col-span-2">
                          <strong className="text-slate-800">Zone:</strong> {matchedAsset.zone}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-slate-600">
                      <p className="font-semibold text-slate-800">{selectedAlert.pipelineId}</p>
                      <p className="text-[11px] mt-0.5">Location: {selectedAlert.location}</p>
                    </div>
                  )}
                </div>

                {/* Recommended Mitigation */}
                <div className="p-3 rounded-lg bg-blue-50/70 border border-blue-200 text-xs">
                  <span className="font-bold text-blue-900 block mb-1">
                    AI Recommended Intervention
                  </span>
                  <p className="text-blue-800 text-[11px] leading-relaxed">
                    Prioritize acoustic correlation survey on {selectedAlert.pipelineId} and inspect branch valves. Rapid pipe joint clamping recommended within 4 hours to prevent hydraulic cavitation.
                  </p>
                </div>

                {/* Quick Actions */}
                <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
                  <Link
                    to="/network-map"
                    className="flex-1 text-center py-2 px-3 rounded-lg bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700 shadow-xs transition-colors"
                  >
                    Locate on GIS Map
                  </Link>
                  <Link
                    to="/maintenance"
                    className="flex-1 text-center py-2 px-3 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold hover:bg-slate-200 transition-colors"
                  >
                    Manage Work Order
                  </Link>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
