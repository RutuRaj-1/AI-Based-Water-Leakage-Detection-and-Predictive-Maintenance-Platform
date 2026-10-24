import { useEffect, useMemo, useState } from 'react'
import {
  MapContainer,
  TileLayer,
  Polyline,
  CircleMarker,
  Marker,
  Popup,
  Tooltip,
  useMap,
} from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import type {
  LeakMarkerProperties,
  NetworkNodeProperties,
  PipelineProperties,
  SelectedFeature,
} from '../../types/dashboard'
import {
  PUNE_DEFAULT_ZOOM,
  PUNE_MAP_CENTER,
  getConditionColor,
  syntheticLeaks,
  syntheticNodes,
  syntheticPipelines,
} from '../../data/puneSyntheticNetworkGeoJSON'
import { MapLayerControls } from './MapLayerControls'
import { MapLegend } from './MapLegend'
import { SyntheticDataDisclaimer } from './SyntheticDataDisclaimer'
import { Badge } from '../common/Badge'

interface WaterNetworkMapProps {
  className?: string
  selectedAssetId?: string | null
  onSelectFeature?: (feature: SelectedFeature | null) => void
}

/**
 * Controller to handle programmatic map pan/zoom and resize invalidation
 */
function MapLifecycleController({
  targetCoords,
}: {
  targetCoords: [number, number] | null
}) {
  const map = useMap()

  useEffect(() => {
    // Invalidate size immediately and shortly after mount to prevent grey tiles
    map.invalidateSize()
    const timer = setTimeout(() => {
      map.invalidateSize()
    }, 250)
    return () => clearTimeout(timer)
  }, [map])

  useEffect(() => {
    if (targetCoords) {
      map.flyTo(targetCoords, Math.max(map.getZoom(), 13), {
        duration: 0.8,
      })
    }
  }, [targetCoords, map])

  return null
}

function getNodeFillColor(type: NetworkNodeProperties['nodeType']): string {
  switch (type) {
    case 'treatment_plant':
      return '#2563EB' // Blue 600
    case 'reservoir':
      return '#1D4ED8' // Blue 700
    case 'pump':
      return '#0284C7' // Sky 600
    case 'junction':
      return '#0EA5E9' // Sky 500
  }
}

function getNodeRadius(type: NetworkNodeProperties['nodeType']): number {
  switch (type) {
    case 'treatment_plant':
      return 10
    case 'reservoir':
      return 8
    case 'pump':
      return 7
    case 'junction':
      return 5
  }
}

