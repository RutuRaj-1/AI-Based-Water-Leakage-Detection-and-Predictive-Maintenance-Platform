import { useState } from 'react'
import { SYNTHETIC_DATA_NOTICE } from '../../data/puneSyntheticNetworkGeoJSON'

interface SyntheticDataDisclaimerProps {
  className?: string
}

export function SyntheticDataDisclaimer({ className = '' }: SyntheticDataDisclaimerProps) {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <div
      className={`pointer-events-auto transition-all duration-200 z-[1000] text-xs ${className}`}
      role="region"
      aria-label="Synthetic Data Disclosure"
    >
      <div className="bg-white/95 backdrop-blur-md border border-amber-300 rounded-lg p-2.5 shadow-sm text-slate-800 flex items-start gap-2 max-w-md">
        <span className="flex-shrink-0 w-4 h-4 rounded-full bg-amber-100 text-amber-800 border border-amber-300 flex items-center justify-center font-bold text-[10px] mt-0.5">
          !
        </span>
        <div className="flex-1">
          <div className="flex items-center justify-between gap-2">
            <span className="font-bold text-[11px] uppercase tracking-wide text-amber-800">
              Synthetic Simulation Network
            </span>
            <button
              type="button"
              onClick={() => setCollapsed(!collapsed)}
              className="text-[10px] text-slate-500 hover:text-slate-800 underline cursor-pointer"
            >
              {collapsed ? 'Details' : 'Hide'}
            </button>
          </div>
          {!collapsed && (
            <p className="text-[11px] text-slate-600 mt-1 leading-snug">
              {SYNTHETIC_DATA_NOTICE}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
