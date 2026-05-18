from nicegui import ui

_TAG = 'div'


def render_stat_card(label: str, value: str, change: str, up: bool):
    with ui.element(_TAG).classes('card stat-card'):
        ui.label(label).classes('stat-label')
        ui.label(value).classes('stat-value')
        ui.label(change).classes('stat-change up' if up else 'stat-change down')
