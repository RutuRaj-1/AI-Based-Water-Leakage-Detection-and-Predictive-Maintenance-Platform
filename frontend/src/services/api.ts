/**
 * Typed client for the Pune Water Network AI backend (FastAPI, /api/v1).
 *
 * Base URL: VITE_API_BASE_URL, defaulting to the same-origin `/api/v1`
 * (proxied to the backend by Vite in dev and by nginx in Docker).
 */

import type { FeatureCollection, LineString, Point } from 'geojson'
import type {
  ActivityEvent,
  CriticalAsset,
  LeakAlert,
  LeakMarkerProperties,
  MaintenanceTask,
  NetworkNodeProperties,
  NetworkSummary,
  PipelineProperties,
  SimulationStatus,
  SimulationTelemetry,
  TelemetryPoint,
  WorkOrderStatus,
} from '../types/dashboard'

export interface DashboardSnapshot {
  generatedAt: string
  notice: string
  telemetry: SimulationTelemetry
  summary: NetworkSummary
  alerts: LeakAlert[]
  criticalAssets: CriticalAsset[]
  maintenanceTasks: MaintenanceTask[]
  pipelines: FeatureCollection<LineString, PipelineProperties>
  nodes: FeatureCollection<Point, NetworkNodeProperties>
  leaks: FeatureCollection<Point, LeakMarkerProperties>
  events: ActivityEvent[]
  history: TelemetryPoint[]
  simulation: SimulationStatus
}

export const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, '') || '/api/v1'

const API_KEY = import.meta.env.VITE_API_KEY as string | undefined

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, init: RequestInit = {}, timeoutMs = 5000): Promise<T> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const headers: Record<string, string> = { Accept: 'application/json' }
    if (init.body) headers['Content-Type'] = 'application/json'
    if (API_KEY) headers['X-API-Key'] = API_KEY
    const res = await fetch(`${API_BASE_URL}${path}`, { ...init, headers, signal: controller.signal })
    if (!res.ok) {
      let detail = res.statusText
      try {
        detail = ((await res.json()) as { detail?: string }).detail ?? detail
      } catch {
        /* non-JSON error body */
      }
      throw new ApiError(res.status, detail)
    }
    return (await res.json()) as T
  } finally {
    clearTimeout(timer)
  }
}

const post = <T>(path: string, body?: unknown) =>
  request<T>(path, { method: 'POST', body: body === undefined ? undefined : JSON.stringify(body) })
const patch = <T>(path: string, body: unknown) =>
  request<T>(path, { method: 'PATCH', body: JSON.stringify(body) })

export const api = {
  health: () => request<{ status: string; version: string; environment: string }>('/health', {}, 2500),
  snapshot: () => request<DashboardSnapshot>('/dashboard/snapshot'),
  setAlertStatus: (id: string, status: LeakAlert['status']) =>
    patch<LeakAlert>(`/alerts/${encodeURIComponent(id)}`, { status }),
  setTaskStatus: (id: string, status: WorkOrderStatus) =>
    patch<MaintenanceTask>(`/maintenance/tasks/${encodeURIComponent(id)}`, { status }),
  simulation: (action: 'pause' | 'resume' | 'reset') => post<SimulationStatus>(`/simulation/${action}`),
  step: (ticks = 1) => post<SimulationStatus>('/simulation/step', { ticks }),
  injectLeak: (pipeId: string, rateM3h = 25) => post<{ leakId: string }>('/simulation/leaks', { pipeId, rateM3h }),
}

