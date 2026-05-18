from nicegui import ui

from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar, plotly_chart,
)
from src.common.config import API_KEY, get_city

from .service import get_data
from .widgets import render_daily_cards

_TAG = 'div'


def register():
    @ui.page('/forecast')
    def forecast_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

        with ui.element(_TAG).classes('app-container'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/forecast')

            with ui.element(_TAG).classes('page-content content-wrapper'):
                if weather.get('error'):
                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                else:
                    city_search_section('/forecast', weather)
                    with ui.element(_TAG).classes('page-header'):
                        ui.label('Dự báo chi tiết').classes('text-h4').style('font-weight:700;margin:0')
                        ui.label(
                            f'Thông tin thời tiết chuyên sâu cho 7 ngày tới tại {weather.get("city_name", "N/A")}'
                        ).style('opacity:0.7')
                    render_daily_cards(weather.get('daily', []))
                    with ui.element(_TAG).classes('card'):
                        ui.label('Biến thiên nhiệt độ & Lượng mưa').classes('text-h6 mb-4')
                        plotly_chart(weather.get('charts', {}).get('detailed'))

            footer()
