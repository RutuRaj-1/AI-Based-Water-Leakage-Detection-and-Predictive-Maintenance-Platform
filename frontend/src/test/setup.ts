import '@testing-library/jest-dom'

// Mock client dimensions for Leaflet containers in JSDOM
if (typeof window !== 'undefined') {
  Object.defineProperty(HTMLElement.prototype, 'clientWidth', {
    configurable: true,
    value: 1024,
  })
  Object.defineProperty(HTMLElement.prototype, 'clientHeight', {
    configurable: true,
    value: 768,
  })
}

