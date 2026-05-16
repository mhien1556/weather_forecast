from ...utils import process_weather_data
import requests

def get_map_data(api_key, city="Hanoi"):
    base_url = "https://api.openweathermap.org/data/2.5"
    geo_params = {"q": city, "appid": api_key, "units": "metric", "lang": "vi"}
    
    try:
        current_r = requests.get(f"{base_url}/weather", params=geo_params, timeout=8)
        current_r.raise_for_status()
        current = current_r.json()
        
        lat, lon = current["coord"]["lat"], current["coord"]["lon"]
        
        processed = process_weather_data({
            "current": current, "lat": lat, "lon": lon
        })
        return processed
    except Exception as e:
        return {"error": str(e)}
