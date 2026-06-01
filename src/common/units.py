"""
Hàm chuyển đổi và định dạng đơn vị đo lường.
Đọc cài đặt từ app.storage.user (lưu tại trang Settings).
"""
from nicegui import app


# ── Giá trị mặc định ──────────────────────────────────────────────────────────
_DEFAULTS = {
    'unit_temp':       'C',      # 'C' | 'F'
    'unit_wind':       'km/h',   # 'km/h' | 'm/s' | 'mph'
    'unit_pressure':   'hPa',    # 'hPa' | 'mmHg'
    'unit_visibility': 'km',     # 'km' | 'miles'
    'theme':           'dark',   # 'dark' | 'light'
}


def get_units() -> dict:
    """Trả về dict cài đặt đơn vị hiện tại từ storage."""
    return {k: app.storage.user.get(k, v) for k, v in _DEFAULTS.items()}


# ── Conversion ─────────────────────────────────────────────────────────────────

def convert_temp(celsius, unit: str = 'C'):
    """Celsius → đơn vị được chọn."""
    if celsius is None or celsius == '--':
        return '--'
    c = float(celsius)
    if unit == 'F':
        return round(c * 9 / 5 + 32, 1)
    return round(c, 1)


def convert_wind(kmh, unit: str = 'km/h'):
    """km/h → đơn vị được chọn."""
    if kmh is None or kmh == '--':
        return '--'
    v = float(kmh)
    if unit == 'm/s':
        return round(v / 3.6, 1)
    if unit == 'mph':
        return round(v / 1.60934, 1)
    return round(v, 1)


def convert_wind_from_ms(ms, unit: str = 'km/h'):
    """m/s → đơn vị được chọn (API OWM trả m/s)."""
    if ms is None or ms == '--':
        return '--'
    v = float(ms)
    if unit == 'm/s':
        return round(v, 1)
    if unit == 'mph':
        return round(v * 2.23694, 1)
    # km/h
    return round(v * 3.6, 1)


def convert_pressure(hpa, unit: str = 'hPa'):
    """hPa → đơn vị được chọn."""
    if hpa is None or hpa == '--':
        return '--'
    v = float(hpa)
    if unit == 'mmHg':
        return round(v * 0.750062, 1)
    return round(v, 1)


def convert_visibility(km, unit: str = 'km'):
    """km → đơn vị được chọn."""
    if km is None or km == '--':
        return '--'
    v = float(km)
    if unit == 'miles':
        return round(v / 1.60934, 1)
    return round(v, 1)


# ── Format helpers (trả chuỗi hoàn chỉnh với đơn vị) ─────────────────────────

def format_temp(celsius) -> str:
    units = get_units()
    u = units['unit_temp']
    sym = '°F' if u == 'F' else '°C'
    val = convert_temp(celsius, u)
    return f'{val}{sym}' if val != '--' else '--'


def format_wind_from_ms(ms) -> str:
    """API OWM trả m/s — dùng hàm này để format."""
    units = get_units()
    u = units['unit_wind']
    val = convert_wind_from_ms(ms, u)
    return f'{val} {u}' if val != '--' else '--'


def format_wind(kmh) -> str:
    """Nguồn dữ liệu đã ở km/h."""
    units = get_units()
    u = units['unit_wind']
    val = convert_wind(kmh, u)
    return f'{val} {u}' if val != '--' else '--'


def format_pressure(hpa) -> str:
    units = get_units()
    u = units['unit_pressure']
    val = convert_pressure(hpa, u)
    return f'{val} {u}' if val != '--' else '--'


def format_visibility(km) -> str:
    units = get_units()
    u = units['unit_visibility']
    val = convert_visibility(km, u)
    return f'{val} {u}' if val != '--' else '--'


# ── Refresh Registry for Real-Time Updates ──────────────────────────────────
class RefreshRegistry:
    _callbacks = {}  # client_id -> list of callbacks

    @classmethod
    def register(cls, client_id, callback):
        if client_id not in cls._callbacks:
            cls._callbacks[client_id] = []
        cls._callbacks[client_id].append(callback)

    @classmethod
    def trigger(cls, client_id):
        if client_id in cls._callbacks:
            for cb in cls._callbacks[client_id]:
                try:
                    cb()
                except Exception as e:
                    pass

    @classmethod
    def clear(cls, client_id):
        cls._callbacks.pop(client_id, None)

