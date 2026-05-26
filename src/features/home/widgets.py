from nicegui import ui

from src.common.components import metric_card, plotly_chart
from src.common.config import API_KEY
from src.common.utils import lucide_to_material

def render_hero(weather: dict):
    with ui.element('div').classes('hero-section'):
        with ui.element('div').classes('location-info'):
            with ui.element('div').classes('location-header flex items-center gap-2'):
                ui.icon('place').style('color:#4facfe;font-size:24px')
                ui.label(weather.get('city_name', 'N/A')).style('font-size:2.5rem;font-weight:700')
            ui.label(weather.get('date_str', '')).classes('date-time')

        with ui.element('div').classes('current-temp-large'):
            with ui.element('div').classes('temp-row flex items-center gap-4'):
                ui.icon(lucide_to_material(weather.get('lucide_icon', 'cloud'))).style('font-size:80px;color:#fff')
                ui.label(f'{weather.get("temp", "--")}°C').classes('temp-value')
            with ui.element('div').classes('condition-info flex items-center gap-1'):
                ui.label(weather.get('desc', ''))
                ui.label(' • ').classes('opacity-50')
                ui.label(f'Cảm giác như {weather.get("feels_like", "--")}°C')


def render_metrics(weather: dict):
    with ui.element('div').classes('metrics-grid'):
        metric_card('droplets', 'Độ ẩm', f'{weather.get("humidity", "--")}%')
        metric_card('wind', 'Gió', f'{weather.get("wind", "--")} km/h')
        metric_card('gauge', 'Áp suất', f'{weather.get("pressure", "--")} hPa')
        metric_card('eye', 'Tầm nhìn', f'{weather.get("visibility", "--")} km')
        metric_card('thermometer-snowflake', 'Điểm sương', f'{weather.get("dew_point", "--")}°C')
        metric_card('sunrise', 'Bình minh', weather.get('sunrise', '--'))
        metric_card('sunset', 'Hoàng hôn', weather.get('sunset', '--'))
        
        uv = weather.get('uv_index')
        metric_card('sun', 'Chỉ số UV', str(uv if uv is not None else '0'))


