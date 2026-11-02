import { useState } from 'react'
import { Link } from 'react-router-dom'
import { DashboardLayout } from '../layouts/DashboardLayout'
import { TopNavbar } from '../components/dashboard/TopNavbar'
import { WaterNetworkMap } from '../components/gis/WaterNetworkMap'
import { Badge } from '../components/common/Badge'
import type { SelectedFeature } from '../types/dashboard'
import {
  syntheticLeaks,
  syntheticNodes,
  syntheticPipelines,
} from '../data/puneSyntheticNetworkGeoJSON'

export function NetworkMapPage() {
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null)

  const handleSelectFeature = (feature: SelectedFeature | null) => {
    setSelectedAssetId(feature ? feature.properties.id : null)
  }

  return (
    <DashboardLayout topNavbar={<TopNavbar />}>
      <div className="flex flex-col gap-3 h-[calc(100vh-5rem)] min-h-[700px]">
        {/* Dedicated Map Header Toolbar */}
        <div className="bg-white border border-slate-200 rounded-xl px-4 py-3 flex flex-wrap items-center justify-between gap-3 shadow-xs shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
              <svg
                className="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" />
                <line x1="8" y1="2" x2="8" y2="18" />
                <line x1="16" y1="6" x2="16" y2="22" />
              </svg>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold text-slate-900 tracking-tight">
                  Pune Municipal Water Distribution Network — GIS View
                </h1>
                <Badge variant="info" size="sm">
                  Full GeoView
                </Badge>
              </div>
              <p className="text-xs text-slate-500">
                Interactive OpenStreetMap basemap with synthetic telemetry layers, pressure nodes, and AI leak anomalies
              </p>
            </div>
          </div>

          {/* Quick Metrics & Links */}
          <div className="flex items-center flex-wrap gap-2 text-xs">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
              <span className="font-semibold text-slate-900">
                {syntheticPipelines.features.length}
              </span>
              <span>Pipelines</span>
            </div>
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
              <span className="font-semibold text-slate-900">
                {syntheticNodes.features.length}
              </span>
              <span>Nodes</span>
            </div>
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-rose-50 text-rose-700 border border-rose-200">
              <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
              <span className="font-bold text-rose-800">
                {syntheticLeaks.features.length} Leaks Active
              </span>
            </div>

            <div className="h-4 w-px bg-slate-200 mx-1 hidden sm:block" />

            <Link
              to="/alerts"
              className="px-3 py-1 rounded-md bg-white border border-slate-300 text-slate-700 hover:text-blue-600 hover:border-blue-400 font-medium transition-colors"
            >
              View Alerts
            </Link>
            <Link
              to="/maintenance"
              className="px-3 py-1 rounded-md bg-blue-600 text-white hover:bg-blue-700 font-medium shadow-xs transition-colors"
            >
              Work Orders
            </Link>
          </div>
        </div>

        {/* Dedicated Expanded Map View Container */}
        <div className="flex-1 min-h-0 w-full relative">
          <WaterNetworkMap
            className="w-full h-full min-h-[620px] rounded-xl border border-slate-200 shadow-xs"
            selectedAssetId={selectedAssetId}
            onSelectFeature={handleSelectFeature}
          />
        </div>
      </div>
    </DashboardLayout>
  )
}
