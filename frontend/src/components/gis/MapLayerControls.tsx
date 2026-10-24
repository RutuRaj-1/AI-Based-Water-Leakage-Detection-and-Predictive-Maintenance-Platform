interface MapLayerControlsProps {
  showPipelines: boolean
  onTogglePipelines: () => void
  showNodes: boolean
  onToggleNodes: () => void
  showLeaks: boolean
  onToggleLeaks: () => void
  pipelinesCount: number
  nodesCount: number
  leaksCount: number
  className?: string
}

export function MapLayerControls({
  showPipelines,
  onTogglePipelines,
  showNodes,
  onToggleNodes,
  showLeaks,
  onToggleLeaks,
  pipelinesCount,
  nodesCount,
  leaksCount,
  className = '',
}: MapLayerControlsProps) {
  return (
    <div
      className={`pointer-events-auto flex items-center gap-1.5 bg-white/95 backdrop-blur-md px-2.5 py-1.5 rounded-lg border border-slate-200 shadow-sm text-xs z-[1000] ${className}`}
      aria-label="Map Layer Visibility Controls"
    >
      <span className="text-[11px] text-slate-500 font-semibold mr-1">Layers:</span>

      <button
        type="button"
        onClick={onTogglePipelines}
        aria-pressed={showPipelines}
        className={`px-2.5 py-1 rounded transition-colors text-[11px] font-medium border flex items-center gap-1.5 cursor-pointer ${
          showPipelines
            ? 'bg-blue-50 text-blue-700 border-blue-200 shadow-2xs'
            : 'bg-slate-50 text-slate-400 border-slate-200 hover:text-slate-600 hover:bg-slate-100'
        }`}
      >
        <span
          className={`w-2 h-2 rounded-full ${showPipelines ? 'bg-blue-600' : 'bg-slate-400'}`}
        />
        <span>Pipelines ({pipelinesCount})</span>
      </button>

      <button
        type="button"
        onClick={onToggleNodes}
        aria-pressed={showNodes}
        className={`px-2.5 py-1 rounded transition-colors text-[11px] font-medium border flex items-center gap-1.5 cursor-pointer ${
          showNodes
            ? 'bg-indigo-50 text-indigo-700 border-indigo-200 shadow-2xs'
            : 'bg-slate-50 text-slate-400 border-slate-200 hover:text-slate-600 hover:bg-slate-100'
        }`}
      >
        <span
          className={`w-2 h-2 rounded-full ${showNodes ? 'bg-indigo-600' : 'bg-slate-400'}`}
        />
        <span>Nodes ({nodesCount})</span>
      </button>

      <button
        type="button"
        onClick={onToggleLeaks}
        aria-pressed={showLeaks}
        className={`px-2.5 py-1 rounded transition-colors text-[11px] font-medium border flex items-center gap-1.5 cursor-pointer ${
          showLeaks
            ? 'bg-red-50 text-red-700 border-red-200 shadow-2xs'
            : 'bg-slate-50 text-slate-400 border-slate-200 hover:text-slate-600 hover:bg-slate-100'
        }`}
      >
        <span
          className={`w-2 h-2 rounded-full ${
            showLeaks ? 'bg-red-600 animate-pulse' : 'bg-slate-400'
          }`}
        />
        <span>Leaks ({leaksCount})</span>
      </button>
    </div>
  )
}
