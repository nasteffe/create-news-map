"""Spec validation: catch common errors before rendering.

Lightweight checks that run fast and fail with clear messages.
Called automatically by render() unless disabled with '_skip_validation'.
"""


def check(spec):
    """Validate a map spec dict. Raises ValueError on problems."""
    errors = []

    # ── Required keys ───────────────────────────────────────────────────
    if 'extent' not in spec:
        errors.append("Missing required key 'extent' — [lon_min, lon_max, lat_min, lat_max]")

    # ── Extent sanity ───────────────────────────────────────────────────
    e = spec.get('extent')
    if e is not None:
        if not (isinstance(e, (list, tuple)) and len(e) == 4):
            errors.append(f"'extent' must be [lon_min, lon_max, lat_min, lat_max], got {e!r}")
        else:
            lon_min, lon_max, lat_min, lat_max = e
            if lon_min >= lon_max:
                errors.append(f"extent lon_min ({lon_min}) >= lon_max ({lon_max})")
            if lat_min >= lat_max:
                errors.append(f"extent lat_min ({lat_min}) >= lat_max ({lat_max})")
            if not (-180 <= lon_min <= 180 and -180 <= lon_max <= 180):
                errors.append(f"extent longitudes out of range: [{lon_min}, {lon_max}]")
            if not (-90 <= lat_min <= 90 and -90 <= lat_max <= 90):
                errors.append(f"extent latitudes out of range: [{lat_min}, {lat_max}]")

    # ── Projection ──────────────────────────────────────────────────────
    proj = spec.get('projection')
    if proj is not None:
        from .render import _PROJECTIONS
        if isinstance(proj, str):
            if proj not in _PROJECTIONS:
                errors.append(
                    f"Unknown projection '{proj}'. "
                    f"Available: {', '.join(sorted(_PROJECTIONS))}")
        elif isinstance(proj, dict):
            name = proj.get('name', 'PlateCarree')
            if name not in _PROJECTIONS:
                errors.append(
                    f"Unknown projection name '{name}'. "
                    f"Available: {', '.join(sorted(_PROJECTIONS))}")

    # ── Panel types ─────────────────────────────────────────────────────
    known_panels = {'bar_chart', 'metrics', 'timeline'}
    for i, p in enumerate(spec.get('panels', [])):
        ptype = p.get('type')
        if ptype not in known_panels:
            errors.append(
                f"panels[{i}]: unknown type '{ptype}'. "
                f"Available: {', '.join(sorted(known_panels))}")
        if 'rect' not in p:
            errors.append(f"panels[{i}] (type='{ptype}'): missing 'rect'")

    # ── Markers ─────────────────────────────────────────────────────────
    for i, m in enumerate(spec.get('markers', [])):
        for key in ('lon', 'lat', 'name', 'color'):
            if key not in m:
                errors.append(f"markers[{i}]: missing required key '{key}'")

    # ── Terrain zones ───────────────────────────────────────────────────
    for i, z in enumerate(spec.get('terrain_zones', [])):
        verts = z.get('vertices')
        if verts is None:
            errors.append(f"terrain_zones[{i}]: missing 'vertices'")
        elif len(verts) < 3:
            errors.append(f"terrain_zones[{i}]: need >= 3 vertices, got {len(verts)}")

    # ── Zones (analytical overlays) ─────────────────────────────────────
    for i, z in enumerate(spec.get('zones', [])):
        verts = z.get('vertices')
        if verts is None:
            errors.append(f"zones[{i}]: missing 'vertices'")
        elif len(verts) < 3:
            errors.append(f"zones[{i}]: need >= 3 vertices, got {len(verts)}")

    # ── Output ──────────────────────────────────────────────────────────
    for i, fmt in enumerate(spec.get('output', {}).get('formats', [])):
        if 'ext' not in fmt:
            errors.append(f"output.formats[{i}]: missing 'ext'")
        if 'dpi' not in fmt:
            errors.append(f"output.formats[{i}]: missing 'dpi'")

    if errors:
        msg = f"Spec validation failed ({len(errors)} error{'s' if len(errors) > 1 else ''}):\n"
        msg += '\n'.join(f"  - {e}" for e in errors)
        raise ValueError(msg)
