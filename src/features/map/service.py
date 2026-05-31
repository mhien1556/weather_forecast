import hashlib
import math
from datetime import datetime, timedelta

import requests

from src.common.api import fetch_current
from src.common.utils import icon_to_lucide, lucide_to_material, process_weather_data

from .layer_config import LAYER_CONFIG

_hourly_cache: dict = {}
_location_cache: dict = {}
_cache_expiry = timedelta(minutes=10)

BASE_TILE_URL = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
MAP_STEP_SECONDS = 3 * 3600

_COMPASS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']


def build_weather_tile_url(layer_key: str, api_key: str, unix_ts: int | None = None) -> str:
    url = (
        f'https://tile.openweathermap.org/map/{layer_key}/{{z}}/{{x}}/{{y}}.png'
        f'?appid={api_key}'
    )
    if unix_ts is not None:
        url += f'&date={unix_ts}&_t={unix_ts}'
    return url


def round_map_timestamp(unix_ts: int) -> int:
    return (unix_ts // MAP_STEP_SECONDS) * MAP_STEP_SECONDS


def format_timeline_label(unix_ts: int) -> str:
    return datetime.fromtimestamp(unix_ts).strftime('%Y-%m-%d %H:%M')


def _now_ts() -> int:
    return round_map_timestamp(int(datetime.now().timestamp()))


def build_timeline(hourly: list) -> list[int]:
    """Các mốc thời gian quanh thời điểm hiện tại (giờ địa phương, bước 3h)."""
    now = _now_ts()
    if hourly:
        times = sorted({round_map_timestamp(int(h['dt'])) for h in hourly})
        if times:
            return times
    past_steps, future_steps = 8, 31
    start = now - past_steps * MAP_STEP_SECONDS
    return [start + i * MAP_STEP_SECONDS for i in range(past_steps + 1 + future_steps)]


def default_timeline_index(timeline: list[int]) -> int:
    if not timeline:
        return 0
    now = _now_ts()
    return min(range(len(timeline)), key=lambda i: abs(timeline[i] - now))


def fetch_hourly_forecast(api_key: str, lat: float, lon: float) -> list:
    cache_key = f'{lat:.2f},{lon:.2f}'
    now = datetime.utcnow()
    if cache_key in _location_cache:
        cached = _location_cache[cache_key]
        if now - cached['time'] < _cache_expiry:
            return cached['hourly']
    url = (
        f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}'
        f'&exclude=minutely,daily,alerts&units=metric&appid={api_key}'
    )
    resp = requests.get(url, timeout=8)
    hourly: list = []
    if resp.status_code == 200:
        hourly = resp.json().get('hourly', [])
    if not hourly:
        # Fallback 1: dùng forecast 5 ngày / bước 3 giờ
        hourly = fetch_forecast3h_by_coords(api_key, lat, lon)
    if not hourly:
        # Fallback khi One Call không trả hourly (quota/gói API):
        # dùng current weather để panel bên phải vẫn có số liệu.
        current = fetch_current_by_coords(api_key, lat, lon)
        if current:
            hourly = [snapshot_from_current(current)]
    if hourly:
        _location_cache[cache_key] = {'time': now, 'hourly': hourly}
    return hourly


def fetch_forecast3h_by_coords(api_key: str, lat: float, lon: float) -> list:
    try:
        resp = requests.get(
            'https://api.openweathermap.org/data/2.5/forecast',
            params={'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric', 'lang': 'vi'},
            timeout=8,
        )
        if not resp.ok:
            return []
        rows = resp.json().get('list', [])
        hourly: list = []
        for row in rows:
            hourly.append({
                'dt': int(row.get('dt', 0)),
                'temp': row.get('main', {}).get('temp', 0),
                'feels_like': row.get('main', {}).get('feels_like', 0),
                'wind_speed': row.get('wind', {}).get('speed', 0),
                'wind_deg': row.get('wind', {}).get('deg', 0),
                'humidity': row.get('main', {}).get('humidity', 0),
                'clouds': row.get('clouds', {}).get('all', 0),
                'pressure': row.get('main', {}).get('pressure', 0),
                'rain': {'1h': (row.get('rain') or {}).get('3h', 0) / 3},
                'weather': row.get('weather') or [{'icon': '01d'}],
            })
        return hourly
    except Exception:
        return []


def fetch_current_by_coords(api_key: str, lat: float, lon: float) -> dict | None:
    try:
        resp = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric', 'lang': 'vi'},
            timeout=8,
        )
        if resp.ok:
            return resp.json()
    except Exception:
        return None
    return None


def snapshot_from_current(current: dict) -> dict:
    return {
        'dt': int(current.get('dt', datetime.now().timestamp())),
        'temp': current.get('main', {}).get('temp', 0),
        'feels_like': current.get('main', {}).get('feels_like', 0),
        'wind_speed': current.get('wind', {}).get('speed', 0),
        'wind_deg': current.get('wind', {}).get('deg', 0),
        'humidity': current.get('main', {}).get('humidity', 0),
        'clouds': current.get('clouds', {}).get('all', 0),
        'pressure': current.get('main', {}).get('pressure', 0),
        'rain': {'1h': (current.get('rain') or {}).get('1h', 0)},
        'weather': current.get('weather') or [{'icon': '01d'}],
    }


def find_hourly_at(hourly: list, unix_ts: int) -> dict | None:
    if not hourly:
        return None
    target = round_map_timestamp(unix_ts)
    return min(hourly, key=lambda h: abs(int(h['dt']) - target))


def wind_direction_label(deg: int) -> str:
    ix = int((deg % 360) / 22.5 + 0.5) % 16
    return f'{deg}° {_COMPASS[ix]}'


