# GIS Design — Pune Water Network AI

> **Status:** Planned. This document describes the intended GIS visualisation approach. The map component has not been implemented yet.

**Lead:** Bhargavi

---

## Purpose

The GIS (Geographic Information System) layer provides interactive spatial visualisation of the Pune water distribution network, including:

- Pipe segment network with health-score colour coding
- Node locations (junctions, reservoirs, tanks)
- Anomaly markers with severity indicators
- Zone and district boundaries (if available)

---

## Planned Technology

| Component | Library/Tool | Notes |
|-----------|-------------|-------|
| Map renderer | Leaflet 1.9 via React-Leaflet | Open-source, well-supported |
| Base tile layer | OpenStreetMap (default); Mapbox/Esri (optional) | OSM is free; Mapbox requires API key |
| Vector overlay | GeoJSON | Pipe segments and nodes as GeoJSON FeatureCollections |
| Spatial queries | PostGIS (backend) | Bounding-box and proximity queries |

---

## Data Requirements

### Pipeline Network GeoJSON

Each pipe segment requires a GeoJSON `LineString` feature with properties:

```json
{
  "type": "Feature",
  "geometry": { "type": "LineString", "coordinates": [[lng, lat], ...] },
  "properties": {
    "pipe_id": "uuid",
    "label": "P-001",
    "health_score": 72.5,
    "diameter_mm": 150,
    "material": "CI",
    "anomaly_count_30d": 2
  }
}
```

### Network Nodes GeoJSON

Each node requires a GeoJSON `Point` feature.

---

## Map Layers (Planned)

| Layer | Type | Description |
|-------|------|-------------|
| Base map | Tile | OpenStreetMap background |
| Pipe network | Vector (LineString) | Coloured by health score (green → yellow → red) |
| Nodes | Vector (Point) | Circles sized by node type (reservoir larger) |
| Anomaly markers | Vector (Point) | Pulsing markers for active anomaly locations |
| Zone boundaries | Vector (Polygon) | Pune administrative zones (if data is available) |

---

## Health Score Colour Scheme (Planned)

| Health Score | Colour | Meaning |
|-------------|--------|---------|
| 80–100 | Green (`#22c55e`) | Healthy |
| 60–79 | Yellow (`#eab308`) | Monitor |
| 40–59 | Orange (`#f97316`) | Attention needed |
| 20–39 | Red (`#ef4444`) | High risk |
| 0–19 | Dark red (`#7f1d1d`) | Critical |

---

## API Integration

The frontend will consume the following planned endpoints to populate map data:

- `GET /api/v1/networks/{network_id}/features` — GeoJSON FeatureCollection for the entire network
- `GET /api/v1/anomalies?active=true` — Current active anomalies with locations
- `GET /api/v1/pipes/{pipe_id}` — Detail panel on pipe click

---

## Decisions Pending

- [ ] Confirm tile provider (OSM free vs Mapbox paid for higher quality)
- [ ] Confirm EPSG for all geometries (WGS84 recommended for Leaflet)
- [ ] Confirm network GeoJSON source (synthetic vs real PMC data)
- [ ] Decide whether to use Leaflet's built-in GeoJSON layer or Mapbox-GL-JS (vector tiles for performance with large networks)
- [ ] Accessibility: colour-blind-safe palette for health-score colours
