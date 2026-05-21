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


# Add function to fetch weather data for a specific time and layer
def get_weather_by_time_and_layer(api_key: str, lat: float, lon: float, layer: str, time_offset: int) -> dict:
    try:
        # Simulate fetching weather data for a specific time and layer
        # Replace with actual API logic if available
        return {
            'layer': layer,
            'time_offset': time_offset,
            'data': {
                'temperature': 25 + time_offset * 0.5,
                'rain': 2.5,
                'wind_speed': 10 + time_offset * 0.2,
                'pressure': 1010 - time_offset * 0.1,
                'clouds': 50 + time_offset * 2,
            }
        }
    except Exception as e:
        return {'error': str(e)}
