"""Physical geography layers.

Every public function draws one layer onto a cartopy GeoAxes.
Signature convention: fn(ax, spec, proj) → None.
Each reads its own key from the spec dict and skips if absent.
"""

import numpy as np
import cartopy.feature as cfeature
from matplotlib.colors import LightSource
from matplotlib.path import Path
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import prepared

from . import text


# ── Layer functions ──────────────────────────────────────────────────────────

def ocean(ax, spec, proj):
    """Fill ocean with a flat colour (axes background)."""
    ax.set_facecolor(spec.get('colors', {}).get('ocean', '#D4E4F0'))


def land(ax, spec, proj):
    """Draw Natural Earth land polygons."""
    colors = spec.get('colors', {})
    res = spec.get('ne_resolution', '10m')
    feat = cfeature.NaturalEarthFeature(
        'physical', 'land', res,
        facecolor=colors.get('land', '#E6DFD4'), edgecolor='none')
    ax.add_feature(feat, zorder=1)


def hillshade(ax, spec, proj):
    """Synthetic hillshade from terrain zone elevations.

    Creates a smoothed DEM grid from the elevation values assigned to each
    terrain zone, then renders a LightSource hillshade at low alpha.
    Adds physical depth without overwhelming the analytical layers.
    """
    zones = spec.get('terrain_zones', [])
    if not zones or not spec.get('hillshade', True):
        return

    extent = spec['extent']
    res = spec.get('hillshade_resolution', 250)
    alpha = spec.get('hillshade_alpha', 0.13)
    passes = spec.get('hillshade_smooth', 12)

    lons = np.linspace(extent[0], extent[1], res)
    lats = np.linspace(extent[2], extent[3], res)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    points = np.column_stack([lon_grid.ravel(), lat_grid.ravel()])

    # Start at sea level; terrain zones paint elevation onto the grid.
    elev = np.full((res, res), 0.0)

    # Apply zones in order (later zones override earlier ones).
    for z in sorted(zones, key=lambda z: z.get('elevation', 100)):
        path = Path(z['vertices'])
        mask = path.contains_points(points).reshape(res, res)
        elev[mask] = z.get('elevation', 100)

    # Box-blur smoothing for natural transitions.
    elev = _smooth(elev, passes)

    # Compute hillshade.
    ls = LightSource(azdeg=315, altdeg=45)
    shade = ls.hillshade(elev, vert_exag=3, dx=1, dy=1)

    ax.imshow(shade, origin='lower',
              extent=[extent[0], extent[1], extent[2], extent[3]],
              transform=proj, cmap='gray', alpha=alpha, zorder=2,
              interpolation='bilinear')


def terrain_zones(ax, spec, proj):
    """Draw coloured terrain polygons (Rif, Atlas, plains, etc.)."""
    for z in spec.get('terrain_zones', []):
        poly = Polygon(z['vertices'])
        ax.add_geometries(
            [poly], proj,
            facecolor=z.get('color', '#C8BCA8'),
            edgecolor='none',
            alpha=z.get('alpha', 0.5),
            zorder=3)


def ocean_mask(ax, spec, proj):
    """Re-draw ocean above terrain zones and hillshade.

    This clips any terrain polygon or hillshade shading that bleeds
    past the coastline into water.  Drawn at zorder=3.5 — above
    terrain_zones (3) and hillshade (2), but below rivers (4),
    borders (5), coastline (6), and all overlays (7+).
    """
    colors = spec.get('colors', {})
    res = spec.get('ne_resolution', '10m')
    feat = cfeature.NaturalEarthFeature(
        'physical', 'ocean', res,
        facecolor=colors.get('ocean', '#D4E4F0'),
        edgecolor='none')
    ax.add_feature(feat, zorder=3.5)


def borders(ax, spec, proj):
    """Country borders from Natural Earth."""
    colors = spec.get('colors', {})
    ax.add_feature(cfeature.BORDERS,
                   edgecolor=colors.get('border', '#8A7A66'),
                   linewidth=spec.get('border_width', 1.2),
                   zorder=5)


