"""Side-panel renderers: bar charts, metrics tables, timelines, quote blocks.

Each panel spec is a dict with a "type" key that selects the renderer.
Panels operate on the figure (not the map axes) via fig.add_axes().
"""

from . import text


def render_panels(fig, spec):
    """Dispatch each panel spec to its renderer."""
    renderers = {
        'bar_chart': _bar_chart,
        'metrics': _metrics,
        'timeline': _timeline,
    }
    for p in spec.get('panels', []):
        fn = renderers.get(p['type'])
        if fn:
            fn(fig, p)


def _bar_chart(fig, p):
    """Horizontal bar chart panel."""
    rect = p['rect']

    # Allocate a title strip above the chart area so the title stays
    # inside the overall panel footprint instead of bleeding upward.
    title_frac = 0.16                       # fraction of rect height for title
    title_h = rect[3] * title_frac
    chart_rect = [rect[0], rect[1], rect[2], rect[3] - title_h]

    ax = fig.add_axes(chart_rect)
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color('#DDDDDD')
        spine.set_linewidth(0.5)

    bars_data = p['bars']
    labels = [b['label'] for b in bars_data]
    values = [b['value'] for b in bars_data]
    colors = [b.get('color', '#2878B0') for b in bars_data]
    alphas = [b.get('alpha', 0.6) for b in bars_data]

    bars = ax.barh(range(len(labels)), values, color=colors, height=0.55,
                   edgecolor='white', linewidth=0.5)
    for bar, a in zip(bars, alphas):
        bar.set_alpha(a)

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=7, **text.font('body'))
    ax.set_xlim(0, p.get('x_max', max(values) * 1.25))
    ax.set_xlabel(p.get('x_label', ''), fontsize=6, color='#666666',
                  **text.font('body'))
    ax.tick_params(axis='x', labelsize=6, colors='#666666')
    ax.invert_yaxis()

    # Value labels on bars.
    for i, v in enumerate(values):
        ax.text(v + 0.15, i, str(v), fontsize=7, va='center',
                color='#333333', clip_on=True, **text.font('mono'))

    # Annotation (optional) — clip to axes.
    ann = p.get('annotation')
    if ann:
        ax.text(ann['x'], ann['y'], ann['text'],
                fontsize=ann.get('size', 6.5),
                color=ann.get('color', '#C03030'),
                ha=ann.get('ha', 'right'), va=ann.get('va', 'top'),
                clip_on=True, **text.font('label'))

    # Title rendered inside the allocated strip above the chart.
    title = p.get('title', '')
    if title:
        fig.text(rect[0], rect[1] + rect[3] - title_h * 0.35,
                 title, fontsize=10, va='center', ha='left',
                 color='#1a1a1a', **text.font('title'))


def _metrics(fig, p):
    """Metrics table + optional quotes block."""
    ax = fig.add_axes(p['rect'])
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color('#DDDDDD')
        spine.set_linewidth(0.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # Title.
    ax.text(0.03, 0.96, p.get('title', ''), fontsize=10,
            color='#1a1a1a', va='top', **text.font('title'))

    # Metric rows.
    y = 0.87
    val_x = p.get('value_x', 0.03)
    desc_x = p.get('desc_x', 0.30)
    for row in p.get('rows', []):
        ax.text(val_x, y, row['value'], fontsize=9,
                color=row.get('color', '#333333'), va='top',
                **text.font('mono'))
        ax.text(desc_x, y, row['description'], fontsize=7,
                color='#333333', va='top', **text.font('body'))
        detail = row.get('detail')
        if detail:
            ax.text(desc_x, y - 0.045, detail, fontsize=5.5,
                    color='#888888', va='top', **text.font('body'))
        y -= p.get('row_spacing', 0.095)

    # Divider line.
    div_y = y + 0.03
    ax.plot([0.03, 0.97], [div_y, div_y], color='#CCCCCC',
            linewidth=0.8, zorder=5)

    # Quotes section (optional).
    quotes = p.get('quotes')
    if quotes:
        y = div_y - 0.04
        ax.text(0.03, y, quotes.get('title', 'VOICES'),
                fontsize=8, color='#1a1a1a', va='top',
                **text.font('label'))
        y -= 0.06
        for q in quotes.get('items', []):
            ax.text(0.05, y, q['quote'], fontsize=6.5, color='#333333',
                    va='top', linespacing=1.3, **text.font('quote'))
            lines = q['quote'].count('\n') + 1
            y -= 0.045 * lines + 0.01
            ax.text(0.05, y, q['attribution'], fontsize=5.5,
                    color='#888888', va='top', **text.font('body'))
            y -= 0.055


def _timeline(fig, p):
    """Vertical timeline panel with dated events.

    Spec shape:
        {
            'type': 'timeline',
            'rect': [x, y, w, h],
            'title': 'KEY EVENTS',
            'events': [
                {'date': 'Jan 11', 'text': 'Dam overflows', 'color': '#C03030'},
                {'date': 'Jan 14', 'text': 'Evacuations begin'},
                ...
            ],
        }
    """
    ax = fig.add_axes(p['rect'])
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color('#DDDDDD')
        spine.set_linewidth(0.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # Title.
    ax.text(0.05, 0.96, p.get('title', 'TIMELINE'), fontsize=10,
            color='#1a1a1a', va='top', **text.font('title'))

    events = p.get('events', [])
    if not events:
        return

    # Layout: vertical line with dots at each event.
    line_x = 0.12
    text_x = 0.18
    n = len(events)
    spacing = p.get('event_spacing', min(0.10, 0.80 / max(n, 1)))
    y = 0.87

    # Draw the vertical spine line.
    y_end = y - (n - 1) * spacing
    ax.plot([line_x, line_x], [y, y_end],
            color='#CCCCCC', linewidth=1.5, zorder=1, solid_capstyle='round')

    for ev in events:
        color = ev.get('color', '#333333')

        # Dot on the timeline.
        ax.plot(line_x, y, 'o', color=color, markersize=5,
                markeredgecolor='white', markeredgewidth=0.5, zorder=3)

        # Date (bold, left of line).
        date = ev.get('date', '')
        ax.text(line_x - 0.02, y, date, fontsize=6.5, color='#666666',
                ha='right', va='center', **text.font('label'))

        # Event text.
        ax.text(text_x, y, ev['text'], fontsize=7, color=color,
                va='center', **text.font('body'))

        # Optional detail line.
        detail = ev.get('detail')
        if detail:
            ax.text(text_x, y - spacing * 0.35, detail, fontsize=5.5,
                    color='#888888', va='center', **text.font('body'))

        y -= spacing
