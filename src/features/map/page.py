from datetime import datetime, timedelta
import requests
import random

from nicegui import ui

from src.common.components import apply_theme, navbar
from src.common.config import API_KEY, get_city

from .constants import MAP_LAYERS
from .service import get_data

_TAG = 'div'

LAYER_METADATA = {
    'temp_new': {
        'title': 'Nhiệt độ',
        'unit': '°C',
        'ranges': [
            {'color': '#1e3a8a', 'label': '-10'},
            {'color': '#3b82f6', 'label': '0'},
            {'color': '#60a5fa', 'label': '15'},
            {'color': '#fef08a', 'label': '25'},
            {'color': '#facc15', 'label': '30'},
            {'color': '#f97316', 'label': '35'},
            {'color': '#ef4444', 'label': '40+'}
        ]
    },
    'precipitation_new': {
        'title': 'Lượng mưa',
        'unit': 'mm',
        'ranges': [
            {'color': '#cbd5e1', 'label': '0'},
            {'color': '#7dd3fc', 'label': '1'},
            {'color': '#3b82f6', 'label': '5'},
            {'color': '#1d4ed8', 'label': '10'},
            {'color': '#4f46e5', 'label': '20'},
            {'color': '#a855f7', 'label': '50'},
            {'color': '#ef4444', 'label': '100+'}
        ]
    },
    'wind_new': {
        'title': 'Tốc độ gió',
        'unit': 'km/h',
        'ranges': [
            {'color': '#cbd5e1', 'label': '0'},
            {'color': '#a7f3d0', 'label': '5'},
            {'color': '#34d399', 'label': '15'},
            {'color': '#facc15', 'label': '30'},
            {'color': '#f97316', 'label': '50'},
            {'color': '#ef4444', 'label': '80+'}
        ]
    },
    'pressure_new': {
        'title': 'Áp suất',
        'unit': 'hPa',
        'ranges': [
            {'color': '#93c5fd', 'label': '970'},
            {'color': '#60a5fa', 'label': '990'},
            {'color': '#3b82f6', 'label': '1010'},
            {'color': '#1d4ed8', 'label': '1020'},
            {'color': '#1e3a8a', 'label': '1040+'}
        ]
    },
    'clouds_new': {
        'title': 'Mây',
        'unit': '%',
        'ranges': [
            {'color': 'rgba(255,255,255,0.1)', 'label': '0%'},
            {'color': 'rgba(255,255,255,0.3)', 'label': '30%'},
            {'color': 'rgba(255,255,255,0.6)', 'label': '70%'},
            {'color': 'rgba(255,255,255,0.95)', 'label': '100%'}
        ]
    }
}