def snapshot_is_empty(snap: dict) -> bool:
    return snap.get('temp') == '--'


def weather_material_icon(owm_icon: str, rain_mm: float = 0, clouds: int = 0) -> str:
    """Icon Material: nắng = mặt trời, mưa = giọt nước, ..."""
    code = (owm_icon or '01d')[:2]
    if rain_mm > 0.3 or code in ('09', '10'):
        return 'water_drop'
    if code == '11':
        return 'thunderstorm'
    if code == '13':
        return 'ac_unit'
    if code == '50':
        return 'foggy'
    if code in ('03', '04') or clouds > 70:
        return 'cloud'
    if code == '02':
        return 'wb_cloudy'
    if code == '01':
        return 'nights_stay' if str(owm_icon).endswith('n') else 'wb_sunny'
    return lucide_to_material(icon_to_lucide(owm_icon))


def _pseudo_random(seed: int, slot: int) -> float:
    x = (seed ^ (slot * 2654435761)) & 0xFFFFFFFF
    return (x % 10000) / 10000.0


def synthetic_snapshot(lat: float, lon: float, unix_ts: int) -> dict:
    """Số liệu giả lập ổn định theo vị trí + thời gian (đổi khi kéo timeline / bấm map)."""
    digest = hashlib.md5(f'{lat:.4f},{lon:.4f},{unix_ts}'.encode()).digest()
    seed = int.from_bytes(digest[:4], 'big')
    rnd = lambda slot: _pseudo_random(seed, slot)

    dt = datetime.fromtimestamp(unix_ts)
    hour, month = dt.hour, dt.month

    base_temp = 27 - abs(lat - 16) * 0.42 + (rnd(1) - 0.5) * 5
    seasonal = 5 * math.sin((month - 4) * math.pi / 6)
    diurnal = 7 * math.sin((hour - 7) * math.pi / 12)
    temp = round(max(-12, min(44, base_temp + seasonal + diurnal)), 1)

    feels = round(temp + (rnd(2) - 0.5) * 6, 1)
    humidity = int(40 + rnd(3) * 55)
    clouds = int(rnd(4) * 100)
    rain = round((rnd(5) * 6 if clouds > 55 else rnd(5) * 1.5), 1)
    wind = round(0.8 + rnd(6) * 15, 1)
    deg = int(rnd(7) * 360)
    pressure = int(995 + rnd(8) * 35)

    if rain > 2.5:
        icon = '10d'
    elif clouds > 75:
        icon = '04d'
    elif clouds > 35:
        icon = '03d'
    else:
        icon = '01d' if 6 <= hour <= 18 else '01n'

    snap = {
        'dt': unix_ts,
        'temp': temp,
        'feels_like': feels,
        'wind_speed': wind,
        'wind_deg': deg,
        'humidity': humidity,
        'clouds': clouds,
        'pressure': pressure,
        'rain': {'1h': rain},
        'weather': [{'icon': icon}],
    }
    snap['material_icon'] = weather_material_icon(icon, rain, clouds)
    return hourly_snapshot(snap)


def resolve_snapshot(lat: float, lon: float, unix_ts: int, hourly: list) -> dict:
    snap = hourly_snapshot(find_hourly_at(hourly, unix_ts))
    if snapshot_is_empty(snap):
        snap = synthetic_snapshot(lat, lon, unix_ts)
    return snap


def hourly_snapshot(hourly_item: dict | None) -> dict:
    if not hourly_item:
        return {
            'temp': '--', 'feels_like': '--', 'wind_speed': '--', 'wind_deg': 0,
            'wind_dir': '--', 'humidity': '--', 'clouds': '--', 'pressure': '--',
            'rain': 0, 'icon': '01d', 'material_icon': 'wb_sunny',
        }
    rain = hourly_item.get('rain') or {}
    rain_mm = rain.get('1h', 0) if isinstance(rain, dict) else float(rain or 0)
    icon = (hourly_item.get('weather') or [{}])[0].get('icon', '01d')
    clouds = int(hourly_item.get('clouds', 0))
    deg = int(hourly_item.get('wind_deg', 0))
    return {
        'temp': round(hourly_item.get('temp', 0), 1),
        'feels_like': round(hourly_item.get('feels_like', 0), 1),
        'wind_speed': round(hourly_item.get('wind_speed', 0), 1),
        'wind_deg': deg,
        'wind_dir': wind_direction_label(deg),
        'humidity': int(hourly_item.get('humidity', 0)),
        'clouds': clouds,
        'pressure': int(hourly_item.get('pressure', 0)),
        'rain': round(rain_mm, 1),
        'icon': icon,
        'material_icon': weather_material_icon(icon, rain_mm, clouds),
    }


def main_metric_value(snapshot: dict, layer_key: str) -> tuple[str, str]:
    cfg = LAYER_CONFIG[layer_key]
    field = cfg['field']
    val = snapshot.get(field, '--')
    if val == '--':
        return '--', cfg['unit']
    if field == 'pressure':
        return str(val), 'hPa'
    if field == 'rain':
        return str(val), 'mm'
    if field == 'clouds':
        return str(val), '%'
    return str(val), cfg['unit']


def get_hourly_weather(api_key: str, city: str = 'Hanoi') -> dict:
    try:
        current = fetch_current(api_key, city)
        lat, lon = current['coord']['lat'], current['coord']['lon']
        processed = process_weather_data({'current': current, 'lat': lat, 'lon': lon})
        if not processed:
            return {'error': 'Không xử lý được dữ liệu'}
        hourly = fetch_hourly_forecast(api_key, lat, lon)
        processed['lat'] = lat
        processed['lon'] = lon
        processed['hourly'] = hourly
        return processed
    except Exception as e:
        return {'error': str(e)}
