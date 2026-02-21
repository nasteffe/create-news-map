"""Gaza: Ceasefire to Reconstruction — January/February 2026.

This file is pure data — a dict describing what to draw.
The newsmap package handles how to draw it.
"""

MAP = {

    # ── Metadata ─────────────────────────────────────────────────────────
    'meta': {
        'title': 'GAZA: CEASEFIRE TO RECONSTRUCTION',
        'subtitle': 'Phase Two of the Gaza Peace Plan — January/February 2026',
        'tagline': 'Gaza Strip  |  Occupied Palestinian Territory',
    },

    # ── Geography ────────────────────────────────────────────────────────
    'extent': [34.0, 34.75, 31.08, 31.72],
    'projection': 'PlateCarree',

    'layout': {
        'size': (16.54, 11.69),           # A4 landscape
        'map': [0.01, 0.145, 0.58, 0.80],
    },

    'colors': {
        'ocean':  '#C8DDE8',
        'land':   '#E8E2D8',
        'border': '#777777',
        'coast':  '#8A9AA6',
        'river':  '#4A90C4',
    },

    # ── Terrain ──────────────────────────────────────────────────────────
    # Gaza sits on a coastal plain rising gently east toward the Negev.
    # Three parallel kurkar (calcareous sandstone) ridges run NE–SW
    # through the strip; real elevation ranges 0–110 m.  The Negev
    # rises to 200–400 m east of the border.  DEM values are
    # exaggerated to produce visible hillshade relief.

    'hillshade': True,
    'hillshade_alpha': 0.18,
    'hillshade_resolution': 300,
    'hillshade_smooth': 10,

    'terrain_zones': [
        # Coastal sand-dune belt (Sheikh Ejlin kurkar ridge zone).
        # Real elevation: 0–40 m; narrow strip along the Mediterranean.
        {
            'name': 'Coastal sand belt',
            'vertices': [
                (34.0, 31.08), (34.28, 31.08), (34.30, 31.20),
                (34.34, 31.35), (34.38, 31.48), (34.42, 31.58),
                (34.44, 31.68), (34.44, 31.72), (34.0, 31.72),
                (34.0, 31.08),
            ],
            'color': '#E5DEC8', 'alpha': 0.18, 'elevation': 20,
        },
        # Inner coastal plain (inter-ridge depressions, alluvium).
        # Real elevation: 20–60 m; where most of Gaza's cities sit.
        {
            'name': 'Inner coastal plain',
            'vertices': [
                (34.28, 31.08), (34.42, 31.08), (34.45, 31.25),
                (34.48, 31.40), (34.50, 31.55), (34.52, 31.68),
                (34.52, 31.72), (34.44, 31.72), (34.44, 31.68),
                (34.42, 31.58), (34.38, 31.48), (34.34, 31.35),
                (34.30, 31.20), (34.28, 31.08),
            ],
            'color': '#DDD5C0', 'alpha': 0.25, 'elevation': 80,
        },
        # Eastern ridge zone (Al Montar kurkar ridge + Israeli border).
        # Real elevation: 40–110 m; Gaza's highest ground & former
        # agricultural heartland.
        {
            'name': 'Eastern ridge / border zone',
            'vertices': [
                (34.42, 31.08), (34.56, 31.08), (34.58, 31.25),
                (34.58, 31.40), (34.57, 31.55), (34.56, 31.68),
                (34.55, 31.72), (34.52, 31.72), (34.52, 31.68),
                (34.50, 31.55), (34.48, 31.40), (34.45, 31.25),
                (34.42, 31.08),
            ],
            'color': '#D0C8B0', 'alpha': 0.30, 'elevation': 250,
        },
        # Western Negev foothills — semi-arid loess hills.
        # Real elevation: 100–250 m.
        {
            'name': 'Western Negev foothills',
            'vertices': [
                (34.56, 31.08), (34.68, 31.08), (34.68, 31.72),
                (34.55, 31.72), (34.56, 31.68), (34.57, 31.55),
                (34.58, 31.40), (34.58, 31.25), (34.56, 31.08),
            ],
            'color': '#C8C0A8', 'alpha': 0.35, 'elevation': 500,
        },
        # Negev plateau — rolling hills, eastern edge of map.
        # Real elevation: 200–400 m.
        {
            'name': 'Negev plateau',
            'vertices': [
                (34.68, 31.08), (34.75, 31.08), (34.75, 31.72),
                (34.68, 31.72), (34.68, 31.08),
            ],
            'color': '#BFB598', 'alpha': 0.40, 'elevation': 900,
        },
        # Sinai desert margin — flat coastal desert south of Rafah.
        # Real elevation: 0–50 m.
        {
            'name': 'Sinai desert margin',
            'vertices': [
                (34.0, 31.08), (34.28, 31.08), (34.25, 31.22),
                (34.20, 31.22), (34.0, 31.18), (34.0, 31.08),
            ],
            'color': '#DDD0B0', 'alpha': 0.22, 'elevation': 40,
        },
    ],

    # Wadi Gaza / Nahal Besor — 105 km river system from the Negev
    # hills to the Mediterranean at Al-Zahra (31.464°N, 34.376°E).
    # Eight curves within the 9 km Gaza crossing.
    'ne_rivers': True,

    'rivers': [
        {
            'name': 'Wadi Gaza',
            'coords': [
                # Nahal Besor in the Negev (Israeli side).
                (34.75, 31.28), (34.65, 31.33),
                # Nahal Gerar confluence near Re'im.
                (34.54, 31.39),
                # Curves north toward Gaza border.
                (34.50, 31.43), (34.47, 31.46),
                # 9 km crossing through central Gaza (eight meanders).
                (34.44, 31.46), (34.42, 31.462),
                (34.40, 31.46), (34.376, 31.464),
            ],
            'width': 2.5,
            'label_pos': (34.60, 31.36),
            'label_rotation': -18,
        },
    ],

    'lakes': False,

    # ── Analytical overlays ──────────────────────────────────────────────

    # "Yellow Line" buffer zone — runs the full eastern border of Gaza,
    # pushed 1.5 km (south) to 6.5 km (north) into the strip.  Covers
    # ~58 % of the enclave; marked on the ground by yellow concrete blocks.
    'zones': [
        {
            'vertices': [
                # Western edge of buffer (the "Yellow Line" itself, S → N)
                (34.28, 31.22), (34.36, 31.30), (34.40, 31.38),
                (34.44, 31.44), (34.46, 31.48), (34.49, 31.52),
                (34.50, 31.56), (34.49, 31.59),
                # Eastern edge (Gaza–Israel border, N → S)
                (34.56, 31.59), (34.56, 31.52), (34.52, 31.44),
                (34.48, 31.38), (34.42, 31.30), (34.35, 31.24),
                (34.28, 31.22),
            ],
            'fill': '#DAA520', 'fill_alpha': 0.12,
            'edge': '#DAA520', 'edge_alpha': 0.70,
            'edge_width': 2.5, 'edge_style': '-',
            'label': '"YELLOW LINE"\nBUFFER ZONE\n~58% of Gaza',
            'label_pos': (34.54, 31.36),
            'label_border': '#DAA520',
            'label_size': 5,
        },
        # Severe destruction zone — northern Gaza.
        {
            'vertices': [
                (34.37, 31.48), (34.44, 31.57), (34.56, 31.59),
                (34.56, 31.48), (34.50, 31.45), (34.37, 31.48),
            ],
            'fill': '#C03030', 'fill_alpha': 0.10,
            'edge': '#C03030', 'edge_alpha': 0.5,
            'label': 'SEVERE DESTRUCTION',
            'label_pos': (34.50, 31.555),
            'label_border': '#C03030',
            'label_size': 5.5,
        },
    ],

    # Rubble / destruction scatter in northern Gaza.
    'scatter_marks': [
        {
            'bounds': (34.40, 34.55, 31.48, 31.58),
            'n': 15, 'marker': 'x', 'color': '#8B4513',
            'alpha': 0.30, 'seed': 7,
        },
    ],

    # ── Point markers ────────────────────────────────────────────────────
    # Label-collision strategy: all southern annotations are single-line;
    # al-Mawasi labels go RIGHT while neighbours go LEFT.
    'markers': [
        # Border crossings (triangle, blue).
        {
            'lon': 34.255, 'lat': 31.243, 'shape': '^', 'size': 10,
            'color': '#2878B0', 'name': 'Rafah Crossing',
            'name_size': 6, 'name_offset': (-0.12, -0.008), 'name_ha': 'center',
            'annotation': 'Reopened Feb 2 | EU-supervised',
            'ann_color': '#2878B0', 'ann_size': 4.5,
            'ann_offset': (-0.12, -0.025), 'ann_ha': 'center',
        },
        {
            'lon': 34.29, 'lat': 31.215, 'shape': '^', 'size': 10,
            'color': '#2878B0', 'name': 'Kerem Abu Salem',
            'name_size': 6, 'name_offset': (0.05, 0.005), 'name_va': 'center',
            'annotation': 'Main aid entry | 65 000+ trucks',
            'ann_color': '#2878B0', 'ann_size': 4.5,
            'ann_offset': (0.05, -0.018),
        },
        {
            'lon': 34.56, 'lat': 31.585, 'shape': '^', 'size': 9,
            'color': '#2878B0', 'name': 'Erez Crossing',
            'name_size': 6, 'name_offset': (-0.04, 0.012), 'name_ha': 'right',
            'annotation': 'Northern border',
            'ann_color': '#666666', 'ann_size': 4.5,
            'ann_offset': (-0.04, -0.015), 'ann_ha': 'right',
        },
        # Southern cities (diamond, orange).
        {
            'lon': 34.245, 'lat': 31.29, 'shape': 'D', 'size': 8,
            'color': '#D97520', 'name': 'Rafah',
            'name_size': 7, 'name_offset': (-0.11, 0.005), 'name_ha': 'center',
            'annotation': 'ISF deploying first | reconstruction priority',
            'ann_color': '#D97520', 'ann_size': 4.5,
            'ann_offset': (-0.11, -0.015), 'ann_ha': 'center',
        },
        {
            'lon': 34.305, 'lat': 31.345, 'shape': 'D', 'size': 8,
            'color': '#D97520', 'name': 'Khan Yunis',
            'name_size': 7, 'name_offset': (-0.07, 0.005), 'name_ha': 'right',
            'annotation': 'Nasser Hospital | ceasefire violations',
            'ann_color': '#D97520', 'ann_size': 4.5,
            'ann_offset': (-0.07, -0.015), 'ann_ha': 'right',
        },
        # Overcrowded displacement zone — labels RIGHT to avoid Khan Yunis.
        {
            'lon': 34.265, 'lat': 31.33, 'shape': 'o', 'size': 5,
            'color': '#C03030', 'name': 'al-Mawasi',
            'name_size': 5, 'name_offset': (0.035, -0.003), 'name_ha': 'left',
            'name_color': '#C03030',
            'annotation': '"Safe zone" | 47 700/km\u00b2',
            'ann_color': '#C03030', 'ann_size': 4,
            'ann_offset': (0.035, -0.016), 'ann_ha': 'left',
        },
        # Central medical hub (diamond, green).
        {
            'lon': 34.34, 'lat': 31.42, 'shape': 'D', 'size': 8,
            'color': '#2B8C5A', 'name': 'Deir al-Balah',
            'name_size': 7, 'name_offset': (-0.06, 0.005), 'name_ha': 'right',
            'annotation': 'MSF field hospital | humanitarian hub',
            'ann_color': '#2B8C5A', 'ann_size': 4.5,
            'ann_offset': (-0.06, -0.015), 'ann_ha': 'right',
        },
        # Central refugee camp (circle, red).
        {
            'lon': 34.393, 'lat': 31.449, 'shape': 'o', 'size': 5,
            'color': '#C03030', 'name': 'Nuseirat',
            'name_size': 5.5, 'name_offset': (-0.05, 0.003), 'name_ha': 'right',
            'name_color': '#C03030',
            'annotation': 'Strikes continue',
            'ann_color': '#666666', 'ann_size': 4,
            'ann_offset': (-0.05, -0.012), 'ann_ha': 'right',
        },
        # Northern crisis cities (square, red).
        {
            'lon': 34.44, 'lat': 31.505, 'shape': 's', 'size': 8,
            'color': '#C03030', 'name': 'Gaza City',
            'name_size': 7.5, 'name_offset': (-0.06, 0.01), 'name_ha': 'right',
            'annotation': 'Mass returns amid rubble\nAl-Shifa Hospital destroyed',
            'ann_color': '#C03030', 'ann_size': 4.5,
            'ann_offset': (-0.06, -0.02), 'ann_ha': 'right',
        },
        {
            'lon': 34.49, 'lat': 31.535, 'shape': 's', 'size': 7,
            'color': '#C03030', 'name': 'Jabalia',
            'name_size': 6.5, 'name_offset': (0.04, 0.008), 'name_va': 'center',
            'annotation': 'Camp destroyed | IPC Phase 4',
            'ann_color': '#C03030', 'ann_size': 4.5,
            'ann_offset': (0.04, -0.015),
        },
    ],

    # ── Arrows ───────────────────────────────────────────────────────────
    'arrow_groups': [
        # Return flow (south → north).
        {
            'arrows': [
                {'from': (34.30, 31.30), 'to': (34.40, 31.48), 'arc': 0.15},
                {'from': (34.28, 31.34), 'to': (34.44, 31.52), 'arc': 0.20},
            ],
            'color': '#D97520', 'width': 2.5, 'alpha': 0.55,
            'label': '690 000 RETURN\nMOVEMENTS',
            'label_pos': (34.22, 31.39),
            'label_size': 5.5,
        },
        # Aid inflow from Kerem Abu Salem.
        {
            'arrows': [
                {'from': (34.30, 31.22), 'to': (34.32, 31.30), 'arc': 0.0},
            ],
            'color': '#2878B0', 'width': 2.0, 'alpha': 0.6,
            'label': 'AID\nINFLOW',
            'label_pos': (34.37, 31.25),
            'label_box': False, 'label_size': 4.5,
        },
        # Medical evacuation (Rafah → Egypt).
        {
            'arrows': [
                {'from': (34.25, 31.24), 'to': (34.20, 31.14), 'arc': 0.0},
            ],
            'color': '#2B8C5A', 'width': 2.0, 'alpha': 0.5,
            'label': 'MEDICAL EVAC\n108 patients',
            'label_pos': (34.08, 31.16),
            'label_box': False, 'label_size': 4.5,
        },
    ],

    # ── Lines ────────────────────────────────────────────────────────────
    'lines': [
        # Salah al-Din Road — main north–south artery.
        {
            'coords': [
                (34.27, 31.24), (34.30, 31.30), (34.33, 31.35),
                (34.36, 31.40), (34.40, 31.45), (34.44, 31.50),
                (34.48, 31.55),
            ],
            'color': '#666666', 'width': 1.5, 'style': '-', 'alpha': 0.35,
            'label': 'Salah al-Din Rd',
            'label_pos': (34.42, 31.465), 'label_color': '#555555',
            'label_size': 4,
        },
    ],

    # ── Callouts ─────────────────────────────────────────────────────────
    'callouts': [
        {
            'lon': 34.08, 'lat': 31.55, 'text': 'MEDITERRANEAN',
            'size': 8, 'color': '#4A7A9A', 'ha': 'center',
            'subtitle': 'SEA', 'subtitle_size': 7, 'subtitle_offset': 0.035,
        },
        {
            'lon': 34.68, 'lat': 31.50, 'text': 'ISRAEL',
            'size': 10, 'color': '#999999', 'ha': 'center',
        },
        {
            'lon': 34.08, 'lat': 31.12, 'text': 'EGYPT',
            'size': 9, 'color': '#999999', 'ha': 'center',
            'subtitle': 'Sinai Peninsula', 'subtitle_size': 5,
            'subtitle_offset': 0.03,
        },
    ],

    # ── Scale bar ────────────────────────────────────────────────────────
    'scale_bar': {'lon': 34.55, 'lat': 31.10, 'km': 10, 'reference_lat': 31.4},

    # ── Right-side panels ────────────────────────────────────────────────
    'panels': [
        {
            'type': 'bar_chart',
            'rect': [0.61, 0.68, 0.36, 0.26],
            'title': 'DAILY AID TRUCKS ENTERING GAZA',
            'x_label': 'trucks per day',
            'x_max': 750,
            'bars': [
                {'label': 'Agreed rate\n(ceasefire deal)', 'value': 600, 'color': '#2878B0', 'alpha': 0.40},
                {'label': 'Actual average\nOct 2025\u2013Jan 2026', 'value': 255, 'color': '#C03030', 'alpha': 0.75},
                {'label': 'Feb 1\u20137\n(daily average)', 'value': 600, 'color': '#2B8C5A', 'alpha': 0.65},
            ],
            'annotation': {
                'x': 255, 'y': 1.58,
                'text': '57% SHORTFALL FOR 4 MONTHS',
                'size': 6, 'color': '#C03030',
            },
        },
        {
            'type': 'metrics',
            'rect': [0.61, 0.145, 0.36, 0.50],
            'title': 'THE SITUATION ON THE GROUND',
            'rows': [
                {'value': '601',     'description': 'killed since ceasefire began',       'color': '#C03030', 'detail': 'Oct 10, 2025 \u2013 Feb 16, 2026'},
                {'value': '1,605',   'description': 'wounded since ceasefire',             'color': '#C03030', 'detail': 'incl. airstrikes, sniper fire'},
                {'value': '690,000', 'description': 'return movements south \u2192 north', 'color': '#D97520', 'detail': 'of 827,000 total movements'},
                {'value': '1.5 M',   'description': 'people still displaced',              'color': '#D97520', 'detail': 'of 2.4 million total population'},
                {'value': '$17 B',   'description': 'pledged at Board of Peace',           'color': '#6B4FA0', 'detail': 'Feb 19 \u2014 US $10B + 9 nations $7B'},
                {'value': '20,000',  'description': 'troops planned for stabilization',    'color': '#1A6B4A', 'detail': 'Indonesia 8,000 + 4 other nations'},
            ],
            'quotes': {
                'title': 'KEY EVENTS \u2014 PAST MONTH',
                'items': [
                    {
                        'quote': 'Jan 14: Phase Two of ceasefire launched\n  \u2014 demilitarization, governance, reconstruction',
                        'attribution': '\u2014 US Special Envoy Steve Witkoff',
                    },
                    {
                        'quote': 'Jan 26: Body of last hostage recovered\n  from northern Gaza cemetery',
                        'attribution': '\u2014 \u201cThere are no more hostages in Gaza\u201d \u2014 PM Netanyahu',
                    },
                    {
                        'quote': 'Feb 2: Rafah crossing reopens after 21 months\n  \u2014 EU Border Assistance Mission supervising',
                        'attribution': '\u2014 first medical evacuations since May 2024',
                    },
                ],
            },
        },
    ],

    # ── Bottom bar ───────────────────────────────────────────────────────
    'bottom_bar': {
        'rect': [0.0, 0.0, 1.0, 0.125],
        'background': '#F4F3F0',
        'flows': [
            {'category': 'CEASEFIRE',  'color': '#C03030', 'text': 'Phase Two launched Jan 14; 601 killed since Oct truce; 1,193 Israeli violations (GMO count); Hamas disarmament: unresolved'},
            {'category': 'AID',        'color': '#2878B0', 'text': '65 000+ trucks entered (COGAT); only 43% of agreed rate Oct\u2013Jan (UN count); UNRWA blocked since Mar 2025'},
            {'category': 'DISPLACED',  'color': '#D97520', 'text': '690 000 returns south \u2192 north; 1.5M still displaced; 20 000 need medical evacuation; 100 000 children malnourished'},
            {'category': 'GOVERNANCE', 'color': '#6B4FA0', 'text': 'NCAG: 15 technocrats chaired by Dr Ali Shaath; Board of Peace: 25 nations; 2 000 police recruits so far'},
            {'category': 'SECURITY',   'color': '#1A6B4A', 'text': 'ISF: 20 000 troops + 12 000 police planned; Indonesia (8 000), Morocco, Kazakhstan, Kosovo, Albania; deploying first to Rafah'},
        ],
        'legend': {
            'markers': [
                {'shape': 's', 'color': '#C03030', 'label': 'Crisis city'},
                {'shape': 'o', 'color': '#C03030', 'label': 'Displacement / camp'},
                {'shape': 'D', 'color': '#D97520', 'label': 'Major city'},
                {'shape': 'D', 'color': '#2B8C5A', 'label': 'Medical hub'},
                {'shape': '^', 'color': '#2878B0', 'label': 'Border crossing'},
            ],
            'lines': [
                {'style': '-',  'color': '#DAA520', 'width': 2.5, 'label': 'Yellow Line buffer'},
                {'style': '-',  'color': '#666666', 'width': 1.5, 'label': 'Main road'},
                {'style': '--', 'color': '#C03030', 'width': 1.5, 'label': 'Destruction zone'},
                {'style': '-',  'color': '#D97520', 'width': 2.0, 'label': 'Return flow'},
            ],
        },
        'sources': 'Sources: OCHA | Gaza Ministry of Health | COGAT | UNRWA | Board of Peace | Al Jazeera | Reuters | CNN | PBS | NPR',
    },

    # ── Figure-level annotations ─────────────────────────────────────────
    'annotations': [
        {
            'x': 0.30, 'y': 0.14,
            'text': '\u2715 61 million tonnes of rubble \u2014 estimated 20 years to clear (UN)',
            'size': 5.5, 'color': '#8B4513',
        },
    ],

    # ── Output ───────────────────────────────────────────────────────────
    'output': {
        'basename': 'gaza_ceasefire_map',
        'formats': [
            {'ext': 'jpg', 'dpi': 200},
            {'ext': 'pdf', 'dpi': 300},
        ],
    },
}
