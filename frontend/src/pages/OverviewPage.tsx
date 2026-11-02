import { useState } from 'react'
import { DashboardLayout } from '../layouts/DashboardLayout'
import { TopNavbar } from '../components/dashboard/TopNavbar'
import { LeftPanel } from '../components/dashboard/LeftPanel'
import { WaterNetworkMap } from '../components/gis/WaterNetworkMap'
import { RightPanel } from '../components/dashboard/RightPanel'
import { BottomPanel } from '../components/dashboard/BottomPanel'
import type { SelectedFeature } from '../types/dashboard'

export function OverviewPage() {
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null)

  const handleSelectFeature = (feature: SelectedFeature | null) => {
    setSelectedAssetId(feature ? feature.properties.id : null)
  }

  return (
    <DashboardLayout
      topNavbar={<TopNavbar />}
      leftPanel={<LeftPanel />}
      centerMap={
        <WaterNetworkMap
          selectedAssetId={selectedAssetId}
          onSelectFeature={handleSelectFeature}
        />
      }
      rightPanel={
        <RightPanel
          selectedAssetId={selectedAssetId}
          onSelectAsset={setSelectedAssetId}
        />
      }
      bottomPanel={<BottomPanel />}
    />
  )
}
