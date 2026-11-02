/**
 * Offline fallback snapshot built from the bundled synthetic data.
 * Used until the backend answers, and whenever it is unreachable, so the
 * dashboard never renders empty.
 */

import type { DashboardSnapshot } from '../services/api'
import { criticalAssets, maintenanceTasks, simulatedAlerts } from './dashboardData'
import {
  SYNTHETIC_DATA_NOTICE,
  syntheticLeaks,
  syntheticNodes,
  syntheticPipelines,
} from './puneSyntheticNetworkGeoJSON'

export const fallbackSnapshot: DashboardSnapshot = {
  generatedAt: new Date(0).toISOString(),
  notice: SYNTHETIC_DATA_NOTICE,
  telemetry: {
    scenarioName: 'Offline demo data (backend unreachable)',
    timeStep: 'static',
    engineStatus: 'standby',
    meanPressureBar: 3.42,
    totalFlowMld: 14.8,
    estimatedLossPct: 3.8,
    activeLeaksCount: simulatedAlerts.filter((a) => a.status !== 'resolved').length,
    totalMonitoredPipes: syntheticPipelines.features.length,
    totalNodes: syntheticNodes.features.length,
    networkHealthScore: 78.4,
  },
  summary: {
    totalLengthKm: 444.0,
    monitoredPipes: syntheticPipelines.features.length,
    junctions: syntheticNodes.features.filter((n) => n.properties.nodeType === 'junction').length,
    pumpingStations: syntheticNodes.features.filter((n) => n.properties.nodeType === 'pump').length,
    reservoirs: syntheticNodes.features.filter((n) => n.properties.nodeType !== 'pump' && n.properties.nodeType !== 'junction').length,
    zones: 8,
    averageHealth: 78.4,
    conditionCategories: [
      { id: 'healthy', label: 'Healthy', range: '80–100 Score', percentage: 64, lengthKm: 284.2, color: '#16A34A' },
      { id: 'monitor', label: 'Monitor', range: '60–79 Score', percentage: 21, lengthKm: 93.2, color: '#D97706' },
      { id: 'attention', label: 'Attention', range: '40–59 Score', percentage: 11, lengthKm: 48.8, color: '#EA580C' },
      { id: 'critical', label: 'Critical', range: '0–39 Score', percentage: 4, lengthKm: 17.8, color: '#DC2626' },
    ],
  },
  alerts: simulatedAlerts,
  criticalAssets,
  maintenanceTasks,
  pipelines: syntheticPipelines,
  nodes: syntheticNodes,
  leaks: syntheticLeaks,
  events: [],
  history: [],
  simulation: {
    running: false,
    paused: false,
    tick: 0,
    simulationTime: new Date(0).toISOString(),
    minutesPerTick: 5,
    tickSeconds: 3,
    autoLeaks: false,
    autoDispatch: false,
    autoRepair: false,
    activeLeaks: 0,
  },
}

