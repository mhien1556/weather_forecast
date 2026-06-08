from nicegui import ui
from datetime import datetime

from src.common.components import metric_card, plotly_chart
from src.common.config import API_KEY, get_current_user
from src.common.units import (
    format_pressure,
    format_temp,
    format_visibility,
    format_wind_from_ms,
)
from src.common.utils import lucide_to_material, get_weather_color
from src.database.user_store import get_favorites, add_favorite, remove_favorite


def render_hero(weather: dict):
    city_name = weather.get('city_name', 'N/A')
    user = get_current_user()
    w_color = get_weather_color(weather.get('icon'))

    with ui.element('div').classes('hero-section'):
        with ui.element('div').classes('location-info'):
            with ui.element('div').classes('location-header flex items-center gap-2'):
                ui.icon('place').style('color:var(--accent-color);font-size:24px')
                ui.label(city_name).style('font-size:2.5rem;font-weight:700')

                if user:
                    uname = user['username']
                    favs = get_favorites(uname)
                    is_fav = city_name in favs

                    def toggle_favorite(btn, city=city_name, username=uname):
                        current_favs = get_favorites(username)
                        if city in current_favs:
                            remove_favorite(username, city)
                            btn.props('icon=favorite_border')
                            ui.notify(f'Đã xóa {city} khỏi danh sách yêu thích', type='info')
                        else:
                            add_favorite(username, city)
                            btn.props('icon=favorite')
                            ui.notify(f'Đã thêm {city} vào danh sách yêu thích!', type='positive')

                    icon_type = 'favorite' if is_fav else 'favorite_border'
                    fav_btn = ui.button(on_click=lambda: toggle_favorite(fav_btn)).props(f'flat round icon={icon_type}').style('color:#f87171; font-size: 1.5rem;')

            ui.label(weather.get('date_str', '')).classes('date-time')

        with ui.element('div').classes('current-temp-large'):
            with ui.element('div').classes('temp-row flex items-center gap-4'):
                # ✅ ĐÃ SỬA: Đổi icon mặc định thành 'sunny' thay vì 'cloud'
                ui.icon(lucide_to_material(weather.get('lucide_icon', 'sunny'))).style(f'font-size:80px;color:{w_color}')
                ui.label(format_temp(weather.get('temp'))).classes('temp-value')
            with ui.element('div').classes('condition-info flex items-center gap-1'):
                ui.label(weather.get('desc', ''))
                ui.label(' • ').classes('opacity-50')
                ui.label(f'Cảm giác như {format_temp(weather.get("feels_like"))}')


def render_metrics(weather: dict):
    with ui.element('div').classes('metrics-grid'):
        # ✅ ĐÃ SỬA: Các icon hiển thị trực quan hơn
        metric_card('water_drop', 'Độ ẩm', f'{weather.get("humidity", "--")}%')
        metric_card('air', 'Gió', format_wind_from_ms(weather.get('wind')))
        metric_card('compress', 'Áp suất', format_pressure(weather.get('pressure')))
        metric_card('remove_red_eye', 'Tầm nhìn', format_visibility(weather.get('visibility')))
        metric_card('device_thermostat', 'Điểm sương', format_temp(weather.get('dew_point')))
        metric_card('wb_twilight', 'Bình minh', weather.get('sunrise', '--'))
        metric_card('wb_sunny', 'Hoàng hôn', weather.get('sunset', '--'))
        uv = weather.get('uv_index')
        metric_card('filter_drama', 'Chỉ số UV', str(uv if uv is not None else '0'))


def render_aqi_card(aqi: dict):
    color = aqi.get('color', '#4ade80')
    with ui.element('div').classes('card bg-black/30 backdrop-blur-md rounded-2xl border border-white/20 p-5 shadow-lg w-full').style('height: 100%; overflow-y: auto;'):
        with ui.row().classes('items-center gap-2 mb-4'):
            ui.icon('air', size='20px').classes('text-green-400')
            ui.label('Chất lượng không khí').classes('font-semibold m-0')

        with ui.element('div').classes('flex flex-col gap-4'):
            with ui.row().classes('items-center gap-4'):
                circle = ui.element('div').classes('w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold border-4')
                circle.style(f'border-color:{color}; color:{color}')
                with circle:
                    ui.label(str(aqi.get('val', '--')))
                with ui.column():
                    ui.label(aqi.get('label', 'Tốt')).classes('font-bold').style(f'color:{color}')
                    ui.label(aqi.get('desc', 'Không khí trong lành.')).classes('text-sm opacity-80')

            pollutants = [
                ('PM2.5', aqi.get('pm25', 12.5), aqi.get('pm25_pct', 15)),
                ('PM10', aqi.get('pm10', 25.0), aqi.get('pm10_pct', 20)),
                ('SO2', aqi.get('so2', 10.5), aqi.get('so2_pct', 10)),
                ('CO', aqi.get('co', 320.1), aqi.get('co_pct', 25)),
                ('NO2', aqi.get('no2', 15.3), aqi.get('no2_pct', 18)),
            ]
            for name, val, pct in pollutants:
                with ui.column().classes('w-full gap-1'):
                    with ui.row().classes('w-full justify-between text-sm'):
                        ui.label(name).classes('opacity-80')
                        ui.label(f'{val} µg/m³').classes('font-mono')
                    with ui.element('div').classes('w-full bg-white/20 rounded-full h-1.5 overflow-hidden'):
                        fill = ui.element('div').classes('h-full rounded-full')
                        fill.style(f'width:{pct}%; background-color:{color}')


