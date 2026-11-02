import { useState } from 'react'
import { useDashboardData } from '../../context/dashboardDataContext'

/**
 * Backend connection indicator + live-simulation operator controls.
 * Controls are disabled while the backend is unreachable.
 */
export function SimulationControls() {
  const { data, connection, lastUpdated, simulationControl, injectLeak } = useDashboardData()
  const [busy, setBusy] = useState(false)
  const live = connection === 'live'
  const paused = data.simulation.paused

  const run = async (fn: () => Promise<void>) => {
    setBusy(true)
    try {
      await fn()
    } finally {
      setBusy(false)
    }
  }

  const handleInject = () => {
    const alerting = new Set(
      data.alerts.filter((a) => a.status !== 'resolved').map((a) => a.pipelineId.replace('Pipe ', '').trim()),
    )
    const candidates = data.pipelines.features.map((f) => f.properties.id).filter((id) => !alerting.has(id))
    if (candidates.length === 0) return
    const target = candidates[Math.floor(Math.random() * candidates.length)]
    void run(() => injectLeak(target, 15 + Math.round(Math.random() * 30)))
  }

  const pill =
    connection === 'live'
      ? { text: `API live · ${data.telemetry.timeStep.split(' · ')[0]}`, cls: 'bg-emerald-50 text-emerald-700 border-emerald-200', dot: 'bg-emerald-500' }
      : connection === 'connecting'
        ? { text: 'Connecting to API…', cls: 'bg-slate-50 text-slate-600 border-slate-200', dot: 'bg-slate-400' }
        : { text: 'API offline · demo data', cls: 'bg-amber-50 text-amber-700 border-amber-200', dot: 'bg-amber-500' }

  const btn =
    'px-2 py-1 rounded-md text-[11px] font-semibold border border-slate-200 bg-white text-slate-700 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer transition-colors'

  return (
    <div className="hidden xl:flex items-center gap-2" aria-label="Backend connection and simulation controls">
      <span
        className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full border text-[11px] font-semibold ${pill.cls}`}
        title={lastUpdated ? `Last update ${lastUpdated.toLocaleTimeString()}` : 'No data received yet'}
      >
        <span className={`w-1.5 h-1.5 rounded-full ${pill.dot} ${live ? 'animate-pulse' : ''}`} />
        {pill.text}
      </span>
      <button type="button" className={btn} disabled={!live || busy} onClick={() => void run(() => simulationControl(paused ? 'resume' : 'pause'))}>
        {paused ? 'Resume' : 'Pause'}
      </button>
      <button type="button" className={btn} disabled={!live || busy} onClick={handleInject} title="Inject a random leak scenario">
        + Leak
      </button>
      <button type="button" className={btn} disabled={!live || busy} onClick={() => void run(() => simulationControl('reset'))}>
        Reset
      </button>
    </div>
  )
}

