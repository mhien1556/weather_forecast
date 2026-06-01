from nicegui import ui

from src.common.components import (
    apply_theme, footer, hero_background, navbar,
)
from src.common.config import API_KEY, get_city
from src.features.home.service import get_data

from .widgets import render_settings_content

_TAG = 'div'


def register():
    @ui.page('/settings')
    def settings_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

        with ui.element(_TAG).classes('app-container'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/settings')

            with ui.element(_TAG).classes('page-content content-wrapper'):
                with ui.element(_TAG).classes('page-header'):
                    ui.label('Cấu hình ứng dụng').classes('text-h4').style('font-weight:700;margin:0')
                    ui.label('Tùy chỉnh đơn vị, giao diện và thiết lập cá nhân').style('opacity:0.7')
                render_settings_content()

            footer()
