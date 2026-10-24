import { useState } from 'react'
import { Badge } from '../common/Badge'
import {
  simulatedAlerts,
  criticalAssets,
  maintenanceTasks,
} from '../../data/dashboardData'

interface RightPanelProps {
  className?: string
  selectedAssetId?: string | null
  onSelectAsset?: (assetId: string) => void
}

export function RightPanel({
  className = '',
  selectedAssetId = null,
  onSelectAsset,
}: RightPanelProps) {
  const [activeTab, setActiveTab] = useState<'alerts' | 'assets' | 'maintenance'>('alerts')

  const isMatched = (id: string, refId?: string) => {
    if (!selectedAssetId) return false
    const cleanRef = refId?.replace('Pipe ', '').trim()
    return (
      id === selectedAssetId ||
      cleanRef === selectedAssetId ||
      selectedAssetId.includes(id) ||
      (cleanRef ? selectedAssetId.includes(cleanRef) : false)
    )
  }

  return (
    <aside
      className={`right-panel bg-white border border-slate-200 rounded-xl p-4 flex flex-col gap-4 shadow-xs overflow-y-auto ${className}`}
      aria-label="Alerts and Maintenance Panel"
    >
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h2 className="text-sm font-bold tracking-wide uppercase text-slate-800">
            Alerts &amp; Maintenance
          </h2>
          <p className="text-[11px] text-slate-500">
            AI leak anomalies &amp; predictive action list
          </p>
        </div>
        <Badge variant="critical" size="sm">
          3 Active
        </Badge>
      </div>

      {/* Segmented Filter Buttons */}
      <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
        <button
          type="button"
          onClick={() => setActiveTab('alerts')}
          className={`py-1.5 px-2 rounded font-medium transition-all text-center cursor-pointer ${
            activeTab === 'alerts'
              ? 'bg-white text-blue-600 shadow-xs font-semibold'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          Leaks ({simulatedAlerts.length})
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('assets')}
          className={`py-1.5 px-2 rounded font-medium transition-all text-center cursor-pointer ${
            activeTab === 'assets'
              ? 'bg-white text-blue-600 shadow-xs font-semibold'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          Critical ({criticalAssets.length})
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('maintenance')}
          className={`py-1.5 px-2 rounded font-medium transition-all text-center cursor-pointer ${
            activeTab === 'maintenance'
              ? 'bg-white text-blue-600 shadow-xs font-semibold'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          Work Orders
        </button>
      </div>

      {/* Tab 1: Simulated Leak Alerts */}
      {activeTab === 'alerts' && (
        <div className="space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wide text-slate-600">
              Live Leak Anomaly Detections
            </span>
            <span className="text-[10px] text-blue-600 font-medium">Illustrative Feed</span>
          </div>

          <div className="space-y-2">
            {simulatedAlerts.map((alert) => {
              const matched = isMatched(alert.id, alert.pipelineId)
              return (
                <div
                  key={alert.id}
                  onClick={() =>
                    onSelectAsset?.(alert.pipelineId.replace('Pipe ', '').trim())
                  }
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      onSelectAsset?.(alert.pipelineId.replace('Pipe ', '').trim())
                    }
                  }}
                  className={`border rounded-lg p-3 transition-all relative cursor-pointer ${
                    matched
                      ? 'bg-blue-50/80 border-blue-400 ring-2 ring-blue-500/20 shadow-xs'
                      : 'bg-slate-50/60 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge
                          variant={alert.severity}
                          size="sm"
                          pulsing={alert.severity === 'critical'}
                        >
                          {alert.severity.toUpperCase()}
                        </Badge>
                        <span className="text-[11px] font-mono text-slate-500">
                          {alert.id}
                        </span>
                        {matched && (
                          <span className="text-[10px] uppercase font-bold text-blue-600 ml-1">
                            Map Selected
                          </span>
                        )}
                        <span className="text-[11px] text-slate-400 ml-auto">
                          {alert.timestamp}
                        </span>
                      </div>

                      <h4 className="text-xs font-semibold text-slate-900">
                        {alert.title}
                      </h4>

                      <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-slate-500">
                        <span>
                          <strong className="text-slate-700 font-medium">Asset:</strong>{' '}
                          {alert.pipelineId}
                        </span>
                        <span>
                          <strong className="text-slate-700 font-medium">Loc:</strong>{' '}
                          {alert.location}
                        </span>
                        <span className="text-red-600 font-semibold">
                          Loss: {alert.estimatedLoss}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Tab 2: Critical Assets Watchlist */}
      {activeTab === 'assets' && (
        <div className="space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wide text-slate-600">
              High Risk Infrastructure
            </span>
            <span className="text-[10px] text-amber-700 font-medium">Score &lt; 50</span>
          </div>

          <div className="space-y-2">
            {criticalAssets.map((asset) => {
              const matched = isMatched(asset.id)
              return (
                <div
                  key={asset.id}
                  onClick={() => onSelectAsset?.(asset.id)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      onSelectAsset?.(asset.id)
                    }
                  }}
                  className={`border rounded-lg p-3 transition-all cursor-pointer ${
                    matched
                      ? 'bg-blue-50/80 border-blue-400 ring-2 ring-blue-500/20 shadow-xs'
                      : 'bg-slate-50/60 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <h4 className="text-xs font-semibold text-slate-900">{asset.name}</h4>
                    <span
                      className={`text-xs font-bold px-1.5 py-0.5 rounded ${
                        asset.healthScore < 30
                          ? 'bg-red-50 text-red-700 border border-red-200'
                          : 'bg-amber-50 text-amber-800 border border-amber-200'
                      }`}
                    >
                      Health: {asset.healthScore}%
                    </span>
                  </div>

                  <div className="space-y-1 text-[11px] text-slate-500">
                    <div className="flex justify-between">
                      <span>Material / Spec:</span>
                      <span className="text-slate-800 font-medium">{asset.material}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Age / Zone:</span>
                      <span className="text-slate-800 font-medium">
                        {asset.ageYears} yrs · {asset.zone}
                      </span>
                    </div>
                  </div>

                  <div className="mt-2 h-1.5 w-full bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        asset.healthScore < 30 ? 'bg-[#DC2626]' : 'bg-[#D97706]'
                      }`}
                      style={{ width: `${asset.healthScore}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Tab 3: Maintenance Priorities */}
      {activeTab === 'maintenance' && (
        <div className="space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wide text-slate-600">
              AI-Ranked Work Orders
            </span>
            <span className="text-[10px] text-blue-600 font-medium">Predictive Urgency</span>
          </div>

          <div className="space-y-2">
            {maintenanceTasks.map((task) => (
              <div
                key={task.id}
                className="bg-slate-50/60 border border-slate-200 hover:border-slate-300 hover:bg-slate-50 rounded-lg p-3 transition-colors"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                    {task.workOrderNumber}
                  </span>
                  <div className="flex items-center gap-1.5">
                    <span className="text-[11px] text-slate-500">Score:</span>
                    <span className="text-xs font-bold text-blue-600">
                      {task.priorityScore}/100
                    </span>
                  </div>
                </div>

                <h4 className="text-xs font-medium text-slate-900 mt-1 leading-snug">
                  {task.title}
                </h4>

                <div className="mt-2 pt-2 border-t border-slate-200/80 flex items-center justify-between text-[10px] text-slate-500">
                  <span className="text-slate-700 font-medium">{task.targetAsset}</span>
                  <span className="text-amber-800 font-semibold">{task.dueDate}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Summary Footnote */}
      <div className="mt-auto pt-3 border-t border-slate-100 text-[10px] text-slate-500 flex items-center justify-between">
        <span>Anomaly Engine: ML-Isolation Forest</span>
        <span className="text-blue-600 font-medium">Confidence: 91.2%</span>
      </div>
    </aside>
  )
}
