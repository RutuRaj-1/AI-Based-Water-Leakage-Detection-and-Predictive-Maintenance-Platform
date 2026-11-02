interface MapLegendProps {
  className?: string
}

export function MapLegend({ className = '' }: MapLegendProps) {
  return (
    <div
      className={`pointer-events-auto bg-white/95 backdrop-blur-md px-3 py-2 rounded-lg border border-slate-200 shadow-sm text-xs z-[1000] flex flex-col gap-2 ${className}`}
      aria-label="Map Legend"
    >
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <span className="font-bold text-[11px] uppercase tracking-wider text-slate-700">
          Pipe Health:
        </span>
        <span className="flex items-center gap-1.5 text-emerald-700 text-[11px] font-medium">
          <span className="w-3 h-1 rounded-sm bg-[#16A34A]" /> Healthy (80–100)
        </span>
        <span className="flex items-center gap-1.5 text-amber-700 text-[11px] font-medium">
          <span className="w-3 h-1 rounded-sm bg-[#D97706]" /> Monitor (60–79)
        </span>
        <span className="flex items-center gap-1.5 text-orange-700 text-[11px] font-medium">
          <span className="w-3 h-1 rounded-sm bg-[#EA580C]" /> Attention (40–59)
        </span>
        <span className="flex items-center gap-1.5 text-red-700 text-[11px] font-medium">
          <span className="w-3 h-1 rounded-sm bg-[#DC2626]" /> Critical (&lt;40)
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 pt-1.5 border-t border-slate-100 text-[11px] text-slate-600">
        <span className="font-bold uppercase tracking-wider text-slate-500 text-[10px]">
          Assets:
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-blue-600 border border-blue-200" />
          <span>Reservoir / WTP</span>
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-sky-600 border border-sky-200" />
          <span>Pump Station</span>
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-cyan-600" />
          <span>Junction</span>
        </span>
        <span className="flex items-center gap-1.5 text-red-700 font-medium ml-auto">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-600" />
          </span>
          <span>Leak Anomaly</span>
        </span>
      </div>
    </div>
  )
}
