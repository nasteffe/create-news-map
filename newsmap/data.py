"""Data loading utilities for external geodata sources.

Supports GeoJSON files and inline GeoJSON geometry dicts.  The render
pipeline calls resolve_geodata() to expand 'geojson' or
'geojson_geometry' keys into spec-compatible 'vertices' lists before
any layers are drawn.
"""

import json
from pathlib import Path
from shapely.geometry import shape


def load_geojson(path):
    """Load a GeoJSON file and return a list of (vertices, properties) tuples.

    Handles FeatureCollection, Feature, and bare Geometry objects.
    Each polygon exterior ring becomes one vertex list.
    """
    with open(Path(path)) as f:
        data = json.load(f)
    return _extract(data)


def geojson_to_vertices(geom_dict):
    """Convert a GeoJSON geometry dict to a list of vertex lists.

    Returns one list per polygon/line in the geometry.
    """
    return _geom_verts(shape(geom_dict))


def resolve_geodata(spec):
    """Expand geojson references in zones and terrain_zones.

    For each item that has a 'geojson' (file path) or 'geojson_geometry'
    (inline dict) key but no 'vertices', the geometry is loaded and the
    item is expanded into one or more entries with 'vertices' set.

    Modifies spec in place and returns it.
    """
    for key in ('zones', 'terrain_zones'):
        items = spec.get(key, [])
        if not items:
            continue
        resolved = []
        for item in items:
            geojson_path = item.get('geojson')
            geojson_geom = item.get('geojson_geometry')

            if geojson_path and 'vertices' not in item:
                for verts, props in load_geojson(geojson_path):
                    entry = {k: v for k, v in item.items() if k != 'geojson'}
                    entry['vertices'] = verts
                    if 'label' not in entry and 'name' in props:
                        entry['label'] = props['name']
                    resolved.append(entry)

            elif geojson_geom and 'vertices' not in item:
                for verts in geojson_to_vertices(geojson_geom):
                    entry = {k: v for k, v in item.items()
                             if k != 'geojson_geometry'}
                    entry['vertices'] = verts
                    resolved.append(entry)

            else:
                resolved.append(item)

        spec[key] = resolved

    return spec


# ── Internal helpers ─────────────────────────────────────────────────────────

def _extract(data):
    """Extract (vertices, properties) pairs from parsed GeoJSON."""
    results = []
    gtype = data.get('type')

    if gtype == 'FeatureCollection':
        for feat in data.get('features', []):
            geom = feat.get('geometry')
            props = feat.get('properties', {})
            if geom:
                for verts in _geom_verts(shape(geom)):
                    results.append((verts, dict(props)))

    elif gtype == 'Feature':
        geom = data.get('geometry')
        props = data.get('properties', {})
        if geom:
            for verts in _geom_verts(shape(geom)):
                results.append((verts, dict(props)))

    else:
        # Bare geometry.
        for verts in _geom_verts(shape(data)):
            results.append((verts, {}))

    return results


def _geom_verts(geom):
    """Convert a shapely geometry to list of coordinate lists."""
    t = geom.geom_type

    if t == 'Polygon':
        return [list(geom.exterior.coords)]
    if t == 'MultiPolygon':
        return [list(p.exterior.coords) for p in geom.geoms]
    if t in ('LineString', 'LinearRing'):
        return [list(geom.coords)]
    if t == 'MultiLineString':
        return [list(line.coords) for line in geom.geoms]
    if t == 'Point':
        return [[(geom.x, geom.y)]]
    if t == 'GeometryCollection':
        out = []
        for g in geom.geoms:
            out.extend(_geom_verts(g))
        return out

    return []
