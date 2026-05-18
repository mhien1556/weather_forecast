import requests

BASE_URL = 'https://api.openweathermap.org/data/2.5'


def fetch_current(api_key: str, city: str) -> dict:
    params = {'q': city, 'appid': api_key, 'units': 'metric', 'lang': 'vi'}
    r = requests.get(f'{BASE_URL}/weather', params=params, timeout=8)
    r.raise_for_status()
    return r.json()


def fetch_forecast(api_key: str, lat: float, lon: float) -> dict:
    params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric', 'lang': 'vi'}
    r = requests.get(f'{BASE_URL}/forecast', params=params, timeout=8)
    r.raise_for_status()
    return r.json()


def fetch_air_quality(api_key: str, lat: float, lon: float):
    r = requests.get(
        f'{BASE_URL}/air_pollution',
        params={'lat': lat, 'lon': lon, 'appid': api_key},
        timeout=8,
    )
    return r.json() if r.ok else None


def fetch_uv_index(api_key: str, lat: float, lon: float):
    r = requests.get(
        f'{BASE_URL}/uvi',
        params={'lat': lat, 'lon': lon, 'appid': api_key},
        timeout=8,
    )
    return r.json().get('value') if r.ok else None
