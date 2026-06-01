from nicegui import ui

from .service import main_metric_value
from src.common.units import format_temp, format_wind_from_ms, format_pressure, get_units, convert_temp, convert_wind_from_ms, convert_pressure

_TAG = 'div'

_ICON_HTML = '<span class="material-icons map-location-weather-glyph icon-sunny">wb_sunny</span>'

_ICON_STYLE = {
    'wb_sunny': 'icon-sunny',
    'nights_stay': 'icon-night',
    'water_drop': 'icon-rain',
    'grain': 'icon-rain',
    'cloud': 'icon-cloud',
    'wb_cloudy': 'icon-cloud',
    'thunderstorm': 'icon-storm',
    'ac_unit': 'icon-snow',
    'foggy': 'icon-fog',
}


def create_location_panel():
    refs: dict = {}

    with ui.element(_TAG).classes('map-location-card'):
        ui.label('Vị trí đã chọn').classes('map-location-title')
        refs['coords'] = ui.label('—').classes('map-location-coords')

        with ui.element(_TAG).classes('map-location-main'):
            with ui.element(_TAG).classes('map-location-icon-wrap'):
                refs['main_glyph'] = ui.html(_ICON_HTML, sanitize=False)
            with ui.element(_TAG).classes('map-location-metric-wrap'):
                refs['main_value'] = ui.label('--').classes('map-location-main-value')
                refs['main_unit'] = ui.label('°C').classes('map-location-main-unit')

        with ui.element(_TAG).classes('map-location-details'):
            rows = [
                ('Cảm giác như', 'feels_like', '°C'),
                ('Tốc độ gió', 'wind_speed', 'm/s'),
                ('Hướng gió', 'wind_dir', ''),
                ('Độ ẩm', 'humidity', '%'),
                ('Mây', 'clouds', '%'),
                ('Áp suất', 'pressure', 'hPa'),
            ]
            for label, key, unit in rows:
                with ui.row().classes('map-location-row w-full justify-between'):
                    ui.label(label).classes('map-location-row-label')
                    refs[key] = ui.label('--').classes('map-location-row-value')

    def update(snapshot: dict, lat: float, lon: float, layer_key: str):
        refs['coords'].set_text(f'{lat:.2f}, {lon:.2f}')
        
        # Format metric chính
        if layer_key == 'temp_new':
            u = get_units()['unit_temp']
            refs['main_value'].set_text(str(convert_temp(snapshot.get('temp'), u)))
            refs['main_unit'].set_text('°F' if u == 'F' else '°C')
        elif layer_key == 'wind_new':
            u = get_units()['unit_wind']
            refs['main_value'].set_text(str(convert_wind_from_ms(snapshot.get('wind_speed'), u)))
            refs['main_unit'].set_text(u)
        elif layer_key == 'pressure_new':
            u = get_units()['unit_pressure']
            refs['main_value'].set_text(str(convert_pressure(snapshot.get('pressure'), u)))
            refs['main_unit'].set_text(u)
        else:
            val, unit = main_metric_value(snapshot, layer_key)
            refs['main_value'].set_text(val)
            refs['main_unit'].set_text(unit)

        icon = snapshot.get('material_icon', 'wb_sunny')
        tone = _ICON_STYLE.get(icon, 'icon-cloud')
        refs['main_glyph'].content = (
            f'<span class="material-icons map-location-weather-glyph {tone}">{icon}</span>'
        )
        refs['feels_like'].set_text(format_temp(snapshot['feels_like']))
        refs['wind_speed'].set_text(format_wind_from_ms(snapshot['wind_speed']))
        refs['wind_dir'].set_text(str(snapshot['wind_dir']))
        refs['humidity'].set_text(f"{snapshot['humidity']} %")
        refs['clouds'].set_text(f"{snapshot['clouds']} %")
        refs['pressure'].set_text(format_pressure(snapshot['pressure']))

    return update
