from nicegui import ui
from datetime import datetime
from src.common.units import format_temp, format_wind_from_ms, get_units

# ── CSS GRID RESPONSIVE - ÉP TẤT CẢ CỘT NẰM TRÊN MỘT DÒNG TUYỆT ĐỐI ──
FC_CSS = """
/* Thiết kế chung cho mỗi thẻ ngày */
.fc-day-row {
    display: grid !important;
    grid-template-columns: 1.2fr 0.5fr 1.5fr 0.8fr 0.8fr 1fr 1fr 1fr 1fr 1.5fr !important;
    align-items: center;
    gap: 10px;
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 15px 20px !important;
    margin-bottom: 10px !important;
    transition: 0.3s;
}

/* Header bảng cũng phải đồng bộ */
.fc-header-row {
    display: grid !important;
    grid-template-columns: 1.2fr 0.5fr 1.5fr 0.8fr 0.8fr 1fr 1fr 1fr 1fr 1.5fr !important;
    padding: 0 20px 10px 20px;
    color: rgba(255,255,255,0.6);
    font-size: 0.8rem;
    font-weight: 600;
}

.fc-badge {
    padding: 4px 8px;
    border-radius: 6px;
    background: rgba(0, 0, 0, 0.2);
    text-align: center;
    font-size: 0.75rem;
}
"""

def render_forecast_page(weather: dict):
    """Trang dự báo thời tiết 7 ngày - Thiết kế chuẩn Grid hiện đại"""
    ui.add_css(FC_CSS)
    
    daily_list = weather.get('daily', [])
    city_name = weather.get('city_name', 'Hà Nội')
    
    if not daily_list:
        with ui.element('div').classes('fc-container'):
            ui.label('Không có dữ liệu dự báo.').classes('text-center text-white')
        return

    # Lấy đơn vị áp suất từ cài đặt người dùng
    p_unit = get_units().get('unit_pressure', 'hPa')

    with ui.element('div').classes('fc-container'):
        # ===== TIÊU ĐỀ TRANG =====
        with ui.element('div').classes('w-full bg-white/5 backdrop-blur-md rounded-2xl border border-white/10 p-6 mb-6 text-center'):
            ui.label('DỰ BÁO THỜI TIẾT 7 NGÀY').classes('text-2xl font-bold text-white tracking-wider')
            with ui.row().classes('items-center justify-center gap-2 mt-2'):
                ui.icon('location_on', color='white', size='18px').classes('opacity-70')
                ui.label(f'{city_name}').classes('text-blue-300 font-medium')

        # ===== HEADER BẢNG =====
        with ui.element('div').classes('fc-header-row'):
            headers = ['Ngày', '', 'Nhiệt độ', 'Mưa', 'Độ ẩm', 'Gió', 'Áp suất', 'UV', 'AQI', 'Trạng thái']
            for h in headers:
                ui.label(h).classes('uppercase text-xs font-bold tracking-widest')

        # ===== CÁC HÀNG DỮ LIỆU =====
        for idx, day in enumerate(daily_list[:7]):
            display_name = 'Hôm nay' if idx == 0 else day.get('day_name', f'Ngày {idx+1}')
            rain_prob = day.get('pop_max', 0)
            aqi_val = day.get('aqi', {}).get('val', 25)
            
            # Tính toán áp suất theo đơn vị đã chọn
            raw_pressure = day.get('pressure', 1013)
            display_pressure = round(raw_pressure * 0.750062, 1) if p_unit == 'mmHg' else raw_pressure
            
            with ui.element('div').classes('fc-day-row'):
                ui.label(display_name).classes('text-white font-semibold')
                ui.icon('cloud' if rain_prob > 30 else 'wb_sunny').classes('text-blue-400')
                ui.label(f"{format_temp(day.get('temp_max', 0))} / {format_temp(day.get('temp_min', 0))}").classes('text-white')
                ui.label(f"{rain_prob}%").classes('text-blue-300 font-bold')
                ui.label(f"{day.get('humidity_avg', 0)}%").classes('text-teal-300')
                ui.label(format_wind_from_ms(day.get('wind_avg', 0))).classes('text-gray-300 text-xs')
                
                # 7. Áp suất (Đã cập nhật)
                ui.label(f"{display_pressure} {p_unit}").style('color:#e2e8f0; font-weight:700; font-size:0.85rem')
                
                ui.label(f"UV {day.get('uvi')}" if day.get('uvi') is not None else "UV --").classes('fc-badge text-orange-400')
                ui.label(f"{aqi_val}").classes('fc-badge text-green-400')
                ui.label(day.get('description', '—').capitalize()).classes('text-white/80 truncate text-sm')