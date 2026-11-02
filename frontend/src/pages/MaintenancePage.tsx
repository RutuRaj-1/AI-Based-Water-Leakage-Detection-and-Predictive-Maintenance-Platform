import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { DashboardLayout } from '../layouts/DashboardLayout'
import { TopNavbar } from '../components/dashboard/TopNavbar'
import { Badge } from '../components/common/Badge'
import { maintenanceTasks, criticalAssets } from '../data/dashboardData'
import type { MaintenanceTask } from '../types/dashboard'

export function MaintenancePage() {
  const [priorityFilter, setPriorityFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState<string>('')
  const [selectedTaskId, setSelectedTaskId] = useState<string>(maintenanceTasks[0]?.id || '')
  const [taskStatusMap, setTaskStatusMap] = useState<Record<string, string>>({
    'task-1': 'In Progress',
    'task-2': 'Dispatched',
    'task-3': 'Scheduled',
    'task-4': 'Scheduled',
    'task-5': 'Planned',
  })

  // Filter tasks
  const filteredTasks = useMemo(() => {
    return maintenanceTasks.filter((task) => {
      const matchesPriority =
        priorityFilter === 'all' || task.priority === priorityFilter

      const matchesSearch =
        searchQuery === '' ||
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.targetAsset.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.workOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.assignedTeam.toLowerCase().includes(searchQuery.toLowerCase())

      return matchesPriority && matchesSearch
    })
  }, [priorityFilter, searchQuery])

  // Selected task
  const selectedTask: MaintenanceTask | undefined = useMemo(() => {
    return (
      maintenanceTasks.find((t) => t.id === selectedTaskId) ||
      filteredTasks[0] ||
      maintenanceTasks[0]
    )
  }, [selectedTaskId, filteredTasks])

  // Correlate with critical asset if applicable
  const matchedAsset = useMemo(() => {
    if (!selectedTask) return null
    return criticalAssets.find((a) =>
      selectedTask.targetAsset.includes(a.id)
    )
  }, [selectedTask])

  const countsByPriority = useMemo(() => {
    return {
      all: maintenanceTasks.length,
      urgent: maintenanceTasks.filter((t) => t.priority === 'urgent').length,
      high: maintenanceTasks.filter((t) => t.priority === 'high').length,
      medium: maintenanceTasks.filter((t) => t.priority === 'medium').length,
      routine: maintenanceTasks.filter((t) => t.priority === 'routine').length,
    }
  }, [])

  const handleUpdateStatus = (taskId: string, newStatus: string) => {
    setTaskStatusMap((prev) => ({ ...prev, [taskId]: newStatus }))
  }

  const getPriorityBadgeVariant = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'critical'
      case 'high':
        return 'high'
      case 'medium':
        return 'moderate'
      default:
        return 'neutral'
    }
  }

  return (
    <DashboardLayout topNavbar={<TopNavbar />}>
      <div className="flex flex-col gap-4 max-w-[1920px] mx-auto w-full pb-8">
        {/* Page Header */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xs">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
                <svg
                  className="w-5 h-5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                </svg>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-lg font-bold text-slate-900 tracking-tight">
                    Predictive Maintenance &amp; Work Orders
                  </h1>
                  <Badge variant="info" size="sm">
                    {maintenanceTasks.length} Active Orders
                  </Badge>
                </div>
                <p className="text-xs text-slate-500">
                  AI-prioritized remedial interventions ranked by asset vulnerability, pressure history, and estimated water loss
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Badge variant="neutral" size="md">
              <span className="text-[11px] font-semibold text-slate-700 uppercase">
                Simulated Maintenance
              </span>
            </Badge>
            <Link
              to="/network-map"
              className="px-3 py-1.5 rounded-lg bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700 shadow-xs transition-colors flex items-center gap-1.5"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" />
                <line x1="8" y1="2" x2="8" y2="18" />
                <line x1="16" y1="6" x2="16" y2="22" />
              </svg>
              View Assets on Map
            </Link>
          </div>
        </div>

        {/* Priority Filter KPI Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <button
            type="button"
            onClick={() => setPriorityFilter('all')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              priorityFilter === 'all'
                ? 'bg-blue-50/80 border-blue-400 ring-2 ring-blue-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-slate-500 block">Total Work Orders</span>
            <span className="text-2xl font-bold text-slate-900 block mt-0.5">{countsByPriority.all}</span>
            <span className="text-[10px] text-slate-500 mt-1 block">All queued actions</span>
          </button>

          <button
            type="button"
            onClick={() => setPriorityFilter('urgent')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              priorityFilter === 'urgent'
                ? 'bg-rose-50 border-rose-400 ring-2 ring-rose-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-rose-600 block">Urgent Priority</span>
            <span className="text-2xl font-bold text-rose-700 block mt-0.5">{countsByPriority.urgent}</span>
            <span className="text-[10px] text-rose-600 font-medium mt-1 block">Score &ge; 90 · Today</span>
          </button>

          <button
            type="button"
            onClick={() => setPriorityFilter('high')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              priorityFilter === 'high'
                ? 'bg-amber-50 border-amber-400 ring-2 ring-amber-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-amber-600 block">High Priority</span>
            <span className="text-2xl font-bold text-amber-700 block mt-0.5">{countsByPriority.high}</span>
            <span className="text-[10px] text-amber-600 font-medium mt-1 block">Score 80–89</span>
          </button>

          <button
            type="button"
            onClick={() => setPriorityFilter('medium')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              priorityFilter === 'medium'
                ? 'bg-orange-50 border-orange-400 ring-2 ring-orange-500/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-orange-600 block">Medium Priority</span>
            <span className="text-2xl font-bold text-orange-700 block mt-0.5">{countsByPriority.medium}</span>
            <span className="text-[10px] text-slate-500 mt-1 block">Scheduled preventive</span>
          </button>

          <button
            type="button"
            onClick={() => setPriorityFilter('routine')}
            className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
              priorityFilter === 'routine'
                ? 'bg-slate-100 border-slate-400 ring-2 ring-slate-400/20 shadow-xs'
                : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
            }`}
          >
            <span className="text-[11px] uppercase font-semibold text-slate-600 block">Routine</span>
            <span className="text-2xl font-bold text-slate-800 block mt-0.5">{countsByPriority.routine}</span>
            <span className="text-[10px] text-slate-500 mt-1 block">Periodic inspection</span>
          </button>
        </div>

        {/* Filter and Search Bar */}
        <div className="bg-white border border-slate-200 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 shadow-xs">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs font-semibold text-slate-600 mr-1">Filter:</span>
            {(['all', 'urgent', 'high', 'medium', 'routine'] as const).map((pri) => (
              <button
                key={pri}
                type="button"
                onClick={() => setPriorityFilter(pri)}
                className={`px-3 py-1 rounded-md text-xs font-medium capitalize transition-all cursor-pointer ${
                  priorityFilter === pri
                    ? 'bg-blue-600 text-white font-semibold shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {pri === 'all' ? 'All Orders' : pri}
              </button>
            ))}
          </div>

          <div className="relative w-full sm:w-72">
            <input
              type="text"
              placeholder="Search by WO#, asset, or team..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200 bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-400 text-slate-800 placeholder-slate-400"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1.5 text-xs text-slate-400 hover:text-slate-600"
              >
                Clear
              </button>
            )}
          </div>
        </div>

        {/* 2-Column Work Orders Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Column 1: Work Order Cards (7 cols) */}
          <div className="lg:col-span-7 flex flex-col gap-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                Work Orders ({filteredTasks.length})
              </span>
              <span className="text-[11px] text-slate-500">
                Select an order to view execution status &amp; asset specs
              </span>
            </div>

            {filteredTasks.length === 0 ? (
              <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">
                <p className="font-medium text-sm">No work orders match the filter criteria.</p>
                <button
                  type="button"
                  onClick={() => {
                    setPriorityFilter('all')
                    setSearchQuery('')
                  }}
                  className="mt-2 text-xs text-blue-600 font-semibold hover:underline"
                >
                  Reset filters
                </button>
              </div>
            ) : (
              filteredTasks.map((task) => {
                const isSelected = task.id === selectedTask?.id
                const currentStatus = taskStatusMap[task.id] || 'Scheduled'
                return (
                  <div
                    key={task.id}
                    onClick={() => setSelectedTaskId(task.id)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        setSelectedTaskId(task.id)
                      }
                    }}
                    className={`bg-white border rounded-xl p-4 transition-all cursor-pointer relative shadow-xs ${
                      isSelected
                        ? 'border-blue-500 ring-2 ring-blue-500/20 bg-blue-50/30'
                        : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50/50'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1.5">
                          <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                            {task.workOrderNumber}
                          </span>
                          <Badge
                            variant={getPriorityBadgeVariant(task.priority)}
                            size="sm"
                            pulsing={task.priority === 'urgent'}
                          >
                            {task.priority.toUpperCase()}
                          </Badge>
                          <span className="text-[11px] px-2 py-0.5 rounded font-medium bg-slate-100 text-slate-700 border border-slate-200">
                            {currentStatus}
                          </span>
                          <div className="ml-auto flex items-center gap-1.5">
                            <span className="text-[11px] text-slate-500">Priority Score:</span>
                            <span className="text-sm font-bold text-blue-600">
                              {task.priorityScore}/100
                            </span>
                          </div>
                        </div>

                        <h3 className="text-sm font-bold text-slate-900 leading-snug">
                          {task.title}
                        </h3>

                        {/* Priority Score Bar */}
                        <div className="mt-2 h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              task.priorityScore >= 90
                                ? 'bg-[#DC2626]'
                                : task.priorityScore >= 75
                                  ? 'bg-[#D97706]'
                                  : 'bg-[#2563EB]'
                            }`}
                            style={{ width: `${task.priorityScore}%` }}
                          />
                        </div>

                        <div className="mt-3 grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs text-slate-600 pt-2 border-t border-slate-100">
                          <div>
                            <span className="text-slate-400 block text-[10px] uppercase font-medium">Target Asset</span>
                            <span className="font-semibold text-slate-800">{task.targetAsset}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px] uppercase font-medium">Assigned Team</span>
                            <span className="font-medium text-slate-800">{task.assignedTeam}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px] uppercase font-medium">Due Date / SLA</span>
                            <span className="font-semibold text-amber-800">{task.dueDate}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>

          {/* Column 2: Selected Work Order Detail Pane (5 cols) */}
          <div className="lg:col-span-5">
            {selectedTask ? (
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs sticky top-20 flex flex-col gap-4">
                <div className="border-b border-slate-100 pb-3 flex items-start justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500">
                      Work Order Specification
                    </span>
                    <h2 className="text-base font-bold text-slate-900 mt-0.5">
                      {selectedTask.workOrderNumber}
                    </h2>
                  </div>
                  <Badge variant={getPriorityBadgeVariant(selectedTask.priority)} size="md">
                    {selectedTask.priority.toUpperCase()}
                  </Badge>
                </div>

                <div className="space-y-1">
                  <span className="text-[10px] uppercase font-bold text-slate-500">Task Objective</span>
                  <p className="text-sm font-semibold text-slate-900 leading-snug">
                    {selectedTask.title}
                  </p>
                </div>

                {/* Priority Score Breakdown */}
                <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-700">Predictive Urgency Score</span>
                    <span className="font-extrabold text-blue-600 text-sm">
                      {selectedTask.priorityScore} / 100
                    </span>
                  </div>
                  <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        selectedTask.priorityScore >= 90
                          ? 'bg-[#DC2626]'
                          : selectedTask.priorityScore >= 75
                            ? 'bg-[#D97706]'
                            : 'bg-[#2563EB]'
                      }`}
                      style={{ width: `${selectedTask.priorityScore}%` }}
                    />
                  </div>
                  <div className="text-[11px] text-slate-500 flex justify-between">
                    <span>Rank: #{maintenanceTasks.findIndex((t) => t.id === selectedTask.id) + 1} of {maintenanceTasks.length}</span>
                    <span>Due: {selectedTask.dueDate}</span>
                  </div>
                </div>

                {/* Associated Asset Info */}
                <div className="space-y-2 text-xs">
                  <span className="text-xs font-bold text-slate-700 block uppercase tracking-wide">
                    Associated Asset Profile
                  </span>
                  {matchedAsset ? (
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-900">{matchedAsset.name}</span>
                        <span className={`text-[11px] font-bold px-1.5 py-0.5 rounded ${
                          matchedAsset.healthScore < 30 ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                        }`}>
                          Condition: {matchedAsset.healthScore}%
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-x-2 gap-y-1 text-[11px] text-slate-600">
                        <div>
                          <strong className="text-slate-800">Material:</strong> {matchedAsset.material}
                        </div>
                        <div>
                          <strong className="text-slate-800">Age:</strong> {matchedAsset.ageYears} yrs
                        </div>
                        <div className="col-span-2">
                          <strong className="text-slate-800">Zone:</strong> {matchedAsset.zone}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-slate-600">
                      <p className="font-semibold text-slate-800">{selectedTask.targetAsset}</p>
                      <p className="text-[11px] mt-0.5">Assigned: {selectedTask.assignedTeam}</p>
                    </div>
                  )}
                </div>

                {/* Team & Dispatch Status Control */}
                <div className="space-y-2 text-xs">
                  <span className="text-xs font-bold text-slate-700 block uppercase tracking-wide">
                    Execution State &amp; Team
                  </span>
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2.5">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Assigned Team:</span>
                      <span className="font-semibold text-slate-900">{selectedTask.assignedTeam}</span>
                    </div>

                    <div className="flex items-center justify-between pt-1 border-t border-slate-200">
                      <span className="text-slate-600">Update Status:</span>
                      <div className="flex items-center gap-1">
                        {(['Scheduled', 'Dispatched', 'In Progress', 'Completed'] as const).map((st) => {
                          const isActive = taskStatusMap[selectedTask.id] === st
                          return (
                            <button
                              key={st}
                              type="button"
                              onClick={() => handleUpdateStatus(selectedTask.id, st)}
                              className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                                isActive
                                  ? 'bg-blue-600 text-white font-semibold'
                                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
                              }`}
                            >
                              {st}
                            </button>
                          )
                        })}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Quick Action Navigation */}
                <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
                  <Link
                    to="/network-map"
                    className="flex-1 text-center py-2 px-3 rounded-lg bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700 shadow-xs transition-colors"
                  >
                    Locate Asset on Map
                  </Link>
                  <Link
                    to="/alerts"
                    className="flex-1 text-center py-2 px-3 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold hover:bg-slate-200 transition-colors"
                  >
                    View Active Alerts
                  </Link>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
