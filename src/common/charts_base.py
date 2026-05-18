"""Cấu hình layout Plotly dùng chung."""

_DEFAULT_MARGIN = dict(l=40, r=20, t=10, b=40)


def chart_layout(**overrides):
    layout = {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': dict(color='rgba(255,255,255,0.6)'),
        'margin': overrides.pop('margin', _DEFAULT_MARGIN),
    }
    layout.update(overrides)
    return layout
