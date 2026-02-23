"""Figure chrome: title block, scale bar, bottom bar (legend + sources).

These operate on the figure or map axes to add non-geographic elements.
"""

import numpy as np
from . import text


def title_block(fig, spec):
    """Draw title, subtitle, tagline in the top-left."""
    meta = spec.get('meta', {})
    fig.text(0.02, 0.97, meta.get('title', ''),
             fontsize=meta.get('title_size', 22),
             color='#1a1a1a', va='top', **text.font('title'))
    sub = meta.get('subtitle')
    if sub:
        fig.text(0.02, 0.935, sub, fontsize=11, color='#444444',
                 va='top', **text.font('body'))
    tag = meta.get('tagline')
    if tag:
        fig.text(0.02, 0.915, tag, fontsize=8, color='#666666',
                 va='top', **text.font('body'))


def scale_bar(ax, spec, proj):
    """Draw a distance scale bar on the map.

    Tick height adapts to the map extent so the bar looks proportional
    at any scale, from city blocks to world maps.
    """
    sb = spec.get('scale_bar')
    if not sb:
        return
    lon, lat = sb['lon'], sb['lat']
    km = sb.get('km', 100)
    ref_lat = sb.get('reference_lat', (spec['extent'][2] + spec['extent'][3]) / 2)
    deg_per_km = 1.0 / (111.32 * np.cos(np.radians(ref_lat)))
    length = km * deg_per_km

    # Tick height: use spec value, or scale from extent.
    lat_span = spec['extent'][3] - spec['extent'][2]
    tick = sb.get('tick', lat_span * 0.008)

    # Format label: sub-km distances show metres.
    if km >= 1:
        label = f'{km:g} km'
    else:
        label = f'{km * 1000:g} m'

    ax.plot([lon, lon + length], [lat, lat],
            color='#333333', linewidth=2.5, transform=proj, zorder=15,
            solid_capstyle='butt')
    for x in [lon, lon + length]:
        ax.plot([x, x], [lat - tick, lat + tick],
                color='#333333', linewidth=1.5, transform=proj, zorder=15)
    ax.text(lon + length / 2, lat + tick * 2, label,
            fontsize=6.5, ha='center', color='#333333',
            path_effects=text.halo(2.5),
            transform=proj, zorder=15, **text.font('label'))


def bottom_bar(fig, spec):
    """Full-width bottom bar: metabolic flows, legend, sources."""
    bb = spec.get('bottom_bar')
    if not bb:
        return

    ax = fig.add_axes(bb.get('rect', [0.0, 0.0, 1.0, 0.125]))
    ax.set_facecolor(bb.get('background', '#F4F3F0'))
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot([0, 1], [1, 1], color='#CCCCCC', linewidth=0.8, zorder=5)

    # Flow rows.
    y = 0.90
    for f in bb.get('flows', []):
        ax.text(0.015, y, f['category'], fontsize=6.5,
                color=f.get('color', '#333333'), va='top',
                **text.font('label'))
        ax.text(0.065, y, f['text'], fontsize=5.5, color='#444444',
                va='top', **text.font('body'))
        y -= bb.get('flow_spacing', 0.185)

    # Legend.
    legend = bb.get('legend', {})
    _draw_legend(ax, legend)

    # Source line.
    sources = bb.get('sources', '')
    if sources:
        ax.text(0.98, 0.06, sources, fontsize=5, color='#999999',
                va='bottom', ha='right', **text.font('body'))


def annotation_text(fig, spec):
    """Draw any free-floating figure-level text annotations."""
    for a in spec.get('annotations', []):
        fig.text(a['x'], a['y'], a['text'],
                 fontsize=a.get('size', 5.5),
                 color=a.get('color', '#666666'),
                 ha=a.get('ha', 'center'), va=a.get('va', 'top'),
                 **text.font('body'))


# ── Legend drawing ───────────────────────────────────────────────────────────

def _draw_legend(ax, legend):
    """Draw marker + line legend in the bottom bar.

    If marker_x / line_x / spacing are omitted, positions are
    auto-computed from the item counts so the legend fills the
    available space without manual tuning.
    """
    marker_items = legend.get('markers', [])
    line_items = legend.get('lines', [])

    # Auto-compute layout when positions aren't explicit.
    n_markers = len(marker_items)
    n_lines = len(line_items)
    n_max = max(n_markers, n_lines, 1)
    y0 = legend.get('y', 0.88)
    spacing = legend.get('spacing', min(0.155, 0.75 / max(n_max, 1)))
    mx = legend.get('marker_x', 0.72)
    lx = legend.get('line_x', mx + 0.12 if n_markers else mx)

    if marker_items or line_items:
        ax.text(mx, y0 + 0.05, 'LEGEND', fontsize=7,
                color='#333333', va='top', **text.font('label'))

    for i, m in enumerate(marker_items):
        ypos = y0 - i * spacing
        ax.plot(mx + 0.01, ypos,
                marker=m['shape'], markersize=6, color=m['color'],
                markeredgecolor='white', markeredgewidth=0.5,
                transform=ax.transAxes, clip_on=False)
        ax.text(mx + 0.035, ypos, m['label'], fontsize=5.5,
                color='#444444', va='center',
                transform=ax.transAxes, **text.font('body'))

    for i, ln in enumerate(line_items):
        ypos = y0 - i * spacing
        ax.plot([lx, lx + 0.025], [ypos, ypos],
                linestyle=ln.get('style', '-'), color=ln['color'],
                linewidth=ln.get('width', 1.5), alpha=0.7,
                transform=ax.transAxes, clip_on=False)
        ax.text(lx + 0.035, ypos, ln['label'], fontsize=5.5,
                color='#444444', va='center',
                transform=ax.transAxes, **text.font('body'))
