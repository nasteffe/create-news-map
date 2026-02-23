"""Smoke tests: every map spec renders without error.

These are the highest-value tests — they catch any breaking change
in the toolkit that silently breaks a map. Each test loads a real
spec and runs the full render pipeline. Output files are written
to a temp directory to avoid polluting the repo.
"""

import os
import importlib
import tempfile
import pytest


def _load_spec(module_path):
    """Import a map module and return its MAP dict."""
    mod = importlib.import_module(module_path)
    return mod.MAP


def _render_to_tmpdir(spec, tmpdir):
    """Render a spec with output files directed to tmpdir."""
    import copy
    spec = copy.deepcopy(spec)

    # Redirect output to temp directory.
    basename = spec.get('output', {}).get('basename', 'map')
    spec.setdefault('output', {})
    spec['output']['basename'] = os.path.join(tmpdir, basename)

    from newsmap.render import render
    render(spec)
    return spec['output']['basename']


# ── Smoke tests ──────────────────────────────────────────────────────────────

class TestSmokeRender:

    def test_morocco_renders(self, tmp_path):
        spec = _load_spec('maps.morocco_flood_2026')
        basename = _render_to_tmpdir(spec, str(tmp_path))
        # Check at least one output file exists and is non-empty.
        jpg = f"{basename}.jpg"
        assert os.path.exists(jpg), f"Expected {jpg}"
        assert os.path.getsize(jpg) > 10_000, "JPG suspiciously small"

    def test_gaza_renders(self, tmp_path):
        spec = _load_spec('maps.gaza_ceasefire_2026')
        basename = _render_to_tmpdir(spec, str(tmp_path))
        jpg = f"{basename}.jpg"
        assert os.path.exists(jpg)
        assert os.path.getsize(jpg) > 10_000

    def test_la_renders(self, tmp_path):
        spec = _load_spec('maps.la_firestorm_2025')
        basename = _render_to_tmpdir(spec, str(tmp_path))
        jpg = f"{basename}.jpg"
        assert os.path.exists(jpg)
        assert os.path.getsize(jpg) > 10_000

    def test_pdf_output(self, tmp_path):
        """At least one map spec requests PDF — verify it's produced."""
        spec = _load_spec('maps.morocco_flood_2026')
        basename = _render_to_tmpdir(spec, str(tmp_path))
        pdf = f"{basename}.pdf"
        assert os.path.exists(pdf), f"Expected {pdf}"
        assert os.path.getsize(pdf) > 10_000, "PDF suspiciously small"


# ── Regression guards ────────────────────────────────────────────────────────

class TestRegressionGuards:

    def test_minimal_spec_renders(self, tmp_path):
        """The absolute minimum spec should produce a valid map."""
        spec = {
            'extent': [-10, -5, 30, 36],
            'meta': {'title': 'TEST'},
            'output': {
                'basename': os.path.join(str(tmp_path), 'test_minimal'),
                'formats': [{'ext': 'jpg', 'dpi': 72}],
            },
        }
        from newsmap.render import render
        render(spec)
        jpg = os.path.join(str(tmp_path), 'test_minimal.jpg')
        assert os.path.exists(jpg)
        assert os.path.getsize(jpg) > 1_000

    def test_empty_overlays_dont_crash(self, tmp_path):
        """A spec with empty marker/zone/panel lists shouldn't crash."""
        spec = {
            'extent': [0, 5, 0, 5],
            'markers': [],
            'zones': [],
            'panels': [],
            'terrain_zones': [],
            'arrow_groups': [],
            'lines': [],
            'callouts': [],
            'scatter_marks': [],
            'output': {
                'basename': os.path.join(str(tmp_path), 'test_empty'),
                'formats': [{'ext': 'jpg', 'dpi': 72}],
            },
        }
        from newsmap.render import render
        render(spec)
        jpg = os.path.join(str(tmp_path), 'test_empty.jpg')
        assert os.path.exists(jpg)
