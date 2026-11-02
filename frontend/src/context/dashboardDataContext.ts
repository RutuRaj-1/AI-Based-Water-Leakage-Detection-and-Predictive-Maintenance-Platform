import { createContext, useContext } from 'react'
import type { DashboardSnapshot } from '../services/api'
import type { LeakAlert, WorkOrderStatus } from '../types/dashboard'

export type ConnectionState = 'connecting' | 'live' | 'offline'

export interface DashboardDataContextValue {
  data: DashboardSnapshot
  connection: ConnectionState
  lastUpdated: Date | null
  refresh: () => Promise<void>
  setAlertStatus: (id: string, status: LeakAlert['status']) => Promise<void>
  setTaskStatus: (id: string, status: WorkOrderStatus) => Promise<void>
  simulationControl: (action: 'pause' | 'resume' | 'reset') => Promise<void>
  injectLeak: (pipeId: string, rateM3h?: number) => Promise<void>
}

export const DashboardDataContext = createContext<DashboardDataContextValue | null>(null)

export function useDashboardData(): DashboardDataContextValue {
  const ctx = useContext(DashboardDataContext)
  if (!ctx) throw new Error('useDashboardData must be used inside <DashboardDataProvider>')
  return ctx
}

