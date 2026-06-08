from nicegui import app, ui

from src.common.components import (
    apply_theme, footer,
    hero_background, navbar,
)
from src.common.config import API_KEY, get_city

from .service import get_data
from .widgets import render_analysis_page

_TAG = 'div'


def register():
    @ui.page('/analysis')
    def analysis_page(city: str = None):
        selected_city = city if city else app.storage.user.get('current_city', get_city())
        weather = get_data(API_KEY, selected_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

        apply_theme(weather)

        with ui.element(_TAG).classes('app-container map-app'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/analysis')

            with ui.element(_TAG).classes('page-content content-wrapper'):
                if weather.get('error'):
                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                else:
                    render_analysis_page(weather)

            footer()