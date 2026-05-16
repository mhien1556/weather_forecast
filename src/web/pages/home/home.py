from ...utils import process_weather_data
from ...charts import create_hourly_chart, create_temp_trend_chart, create_precip_chart
import requests
import os

def get_home_data(api_key, city="Hanoi"):
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
        
        aqi_r = requests.get(f"{base_url}/air_pollution", params={"lat": lat, "lon": lon, "appid": api_key}, timeout=8)
        air_quality = aqi_r.json() if aqi_r.ok else None
        
        uv_r = requests.get(f"{base_url}/uvi", params={"lat": lat, "lon": lon, "appid": api_key}, timeout=8)
        uv_index = uv_r.json().get("value") if uv_r.ok else None
        
        processed = process_weather_data({
            "current": current, "forecast": forecast, "air_quality": air_quality, "uv_index": uv_index, "lat": lat, "lon": lon
        })
        
        processed['charts'] = {
            'hourly': create_hourly_chart(processed.get('hourly')),
            'temp_trend': create_temp_trend_chart(processed.get('daily')),
            'precip': create_precip_chart(processed.get('daily'))
        }
        return processed
    except Exception as e:
        return {"error": str(e)}
