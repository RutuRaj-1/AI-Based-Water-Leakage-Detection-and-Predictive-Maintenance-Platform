import type { FeatureCollection, LineString, Point } from 'geojson'
import type {
  LeakMarkerProperties,
  NetworkNodeProperties,
  PipelineCondition,
  PipelineProperties,
} from '../types/dashboard'

export const SYNTHETIC_DATA_NOTICE =
  'SIMULATED DATA: Synthetic water distribution hydraulic geometry for Pune network demonstration and AI predictive maintenance testing. Coordinates and sensor telemetry do not represent verified Pune Municipal Corporation (PMC) infrastructure.'

export const PUNE_MAP_CENTER: [number, number] = [18.5204, 73.8567] // Latitude, Longitude for Leaflet
export const PUNE_DEFAULT_ZOOM = 12

export const CONDITION_COLORS: Record<PipelineCondition, string> = {
  healthy: '#16A34A', // Green 600
  monitor: '#D97706', // Amber 600
  attention: '#EA580C', // Orange 600
  critical: '#DC2626', // Red 600
}

export function getConditionColor(condition: PipelineCondition): string {
  return CONDITION_COLORS[condition] ?? '#94a3b8'
}

/**
 * Synthetic Pune Water Distribution Pipelines
 * Note: GeoJSON coordinates are in [longitude, latitude] standard EPSG:4326.
 */
export const syntheticPipelines: FeatureCollection<LineString, PipelineProperties> = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'P-104',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.858, 18.5018],
          [73.861, 18.479],
          [73.855, 18.465],
          [73.856, 18.4485],
        ],
      },
      properties: {
        id: 'P-104',
        name: 'Katraj Feeder Main (P-104)',
        zone: 'Zone 4 — Katraj',
        diameterMm: 300,
        material: 'Cast Iron (CI 300mm)',
        healthScore: 24,
        condition: 'critical',
        pressureBar: 1.9,
        flowRateMld: 28.4,
        lengthKm: 6.8,
      },
    },
    {
      type: 'Feature',
      id: 'P-042',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.8585, 18.5025],
          [73.844, 18.52],
          [73.852, 18.5315],
        ],
      },
      properties: {
        id: 'P-042',
        name: 'Shivajinagar Sub-main (P-042)',
        zone: 'Zone 1 — Central',
        diameterMm: 250,
        material: 'Ductile Iron (DI 250mm)',
        healthScore: 31,
        condition: 'critical',
        pressureBar: 2.3,
        flowRateMld: 19.2,
        lengthKm: 4.2,
      },
    },
    {
      type: 'Feature',
      id: 'P-067',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.8474, 18.4975],
          [73.853, 18.4985],
          [73.858, 18.5018],
        ],
      },
      properties: {
        id: 'P-067',
        name: 'Swargate DMA-3 Feeder (P-067)',
        zone: 'Zone 3 — Swargate DMA',
        diameterMm: 350,
        material: 'Mild Steel (MS 350mm)',
        healthScore: 52,
        condition: 'attention',
        pressureBar: 3.1,
        flowRateMld: 24.1,
        lengthKm: 2.1,
      },
    },
    {
      type: 'Feature',
      id: 'P-088',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.8585, 18.5025],
          [73.892, 18.498],
          [73.928, 18.502],
        ],
      },
      properties: {
        id: 'P-088',
        name: 'Hadapsar Distribution (P-088)',
        zone: 'Zone 7 — Hadapsar',
        diameterMm: 200,
        material: 'Mild Steel (MS 200mm)',
        healthScore: 38,
        condition: 'critical',
        pressureBar: 2.7,
        flowRateMld: 14.5,
        lengthKm: 7.6,
      },
    },
    {
      type: 'Feature',
      id: 'P-211',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.8474, 18.4975],
          [73.828, 18.503],
          [73.815, 18.505],
          [73.808, 18.5075],
        ],
      },
      properties: {
        id: 'P-211',
        name: 'Kothrud West Arterial (P-211)',
        zone: 'Zone 2 — Kothrud',
        diameterMm: 250,
        material: 'Ductile Iron (DI 250mm)',
        healthScore: 68,
        condition: 'monitor',
        pressureBar: 3.2,
        flowRateMld: 18.0,
        lengthKm: 4.8,
      },
    },
    {
      type: 'Feature',
      id: 'P-015',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.8474, 18.4975],
          [73.878, 18.514],
          [73.893, 18.536],
        ],
      },
      properties: {
        id: 'P-015',
        name: 'Cantonment Main Trunk (P-015)',
        zone: 'Zone 5 — Cantonment',
        diameterMm: 500,
        material: 'Prestressed Concrete (PSC 500mm)',
        healthScore: 92,
        condition: 'healthy',
        pressureBar: 4.2,
        flowRateMld: 42.0,
        lengthKm: 6.1,
      },
    },
    {
      type: 'Feature',
      id: 'P-033',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.852, 18.5315],
          [73.829, 18.537],
          [73.805, 18.56],
        ],
      },
      properties: {
        id: 'P-033',
        name: 'Aundh-Baner Feeder (P-033)',
        zone: 'Zone 6 — Aundh/Baner',
        diameterMm: 350,
        material: 'Ductile Iron (DI 350mm)',
        healthScore: 86,
        condition: 'healthy',
        pressureBar: 3.7,
        flowRateMld: 26.5,
        lengthKm: 5.9,
      },
    },
    {
      type: 'Feature',
      id: 'P-050',
      geometry: {
        type: 'LineString',
        coordinates: [
          [73.893, 18.536],
          [73.902, 18.548],
          [73.914, 18.567],
        ],
      },
      properties: {
        id: 'P-050',
        name: 'Viman Nagar Primary Main (P-050)',
        zone: 'Zone 8 — Viman Nagar',
        diameterMm: 300,
        material: 'Ductile Iron (DI 300mm)',
        healthScore: 88,
        condition: 'healthy',
        pressureBar: 3.5,
        flowRateMld: 21.0,
        lengthKm: 5.3,
      },
    },
  ],
}

