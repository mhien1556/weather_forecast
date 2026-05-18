from nicegui import ui

from src.common.utils import lucide_to_material

_TAG = 'div'


def render_daily_cards(daily: list):
    with ui.element(_TAG).classes('daily-detail-grid'):
        for i, day in enumerate(daily[:7]):
            with ui.element(_TAG).classes('card detail-forecast-card'):
                with ui.row().classes('detail-header w-full justify-between'):
                    ui.label('Hôm nay' if i == 0 else day['day_name']).classes('day-label').style('font-weight:600')
                    ui.label(day['date']).classes('date-label').style('opacity:0.6')
                with ui.column().classes('detail-body items-center'):
                    ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud'))).style('font-size:64px;color:#4facfe')
                    with ui.row().classes('temp-range'):
                        ui.label(f'{round(day["temp_max"])}°').style('font-weight:700;font-size:2rem')
                        ui.label(f'{round(day["temp_min"])}°').classes('min').style('font-size:2rem;opacity:0.6')
                    ui.label(day['description'].capitalize()).style('opacity:0.8')
                with ui.row().classes('detail-footer w-full justify-around'):
                    with ui.row().classes('footer-stat items-center gap-1'):
                        ui.icon('opacity')
                        ui.label(f'{day["humidity_avg"]}%')
                    with ui.row().classes('footer-stat items-center gap-1'):
                        ui.icon('air')
                        ui.label(f'{day["wind_avg"]} m/s')
