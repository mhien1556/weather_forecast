import os
import socket

from nicegui import app, ui

from .features import register_all

_FALLBACK_PORTS = (8080, 5001, 5050, 8765, 8888)


def pick_port(preferred: int) -> int:
    """Chọn cổng trống; tránh WinError 10013/10048 khi 5000 bị chiếm hoặc bị chặn."""
    candidates = [preferred, *_FALLBACK_PORTS]
    seen: set[int] = set()
    for port in candidates:
        if port in seen:
            continue
        seen.add(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    raise RuntimeError(
        'No free port. Close other apps or set PORT env (e.g. PORT=9000).'
    )


def run():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    app.add_static_files('/static', static_dir)

    register_all()
    preferred = int(os.getenv('PORT', '8080'))
    port = int(os.getenv('WEATHERNOW_PORT') or 0)
    if not port:
        port = pick_port(preferred)
        os.environ['WEATHERNOW_PORT'] = str(port)
    if port != preferred:
        print(f'Port {preferred} busy, using http://localhost:{port}')

    secret = os.getenv('FLASK_SECRET_KEY', 'weathernow-dev-secret')
    print(f'WeatherNow: http://localhost:{port}')
    ui.run(
        title='WeatherNow | Du bao thoi tiet',
        port=port,
        reload=True,
        storage_secret=secret,
        dark=True,
    )
