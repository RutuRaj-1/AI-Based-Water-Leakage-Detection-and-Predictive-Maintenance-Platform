interface SparklineProps {
  values: number[]
  className?: string
  stroke?: string
  width?: number
  height?: number
}

/** Tiny dependency-free SVG trend line. */
export function Sparkline({ values, className = '', stroke = '#2563EB', width = 96, height = 24 }: SparklineProps) {
  if (values.length < 2) return null
  const min = Math.min(...values)
  const max = Math.max(...values)
  const span = max - min || 1
  const step = width / (values.length - 1)
  const points = values
    .map((v, i) => `${(i * step).toFixed(1)},${(height - 2 - ((v - min) / span) * (height - 4)).toFixed(1)}`)
    .join(' ')
  return (
    <svg className={className} width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-hidden="true">
      <polyline points={points} fill="none" stroke={stroke} strokeWidth="1.5" strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  )
}

