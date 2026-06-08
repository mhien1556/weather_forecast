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
                refs['main_unit'] = ui.label('').classes('map-location-main-unit')

        with ui.element(_TAG).classes('map-location-details'):
            rows = [('Cảm giác như', 'feels_like'), ('Tốc độ gió', 'wind_speed'), 
                    ('Hướng gió', 'wind_dir'), ('Độ ẩm', 'humidity'), 
                    ('Mây', 'clouds'), ('Áp suất', 'pressure')]
            for label, key in rows:
                with ui.row().classes('map-location-row w-full justify-between'):
                    ui.label(label).classes('map-location-row-label')
                    refs[key] = ui.label('--').classes('map-location-row-value')

    def update(snapshot: dict, lat: float, lon: float, layer_key: str):
        # 1. Lấy đơn vị mới nhất từ storage
        u = get_units() 
        refs['coords'].set_text(f'{lat:.2f}, {lon:.2f}')

        # 2. Xử lý thông số chính (Main)
        if layer_key == 'temp_new':
            val = convert_temp(snapshot.get('temp', 0), u['unit_temp'])
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text('°F' if u['unit_temp'] == 'F' else '°C')
        elif layer_key == 'wind_new':
            val = convert_wind_from_ms(snapshot.get('wind_speed', 0), u['unit_wind'])
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text(u['unit_wind'])
        elif layer_key == 'pressure_new':
            val = convert_pressure(snapshot.get('pressure', 1013), u['unit_pressure'])
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text(u['unit_pressure'])
        else:
            val, unit = main_metric_value(snapshot, layer_key)
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text(unit)

        # 3. Xử lý 6 thông số chi tiết (Đã fix 100% bằng cách gọi hàm convert trực tiếp)
        refs['feels_like'].set_text(f"{convert_temp(snapshot.get('feels_like', 0), u['unit_temp'])} {'°F' if u['unit_temp'] == 'F' else '°C'}")
        refs['wind_speed'].set_text(f"{convert_wind_from_ms(snapshot.get('wind_speed', 0), u['unit_wind'])} {u['unit_wind']}")
        refs['wind_dir'].set_text(str(snapshot.get('wind_dir', '--')))
        refs['humidity'].set_text(f"{snapshot.get('humidity', 0)} %")
        refs['clouds'].set_text(f"{snapshot.get('clouds', 0)} %")
        refs['pressure'].set_text(f"{convert_pressure(snapshot.get('pressure', 1013), u['unit_pressure'])} {u['unit_pressure']}")

        # 4. Cập nhật Icon
        icon = snapshot.get('material_icon', 'wb_sunny')
        tone = _ICON_STYLE.get(icon, 'icon-cloud')
        refs['main_glyph'].content = f'<span class="material-icons map-location-weather-glyph {tone}">{icon}</span>'

    return update
    refs: dict = {}

    with ui.element(_TAG).classes('map-location-card'):
        ui.label('Vị trí đã chọn').classes('map-location-title')
        refs['coords'] = ui.label('—').classes('map-location-coords')

        with ui.element(_TAG).classes('map-location-main'):
            with ui.element(_TAG).classes('map-location-icon-wrap'):
                refs['main_glyph'] = ui.html(_ICON_HTML, sanitize=False)
            with ui.element(_TAG).classes('map-location-metric-wrap'):
                refs['main_value'] = ui.label('--').classes('map-location-main-value')
                refs['main_unit'] = ui.label('').classes('map-location-main-unit')

        with ui.element(_TAG).classes('map-location-details'):
            # Danh sách các thông số chi tiết
            rows = [
                ('Cảm giác như', 'feels_like'), ('Tốc độ gió', 'wind_speed'), 
                ('Hướng gió', 'wind_dir'), ('Độ ẩm', 'humidity'), 
                ('Mây', 'clouds'), ('Áp suất', 'pressure')
            ]
            for label, key in rows:
                with ui.row().classes('map-location-row w-full justify-between'):
                    ui.label(label).classes('map-location-row-label')
                    refs[key] = ui.label('--').classes('map-location-row-value')

    def update(snapshot: dict, lat: float, lon: float, layer_key: str):
        u = get_units()  # Lấy cài đặt đơn vị mới nhất
        refs['coords'].set_text(f'{lat:.2f}, {lon:.2f}')

        # 1. Xử lý thông số chính (nằm ở đầu thẻ)
        if layer_key == 'temp_new':
            val = convert_temp(snapshot.get('temp', 0), u['unit_temp'])
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text('°F' if u['unit_temp'] == 'F' else '°C')
        elif layer_key == 'wind_new':
            val = convert_wind_from_ms(snapshot.get('wind_speed', 0), u['unit_wind'])
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text(u['unit_wind'])
        elif layer_key == 'pressure_new':
            val = convert_pressure(snapshot.get('pressure', 1013), u['unit_pressure'])
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text(u['unit_pressure'])
        else:
            # Nếu là layer khác, hiển thị mặc định
            val, unit = main_metric_value(snapshot, layer_key)
            refs['main_value'].set_text(str(val))
            refs['main_unit'].set_text(unit)

        # 2. Cập nhật các thông số chi tiết dưới bảng
        refs['feels_like'].set_text(f"{convert_temp(snapshot.get('feels_like', 0), u['unit_temp'])} {'°F' if u['unit_temp'] == 'F' else '°C'}")
        refs['wind_speed'].set_text(f"{convert_wind_from_ms(snapshot.get('wind_speed', 0), u['unit_wind'])} {u['unit_wind']}")
        refs['wind_dir'].set_text(str(snapshot.get('wind_dir', '--')))
        refs['humidity'].set_text(f"{snapshot.get('humidity', 0)} %")
        refs['clouds'].set_text(f"{snapshot.get('clouds', 0)} %")
        refs['pressure'].set_text(f"{convert_pressure(snapshot.get('pressure', 1013), u['unit_pressure'])} {u['unit_pressure']}")

        # 3. Cập nhật icon
        icon = snapshot.get('material_icon', 'wb_sunny')
        tone = _ICON_STYLE.get(icon, 'icon-cloud')
        refs['main_glyph'].content = f'<span class="material-icons map-location-weather-glyph {tone}">{icon}</span>'

    return update
    refs: dict = {}

    with ui.element(_TAG).classes('map-location-card'):
        ui.label('Vị trí đã chọn').classes('map-location-title')
        refs['coords'] = ui.label('—').classes('map-location-coords')

        with ui.element(_TAG).classes('map-location-main'):
            with ui.element(_TAG).classes('map-location-icon-wrap'):
                refs['main_glyph'] = ui.html(_ICON_HTML, sanitize=False)
            with ui.element(_TAG).classes('map-location-metric-wrap'):
                refs['main_value'] = ui.label('--').classes('map-location-main-value')
                refs['main_unit'] = ui.label('').classes('map-location-main-unit')

        with ui.element(_TAG).classes('map-location-details'):
            rows = [
                ('Cảm giác như', 'feels_like'),
                ('Tốc độ gió', 'wind_speed'),
                ('Hướng gió', 'wind_dir'),
                ('Độ ẩm', 'humidity'),
                ('Mây', 'clouds'),
                ('Áp suất', 'pressure'),
            ]
            for label, key in rows:
                with ui.row().classes('map-location-row w-full justify-between'):
                    ui.label(label).classes('map-location-row-label')
                    refs[key] = ui.label('--').classes('map-location-row-value')

    def update(snapshot: dict, lat: float, lon: float, layer_key: str):
        refs['coords'].set_text(f'{lat:.2f}, {lon:.2f}')
        u = get_units()

        # Xử lý chỉ số chính (Main Metric)
        if layer_key == 'temp_new':
            refs['main_value'].set_text(str(convert_temp(snapshot.get('temp'), u['unit_temp'])))
            refs['main_unit'].set_text('°F' if u['unit_temp'] == 'F' else '°C')
        elif layer_key == 'wind_new':
            refs['main_value'].set_text(str(convert_wind_from_ms(snapshot.get('wind_speed'), u['unit_wind'])))
            refs['main_unit'].set_text(u['unit_wind'])
        elif layer_key == 'pressure_new':
            refs['main_value'].set_text(str(convert_pressure(snapshot.get('pressure'), u['unit_pressure'])))
            refs['main_unit'].set_text(u['unit_pressure'])
        else:
            val, unit = main_metric_value(snapshot, layer_key)
            refs['main_value'].set_text(val)
            refs['main_unit'].set_text(unit)

        # Cập nhật Icon
        icon = snapshot.get('material_icon', 'wb_sunny')
        tone = _ICON_STYLE.get(icon, 'icon-cloud')
        refs['main_glyph'].content = f'<span class="material-icons map-location-weather-glyph {tone}">{icon}</span>'

        # Cập nhật các thông số chi tiết dưới bảng
        refs['feels_like'].set_text(f"{convert_temp(snapshot['feels_like'], u['unit_temp'])} {'°F' if u['unit_temp'] == 'F' else '°C'}")
        refs['wind_speed'].set_text(f"{convert_wind_from_ms(snapshot['wind_speed'], u['unit_wind'])} {u['unit_wind']}")
        refs['wind_dir'].set_text(str(snapshot['wind_dir']))
        refs['humidity'].set_text(f"{snapshot['humidity']} %")
        refs['clouds'].set_text(f"{snapshot['clouds']} %")
        refs['pressure'].set_text(f"{convert_pressure(snapshot['pressure'], u['unit_pressure'])} {u['unit_pressure']}")

    return update
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