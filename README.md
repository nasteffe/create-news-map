# newsmap

Composable toolkit for publication-quality analytical news maps.

Maps are defined as **pure data specs** (plain Python dicts) with no rendering
logic. The toolkit handles geography, overlays, panels, and chrome — at any
geographic scale from city block to world overview.

## Install

```bash
pip install matplotlib cartopy shapely numpy
```

Or with the project metadata:

```bash
pip install -e .
```

## Quick start

Render all maps (outputs to `output/`):

```bash
python make_map.py
```

Render one map:

```bash
python make_map.py maps.morocco_flood_2026
```

Output files go to the `output/` directory by default. Override with `output.dir` in your spec.

## Writing a map spec

Create a Python module in `maps/` that exports a `MAP` dict. Minimal example:

```python
MAP = {
    'extent': [-7.6, -3.6, 32.6, 37.0],
    'meta': {'title': 'MY MAP'},
    'output': {
        'basename': 'my_map',
        'formats': [{'ext': 'jpg', 'dpi': 200}],
    },
}
```

The toolkit auto-computes scale-aware defaults (coastlines, hillshade, scale
bar, layout) from the extent alone. Override any default by adding the key to
your spec — user values always win.

### Spec keys

| Key | Purpose |
|-----|---------|
| `extent` | `[lon_min, lon_max, lat_min, lat_max]` — required |
| `meta` | Title, subtitle, tagline |
| `terrain_zones` | Colored elevation polygons for hillshade |
| `rivers` | Manual river polylines with labels |
| `zones` | Analytical overlay polygons — `vertices`, `geojson`, or `geojson_geometry` |
| `scatter_marks` | Random scatter fields (destruction, farmland) |
| `markers` | Point markers with auto-placed labels (or explicit `name_offset`) |
| `arrow_groups` | Grouped flow arrows (displacement, wind) |
| `lines` | Styled lines (roads, supply chains) |
| `callouts` | Text labels on the map |
| `inset` | Locator inset map with context labels |
| `panels` | Side panels: `bar_chart`, `metrics`, `timeline` |
| `bottom_bar` | Metabolic flows, legend, source attribution |
| `output` | `dir` (default `'output'`), `basename`, and format list (ext + dpi) |

## Architecture

```
newsmap/
  text.py      Font resolution, halo effects
  geo.py       Physical geography (ocean, land, hillshade, terrain, borders, coast, rivers, lakes)
  marks.py     Analytical overlays (zones, markers, arrows, lines, callouts)
  labels.py    Label collision avoidance (auto-placement for marker names)
  data.py      GeoJSON loading and geodata resolution
  panels.py    Side panels (bar charts, metrics, timelines)
  chrome.py    Figure chrome (title, scale bar, legend, sources)
  defaults.py  Scale-aware defaults engine
  validate.py  Spec validation
  render.py    Composable pipeline: spec → layers → figure → files

maps/
  morocco_flood_2026.py    Western Mediterranean flood crisis
  gaza_ceasefire_2026.py   Gaza ceasefire-to-reconstruction
  la_firestorm_2025.py     Los Angeles wildfire event

output/       Generated maps (gitignored)
make_map.py   CLI entry point with auto-discovery
```

Design principles:

- **Pure data specs** — maps are plain dicts, no logic
- **Scale-aware defaults** — sensible rendering from city to world scale
- **Composable layers** — small modules, each does one thing
- **Override anything** — every computed default is replaceable

## Tests

```bash
python -m pytest tests/ -v
```

110 tests across six categories: defaults, validation, geography, labels, data, smoke rendering.
