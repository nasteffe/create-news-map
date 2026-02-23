"""Unit tests for newsmap.data — GeoJSON loading and geodata resolution."""

import json
import pytest
from pathlib import Path
from newsmap.data import load_geojson, geojson_to_vertices, resolve_geodata


# ── GeoJSON vertex extraction ────────────────────────────────────────────────

class TestGeojsonToVertices:

    def test_polygon(self):
        geom = {
            'type': 'Polygon',
            'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        }
        verts = geojson_to_vertices(geom)
        assert len(verts) == 1
        assert len(verts[0]) == 5  # closed ring
        assert verts[0][0] == (0, 0)

    def test_multipolygon(self):
        geom = {
            'type': 'MultiPolygon',
            'coordinates': [
                [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                [[[2, 2], [3, 2], [3, 3], [2, 2]]],
            ]
        }
        verts = geojson_to_vertices(geom)
        assert len(verts) == 2

    def test_linestring(self):
        geom = {
            'type': 'LineString',
            'coordinates': [[0, 0], [1, 1], [2, 0]]
        }
        verts = geojson_to_vertices(geom)
        assert len(verts) == 1
        assert len(verts[0]) == 3

    def test_point(self):
        geom = {'type': 'Point', 'coordinates': [5, 10]}
        verts = geojson_to_vertices(geom)
        assert len(verts) == 1
        assert verts[0] == [(5, 10)]


# ── File loading ─────────────────────────────────────────────────────────────

class TestLoadGeojson:

    def test_feature_collection(self, tmp_path):
        fc = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {'name': 'Flood Zone A'},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                    }
                },
                {
                    'type': 'Feature',
                    'properties': {'name': 'Flood Zone B'},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[[2, 2], [3, 2], [3, 3], [2, 2]]]
                    }
                },
            ]
        }
        path = tmp_path / 'flood.geojson'
        path.write_text(json.dumps(fc))

        results = load_geojson(path)
        assert len(results) == 2
        verts_a, props_a = results[0]
        assert props_a['name'] == 'Flood Zone A'
        assert len(verts_a) == 5

    def test_single_feature(self, tmp_path):
        feat = {
            'type': 'Feature',
            'properties': {'id': 42},
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 0]]]
            }
        }
        path = tmp_path / 'zone.geojson'
        path.write_text(json.dumps(feat))

        results = load_geojson(path)
        assert len(results) == 1
        assert results[0][1]['id'] == 42

    def test_bare_geometry(self, tmp_path):
        geom = {
            'type': 'Polygon',
            'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 0]]]
        }
        path = tmp_path / 'bare.geojson'
        path.write_text(json.dumps(geom))

        results = load_geojson(path)
        assert len(results) == 1
        assert results[0][1] == {}   # no properties


# ── resolve_geodata ──────────────────────────────────────────────────────────

class TestResolveGeodata:

    def test_no_geojson_keys_unchanged(self):
        spec = {
            'zones': [{'vertices': [[0, 0], [1, 0], [1, 1]], 'fill': '#C00'}],
            'terrain_zones': [{'vertices': [[0, 0], [1, 0], [1, 1]], 'elevation': 100}],
        }
        resolve_geodata(spec)
        # Should be unchanged.
        assert len(spec['zones']) == 1
        assert spec['zones'][0]['fill'] == '#C00'

    def test_geojson_path_expands_zone(self, tmp_path):
        fc = {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'properties': {'name': 'Flood'},
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                }
            }]
        }
        path = tmp_path / 'flood.geojson'
        path.write_text(json.dumps(fc))

        spec = {
            'zones': [{'geojson': str(path), 'fill': '#C03030', 'fill_alpha': 0.2}],
        }
        resolve_geodata(spec)

        assert len(spec['zones']) == 1
        zone = spec['zones'][0]
        assert 'vertices' in zone
        assert zone['fill'] == '#C03030'
        assert zone['label'] == 'Flood'       # inherited from properties
        assert 'geojson' not in zone           # key removed

    def test_inline_geojson_geometry(self):
        spec = {
            'zones': [{
                'geojson_geometry': {
                    'type': 'Polygon',
                    'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 0]]]
                },
                'fill': '#00C',
            }],
        }
        resolve_geodata(spec)

        assert len(spec['zones']) == 1
        assert 'vertices' in spec['zones'][0]
        assert 'geojson_geometry' not in spec['zones'][0]

    def test_vertices_takes_precedence(self):
        """If vertices is already set, geojson is ignored."""
        spec = {
            'zones': [{
                'vertices': [[0, 0], [1, 0], [1, 1]],
                'geojson': '/nonexistent/path.geojson',
            }],
        }
        # Should not raise — geojson is skipped because vertices exists.
        resolve_geodata(spec)
        assert spec['zones'][0]['vertices'] == [[0, 0], [1, 0], [1, 1]]

    def test_multipolygon_expands_to_multiple(self, tmp_path):
        geom = {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'MultiPolygon',
                'coordinates': [
                    [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                    [[[2, 2], [3, 2], [3, 3], [2, 2]]],
                ]
            }
        }
        path = tmp_path / 'multi.geojson'
        path.write_text(json.dumps(geom))

        spec = {'zones': [{'geojson': str(path), 'fill': '#C00'}]}
        resolve_geodata(spec)
        assert len(spec['zones']) == 2
        assert all(z['fill'] == '#C00' for z in spec['zones'])

    def test_empty_spec_no_error(self):
        spec = {}
        resolve_geodata(spec)
        assert 'zones' not in spec