def get_simulated_weather(lat: float, lon: float, offset_hours: int, base_weather: dict) -> dict:
    """
    Simulates weather values for the given coordinates and timeline offset.
    Uses latitude, longitude, and offset_hours to seed the random generator,
    ensuring consistent values for the same place/time but realistic changes.
    """
    lat_key = int(round(lat, 3) * 1000)
    lon_key = int(round(lon, 3) * 1000)
    seed = abs(lat_key * 100000 + lon_key * 17 + offset_hours * 1013)
    
    rng = random.Random(seed)
    
    # Get base values from weather data, falling back to realistic defaults
    b_temp = base_weather.get('temp', 28.7)
    if isinstance(b_temp, str) or b_temp is None:
        b_temp = 28.7
        
    b_humidity = base_weather.get('humidity', 78)
    if isinstance(b_humidity, str) or b_humidity is None:
        b_humidity = 78
        
    b_pressure = base_weather.get('pressure', 1006)
    if isinstance(b_pressure, str) or b_pressure is None:
        b_pressure = 1006
        
    b_wind = base_weather.get('wind', 14.6)
    if isinstance(b_wind, str) or b_wind is None:
        b_wind = 14.6
        
    b_clouds = base_weather.get('clouds', 64)
    if isinstance(b_clouds, str) or b_clouds is None:
        b_clouds = 64
        
    b_visibility = base_weather.get('visibility', 10)
    if isinstance(b_visibility, str) or b_visibility is None:
        b_visibility = 10
    
    # 1. Temperature: has a diurnal cycle depending on hour of day
    hour_of_day = (datetime.now().hour + offset_hours) % 24
    diurnal_effect = -4.0 * (((hour_of_day - 14) / 12.0) ** 2) + 2.0
    temp = b_temp + diurnal_effect + rng.uniform(-1.5, 1.5)
    temp = round(max(-5.0, min(48.0, temp)), 1)
    
    # 2. Clouds
    clouds = b_clouds + rng.uniform(-20, 20)
    clouds = int(max(0, min(100, round(clouds))))
    
    # 3. Rain (Precipitation): higher chance if clouds are high
    rain_chance = clouds / 100.0 + rng.uniform(-0.15, 0.25)
    if rain_chance > 0.65:
        rain = rng.uniform(0.1, 10.0)
        if rain_chance > 0.82:
            rain += rng.uniform(10.0, 45.0)
        rain = round(rain, 1)
    else:
        rain = 0.0
        
    # 4. Pressure: slight variations
    pressure = b_pressure + rng.uniform(-5.0, 5.0) + (1.0 if (6 <= hour_of_day <= 18) else -1.0)
    pressure = int(round(pressure))
    
    # 5. Wind Speed
    wind = b_wind + rng.uniform(-4.0, 8.0)
    wind = round(max(0.0, wind), 1)
    
    # 6. Wind direction
    wind_dir = rng.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    
    # 7. Humidity: inversely proportional to temperature
    humidity = b_humidity - (temp - b_temp) * 2.5 + rng.uniform(-5.0, 5.0)
    humidity = int(max(10, min(100, round(humidity))))
    
    # 8. Visibility: affected by rain and clouds
    visibility = b_visibility
    if rain > 10.0:
        visibility = max(1.0, visibility - rng.uniform(5.0, 8.0))
    elif rain > 0.0:
        visibility = max(2.0, visibility - rng.uniform(2.0, 4.0))
    elif clouds > 75:
        visibility = max(4.0, visibility - rng.uniform(0.5, 2.0))
    visibility = int(round(max(1.0, min(10.0, visibility))))
    
    # Classifications for Yếu / Trung bình / Cao
    # Temp
    if temp < 20.0: temp_lvl = 'Yếu'
    elif temp <= 32.0: temp_lvl = 'Trung bình'
    else: temp_lvl = 'Cao'
    
    # Rain
    if rain == 0.0: rain_lvl = 'Yếu (Không mưa)'
    elif rain < 2.0: rain_lvl = 'Yếu'
    elif rain <= 10.0: rain_lvl = 'Trung bình'
    else: rain_lvl = 'Cao'
    
    # Wind
    if wind < 10.0: wind_lvl = 'Yếu'
    elif wind <= 25.0: wind_lvl = 'Trung bình'
    else: wind_lvl = 'Cao'
    
    # Pressure
    if pressure < 1006: pressure_lvl = 'Yếu'
    elif pressure <= 1014: pressure_lvl = 'Trung bình'
    else: pressure_lvl = 'Cao'
    
    # Clouds
    if clouds < 30: clouds_lvl = 'Yếu'
    elif clouds <= 70: clouds_lvl = 'Trung bình'
    else: clouds_lvl = 'Cao'
    
    return {
        'temp': temp, 'temp_level': temp_lvl,
        'rain': rain, 'rain_level': rain_lvl,
        'pressure': pressure, 'pressure_level': pressure_lvl,
        'wind': wind, 'wind_level': wind_lvl,
        'wind_dir': wind_dir,
        'humidity': humidity,
        'clouds': clouds, 'clouds_level': clouds_lvl,
        'visibility': visibility
    }


