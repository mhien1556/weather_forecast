from src.services.weather_api import fetch_air_quality, fetch_current, fetch_forecast
from src.common.utils import process_weather_data
from src.common.cache import get as cache_get, set as cache_set

from .charts import build_charts


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    cache_key = f'analysis:{city.lower().strip()}'
    cached = cache_get(cache_key)
    if cached:
        return cached

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
        cache_set(cache_key, processed)
        return processed
    except Exception as e:
        return {'error': str(e)}