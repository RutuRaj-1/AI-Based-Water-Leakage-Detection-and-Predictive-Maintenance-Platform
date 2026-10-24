import React from 'react'
import type { SeverityLevel } from '../../types/dashboard'

interface BadgeProps {
  children: React.ReactNode
  variant?: SeverityLevel | 'info' | 'accent' | 'neutral'
  size?: 'sm' | 'md'
  pulsing?: boolean
  className?: string
}

const variantStyles: Record<string, string> = {
  critical: 'bg-red-50 text-red-700 border-red-200',
  high: 'bg-orange-50 text-orange-700 border-orange-200',
  moderate: 'bg-amber-50 text-amber-800 border-amber-200',
  low: 'bg-blue-50 text-blue-700 border-blue-200',
  normal: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  info: 'bg-blue-50 text-blue-700 border-blue-200',
  accent: 'bg-sky-50 text-sky-800 border-sky-200',
  neutral: 'bg-slate-100 text-slate-700 border-slate-200',
}

export function Badge({
  children,
  variant = 'neutral',
  size = 'sm',
  pulsing = false,
  className = '',
}: BadgeProps) {
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-sm'
  const style = variantStyles[variant] || variantStyles.neutral

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-medium rounded-full border ${style} ${sizeClasses} ${className}`}
    >
      {pulsing && (
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-current opacity-75" />
          <span className="relative inline-flex rounded-full h-2 w-2 bg-current" />
        </span>
      )}
      {children}
    </span>
  )
}