/**
 * Synthetic Network Nodes (Pumps, Reservoirs, Treatment Plants, Junctions)
 */
export const syntheticNodes: FeatureCollection<Point, NetworkNodeProperties> = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'RES-PARVATI',
      geometry: {
        type: 'Point',
        coordinates: [73.8474, 18.4975],
      },
      properties: {
        id: 'RES-PARVATI',
        name: 'Parvati WTP & Master Reservoir',
        nodeType: 'treatment_plant',
        zone: 'Central Water Works',
        pressureBar: 4.8,
        elevationM: 570,
        baseDemandLps: 450,
      },
    },
    {
      type: 'Feature',
      id: 'RES-KATRAJ',
      geometry: {
        type: 'Point',
        coordinates: [73.856, 18.4485],
      },
      properties: {
        id: 'RES-KATRAJ',
        name: 'Katraj Elevated Storage Reservoir',
        nodeType: 'reservoir',
        zone: 'Zone 4 — Katraj',
        pressureBar: 3.2,
        elevationM: 615,
        baseDemandLps: 220,
      },
    },
    {
      type: 'Feature',
      id: 'RES-CHATURSHRINGI',
      geometry: {
        type: 'Point',
        coordinates: [73.829, 18.537],
      },
      properties: {
        id: 'RES-CHATURSHRINGI',
        name: 'Chaturshringi High Reservoir',
        nodeType: 'reservoir',
        zone: 'Zone 6 — Aundh/Baner',
        pressureBar: 3.9,
        elevationM: 595,
        baseDemandLps: 180,
      },
    },
    {
      type: 'Feature',
      id: 'PS-02',
      geometry: {
        type: 'Point',
        coordinates: [73.8485, 18.499],
      },
      properties: {
        id: 'PS-02',
        name: 'Parvati High-Lift Pump PS-02',
        nodeType: 'pump',
        zone: 'Parvati WTP',
        pressureBar: 5.4,
        elevationM: 568,
        baseDemandLps: 320,
      },
    },
    {
      type: 'Feature',
      id: 'PS-05',
      geometry: {
        type: 'Point',
        coordinates: [73.858, 18.5018],
      },
      properties: {
        id: 'PS-05',
        name: 'Swargate Booster Station PS-05',
        nodeType: 'pump',
        zone: 'Zone 3 — Swargate DMA',
        pressureBar: 4.1,
        elevationM: 555,
        baseDemandLps: 210,
      },
    },
    {
      type: 'Feature',
      id: 'J-SWARGATE',
      geometry: {
        type: 'Point',
        coordinates: [73.8585, 18.5025],
      },
      properties: {
        id: 'J-SWARGATE',
        name: 'Swargate Main Junction',
        nodeType: 'junction',
        zone: 'Zone 3 — Swargate DMA',
        pressureBar: 3.8,
        elevationM: 554,
        baseDemandLps: 120,
      },
    },
    {
      type: 'Feature',
      id: 'J-SHIVAJINAGAR',
      geometry: {
        type: 'Point',
        coordinates: [73.852, 18.5315],
      },
      properties: {
        id: 'J-SHIVAJINAGAR',
        name: 'Shivajinagar Interconnect',
        nodeType: 'junction',
        zone: 'Zone 1 — Central',
        pressureBar: 3.5,
        elevationM: 552,
        baseDemandLps: 140,
      },
    },
    {
      type: 'Feature',
      id: 'J-HADAPSAR',
      geometry: {
        type: 'Point',
        coordinates: [73.928, 18.502],
      },
      properties: {
        id: 'J-HADAPSAR',
        name: 'Hadapsar Terminal Junction',
        nodeType: 'junction',
        zone: 'Zone 7 — Hadapsar',
        pressureBar: 3.1,
        elevationM: 550,
        baseDemandLps: 160,
      },
    },
    {
      type: 'Feature',
      id: 'J-KOTHRUD',
      geometry: {
        type: 'Point',
        coordinates: [73.808, 18.5075],
      },
      properties: {
        id: 'J-KOTHRUD',
        name: 'Kothrud West Junction',
        nodeType: 'junction',
        zone: 'Zone 2 — Kothrud',
        pressureBar: 3.4,
        elevationM: 565,
        baseDemandLps: 130,
      },
    },
  ],
}

