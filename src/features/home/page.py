from nicegui import ui

from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar,
)
from src.common.config import API_KEY, get_city

from .service import get_data
from .widgets import render_dashboard, render_hero, render_metrics

_TAG = 'div'


def register():
    @ui.page('/')
    def home_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY trong .env'}

        with ui.element(_TAG).classes('app-container'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/')

            with ui.element(_TAG).classes('page-content content-wrapper'):
                if weather.get('error'):
                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                else:
                    city_search_section('/', weather)
                    render_hero(weather)
                    render_metrics(weather)
                    render_dashboard(weather)

            footer()
