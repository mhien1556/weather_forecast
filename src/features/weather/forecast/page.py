from nicegui import app, ui

from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar, plotly_chart,
)
from src.common.config import API_KEY, get_city

from .service import get_data
from .widgets import render_forecast_page  # ← đổi từ render_daily_cards

_TAG = 'div'


def register():
    @ui.page('/forecast')
    def forecast_page(city: str = None):
        apply_theme()

        selected_city = city if city else app.storage.user.get('current_city', get_city())
        weather = get_data(API_KEY, selected_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

        with ui.element(_TAG).classes('app-container map-app'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/forecast')

            with ui.element(_TAG).classes('page-content content-wrapper'):
                if weather.get('error'):
                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                else:
                    city_search_section('/forecast', weather)
                    # ← render_forecast_page xử lý toàn bộ: tiêu đề + cards + charts
                    render_forecast_page(weather)  # ← thay thế toàn bộ phần dưới

            footer()