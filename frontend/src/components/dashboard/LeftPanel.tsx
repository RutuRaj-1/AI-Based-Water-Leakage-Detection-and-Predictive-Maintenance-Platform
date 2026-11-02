import type { PipelineConditionCategory } from '../../types/dashboard'
import { Badge } from '../common/Badge'

interface LeftPanelProps {
  className?: string
}

export function LeftPanel({ className = '' }: LeftPanelProps) {
  // Illustrative pipeline condition distribution matching docs/gis-design.md
  const conditionCategories: PipelineConditionCategory[] = [
    {
      id: 'healthy',
      label: 'Healthy',
      range: '80–100 Score',
      percentage: 64,
      lengthKm: 284.2,
      color: '#16A34A', // Green
    },
    {
      id: 'monitor',
      label: 'Monitor',
      range: '60–79 Score',
      percentage: 21,
      lengthKm: 93.2,
      color: '#D97706', // Amber
    },
    {
      id: 'attention',
      label: 'Attention',
      range: '40–59 Score',
      percentage: 11,
      lengthKm: 48.8,
      color: '#EA580C', // Orange
    },
    {
      id: 'critical',
      label: 'Critical',
      range: '0–39 Score',
      percentage: 4,
      lengthKm: 17.8,
      color: '#DC2626', // Red
    },
  ]

  const assetMetrics = [
    { label: 'Total Network Length', value: '444.0 km', subtext: 'Simulated Network' },
    { label: 'Monitored Segments', value: '1,280 pipes', subtext: 'Cast Iron & DI mains' },
    { label: 'Pressure Junctions', value: '842 nodes', subtext: 'Simulated sensor nodes' },
    { label: 'Pumping Stations', value: '6 stations', subtext: 'Parvati, Cantonment, etc.' },
    { label: 'Storage Reservoirs', value: '14 tanks', subtext: 'Elevated & Ground reservoirs' },
    { label: 'District Metered Areas', value: '12 DMAs', subtext: 'Pune Municipal Area' },
  ]

  return (
    <aside
      className={`left-panel bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-5 shadow-xs overflow-y-auto ${className}`}
      aria-label="Asset Health and Network Statistics"
    >
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h2 className="text-sm font-bold tracking-wide uppercase text-slate-800">
            Asset Health &amp; Pipeline Condition
          </h2>
          <p className="text-[11px] text-slate-500">
            Real-time condition scoring &amp; telemetry
          </p>
        </div>
        <Badge variant="neutral" size="sm">
          Simulated
        </Badge>
      </div>

      {/* Network Health Score Hero Card */}
      <div className="rounded-lg bg-slate-50/80 border border-slate-200 p-4 relative overflow-hidden">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-600">
              Composite Network Health
            </span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-slate-900 tracking-tight">
                78.4
              </span>
              <span className="text-sm font-semibold text-slate-500">/ 100</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium ml-1">
                Good State
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Based on 1,280 simulated pipe telemetry streams
            </p>
          </div>

          {/* Circular Progress Ring */}
          <div className="relative w-16 h-16 flex items-center justify-center">
            <svg className="w-16 h-16 -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-slate-200 stroke-current"
                strokeWidth="3.5"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className="text-blue-600 stroke-current"
                strokeDasharray="78.4, 100"
                strokeWidth="3.5"
                strokeLinecap="round"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <span className="absolute text-xs font-bold text-slate-800">78%</span>
          </div>
        </div>

        {/* Mini progress bar breakdown */}
        <div className="mt-3.5 space-y-1.5">
          <div className="flex h-2 w-full overflow-hidden rounded-full bg-slate-200 gap-0.5">
            <div style={{ width: '64%' }} className="bg-[#16A34A]" title="Healthy: 64%" />
            <div style={{ width: '21%' }} className="bg-[#D97706]" title="Monitor: 21%" />
            <div style={{ width: '11%' }} className="bg-[#EA580C]" title="Attention: 11%" />
            <div style={{ width: '4%' }} className="bg-[#DC2626]" title="Critical: 4%" />
          </div>
          <div className="flex justify-between text-[10px] text-slate-500">
            <span>64% Good</span>
            <span>21% Fair</span>
            <span>15% At-Risk</span>
          </div>
        </div>
      </div>

      {/* Pipeline Condition Breakdown */}
      <div className="space-y-2.5">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold tracking-wide uppercase text-slate-700">
            Pipeline Health Distribution
          </h3>
          <span className="text-[10px] text-slate-500">Total 444 km</span>
        </div>

        <div className="space-y-2">
          {conditionCategories.map((cat) => (
            <div
              key={cat.id}
              className="bg-slate-50/70 border border-slate-200 rounded-lg p-2.5 hover:border-slate-300 transition-colors"
            >
              <div className="flex items-center justify-between text-xs mb-1.5">
                <div className="flex items-center gap-2">
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: cat.color }}
                  />
                  <span className="font-semibold text-slate-800">{cat.label}</span>
                  <span className="text-[10px] text-slate-500">({cat.range})</span>
                </div>
                <div className="flex items-baseline gap-1.5">
                  <span className="font-bold text-slate-900">{cat.percentage}%</span>
                  <span className="text-[11px] text-slate-500">({cat.lengthKm} km)</span>
                </div>
              </div>
              <div className="h-1.5 w-full bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{
                    width: `${cat.percentage}%`,
                    backgroundColor: cat.color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Compact Network Asset Statistics */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold tracking-wide uppercase text-slate-700">
            Monitored Assets
          </h3>
          <span className="text-[10px] text-slate-500">Simulated Counts</span>
        </div>

        <div className="grid grid-cols-2 gap-2">
          {assetMetrics.map((item) => (
            <div
              key={item.label}
              className="bg-slate-50/70 border border-slate-200 rounded-lg p-2.5 flex flex-col justify-between"
            >
              <span className="text-[10px] uppercase font-medium text-slate-500 tracking-wider">
                {item.label}
              </span>
              <span className="text-sm font-bold text-slate-900 mt-1">{item.value}</span>
              <span className="text-[9px] text-slate-500 mt-0.5 truncate">
                {item.subtext}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Illustrative Notice */}
      <div className="mt-auto pt-2 border-t border-slate-100 text-[10px] text-slate-400 flex items-center justify-between">
        <span>Dataset: Synthetic Pune WDN</span>
        <span>Version: v0.1.0-sim</span>
      </div>
    </aside>
  )
}
