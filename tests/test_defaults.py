"""Unit tests for newsmap.defaults — scale classification, scale bar, merge."""

import pytest
from newsmap.defaults import classify_scale, _pick_scale_km, for_extent, deep_merge


# ── classify_scale ───────────────────────────────────────────────────────────

class TestClassifyScale:

    def test_city_scale(self):
        # 0.3° span → city
        name, span = classify_scale([-118.5, -118.2, 34.0, 34.3])
        assert name == 'city'
        assert span == pytest.approx(0.3)

    def test_metro_scale(self):
        # 0.85° span → metro
        name, span = classify_scale([-118.80, -117.95, 33.90, 34.40])
        assert name == 'metro'
        assert span == pytest.approx(0.85)

    def test_region_scale(self):
        # 4.4° span → region
        name, span = classify_scale([-9.5, -5.5, 31.0, 35.4])
        assert name == 'region'
        assert span == pytest.approx(4.4)

    def test_country_scale(self):
        # 15° span → country
        name, span = classify_scale([0, 15, 0, 10])
        assert name == 'country'
        assert span == pytest.approx(15.0)

    def test_continent_scale(self):
        # 60° span → continent
        name, span = classify_scale([-30, 30, -10, 40])
        assert name == 'continent'
        assert span == pytest.approx(60.0)

    def test_world_scale(self):
        # 360° span → world
        name, span = classify_scale([-180, 180, -90, 90])
        assert name == 'world'
        assert span == pytest.approx(360.0)

    def test_exact_threshold_city(self):
        # Exactly 0.5° → city (inclusive)
        name, _ = classify_scale([0, 0.5, 0, 0.3])
        assert name == 'city'

    def test_just_over_city(self):
        # 0.51° → metro
        name, _ = classify_scale([0, 0.51, 0, 0.3])
        assert name == 'metro'

    def test_dominant_span_is_max(self):
        # lon_span=1.0, lat_span=0.5 → span picks the larger (1.0 → metro)
        name, span = classify_scale([0, 1.0, 0, 0.5])
        assert span == pytest.approx(1.0)
        assert name == 'metro'


# ── _pick_scale_km ───────────────────────────────────────────────────────────

class TestPickScaleKm:

    def test_city_scale_bar(self):
        # 0.3° → map ~33 km → target ~5 km → picks 5
        km = _pick_scale_km(0.3)
        assert km == 5

    def test_metro_scale_bar(self):
        # 0.85° → map ~94 km → target ~14 km → picks 10 or 20
        km = _pick_scale_km(0.85)
        assert km in (10, 20)

    def test_region_scale_bar(self):
        # 4.4° → map ~488 km → target ~73 km → picks 50 or 100
        km = _pick_scale_km(4.4)
        assert km in (50, 100)

    def test_country_scale_bar(self):
        # 15° → map ~1665 km → target ~250 km → picks 200 or 500
        km = _pick_scale_km(15.0)
        assert km in (200, 500)

    def test_world_scale_bar(self):
        # 180° → map ~19980 km → target ~2997 km → picks 2000 or 5000
        km = _pick_scale_km(180.0)
        assert km in (2000, 5000)

    def test_result_is_in_nice_list(self):
        nice = [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        for span in [0.1, 0.5, 1, 5, 10, 50, 100]:
            assert _pick_scale_km(span) in nice


# ── for_extent ───────────────────────────────────────────────────────────────

class TestForExtent:

    def test_returns_dict(self):
        result = for_extent([-10, -5, 30, 36])
        assert isinstance(result, dict)

    def test_scale_bar_inside_extent(self):
        extent = [-10, -5, 30, 36]
        result = for_extent(extent)
        sb = result['scale_bar']
        assert extent[0] <= sb['lon'] <= extent[1]
        assert extent[2] <= sb['lat'] <= extent[3]

    def test_mid_point(self):
        extent = [-10, -5, 30, 36]
        result = for_extent(extent)
        mid = result['_scale']['mid']
        assert mid[0] == pytest.approx(-7.5)
        assert mid[1] == pytest.approx(33.0)

    def test_offset_is_small_fraction_of_span(self):
        extent = [0, 10, 0, 10]
        result = for_extent(extent)
        offset = result['_scale']['offset']
        span = result['_scale']['span']
        assert offset == pytest.approx(span * 0.015)

    def test_ne_resolution_scales(self):
        # City gets finest, world gets coarsest
        city = for_extent([0, 0.3, 0, 0.3])
        world = for_extent([-180, 180, -90, 90])
        assert city['ne_resolution'] == '10m'
        assert world['ne_resolution'] == '110m'

    def test_hillshade_resolution_scales(self):
        city = for_extent([0, 0.3, 0, 0.3])
        world = for_extent([-180, 180, -90, 90])
        assert city['hillshade_resolution'] > world['hillshade_resolution']


# ── deep_merge ───────────────────────────────────────────────────────────────

class TestDeepMerge:

    def test_simple_override(self):
        base = {'a': 1, 'b': 2}
        over = {'b': 3}
        assert deep_merge(base, over) == {'a': 1, 'b': 3}

    def test_new_key(self):
        result = deep_merge({'a': 1}, {'b': 2})
        assert result == {'a': 1, 'b': 2}

    def test_nested_merge(self):
        base = {'colors': {'ocean': 'blue', 'land': 'green'}}
        over = {'colors': {'ocean': 'red'}}
        result = deep_merge(base, over)
        assert result['colors']['ocean'] == 'red'
        assert result['colors']['land'] == 'green'

    def test_list_replaces_not_merges(self):
        base = {'items': [1, 2, 3]}
        over = {'items': [4, 5]}
        assert deep_merge(base, over)['items'] == [4, 5]

    def test_base_unchanged(self):
        base = {'a': {'b': 1}}
        over = {'a': {'b': 2}}
        deep_merge(base, over)
        assert base['a']['b'] == 1  # Original untouched

    def test_override_unchanged(self):
        base = {'a': 1}
        over = {'a': {'nested': 2}}
        deep_merge(base, over)
        assert over == {'a': {'nested': 2}}

    def test_empty_override(self):
        base = {'a': 1, 'b': 2}
        assert deep_merge(base, {}) == {'a': 1, 'b': 2}

    def test_empty_base(self):
        assert deep_merge({}, {'a': 1}) == {'a': 1}

    def test_deep_nesting(self):
        base = {'a': {'b': {'c': 1, 'd': 2}}}
        over = {'a': {'b': {'c': 99}}}
        result = deep_merge(base, over)
        assert result['a']['b']['c'] == 99
        assert result['a']['b']['d'] == 2
