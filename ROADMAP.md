# newsmap — Roadmap

## Completed

### A: Generalizable
Prove the toolkit works across crisis types without code changes.

- Three maps shipped: flood (Morocco), conflict (Gaza), wildfire (LA)
- LA Firestorm added with zero toolkit modifications
- Scale-aware defaults handle city, metro, and region scales

### C: Robust
Comprehensive test suite.

- 71 tests across four categories: defaults, validation, geo, smoke
- All three production maps render end-to-end in the smoke tests
- Minimal and edge-case specs verified (empty overlays, bare extent)

### B: Visual polish
Improve readability of chrome, legends, and small text.

- Bottom bar flow text, legend items, and source lines enlarged
- Scale bar and inset map labels enlarged
- Panel titles standardized to 10pt across bar chart, metrics, timeline
- Timeline date and event text enlarged
- All changes in toolkit defaults — existing specs benefit automatically

### D: Distribution
Packaging and documentation for someone cloning the repo.

- `pyproject.toml` with dependencies, dev extras, CLI entry point
- `README.md` with install, quick start, spec reference, architecture

### E: Real data integration
GeoJSON loading for zones and terrain zones.

- `newsmap/data.py` — load GeoJSON files or inline geometry dicts
- Zones/terrain_zones accept `geojson` (file path) or `geojson_geometry`
  (inline dict) as alternatives to hand-typed `vertices`
- MultiPolygon features auto-expand to multiple zone entries
- Properties inheritance (e.g. `name` → `label`)
- Render pipeline resolves geodata before layer drawing
- Synthetic hillshade from terrain polygons remains the fallback

### F: Label collision avoidance
Automatic label placement for marker names.

- `newsmap/labels.py` — greedy 8-candidate placement algorithm
- Estimates text bounding boxes in data coordinates from font size and extent
- Avoids overlap with other marker labels, marker dots, zone labels, callouts
- Penalizes out-of-bounds placement, prefers NE (cartographic convention)
- Markers with explicit `name_offset` are fixed by default
- Set `auto_labels: True` in spec to re-optimize all labels
- 105 tests total (34 new), all passing

---

## Open

### E+: Real raster data
The GeoJSON integration (E) handles vector data. Real raster data
(DEM, satellite imagery) would further improve map accuracy:

- **DEM raster** — SRTM or Copernicus 30m tiles for real hillshade
- **Flood extent** — Copernicus EMS or Sentinel-1 SAR flood polygons
- **Fire perimeters** — NIFC/IRWIN GeoJSON feeds for US wildfires
- **Rivers** — HydroSHEDS or higher-resolution Natural Earth overrides

Trade-off: requires rasterio (not currently installed) and adds data
download/caching complexity.

### G: Colour system
Each map hand-picks colours per marker and zone. A structured palette
system (e.g. crisis-type presets, sequential/diverging ramps for panels)
would make new maps more consistent and reduce spec boilerplate.

### H: Editorial workflow
Several commits show fact-check correction passes applied after initial
render. A more systematic approach could include:
- **Source annotations** — link each data point to its provenance URL
- **Diff rendering** — highlight what changed between spec versions
- **Review checklist** — automated checks for stale dates, missing sources,
  or implausible metric values

### I: Additional panel types
The current panel set (bar chart, metrics, timeline) covers most needs.
Candidates for new panel types:
- **Choropleth legend** — continuous colour ramp with labelled stops
- **Sparkline row** — compact time-series for multiple indicators
- **Comparison table** — side-by-side before/after or country-vs-country
- **Photo/image inset** — satellite imagery or ground photos

### J: Export and sharing
Currently outputs JPG and PDF. Possible additions:
- **SVG** — for web embedding and further editing in Illustrator/Inkscape
- **PNG with transparency** — for compositing over satellite basemaps
- **Interactive HTML** — Folium or static Leaflet export for web viewing
- **Social media crops** — auto-generate 16:9, 1:1, and 9:16 variants
