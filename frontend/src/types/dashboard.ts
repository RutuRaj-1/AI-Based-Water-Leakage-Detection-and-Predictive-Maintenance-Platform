/**
 * Type definitions for the Pune Water Network AI Dashboard (Phase 1 — Simulated)
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

