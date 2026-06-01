from nicegui import ui

from src.common.components import metric_card, plotly_chart
from src.common.config import API_KEY
from src.common.utils import lucide_to_material
from src.common.units import format_temp, format_wind_from_ms, format_pressure, format_visibility


def render_hero(weather: dict):
    with ui.element('div').classes('hero-section'):
        with ui.element('div').classes('location-info'):
            with ui.element('div').classes('location-header'):
                ui.icon('place').style('color:#4facfe;font-size:24px')
                ui.label(weather.get('city_name', 'N/A')).style('font-size:2.5rem;font-weight:700')
            ui.label(weather.get('date_str', '')).classes('date-time')

        with ui.element('div').classes('current-temp-large'):
            with ui.element('div').classes('temp-row'):
                ui.icon(lucide_to_material(weather.get('lucide_icon', 'cloud'))).style('font-size:80px;color:#fff')
                ui.label(format_temp(weather.get("temp", "--"))).classes('temp-value')
            with ui.element('div').classes('condition-info'):
                ui.label(weather.get('desc', ''))
                ui.label(' • ').style('opacity:0.5')
                ui.label(f'Cảm giác như {format_temp(weather.get("feels_like", "--"))}')


def render_metrics(weather: dict):
    with ui.element('div').classes('metrics-grid'):
        metric_card('droplets', 'Độ ẩm', f'{weather.get("humidity", "--")}%')
        metric_card('wind', 'Gió', format_wind_from_ms(weather.get("wind", "--")))
        metric_card('gauge', 'Áp suất', format_pressure(weather.get("pressure", "--")))
        metric_card('eye', 'Tầm nhìn', format_visibility(weather.get("visibility", "--")))
        metric_card('thermometer-snowflake', 'Điểm sương', format_temp(weather.get("dew_point", "--")))
        metric_card('sunrise', 'Bình minh', weather.get('sunrise', '--'))
        metric_card('sunset', 'Hoàng hôn', weather.get('sunset', '--'))
        uv = weather.get('uv_index')
        metric_card('sun', 'Chỉ số UV', str(uv if uv is not None else '0'))


def render_dashboard(weather: dict):
    charts = weather.get('charts', {})
    aqi = weather.get('aqi') or {}
    lat = weather.get('lat', 21.0285)
    lon = weather.get('lon', 105.8542)

    with ui.element('div').classes('dashboard-layout'):
        with ui.element('div').classes('dashboard-main'):
            with ui.element('div').classes('card chart-card'):
                with ui.row().classes('items-center gap-2 mb-4'):
                    ui.icon('schedule')
                    ui.label('Dự báo theo giờ').classes('text-h6').style('margin:0')
                plotly_chart(charts.get('hourly'))

            with ui.element('div').classes('trends-row'):
                with ui.element('div').classes('card chart-card'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('trending_up')
                        ui.label('Xu hướng nhiệt độ').classes('text-h6').style('margin:0')
                    plotly_chart(charts.get('temp_trend'))
                with ui.element('div').classes('card chart-card'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('grain')
                        ui.label('Khả năng kết tủa').classes('text-h6').style('margin:0')
                    plotly_chart(charts.get('precip'))

            with ui.element('div').classes('card radar-card-main'):
                with ui.element('div').classes('radar-header'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('map').style('color:#4facfe')
                        ui.label('Bản đồ vệ tinh').style('margin:0;font-weight:600')
                with ui.element('div').classes('radar-container'):
                    m = ui.leaflet(center=(lat, lon), zoom=8).classes('w-full h-full')
                    m.tile_layer(
                        url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                        options={'maxZoom': 18},
                    )
                    if API_KEY:
                        m.tile_layer(
                            url_template=f'https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
                            options={'opacity': 0.6},
                        )
                    m.marker(latlng=(lat, lon))

        with ui.element('div').classes('dashboard-sidebar'):
            render_aqi_card(aqi)
            render_forecast_sidebar(weather.get('daily', []))


def render_aqi_card(aqi: dict):
    color = aqi.get('color', '#4ade80')
    with ui.element('div').classes('card'):
        with ui.row().classes('items-center gap-2 mb-4'):
            ui.icon('air')
            ui.label('Chất lượng không khí').classes('text-h6').style('margin:0')
        with ui.element('div').classes('aqi-detailed'):
            with ui.row().classes('aqi-main items-center'):
                with ui.element('div').classes('aqi-gauge-large').style(f'border-color:{color}'):
                    ui.label(str(aqi.get('val', '--')))
                with ui.column():
                    ui.label(aqi.get('label', 'Tốt')).classes('aqi-status-badge').style(
                        f'background:{color}22;color:{color}'
                    )
                    ui.label(aqi.get('desc', 'Không khí trong lành.')).classes('aqi-status-desc')
            for name, val, pct in [
                ('PM2.5', aqi.get('pm25', 12.5), aqi.get('pm25_pct', 15)),
                ('Carbon Monoxit', aqi.get('co', 320.1), aqi.get('co_pct', 25)),
            ]:
                with ui.column().classes('pollutant-item w-full'):
                    with ui.row().classes('pollutant-info w-full justify-between'):
                        ui.label(name).classes('pollutant-name')
                        ui.label(f'{val} µg/m³').classes('pollutant-val')
                    with ui.element('div').classes('pollutant-bar'):
                        ui.element('div').classes('pollutant-fill').style(f'width:{pct}%')


def render_forecast_sidebar(daily: list):
    with ui.element('div').classes('card'):
        with ui.row().classes('items-center gap-2 mb-4'):
            ui.icon('calendar_today')
            ui.label('Dự báo 7 ngày').classes('text-h6').style('margin:0')
        if not daily:
            ui.label('Dữ liệu không khả dụng.').style('opacity:0.5')
            return
        for i, day in enumerate(daily[:7]):
            with ui.element('div').classes('forecast-row'):
                ui.label('Hôm nay' if i == 0 else day['day_name']).classes('forecast-day')
                with ui.row().classes('items-center gap-2 justify-center'):
                    ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud')))
                    ui.label(f'{day["pop_max"]}%').style('font-size:0.8rem;opacity:0.6')
                with ui.row().classes('forecast-temps justify-end'):
                    ui.label(format_temp(day["temp_max"])).style('font-weight:600')
                    ui.label(format_temp(day["temp_min"])).classes('min')
