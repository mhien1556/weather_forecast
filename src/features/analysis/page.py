from nicegui import ui

from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar, plotly_chart,
)
from src.common.config import API_KEY, get_city
from src.common.units import RefreshRegistry, get_units, convert_temp

from .service import get_data
from .widgets import render_stat_card
from .charts import build_charts

_TAG = 'div'


def register():
    @ui.page('/analysis')
    def analysis_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

        with ui.element(_TAG).classes('app-container'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/analysis')

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
                            city_search_section('/analysis', weather)
                            with ui.element(_TAG).classes('page-header'):
                                ui.label('Phân tích chuyên sâu').classes('text-h4').style('font-weight:700;margin:0')
                                ui.label(
                                    f'Xu hướng và thống kê khí tượng tại {weather.get("city_name", "N/A")}'
                                ).style('opacity:0.7')

                            # Re-generate analysis charts with active temperature unit
                            charts = build_charts(weather)
                            stats = weather.get('stats', {})

                            with ui.element(_TAG).classes('analysis-row'):
                                with ui.element(_TAG).classes('card'):
                                    ui.label('So sánh nhiệt độ (7 ngày)').classes('text-h6 mb-4')
                                    plotly_chart(charts.get('monthly'))
                                with ui.element(_TAG).classes('card'):
                                    ui.label('Phân bổ chất lượng không khí').classes('text-h6 mb-4')
                                    plotly_chart(charts.get('aqi_dist'))

                            with ui.element(_TAG).classes('card'):
                                ui.label('Xác suất hiện tượng thời tiết đặc biệt').classes('text-h6 mb-4')
                                plotly_chart(charts.get('events'))

                            u_temp = get_units()['unit_temp']
                            avg_temp_raw = stats.get("avg_temp", "--")
                            if avg_temp_raw != "--" and avg_temp_raw is not None:
                                avg_temp_val = convert_temp(avg_temp_raw, u_temp)
                            else:
                                avg_temp_val = "--"
                            temp_sym = '°F' if u_temp == 'F' else '°C'

                            with ui.element(_TAG).classes('analysis-metrics'):
                                render_stat_card(
                                    'Nhiệt độ trung bình',
                                    f'{avg_temp_val}{temp_sym}',
                                    '+1.2° so với tuần trước', True,
                                )
                                render_stat_card(
                                    'Tổng lượng mưa dự kiến',
                                    f'{stats.get("total_rain", "--")} mm',
                                    '-15% so với tuần trước', False,
                                )
                                sunny_h = stats.get('sunny_days', 0) * 3 if stats else '--'
                                render_stat_card(
                                    'Số giờ nắng dự kiến', f'{sunny_h}h',
                                    '+3h so với tuần trước', True,
                                )

                    footer()

                draw_content()

            # Register for real-time UI updates
            client_id = ui.context.client.id
            RefreshRegistry.register(client_id, draw_content.refresh)
            ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
