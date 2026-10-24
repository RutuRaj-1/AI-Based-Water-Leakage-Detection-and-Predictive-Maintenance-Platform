import type { SimulationTelemetry } from '../../types/dashboard'
import { Badge } from '../common/Badge'

interface BottomPanelProps {
  className?: string
}

export function BottomPanel({ className = '' }: BottomPanelProps) {
  const telemetry: SimulationTelemetry = {
    scenarioName: 'Pune Morning Peak Demand (Simulated)',
    timeStep: 'Step 32 / 96 · T+08:00 hrs',
    engineStatus: 'running',
    meanPressureBar: 3.42,
    totalFlowMld: 14.8,
    estimatedLossPct: 3.8,
    activeLeaksCount: 3,
    totalMonitoredPipes: 1280,
    totalNodes: 842,
    networkHealthScore: 78.4,
  }

  const statItems = [
    {
      label: 'Composite Network Health',
      value: `${telemetry.networkHealthScore}%`,
      badge: 'Good State',
      badgeVariant: 'normal' as const,
      subtext: '96% assets in service',
    },
    {
      label: 'Monitored Assets',
      value: '2,122 Items',
      badge: 'Active Scada',
      badgeVariant: 'info' as const,
      subtext: `${telemetry.totalMonitoredPipes} pipes · ${telemetry.totalNodes} nodes`,
    },
    {
      label: 'Simulated Leak Detections',
      value: `${telemetry.activeLeaksCount} Anomalies`,
      badge: 'Attention',
      badgeVariant: 'critical' as const,
      subtext: 'Estimated loss ~66.5 m³/hr',
    },
    {
      label: 'System Pressure (Mean)',
      value: `${telemetry.meanPressureBar} bar`,
      badge: 'Nominal',
      badgeVariant: 'normal' as const,
      subtext: 'Min 2.1 bar · Max 4.8 bar',
    },
    {
      label: 'Current Total Flow',
      value: `${telemetry.totalFlowMld} MLD`,
      badge: 'Peak Hour',
      badgeVariant: 'accent' as const,
      subtext: `Unaccounted loss: ~${telemetry.estimatedLossPct}%`,
    },
  ]

  return (
    <footer
      className={`bottom-panel bg-white border-t border-slate-200 p-3 sm:p-4 text-slate-800 shadow-xs ${className}`}
      aria-label="Simulation and Network Summary"
    >
      <div className="max-w-[1920px] mx-auto flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
        {/* Left: Simulation Engine Status */}
        <div className="flex items-center gap-3.5 bg-slate-50 border border-slate-200 rounded-lg p-2.5 sm:px-3.5 min-w-[280px]">
          <div className="relative flex items-center justify-center w-9 h-9 rounded-md bg-blue-50 border border-blue-200 text-blue-600">
            {/* Simulation Gear / Pulse SVG */}
            <svg
              className="w-5 h-5 animate-[spin_6s_linear_infinite]"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-800 uppercase tracking-wide">
                Simulation Engine
              </span>
              <Badge variant="normal" size="sm" pulsing>
                Active
              </Badge>
            </div>
            <div className="text-[11px] text-slate-700 font-medium truncate">
              {telemetry.scenarioName}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              EPANET / WNTR Model · {telemetry.timeStep}
            </div>
          </div>
        </div>

        {/* Center / Right: Live KPI Stat Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 flex-1">
          {statItems.map((item) => (
            <div
              key={item.label}
              className="bg-slate-50 border border-slate-200 rounded-lg p-2.5 flex flex-col justify-between hover:border-slate-300 transition-colors shadow-2xs"
            >
              <div className="flex items-center justify-between gap-1 mb-1">
                <span className="text-[10px] uppercase font-semibold text-slate-500 tracking-wider truncate">
                  {item.label}
                </span>
                <Badge variant={item.badgeVariant} size="sm">
                  {item.badge}
                </Badge>
              </div>
              <div className="text-base font-bold text-slate-900 tracking-tight">
                {item.value}
              </div>
              <div className="text-[10px] text-slate-500 truncate mt-0.5">
                {item.subtext}
              </div>
            </div>
          ))}
        </div>
      </div>
    </footer>
  )
}
