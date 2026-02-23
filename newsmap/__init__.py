"""newsmap — small composable tools for analytical news maps."""
from .render import render
from .defaults import for_extent, classify_scale
from .validate import check
from .data import load_geojson, resolve_geodata
