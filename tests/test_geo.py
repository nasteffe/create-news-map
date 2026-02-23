"""Unit tests for newsmap.geo — hillshade smoothing."""

import numpy as np
import pytest
from newsmap.geo import _smooth


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
