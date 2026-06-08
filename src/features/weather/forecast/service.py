from datetime import datetime, timedelta
from src.services.weather_api import fetch_current, fetch_forecast
from src.features.weather.components.charts_daily import create_precip_chart, create_temp_trend_chart
from src.common.utils import process_weather_data
from src.common.cache import get as cache_get, set as cache_set
from src.common.units import get_units
from .charts import create_detailed_chart


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    units = get_units()
    cache_key = f"forecast:{city.lower().strip()}:{units.get('unit_temp', 'C')}:{units.get('unit_pressure', 'hPa')}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    try:
        current = fetch_current(api_key, city)
        lat, lon = current['coord']['lat'], current['coord']['lon']
        forecast = fetch_forecast(api_key, lat, lon)

        processed = process_weather_data({
            'current': current, 'forecast': forecast, 'lat': lat, 'lon': lon,
        })
        if not processed:
            return {'error': 'Không xử lý được dữ liệu'}

        daily = processed.get('daily', [])
        while len(daily) < 7:
            last_day_date = datetime.strptime(daily[-1]['date'], '%Y-%m-%d') if daily else datetime.now()
            next_day = last_day_date + timedelta(days=1)
            day_num = next_day.weekday()
            day_name = 'Chủ nhật' if day_num == 6 else f'Thứ {day_num + 2}'
            mock_day = daily[-1].copy() if daily else {
                'temp_max': 30, 'temp_min': 25, 'lucide_icon': 'cloud',
                'description': 'không có dữ liệu', 'humidity_avg': 0, 'wind_avg': 0
            }
            mock_day['date'] = next_day.strftime('%Y-%m-%d')
            mock_day['day_name'] = day_name
            daily.append(mock_day)

        processed['charts'] = {
            'detailed': create_detailed_chart(daily),
            'temp_trend': create_temp_trend_chart(daily),
            'precip': create_precip_chart(daily),
        }
        cache_set(cache_key, processed)
        return processed
    except Exception as e:
        return {'error': str(e)}