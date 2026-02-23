"""Analytical overlay primitives.

Zones, markers, arrows, lines, callouts — the data layers that sit
on top of the physical geography.
Signature convention: fn(ax, spec, proj) → None.
"""

import numpy as np
from shapely.geometry import Polygon

from . import text


def zones(ax, spec, proj):
    """Draw analytical zone polygons (flood extent, etc.)."""
    for z in spec.get('zones', []):
        verts = z['vertices']
        poly = Polygon(verts)
        # Fill.
        ax.add_geometries(
            [poly], proj,
            facecolor=z.get('fill', '#C03030'),
            alpha=z.get('fill_alpha', 0.12),
            edgecolor='none', zorder=7)
        # Dashed outline.
        xs = [v[0] for v in verts] + [verts[0][0]]
        ys = [v[1] for v in verts] + [verts[0][1]]
        ax.plot(xs, ys,
                color=z.get('edge', z.get('fill', '#C03030')),
                linewidth=z.get('edge_width', 1.8),
                linestyle=z.get('edge_style', '--'),
                alpha=z.get('edge_alpha', 0.6),
                transform=proj, zorder=7)
        # Label.
        lp = z.get('label_pos')
        if lp and z.get('label'):
            ax.text(lp[0], lp[1], z['label'],
                    fontsize=z.get('label_size', 7),
                    color=z.get('edge', '#C03030'),
                    ha='center', va='center', transform=proj, zorder=15,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=z.get('label_border', z.get('edge', '#B03030')),
                              alpha=0.9, linewidth=1.0),
                    **text.font('label'))


def scatter(ax, spec, proj):
    """Draw scatter-mark fields (e.g. farmland X-hatching).

    Points are filtered to land areas so that marks never appear
    in water.  Over-generates by 2x and keeps the first N on-land
    points to maintain the requested density.
    """
    if not spec.get('scatter_marks'):
        return

    from . import geo as _geo
    from shapely.geometry import Point

    land = _geo.land_geometry(spec)

    for s in spec.get('scatter_marks', []):
        np.random.seed(s.get('seed', 42))
        bounds = s['bounds']  # (lon_min, lon_max, lat_min, lat_max)
        n = s.get('n', 20)

        # Over-generate to compensate for points filtered out of water.
        pool = n * 3
        all_lons = np.random.uniform(bounds[0], bounds[1], pool)
        all_lats = np.random.uniform(bounds[2], bounds[3], pool)

        # Keep only points on land.
        on_land = [i for i in range(pool)
                   if land.contains(Point(all_lons[i], all_lats[i]))]
        keep = on_land[:n]

        if not keep:
            continue

        lons = all_lons[keep]
        lats = all_lats[keep]

        ax.scatter(lons, lats,
                   marker=s.get('marker', 'x'),
                   s=s.get('size', 25),
                   c=s.get('color', '#7A5230'),
                   alpha=s.get('alpha', 0.35),
                   linewidths=s.get('linewidth', 1.5),
                   transform=proj, zorder=8)


def markers(ax, spec, proj):
    """Draw point markers with name labels and annotations.

    When markers omit 'name_offset', label positions are resolved
    automatically to minimize overlap.  Set 'auto_labels': True
    in the spec to re-optimize even explicit offsets.
    """
    from . import labels as _labels

    marker_list = spec.get('markers', [])
    if not marker_list:
        return

    # Resolve label positions (collision avoidance).
    placements = _labels.resolve(marker_list, spec)

    for m, (dx, dy, ha) in zip(marker_list, placements):
        lon, lat = m['lon'], m['lat']
        # Marker dot.
        ax.plot(lon, lat,
                marker=m.get('shape', 'o'),
                markersize=m.get('size', 7),
                color=m['color'],
                markeredgecolor=m.get('edge_color', 'white'),
                markeredgewidth=m.get('edge_width', 0.7),
                transform=proj, zorder=13)
        # Name label (position from collision resolver).
        ax.text(lon + dx, lat + dy, m['name'],
                fontsize=m.get('name_size', 6.5),
                color=m.get('name_color', '#1a1a1a'),
                ha=ha,
                va=m.get('name_va', 'baseline'),
                path_effects=text.halo(3.2),
                transform=proj, zorder=15,
                **text.font('label'))
        # Annotation (optional).
        ann = m.get('annotation')
        if ann:
            ad = m.get('ann_offset', (0.06, -0.06))
            ax.text(lon + ad[0], lat + ad[1], ann,
                    fontsize=m.get('ann_size', 4.8),
                    color=m.get('ann_color', m['color']),
                    ha=m.get('ann_ha', 'left'),
                    va=m.get('ann_va', 'top'),
                    path_effects=text.halo(2.5),
                    transform=proj, zorder=15,
                    **text.font('body'))


