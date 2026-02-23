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

---

## Open

### E: Real data integration
Terrain currently uses synthetic hillshade built from hand-drawn polygons.
Rivers and flood extents are also manual coordinates. Integrating real
geospatial data would improve accuracy and reduce spec authoring effort.

Candidates:
- **DEM raster** — SRTM or Copernicus 30m tiles for real hillshade
- **Flood extent** — Copernicus Emergency Management Service or Sentinel-1
  SAR-derived flood polygons
- **Fire perimeters** — NIFC/IRWIN GeoJSON feeds for US wildfires
- **Rivers** — HydroSHEDS or higher-resolution Natural Earth overrides

Trade-off: adds data download/caching complexity. The current synthetic
approach keeps specs self-contained and reproducible with no external files.

### F: Label collision avoidance
Marker labels are placed with fixed offsets. When markers cluster (northern
Gaza, Morocco flood zone), labels overlap. An automatic label placement
pass — either adjustable-force layout or greedy grid snapping — would
eliminate manual `name_offset` tuning in specs.

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
