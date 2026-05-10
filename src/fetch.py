import requests
import streamlit as st
from config import API_KEY, BASE_URL

# ─────────────────────────────────────────────
# Cached API calls (60s TTL)
# ─────────────────────────────────────────────

@st.cache_data(ttl=60, show_spinner=False)
def get_current_weather(city: str) -> dict:
    url = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=60, show_spinner=False)
def get_forecast_5days(city: str) -> dict:
    url = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300, show_spinner=False)
def get_air_quality(lat: float, lon: float) -> dict:
    """Fetch Air Quality Index (AQI) from OpenWeatherMap Air Pollution API."""
    url = f"{BASE_URL}/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


@st.cache_data(ttl=300, show_spinner=False)
def get_uv_index(lat: float, lon: float) -> float | None:
    """Fetch UV index via One Call API 3.0 (or fallback to None)."""
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,daily,alerts",
        "appid": API_KEY,
        "units": "metric",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("current", {}).get("uvi")
    except Exception:
        pass
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def geocode_city(city: str) -> dict | None:
    """Return lat/lon for a city name using OWM Geocoding API."""
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": API_KEY}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        if results:
            return {"lat": results[0]["lat"], "lon": results[0]["lon"]}
    except Exception:
        pass
    return None