def register():
    @ui.page('/map')
    def map_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
        
        lat = weather.get('lat', 10.8231) if not weather.get('error') else 10.8231
        lon = weather.get('lon', 106.6297) if not weather.get('error') else 106.6297

        # ==================== STATE MANAGEMENT ====================
        state = {
            'layer': {'key': 'precipitation_new', 'label': 'Lượng mưa', 'range': '0 ... 100+ mm'},
            'timeline': {'playing': False, 'offset': 7, 'total_hours': 24},
            'location': {'lat': lat, 'lon': lon, 'name': city},
            'weather_data': weather,
            'layer_visible': True
        }
        
        map_ref = {'leaflet': None, 'weather_layer': None, 'marker': None}
        
        ui_refs = {
            'search_input': None, 'search_btn': None, 'search_feedback': None,
            'play_btn': None, 'time_slider': None, 'time_label_start': None, 'time_label_end': None,
            'menu_items': [],
            'info_title': None, 'info_coords': None,
            'info_temp': None, 'info_precip': None, 'info_pressure': None,
            'info_wind': None, 'info_wind_dir': None, 'info_humidity': None, 
            'info_cloud': None, 'info_visibility': None, 'info_update': None,
            'legend_title': None, 'legend_value': None, 'legend_gradient': None, 'legend_ranges': None,
            'eye_btn': None, 'eye_btn_icon': None
        }

        def format_time(offset_hours: int) -> tuple:
            target = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=offset_hours)
            return target.strftime('%d/%m'), target.strftime('%H:%M')

        def update_info_panel():
            w = state['weather_data']
            offset = state['timeline']['offset']
            lat_val = state['location']['lat']
            lon_val = state['location']['lon']
            
            # Use base mock dictionary if weather api has error
            base_w = w if not w.get('error') else {
                'temp': 28.7, 'humidity': 78, 'pressure': 1006, 'wind': 14.6, 'clouds': 64, 'visibility': 10000
            }
            
            sim = get_simulated_weather(lat_val, lon_val, offset, base_w)
            
            ui_refs['info_title'].set_text(state['layer']['label'])
            ui_refs['info_coords'].set_text(f"{lat_val:.4f}° N, {lon_val:.4f}° E")
            
            if ui_refs['info_temp']: ui_refs['info_temp'].set_text(f"{sim['temp']} °C ({sim['temp_level']})")
            if ui_refs['info_precip']: ui_refs['info_precip'].set_text(f"{sim['rain']} mm ({sim['rain_level']})")
            if ui_refs['info_pressure']: ui_refs['info_pressure'].set_text(f"{sim['pressure']} hPa ({sim['pressure_level']})")
            if ui_refs['info_wind']: ui_refs['info_wind'].set_text(f"{sim['wind']} km/h ({sim['wind_level']})")
            if ui_refs['info_wind_dir']: ui_refs['info_wind_dir'].set_text(f"{sim['wind_dir']}")
            if ui_refs['info_humidity']: ui_refs['info_humidity'].set_text(f"{sim['humidity']} %")
            if ui_refs['info_cloud']: ui_refs['info_cloud'].set_text(f"{sim['clouds']} % ({sim['clouds_level']})")
            if ui_refs['info_visibility']: ui_refs['info_visibility'].set_text(f"{sim['visibility']} km")
            
            d_str, t_str = format_time(offset)
            ui_refs['info_update'].set_text(f"Cập nhật: {t_str}, {d_str}/2026")

        def update_legend():
            metadata = LAYER_METADATA.get(state['layer']['key'], {})
            if not metadata: return
            
            # Get current simulated weather value for this layer
            w = state['weather_data']
            offset = state['timeline']['offset']
            lat_val = state['location']['lat']
            lon_val = state['location']['lon']
            base_w = w if not w.get('error') else {
                'temp': 28.7, 'humidity': 78, 'pressure': 1006, 'wind': 14.6, 'clouds': 64, 'visibility': 10000
            }
            sim = get_simulated_weather(lat_val, lon_val, offset, base_w)
            
            key = state['layer']['key']
            val_str = ""
            if key == 'temp_new':
                val_str = f": {sim['temp']} °C"
            elif key == 'precipitation_new':
                val_str = f": {sim['rain']} mm"
            elif key == 'wind_new':
                val_str = f": {sim['wind']} km/h"
            elif key == 'pressure_new':
                val_str = f": {sim['pressure']} hPa"
            elif key == 'clouds_new':
                val_str = f": {sim['clouds']} %"

            ui_refs['legend_title'].set_text(f"{metadata['title']} ({metadata['unit']}){val_str}")
            ranges = metadata.get('ranges', [])
            if ranges:
                gradient_stops = ', '.join([f"{r['color']} {i*100//(len(ranges)-1) if len(ranges)>1 else 0}%" for i, r in enumerate(ranges)])
                ui_refs['legend_gradient'].style(f"background: linear-gradient(90deg, {gradient_stops});")
                range_html = '<div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#cbd5e1;margin-top:0.35rem;font-weight:500;">'
                for r in ranges:
                    range_html += f'<span>{r["label"]}</span>'
                range_html += '</div>'
                ui_refs['legend_ranges'].set_content(range_html)

        def set_layer(key: str, label: str, range_text: str, btn_el):
            state['layer']['key'] = key
            state['layer']['label'] = label
            state['layer']['range'] = range_text
            
            for item in ui_refs['menu_items']:
                item.classes(remove='active')
            
            btn_el.classes(add='active')
            
            if API_KEY and map_ref['leaflet'] and state['layer_visible']:
                if map_ref['weather_layer']:
                    map_ref['leaflet'].remove_layer(map_ref['weather_layer'])
                map_ref['weather_layer'] = map_ref['leaflet'].tile_layer(
                    url_template=f'https://tile.openweathermap.org/map/{key}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
                    options={'opacity': 0.8, 'className': 'fade-layer'},
                )
            
            update_info_panel()
            update_legend()

        def toggle_play():
            state['timeline']['playing'] = not state['timeline']['playing']
            ui_refs['play_btn'].set_name('pause' if state['timeline']['playing'] else 'play_arrow')

        def on_slider_change(e):
            if e.value is not None:
                state['timeline']['offset'] = int(e.value)
                d1, t1 = format_time(state['timeline']['offset'])
                ui_refs['time_label_start'].set_content(f'<div class="timeline-date">{d1}</div><div class="timeline-time">{t1}</div>')
                update_info_panel()
                update_legend()

        def toggle_layer_visibility():
            state['layer_visible'] = not state['layer_visible']
            ui_refs['eye_btn_icon'].set_name('visibility' if state['layer_visible'] else 'visibility_off')

        def handle_map_click(e):
            latlng = e.args.get('latlng')
            if latlng:
                new_lat = latlng['lat']
                new_lon = latlng['lng']
                state['location']['lat'] = new_lat
                state['location']['lon'] = new_lon
                
                if map_ref['marker']:
                    map_ref['marker'].move(new_lat, new_lon)
                
                update_info_panel()
                update_legend()
            
            if map_ref['leaflet']:
                if not state['layer_visible']:
                    if map_ref['weather_layer']:
                        map_ref['leaflet'].remove_layer(map_ref['weather_layer'])
                else:
                    if API_KEY:
                        map_ref['weather_layer'] = map_ref['leaflet'].tile_layer(
                            url_template=f'https://tile.openweathermap.org/map/{state["layer"]["key"]}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
                            options={'opacity': 0.8, 'className': 'fade-layer'},
                        )

        def search_location():
            search_query = ui_refs['search_input'].value
            if not search_query:
                ui_refs['search_feedback'].set_text('Vui lòng nhập tên địa điểm!')
                ui_refs['search_feedback'].style('color: #f87171')
                return
            
            ui_refs['search_feedback'].set_text('Đang tìm kiếm...')
            ui_refs['search_feedback'].style('color: #60a5fa')
            
            try:
                # 1. Fetch location from Nominatim (OpenStreetMap geocoding)
                headers = {'User-Agent': 'WeatherNow-App/1.0'}
                url = f"https://nominatim.openstreetmap.org/search?q={search_query}&format=json&limit=1"
                r = requests.get(url, headers=headers, timeout=5)
                
                if r.status_code == 200 and r.json():
                    data = r.json()[0]
                    new_lat = float(data['lat'])
                    new_lon = float(data['lon'])
                    display_name = data.get('display_name', search_query)
                    short_name = display_name.split(',')[0]
                    
                    state['location']['lat'] = new_lat
                    state['location']['lon'] = new_lon
                    state['location']['name'] = short_name
                    
                    if map_ref['leaflet']:
                        map_ref['leaflet'].center = (new_lat, new_lon)
                        if map_ref['marker']:
                            map_ref['marker'].move(new_lat, new_lon)
                    
                    # Fetch mock or actual weather data
                    w_data = get_data(API_KEY, short_name) if API_KEY else {'error': 'Thiếu API KEY'}
                    if 'error' in w_data:
                        w_data = {
                            'temp': 28.7,
                            'humidity': 78,
                            'pressure': 1006,
                            'wind': 14.6,
                            'clouds': 64,
                            'visibility': 10000,
                            'stats': {'total_rain': 0.0}
                        }
                    state['weather_data'] = w_data
                    
                    ui_refs['search_feedback'].set_text(f"Tìm thấy: {short_name}")
                    ui_refs['search_feedback'].style('color: #34d399')
                    
                    update_info_panel()
                    update_legend()
                else:
                    # Vietnamese cities fallback dictionary (offline support)
                    local_cities = {
                        'hà nội': (21.0285, 105.8542, 'Hanoi'),
                        'hanoi': (21.0285, 105.8542, 'Hanoi'),
                        'hồ chí minh': (10.8231, 106.6297, 'Ho Chi Minh City'),
                        'ho chi minh': (10.8231, 106.6297, 'Ho Chi Minh City'),
                        'tphcm': (10.8231, 106.6297, 'Ho Chi Minh City'),
                        'sài gòn': (10.8231, 106.6297, 'Ho Chi Minh City'),
                        'saigon': (10.8231, 106.6297, 'Ho Chi Minh City'),
                        'đà nẵng': (16.0544, 108.2022, 'Da Nang'),
                        'da nang': (16.0544, 108.2022, 'Da Nang'),
                        'nha trang': (12.2388, 109.1967, 'Nha Trang'),
                        'cần thơ': (10.0452, 105.7469, 'Can Tho'),
                        'can tho': (10.0452, 105.7469, 'Can Tho'),
                        'hải phòng': (20.8449, 106.6881, 'Hai Phong'),
                        'hai phong': (20.8449, 106.6881, 'Hai Phong'),
                    }
                    
                    q_lower = search_query.lower().strip()
                    matched = False
                    for city_k, coords in local_cities.items():
                        if city_k in q_lower:
                            new_lat, new_lon, short_name = coords
                            state['location']['lat'] = new_lat
                            state['location']['lon'] = new_lon
                            state['location']['name'] = short_name
                            
                            if map_ref['leaflet']:
                                map_ref['leaflet'].center = (new_lat, new_lon)
                                if map_ref['marker']:
                                    map_ref['marker'].move(new_lat, new_lon)
                            
                            w_data = get_data(API_KEY, short_name) if API_KEY else {'error': 'Thiếu API KEY'}
                            if 'error' in w_data:
                                w_data = {
                                    'temp': 28.7,
                                    'humidity': 78,
                                    'pressure': 1006,
                                    'wind': 14.6,
                                    'clouds': 64,
                                    'visibility': 10000,
                                    'stats': {'total_rain': 0.0}
                                }
                            state['weather_data'] = w_data
                            
                            ui_refs['search_feedback'].set_text(f"Tìm thấy: {short_name}")
                            ui_refs['search_feedback'].style('color: #34d399')
                            
                            update_info_panel()
                            update_legend()
                            matched = True
                            break
                            
                    if not matched:
                        ui_refs['search_feedback'].set_text('Không tìm thấy địa điểm!')
                        ui_refs['search_feedback'].style('color: #f87171')
            except Exception as e:
                ui_refs['search_feedback'].set_text(f"Lỗi kết nối: {str(e)}")
                ui_refs['search_feedback'].style('color: #f87171')

        # ==================== CSS STYLING ====================
        ui.html(f'''
            <style>
                /* RESET & MAP */
                .map-page-wrapper {{ position: relative; height: calc(100vh - 60px); overflow: hidden; background: #cdd2d4; }}
                .map-container-full {{ position: relative; width: 100%; height: 100%; }}
                .map-leaflet {{ width: 100%; height: 100%; filter: brightness(0.95) saturate(1.1) contrast(1.1); z-index: 1; }}
                .leaflet-control-zoom, .leaflet-control-attribution {{ display: none !important; }}
                
                .fade-layer {{ transition: opacity 0.5s ease-in-out; }}
                
                .map-overlay-wrapper {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999 !important; pointer-events: none; }}
                .map-overlay {{ pointer-events: auto; }}
                
                /* =====================
                   ULTRA PREMIUM GLASSMORPHISM 
                   ===================== */
                .panel-dark {{
                    background: rgba(30, 34, 43, 0.75);
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    border-radius: 10px;
                    color: #f8fafc;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }}
                
                /* TOP LEFT SEARCH */
                .search-panel-container {{ position: absolute; top: 16px; left: 16px; width: 300px; display: flex; flex-direction: column; gap: 8px; }}
                .search-box {{ display: flex; gap: 8px; align-items: center; background: transparent; }}
                .search-input-wrapper {{
                    flex: 1; background: rgba(0, 0, 0, 0.2); border-radius: 8px; padding: 4px 10px; height: 38px;
                    display: flex; align-items: center; border: 1px solid rgba(255, 255, 255, 0.05);
                }}
                .search-input-wrapper input {{
                    background: transparent; border: none; color: #f8fafc; outline: none; width: 100%; font-size: 0.85rem;
                }}
                .search-input-wrapper input::placeholder {{ color: #94a3b8; }}
                .btn-search {{
                    width: 38px; height: 38px; background: rgba(59, 130, 246, 0.8); border-radius: 8px;
                    display: flex; justify-content: center; align-items: center; cursor: pointer;
                    border: 1px solid rgba(255, 255, 255, 0.1); transition: 0.2s;
                }}
                .btn-search:hover {{ background: rgba(59, 130, 246, 1); }}
                .search-feedback {{ font-size: 0.75rem; color: #cbd5e1; padding-left: 4px; font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.6); }}
                
                /* LEFT SIDEBAR */
                .sidebar-panel {{
                    position: absolute; top: 76px; left: 16px; width: 220px; padding: 8px;
                    display: flex; flex-direction: column; gap: 2px;
                }}
                .layer-item {{
                    display: flex; align-items: center; justify-content: space-between;
                    padding: 10px 12px; border-radius: 8px; cursor: pointer;
                    color: #cbd5e1; transition: all 0.2s; font-size: 0.85rem; font-weight: 500;
                }}
                .layer-item-content {{ display: flex; align-items: center; gap: 10px; }}
                .layer-item:hover {{ background: rgba(255, 255, 255, 0.1); color: #fff; }}
                .layer-item.active {{ background: rgba(59, 130, 246, 0.9); color: #fff; }}
                
                .layer-arrow {{ opacity: 0; transform: translateX(-5px); transition: 0.2s; font-size: 14px; }}
                .layer-item.active .layer-arrow {{ opacity: 1; transform: translateX(0); }}
                
                .sidebar-divider {{ height: 1px; background: rgba(255, 255, 255, 0.08); margin: 6px 0; }}
                .wind-toggle-row {{ display: flex; justify-content: space-between; align-items: center; padding: 4px 12px; font-size: 0.8rem; color: #cbd5e1; }}
                
                /* RIGHT INFO PANEL (Sleek Glass design) */
                .info-panel {{
                    position: absolute; top: 16px; right: 16px; width: 280px; padding: 16px;
                    display: flex; flex-direction: column; gap: 12px;
                }}
                .info-title {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 0px; color: #fff; font-family: 'Outfit', sans-serif; }}
                .info-subtitle {{ font-size: 0.75rem; color: #94a3b8; line-height: 1.2; }}
                .info-coords {{ font-size: 0.75rem; font-weight: 500; color: #f8fafc; margin-top: 2px; }}
                
                .info-list {{ display: flex; flex-direction: column; gap: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding: 12px 0; }}
                .info-row {{ display: flex; justify-content: space-between; align-items: center; }}
                .info-label-group {{ display: flex; align-items: center; gap: 10px; color: #cbd5e1; font-size: 0.8rem; }}
                .info-label-group .q-icon {{ font-size: 16px; width: 16px; color: #94a3b8; }}
                
                /* Icon colors aligned with mockup style */
                .icon-blue {{ color: #60a5fa !important; }}
                .icon-red {{ color: #f87171 !important; }}
                .icon-green {{ color: #34d399 !important; }}
                .icon-gray {{ color: #cbd5e1 !important; }}
                
                .info-val {{ font-size: 0.85rem; font-weight: 600; color: #f8fafc; letter-spacing: 0.3px; text-align: right; max-width: 170px; }}
                .info-footer {{ font-size: 0.75rem; color: #94a3b8; font-weight: 500; }}
                
                /* EYE BUTTON - Premium floating toggle */
                .eye-btn {{
                    position: absolute; top: 16px; right: 312px; width: 38px; height: 38px;
                    border-radius: 8px; display: grid; place-items: center; cursor: pointer; font-size: 18px;
                    background: rgba(30, 34, 43, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); color: #93c5fd;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: 0.2s;
                }}
                .eye-btn:hover {{ background: rgba(30, 34, 43, 0.95); transform: scale(1.05); }}
                
                /* RIGHT BOTTOM LEGEND */
                .legend-panel {{
                    position: absolute; bottom: 16px; right: 16px; width: 280px; padding: 14px;
                    display: flex; flex-direction: column; gap: 8px;
                }}
                .legend-title {{ font-size: 0.8rem; font-weight: 600; color: #f8fafc; margin-bottom: 2px; }}
                .legend-gradient-bar {{ height: 12px; border-radius: 4px; width: 100%; }}
                
                /* LEFT BOTTOM TIMELINE */
                .timeline-panel {{
                    position: absolute; bottom: 16px; left: 16px; width: 380px; padding: 8px 12px;
                    display: flex; align-items: center; gap: 12px; border-radius: 10px;
                }}
                .play-btn {{
                    width: 32px; height: 32px; background: rgba(59, 130, 246, 0.9); border-radius: 50%;
                    display: grid; place-items: center; cursor: pointer; color: white; border: none; font-size: 16px; flex-shrink: 0;
                    transition: 0.2s; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
                }}
                .play-btn:hover {{ background: rgba(59, 130, 246, 1); transform: scale(1.05); }}
                
                .time-stack {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-width: 35px; flex-shrink: 0; }}
                .timeline-date {{ font-size: 0.65rem; color: #cbd5e1; font-weight: 500; line-height: 1.1; }}
                .timeline-time {{ font-size: 0.8rem; font-weight: 700; color: #f8fafc; line-height: 1.1; }}
                
                /* TIMELINE SLIDER WITH TICK MARKS RULER */
                .slider-container {{ flex: 1; position: relative; display: flex; flex-direction: column; justify-content: center; padding: 8px 0; }}
                .ruler-bg {{
                    position: absolute; top: 40%; left: 0; right: 0; transform: translateY(-50%); height: 8px;
                    background-image: linear-gradient(90deg, rgba(255, 255, 255, 0.2) 1px, transparent 1px);
                    background-size: calc(100% / 24) 100%;
                    background-position: left center;
                    opacity: 0.5; pointer-events: none;
                }}
                .ruler-labels {{
                    position: absolute; bottom: -8px; left: 0; right: 0; display: flex; justify-content: space-between;
                    font-size: 0.6rem; color: #94a3b8; font-family: monospace; font-weight: 500;
                }}
                
                /* Quasar Slider overrides to look like mockup design */
                .q-slider__track {{ height: 2px !important; background: rgba(255, 255, 255, 0.2) !important; }}
                .q-slider__thumb {{ width: 12px !important; height: 12px !important; border: 2px solid #fff; background: #3b82f6 !important; box-shadow: 0 0 6px rgba(0, 0, 0, 0.8); }}
                
                @media (max-width: 768px) {{
                    .search-panel-container {{ width: calc(100vw - 32px); left: 16px; top: 16px; }}
                    .info-panel {{ display: none; }}
                    .sidebar-panel {{ display: none; }}
                    .eye-btn {{ display: none; }}
                    .timeline-panel {{ width: calc(100vw - 32px); left: 16px; bottom: 16px; }}
                    .legend-panel {{ bottom: 80px; right: 16px; width: calc(100vw - 32px); }}
                }}
            </style>
        ''')

        # ==================== COMPONENT RENDERERS ====================
        
        def render_map():
            m = ui.leaflet(center=(lat, lon), zoom=5, options={'zoomControl': False}).classes('map-leaflet w-full h-full')
            map_ref['leaflet'] = m
            m.on('map-click', handle_map_click)
            m.tile_layer(
                url_template='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
                options={'maxZoom': 19, 'attribution': '© CartoDB, OpenStreetMap'}
            )
            if API_KEY:
                map_ref['weather_layer'] = m.tile_layer(
                    url_template=f'https://tile.openweathermap.org/map/{state["layer"]["key"]}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
                    options={'opacity': 0.8, 'className': 'fade-layer'},
                )
            map_ref['marker'] = m.marker(latlng=(lat, lon))

        def render_search_panel():
            with ui.element(_TAG).classes('search-panel-container map-overlay'):
                with ui.element(_TAG).classes('search-box'):
                    with ui.element(_TAG).classes('search-input-wrapper'):
                        ui_refs['search_input'] = ui.input(placeholder='Nhập thành phố, quốc gia...').props('borderless dense').style('width: 100%; color: #fff').on('keydown.enter', search_location)
                    
                    with ui.element('button').classes('btn-search').on('click', search_location):
                        ui.icon('search').style('font-size: 18px; color: #fff;')
                
                ui_refs['search_feedback'] = ui.label('Nhập tên để tìm kiếm địa điểm').classes('search-feedback')

        def render_sidebar():
            with ui.element(_TAG).classes('sidebar-panel panel-dark map-overlay'):
                for i, (key, label, icon, range_text) in enumerate(MAP_LAYERS):
                    is_active = (key == state['layer']['key'])
                    item = ui.element(_TAG).classes('layer-item' + (' active' if is_active else ''))
                    ui_refs['menu_items'].append(item)
                    with item:
                        with ui.element(_TAG).classes('layer-item-content'):
                            ui.icon(icon)
                            ui.label(label)
                        ui.icon('chevron_right').classes('layer-arrow')
                    
                    item.on('click', lambda _, k=key, l=label, r=range_text, el=item: set_layer(k, l, r, el))
                
                ui.element(_TAG).classes('sidebar-divider')
                with ui.row().classes('wind-toggle-row w-full'):
                    ui.label('Hiệu ứng gió')
                    ui.switch(value=True).props('dense color="primary" size="sm"')

        def render_info_panel():
            with ui.element(_TAG).classes('info-panel panel-dark map-overlay'):
                with ui.column().classes('gap-1'):
                    ui_refs['info_title'] = ui.label(state['layer']['label']).classes('info-title')
                    ui.label('Vị trí đã chọn').classes('info-subtitle')
                    ui_refs['info_coords'] = ui.label(f"{lat:.4f}° N, {lon:.4f}° E").classes('info-coords')
                
                with ui.element(_TAG).classes('info-list'):
                    def info_row(label, icon, ref_key, default_val, icon_class=''):
                        with ui.element(_TAG).classes('info-row w-full'):
                            with ui.element(_TAG).classes('info-label-group'):
                                ui.icon(icon).classes(icon_class)
                                ui.label(label)
                            ui_refs[ref_key] = ui.label(default_val).classes('info-val')
                    
                    info_row('Lượng mưa', 'water_drop', 'info_precip', '12.4 mm (Trung bình)', 'icon-blue')
                    info_row('Nhiệt độ', 'thermostat', 'info_temp', '28.7 °C (Trung bình)', 'icon-red')
                    info_row('Áp suất', 'speed', 'info_pressure', '1006 hPa (Trung bình)', 'icon-green') 
                    info_row('Tốc độ gió', 'air', 'info_wind', '14.6 km/h (Trung bình)', 'icon-blue')
                    info_row('Hướng gió', 'explore', 'info_wind_dir', 'SE', 'icon-blue')
                    info_row('Độ ẩm', 'water_drop', 'info_humidity', '78 %', 'icon-blue')
                    info_row('Mây', 'cloud', 'info_cloud', '64 % (Trung bình)', 'icon-gray')
                    info_row('Tầm nhìn', 'visibility', 'info_visibility', '10 km', 'icon-gray')
                
                ui_refs['info_update'] = ui.label(f'Cập nhật: 07:00, 20/05/2026').classes('info-footer')

        def render_eye_button():
            with ui.element('button').classes('eye-btn map-overlay').on('click', toggle_layer_visibility):
                ui_refs['eye_btn_icon'] = ui.icon('visibility')

        def render_legend():
            with ui.element(_TAG).classes('legend-panel panel-dark map-overlay'):
                ui_refs['legend_title'] = ui.label('Lượng mưa (mm)').classes('legend-title')
                ui_refs['legend_gradient'] = ui.element(_TAG).classes('legend-gradient-bar')
                ui_refs['legend_ranges'] = ui.html('<div></div>')

        def render_timeline():
            with ui.element(_TAG).classes('timeline-panel panel-dark map-overlay'):
                with ui.element('button').classes('play-btn').on('click', toggle_play):
                    ui_refs['play_btn'] = ui.icon('play_arrow')
                
                d1, t1 = format_time(7)
                ui_refs['time_label_start'] = ui.html(f'<div class="timeline-date">{d1}</div><div class="timeline-time">{t1}</div>').classes('time-stack')
                
                with ui.element(_TAG).classes('slider-container'):
                    ui.element(_TAG).classes('ruler-bg')
                    with ui.element(_TAG).classes('ruler-labels'):
                        ui.label('00:00')
                        ui.label('06:00')
                        ui.label('07:00').style('color: #f8fafc; font-weight: bold;')
                        ui.label('12:00')
                        ui.label('18:00')
                        ui.label('23:00')
                    
                    ui_refs['time_slider'] = ui.slider(
                        min=0, max=23, value=7, step=1, on_change=on_slider_change
                    ).props('color="primary" track-color="transparent" dense').classes('w-full')
                
                d2, t2 = format_time(23)
                ui_refs['time_label_end'] = ui.html(f'<div class="timeline-date">{d2}</div><div class="timeline-time">{t2}</div>').classes('time-stack')

        # ==================== PAGE STRUCTURE ====================
        with ui.element(_TAG).classes('app-container'):
            navbar('/map')

            with ui.element(_TAG).classes('page-content map-page-wrapper'):
                with ui.element(_TAG).classes('map-container-full'):
                    render_map()
                    
                    with ui.element(_TAG).classes('map-overlay-wrapper'):
                        render_search_panel()
                        render_sidebar()
                        render_info_panel()
                        render_eye_button()
                        render_legend()
                        render_timeline()

        # ==================== TIMELINE PLAY TICKER ====================
        def timeline_step():
            if state['timeline']['playing']:
                new_val = (state['timeline']['offset'] + 1) % 24
                ui_refs['time_slider'].value = new_val

        # Periodic timer (ticks every 1.5 seconds to advance timeline hours)
        play_timer = ui.timer(1.5, timeline_step)

        # Initial Updates
        update_info_panel()
        update_legend()
