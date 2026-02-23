"""Tests for newsmap.validate — spec validation catches errors early."""

import pytest
from newsmap.validate import check


def _minimal_spec(**overrides):
    """A valid minimal spec. Override any key to test breakage."""
    spec = {'extent': [-10, -5, 30, 36]}
    spec.update(overrides)
    return spec


# ── Valid specs pass ─────────────────────────────────────────────────────────

class TestValidSpecs:

    def test_minimal_spec_passes(self):
        check(_minimal_spec())  # No exception

    def test_with_projection_string(self):
        check(_minimal_spec(projection='PlateCarree'))

    def test_with_projection_dict(self):
        check(_minimal_spec(projection={'name': 'Robinson', 'central_longitude': -5}))

    def test_with_valid_panels(self):
        check(_minimal_spec(panels=[
            {'type': 'bar_chart', 'rect': [0.6, 0.7, 0.35, 0.2]},
            {'type': 'metrics', 'rect': [0.6, 0.4, 0.35, 0.3]},
            {'type': 'timeline', 'rect': [0.6, 0.1, 0.35, 0.25]},
        ]))

    def test_with_valid_markers(self):
        check(_minimal_spec(markers=[
            {'lon': -7.5, 'lat': 33.0, 'name': 'Test', 'color': '#FF0000'},
        ]))

    def test_with_terrain_zones(self):
        check(_minimal_spec(terrain_zones=[
            {'vertices': [(0, 0), (1, 0), (1, 1)], 'elevation': 500},
        ]))

    def test_with_output_formats(self):
        check(_minimal_spec(output={
            'formats': [{'ext': 'jpg', 'dpi': 200}, {'ext': 'pdf', 'dpi': 300}],
        }))


# ── Missing/bad extent ──────────────────────────────────────────────────────

class TestExtentValidation:

    def test_missing_extent(self):
        with pytest.raises(ValueError, match="Missing required key 'extent'"):
            check({})

    def test_extent_wrong_length(self):
        with pytest.raises(ValueError, match="must be"):
            check({'extent': [1, 2, 3]})

    def test_extent_not_list(self):
        with pytest.raises(ValueError, match="must be"):
            check({'extent': 'bad'})

    def test_lon_min_ge_lon_max(self):
        with pytest.raises(ValueError, match="lon_min.*>=.*lon_max"):
            check({'extent': [10, -10, 30, 36]})

    def test_lat_min_ge_lat_max(self):
        with pytest.raises(ValueError, match="lat_min.*>=.*lat_max"):
            check({'extent': [-10, -5, 36, 30]})

    def test_lon_out_of_range(self):
        with pytest.raises(ValueError, match="longitudes out of range"):
            check({'extent': [-200, -5, 30, 36]})

    def test_lat_out_of_range(self):
        with pytest.raises(ValueError, match="latitudes out of range"):
            check({'extent': [-10, -5, 30, 100]})

    def test_equal_lon(self):
        with pytest.raises(ValueError, match="lon_min.*>=.*lon_max"):
            check({'extent': [5, 5, 30, 36]})


# ── Projection ───────────────────────────────────────────────────────────────

class TestProjectionValidation:

    def test_unknown_projection_string(self):
        with pytest.raises(ValueError, match="Unknown projection 'BadProj'"):
            check(_minimal_spec(projection='BadProj'))

    def test_unknown_projection_dict(self):
        with pytest.raises(ValueError, match="Unknown projection name 'BadProj'"):
            check(_minimal_spec(projection={'name': 'BadProj'}))


# ── Panels ───────────────────────────────────────────────────────────────────

class TestPanelValidation:

    def test_unknown_panel_type(self):
        with pytest.raises(ValueError, match="unknown type 'sparkline'"):
            check(_minimal_spec(panels=[{'type': 'sparkline', 'rect': [0, 0, 1, 1]}]))

    def test_missing_rect(self):
        with pytest.raises(ValueError, match="missing 'rect'"):
            check(_minimal_spec(panels=[{'type': 'bar_chart'}]))


# ── Markers ──────────────────────────────────────────────────────────────────

class TestMarkerValidation:

    def test_missing_required_keys(self):
        with pytest.raises(ValueError, match="missing required key 'color'"):
            check(_minimal_spec(markers=[{'lon': 0, 'lat': 0, 'name': 'X'}]))

    def test_missing_lon(self):
        with pytest.raises(ValueError, match="missing required key 'lon'"):
            check(_minimal_spec(markers=[{'lat': 0, 'name': 'X', 'color': 'red'}]))


# ── Zones ────────────────────────────────────────────────────────────────────

class TestZoneValidation:

    def test_missing_vertices_terrain(self):
        with pytest.raises(ValueError, match="terrain_zones.*missing 'vertices'"):
            check(_minimal_spec(terrain_zones=[{'elevation': 500}]))

    def test_too_few_vertices_terrain(self):
        with pytest.raises(ValueError, match="need >= 3 vertices"):
            check(_minimal_spec(terrain_zones=[{'vertices': [(0, 0), (1, 1)]}]))

    def test_missing_vertices_zone(self):
        with pytest.raises(ValueError, match="zones.*missing 'vertices'"):
            check(_minimal_spec(zones=[{'fill': '#FF0000'}]))

    def test_too_few_vertices_zone(self):
        with pytest.raises(ValueError, match="need >= 3 vertices"):
            check(_minimal_spec(zones=[{'vertices': [(0, 0)]}]))


# ── Output ───────────────────────────────────────────────────────────────────

class TestOutputValidation:

    def test_missing_ext(self):
        with pytest.raises(ValueError, match="missing 'ext'"):
            check(_minimal_spec(output={'formats': [{'dpi': 200}]}))

    def test_missing_dpi(self):
        with pytest.raises(ValueError, match="missing 'dpi'"):
            check(_minimal_spec(output={'formats': [{'ext': 'jpg'}]}))


# ── Multiple errors ──────────────────────────────────────────────────────────

class TestMultipleErrors:

    def test_collects_all_errors(self):
        """Validator should report ALL errors, not just the first."""
        with pytest.raises(ValueError) as exc_info:
            check({
                'extent': [10, -10, 36, 30],  # Both lon & lat reversed
                'markers': [{'lon': 0}],       # Missing lat, name, color
            })
        msg = str(exc_info.value)
        assert 'lon_min' in msg
        assert 'lat_min' in msg
        assert "missing required key" in msg

    def test_error_count_in_message(self):
        with pytest.raises(ValueError, match=r"\d+ errors?\)"):
            check({'extent': [10, -10, 36, 30]})
