from src.services.weather_api import fetch_air_quality, fetch_current, fetch_forecast, fetch_uv_index
from src.features.weather.components.charts_daily import create_precip_chart
from src.common.utils import process_weather_data

from .charts import create_hourly_chart, create_temp_trend_chart


def _map_weather_icon(icon_code: str) -> str:
    """Map OpenWeatherMap icon code to icon name"""
    if not icon_code:
        return 'partly_cloudy_day'
    
    code = icon_code[:2]
    
    icon_map = {
        '01': 'sunny',              # clear sky
        '02': 'partly_cloudy_day', # few clouds
        '03': 'cloud',             # scattered clouds
        '04': 'cloud',             # broken clouds
        '09': 'rainy',             # shower rain
        '10': 'rainy',             # rain
        '11': 'thunderstorm',      # thunderstorm
        '13': 'ac_unit',           # snow
        '50': 'mist',              # mist/fog
    }
    
    return icon_map.get(code, 'partly_cloudy_day')


def _enrich_hourly(hourly_data: list, raw_forecast: dict) -> list:
    """Đảm bảo mỗi entry hourly có đủ humidity, pop và icon."""
    if not hourly_data:
        return hourly_data

    # Tạo lookup từ raw forecast list (key = time string)
    raw_map = {}
    try:
        for item in raw_forecast.get('list', []):
            import datetime
            dt = datetime.datetime.fromtimestamp(item['dt'])
            key = dt.strftime('%H:%M')
            raw_map[key] = item
    except Exception:
        pass

    enriched = []
    for h in hourly_data:
        entry = dict(h)
        time_key = entry.get('time', '')
        raw = raw_map.get(time_key, {})

        # humidity: thử lấy từ entry trước, fallback raw forecast
        if 'humidity' not in entry or entry['humidity'] is None:
            entry['humidity'] = raw.get('main', {}).get('humidity', 0)

        # pop (probability of precipitation): 0.0–1.0 trong raw forecast
        if 'pop' not in entry or entry['pop'] is None:
            raw_pop = raw.get('pop', 0)
            entry['pop'] = raw_pop

        # icon: lấy từ raw forecast
        if 'icon' not in entry or not entry['icon']:
            weather_data = raw.get('weather', [{}])[0] if raw.get('weather') else {}
            icon_code = weather_data.get('icon', '')
            entry['icon'] = _map_weather_icon(icon_code)

        enriched.append(entry)
    return enriched


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    try:
        current = fetch_current(api_key, city)
        if not current or 'coord' not in current:
            return {'error': 'Không tìm thấy thành phố'}

        lat, lon = current['coord']['lat'], current['coord']['lon']

        forecast    = fetch_forecast(api_key, lat, lon)
        air_quality = fetch_air_quality(api_key, lat, lon)
        uv_index    = fetch_uv_index(api_key, lat, lon)

        processed = process_weather_data({
            'current': current,
            'forecast': forecast,
            'air_quality': air_quality,
            'uv_index': uv_index,
            'lat': lat,
            'lon': lon,
        })
        if not processed:
            return {'error': 'Không xử lý được dữ liệu'}

        # ===== LẤY ICON TỪ CURRENT WEATHER =====
        current_weather = current.get('weather', [{}])[0] if current.get('weather') else {}
        current_icon_code = current_weather.get('icon', '')
        processed['icon'] = _map_weather_icon(current_icon_code)
        
        # Ghi đè lucide_icon cũ nếu có
        if 'lucide_icon' in processed:
            processed['lucide_icon'] = processed['icon']

        # ===== THÊM ICON CHO DAILY DATA =====
        daily_data = processed.get('daily', [])
        for day in daily_data:
            if 'icon' not in day or not day.get('icon'):
                # Thử lấy từ forecast data
                day_icon_code = day.get('icon_code', '')
                if day_icon_code:
                    day['icon'] = _map_weather_icon(day_icon_code)
                else:
                    # Fallback theo mô tả
                    desc = day.get('desc', '').lower()
                    if 'mưa' in desc:
                        day['icon'] = 'rainy'
                    elif 'nắng' in desc:
                        day['icon'] = 'sunny'
                    elif 'dông' in desc:
                        day['icon'] = 'thunderstorm'
                    else:
                        day['icon'] = 'partly_cloudy_day'

        # 🛠️ Bù ngày nếu thiếu (đủ 7 ngày)
        if len(daily_data) > 0 and len(daily_data) < 7:
            from datetime import datetime, timedelta
            viet_days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
            while len(daily_data) < 7:
                last_day = daily_data[-1]
                try:
                    last_date_obj = datetime.strptime(last_day['date'], '%Y-%m-%d')
                    next_date_obj = last_date_obj + timedelta(days=1)
                    next_date_str = next_date_obj.strftime('%Y-%m-%d')
                    next_day_name = viet_days[next_date_obj.weekday()]
                except Exception:
                    next_date_str = last_day['date']
                    next_day_name = 'Thứ 2'
                padded_day = last_day.copy()
                padded_day['date']     = next_date_str
                padded_day['day_name'] = next_day_name
                padded_day['temp_max'] = last_day['temp_max'] - 0.5
                padded_day['temp_min'] = last_day['temp_min'] + 0.5
                padded_day['icon']     = last_day.get('icon', 'partly_cloudy_day')
                daily_data.append(padded_day)

        print(f"\n[DEBUG] Daily data count after padding: {len(daily_data)}")
        if daily_data:
            print(f"[DEBUG] First day icon: '{daily_data[0].get('icon')}'")

        hourly_data = processed.get('hourly', [])
        print(f"[DEBUG] Hourly data count: {len(hourly_data)}\n")

        # Enrich hourly với humidity + pop + icon từ raw forecast nếu thiếu
        hourly_data = _enrich_hourly(hourly_data, forecast or {})

        processed['charts'] = {
            'hourly':     create_hourly_chart(hourly_data),
            'temp_trend': create_temp_trend_chart(daily_data),
            'precip':     create_precip_chart(daily_data),
        }
        return processed
    except Exception as e:
        print(f"[ERROR] get_data: {e}")
        import traceback
        traceback.print_exc()
        return {'error': f'Lỗi server: {str(e)}'}