/**
 * Synthetic Simulated Leak Anomaly Markers
 */
export const syntheticLeaks: FeatureCollection<Point, LeakMarkerProperties> = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      id: 'ALT-104',
      geometry: {
        type: 'Point',
        coordinates: [73.855, 18.465],
      },
      properties: {
        id: 'ALT-104',
        pipelineId: 'P-104',
        severity: 'critical',
        estimatedLoss: '~42 m³/hr',
        location: 'Katraj Trunk Sector 4',
        detectionTime: '12m ago',
        status: 'active',
      },
    },
    {
      type: 'Feature',
      id: 'ALT-089',
      geometry: {
        type: 'Point',
        coordinates: [73.853, 18.4985],
      },
      properties: {
        id: 'ALT-089',
        pipelineId: 'P-067',
        severity: 'high',
        estimatedLoss: '~18 m³/hr',
        location: 'Swargate DMA-3 Feeder',
        detectionTime: '35m ago',
        status: 'investigating',
      },
    },
    {
      type: 'Feature',
      id: 'ALT-062',
      geometry: {
        type: 'Point',
        coordinates: [73.815, 18.505],
      },
      properties: {
        id: 'ALT-062',
        pipelineId: 'P-211',
        severity: 'moderate',
        estimatedLoss: '~6.5 m³/hr',
        location: 'Kothrud West Arterial',
        detectionTime: '1h 14m ago',
        status: 'active',
      },
    },
  ],
}