def coastline(ax, spec, proj):
    """Coastline from Natural Earth."""
    colors = spec.get('colors', {})
    res = spec.get('ne_resolution', '10m')
    feat = cfeature.NaturalEarthFeature(
        'physical', 'coastline', res,
        facecolor='none', edgecolor=colors.get('coast', '#8A7A66'))
    ax.add_feature(feat, linewidth=spec.get('coast_width', 1.5), zorder=6)


def rivers(ax, spec, proj):
    """Draw rivers: Natural Earth base + manual overrides from spec."""
    colors = spec.get('colors', {})
    river_color = colors.get('river', '#4A90C4')

    # Natural Earth rivers as a subtle base layer.
    if spec.get('ne_rivers', True):
        try:
            res = spec.get('ne_resolution', '10m')
            feat = cfeature.NaturalEarthFeature(
                'physical', 'rivers_lake_centerlines', res,
                facecolor='none', edgecolor=river_color)
            ax.add_feature(feat, linewidth=1.2, alpha=0.5, zorder=4)
        except Exception:
            pass

    # Manual river lines from spec for key rivers.
    for r in spec.get('rivers', []):
        coords = r['coords']
        ax.plot([c[0] for c in coords], [c[1] for c in coords],
                color=river_color,
                linewidth=r.get('width', 2.0),
                alpha=r.get('alpha', 0.8),
                transform=proj, zorder=4, solid_capstyle='round')
        # Optional label.
        lp = r.get('label_pos')
        if lp:
            ax.text(lp[0], lp[1], r['name'],
                    fontsize=r.get('label_size', 6),
                    color=river_color, fontstyle='italic',
                    rotation=r.get('label_rotation', 0),
                    path_effects=text.halo(2.5),
                    transform=proj, zorder=10,
                    **text.font('body'))


def lakes(ax, spec, proj):
    """Natural Earth lakes/reservoirs."""
    if not spec.get('lakes', True):
        return
    try:
        res = spec.get('ne_resolution', '10m')
        feat = cfeature.NaturalEarthFeature(
            'physical', 'lakes', res,
            facecolor=spec.get('colors', {}).get('ocean', '#D4E4F0'),
            edgecolor='none')
        ax.add_feature(feat, alpha=0.6, zorder=4)
    except Exception:
        pass


# ── Internal helpers ─────────────────────────────────────────────────────────

def _smooth(grid, passes=10):
    """Simple 3x3 box-blur. No scipy dependency."""
    for _ in range(passes):
        p = np.pad(grid, 1, mode='edge')
        grid = (p[:-2, :-2] + p[:-2, 1:-1] + p[:-2, 2:] +
                p[1:-1, :-2] + p[1:-1, 1:-1] + p[1:-1, 2:] +
                p[2:, :-2] + p[2:, 1:-1] + p[2:, 2:]) / 9.0
    return grid


# ── Land geometry for point-in-land tests ────────────────────────────────────

# Module-level cache: {(resolution, extent_tuple): prepared_geometry}
_land_cache = {}


def land_geometry(spec):
    """Return a prepared shapely geometry for land within the map extent.

    Uses Natural Earth land polygons at the spec's resolution, clipped
    to the map extent for fast point-in-polygon tests.  The result is
    cached per (resolution, extent) so repeated calls are free.
    """
    extent = spec['extent']
    res = spec.get('ne_resolution', '10m')
    key = (res, tuple(extent))

    if key in _land_cache:
        return _land_cache[key]

    # Build a bounding box slightly larger than the extent to avoid
    # edge artefacts with coastline simplification.
    pad = 0.5
    bbox = box(extent[0] - pad, extent[2] - pad,
               extent[1] + pad, extent[3] + pad)

    # Load Natural Earth land geometries that intersect our bbox.
    reader = cfeature.NaturalEarthFeature('physical', 'land', res)
    land_polys = []
    for geom in reader.geometries():
        clipped = geom.intersection(bbox)
        if not clipped.is_empty:
            land_polys.append(clipped)

    if land_polys:
        merged = unary_union(land_polys)
    else:
        # Fallback: treat entire extent as land (no filtering).
        merged = bbox

    prep = prepared.prep(merged)
    _land_cache[key] = prep
    return prep
