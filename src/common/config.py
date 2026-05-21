import os
from dotenv import load_dotenv
from nicegui import app
from .utils import get_location_by_ip

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY', '')


def get_city() -> str:
    if 'city' not in app.storage.user:
        app.storage.user['city'] = get_location_by_ip()
    return app.storage.user['city']


def set_city(city: str) -> None:
    city = city.strip() or get_location_by_ip()
    app.storage.user['city'] = city
    # Tự động lưu lịch sử nếu đã đăng nhập
    user = app.storage.user.get('user')
    if user:
        try:
            from .user_store import add_history
            add_history(user['username'], city)
        except Exception:
            pass


def clear_city() -> None:
    app.storage.user.pop('city', None)


# ── Auth helpers ──────────────────────────────────────────────
def get_current_user() -> dict | None:
    return app.storage.user.get('user')


def set_current_user(user: dict) -> None:
    app.storage.user['user'] = {
        'username': user['username'],
        'name': user['name'],
        'email': user.get('email', ''),
        'avatar': user.get('avatar', user['name'][0].upper()),
    }


def logout_user() -> None:
    app.storage.user.pop('user', None)
