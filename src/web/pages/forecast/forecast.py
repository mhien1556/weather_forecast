from ...utils import process_weather_data
from ...charts import create_detailed_forecast_chart, create_temp_trend_chart, create_precip_chart
import requests

def get_forecast_data(api_key, city="Hanoi"):
    base_url = "https://api.openweathermap.org/data/2.5"
    geo_params = {"q": city, "appid": api_key, "units": "metric", "lang": "vi"}
    
    try:
        current_r = requests.get(f"{base_url}/weather", params=geo_params, timeout=8)
        current_r.raise_for_status()
        current = current_r.json()
        
        lat, lon = current["coord"]["lat"], current["coord"]["lon"]
        coord_params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "vi"}
        
        forecast_r = requests.get(f"{base_url}/forecast", params=coord_params, timeout=8)
        forecast = forecast_r.json()
        
        processed = process_weather_data({
            "current": current, "forecast": forecast, "lat": lat, "lon": lon
        })
        
        processed['charts'] = {
            'detailed': create_detailed_forecast_chart(processed.get('daily')),
            'temp_trend': create_temp_trend_chart(processed.get('daily')),
            'precip': create_precip_chart(processed.get('daily'))
        }
        return processed
    except Exception as e:
        return {"error": str(e)}
