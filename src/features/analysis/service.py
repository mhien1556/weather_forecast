from src.common.api import fetch_air_quality, fetch_current, fetch_forecast
from src.common.utils import process_weather_data

from .charts import build_charts


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    try:
        current = fetch_current(api_key, city)
        lat, lon = current['coord']['lat'], current['coord']['lon']
        forecast = fetch_forecast(api_key, lat, lon)
        air_quality = fetch_air_quality(api_key, lat, lon)

        processed = process_weather_data({
            'current': current,
            'forecast': forecast,
            'air_quality': air_quality,
            'lat': lat,
            'lon': lon,
        })
        if not processed:
            return {'error': 'Không xử lý được dữ liệu'}

        processed['charts'] = build_charts(processed)
        return processed
    except Exception as e:
        return {'error': str(e)}
