import React from 'react'

interface DashboardLayoutProps {
  topNavbar: React.ReactNode
  leftPanel?: React.ReactNode
  centerMap?: React.ReactNode
  rightPanel?: React.ReactNode
  bottomPanel?: React.ReactNode
  children?: React.ReactNode
}

export function DashboardLayout({
  topNavbar,
  leftPanel,
  centerMap,
  rightPanel,
  bottomPanel,
  children,
}: DashboardLayoutProps) {
  return (
    <div className="dashboard-root min-h-screen bg-[#F5F7FA] text-slate-800 flex flex-col font-sans">
      {/* 1. Top Navigation */}
      {topNavbar}

      {/* 2. Main Content Area */}
      {children ? (
        <main className="dashboard-main flex-1 w-full max-w-[1920px] mx-auto p-2 sm:p-4 flex flex-col min-w-0">
          {children}
        </main>
      ) : (
        <main className="dashboard-main flex-1 w-full max-w-[1920px] mx-auto p-2 sm:p-4 flex flex-col xl:flex-row gap-3 sm:gap-4 overflow-hidden">
          {/* Left Panel: Asset Health & Pipeline Conditions */}
          {leftPanel && (
            <div className="w-full xl:w-[330px] 2xl:w-[360px] xl:shrink-0 flex flex-col">
              {leftPanel}
            </div>
          )}

          {/* Center Panel: Large GIS Map Area */}
          {centerMap && (
            <div className="flex-1 flex flex-col min-w-0">
              {centerMap}
            </div>
          )}

          {/* Right Panel: Leak Alerts & Maintenance Priorities */}
          {rightPanel && (
            <div className="w-full xl:w-[350px] 2xl:w-[380px] xl:shrink-0 flex flex-col">
              {rightPanel}
            </div>
          )}
        </main>
      )}

      {/* 3. Bottom Summary & Simulation Controls */}
      {bottomPanel}
    </div>
  )
}
