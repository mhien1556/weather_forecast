from nicegui import app, ui  # Hoặc dùng `from nicegui import ui` tùy theo Cách 1 hoặc Cách 2 ở bước trước

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
    def forecast_page(city: str = None):
        apply_theme()
        
        # Lấy thành phố theo logic đồng bộ đã chọn ở bước trước
        selected_city = city if city else app.storage.user.get('current_city', get_city())
        
        weather = get_data(API_KEY, selected_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

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
                    
                    # 1. Danh sách các thẻ thời tiết 7 ngày
                    render_daily_cards(weather.get('daily', []))
                    
                    # 2. Khối biểu đồ biến thiên nhiệt độ
                    # THAY ĐỔI: Thêm class 'mt-8' (hoặc 'mt-6') vào card để tạo khoảng cách với phần trên
                    with ui.element(_TAG).classes('card mt-8'):
                        ui.label('Biến thiên nhiệt độ & Lượng mưa').classes('text-h6 mb-4')
                        plotly_chart(weather.get('charts', {}).get('detailed'))

            footer()