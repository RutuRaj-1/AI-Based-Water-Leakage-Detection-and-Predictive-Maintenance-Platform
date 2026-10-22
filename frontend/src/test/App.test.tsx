/**
 * App smoke test — confirms the application renders without crashing.
 * Foundation stage only.
 */
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from '../App'

describe('App', () => {
  it('renders the project title', () => {
    render(<App />)
    expect(
      screen.getByText(/Pune Water Network AI/i)
    ).toBeInTheDocument()
  })

  it('shows the foundation badge', () => {
    render(<App />)
    // "Foundation" appears in both the header badge and the footer; use getAllByText
    const matches = screen.getAllByText(/Foundation/i)
    expect(matches.length).toBeGreaterThan(0)
    // The header badge specifically
    expect(screen.getByText('Foundation · Stage 1')).toBeInTheDocument()
  })
})
