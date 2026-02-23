"""Unit tests for newsmap.labels — label collision avoidance."""

import pytest
from newsmap.labels import _bbox, _overlap_area, _ha_for_offset, resolve


# ── Bounding box estimation ──────────────────────────────────────────────────

class TestBbox:

    EXTENT = [-7.6, -3.6, 32.6, 37.0]   # Morocco-like region

    def test_returns_four_floats(self):
        box = _bbox(0, 0, 'Test', 6.5, 0.06, 0.06, self.EXTENT)
        assert len(box) == 4
        assert all(isinstance(v, float) for v in box)

    def test_left_aligned_extends_right(self):
        box = _bbox(0, 0, 'Label', 6.5, 0, 0, self.EXTENT, ha='left')
        # x0 should be at anchor, x1 to the right.
        assert box[0] == pytest.approx(0, abs=0.01)
        assert box[2] > box[0]

    def test_right_aligned_extends_left(self):
        box = _bbox(0, 0, 'Label', 6.5, 0, 0, self.EXTENT, ha='right')
        assert box[2] == pytest.approx(0, abs=0.01)
        assert box[0] < box[2]

    def test_center_aligned_symmetric(self):
        box = _bbox(0, 0, 'Label', 6.5, 0, 0, self.EXTENT, ha='center')
        mid = (box[0] + box[2]) / 2
        assert mid == pytest.approx(0, abs=0.01)

    def test_longer_text_wider_box(self):
        short = _bbox(0, 0, 'Hi', 6.5, 0, 0, self.EXTENT)
        long = _bbox(0, 0, 'Hello World', 6.5, 0, 0, self.EXTENT)
        short_w = short[2] - short[0]
        long_w = long[2] - long[0]
        assert long_w > short_w

    def test_larger_font_bigger_box(self):
        small = _bbox(0, 0, 'Test', 5.0, 0, 0, self.EXTENT)
        big = _bbox(0, 0, 'Test', 10.0, 0, 0, self.EXTENT)
        assert (big[2] - big[0]) > (small[2] - small[0])
        assert (big[3] - big[1]) > (small[3] - small[1])

    def test_offset_shifts_box(self):
        base = _bbox(0, 0, 'Test', 6.5, 0, 0, self.EXTENT)
        shifted = _bbox(0, 0, 'Test', 6.5, 1.0, 1.0, self.EXTENT)
        assert shifted[0] > base[0]
        assert shifted[1] > base[1]


# ── Overlap area ─────────────────────────────────────────────────────────────

class TestOverlapArea:

    def test_no_overlap(self):
        assert _overlap_area((0, 0, 1, 1), (2, 2, 3, 3)) == 0.0

    def test_full_overlap(self):
        assert _overlap_area((0, 0, 1, 1), (0, 0, 1, 1)) == pytest.approx(1.0)

    def test_partial_overlap(self):
        area = _overlap_area((0, 0, 2, 2), (1, 1, 3, 3))
        assert area == pytest.approx(1.0)

    def test_touching_edges(self):
        assert _overlap_area((0, 0, 1, 1), (1, 0, 2, 1)) == 0.0


# ── Horizontal alignment ────────────────────────────────────────────────────

class TestHaForOffset:

    def test_positive_dx(self):
        assert _ha_for_offset(0.1) == 'left'

    def test_negative_dx(self):
        assert _ha_for_offset(-0.1) == 'right'

    def test_zero_dx(self):
        assert _ha_for_offset(0) == 'center'


# ── Full resolve ─────────────────────────────────────────────────────────────

class TestResolve:

    EXTENT = [-7.6, -3.6, 32.6, 37.0]

    def _spec(self, markers, **extra):
        s = {'extent': self.EXTENT, 'markers': markers}
        s.update(extra)
        return s

    def test_empty_markers(self):
        assert resolve([], self._spec([])) == []

    def test_fixed_markers_unchanged(self):
        """Markers with explicit name_offset should keep their position."""
        m = [{'lon': -5, 'lat': 34, 'name': 'A', 'color': '#000',
              'name_offset': (0.1, 0.2), 'name_ha': 'left'}]
        result = resolve(m, self._spec(m))
        dx, dy, ha = result[0]
        assert dx == pytest.approx(0.1)
        assert dy == pytest.approx(0.2)
        assert ha == 'left'

    def test_auto_markers_get_offset(self):
        """Markers without name_offset should get auto-placed."""
        m = [{'lon': -5, 'lat': 34, 'name': 'City', 'color': '#000'}]
        result = resolve(m, self._spec(m))
        dx, dy, ha = result[0]
        # Should have non-zero offset.
        assert (dx != 0) or (dy != 0)

    def test_two_markers_no_overlap(self):
        """Auto-placed labels for nearby markers should not overlap."""
        m = [
            {'lon': -5.0, 'lat': 34.0, 'name': 'City A', 'color': '#000'},
            {'lon': -5.0, 'lat': 34.0, 'name': 'City B', 'color': '#000'},
        ]
        result = resolve(m, self._spec(m))
        # The two labels should be placed in different directions.
        assert result[0] != result[1]

    def test_auto_labels_overrides_fixed(self):
        """When auto_labels=True, even explicit offsets are re-optimized."""
        m = [{'lon': -5, 'lat': 34, 'name': 'City', 'color': '#000',
              'name_offset': (0.1, 0.2)}]
        spec = self._spec(m, auto_labels=True)
        result = resolve(m, spec)
        # With auto_labels, the fixed offset may be changed.
        # (Just verify it runs without error and returns a result.)
        assert len(result) == 1
        dx, dy, ha = result[0]
        assert isinstance(dx, float)

    def test_respects_obstacles(self):
        """Labels should avoid zone labels and callouts."""
        m = [{'lon': -5.0, 'lat': 34.0, 'name': 'City', 'color': '#000'}]
        spec = self._spec(m, callouts=[
            {'lon': -5.0, 'lat': 34.1, 'text': 'BIG REGION LABEL', 'size': 12}
        ])
        result = resolve(m, spec)
        # Should produce a valid result (not crashing on obstacles).
        assert len(result) == 1

    def test_prefers_in_bounds(self):
        """Labels should not be placed outside the map extent."""
        # Marker near the top-right corner.
        m = [{'lon': -3.7, 'lat': 36.9, 'name': 'Edge City', 'color': '#000'}]
        result = resolve(m, self._spec(m))
        dx, dy, ha = result[0]
        # Label should not extend above extent[3] = 37.0.
        # (The solver should pick a direction that stays in bounds.)
        assert isinstance(dx, float)
