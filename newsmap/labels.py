"""Label collision avoidance for marker name labels.

Estimates text bounding boxes in data coordinates and nudges labels
to reduce overlap. Markers with explicit name_offset are fixed unless
the spec opts into full auto-placement with 'auto_labels': True.
"""

import numpy as np

# Average character width as fraction of font height (proportional font).
_CHAR_WIDTH_RATIO = 0.55

# Default map layout (matches defaults.py).
_MAP_W_IN = 0.58 * 16.54   # ~9.59 inches
_MAP_H_IN = 0.80 * 11.69   # ~9.35 inches


def _bbox(lon, lat, label, fontsize, dx, dy, extent, ha='left'):
    """Estimate a label's bounding box in data coordinates.

    Returns (x0, y0, x1, y1) — bottom-left to top-right.
    """
    lon_span = extent[1] - extent[0]
    lat_span = extent[3] - extent[2]

    deg_per_pt_x = lon_span / (_MAP_W_IN * 72)
    deg_per_pt_y = lat_span / (_MAP_H_IN * 72)

    w = len(label) * fontsize * _CHAR_WIDTH_RATIO * deg_per_pt_x
    h = fontsize * 1.4 * deg_per_pt_y

    cx = lon + dx
    cy = lat + dy

    if ha == 'left':
        x0, x1 = cx, cx + w
    elif ha == 'right':
        x0, x1 = cx - w, cx
    else:
        x0, x1 = cx - w / 2, cx + w / 2

    return (x0, cy - h / 2, x1, cy + h / 2)


def _overlap_area(a, b):
    """Overlap area between two (x0, y0, x1, y1) boxes. 0 if none."""
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    if dx <= 0 or dy <= 0:
        return 0.0
    return dx * dy


def _ha_for_offset(dx):
    """Pick horizontal alignment that keeps text away from anchor."""
    if dx > 0:
        return 'left'
    if dx < 0:
        return 'right'
    return 'center'


def _candidates(d):
    """Eight candidate offsets around the anchor point."""
    d2 = d * 1.4
    return [
        ( d,  d),    # NE
        (-d,  d),    # NW
        ( d, -d),    # SE
        (-d, -d),    # SW
        ( d2, 0),    # E
        (-d2, 0),    # W
        ( 0,  d2),   # N
        ( 0, -d2),   # S
    ]


def resolve(markers, spec):
    """Compute label offsets for markers, minimizing overlaps.

    Returns a list of (dx, dy, ha) tuples, one per marker.

    Markers with explicit 'name_offset' keep their position unless
    spec['auto_labels'] is True. Markers without name_offset get
    automatic placement via greedy candidate selection.
    """
    extent = spec['extent']
    scale = spec.get('_scale', {})
    d = scale.get('offset',
                  max(extent[1] - extent[0],
                      extent[3] - extent[2]) * 0.015)
    auto_all = spec.get('auto_labels', False)

    if not markers:
        return []

    # ── Collect fixed obstacles (zone labels, callouts) ─────────────
    obstacles = []
    for z in spec.get('zones', []):
        lp = z.get('label_pos')
        if lp and z.get('label'):
            obstacles.append(
                _bbox(lp[0], lp[1], z['label'],
                      z.get('label_size', 7), 0, 0, extent, 'center'))
    for c in spec.get('callouts', []):
        obstacles.append(
            _bbox(c['lon'], c['lat'], c['text'],
                  c.get('size', 9), 0, 0, extent,
                  c.get('ha', 'center')))

    # ── Initialize placements ───────────────────────────────────────
    results = []
    adjustable = []
    for m in markers:
        if 'name_offset' in m and not auto_all:
            dx, dy = m['name_offset']
            ha = m.get('name_ha', 'left')     # preserve original default
            results.append((dx, dy, ha))
            adjustable.append(False)
        else:
            # Start at NE; will be optimized below.
            results.append((d, d, 'left'))
            adjustable.append(True)

    # ── Greedy placement for adjustable labels ──────────────────────
    cands = _candidates(d)
    dot_r = d * 0.5

    for i, m in enumerate(markers):
        if not adjustable[i]:
            continue

        lon, lat = m['lon'], m['lat']
        name = m['name']
        fs = m.get('name_size', 6.5)

        best_score = float('inf')
        best = results[i]

        for cdx, cdy in cands:
            cha = _ha_for_offset(cdx)
            box = _bbox(lon, lat, name, fs, cdx, cdy, extent, cha)

            # Penalize out-of-bounds.
            if (box[0] < extent[0] or box[2] > extent[1]
                    or box[1] < extent[2] or box[3] > extent[3]):
                score = 1e6
            else:
                score = 0.0

            # Overlap with other marker labels.
            for j in range(len(markers)):
                if j == i:
                    continue
                dxj, dyj, haj = results[j]
                mj = markers[j]
                other = _bbox(mj['lon'], mj['lat'], mj['name'],
                              mj.get('name_size', 6.5),
                              dxj, dyj, extent, haj)
                score += _overlap_area(box, other)

            # Overlap with marker dots (penalize more heavily).
            for j in range(len(markers)):
                if j == i:
                    continue
                mj = markers[j]
                dot = (mj['lon'] - dot_r, mj['lat'] - dot_r,
                       mj['lon'] + dot_r, mj['lat'] + dot_r)
                score += _overlap_area(box, dot) * 3

            # Overlap with fixed obstacles (zones, callouts).
            for obs in obstacles:
                score += _overlap_area(box, obs)

            # Slight preference for NE (conventional cartographic placement).
            if cdx > 0 and cdy > 0:
                score *= 0.95

            if score < best_score:
                best_score = score
                best = (cdx, cdy, cha)

        results[i] = best

    return results
