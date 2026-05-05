import requests
from config import API_KEY, BASE_URL

def get_current_weather(city: str) -> dict:
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "vi"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_forecast_5days(city: str) -> dict:
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "vi"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()