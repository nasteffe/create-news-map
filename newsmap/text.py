"""Typography primitives: font resolution, text effects."""

import matplotlib.font_manager as fm
import matplotlib.patheffects as pe

_available = None


def _get_available():
    global _available
    if _available is None:
        _available = {f.name for f in fm.fontManager.ttflist}
    return _available


def pick(preferences, fallback='sans-serif'):
    """Return first available font family from a preference list."""
    available = _get_available()
    for name in preferences:
        if name in available:
            return name
    return fallback


# Resolved font families — computed once at import time.
TITLE = pick(['Big Shoulders Display', 'Oswald', 'Liberation Sans'])
LABEL = pick(['Inter', 'Source Sans Pro', 'Liberation Sans'])
BODY = pick(['Inter', 'Source Sans Pro', 'Liberation Sans'])
MONO = pick(['JetBrains Mono', 'IBM Plex Mono', 'Liberation Mono'], 'monospace')
QUOTE = pick(['Crimson Pro', 'Lora', 'Liberation Serif'], 'serif')

_ROLES = {
    'title': lambda: {'family': TITLE, 'weight': 'bold'},
    'label': lambda: {'family': LABEL, 'weight': 'bold'},
    'body':  lambda: {'family': BODY,  'weight': 'normal'},
    'mono':  lambda: {'family': MONO,  'weight': 'bold'},
    'quote': lambda: {'family': QUOTE, 'style': 'italic'},
}


def font(role, **overrides):
    """Get matplotlib font dict for a named role."""
    d = _ROLES[role]()
    d.update(overrides)
    return d


def halo(width=3.2):
    """White stroke outline for legibility over terrain."""
    return [pe.withStroke(linewidth=width, foreground='white')]
