import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { Badge } from '../common/Badge'

interface TopNavbarProps {
  activeTab?: string
  onTabChange?: (tab: string) => void
}

export function TopNavbar({ activeTab, onTabChange }: TopNavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navItems = [
    { to: '/', label: 'Overview', end: true },
    { to: '/network-map', label: 'Network Map' },
    { to: '/alerts', label: 'Alerts', badgeCount: 3 },
    { to: '/maintenance', label: 'Maintenance' },
  ]

  return (
    <header className="top-navbar bg-white border-b border-slate-200 text-slate-800 sticky top-0 z-40 shadow-xs">
      <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Left Branding */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center shadow-xs">
            {/* Water Network Droplet / Node SVG */}
            <svg
              className="w-6 h-6 text-white"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
              <circle cx="12" cy="14" r="2.5" fill="currentColor" opacity="0.6" />
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight text-slate-900">
                Pune Water Network AI
              </span>
              <span className="text-[10px] uppercase font-semibold tracking-wider px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                Phase 2
              </span>
            </div>
            <p className="text-[11px] text-slate-500 hidden sm:block">
              AI-Powered Leakage Detection &amp; Predictive Maintenance
            </p>
          </div>
        </div>

        {/* Center Navigation Links (Desktop) */}
        <nav
          className="hidden md:flex items-center gap-1 bg-slate-100/80 p-1 rounded-lg border border-slate-200"
          aria-label="Main Navigation"
        >
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              onClick={() => onTabChange?.(item.to)}
              className={({ isActive }) => {
                const active = isActive || activeTab === item.to
                return `relative px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-150 flex items-center gap-2 ${
                  active
                    ? 'bg-white text-blue-600 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
                }`
              }}
            >
              {({ isActive }) => {
                const active = isActive || activeTab === item.to
                return (
                  <>
                    <span>{item.label}</span>
                    {item.badgeCount && (
                      <span
                        className={`text-[10px] px-1.5 py-0.2 rounded-full font-bold ${
                          active
                            ? 'bg-blue-100 text-blue-700'
                            : 'bg-red-600 text-white'
                        }`}
                      >
                        {item.badgeCount}
                      </span>
                    )}
                  </>
                )
              }}
            </NavLink>
          ))}
        </nav>

        {/* Right Status Controls */}
        <div className="flex items-center gap-3">
          {/* Simulation Badge */}
          <Badge variant="neutral" size="md" pulsing={true} className="bg-slate-50 border-slate-200 text-slate-700">
            <span className="text-[11px] font-bold tracking-wider uppercase text-slate-700">
              SIMULATED DATA
            </span>
          </Badge>

          {/* Time & District Badge */}
          <div className="hidden lg:flex flex-col text-right text-xs">
            <span className="text-slate-800 font-medium">PMC Water Works · Sector IV</span>
            <span className="text-slate-500 text-[11px]">Pune, Maharashtra</span>
          </div>

          {/* Mobile Menu Toggle Button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-400"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {mobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1 shadow-md">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              onClick={() => {
                onTabChange?.(item.to)
                setMobileMenuOpen(false)
              }}
              className={({ isActive }) => {
                const active = isActive || activeTab === item.to
                return `w-full text-left px-3 py-2 rounded-md text-sm font-medium flex items-center justify-between ${
                  active
                    ? 'bg-blue-50 text-blue-700 font-semibold'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`
              }}
            >
              <span>{item.label}</span>
              {item.badgeCount && (
                <span className="text-[10px] px-1.5 py-0.5 rounded-full font-bold bg-red-600 text-white">
                  {item.badgeCount}
                </span>
              )}
            </NavLink>
          ))}
          <div className="pt-2 text-xs text-slate-500 border-t border-slate-100">
            PMC Water Works · Sector IV (Simulated)
          </div>
        </div>
      )}
    </header>
  )
}
