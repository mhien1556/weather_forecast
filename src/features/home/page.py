from nicegui import ui

from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar,
)
from src.common.config import API_KEY, get_city
from src.common.units import RefreshRegistry

from .service import get_data
from .widgets import render_dashboard, render_hero, render_metrics
from .charts import create_hourly_chart
from src.common.charts_daily import create_temp_trend_chart, create_precip_chart

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

            content_container = ui.element(_TAG).classes('w-full')
            with content_container:
                @ui.refreshable
                def draw_content():
                    nonlocal weather
                    current_city = get_city()
                    # If user updated default city in settings drawer, reload weather data
                    if not weather.get('error') and weather.get('city_name', '').split(',')[0].strip().lower() != current_city.split(',')[0].strip().lower():
                        weather = get_data(API_KEY, current_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
                    
                    # Re-apply theme and dynamic background state
                    apply_theme()

                    with ui.element(_TAG).classes('page-content content-wrapper'):
                        if weather.get('error'):
                            ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                        else:
                            # Re-generate home charts with the active units
                            if 'charts' in weather:
                                weather['charts']['hourly'] = create_hourly_chart(weather.get('hourly', []))
                                weather['charts']['temp_trend'] = create_temp_trend_chart(weather.get('daily', []))
                                weather['charts']['precip'] = create_precip_chart(weather.get('daily', []))
                            
                            city_search_section('/', weather)
                            render_hero(weather)
                            render_metrics(weather)
                            render_dashboard(weather)
                    
                    footer()

                draw_content()

            # Register for real-time UI updates
            client_id = ui.context.client.id
            RefreshRegistry.register(client_id, draw_content.refresh)
            ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
