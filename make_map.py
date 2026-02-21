#!/usr/bin/env python3
"""CLI entry point: render map specs.

Usage:
    python make_map.py                         # render all maps in maps/
    python make_map.py maps.morocco_flood_2026  # render one map
"""

import sys
import importlib
import newsmap


def main():
    targets = sys.argv[1:] or _discover()
    for module_path in targets:
        mod = importlib.import_module(module_path)
        spec = getattr(mod, 'MAP')
        title = spec.get('meta', {}).get('title', module_path)
        print(f"\n> {title}")
        newsmap.render(spec)


def _discover():
    """Find all map modules under maps/."""
    from pathlib import Path
    found = []
    for p in Path('maps').glob('*.py'):
        if p.name.startswith('_'):
            continue
        found.append(f'maps.{p.stem}')
    return sorted(found)


if __name__ == '__main__':
    main()
