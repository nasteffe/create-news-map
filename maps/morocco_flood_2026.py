"""Western Mediterranean Deluge: Morocco Flood Crisis 2026-02.

This file is pure data — a dict describing what to draw.
The newsmap package handles how to draw it.
"""

MAP = {

    # ── Metadata ─────────────────────────────────────────────────────────
    'meta': {
        'title': 'WESTERN MEDITERRANEAN DELUGE',
        'subtitle': 'Morocco Flood Crisis \u2014 January/February 2026',
        'tagline': 'Gharb\u2013Loukkos Basins  |  NW Morocco',
    },

    # ── Geography ────────────────────────────────────────────────────────
    'extent': [-7.6, -3.6, 32.6, 37.0],
    'projection': 'PlateCarree',

    'layout': {
        'size': (16.54, 11.69),           # A4 landscape
        'map': [0.01, 0.145, 0.58, 0.80],
    },

    'colors': {
        'ocean':  '#D4E4F0',
        'land':   '#E6DFD4',
        'border': '#8A7A66',
        'coast':  '#8A7A66',
        'river':  '#4A90C4',
    },

    # ── Terrain zones (bottom → top by elevation) ────────────────────────
    # Each zone paints a colour polygon AND feeds the hillshade DEM.
    'hillshade': True,
    'hillshade_alpha': 0.13,
    'hillshade_resolution': 280,
    'hillshade_smooth': 14,

    'terrain_zones': [
        {
            'name': 'Gharb Plain',
            'vertices': [
                (-6.5, 34.0), (-5.6, 34.0), (-5.5, 34.15), (-5.5, 34.5),
                (-5.6, 34.8), (-6.0, 34.85), (-6.4, 34.6), (-6.6, 34.3),
                (-6.5, 34.0),
            ],
            'color': '#EDE8DF', 'alpha': 0.7, 'elevation': 30,
        },
        {
            'name': 'Coastal lowlands (Morocco)',
            'vertices': [
                (-7.6, 33.0), (-7.6, 35.5), (-6.6, 35.5), (-6.3, 35.0),
                (-6.5, 34.6), (-6.6, 34.3), (-6.5, 34.0), (-7.0, 33.5),
                (-7.6, 33.0),
            ],
            'color': '#E2DBD0', 'alpha': 0.25, 'elevation': 80,
        },
        {
            'name': 'Middle Atlas foothills',
            'vertices': [
                (-6.0, 33.8), (-5.5, 33.6), (-4.8, 33.4), (-4.0, 33.2),
                (-3.6, 33.0), (-3.6, 33.6), (-4.0, 34.0), (-4.5, 34.2),
                (-5.0, 34.15), (-5.5, 34.05), (-6.0, 33.95), (-6.0, 33.8),
            ],
            'color': '#C8BCA8', 'alpha': 0.5, 'elevation': 600,
        },
        {
            'name': 'Rif Mountains',
            'vertices': [
                (-5.8, 35.4), (-5.4, 35.5), (-4.8, 35.3), (-4.2, 35.1),
                (-3.8, 34.9), (-3.6, 34.7), (-4.0, 34.6), (-4.5, 34.65),
                (-5.0, 34.75), (-5.5, 35.0), (-5.8, 35.2), (-5.8, 35.4),
            ],
            'color': '#C0B098', 'alpha': 0.6, 'elevation': 1200,
        },
        {
            'name': 'Andalusian highlands',
            'vertices': [
                (-6.0, 36.2), (-5.5, 36.0), (-4.8, 36.3), (-4.0, 36.5),
                (-3.6, 36.8), (-3.6, 37.0), (-4.5, 37.0), (-5.5, 37.0),
                (-6.5, 37.0), (-7.0, 36.8), (-6.5, 36.5), (-6.0, 36.2),
            ],
            'color': '#C8BCA8', 'alpha': 0.45, 'elevation': 800,
        },
    ],

    # ── Rivers ───────────────────────────────────────────────────────────
    'ne_rivers': True,

    'rivers': [
        {
            'name': 'Loukkos',
            'coords': [
                (-5.45, 34.98), (-5.55, 34.92), (-5.62, 34.88),
                (-5.72, 34.78), (-5.78, 34.72), (-5.88, 34.58),
                (-5.95, 34.48), (-6.05, 34.35), (-6.15, 34.25),
            ],
            'width': 2.8,
            'label_pos': (-5.70, 34.65),
            'label_rotation': -55,
        },
        {
            'name': 'Sebou',
            'coords': [
                (-4.3, 34.08), (-4.5, 34.04), (-4.7, 34.0),
                (-4.9, 34.01), (-5.1, 34.02), (-5.3, 34.06),
                (-5.4, 34.10), (-5.55, 34.14), (-5.7, 34.18),
                (-5.9, 34.22), (-6.1, 34.24), (-6.3, 34.26),
                (-6.55, 34.28),
            ],
            'width': 3.2,
            'label_pos': (-5.15, 34.14),
            'label_rotation': -5,
        },
    ],

    # ── Analytical overlays ──────────────────────────────────────────────

    # Flood extent zone.
    'zones': [
        {
            'vertices': [
                (-6.55, 33.98), (-6.15, 34.0), (-5.75, 34.15),
                (-5.65, 34.6), (-5.7, 34.75), (-6.0, 34.8),
                (-6.4, 34.5), (-6.55, 33.98),
            ],
            'fill': '#C03030', 'fill_alpha': 0.12,
            'edge': '#C03030', 'edge_alpha': 0.6,
            'label': 'FLOOD EXTENT',
            'label_pos': (-6.05, 34.42),
            'label_border': '#B03030',
        },
    ],

    # Submerged farmland hatching.
    'scatter_marks': [
        {
            'bounds': (-6.45, -5.8, 34.05, 34.65),
            'n': 20, 'marker': 'x', 'color': '#7A5230',
            'alpha': 0.35, 'seed': 42,
        },
    ],

    # Point markers: dams, crisis cities, camps, context cities.
    'markers': [
        # Dams (triangle, blue).
        {
            'lon': -5.6, 'lat': 34.95, 'shape': '^', 'size': 10,
            'color': '#2878B0', 'name': 'Oued El Makhazine',
            'name_size': 5.5, 'name_offset': (0.12, 0.0), 'name_va': 'center',
            'annotation': '146% capacity', 'ann_color': '#C03030',
            'ann_size': 5, 'ann_offset': (0.12, -0.06),
        },
        {
            'lon': -5.05, 'lat': 34.45, 'shape': '^', 'size': 10,
            'color': '#2878B0', 'name': 'Al Wahda',
            'name_size': 5.5, 'name_offset': (0.12, 0.0), 'name_va': 'center',
            'annotation': 'critical threshold', 'ann_color': '#C03030',
            'ann_size': 5, 'ann_offset': (0.12, -0.06),
        },
        # Crisis cities (square, red).
        {
            'lon': -5.90, 'lat': 34.98, 'shape': 's', 'size': 7,
            'color': '#C03030', 'name': 'Ksar El Kebir',
            'annotation': '85% evacuated\n~50 000 displaced',
        },
        {
            'lon': -5.71, 'lat': 34.22, 'shape': 's', 'size': 7,
            'color': '#C03030', 'name': 'Sidi Kacem',
            'annotation': 'villages submerged',
        },
        {
            'lon': -5.93, 'lat': 34.26, 'shape': 's', 'size': 7,
            'color': '#C03030', 'name': 'Sidi Slimane',
            'annotation': 'partially submerged',
        },
        # Displacement camp (triangle, gold).
        {
            'lon': -6.58, 'lat': 34.26, 'shape': '^', 'size': 9,
            'color': '#CC9900', 'name': 'Kenitra',
            'name_size': 7, 'name_offset': (-0.14, 0.10), 'name_ha': 'center',
            'annotation': '40 000 in camps\n3 000 families',
            'ann_color': '#CC9900', 'ann_size': 4.8,
            'ann_offset': (-0.14, -0.04), 'ann_ha': 'center',
        },
        # Provincial hub (diamond, orange).
        {
            'lon': -6.15, 'lat': 35.19, 'shape': 'D', 'size': 8,
            'color': '#D97520', 'name': 'Larache',
            'name_size': 7, 'name_offset': (0.12, 0.0), 'name_va': 'center',
            'annotation': '81 700 evacuated',
            'ann_color': '#D97520', 'ann_size': 4.8,
            'ann_offset': (0.12, -0.07),
        },
        # Context cities (circle, grey).
        {
            'lon': -5.80, 'lat': 35.77, 'shape': 'o', 'size': 6,
            'color': '#666666', 'name': 'Tangier', 'name_color': '#333333',
            'annotation': '1 500 mm since Sep 2025',
            'ann_color': '#666666', 'ann_size': 4.5,
        },
        {
            'lon': -5.37, 'lat': 35.57, 'shape': 'o', 'size': 6,
            'color': '#666666', 'name': 'Tetouan', 'name_color': '#333333',
            'annotation': 'flash flood: 4 dead',
            'ann_color': '#666666', 'ann_size': 4.5,
        },
        {
            'lon': -6.83, 'lat': 33.97, 'shape': 'o', 'size': 6,
            'color': '#666666', 'name': 'Rabat', 'name_color': '#333333',
        },
    ],

    # Displacement + dam-release arrows.
    'arrow_groups': [
        {
            'arrows': [
                {'from': (-5.95, 34.85), 'to': (-6.52, 34.35), 'arc': 0.2},
                {'from': (-5.82, 34.25), 'to': (-6.52, 34.3),  'arc': -0.1},
                {'from': (-6.12, 35.1),  'to': (-6.52, 34.38), 'arc': 0.2},
            ],
            'color': '#D97520', 'width': 2.5, 'alpha': 0.55,
            'label': 'DISPLACEMENT', 'label_pos': (-6.10, 34.62),
        },
        {
            'arrows': [
                {'from': (-5.6, 34.90), 'to': (-5.78, 34.68), 'arc': 0.15},
            ],
            'color': '#2878B0', 'width': 2.0, 'alpha': 1.0,
            'label': 'releases\n560 m\u00b3/s', 'label_pos': (-5.78, 34.80),
            'label_box': False, 'label_size': 4.5,
        },
    ],

    # Supply chain disruption line.
    'lines': [
        {
            'coords': [(-6.2, 35.15), (-5.9, 35.4), (-5.6, 35.83)],
            'color': '#7B3FA0', 'width': 2.0, 'style': '--', 'alpha': 0.5,
            'end_marker': {'shape': 'X', 'size': 14, 'color': '#C03030'},
            'label': 'SUPPLY CHAIN\nDISRUPTED',
            'label_pos': (-5.15, 35.85), 'label_color': '#7B3FA0',
        },
    ],

    # Region callouts.
    'callouts': [
        {
            'lon': -5.3, 'lat': 36.65, 'text': 'ANDALUSIA',
            'size': 9, 'color': '#C03030',
            'subtitle': '40 000 ha | 80% olive crop lost | EUR 3.5 bn',
            'subtitle_offset': 0.17, 'subtitle_size': 5,
        },
    ],

    # ── Scale bar ────────────────────────────────────────────────────────
    'scale_bar': {'lon': -7.3, 'lat': 32.85, 'km': 100, 'reference_lat': 34.0},

    # ── Right-side panels ────────────────────────────────────────────────
    'panels': [
        {
            'type': 'bar_chart',
            'rect': [0.61, 0.68, 0.36, 0.26],
            'title': 'WATER INFLOW TO MOROCCAN DAMS',
            'x_label': 'billions of cubic metres',
            'x_max': 11,
            'bars': [
                {'label': '2024\n(full year)',               'value': 4.5,  'color': '#2878B0', 'alpha': 0.45},
                {'label': '2025\n(full year)',               'value': 4.5,  'color': '#2878B0', 'alpha': 0.45},
                {'label': '2026-01-11 to\n2026-02-11',      'value': 8.82, 'color': '#C03030', 'alpha': 0.75},
            ],
            'annotation': {
                'x': 8.82, 'y': 2.42,
                'text': 'ONE MONTH = TWO YEARS',
                'size': 6.5, 'color': '#C03030',
            },
        },
        {
            'type': 'metrics',
            'rect': [0.61, 0.145, 0.36, 0.50],
            'title': 'THE HUMAN COST',
            'rows': [
                {'value': '188 000',   'description': 'persons displaced',          'color': '#D97520', 'detail': 'across 4 provinces'},
                {'value': '40 000',    'description': 'in tent camps near Kenitra',  'color': '#CC9900', 'detail': 'blue tents | livestock separated'},
                {'value': '4',         'description': 'confirmed dead',              'color': '#C03030', 'detail': 'incl. 2-year-old | 1 missing'},
                {'value': '110 000+',  'description': 'hectares submerged',          'color': '#7A5230', 'detail': 'cereal | sugar beet | citrus'},
                {'value': '$328 M',    'description': 'government relief package',   'color': '#2878B0', 'detail': '~10% earmarked for farmers'},
                {'value': 'CHF 1.6 M', 'description': 'IFRC emergency appeal',      'color': '#2878B0', 'detail': 'Red Crescent operations'},
            ],
            'quotes': {
                'title': 'VOICES FROM THE CAMPS',
                'items': [
                    {
                        'quote': '\u201cThe water took everything.\u201d',
                        'attribution': '\u2014 Ibrahim Bernous, 32, camp near Kenitra',
                    },
                    {
                        'quote': '\u201cWe have no grain left to feed our livestock,\n  and they are our main source of income.\u201d',
                        'attribution': '\u2014 Chergui al-Alja, 42',
                    },
                    {
                        'quote': '\u201cAll of it is gone now. Still, praise be to\n  God for this blessing.\u201d',
                        'attribution': '\u2014 Mohamed Reouani, 63, Ouled Salama',
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
            {'category': 'WATER',  'color': '#2878B0', 'text': '8.82 \u00d7 10\u2079 m\u00b3 inflow in one month \u2248 2 years combined on drought-degraded soils: max runoff, min infiltration'},
            {'category': 'SOIL',   'color': '#7A5230', 'text': '110 000+ ha waterlogged: topsoil stripping, salinization risk in coastal lowlands; restoration: months to years'},
            {'category': 'AGRI',   'color': '#8B6914', 'text': '7-year drought depleted reserves; flood destroyed current + next season capacity; price spike cycle repeats'},
            {'category': 'TRADE',  'color': '#7B3FA0', 'text': 'Spain + Morocco = 58% UK tomatoes, 72% cucumbers, 75% sweet peppers in winter; Strait transport disrupted'},
            {'category': 'PEOPLE', 'color': '#D97520', 'text': '188 000 displaced (rainfed smallholders + pastoralists): structural vulnerability to next drought\u2013deluge cycle'},
        ],
        'legend': {
            'markers': [
                {'shape': 's', 'color': '#C03030', 'label': 'Crisis city'},
                {'shape': '^', 'color': '#CC9900', 'label': 'Displacement camp'},
                {'shape': 'D', 'color': '#D97520', 'label': 'Provincial hub'},
                {'shape': 'o', 'color': '#666666', 'label': 'Context city'},
                {'shape': '^', 'color': '#2878B0', 'label': 'Dam'},
            ],
            'lines': [
                {'style': '--', 'color': '#C03030', 'width': 1.5, 'label': 'Flood extent'},
                {'style': '-',  'color': '#4A90C4', 'width': 2.0, 'label': 'River'},
                {'style': '--', 'color': '#7B3FA0', 'width': 1.5, 'label': 'Supply chain disruption'},
                {'style': '-',  'color': '#D97520', 'width': 2.0, 'label': 'Displacement flow'},
            ],
        },
        'sources': 'Sources: IFRC | Moroccan Interior Ministry | COAG Andalusia | AFP | ESA/Copernicus | ReliefWeb | Met Office',
    },

    # ── Figure-level annotations ─────────────────────────────────────────
    'annotations': [
        {
            'x': 0.30, 'y': 0.14,
            'text': '\u2715 110 000+ ha submerged farmland: cereal, sugar beet, citrus',
            'size': 5.5, 'color': '#7A5230',
        },
    ],

    # ── Output ───────────────────────────────────────────────────────────
    'output': {
        'basename': 'morocco_crisis_map',
        'formats': [
            {'ext': 'jpg', 'dpi': 200},
            {'ext': 'pdf', 'dpi': 300},
        ],
    },
}
