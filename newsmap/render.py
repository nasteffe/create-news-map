"""Render pipeline: spec → figure → files.

The pipeline is function composition: create axes, apply layers in
sequence, save. Each layer reads its own keys from the spec and skips
gracefully if the data isn't present.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import warnings

from . import geo, marks, panels, chrome

warnings.filterwarnings('ignore')

# Layer sequence — order matters (bottom to top).
GEO_LAYERS = [
    geo.ocean,
    geo.land,
    geo.hillshade,
    geo.terrain_zones,
    geo.borders,
    geo.coastline,
    geo.rivers,
    geo.lakes,
]

OVERLAY_LAYERS = [
    marks.zones,
    marks.scatter,
    marks.markers,
    marks.arrow_groups,
    marks.lines,
    marks.callouts,
]


def render(spec):
    """Main entry point: render a map spec to output files.

    spec is a plain dict. See maps/morocco_flood_2026.py for the full
    shape. Every key is optional — omit what you don't need.
    """
    size = spec.get('layout', {}).get('size', (16.54, 11.69))
    proj = _get_projection(spec)
    fig = plt.figure(figsize=size, dpi=150)
    fig.patch.set_facecolor('white')

    # Map axes.
    map_rect = spec.get('layout', {}).get('map', [0.01, 0.145, 0.58, 0.80])
    ax = fig.add_axes(map_rect, projection=proj)
    ax.set_extent(spec['extent'], crs=proj)

    # Apply geography layers, then overlays.
    for layer in GEO_LAYERS + OVERLAY_LAYERS:
        layer(ax, spec, proj)

    # Figure-level elements.
    chrome.title_block(fig, spec)
    chrome.scale_bar(ax, spec, proj)
    panels.render_panels(fig, spec)
    chrome.bottom_bar(fig, spec)
    chrome.annotation_text(fig, spec)

    # Save.
    output = spec.get('output', {})
    basename = output.get('basename', 'map')
    for fmt in output.get('formats', [{'ext': 'jpg', 'dpi': 200}]):
        path = f"{basename}.{fmt['ext']}"
        fig.savefig(path, dpi=fmt['dpi'],
                    bbox_inches='tight', pad_inches=0.1,
                    facecolor='white')
        print(f"  {path} ({fmt['dpi']} dpi)")

    plt.close(fig)
    return fig


def _get_projection(spec):
    """Resolve projection name to cartopy CRS."""
    name = spec.get('projection', 'PlateCarree')
    projections = {
        'PlateCarree': ccrs.PlateCarree,
        'Mercator': ccrs.Mercator,
        'LambertConformal': ccrs.LambertConformal,
        'Robinson': ccrs.Robinson,
    }
    cls = projections.get(name, ccrs.PlateCarree)
    return cls()
