import os
import logging
from nicegui import app, ui

from .features import register_all
from src.features.user_management.admin.page import AdminPage


# Dùng chung 1 instance để tránh tạo nhiều object
_admin = AdminPage()

ui.page('/admin')(lambda: _admin.create())
ui.page('/admin/user/{username}')(lambda username: _admin.view_user_detail(username))
ui.page('/admin/edit/{username}')(lambda username: _admin.edit_user_dialog(username))

def run():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    app.add_static_files('/static', static_dir)

    # Cấu hình API không còn dùng nữa
    register_all()

    # ── TẮT CÁC LOG KẾT NỐI PHIỀN PHỨC CỦA NICEGUI & UVICORN ─────────────────
    logging.getLogger('uvicorn.error').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('nicegui').setLevel(logging.WARNING)
    # ─────────────────────────────────────────────────────────────────────────

    secret = os.getenv('STORAGE_SECRET', 'weathernow-super-secret-key-2024')
    ui.run(
        title='WeatherForecast | Quản trị',
        port=5001,
        host='0.0.0.0',
        reload=False, 
        storage_secret=secret,
        dark=True,
        reconnect_timeout=30,
    )