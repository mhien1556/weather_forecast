import os

from nicegui import app, ui

from .features import register_all

def run():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    app.add_static_files('/static', static_dir)
    
    register_all()
    secret = os.getenv('FLASK_SECRET_KEY', 'weathernow-dev-secret')
    ui.run(
        title='WeatherNow | Du bao thoi tiet',
        port=5000,
        reload=False,
        storage_secret=secret,
        dark=True,
    )