def render_dashboard(weather: dict):
    charts = weather.get('charts', {})
    aqi = weather.get('aqi') or {}
    lat = weather.get('lat', 21.0285)
    lon = weather.get('lon', 105.8542)

    with ui.element('div').classes('dashboard-layout gap-4 flex flex-col md:flex-row w-full'):
        # VÙNG HIỂN THỊ CHÍNH (MAIN)
        with ui.element('div').classes('dashboard-main flex-1 flex flex-col gap-4'):
            
            # Dự báo theo giờ (Giữ lại vì hỗ trợ trực tiếp thông tin trong ngày)
            with ui.element('div').classes('card chart-card'):
                with ui.row().classes('items-center gap-2 mb-4'):
                    ui.icon('schedule')
                    ui.label('Dự báo chi tiết trong ngày').classes('text-h6 m-0')
                plotly_chart(charts.get('hourly'))

            # Bản đồ vệ tinh thời gian thực
            with ui.element('div').classes('card radar-card-main h-[400px]'):
                with ui.element('div').classes('radar-header'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('map').style('color:#4facfe')
                        ui.label('Bản đồ mây vệ tinh & Lượng mưa').classes('m-0 font-semibold')
                        
                with ui.element('div').classes('radar-container h-[calc(100%-60px)]'):
                    m = ui.leaflet(center=(lat, lon), zoom=8, options={'zoomControl': False}).classes('w-full h-full')
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
                   
        # THANH BÊN (SIDEBAR)
        with ui.element('div').classes('dashboard-sidebar w-full md:w-[320px] shrink-0 flex flex-col gap-4'):
            # Chất lượng không khí thực tế
            render_aqi_card(aqi)
            
            # Thay thế danh sách 7 ngày lặp lại bằng một Banner điều hướng thông minh
            with ui.element('div').classes('card flex flex-col gap-3 justify-between items-center p-5 text-center bg-gradient-to-br from-blue-500/10 to-transparent rounded-xl border border-white/10'):
                ui.icon('calendar_month').style('font-size: 42px; color: #4facfe')
                with ui.column().classes('gap-1'):
                    ui.label('Lên kế hoạch tuần mới?').classes('text-lg font-bold text-white')
                    ui.label('Xem ngay phân tích dự báo xu hướng thời tiết 7 ngày tới với biểu đồ thông minh.').classes('text-xs opacity-70')
                # Nút nhấn chuyển trang sang tab /forecast
                ui.button('Xem Dự Báo 7 Ngày', on_click=lambda: ui.navigate.to('/forecast')).classes('w-full bg-[#4facfe] text-white font-medium rounded-lg py-2 shadow-md hover:opacity-90')

def render_aqi_card(aqi: dict):
    color = aqi.get('color', '#4ade80')
    with ui.element('div').classes('card'):
        with ui.row().classes('items-center gap-2 mb-4'):
            ui.icon('air')
            ui.label('Chất lượng không khí').classes('text-h6 m-0')
            
        with ui.element('div').classes('aqi-detailed flex flex-col gap-4'):
            with ui.row().classes('aqi-main items-center gap-4'):
                with ui.element('div').classes('aqi-gauge-large').style(f'border-color:{color}'):
                    ui.label(str(aqi.get('val', '--')))
                with ui.column():
                    ui.label(aqi.get('label', 'Tốt')).classes('aqi-status-badge').style(
                        f'background:{color}22;color:{color}'
                    )
                    ui.label(aqi.get('desc', 'Không khí trong lành.')).classes('aqi-status-desc')
                    
            # Pollutants list
            pollutants = [
                ('PM2.5', aqi.get('pm25', 12.5), aqi.get('pm25_pct', 15)),
                ('PM10', aqi.get('pm10', 25.0), aqi.get('pm10_pct', 20)),
                ('SO2', aqi.get('so2', 10.5), aqi.get('so2_pct', 10)),
                ('CO', aqi.get('co', 320.1), aqi.get('co_pct', 25)),
                ('NO2', aqi.get('no2', 15.3), aqi.get('no2_pct', 18)),
            ]
            for name, val, pct in pollutants:
                with ui.column().classes('pollutant-item w-full gap-1'):
                    with ui.row().classes('pollutant-info w-full justify-between'):
                        ui.label(name).classes('pollutant-name')
                        ui.label(f'{val} µg/m³').classes('pollutant-val')
                    with ui.element('div').classes('pollutant-bar w-full bg-gray-200 rounded-full h-2 overflow-hidden'):
                        ui.element('div').classes('pollutant-fill h-full').style(f'width:{pct}%; background-color:{color}')


def render_forecast_sidebar(daily: list):
    with ui.element('div').classes('card'):
        with ui.row().classes('items-center gap-2 mb-4'):
            ui.icon('calendar_today')
            ui.label('Dự báo 7 ngày').classes('text-h6 m-0')
        
        if not daily:
            ui.label('Dữ liệu không khả dụng.').classes('opacity-50')
            return

        for i, day in enumerate(daily[:7]):
            try:
                day_name = day.get('day_name', f'Thứ {i+1}')
                display_name = 'Hôm nay' if i == 0 else day_name
                
                # Hàm ép kiểu an toàn tránh sập layout nếu data trả về sai kiểu dữ liệu
                def safe_round(val):
                    try:
                        return round(float(val))
                    except (TypeError, ValueError):
                        return '--'

                temp_max = safe_round(day.get('temp_max'))
                temp_min = safe_round(day.get('temp_min'))
                pop_max = day.get('pop_max', 0)

                with ui.element('div').classes('forecast-row flex items-center justify-between py-2 border-b border-gray-100 last:border-none'):
                    ui.label(display_name).classes('forecast-day w-1/3')
                    
                    with ui.row().classes('items-center gap-1 justify-center w-1/3'):
                        ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud'))).classes('text-gray-500')
                        ui.label(f'{pop_max}%').classes('text-[0.8rem] opacity-60')
                        
                    with ui.row().classes('forecast-temps justify-end gap-2 w-1/3 text-right'):
                        ui.label(f'{temp_max}°').classes('font-semibold')
                        ui.label(f'{temp_min}°').classes('text-gray-400')
            except Exception as e:
                print(f"Lỗi render ngày thứ {i}: {e}")