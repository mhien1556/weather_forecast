"""
API fetch functions for WeatherNow.
All responses are cached with Streamlit's cache_data.
"""

import sys
import os

# Ensure project root is on sys.path so `config` can always be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import streamlit as st
from config import API_KEY, BASE_URL


def _get(url: str, params: dict, timeout: int = 10) -> dict:
    """Shared GET helper — raises on HTTP error."""
    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=60, show_spinner=False)
def get_current_weather(city: str) -> dict:
    return _get(
        f"{BASE_URL}/weather",
        {"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"},
    )


@st.cache_data(ttl=60, show_spinner=False)
def get_forecast_5days(city: str) -> dict:
    return _get(
        f"{BASE_URL}/forecast",
        {"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"},
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_air_quality(lat: float, lon: float) -> dict:
    try:
        return _get(
            f"{BASE_URL}/air_pollution",
            {"lat": lat, "lon": lon, "appid": API_KEY},
        )
    except Exception:
        return {}


@st.cache_data(ttl=300, show_spinner=False)
def get_uv_index(lat: float, lon: float) -> float | None:
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/3.0/onecall",
            params={
                "lat": lat,
                "lon": lon,
                "exclude": "minutely,hourly,daily,alerts",
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json().get("current", {}).get("uvi")
    except Exception:
        pass
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def geocode_city(city: str) -> dict | None:
    try:
        results = _get(
            "http://api.openweathermap.org/geo/1.0/direct",
            {"q": city, "limit": 1, "appid": API_KEY},
        )
        if results:
            return {"lat": results[0]["lat"], "lon": results[0]["lon"]}
    except Exception:
        pass
    return None
