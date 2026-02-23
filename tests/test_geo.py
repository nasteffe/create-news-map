"""Unit tests for newsmap.geo — hillshade smoothing and land geometry."""

import numpy as np
import pytest
from newsmap.geo import _smooth, land_geometry, ocean_mask


class TestSmooth:

    def test_preserves_shape(self):
        grid = np.random.rand(20, 20)
        result = _smooth(grid, passes=5)
        assert result.shape == (20, 20)

    def test_uniform_grid_unchanged(self):
        """A grid of constant value should stay constant after smoothing."""
        grid = np.full((10, 10), 42.0)
        result = _smooth(grid, passes=10)
        np.testing.assert_allclose(result, 42.0)

    def test_reduces_extremes(self):
        """Smoothing should reduce the max and raise the min."""
        grid = np.zeros((15, 15))
        grid[7, 7] = 100.0
        result = _smooth(grid, passes=5)
        assert result.max() < 100.0
        assert result.min() >= 0.0

    def test_more_passes_smoother(self):
        """More passes → smaller difference between max and min."""
        grid = np.zeros((15, 15))
        grid[7, 7] = 100.0
        r5 = _smooth(grid, passes=5)
        r20 = _smooth(grid, passes=20)
        assert (r20.max() - r20.min()) < (r5.max() - r5.min())

    def test_zero_passes_identity(self):
        grid = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = _smooth(grid, passes=0)
        np.testing.assert_array_equal(result, grid)

    def test_conserves_total_energy(self):
        """Smoothing should roughly preserve the total sum (mass conservation)."""
        grid = np.zeros((20, 20))
        grid[10, 10] = 100.0
        result = _smooth(grid, passes=5)
        # Not exact due to edge padding, but should be close.
        np.testing.assert_allclose(result.sum(), grid.sum(), rtol=0.15)


# ── Land geometry ────────────────────────────────────────────────────────────

class TestLandGeometry:
    """Test the Natural Earth land geometry loader."""

    def test_returns_prepared_geometry(self):
        from shapely.geometry import Point
        spec = {'extent': [-7.6, -3.6, 32.6, 37.0], 'ne_resolution': '110m'}
        geom = land_geometry(spec)
        # Should be a prepared geometry with a .contains method.
        assert hasattr(geom, 'contains')
        # Inland Morocco point should be on land.
        assert geom.contains(Point(-5.0, 34.0))

    def test_ocean_point_excluded(self):
        from shapely.geometry import Point
        spec = {'extent': [-7.6, -3.6, 32.6, 37.0], 'ne_resolution': '110m'}
        geom = land_geometry(spec)
        # Point well into the Atlantic should not be on land.
        assert not geom.contains(Point(-7.5, 34.0))

    def test_caching(self):
        spec = {'extent': [-7.6, -3.6, 32.6, 37.0], 'ne_resolution': '110m'}
        g1 = land_geometry(spec)
        g2 = land_geometry(spec)
        assert g1 is g2

    def test_gaza_coast(self):
        """Mediterranean off Gaza coast should be water."""
        from shapely.geometry import Point
        spec = {'extent': [34.0, 34.75, 31.08, 31.72], 'ne_resolution': '110m'}
        geom = land_geometry(spec)
        # Point in the Mediterranean, west of Gaza.
        assert not geom.contains(Point(34.05, 31.5))

    def test_la_ocean(self):
        """Pacific Ocean off LA coast should be water."""
        from shapely.geometry import Point
        spec = {'extent': [-118.80, -117.95, 33.90, 34.40], 'ne_resolution': '110m'}
        geom = land_geometry(spec)
        # Point in the Pacific.
        assert not geom.contains(Point(-118.75, 33.95))
