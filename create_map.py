#!/usr/bin/env python3
"""
Western Mediterranean Deluge: Morocco Flood Crisis 2026-02
Production-quality A4 landscape analytical map.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely import ops
import warnings
warnings.filterwarnings('ignore')

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
A4_LANDSCAPE = (16.54, 11.69)  # inches
MAP_EXTENT = [-7.6, -3.6, 32.6, 37.0]  # lon_min, lon_max, lat_min, lat_max

# Colors
C_OCEAN = '#D4E4F0'
C_LAND = '#E6DFD4'
C_RIF = '#C0B098'
C_ATLAS = '#C8BCA8'
C_GHARB = '#EDE8DF'
C_BORDER = '#8A7A66'
C_COAST = '#8A7A66'
C_RIVER = '#4A90C4'
C_FLOOD = '#C03030'
C_DISPLACE = '#D97520'
C_CAMP = '#CC9900'
C_AGRI = '#7A5230'
C_TRADE = '#7B3FA0'
C_WATER = '#2878B0'
C_CONTEXT = '#666666'
C_BOTTOM_BG = '#F4F3F0'

# Fonts
FONT_TITLE = {'family': 'Liberation Sans', 'weight': 'bold'}
FONT_LABEL = {'family': 'Liberation Sans', 'weight': 'bold'}
FONT_BODY = {'family': 'Liberation Sans', 'weight': 'normal'}
FONT_MONO = {'family': 'Liberation Mono', 'weight': 'bold'}
FONT_QUOTE = {'family': 'Liberation Serif', 'style': 'italic'}

# White halo for map labels
HALO = [pe.withStroke(linewidth=3.2, foreground='white')]
HALO_THIN = [pe.withStroke(linewidth=2.5, foreground='white')]


def draw_map(ax):
    """Draw the basemap with all geographic layers."""
    proj = ccrs.PlateCarree()
    ax.set_extent(MAP_EXTENT, crs=proj)

    # 1. Ocean fill
    ax.set_facecolor(C_OCEAN)

    # 2. Land fill
    land = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                         facecolor=C_LAND, edgecolor='none')
    ax.add_feature(land, zorder=1)

    # 3. Terrain shading polygons
    _draw_terrain(ax, proj)

    # 4. Country borders
    ax.add_feature(cfeature.BORDERS, edgecolor=C_BORDER, linewidth=1.2, zorder=5)

    # 5. Coastlines
    coast = cfeature.NaturalEarthFeature('physical', 'coastline', '10m',
                                          facecolor='none', edgecolor=C_COAST)
    ax.add_feature(coast, linewidth=1.5, zorder=6)

    # 6. Rivers
    _draw_rivers(ax, proj)


def _draw_terrain(ax, proj):
    """Draw approximate terrain polygons for visual relief."""
    # Rif Mountains
    rif_coords = [
        (-5.8, 35.4), (-5.4, 35.5), (-4.8, 35.3), (-4.2, 35.1),
        (-3.8, 34.9), (-3.6, 34.7), (-4.0, 34.6), (-4.5, 34.65),
        (-5.0, 34.75), (-5.5, 35.0), (-5.8, 35.2), (-5.8, 35.4)
    ]
    rif = Polygon(rif_coords)
    ax.add_geometries([rif], proj, facecolor=C_RIF, edgecolor='none',
                      alpha=0.6, zorder=2)

    # Middle Atlas foothills
    atlas_coords = [
        (-6.0, 33.8), (-5.5, 33.6), (-4.8, 33.4), (-4.0, 33.2),
        (-3.6, 33.0), (-3.6, 33.6), (-4.0, 34.0), (-4.5, 34.2),
        (-5.0, 34.15), (-5.5, 34.05), (-6.0, 33.95), (-6.0, 33.8)
    ]
    atlas = Polygon(atlas_coords)
    ax.add_geometries([atlas], proj, facecolor=C_ATLAS, edgecolor='none',
                      alpha=0.5, zorder=2)

    # Gharb Plain (flood zone — distinctly flat/lighter)
    gharb_coords = [
        (-6.5, 34.0), (-5.6, 34.0), (-5.5, 34.15), (-5.5, 34.5),
        (-5.6, 34.8), (-6.0, 34.85), (-6.4, 34.6), (-6.6, 34.3),
        (-6.5, 34.0)
    ]
    gharb = Polygon(gharb_coords)
    ax.add_geometries([gharb], proj, facecolor=C_GHARB, edgecolor='none',
                      alpha=0.7, zorder=2)

    # Andalusian highlands
    anda_coords = [
        (-6.0, 36.2), (-5.5, 36.0), (-4.8, 36.3), (-4.0, 36.5),
        (-3.6, 36.8), (-3.6, 37.0), (-4.5, 37.0), (-5.5, 37.0),
        (-6.5, 37.0), (-7.0, 36.8), (-6.5, 36.5), (-6.0, 36.2)
    ]
    anda = Polygon(anda_coords)
    ax.add_geometries([anda], proj, facecolor=C_ATLAS, edgecolor='none',
                      alpha=0.45, zorder=2)


def _draw_rivers(ax, proj):
    """Draw major rivers with cartopy NaturalEarth + manual supplements."""
    # Try to get rivers from Natural Earth
    try:
        rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines',
                                               '10m', facecolor='none',
                                               edgecolor=C_RIVER)
        ax.add_feature(rivers, linewidth=1.5, alpha=0.7, zorder=4)
    except Exception:
        pass

    # Manual river lines for key rivers that may not be detailed enough
    # Loukkos River
    loukkos = [(-5.45, 34.98), (-5.55, 34.92), (-5.62, 34.88),
               (-5.72, 34.78), (-5.78, 34.72), (-5.88, 34.58),
               (-5.95, 34.48), (-6.05, 34.35), (-6.15, 34.25)]
    ax.plot([p[0] for p in loukkos], [p[1] for p in loukkos],
            color=C_RIVER, linewidth=2.8, alpha=0.8, transform=proj, zorder=4,
            solid_capstyle='round')

    # Sebou River
    sebou = [(-4.3, 34.08), (-4.5, 34.04), (-4.7, 34.0),
             (-4.9, 34.01), (-5.1, 34.02), (-5.3, 34.06),
             (-5.4, 34.10), (-5.55, 34.14), (-5.7, 34.18),
             (-5.9, 34.22), (-6.1, 34.24), (-6.3, 34.26),
             (-6.55, 34.28)]
    ax.plot([p[0] for p in sebou], [p[1] for p in sebou],
            color=C_RIVER, linewidth=3.2, alpha=0.8, transform=proj, zorder=4,
            solid_capstyle='round')

    # River labels
    ax.text(-5.70, 34.65, 'Loukkos', fontsize=6, color=C_RIVER,
            fontstyle='italic', path_effects=HALO_THIN, transform=proj, zorder=10,
            rotation=-55, **FONT_BODY)
    ax.text(-5.15, 34.14, 'Sebou', fontsize=6, color=C_RIVER,
            fontstyle='italic', path_effects=HALO_THIN, transform=proj, zorder=10,
            rotation=-5, **FONT_BODY)


def draw_flood_extent(ax, proj):
    """Draw the flood extent polygon with dashed outline."""
    vertices = [
        (-6.55, 33.98), (-6.15, 34.0), (-5.75, 34.15),
        (-5.65, 34.6), (-5.7, 34.75), (-6.0, 34.8),
        (-6.4, 34.5), (-6.55, 33.98)
    ]
    flood_poly = Polygon(vertices)
    ax.add_geometries([flood_poly], proj, facecolor=C_FLOOD, alpha=0.12,
                      edgecolor='none', zorder=7)
    # Dashed outline
    xs = [v[0] for v in vertices] + [vertices[0][0]]
    ys = [v[1] for v in vertices] + [vertices[0][1]]
    ax.plot(xs, ys, color=C_FLOOD, linewidth=1.8, linestyle='--',
            alpha=0.6, transform=proj, zorder=7)

    # Label
    ax.text(-6.05, 34.42, 'FLOOD EXTENT', fontsize=7, color=C_FLOOD,
            transform=proj, zorder=15, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#B03030', alpha=0.9, linewidth=1.0),
            **FONT_LABEL)


def draw_farmland_hatching(ax, proj):
    """Draw X-pattern markers for submerged farmland."""
    np.random.seed(42)
    # Scatter X marks within the Gharb plain
    farm_lons = np.random.uniform(-6.45, -5.8, 20)
    farm_lats = np.random.uniform(34.05, 34.65, 20)
    for lon, lat in zip(farm_lons, farm_lats):
        ax.plot(lon, lat, marker='x', markersize=5, color=C_AGRI,
                alpha=0.35, transform=proj, zorder=8, markeredgewidth=1.5)


def draw_dams(ax, proj):
    """Draw dam locations with triangle markers and annotations."""
    # Oued El Makhazine
    ax.plot(-5.6, 34.95, marker='^', markersize=10, color=C_WATER,
            markeredgecolor='white', markeredgewidth=0.8,
            transform=proj, zorder=12)
    ax.text(-5.48, 34.95, 'Oued El Makhazine', fontsize=5.5,
            color='#333333', transform=proj, zorder=15,
            path_effects=HALO_THIN, va='center', **FONT_LABEL)
    ax.text(-5.48, 34.89, '146% capacity', fontsize=5, color=C_FLOOD,
            transform=proj, zorder=15, path_effects=HALO_THIN,
            va='center', **FONT_BODY)

    # Arrow from dam downstream
    ax.annotate('', xy=(-5.78, 34.68), xytext=(-5.6, 34.90),
                arrowprops=dict(arrowstyle='->', color=C_WATER,
                                lw=2.0, connectionstyle='arc3,rad=0.15'),
                transform=proj, zorder=11)
    ax.text(-5.78, 34.80, 'releases\n560 m³/s', fontsize=4.5,
            color=C_WATER, transform=proj, zorder=15,
            ha='center', va='center', path_effects=HALO_THIN,
            **FONT_BODY)

    # Al Wahda
    ax.plot(-5.05, 34.45, marker='^', markersize=10, color=C_WATER,
            markeredgecolor='white', markeredgewidth=0.8,
            transform=proj, zorder=12)
    ax.text(-4.93, 34.45, 'Al Wahda', fontsize=5.5,
            color='#333333', transform=proj, zorder=15,
            path_effects=HALO_THIN, va='center', **FONT_LABEL)
    ax.text(-4.93, 34.39, 'critical threshold', fontsize=5,
            color=C_FLOOD, transform=proj, zorder=15,
            path_effects=HALO_THIN, va='center', **FONT_BODY)


def draw_cities(ax, proj):
    """Draw all city markers with annotations."""
    # Crisis cities (square, red)
    crisis_cities = [
        (-5.90, 34.98, 'Ksar El Kebir', '85% evacuated\n~50 000 displaced'),
        (-5.71, 34.22, 'Sidi Kacem', 'villages submerged'),
        (-5.93, 34.26, 'Sidi Slimane', 'partially submerged'),
    ]
    for lon, lat, name, annotation in crisis_cities:
        ax.plot(lon, lat, marker='s', markersize=7, color=C_FLOOD,
                markeredgecolor='white', markeredgewidth=0.7,
                transform=proj, zorder=13)
        ax.text(lon + 0.06, lat + 0.06, name, fontsize=6.5,
                color='#1a1a1a', transform=proj, zorder=15,
                path_effects=HALO, **FONT_LABEL)
        ax.text(lon + 0.06, lat - 0.06, annotation, fontsize=4.8,
                color=C_FLOOD, transform=proj, zorder=15,
                path_effects=HALO_THIN, va='top', **FONT_BODY)

    # Displacement camp (triangle, gold)
    ax.plot(-6.58, 34.26, marker='^', markersize=9, color=C_CAMP,
            markeredgecolor='white', markeredgewidth=0.7,
            transform=proj, zorder=13)
    ax.text(-6.72, 34.36, 'Kenitra', fontsize=7, color='#1a1a1a',
            transform=proj, zorder=15, path_effects=HALO,
            ha='center', **FONT_LABEL)
    ax.text(-6.72, 34.22, '40 000 in camps\n3 000 families', fontsize=4.8,
            color=C_CAMP, transform=proj, zorder=15,
            path_effects=HALO_THIN, ha='center', va='top', **FONT_BODY)

    # Provincial hub (diamond, orange)
    ax.plot(-6.15, 35.19, marker='D', markersize=8, color=C_DISPLACE,
            markeredgecolor='white', markeredgewidth=0.7,
            transform=proj, zorder=13)
    ax.text(-6.03, 35.19, 'Larache', fontsize=7, color='#1a1a1a',
            transform=proj, zorder=15, path_effects=HALO,
            va='center', **FONT_LABEL)
    ax.text(-6.03, 35.12, '81 700 evacuated', fontsize=4.8,
            color=C_DISPLACE, transform=proj, zorder=15,
            path_effects=HALO_THIN, va='top', **FONT_BODY)

    # Context cities (circle, grey)
    context_cities = [
        (-5.80, 35.77, 'Tangier', '1 500 mm since Sep 2025'),
        (-5.37, 35.57, 'Tetouan', 'flash flood: 4 dead'),
        (-6.83, 33.97, 'Rabat', ''),
    ]
    for lon, lat, name, annotation in context_cities:
        ax.plot(lon, lat, marker='o', markersize=6, color=C_CONTEXT,
                markeredgecolor='white', markeredgewidth=0.7,
                transform=proj, zorder=13)
        ax.text(lon + 0.06, lat + 0.06, name, fontsize=6.5,
                color='#333333', transform=proj, zorder=15,
                path_effects=HALO, **FONT_LABEL)
        if annotation:
            ax.text(lon + 0.06, lat - 0.04, annotation, fontsize=4.5,
                    color=C_CONTEXT, transform=proj, zorder=15,
                    path_effects=HALO_THIN, va='top', **FONT_BODY)


def draw_displacement_arrows(ax, proj):
    """Draw three displacement flow arrows converging on Kenitra."""
    arrows = [
        ((-5.95, 34.85), (-6.52, 34.35), 0.2),
        ((-5.82, 34.25), (-6.52, 34.3), -0.1),
        ((-6.12, 35.1), (-6.52, 34.38), 0.2),
    ]
    for (x1, y1), (x2, y2), rad in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=C_DISPLACE,
                                    lw=2.5, alpha=0.55,
                                    connectionstyle=f'arc3,rad={rad}'),
                    transform=proj, zorder=10)

    # Label
    ax.text(-6.10, 34.62, 'DISPLACEMENT', fontsize=5.5,
            color=C_DISPLACE, transform=proj, zorder=15,
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=C_DISPLACE, alpha=0.9, linewidth=0.8),
            **FONT_LABEL)


def draw_supply_chain(ax, proj):
    """Draw supply chain disruption line through Strait of Gibraltar."""
    route = [(-6.2, 35.15), (-5.9, 35.4), (-5.6, 35.83)]
    ax.plot([p[0] for p in route], [p[1] for p in route],
            color=C_TRADE, linewidth=2.0, linestyle='--', alpha=0.5,
            transform=proj, zorder=9)
    # Red X at the Strait crossing
    ax.plot(-5.6, 35.83, marker='X', markersize=14, color=C_FLOOD,
            markeredgecolor='white', markeredgewidth=1.0,
            transform=proj, zorder=14)
    # Label
    ax.text(-5.15, 35.85, 'SUPPLY CHAIN\nDISRUPTED', fontsize=5,
            color=C_TRADE, transform=proj, zorder=15,
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=C_TRADE, alpha=0.9, linewidth=0.8),
            **FONT_LABEL)


def draw_andalusia_callout(ax, proj):
    """Draw Andalusia callout text over southern Spain."""
    ax.text(-5.3, 36.65, 'ANDALUSIA', fontsize=9, color=C_FLOOD,
            transform=proj, zorder=15, ha='center',
            path_effects=HALO, **FONT_LABEL)
    ax.text(-5.3, 36.48, '40 000 ha | 80% olive crop lost | EUR 3.5 bn',
            fontsize=5, color='#444444', transform=proj, zorder=15,
            ha='center', path_effects=HALO_THIN, **FONT_BODY)


def draw_scale_bar(ax, proj):
    """Draw a 100 km scale bar in the bottom-left of the map."""
    # At ~34°N, 1 degree longitude ≈ 93 km
    bar_lon = -7.3
    bar_lat = 32.85
    bar_length_deg = 100 / 93.0  # ~1.075 degrees

    ax.plot([bar_lon, bar_lon + bar_length_deg], [bar_lat, bar_lat],
            color='#333333', linewidth=2.5, transform=proj, zorder=15,
            solid_capstyle='butt')
    # End ticks
    for x in [bar_lon, bar_lon + bar_length_deg]:
        ax.plot([x, x], [bar_lat - 0.06, bar_lat + 0.06],
                color='#333333', linewidth=1.5, transform=proj, zorder=15)
    ax.text(bar_lon + bar_length_deg / 2, bar_lat + 0.12, '100 km',
            fontsize=5.5, ha='center', color='#333333',
            transform=proj, zorder=15, path_effects=HALO_THIN,
            **FONT_LABEL)


def draw_map_title(fig):
    """Draw the main title in the top-left area of the figure."""
    fig.text(0.02, 0.97, 'WESTERN MEDITERRANEAN DELUGE',
             fontsize=22, color='#1a1a1a', va='top', **FONT_TITLE)
    fig.text(0.02, 0.935, 'Morocco Flood Crisis — January/February 2026',
             fontsize=11, color='#444444', va='top', **FONT_BODY)
    fig.text(0.02, 0.915, 'Gharb–Loukkos Basins  |  NW Morocco',
             fontsize=8, color=C_CONTEXT, va='top', **FONT_BODY)


def draw_panel_inflow(fig):
    """Draw the water inflow bar chart panel (top right)."""
    ax = fig.add_axes([0.61, 0.68, 0.36, 0.26])
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color('#DDDDDD')
        spine.set_linewidth(0.5)

    labels = ['2024\n(full year)', '2025\n(full year)',
              '2026-01-11 to\n2026-02-11']
    values = [4.5, 4.5, 8.82]
    colors = [C_WATER, C_WATER, C_FLOOD]
    alphas = [0.45, 0.45, 0.75]

    bars = ax.barh(range(len(labels)), values, color=colors, height=0.55,
                   edgecolor='white', linewidth=0.5)
    for bar, a in zip(bars, alphas):
        bar.set_alpha(a)

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=7, **FONT_BODY)
    ax.set_xlim(0, 11)
    ax.set_xlabel('billions of cubic metres', fontsize=6, color='#666666',
                  **FONT_BODY)
    ax.tick_params(axis='x', labelsize=6, colors='#666666')
    ax.invert_yaxis()

    # Value labels on bars
    for i, v in enumerate(values):
        ax.text(v + 0.15, i, f'{v}', fontsize=7, va='center',
                color='#333333', **FONT_MONO)

    # Annotation on red bar
    ax.text(8.82, 2.42, 'ONE MONTH = TWO YEARS', fontsize=6.5,
            color=C_FLOOD, ha='right', va='top', **FONT_LABEL)

    # Title
    ax.set_title('WATER INFLOW TO MOROCCAN DAMS', fontsize=9,
                 loc='left', pad=8, color='#1a1a1a', **FONT_TITLE)


def draw_panel_human_cost(fig):
    """Draw the human cost metrics and voices panel (bottom right)."""
    ax = fig.add_axes([0.61, 0.145, 0.36, 0.50])
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color('#DDDDDD')
        spine.set_linewidth(0.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.text(0.03, 0.96, 'THE HUMAN COST', fontsize=10,
            color='#1a1a1a', va='top', **FONT_TITLE)

    # Metrics
    metrics = [
        ('188 000', 'persons displaced', C_DISPLACE, 'across 4 provinces'),
        ('40 000', 'in tent camps near Kenitra', C_CAMP, 'blue tents | livestock separated'),
        ('4', 'confirmed dead', C_FLOOD, 'incl. 2-year-old | 1 missing'),
        ('110 000+', 'hectares submerged', C_AGRI, 'cereal | sugar beet | citrus'),
        ('$328 M', 'government relief package', C_WATER, '~10% earmarked for farmers'),
        ('CHF 1.6 M', 'IFRC emergency appeal', C_WATER, 'Red Crescent operations'),
    ]

    y = 0.87
    for value, desc, color, detail in metrics:
        ax.text(0.03, y, value, fontsize=9, color=color, va='top',
                **{'family': 'Liberation Mono', 'weight': 'bold'})
        ax.text(0.30, y, desc, fontsize=7, color='#333333', va='top',
                **FONT_BODY)
        ax.text(0.30, y - 0.045, detail, fontsize=5.5, color='#888888',
                va='top', **FONT_BODY)
        y -= 0.095

    # Divider
    divider_y = y + 0.03
    ax.plot([0.03, 0.97], [divider_y, divider_y], color='#CCCCCC',
            linewidth=0.8, zorder=5)

    # Voices section
    y = divider_y - 0.04
    ax.text(0.03, y, 'VOICES FROM THE CAMPS', fontsize=8,
            color='#1a1a1a', va='top', **FONT_LABEL)
    y -= 0.06

    quotes = [
        ('"The water took everything."',
         '— Ibrahim Bernous, 32, camp near Kenitra'),
        ('"We have no grain left to feed our livestock,\n  and they are our main source of income."',
         '— Chergui al-Alja, 42'),
        ('"All of it is gone now. Still, praise be to\n  God for this blessing."',
         '— Mohamed Reouani, 63, Ouled Salama'),
    ]

    for quote, attribution in quotes:
        ax.text(0.05, y, quote, fontsize=6.5, color='#333333', va='top',
                **FONT_QUOTE, linespacing=1.3)
        lines = quote.count('\n') + 1
        y -= 0.045 * lines + 0.01
        ax.text(0.05, y, attribution, fontsize=5.5, color='#888888',
                va='top', **FONT_BODY)
        y -= 0.055


def draw_bottom_bar(fig):
    """Draw the metabolic flow analysis bar at the bottom."""
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.125])
    ax.set_facecolor(C_BOTTOM_BG)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # Top border line
    ax.plot([0, 1], [1, 1], color='#CCCCCC', linewidth=0.8, zorder=5)

    # Metabolic flow rows
    flows = [
        ('WATER', '8.82 × 10⁹ m³ inflow in one month ≈ 2 years combined on drought-degraded soils: max runoff, min infiltration'),
        ('SOIL', '110 000+ ha waterlogged: topsoil stripping, salinization risk in coastal lowlands; restoration: months to years'),
        ('AGRI', '7-year drought depleted reserves; flood destroyed current + next season capacity; price spike cycle repeats'),
        ('TRADE', 'Spain + Morocco = 58% UK tomatoes, 72% cucumbers, 75% sweet peppers in winter; Strait transport disrupted'),
        ('PEOPLE', '188 000 displaced (rainfed smallholders + pastoralists): structural vulnerability to next drought–deluge cycle'),
    ]

    cat_colors = {
        'WATER': C_WATER, 'SOIL': C_AGRI, 'AGRI': '#8B6914',
        'TRADE': C_TRADE, 'PEOPLE': C_DISPLACE
    }

    y = 0.90
    for cat, text in flows:
        ax.text(0.015, y, cat, fontsize=5.5, color=cat_colors[cat],
                va='top', **FONT_LABEL)
        ax.text(0.065, y, text, fontsize=5, color='#444444',
                va='top', **FONT_BODY)
        y -= 0.185

    # Legend (right side)
    legend_x = 0.72
    legend_y = 0.88

    legend_items = [
        ('s', C_FLOOD, 'Crisis city'),
        ('^', C_CAMP, 'Displacement camp'),
        ('D', C_DISPLACE, 'Provincial hub'),
        ('o', C_CONTEXT, 'Context city'),
        ('^', C_WATER, 'Dam'),
    ]

    ax.text(legend_x, legend_y + 0.05, 'LEGEND', fontsize=6,
            color='#333333', va='top', **FONT_LABEL)

    for i, (marker, color, label) in enumerate(legend_items):
        ypos = legend_y - i * 0.155
        ax.plot(legend_x + 0.01, ypos, marker=marker, markersize=6,
                color=color, markeredgecolor='white', markeredgewidth=0.5,
                transform=ax.transAxes, clip_on=False)
        ax.text(legend_x + 0.035, ypos, label, fontsize=5,
                color='#444444', va='center', **FONT_BODY,
                transform=ax.transAxes)

    # Line legend items
    line_items = [
        ('--', C_FLOOD, 1.5, 'Flood extent'),
        ('-', C_RIVER, 2.0, 'River'),
        ('--', C_TRADE, 1.5, 'Supply chain disruption'),
        ('-', C_DISPLACE, 2.0, 'Displacement flow'),
    ]

    lx = 0.84
    for i, (ls, color, lw, label) in enumerate(line_items):
        ypos = legend_y - i * 0.155
        ax.plot([lx, lx + 0.025], [ypos, ypos], linestyle=ls, color=color,
                linewidth=lw, alpha=0.7, transform=ax.transAxes, clip_on=False)
        ax.text(lx + 0.035, ypos, label, fontsize=5, color='#444444',
                va='center', **FONT_BODY, transform=ax.transAxes)

    # Hatching legend
    ypos = legend_y - 4 * 0.155
    ax.plot(legend_x + 0.01, ypos, marker='x', markersize=5,
            color=C_AGRI, alpha=0.5, markeredgewidth=1.5,
            transform=ax.transAxes, clip_on=False)
    ax.text(legend_x + 0.035, ypos, 'Submerged farmland', fontsize=5,
            color='#444444', va='center', **FONT_BODY,
            transform=ax.transAxes)

    # Source line
    ax.text(0.98, 0.06,
            'Sources: IFRC | Moroccan Interior Ministry | COAG Andalusia | AFP | ESA/Copernicus | ReliefWeb | Met Office',
            fontsize=4, color='#999999', va='bottom', ha='right',
            **FONT_BODY)


def create_map():
    """Main function to create the full map figure."""
    proj = ccrs.PlateCarree()

    fig = plt.figure(figsize=A4_LANDSCAPE, dpi=200)
    fig.patch.set_facecolor('white')

    # Map axes (left 59% of figure, leaving space for panels and bottom bar)
    ax_map = fig.add_axes([0.01, 0.145, 0.58, 0.80], projection=proj)

    # Draw all map layers
    draw_map(ax_map)
    draw_flood_extent(ax_map, proj)
    draw_farmland_hatching(ax_map, proj)
    draw_dams(ax_map, proj)
    draw_cities(ax_map, proj)
    draw_displacement_arrows(ax_map, proj)
    draw_supply_chain(ax_map, proj)
    draw_andalusia_callout(ax_map, proj)
    draw_scale_bar(ax_map, proj)

    # Draw title
    draw_map_title(fig)

    # Draw right-side panels
    draw_panel_inflow(fig)
    draw_panel_human_cost(fig)

    # Draw bottom bar
    draw_bottom_bar(fig)

    # Farmland annotation below map
    fig.text(0.30, 0.14, '✕ 110 000+ ha submerged farmland: cereal, sugar beet, citrus',
             fontsize=5.5, color=C_AGRI, va='top', ha='center', **FONT_BODY)

    # Save outputs
    fig.savefig('morocco_crisis_map.jpg', dpi=200, bbox_inches='tight',
                pad_inches=0.1, facecolor='white')
    print("Saved morocco_crisis_map.jpg at 200 dpi")

    fig.savefig('morocco_crisis_map.pdf', dpi=300, bbox_inches='tight',
                pad_inches=0.1, facecolor='white')
    print("Saved morocco_crisis_map.pdf at 300 dpi")

    plt.close(fig)


if __name__ == '__main__':
    create_map()
