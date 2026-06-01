import os
from pathlib import Path

from dotenv import load_dotenv
from nicegui import app

from .utils import get_location_by_ip

_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT / '.env')

API_KEY = os.getenv('OPENWEATHER_API_KEY', '').strip()


def get_city() -> str:
    if 'city' not in app.storage.user:
        app.storage.user['city'] = get_location_by_ip()
    return app.storage.user['city']


def set_city(city: str) -> None:
    app.storage.user['city'] = city.strip() or get_location_by_ip()

def clear_city() -> None:
    app.storage.user.pop('city', None)