function createLeakMarkerIcon(severity: string, isSelected: boolean): L.DivIcon {
  const color =
    severity === 'critical'
      ? 'bg-[#DC2626]'
      : severity === 'high'
        ? 'bg-[#D97706]'
        : 'bg-[#EAB308]'
  const pingColor =
    severity === 'critical'
      ? 'bg-red-400'
      : severity === 'high'
        ? 'bg-amber-400'
        : 'bg-yellow-400'

  return L.divIcon({
    className: 'leak-anomaly-divicon',
    html: `
      <div class="relative flex items-center justify-center w-8 h-8" style="cursor: pointer;">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full ${pingColor} opacity-75"></span>
        <span class="relative inline-flex rounded-full h-4 w-4 ${color} ${
          isSelected ? 'ring-4 ring-blue-600 shadow-md scale-125' : 'ring-2 ring-white shadow-sm'
        }"></span>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -14],
  })
}

export function WaterNetworkMap({
  className = '',
  selectedAssetId,
  onSelectFeature,
}: WaterNetworkMapProps) {
  // Layer visibility state
  const [showPipelines, setShowPipelines] = useState(true)
  const [showNodes, setShowNodes] = useState(true)
  const [showLeaks, setShowLeaks] = useState(true)

  // Internal clicked selection and camera target
  const [clickedSelection, setClickedSelection] = useState<SelectedFeature | null>(null)
  const [clickedTarget, setClickedTarget] = useState<[number, number] | null>(null)

  // Derived camera target from external selection
  const externalTarget = useMemo<[number, number] | null>(() => {
    if (!selectedAssetId) return null

    const leakMatch = syntheticLeaks.features.find(
      (f) => f.properties.id === selectedAssetId || f.properties.pipelineId === selectedAssetId
    )
    if (leakMatch) {
      return [leakMatch.geometry.coordinates[1], leakMatch.geometry.coordinates[0]]
    }

    const pipeMatch = syntheticPipelines.features.find(
      (f) => f.properties.id === selectedAssetId
    )
    if (pipeMatch) {
      const midIdx = Math.floor(pipeMatch.geometry.coordinates.length / 2)
      const midCoord = pipeMatch.geometry.coordinates[midIdx]
      if (midCoord) {
        return [midCoord[1], midCoord[0]]
      }
    }

    const nodeMatch = syntheticNodes.features.find((f) => f.properties.id === selectedAssetId)
    if (nodeMatch) {
      return [nodeMatch.geometry.coordinates[1], nodeMatch.geometry.coordinates[0]]
    }

    return null
  }, [selectedAssetId])

  // Active fly target: user click takes precedence when active, otherwise external target
  const activeFlyTarget = clickedTarget ?? externalTarget

  // Derived active selection: matches selectedAssetId if provided, else local clicked selection
  const activeSelection = useMemo<SelectedFeature | null>(() => {
    if (!selectedAssetId) {
      return clickedSelection
    }

    const leakMatch = syntheticLeaks.features.find(
      (f) => f.properties.id === selectedAssetId || f.properties.pipelineId === selectedAssetId
    )
    if (leakMatch) {
      return { type: 'leak', properties: leakMatch.properties }
    }

    const pipeMatch = syntheticPipelines.features.find(
      (f) => f.properties.id === selectedAssetId
    )
    if (pipeMatch) {
      return { type: 'pipeline', properties: pipeMatch.properties }
    }

    const nodeMatch = syntheticNodes.features.find((f) => f.properties.id === selectedAssetId)
    if (nodeMatch) {
      return { type: 'node', properties: nodeMatch.properties }
    }

    return clickedSelection
  }, [selectedAssetId, clickedSelection])

  const handleSelectPipeline = (pipe: PipelineProperties, coords: [number, number][]) => {
    const feature: SelectedFeature = { type: 'pipeline', properties: pipe }
    setClickedSelection(feature)
    if (coords.length > 0) {
      const mid = coords[Math.floor(coords.length / 2)]
      if (mid) setClickedTarget(mid)
    }
    onSelectFeature?.(feature)
  }

  const handleSelectNode = (node: NetworkNodeProperties, coords: [number, number]) => {
    const feature: SelectedFeature = { type: 'node', properties: node }
    setClickedSelection(feature)
    setClickedTarget(coords)
    onSelectFeature?.(feature)
  }

  const handleSelectLeak = (leak: LeakMarkerProperties, coords: [number, number]) => {
    const feature: SelectedFeature = { type: 'leak', properties: leak }
    setClickedSelection(feature)
    setClickedTarget(coords)
    onSelectFeature?.(feature)
  }

  const handleClearSelection = () => {
    setClickedSelection(null)
    setClickedTarget(null)
    onSelectFeature?.(null)
  }

  const resetPuneCenter = () => {
    setClickedTarget(PUNE_MAP_CENTER)
  }

  // Pre-process pipeline polylines with Leaflet [lat, lon] coordinates
  const preparedPipelines = useMemo(() => {
    return syntheticPipelines.features.map((f) => {
      const positions: [number, number][] = f.geometry.coordinates.map(
        ([lon, lat]) => [lat, lon]
      )
      return {
        ...f,
        positions,
      }
    })
  }, [])

  const currentSelectedId =
    activeSelection?.properties.id ?? selectedAssetId ?? null

  return (
    <section
      className={`map-panel relative bg-white border border-slate-200 rounded-xl overflow-hidden flex flex-col shadow-xs min-h-[500px] lg:min-h-[620px] h-full ${className}`}
      aria-label="Water Network GIS Map Panel"
    >
      {/* Top Map Toolbar Bar */}
      <div className="absolute top-3 left-3 right-3 z-[1000] flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        {/* Left Status & Zone indicator */}
        <div className="pointer-events-auto flex items-center gap-2 bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs font-semibold text-slate-800">
            Pune Municipal Water Distribution
          </span>
          <span className="text-slate-300 text-xs">|</span>
          <span className="text-[11px] text-blue-600 font-mono">
            {PUNE_MAP_CENTER[0]}° N, {PUNE_MAP_CENTER[1]}° E
          </span>
          <Badge variant="info" size="sm">
            GIS Live
          </Badge>
        </div>

        {/* Layer Visibility Controls */}
        <MapLayerControls
          showPipelines={showPipelines}
          onTogglePipelines={() => setShowPipelines(!showPipelines)}
          showNodes={showNodes}
          onToggleNodes={() => setShowNodes(!showNodes)}
          showLeaks={showLeaks}
          onToggleLeaks={() => setShowLeaks(!showLeaks)}
          pipelinesCount={syntheticPipelines.features.length}
          nodesCount={syntheticNodes.features.length}
          leaksCount={syntheticLeaks.features.length}
        />
      </div>

      {/* Synthetic Data Disclaimer (Top Left Under Toolbar) */}
      <div className="absolute top-14 left-3 z-[1000] pointer-events-none">
        <SyntheticDataDisclaimer />
      </div>

      {/* Map Reset & Zoom Shortcuts (Right Side) */}
      <div className="absolute top-16 right-3 z-[1000] flex flex-col gap-1.5 pointer-events-none">
        <div className="pointer-events-auto bg-white/95 backdrop-blur-md border border-slate-200 rounded-lg p-1 shadow-sm">
          <button
            type="button"
            onClick={resetPuneCenter}
            className="w-8 h-8 rounded flex items-center justify-center text-slate-700 hover:text-slate-900 hover:bg-slate-100 text-xs font-bold transition-colors cursor-pointer"
            title="Recenter Pune Network"
            aria-label="Recenter Pune Network"
          >
            ⌖
          </button>
        </div>
      </div>

      {/* Selected Asset Details Floating Card */}
      {activeSelection && (
        <div className="absolute top-36 right-3 z-[1000] max-w-sm w-72 bg-white/95 backdrop-blur-md border border-slate-200 rounded-xl p-3.5 shadow-lg text-slate-800">
          <div className="flex items-start justify-between gap-2 border-b border-slate-100 pb-2 mb-2.5">
            <div>
              <span className="text-[10px] uppercase font-bold tracking-wider text-blue-600">
                {activeSelection.type === 'pipeline'
                  ? 'Selected Pipeline'
                  : activeSelection.type === 'node'
                    ? 'Selected Node'
                    : 'Active Leak Anomaly'}
              </span>
              <h4 className="text-xs font-bold text-slate-900 mt-0.5">
                {'name' in activeSelection.properties
                  ? activeSelection.properties.name
                  : activeSelection.properties.id}
              </h4>
            </div>
            <button
              type="button"
              onClick={handleClearSelection}
              className="text-slate-400 hover:text-slate-700 p-1 rounded hover:bg-slate-100 text-xs cursor-pointer"
              aria-label="Close details"
            >
              ✕
            </button>
          </div>

          {activeSelection.type === 'pipeline' && (
            <div className="space-y-1.5 text-[11px] text-slate-600">
              <div className="flex justify-between">
                <span className="text-slate-500">Condition:</span>
                <span
                  className="font-bold uppercase text-[10px] px-1.5 py-0.5 rounded"
                  style={{
                    backgroundColor: `${getConditionColor(activeSelection.properties.condition)}15`,
                    color: getConditionColor(activeSelection.properties.condition),
                  }}
                >
                  {activeSelection.properties.condition} ({activeSelection.properties.healthScore}%)
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Zone:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.zone}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Material / Diameter:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.material} ({activeSelection.properties.diameterMm}mm)
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Pressure / Flow:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.pressureBar} bar · {activeSelection.properties.flowRateMld} MLD
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Length:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.lengthKm} km
                </span>
              </div>
            </div>
          )}

          {activeSelection.type === 'node' && (
            <div className="space-y-1.5 text-[11px] text-slate-600">
              <div className="flex justify-between">
                <span className="text-slate-500">Node Type:</span>
                <span className="font-semibold capitalize text-blue-600">
                  {activeSelection.properties.nodeType.replace('_', ' ')}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Zone:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.zone}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Pressure / Elevation:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.pressureBar} bar · {activeSelection.properties.elevationM}m MSL
                </span>
              </div>
              {activeSelection.properties.baseDemandLps !== undefined && (
                <div className="flex justify-between">
                  <span className="text-slate-500">Base Demand:</span>
                  <span className="font-medium text-slate-800">
                    {activeSelection.properties.baseDemandLps} L/s
                  </span>
                </div>
              )}
            </div>
          )}

          {activeSelection.type === 'leak' && (
            <div className="space-y-1.5 text-[11px] text-slate-600">
              <div className="flex justify-between">
                <span className="text-slate-500">Severity:</span>
                <Badge variant={activeSelection.properties.severity} size="sm">
                  {activeSelection.properties.severity.toUpperCase()}
                </Badge>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Pipeline Asset:</span>
                <span className="font-mono font-semibold text-red-600">
                  {activeSelection.properties.pipelineId}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Location:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.location}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Estimated Loss:</span>
                <span className="font-semibold text-red-600">
                  {activeSelection.properties.estimatedLoss}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Detected:</span>
                <span className="font-medium text-slate-800">
                  {activeSelection.properties.detectionTime}
                </span>
              </div>
            </div>
          )}

          <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-500">
            <span>Asset ID: <strong className="text-slate-800 font-mono">{activeSelection.properties.id}</strong></span>
            <span className="text-blue-600 font-medium">Synced with Panels</span>
          </div>
        </div>
      )}

      {/* Main Interactive Leaflet Container */}
      <div className="relative flex-1 w-full h-full min-h-[460px] bg-slate-100">
        <MapContainer
          center={PUNE_MAP_CENTER}
          zoom={PUNE_DEFAULT_ZOOM}
          scrollWheelZoom={true}
          style={{ width: '100%', height: '100%', minHeight: '460px', backgroundColor: '#e2e8f0' }}
          className="z-0"
        >
          {/* OpenStreetMap Standard Basemap with Attribution */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            maxZoom={19}
          />

          <MapLifecycleController targetCoords={activeFlyTarget} />

          {/* 1. Pipeline Polyline Layers */}
          {showPipelines &&
            preparedPipelines.map((pipe) => {
              const isSelected =
                currentSelectedId === pipe.properties.id ||
                (activeSelection?.type === 'leak' &&
                  activeSelection.properties.pipelineId === pipe.properties.id)
              const strokeColor = isSelected
                ? '#1E293B'
                : getConditionColor(pipe.properties.condition)

              return (
                <Polyline
                  key={pipe.properties.id}
                  positions={pipe.positions}
                  pathOptions={{
                    color: strokeColor,
                    weight: isSelected ? 6 : 4,
                    opacity: isSelected ? 1 : 0.85,
                    dashArray:
                      pipe.properties.condition === 'critical' ? '6, 6' : undefined,
                  }}
                  eventHandlers={{
                    click: () => handleSelectPipeline(pipe.properties, pipe.positions),
                  }}
                >
                  <Tooltip sticky direction="top" className="custom-leaflet-tooltip">
                    <div className="text-xs">
                      <strong className="block font-bold">{pipe.properties.name}</strong>
                      <span>Health: {pipe.properties.healthScore}% · {pipe.properties.pressureBar} bar</span>
                    </div>
                  </Tooltip>
                  <Popup>
                    <div className="text-xs p-1">
                      <strong className="text-sm font-bold block mb-1 text-slate-900">
                        {pipe.properties.name}
                      </strong>
                      <p className="text-slate-700 mb-1">
                        Zone: {pipe.properties.zone} | Spec: {pipe.properties.material}
                      </p>
                      <p className="text-slate-700">
                        Health Score:{' '}
                        <strong
                          style={{ color: getConditionColor(pipe.properties.condition) }}
                        >
                          {pipe.properties.healthScore}% ({pipe.properties.condition})
                        </strong>
                      </p>
                    </div>
                  </Popup>
                </Polyline>
              )
            })}

          {/* 2. Network Node Circle Markers */}
          {showNodes &&
            syntheticNodes.features.map((node) => {
              const coords: [number, number] = [
                node.geometry.coordinates[1],
                node.geometry.coordinates[0],
              ]
              const isSelected = currentSelectedId === node.properties.id
              const fillColor = getNodeFillColor(node.properties.nodeType)
              const radius = getNodeRadius(node.properties.nodeType)

              return (
                <CircleMarker
                  key={node.properties.id}
                  center={coords}
                  radius={isSelected ? radius + 3 : radius}
                  pathOptions={{
                    color: isSelected ? '#1E293B' : '#FFFFFF',
                    fillColor: fillColor,
                    fillOpacity: 0.95,
                    weight: isSelected ? 3 : 2,
                  }}
                  eventHandlers={{
                    click: () => handleSelectNode(node.properties, coords),
                  }}
                >
                  <Tooltip sticky direction="top">
                    <div className="text-xs">
                      <strong>{node.properties.name}</strong>
                      <span className="block text-[11px] capitalize text-slate-600">
                        {node.properties.nodeType.replace('_', ' ')} · {node.properties.pressureBar} bar
                      </span>
                    </div>
                  </Tooltip>
                  <Popup>
                    <div className="text-xs p-1 text-slate-900">
                      <strong className="block text-sm font-bold">{node.properties.name}</strong>
                      <span className="block text-slate-600 capitalize">
                        Type: {node.properties.nodeType.replace('_', ' ')}
                      </span>
                      <span className="block text-slate-600">
                        Pressure: {node.properties.pressureBar} bar | Elev: {node.properties.elevationM}m
                      </span>
                    </div>
                  </Popup>
                </CircleMarker>
              )
            })}

          {/* 3. Simulated Leak Anomaly Markers */}
          {showLeaks &&
            syntheticLeaks.features.map((leak) => {
              const coords: [number, number] = [
                leak.geometry.coordinates[1],
                leak.geometry.coordinates[0],
              ]
              const isSelected =
                currentSelectedId === leak.properties.id ||
                currentSelectedId === leak.properties.pipelineId

              const icon = createLeakMarkerIcon(leak.properties.severity, isSelected)

              return (
                <Marker
                  key={leak.properties.id}
                  position={coords}
                  icon={icon}
                  eventHandlers={{
                    click: () => handleSelectLeak(leak.properties, coords),
                  }}
                >
                  <Tooltip sticky direction="top">
                    <div className="text-xs">
                      <strong className="text-rose-600 font-bold block">
                        Leak Anomaly: {leak.properties.id}
                      </strong>
                      <span>{leak.properties.location} · Loss: {leak.properties.estimatedLoss}</span>
                    </div>
                  </Tooltip>
                  <Popup>
                    <div className="text-xs p-1 text-slate-900">
                      <strong className="text-sm font-bold text-rose-600 block mb-0.5">
                        Simulated Leak {leak.properties.id}
                      </strong>
                      <p className="text-slate-700">Location: {leak.properties.location}</p>
                      <p className="text-slate-700">Pipeline: {leak.properties.pipelineId}</p>
                      <p className="text-rose-600 font-semibold">
                        Estimated Loss: {leak.properties.estimatedLoss}
                      </p>
                    </div>
                  </Popup>
                </Marker>
              )
            })}
        </MapContainer>
      </div>

      {/* Map Legend Footer (Bottom overlay) */}
      <div className="absolute bottom-3 left-3 right-3 z-[1000] flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        <MapLegend />
      </div>
    </section>
  )
}
