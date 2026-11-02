import { Badge } from '../common/Badge'

interface MapPlaceholderProps {
  className?: string
}

export function MapPlaceholder({ className = '' }: MapPlaceholderProps) {
  return (
    <section
      className={`map-panel relative bg-[#070e1b] border border-slate-800 rounded-xl overflow-hidden flex flex-col shadow-2xl shadow-black/40 min-h-[460px] lg:min-h-[580px] ${className}`}
      aria-label="Water Network GIS Map Panel"
    >
      {/* Top Map Toolbar Bar */}
      <div className="absolute top-3 left-3 right-3 z-20 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        {/* Left Status & Zone indicator */}
        <div className="pointer-events-auto flex items-center gap-2 bg-[#091528]/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-sky-500/25 shadow-lg">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs font-semibold text-slate-200">
            Pune Municipal Water Distribution
          </span>
          <span className="text-slate-500 text-xs">|</span>
          <span className="text-[11px] text-sky-300 font-mono">18.5204° N, 73.8567° E</span>
        </div>

        {/* Layer Controls Preview */}
        <div className="pointer-events-auto hidden sm:flex items-center gap-1.5 bg-[#091528]/90 backdrop-blur-md px-2.5 py-1.5 rounded-lg border border-slate-800 shadow-lg text-xs">
          <span className="text-[11px] text-slate-400 font-medium mr-1">Layers:</span>
          <span className="px-2 py-0.5 rounded bg-sky-950/70 text-sky-300 border border-sky-500/30 font-medium text-[11px]">
            Pipelines
          </span>
          <span className="px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/60 text-[11px]">
            Pressure Nodes
          </span>
          <span className="px-2 py-0.5 rounded bg-red-950/70 text-red-300 border border-red-500/30 text-[11px]">
            Leak Anomalies (3)
          </span>
        </div>
      </div>

      {/* Map Zoom / Controls Mockup (Right Side) */}
      <div className="absolute top-16 right-3 z-20 flex flex-col gap-1.5 pointer-events-none">
        <div className="pointer-events-auto bg-[#091528]/90 backdrop-blur-md border border-slate-800 rounded-lg p-1 flex flex-col shadow-lg">
          <button
            type="button"
            className="w-8 h-8 rounded flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-800 text-sm font-bold"
            title="Zoom In (Interactive in Phase 2)"
            disabled
          >
            +
          </button>
          <div className="h-[1px] bg-slate-800 my-0.5" />
          <button
            type="button"
            className="w-8 h-8 rounded flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-800 text-sm font-bold"
            title="Zoom Out (Interactive in Phase 2)"
            disabled
          >
            −
          </button>
        </div>
        <div className="pointer-events-auto bg-[#091528]/90 backdrop-blur-md border border-slate-800 rounded-lg p-1 shadow-lg">
          <button
            type="button"
            className="w-8 h-8 rounded flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-800 text-xs font-semibold"
            title="Center Pune Network"
            disabled
          >
            ⌖
          </button>
        </div>
      </div>

      {/* Main Map Visualization Graphic (Subtle GIS & Pune schematic background) */}
      <div className="relative flex-1 w-full h-full flex items-center justify-center overflow-hidden bg-[radial-gradient(ellipse_at_center,_#0f2347_0%,_#091322_55%,_#050a14_100%)]">
        {/* Cartographic Coordinate Grid */}
        <div
          className="absolute inset-0 opacity-20 pointer-events-none"
          style={{
            backgroundImage: `
              linear-gradient(to right, rgba(56, 189, 248, 0.15) 1px, transparent 1px),
              linear-gradient(to bottom, rgba(56, 189, 248, 0.15) 1px, transparent 1px)
            `,
            backgroundSize: '40px 40px',
          }}
        />

        {/* Concentric Radar / Scan Rings for Pune Central Area */}
        <div className="absolute w-[600px] h-[600px] rounded-full border border-sky-500/10 pointer-events-none" />
        <div className="absolute w-[420px] h-[420px] rounded-full border border-sky-500/15 pointer-events-none" />
        <div className="absolute w-[240px] h-[240px] rounded-full border border-sky-500/20 pointer-events-none" />

        {/* Schematic SVG Map of Pune Water Mains & Landmarks */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none"
          viewBox="0 0 1000 650"
          preserveAspectRatio="xMidYMid meet"
          aria-hidden="true"
        >
          <defs>
            {/* Pulsing anomaly marker gradient */}
            <radialGradient id="anomalyGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ef4444" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#ef4444" stopOpacity="0" />
            </radialGradient>
            <linearGradient id="mulaMuthaRiver" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#0284c7" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#0369a1" stopOpacity="0.1" />
            </linearGradient>
          </defs>

          {/* Mula-Mutha River Schematic */}
          <path
            d="M 120 180 Q 280 260 450 240 T 780 200 T 960 290"
            fill="none"
            stroke="url(#mulaMuthaRiver)"
            strokeWidth="28"
            strokeLinecap="round"
          />
          <path
            d="M 120 180 Q 280 260 450 240 T 780 200 T 960 290"
            fill="none"
            stroke="#38bdf8"
            strokeOpacity="0.35"
            strokeWidth="3"
            strokeDasharray="6 4"
          />
          <text x="740" y="215" fill="#38bdf8" fillOpacity="0.4" fontSize="11" fontWeight="600">
            Mula-Mutha River Basin
          </text>

          {/* Arterial Pipeline Grid (Healthy - Green) */}
          <g stroke="#22c55e" strokeWidth="2.5" strokeOpacity="0.75" strokeLinecap="round">
            <line x1="220" y1="460" x2="380" y2="340" />
            <line x1="380" y1="340" x2="520" y2="310" />
            <line x1="520" y1="310" x2="710" y2="280" />
            <line x1="380" y1="340" x2="360" y2="190" />
            <line x1="520" y1="310" x2="560" y2="160" />
            <line x1="560" y1="160" x2="740" y2="140" />
            <line x1="220" y1="460" x2="480" y2="490" />
            <line x1="480" y1="490" x2="680" y2="470" />
          </g>

          {/* Pipeline Branches (Monitor - Yellow) */}
          <g stroke="#eab308" strokeWidth="2" strokeOpacity="0.75" strokeLinecap="round">
            <line x1="360" y1="190" x2="260" y2="140" />
            <line x1="710" y1="280" x2="840" y2="340" />
            <line x1="680" y1="470" x2="790" y2="520" />
          </g>

          {/* Pipeline Branches (Attention - Orange) */}
          <g stroke="#f97316" strokeWidth="2" strokeOpacity="0.8" strokeLinecap="round">
            <line x1="520" y1="310" x2="480" y2="490" />
            <line x1="710" y1="280" x2="680" y2="470" />
          </g>

          {/* Pipeline Segment with Critical Leak (Red - Anomaly Line) */}
          <g stroke="#ef4444" strokeWidth="3.5" strokeOpacity="0.9" strokeLinecap="round">
            <line x1="480" y1="490" x2="410" y2="580" strokeDasharray="5 3" />
            <line x1="380" y1="340" x2="440" y2="380" strokeDasharray="5 3" />
          </g>

          {/* Major Node Markers (Pumping Stations & Reservoirs) */}
          {/* Khadakwasla / Parvati Reservoir */}
          <circle cx="220" cy="460" r="8" fill="#0284c7" stroke="#38bdf8" strokeWidth="2" />
          <text x="145" y="485" fill="#e2e8f0" fontSize="11" fontWeight="600">
            Parvati WTP
          </text>

          {/* Swargate Hub */}
          <circle cx="480" cy="490" r="7" fill="#0ea5e9" stroke="#7dd3fc" strokeWidth="2" />
          <text x="495" y="495" fill="#e2e8f0" fontSize="11" fontWeight="600">
            Swargate Node
          </text>

          {/* Shivajinagar Junction */}
          <circle cx="520" cy="310" r="7" fill="#0ea5e9" stroke="#7dd3fc" strokeWidth="2" />
          <text x="535" y="305" fill="#e2e8f0" fontSize="11" fontWeight="600">
            Shivajinagar
          </text>

          {/* Kothrud Sub-network */}
          <circle cx="380" cy="340" r="6" fill="#0ea5e9" stroke="#7dd3fc" strokeWidth="2" />
          <text x="310" y="335" fill="#e2e8f0" fontSize="11" fontWeight="600">
            Kothrud DMA
          </text>

          {/* Katraj Feeder */}
          <circle cx="410" cy="580" r="6" fill="#ef4444" stroke="#fca5a5" strokeWidth="2" />
          <text x="425" y="590" fill="#fca5a5" fontSize="11" fontWeight="600">
            Katraj Trunk P-104
          </text>

          {/* Hadapsar Sector */}
          <circle cx="710" cy="280" r="6" fill="#0ea5e9" stroke="#7dd3fc" strokeWidth="2" />
          <text x="725" y="275" fill="#e2e8f0" fontSize="11" fontWeight="600">
            Hadapsar Sector
          </text>

          {/* Baner / Aundh Area */}
          <circle cx="360" cy="190" r="6" fill="#0ea5e9" stroke="#7dd3fc" strokeWidth="2" />
          <text x="290" y="195" fill="#e2e8f0" fontSize="11" fontWeight="600">
            Baner-Aundh
          </text>

          {/* Simulated Active Leak Pulse Indicators */}
          {/* Anomaly 1: Katraj */}
          <circle cx="410" cy="580" r="22" fill="url(#anomalyGlow)" />
          <circle cx="410" cy="580" r="14" fill="#ef4444" fillOpacity="0.4" />
          <circle cx="410" cy="580" r="4" fill="#ffffff" />

          {/* Anomaly 2: Swargate DMA-3 */}
          <circle cx="440" cy="380" r="18" fill="url(#anomalyGlow)" />
          <circle cx="440" cy="380" r="11" fill="#f97316" fillOpacity="0.4" />
          <circle cx="440" cy="380" r="3.5" fill="#ffffff" />

          {/* Anomaly 3: Hadapsar Branch */}
          <circle cx="840" cy="340" r="16" fill="url(#anomalyGlow)" />
          <circle cx="840" cy="340" r="9" fill="#eab308" fillOpacity="0.4" />
          <circle cx="840" cy="340" r="3" fill="#ffffff" />
        </svg>

        {/* Phase 1 Integration Badge & Notice Callout (Center) */}
        <div className="z-10 max-w-md mx-4 text-center bg-[#061124]/92 border border-sky-500/40 rounded-xl p-5 backdrop-blur-md shadow-2xl shadow-black/60">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-sky-500/15 border border-sky-400/30 text-sky-300 mb-3">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth="1.8"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 20l-5.447-2.724A2 2 0 012.5 15.485V5.515a2 2 0 011.053-1.761L9 1m0 19l6-3m-6 3V1m6 16l5.447 2.724A2 2 0 0021.5 17.962V7.986a2 2 0 00-1.053-1.761L15 3.5m0 13.5V3.5m0 0L9 1"
              />
            </svg>
          </div>
          <h3 className="text-base font-bold text-white tracking-wide">
            Interactive GIS Map View
          </h3>
          <p className="text-xs text-sky-200/80 mt-1.5 leading-relaxed">
            Central visualization canvas for Pune Water Distribution Network.
            Interactive Leaflet/GeoJSON layers, pipe inspections, and real-time hydraulic
            telemetry will be integrated in <strong>Phase 2</strong>.
          </p>
          <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
            <Badge variant="accent" size="sm">
              Phase 1 Visual Placeholder
            </Badge>
            <Badge variant="info" size="sm">
              EPSG:4326 · WGS84
            </Badge>
            <Badge variant="neutral" size="sm">
              Pune Municipal Corp.
            </Badge>
          </div>
        </div>
      </div>

      {/* Map Legend Footer (Bottom overlay) */}
      <div className="absolute bottom-3 left-3 right-3 z-20 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        {/* Pipeline Condition Legend */}
        <div className="pointer-events-auto flex items-center gap-3 bg-[#091528]/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-800 shadow-lg text-[11px]">
          <span className="font-semibold text-slate-300">Pipe Health:</span>
          <span className="flex items-center gap-1.5 text-emerald-400">
            <span className="w-2.5 h-1 rounded bg-emerald-500" /> Healthy (80–100)
          </span>
          <span className="flex items-center gap-1.5 text-yellow-400">
            <span className="w-2.5 h-1 rounded bg-yellow-500" /> Monitor (60–79)
          </span>
          <span className="flex items-center gap-1.5 text-orange-400">
            <span className="w-2.5 h-1 rounded bg-orange-500" /> Attention (40–59)
          </span>
          <span className="flex items-center gap-1.5 text-red-400">
            <span className="w-2.5 h-1 rounded bg-red-500" /> Critical (&lt;40)
          </span>
        </div>

        {/* Anomaly Indicator Legend */}
        <div className="pointer-events-auto hidden md:flex items-center gap-2 bg-[#091528]/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-800 shadow-lg text-[11px] text-slate-300">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500" />
          </span>
          <span>Simulated Leak Anomaly Location</span>
        </div>
      </div>
    </section>
  )
}
