"""Render pipeline: spec → figure → files.

The pipeline is function composition: create axes, apply layers in
sequence, save. Each layer reads its own keys from the spec and skips
gracefully if the data isn't present.

Scale-aware defaults are computed from the extent and deep-merged under
the user spec, so every value is overridable and existing specs render
identically.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import warnings

from . import geo, marks, panels, chrome, defaults, validate, data

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
    shape. Every key is optional except 'extent'. Omit what you don't
    need — scale-aware defaults fill the rest.
    """
    # Validate before rendering (skip with '_skip_validation': True).
    if not spec.get('_skip_validation'):
        validate.check(spec)

    # Resolve external geodata (GeoJSON → vertices) before merging.
    data.resolve_geodata(spec)

    # Merge scale-aware defaults under user spec (user always wins).
    computed = defaults.for_extent(spec['extent'])
    spec = defaults.deep_merge(computed, spec)

    size = spec['layout']['size']
    proj = _get_projection(spec)
    fig = plt.figure(figsize=size, dpi=150)
    fig.patch.set_facecolor('white')

    # Map axes.
    map_rect = spec['layout']['map']
    ax = fig.add_axes(map_rect, projection=proj)
    ax.set_extent(spec['extent'], crs=proj)

    # Apply geography layers, then overlays.
    for layer in GEO_LAYERS + OVERLAY_LAYERS:
        layer(ax, spec, proj)

    # Figure-level elements.
    chrome.title_block(fig, spec)
    chrome.scale_bar(ax, spec, proj)
    _inset_map(fig, spec)
    panels.render_panels(fig, spec)
    chrome.bottom_bar(fig, spec)
    chrome.annotation_text(fig, spec)

    # Save.
    output = spec['output']
    basename = output.get('basename', 'map')
    for fmt in output.get('formats', [{'ext': 'jpg', 'dpi': 200}]):
        path = f"{basename}.{fmt['ext']}"
        fig.savefig(path, dpi=fmt['dpi'],
                    bbox_inches='tight', pad_inches=0.1,
                    facecolor='white')
        print(f"  {path} ({fmt['dpi']} dpi)")

    plt.close(fig)
    return fig


def _inset_map(fig, spec):
    """Draw a small locator inset showing the main map area in context."""
    inset = spec.get('inset')
    if not inset:
        return

    import cartopy.feature as cfeature
    from matplotlib.patches import Rectangle

    proj = ccrs.PlateCarree()
    ax = fig.add_axes(inset['rect'], projection=proj)
    ax.set_extent(inset['extent'], crs=proj)

    # Simplified background.
    colors = spec.get('colors', {})
    ax.set_facecolor(colors.get('ocean', '#C8DDE8'))
    inset_res = inset.get('resolution', '50m')
    ax.add_feature(cfeature.NaturalEarthFeature(
        'physical', 'land', inset_res,
        facecolor=colors.get('land', '#E8E2D8'), edgecolor='none'), zorder=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3,
                   edgecolor='#AAAAAA', zorder=2)
    ax.coastlines(resolution=inset_res, linewidth=0.4, color='#8A9AA6', zorder=3)

    # Red rectangle showing the main map extent.
    e = spec['extent']  # [lon_min, lon_max, lat_min, lat_max]
    rect = Rectangle((e[0], e[2]), e[1] - e[0], e[3] - e[2],
                      linewidth=1.5, edgecolor='#C03030',
                      facecolor='#C03030', alpha=0.35,
                      transform=proj, zorder=10)
    ax.add_patch(rect)

    # Frame.
    for spine in ax.spines.values():
        spine.set_edgecolor('#666666')
        spine.set_linewidth(0.8)

    # Optional labels.
    from . import text as _text
    for lbl in inset.get('labels', []):
        ax.text(lbl['lon'], lbl['lat'], lbl['text'],
                fontsize=lbl.get('size', 5.5),
                color=lbl.get('color', '#666666'),
                ha=lbl.get('ha', 'center'), va=lbl.get('va', 'center'),
                transform=proj, zorder=15, **_text.font('body'))


# ── Projection handling ─────────────────────────────────────────────────────

_PROJECTIONS = {
    'PlateCarree': ccrs.PlateCarree,
    'Mercator': ccrs.Mercator,
    'LambertConformal': ccrs.LambertConformal,
    'Robinson': ccrs.Robinson,
    'Mollweide': ccrs.Mollweide,
    'Orthographic': ccrs.Orthographic,
    'AlbersEqualArea': ccrs.AlbersEqualArea,
    'AzimuthalEquidistant': ccrs.AzimuthalEquidistant,
    'LambertAzimuthalEqualArea': ccrs.LambertAzimuthalEqualArea,
    'NorthPolarStereo': ccrs.NorthPolarStereo,
    'SouthPolarStereo': ccrs.SouthPolarStereo,
}


def _get_projection(spec):
    """Resolve projection to cartopy CRS.

    Accepts either a string name or a dict with 'name' + parameters:
        'projection': 'PlateCarree'
        'projection': {'name': 'Robinson', 'central_longitude': -5}
    """
    proj_spec = spec.get('projection', 'PlateCarree')

    if isinstance(proj_spec, str):
        cls = _PROJECTIONS.get(proj_spec, ccrs.PlateCarree)
        return cls()

    # Dict form: {'name': '...', **kwargs}
    name = proj_spec.get('name', 'PlateCarree')
    cls = _PROJECTIONS.get(name, ccrs.PlateCarree)
    params = {k: v for k, v in proj_spec.items() if k != 'name'}
    return cls(**params)
