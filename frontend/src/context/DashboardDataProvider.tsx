import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react'
import { fallbackSnapshot } from '../data/fallbackSnapshot'
import { api, type DashboardSnapshot } from '../services/api'
import {
  DashboardDataContext,
  type ConnectionState,
  type DashboardDataContextValue,
} from './dashboardDataContext'

interface ProviderProps {
  children: ReactNode
  /** Polling interval in ms. 0 disables background polling (used in tests). */
  pollMs?: number
}

/**
 * Fetches the live dashboard snapshot from the backend, polls it, and exposes
 * operator actions. Falls back to bundled synthetic data when the API is down.
 */
export function DashboardDataProvider({ children, pollMs = 3000 }: ProviderProps) {
  const [data, setData] = useState<DashboardSnapshot>(fallbackSnapshot)
  const [connection, setConnection] = useState<ConnectionState>('connecting')
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const mounted = useRef(true)
  const wasOffline = useRef(false)

  const refresh = useCallback(async () => {
    try {
      const snap = await api.snapshot()
      if (!mounted.current) return
      wasOffline.current = false
      setData(snap)
      setConnection('live')
      setLastUpdated(new Date())
    } catch {
      if (!mounted.current) return
      if (!wasOffline.current) setData(fallbackSnapshot)
      wasOffline.current = true
      setConnection('offline')
    }
  }, [])

  useEffect(() => {
    mounted.current = true
    const initTimer = setTimeout(() => {
      void refresh()
    }, 0)
    let timer: ReturnType<typeof setInterval> | undefined
    if (pollMs > 0) {
      timer = setInterval(() => {
        if (!document.hidden) void refresh()
      }, pollMs)
    }
    return () => {
      mounted.current = false
      clearTimeout(initTimer)
      if (timer) clearInterval(timer)
    }
  }, [refresh, pollMs])

  const value = useMemo<DashboardDataContextValue>(() => {
    const act = (fn: () => Promise<unknown>) => async () => {
      try {
        await fn()
      } catch (err) {
        console.warn('Backend action failed:', err)
      }
      await refresh()
    }
    return {
      data,
      connection,
      lastUpdated,
      refresh,
      setAlertStatus: (id, status) => act(() => api.setAlertStatus(id, status))(),
      setTaskStatus: (id, status) => act(() => api.setTaskStatus(id, status))(),
      simulationControl: (action) => act(() => api.simulation(action))(),
      injectLeak: (pipeId, rate) => act(() => api.injectLeak(pipeId, rate))(),
    }
  }, [data, connection, lastUpdated, refresh])

  return <DashboardDataContext.Provider value={value}>{children}</DashboardDataContext.Provider>
}