def arrow_groups(ax, spec, proj):
    """Draw grouped arrows (displacement flows, dam releases, etc.)."""
    for g in spec.get('arrow_groups', []):
        color = g.get('color', '#D97520')
        for a in g['arrows']:
            ax.annotate('',
                        xy=a['to'], xytext=a['from'],
                        arrowprops=dict(
                            arrowstyle='->',
                            color=color,
                            lw=g.get('width', 2.5),
                            alpha=g.get('alpha', 0.55),
                            connectionstyle=f"arc3,rad={a.get('arc', 0.0)}"),
                        transform=proj, zorder=10)
        # Group label.
        lp = g.get('label_pos')
        if lp and g.get('label'):
            label_color = g.get('label_color', color)
            if g.get('label_box', True):
                ax.text(lp[0], lp[1], g['label'],
                        fontsize=g.get('label_size', 5.5),
                        color=label_color,
                        ha='center', va='center', transform=proj, zorder=15,
                        bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                                  edgecolor=label_color, alpha=0.9, linewidth=0.8),
                        **text.font('label'))
            else:
                ax.text(lp[0], lp[1], g['label'],
                        fontsize=g.get('label_size', 4.5),
                        color=label_color,
                        ha='center', va='center',
                        path_effects=text.halo(2.5),
                        transform=proj, zorder=15,
                        **text.font('body'))


def lines(ax, spec, proj):
    """Draw styled lines (supply chain disruption, routes, etc.)."""
    for ln in spec.get('lines', []):
        coords = ln['coords']
        ax.plot([c[0] for c in coords], [c[1] for c in coords],
                color=ln.get('color', '#7B3FA0'),
                linewidth=ln.get('width', 2.0),
                linestyle=ln.get('style', '--'),
                alpha=ln.get('alpha', 0.5),
                transform=proj, zorder=9)
        # End marker (optional).
        em = ln.get('end_marker')
        if em:
            end = coords[-1]
            ax.plot(end[0], end[1],
                    marker=em.get('shape', 'X'),
                    markersize=em.get('size', 14),
                    color=em.get('color', '#C03030'),
                    markeredgecolor=em.get('edge_color', 'white'),
                    markeredgewidth=em.get('edge_width', 1.0),
                    transform=proj, zorder=14)
        # Label (optional).
        lp = ln.get('label_pos')
        if lp and ln.get('label'):
            lc = ln.get('label_color', ln.get('color', '#7B3FA0'))
            ax.text(lp[0], lp[1], ln['label'],
                    fontsize=ln.get('label_size', 5),
                    color=lc, ha='center', va='center',
                    transform=proj, zorder=15,
                    bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                              edgecolor=lc, alpha=0.9, linewidth=0.8),
                    **text.font('label'))


def callouts(ax, spec, proj):
    """Draw text callouts over map areas (region labels, etc.)."""
    for c in spec.get('callouts', []):
        ax.text(c['lon'], c['lat'], c['text'],
                fontsize=c.get('size', 9),
                color=c.get('color', '#C03030'),
                ha=c.get('ha', 'center'),
                path_effects=text.halo(3.2),
                transform=proj, zorder=15,
                **text.font('label'))
        sub = c.get('subtitle')
        if sub:
            ax.text(c['lon'], c['lat'] - c.get('subtitle_offset', 0.17),
                    sub,
                    fontsize=c.get('subtitle_size', 5),
                    color=c.get('subtitle_color', '#444444'),
                    ha=c.get('ha', 'center'),
                    path_effects=text.halo(2.5),
                    transform=proj, zorder=15,
                    **text.font('body'))
