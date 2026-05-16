from ...utils import process_weather_data
from ...charts import create_analysis_charts
import requests

def get_analysis_data(api_key, city="Hanoi"):
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
        
        processed = process_weather_data({
            "current": current, "forecast": forecast, "air_quality": air_quality, "lat": lat, "lon": lon
        })
        
        processed['charts'] = create_analysis_charts(processed)
        return processed
    except Exception as e:
        return {"error": str(e)}
