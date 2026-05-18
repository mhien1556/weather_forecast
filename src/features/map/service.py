from src.common.api import fetch_current
from src.common.utils import process_weather_data


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    try:
        current = fetch_current(api_key, city)
        lat, lon = current['coord']['lat'], current['coord']['lon']
        processed = process_weather_data({'current': current, 'lat': lat, 'lon': lon})
        if not processed:
            return {'error': 'Không xử lý được dữ liệu'}
        return processed
    except Exception as e:
        return {'error': str(e)}
