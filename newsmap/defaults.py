"""Scale-aware defaults: compute sensible rendering parameters from extent.

The goal: a user should be able to specify just an extent, some markers,
and a title — and get a reasonable analytical map at any geographic scale,
from world overview down to city block.

All values here are overridable. The merge order is:
    computed_defaults | user_spec  (user wins)
"""

import copy

# ── Scale classification ────────────────────────────────────────────────────

_SCALE_BREAKS = [
    # (max_span, name)
    (0.5,   'city'),
    (2.0,   'metro'),
    (8.0,   'region'),
    (30.0,  'country'),
    (100.0, 'continent'),
]


def classify_scale(extent):
    """Return a scale name and the dominant span in degrees."""
    lon_span = extent[1] - extent[0]
    lat_span = extent[3] - extent[2]
    span = max(lon_span, lat_span)
    for threshold, name in _SCALE_BREAKS:
        if span <= threshold:
            return name, span
    return 'world', span


# ── Defaults by scale ───────────────────────────────────────────────────────

# Natural Earth resolution: finer for tighter extents.
_NE_RES = {
    'city': '10m', 'metro': '10m', 'region': '10m',
    'country': '10m', 'continent': '50m', 'world': '110m',
}

# Hillshade grid cells: more cells for tighter extents (finer detail).
_HS_RES = {
    'city': 350, 'metro': 300, 'region': 280,
    'country': 250, 'continent': 200, 'world': 180,
}

_HS_SMOOTH = {
    'city': 16, 'metro': 14, 'region': 12,
    'country': 10, 'continent': 8, 'world': 6,
}

# Round scale-bar distances (km).
_NICE_KM = [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]


def _pick_scale_km(span):
    """Choose a round km value ≈15% of the map width."""
    # 1° latitude ≈ 111 km.
    map_km = span * 111
    target = map_km * 0.15
    return min(_NICE_KM, key=lambda k: abs(k - target))


# ── Main entry point ────────────────────────────────────────────────────────

def for_extent(extent):
    """Compute a full defaults dict from a [lon_min, lon_max, lat_min, lat_max].

    Returns a spec-shaped dict that render() will deep-merge under the
    user's spec, so every value here is overridable.
    """
    scale, span = classify_scale(extent)
    lon_span = extent[1] - extent[0]
    lat_span = extent[3] - extent[2]
    mid_lon = (extent[0] + extent[1]) / 2
    mid_lat = (extent[2] + extent[3]) / 2

    # Offset unit: a small fraction of span, used for label placement.
    offset = span * 0.015

    # Scale bar position: bottom-left of map area.
    sb_lon = extent[0] + lon_span * 0.05
    sb_lat = extent[2] + lat_span * 0.05
    sb_km = _pick_scale_km(span)
    sb_tick = span * 0.008

    return {
        # Natural Earth feature resolution.
        'ne_resolution': _NE_RES[scale],

        # Hillshade.
        'hillshade': True,
        'hillshade_alpha': 0.13,
        'hillshade_resolution': _HS_RES[scale],
        'hillshade_smooth': _HS_SMOOTH[scale],

        # Rivers.
        'ne_rivers': True,
        'lakes': scale not in ('city',),

        # Colors — neutral palette that works at any scale.
        'colors': {
            'ocean':  '#D4E4F0',
            'land':   '#E6DFD4',
            'border': '#8A7A66',
            'coast':  '#8A7A66',
            'river':  '#4A90C4',
        },

        # Layout.
        'projection': 'PlateCarree',
        'layout': {
            'size': (16.54, 11.69),
            'map': [0.01, 0.145, 0.58, 0.80],
        },

        # Scale bar.
        'scale_bar': {
            'lon': sb_lon,
            'lat': sb_lat,
            'km': sb_km,
            'reference_lat': mid_lat,
            'tick': sb_tick,
        },

        # Output.
        'output': {
            'basename': 'map',
            'formats': [{'ext': 'jpg', 'dpi': 200}],
        },

        # Internal: computed scale metadata (used by renderers).
        '_scale': {
            'name': scale,
            'span': span,
            'offset': offset,
            'lon_span': lon_span,
            'lat_span': lat_span,
            'mid': (mid_lon, mid_lat),
        },
    }


# ── Deep merge ──────────────────────────────────────────────────────────────

def deep_merge(base, override):
    """Recursively merge override into base. override wins on conflicts.

    Lists are NOT merged — override replaces entirely.
    """
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result