def render_dashboard(weather: dict):
    charts = weather.get('charts', {})
    aqi = weather.get('aqi') or {}
    lat = weather.get('lat', 21.0285)
    lon = weather.get('lon', 105.8542)

    # Chiều cao cố định cho từng row
    ROW1_H = '380px'   # biểu đồ giờ ~ AQI
    ROW2_H = '460px'   # bản đồ ~ kế hoạch

    with ui.element('div').classes('w-full flex flex-col gap-6'):
        # ── CSS Grid 2D thật sự: 2 cols x 2 rows, assign rõ từng ô ──
        with ui.element('div').style(
            'display: grid;'
            'grid-template-columns: 2fr 1fr;'
            f'grid-template-rows: {ROW1_H} {ROW2_H};'
            'gap: 24px;'
        ):
            # Ô [row1, col1]: Biểu đồ theo giờ
            with ui.element('div').classes('card bg-white/5 backdrop-blur-md rounded-2xl border border-white/20 p-5 shadow-lg flex flex-col').style('grid-column:1; grid-row:1; overflow:hidden;'):
                with ui.row().classes('items-center gap-2 mb-4'):
                    ui.icon('schedule', size='24px').classes('text-blue-400')
                    ui.label('Dự báo chi tiết trong ngày').classes('text-h6 font-semibold m-0')
                chart_container = ui.element('div').classes('flex-1 w-full relative')
                with chart_container:
                    plotly_chart(charts.get('hourly'), height_class='h-full absolute inset-0')

            # Ô [row1, col2]: AQI
            with ui.element('div').style('grid-column:2; grid-row:1; overflow:hidden;'):
                render_aqi_card(aqi)

            # Ô [row2, col1]: Bản đồ
            with ui.element('div').classes('card bg-black/30 backdrop-blur-md rounded-2xl border border-white/20 overflow-hidden shadow-lg flex flex-col').style('grid-column:1; grid-row:2;'):
                with ui.element('div').classes('p-4 border-b border-white/10'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('map', size='20px').classes('text-blue-400')
                        ui.label('Bản đồ').classes('font-semibold m-0')
                map_container = ui.element('div').classes('flex-1 relative w-full')
                with map_container:
                    m = ui.leaflet(center=(lat, lon), zoom=8, options={'zoomControl': False}).classes('w-full h-full rounded-b-2xl absolute inset-0')
                    m.tile_layer(url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', options={'maxZoom': 18})
                    if API_KEY:
                        m.tile_layer(url_template=f'https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}', options={'opacity': 0.6})
                    m.marker(latlng=(lat, lon))

            # Ô [row2, col2]: Kế hoạch tuần
            with ui.element('div').classes('card bg-gradient-to-br from-blue-500/10 to-purple-500/10 backdrop-blur-md rounded-2xl border border-white/20 p-5 shadow-lg flex flex-col items-center justify-center gap-3').style('grid-column:2; grid-row:2;'):
                ui.icon('calendar_month', size='48px').classes('text-blue-400')
                ui.label('Lên kế hoạch tuần mới?').classes('text-lg font-bold text-center')
                ui.label('Xem ngay phân tích dự báo xu hướng thời tiết 7 ngày tới.').classes('text-sm opacity-80 text-center px-2')
                ui.button('Xem dự báo 7 ngày', on_click=lambda: ui.navigate.to('/forecast')).classes('w-full text-white font-semibold py-3 rounded-xl shadow-md mt-4').style('background:var(--accent-color)')


def render_forecast_sidebar(daily: list):
    with ui.element('div').classes('card bg-white/5 backdrop-blur-md rounded-2xl border border-white/20 p-5 shadow-lg'):
        with ui.row().classes('items-center gap-2 mb-4'):
            ui.icon('calendar_today', size='20px').classes('text-blue-400')
            ui.label('Dự báo 7 ngày').classes('text-h6 font-semibold m-0')

        if not daily:
            ui.label('Dữ liệu không khả dụng.').classes('opacity-50')
            return

        for i, day in enumerate(daily[:7]):
            try:
                day_name = day.get('day_name', f'Thứ {i+1}')
                display_name = 'Hôm nay' if i == 0 else day_name
                pop_max = day.get('pop_max', 0)

                with ui.element('div').classes('forecast-row flex items-center justify-between py-3 border-b border-white/10 last:border-none'):
                    ui.label(display_name).classes('forecast-day w-1/3 font-medium')
                    with ui.row().classes('items-center gap-1 justify-center w-1/3'):
                        ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud'))).classes('text-gray-400 text-sm')
                        ui.label(f'{pop_max}%').classes('text-[0.75rem] opacity-60')
                    with ui.row().classes('forecast-temps justify-end gap-2 w-1/3 text-right'):
                        ui.label(format_temp(day.get('temp_max'))).classes('font-semibold')
                        ui.label(format_temp(day.get('temp_min'))).classes('text-gray-400')
            except Exception as e:
                print(f"Lỗi render ngày thứ {i}: {e}")