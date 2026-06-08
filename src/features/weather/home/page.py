from nicegui import ui

from src.common.components import (
    apply_theme, footer,
    hero_background, navbar,
)
from src.common.config import API_KEY, get_city, get_current_user

from .service import get_data
from .widgets import render_dashboard, render_hero, render_metrics

_TAG = 'div'

def register():
    @ui.page('/')
    def home_page():
        apply_theme()

        # Logic đăng nhập (giữ nguyên của bạn)
        # if not get_current_user():
        #    ui.navigate.to('/login')
        #    return

        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY trong .env'}

        with ui.element(_TAG).classes('app-container map-app'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/')

            with ui.column().classes('page-content w-full items-center').style('gap:0'):
                if weather.get('error'):
                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                else:
                    user = get_current_user()
                    render_hero(weather)
                    render_metrics(weather)
                    render_dashboard(weather)

        footer()