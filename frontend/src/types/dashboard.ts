/**
 * Type definitions for the Pune Water Network AI Dashboard (live API + offline fallback)
 */

export type SeverityLevel = 'critical' | 'high' | 'moderate' | 'low' | 'normal'

export interface PipelineConditionCategory {
  id: string
  label: string
  range: string
  percentage: number
  lengthKm: number
  color: string
}

export interface LeakAlert {
  id: string
  title: string
  location: string
  pipelineId: string
  estimatedLoss: string
  severity: SeverityLevel
  timestamp: string
  status: 'active' | 'investigating' | 'resolved'
  detectedAt?: string
  estimatedLossM3h?: number
  autoDispatched?: boolean
}

export interface CriticalAsset {
  id: string
  name: string
  assetType: 'pipe' | 'junction' | 'pump' | 'reservoir'
  healthScore: number
  material: string
  ageYears: number
  criticality: 'urgent' | 'high' | 'medium'
  zone: string
  failureRisk?: number
}

export interface MaintenanceTask {
  id: string
  workOrderNumber: string
  title: string
  targetAsset: string
  priority: 'urgent' | 'high' | 'medium' | 'routine'
  priorityScore: number
  assignedTeam: string
  dueDate: string
  status?: WorkOrderStatus
  kind?: string
  assetId?: string
}

export interface SimulationTelemetry {
  scenarioName: string
  timeStep: string
  engineStatus: 'running' | 'paused' | 'standby'
  meanPressureBar: number
  totalFlowMld: number
  estimatedLossPct: number
  activeLeaksCount: number
  totalMonitoredPipes: number
  totalNodes: number
  networkHealthScore: number
}

export type PipelineCondition = 'healthy' | 'monitor' | 'attention' | 'critical'

export interface PipelineProperties {
  id: string
  name: string
  zone: string
  diameterMm: number
  material: string
  healthScore: number
  condition: PipelineCondition
  pressureBar: number
  flowRateMld: number
  lengthKm: number
}

export type NetworkNodeType = 'reservoir' | 'pump' | 'junction' | 'treatment_plant'

export interface NetworkNodeProperties {
  id: string
  name: string
  nodeType: NetworkNodeType
  zone: string
  pressureBar: number
  elevationM: number
  baseDemandLps?: number
}

export interface LeakMarkerProperties {
  id: string
  pipelineId: string
  severity: SeverityLevel
  estimatedLoss: string
  location: string
  detectionTime: string
  status: 'active' | 'investigating' | 'resolved'
}

export type SelectedFeature =
  | { type: 'pipeline'; properties: PipelineProperties }
  | { type: 'node'; properties: NetworkNodeProperties }
  | { type: 'leak'; properties: LeakMarkerProperties }


// ---------------------------------------------------------------------------
// Live API additions (backend: /api/v1/dashboard/snapshot)
// ---------------------------------------------------------------------------
export type WorkOrderStatus = 'open' | 'in_progress' | 'completed'

export interface NetworkSummary {
  totalLengthKm: number
  monitoredPipes: number
  junctions: number
  pumpingStations: number
  reservoirs: number
  zones: number
  averageHealth: number
  conditionCategories: PipelineConditionCategory[]
}

export interface TelemetryPoint {
  time: string
  meanPressureBar: number
  totalFlowMld: number
  estimatedLossPct: number
  activeLeaksCount: number
  networkHealthScore: number
}

export interface ActivityEvent {
  id: number
  time: string
  level: 'info' | 'warning' | 'critical' | 'success'
  kind: string
  message: string
}

export interface SimulationStatus {
  running: boolean
  paused: boolean
  tick: number
  simulationTime: string
  minutesPerTick: number
  tickSeconds: number
  autoLeaks: boolean
  autoDispatch: boolean
  autoRepair: boolean
  activeLeaks: number
}

