import type { CriticalAsset, LeakAlert, MaintenanceTask } from '../types/dashboard'

/**
 * Illustrative simulated leak alerts for Pune Water Network AI
 * All data is synthetic and generated for demonstration purposes.
 */
export const simulatedAlerts: LeakAlert[] = [
  {
    id: 'ALT-104',
    title: 'Sudden Pressure Drop (>1.4 bar)',
    location: 'Katraj Trunk Sector 4',
    pipelineId: 'Pipe P-104',
    estimatedLoss: '~42 m³/hr',
    severity: 'critical',
    timestamp: '12m ago',
    status: 'active',
  },
  {
    id: 'ALT-089',
    title: 'Night Flow Rate Deviation',
    location: 'Swargate DMA-3 Feeder',
    pipelineId: 'Pipe P-067',
    estimatedLoss: '~18 m³/hr',
    severity: 'high',
    timestamp: '35m ago',
    status: 'investigating',
  },
  {
    id: 'ALT-062',
    title: 'Acoustic Signature Anomaly',
    location: 'Kothrud West Arterial',
    pipelineId: 'Pipe P-211',
    estimatedLoss: '~6.5 m³/hr',
    severity: 'moderate',
    timestamp: '1h 14m ago',
    status: 'active',
  },
  {
    id: 'ALT-055',
    title: 'Flow Micro-Turbulence Spike',
    location: 'Sinhagad Main Feed Branch',
    pipelineId: 'Pipe P-101',
    estimatedLoss: '~4.2 m³/hr',
    severity: 'moderate',
    timestamp: '2h 10m ago',
    status: 'investigating',
  },
  {
    id: 'ALT-047',
    title: 'Minor Joint Seepage Indicator',
    location: 'Hadapsar Distribution Line',
    pipelineId: 'Pipe P-088',
    estimatedLoss: '~2.1 m³/hr',
    severity: 'low',
    timestamp: '4h 45m ago',
    status: 'active',
  },
  {
    id: 'ALT-031',
    title: 'Telemetry Heartbeat Restored',
    location: 'Parvati Intake Pumping',
    pipelineId: 'PS-01',
    estimatedLoss: '0 m³/hr',
    severity: 'normal',
    timestamp: '6h 12m ago',
    status: 'resolved',
  },
]

/**
 * Illustrative critical assets watchlist
 */
export const criticalAssets: CriticalAsset[] = [
  {
    id: 'P-104',
    name: 'Katraj Feeder Main (P-104)',
    assetType: 'pipe',
    healthScore: 24,
    material: 'Cast Iron (CI 300mm)',
    ageYears: 38,
    criticality: 'urgent',
    zone: 'Zone 4 — Katraj',
  },
  {
    id: 'P-042',
    name: 'Shivajinagar Sub-main (P-042)',
    assetType: 'pipe',
    healthScore: 31,
    material: 'Ductile Iron (DI 250mm)',
    ageYears: 29,
    criticality: 'high',
    zone: 'Zone 1 — Central',
  },
  {
    id: 'PS-02',
    name: 'Parvati High-Lift Pump PS-02',
    assetType: 'pump',
    healthScore: 46,
    material: 'Centrifugal 45kW',
    ageYears: 14,
    criticality: 'medium',
    zone: 'Parvati WTP',
  },
  {
    id: 'P-088',
    name: 'Hadapsar Distribution (P-088)',
    assetType: 'pipe',
    healthScore: 38,
    material: 'Mild Steel (MS 200mm)',
    ageYears: 22,
    criticality: 'high',
    zone: 'Zone 7 — Hadapsar',
  },
]

/**
 * Illustrative predictive maintenance tasks / work orders
 */
export const maintenanceTasks: MaintenanceTask[] = [
  {
    id: 'task-1',
    workOrderNumber: 'WO-804',
    title: 'Emergency acoustic survey & pipe joint clamp',
    targetAsset: 'Pipe P-104 (Katraj)',
    priority: 'urgent',
    priorityScore: 94,
    assignedTeam: 'Rapid Response Unit 2',
    dueDate: 'Today · Immediate',
  },
  {
    id: 'task-2',
    workOrderNumber: 'WO-802',
    title: 'Isolation valve inspection & seal replacement',
    targetAsset: 'Valve V-41 (Swargate)',
    priority: 'high',
    priorityScore: 81,
    assignedTeam: 'South Maintenance Crew',
    dueDate: 'Tomorrow · 09:00',
  },
  {
    id: 'task-3',
    workOrderNumber: 'WO-799',
    title: 'Ultrasonic pipe wall thickness diagnostic',
    targetAsset: 'Pipe P-042 (Shivajinagar)',
    priority: 'medium',
    priorityScore: 62,
    assignedTeam: 'Asset Inspection Team',
    dueDate: 'Oct 26 · Scheduled',
  },
  {
    id: 'task-4',
    workOrderNumber: 'WO-795',
    title: 'Pumping impellor dynamic balance test',
    targetAsset: 'Pump PS-02 (Parvati WTP)',
    priority: 'medium',
    priorityScore: 58,
    assignedTeam: 'Electro-Mechanical Unit',
    dueDate: 'Oct 28 · Preventive',
  },
  {
    id: 'task-5',
    workOrderNumber: 'WO-788',
    title: 'Hadapsar distribution cathodics & soil pH test',
    targetAsset: 'Pipe P-088 (Hadapsar)',
    priority: 'routine',
    priorityScore: 45,
    assignedTeam: 'Corrosion Survey Unit',
    dueDate: 'Nov 02 · Routine',
  },
]
