from nicegui import ui

from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar, plotly_chart,
)
from src.common.config import API_KEY, get_city
from src.common.units import RefreshRegistry

from .service import get_data
from .widgets import render_daily_cards
from .charts import create_detailed_chart

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

            content_container = ui.element(_TAG).classes('w-full')
            with content_container:
                @ui.refreshable
                def draw_content():
                    nonlocal weather
                    current_city = get_city()
                    # If user updated default city in settings drawer, reload weather data
                    if not weather.get('error') and weather.get('city_name', '').split(',')[0].strip().lower() != current_city.split(',')[0].strip().lower():
                        weather = get_data(API_KEY, current_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
                    
                    # Re-apply theme
                    apply_theme()

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
                            
                            # Re-generate detailed forecast chart with the active temperature unit
                            detailed_chart = create_detailed_chart(weather.get('daily', []))
                            with ui.element(_TAG).classes('card'):
                                ui.label('Biến thiên nhiệt độ & Lượng mưa').classes('text-h6 mb-4')
                                plotly_chart(detailed_chart)

                    footer()

                draw_content()

            # Register for real-time UI updates
            client_id = ui.context.client.id
            RefreshRegistry.register(client_id, draw_content.refresh)
            ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
