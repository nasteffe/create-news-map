"""Los Angeles Firestorm: Palisades & Eaton Fires 2025-01.

This file is pure data — a dict describing what to draw.
The newsmap package handles how to draw it.
"""

MAP = {

    # ── Metadata ─────────────────────────────────────────────────────────
    'meta': {
        'title': 'LOS ANGELES FIRESTORM',
        'subtitle': 'Palisades & Eaton Fires \u2014 January 2025',
        'tagline': 'Greater Los Angeles  |  Southern California',
    },

    # ── Geography ────────────────────────────────────────────────────────
    'extent': [-118.80, -117.95, 33.90, 34.40],
    'projection': 'PlateCarree',

    'layout': {
        'size': (16.54, 11.69),           # A3 landscape
        'map': [0.01, 0.15, 0.58, 0.80],
    },

    'colors': {
        'ocean':  '#C8DDE8',
        'land':   '#E8E2D8',
        'border': '#999999',
        'coast':  '#8A9AA6',
        'river':  '#7AAAC4',
    },

    # ── Terrain ──────────────────────────────────────────────────────────
    'hillshade': True,
    'hillshade_alpha': 0.15,
    'hillshade_resolution': 280,
    'hillshade_smooth': 12,

    'terrain_zones': [
        {
            'name': 'LA Basin',
            'vertices': [
                (-118.70, 33.90), (-118.70, 34.05), (-118.50, 34.05),
                (-118.30, 34.05), (-118.10, 34.10), (-117.95, 34.05),
                (-117.95, 33.90), (-118.70, 33.90),
            ],
            'color': '#E8E2D8', 'alpha': 0.25, 'elevation': 50,
        },
        {
            'name': 'San Fernando Valley',
            'vertices': [
                (-118.65, 34.14), (-118.35, 34.14), (-118.20, 34.17),
                (-118.20, 34.28), (-118.35, 34.30), (-118.55, 34.30),
                (-118.65, 34.25), (-118.65, 34.14),
            ],
            'color': '#DDD8CC', 'alpha': 0.35, 'elevation': 220,
        },
        {
            'name': 'Santa Monica Mountains',
            'vertices': [
                (-118.75, 34.02), (-118.60, 34.03), (-118.45, 34.06),
                (-118.35, 34.10), (-118.30, 34.13), (-118.35, 34.16),
                (-118.50, 34.13), (-118.65, 34.11), (-118.75, 34.07),
                (-118.75, 34.02),
            ],
            'color': '#C8BCA8', 'alpha': 0.45, 'elevation': 600,
        },
        {
            'name': 'San Gabriel Mountains',
            'vertices': [
                (-118.35, 34.24), (-118.15, 34.22), (-117.95, 34.22),
                (-117.95, 34.40), (-118.15, 34.40), (-118.35, 34.40),
                (-118.50, 34.35), (-118.35, 34.24),
            ],
            'color': '#B8A898', 'alpha': 0.50, 'elevation': 1800,
        },
    ],

    # ── Fire perimeters ──────────────────────────────────────────────────
    'zones': [
        {
            'vertices': [
                (-118.55, 34.04), (-118.52, 34.03), (-118.49, 34.03),
                (-118.47, 34.05), (-118.47, 34.08), (-118.50, 34.10),
                (-118.56, 34.10), (-118.58, 34.07), (-118.55, 34.04),
            ],
            'fill': '#FF4500', 'fill_alpha': 0.22,
            'edge': '#FF4500', 'edge_alpha': 0.75,
            'label': 'PALISADES FIRE',
            'label_pos': (-118.535, 34.06),
            'label_border': '#FF4500',
        },
        {
            'vertices': [
                (-118.18, 34.17), (-118.14, 34.16), (-118.08, 34.18),
                (-118.06, 34.21), (-118.08, 34.25), (-118.14, 34.26),
                (-118.18, 34.24), (-118.20, 34.21), (-118.18, 34.17),
            ],
            'fill': '#FF4500', 'fill_alpha': 0.22,
            'edge': '#FF4500', 'edge_alpha': 0.75,
            'label': 'EATON FIRE',
            'label_pos': (-118.13, 34.21),
            'label_border': '#FF4500',
        },
    ],

    # ── Scatter: destroyed structures ────────────────────────────────────
    'scatter_marks': [
        {
            'bounds': (-118.56, -118.48, 34.04, 34.09),
            'n': 25, 'marker': 'x', 'color': '#8B0000',
            'alpha': 0.30, 'seed': 42,
        },
        {
            'bounds': (-118.18, -118.07, 34.17, 34.24),
            'n': 20, 'marker': 'x', 'color': '#8B0000',
            'alpha': 0.30, 'seed': 43,
        },
    ],

    # ── Point markers ────────────────────────────────────────────────────
    'markers': [
        # Major fire communities (square, fire-orange).
        {
            'lon': -118.53, 'lat': 34.04, 'shape': 's', 'size': 7,
            'color': '#FF4500', 'name': 'Pacific Palisades',
            'name_offset': (-0.03, 0.02), 'name_ha': 'right',
            'annotation': '23 448 acres | ~5 300 structures',
            'ann_color': '#FF4500', 'ann_size': 4.5,
            'ann_offset': (-0.03, -0.01), 'ann_ha': 'right',
        },
        {
            'lon': -118.13, 'lat': 34.19, 'shape': 's', 'size': 7,
            'color': '#FF4500', 'name': 'Altadena',
            'name_offset': (0.03, 0.01), 'name_va': 'center',
            'annotation': '14 117 acres | ~7 000 structures',
            'ann_color': '#FF4500', 'ann_size': 4.5,
            'ann_offset': (0.03, -0.01),
        },
        # Secondary fires (triangle, orange).
        {
            'lon': -118.47, 'lat': 34.31, 'shape': '^', 'size': 7,
            'color': '#D4760A', 'name': 'Hurst Fire',
            'name_size': 5.5, 'name_offset': (0.03, 0.0), 'name_va': 'center',
            'annotation': '799 acres', 'ann_size': 4.5,
            'ann_offset': (0.03, -0.015),
        },
        {
            'lon': -118.64, 'lat': 34.21, 'shape': '^', 'size': 7,
            'color': '#D4760A', 'name': 'Kenneth Fire',
            'name_size': 5.5, 'name_offset': (-0.03, 0.0),
            'name_ha': 'right', 'name_va': 'center',
            'annotation': '1 052 acres', 'ann_size': 4.5,
            'ann_offset': (-0.03, -0.015), 'ann_ha': 'right',
        },
        # Context cities (circle, grey).
        {
            'lon': -118.24, 'lat': 34.05, 'shape': 'o', 'size': 7,
            'color': '#666666', 'name': 'Downtown LA', 'name_color': '#333333',
            'name_size': 6, 'name_offset': (0.03, 0.0), 'name_va': 'center',
        },
        {
            'lon': -118.49, 'lat': 34.02, 'shape': 'o', 'size': 5,
            'color': '#666666', 'name': 'Santa Monica', 'name_color': '#555555',
            'name_size': 5, 'name_offset': (0.02, 0.0), 'name_va': 'center',
        },
        {
            'lon': -118.14, 'lat': 34.15, 'shape': 'o', 'size': 5,
            'color': '#666666', 'name': 'Pasadena', 'name_color': '#555555',
            'name_size': 5.5, 'name_offset': (0.03, 0.0), 'name_va': 'center',
        },
        {
            'lon': -118.35, 'lat': 34.18, 'shape': 'o', 'size': 5,
            'color': '#666666', 'name': 'Burbank', 'name_color': '#555555',
            'name_size': 5, 'name_offset': (0.0, 0.015),
        },
        {
            'lon': -118.41, 'lat': 33.94, 'shape': 'o', 'size': 4,
            'color': '#999999', 'name': 'LAX', 'name_color': '#666666',
            'name_size': 5, 'name_offset': (0.02, 0.0), 'name_va': 'center',
        },
        {
            'lon': -118.69, 'lat': 34.03, 'shape': 'o', 'size': 4,
            'color': '#999999', 'name': 'Malibu', 'name_color': '#666666',
            'name_size': 5, 'name_offset': (0.0, -0.015),
        },
        {
            'lon': -118.19, 'lat': 33.93, 'shape': 'o', 'size': 4,
            'color': '#999999', 'name': 'Long Beach', 'name_color': '#666666',
            'name_size': 5, 'name_offset': (0.0, -0.015),
        },
    ],

    # ── Wind arrows (Santa Ana: NE to SW) ────────────────────────────────
    'arrow_groups': [
        {
            'arrows': [
                {'from': (-118.30, 34.35), 'to': (-118.50, 34.12), 'arc': 0.05},
                {'from': (-117.98, 34.32), 'to': (-118.12, 34.22), 'arc': -0.05},
                {'from': (-118.15, 34.38), 'to': (-118.30, 34.18), 'arc': 0.05},
            ],
            'color': '#D4760A', 'width': 2.5, 'alpha': 0.45,
            'label': 'SANTA ANA WINDS\n60\u2013100+ mph gusts',
            'label_pos': (-118.10, 34.37),
            'label_size': 5,
        },
    ],

    # ── Freeways ─────────────────────────────────────────────────────────
    'lines': [
        # I-405 (north-south through west LA).
        {
            'coords': [
                (-118.47, 33.93), (-118.47, 34.00), (-118.48, 34.05),
                (-118.49, 34.10), (-118.49, 34.16),
            ],
            'color': '#888888', 'width': 1.2, 'style': '-', 'alpha': 0.40,
            'label': 'I-405', 'label_pos': (-118.44, 33.95),
            'label_color': '#888888', 'label_size': 4.5,
        },
        # I-210 (Foothill Fwy, past Eaton fire).
        {
            'coords': [
                (-118.28, 34.18), (-118.21, 34.17), (-118.14, 34.15),
                (-118.06, 34.14), (-117.98, 34.13),
            ],
            'color': '#888888', 'width': 1.2, 'style': '-', 'alpha': 0.40,
            'label': 'I-210', 'label_pos': (-118.01, 34.12),
            'label_color': '#888888', 'label_size': 4.5,
        },
        # I-10 (east-west, southern LA).
        {
            'coords': [
                (-118.49, 34.01), (-118.35, 34.03), (-118.24, 34.04),
                (-118.10, 34.07), (-117.98, 34.06),
            ],
            'color': '#888888', 'width': 1.0, 'style': '-', 'alpha': 0.30,
            'label': 'I-10', 'label_pos': (-118.01, 34.05),
            'label_color': '#888888', 'label_size': 4,
        },
    ],

    # ── Callouts ─────────────────────────────────────────────────────────
    'callouts': [
        {
            'lon': -118.55, 'lat': 34.13, 'text': 'SANTA MONICA\nMOUNTAINS',
            'size': 5.5, 'color': '#9A8A70', 'ha': 'center',
        },
        {
            'lon': -118.25, 'lat': 34.34, 'text': 'SAN GABRIEL MOUNTAINS',
            'size': 6, 'color': '#9A8A70', 'ha': 'center',
        },
        {
            'lon': -118.45, 'lat': 34.22, 'text': 'SAN FERNANDO\nVALLEY',
            'size': 5.5, 'color': '#9A8A70', 'ha': 'center',
        },
    ],

    # ── Inset: California context ────────────────────────────────────────
    'inset': {
        'rect': [0.37, 0.15, 0.22, 0.19],
        'extent': [-125, -114, 32, 42],
        'labels': [
            {'lon': -120.0, 'lat': 37.0, 'text': 'CALIFORNIA', 'size': 5, 'color': '#555555'},
            {'lon': -117.0, 'lat': 38.5, 'text': 'NEVADA', 'size': 4, 'color': '#777777'},
            {'lon': -123.0, 'lat': 37.5, 'text': 'PACIFIC\nOCEAN', 'size': 3.5, 'color': '#6A8DA8', 'ha': 'center'},
        ],
    },

    # ── Scale bar ────────────────────────────────────────────────────────
    'scale_bar': {'lon': -118.75, 'lat': 33.93, 'km': 10, 'reference_lat': 34.15},

    # ── Right-side panels ────────────────────────────────────────────────
    'panels': [
        {
            'type': 'bar_chart',
            'rect': [0.62, 0.74, 0.35, 0.20],
            'title': 'CALIFORNIA WILDFIRE INSURED LOSSES',
            'x_label': 'billions USD (estimated)',
            'x_max': 50,
            'bars': [
                {'label': '2017 Wine\nCountry',  'value': 13,   'color': '#D4760A', 'alpha': 0.45},
                {'label': '2018 Camp+\nWoolsey',  'value': 12.5, 'color': '#D4760A', 'alpha': 0.45},
                {'label': '2025 LA\nFirestorm',   'value': 40,   'color': '#C03030', 'alpha': 0.75},
            ],
            'annotation': {
                'x': 40, 'y': 2.42,
                'text': 'COSTLIEST US WILDFIRE EVENT',
                'size': 6, 'color': '#C03030',
            },
        },
        {
            'type': 'metrics',
            'rect': [0.62, 0.40, 0.35, 0.32],
            'title': 'IMPACT SUMMARY',
            'row_spacing': 0.085,
            'rows': [
                {'value': '29+',      'description': 'confirmed dead',           'color': '#C03030', 'detail': 'Palisades + Eaton fires'},
                {'value': '12 000+',  'description': 'structures destroyed',     'color': '#FF4500', 'detail': '~5 300 Palisades | ~7 000 Eaton'},
                {'value': '180 000',  'description': 'evacuated at peak',        'color': '#D97520', 'detail': 'mandatory + voluntary evacuation zones'},
                {'value': '37 500',   'description': 'acres burned (combined)',   'color': '#8B4513', 'detail': 'Palisades 23 448 | Eaton 14 117'},
                {'value': '$250 B+',  'description': 'estimated total damages',  'color': '#C03030', 'detail': 'insured losses alone: ~$40 B'},
                {'value': '100+ mph', 'description': 'peak Santa Ana gusts',     'color': '#D4760A', 'detail': 'relative humidity below 10%'},
            ],
            'quotes': {
                'title': 'VOICES FROM THE FIRE',
                'items': [
                    {
                        'quote': '\u201cWe came back to nothing.\n  Just the chimney was left.\u201d',
                        'attribution': '\u2014 Palisades homeowner, Jan 9',
                    },
                    {
                        'quote': '\u201cThe hydrants just stopped.\n  We had nothing to fight it with.\u201d',
                        'attribution': '\u2014 LAFD firefighter, Palisades',
                    },
                ],
            },
        },
        {
            'type': 'timeline',
            'rect': [0.62, 0.15, 0.35, 0.23],
            'title': 'FIRE CHRONOLOGY',
            'events': [
                {'date': 'Jan 7 AM', 'text': 'Palisades Fire ignites; rapid spread',        'color': '#FF4500'},
                {'date': 'Jan 7 PM', 'text': 'Eaton Fire erupts near Altadena',              'color': '#FF4500'},
                {'date': 'Jan 8',    'text': 'Hurst Fire; 80 000 under evacuation',          'color': '#D97520'},
                {'date': 'Jan 9',    'text': 'Palisades fire jumps I-405; 0% contained',     'color': '#C03030'},
                {'date': 'Jan 10',   'text': 'Kenneth Fire; death toll surpasses 10',         'color': '#C03030'},
                {'date': 'Jan 12',   'text': '150 000+ evacuated; 10 000+ structures gone',   'color': '#D97520'},
                {'date': 'Jan 14',   'text': 'Winds ease; first containment progress',       'color': '#2878B0'},
            ],
        },
    ],

    # ── Bottom bar ───────────────────────────────────────────────────────
    'bottom_bar': {
        'rect': [0.0, 0.0, 1.0, 0.14],
        'background': '#F4F3F0',
        'flow_spacing': 0.17,
        'flows': [
            {'category': 'FIRE',   'color': '#FF4500', 'text': 'Santa Ana winds (NE\u2192SW) + 8 months without rain + dense WUI vegetation = fire conditions beyond suppression capacity'},
            {'category': 'WATER',  'color': '#2878B0', 'text': 'Hydrants ran dry in Palisades; DWP pressure collapsed under simultaneous demand; Eaton reservoir offline during critical hours'},
            {'category': 'HOUSE',  'color': '#D97520', 'text': '12 000+ structures lost in America\u2019s most expensive metro; median Palisades home $3.5 M; rebuilding timeline: 3\u20135 years'},
            {'category': 'INSURE', 'color': '#8B4513', 'text': 'State Farm cancelled 72 000 CA policies in 2024; FAIR Plan (insurer of last resort) $6 B+ exposed; coverage gap widens'},
            {'category': 'CLIM.',  'color': '#C03030', 'text': 'Drought \u2192 record rain \u2192 explosive growth \u2192 drought \u2192 fire: accelerating cycle; 2025 losses exceed all prior CA wildfire years combined'},
        ],
        'legend': {
            'y': 0.82,
            'markers': [
                {'shape': 's', 'color': '#FF4500', 'label': 'Major fire community'},
                {'shape': '^', 'color': '#D4760A', 'label': 'Secondary fire'},
                {'shape': 'o', 'color': '#666666', 'label': 'City / landmark'},
            ],
            'lines': [
                {'style': '--', 'color': '#FF4500', 'width': 1.5, 'label': 'Fire perimeter'},
                {'style': '-',  'color': '#888888', 'width': 1.0, 'label': 'Freeway'},
                {'style': '-',  'color': '#D4760A', 'width': 2.0, 'label': 'Wind direction'},
            ],
        },
        'sources': 'Sources: CAL FIRE | LAFD | NOAA/NWS | CoreLogic | CA Dept of Insurance | FEMA | Reuters | AP',
    },

    # ── Output ───────────────────────────────────────────────────────────
    'output': {
        'basename': 'la_firestorm_map',
        'formats': [
            {'ext': 'jpg', 'dpi': 200},
            {'ext': 'pdf', 'dpi': 300},
        ],
    },
}
