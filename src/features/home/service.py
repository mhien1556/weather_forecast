from src.common.api import fetch_air_quality, fetch_current, fetch_forecast, fetch_uv_index
from src.common.charts_daily import create_precip_chart, create_temp_trend_chart
from src.common.utils import process_weather_data

from .charts import create_hourly_chart


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    try:
        current = fetch_current(api_key, city)
        lat, lon = current['coord']['lat'], current['coord']['lon']

        forecast = fetch_forecast(api_key, lat, lon)
        air_quality = fetch_air_quality(api_key, lat, lon)
        uv_index = fetch_uv_index(api_key, lat, lon)

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

        processed['charts'] = {
            'hourly': create_hourly_chart(processed.get('hourly')),
            'temp_trend': create_temp_trend_chart(processed.get('daily')),
            'precip': create_precip_chart(processed.get('daily')),
        }
        return processed
    except Exception as e:
        return {'error': str(e)}
