from src.common.api import fetch_current, fetch_forecast
from src.common.charts_daily import create_precip_chart, create_temp_trend_chart
from src.common.utils import process_weather_data

from .charts import create_detailed_chart


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
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
        processed['charts'] = {
            'detailed': create_detailed_chart(daily),
            'temp_trend': create_temp_trend_chart(daily),
            'precip': create_precip_chart(daily),
        }
        return processed
    except Exception as e:
        return {'error': str(e)}
