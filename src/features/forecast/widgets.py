from nicegui import ui

from src.common.components import plotly_chart
from src.common.utils import lucide_to_material

_TAG = 'div'


def generate_weather_insight(day_data: dict) -> str:
    """Hàm xử lý logic Python để đưa ra lời khuyên thông minh"""
    pop = day_data.get('pop_max', 0)
    t_max = day_data.get('temp_max', 30)
    
    if pop > 70:
        return f"⚠️ Cảnh báo: Khả năng đổ mưa rất cao ({pop}%). Bạn nên ưu tiên các hoạt động trong nhà, luôn mang theo ô hoặc áo mưa khi di chuyển ngoài đường."
    elif pop > 40:
        return f"🌧️ Thời tiết có xu hướng xuất hiện mưa dông rải rác một vài nơi trong ngày. Đề phòng các cơn mưa bất chợt vào giờ cao điểm."
    elif t_max >= 36:
        return f"☀️ Thời tiết nắng nóng gay gắt đỉnh điểm lên tới {round(t_max)}°C. Hạn chế tiếp xúc trực tiếp ánh nắng mặt trời vào buổi trưa để bảo vệ sức khỏe."
    else:
        return "✅ Điều kiện thời tiết lý tưởng cho các hoạt động ngoài trời, học tập và di chuyển. Bầu trời thoáng đãng, không khí dễ chịu."


def render_forecast_page(weather: dict):
    """Render trang dự báo chi tiết 7 ngày"""
    daily_list = weather.get('daily', [])
    charts = weather.get('charts', {})
    city_name = weather.get('city_name', 'Hà Nội')
    
    if not daily_list:
        ui.label('Không tìm thấy dữ liệu dự báo chi tiết.').classes('opacity-50 p-5')
        return

    # ✅ Trạng thái thẻ ngày đang được chọn (Mặc định hôm nay)
    selected_day_index = ui.state(0)

    with ui.column().classes('w-full gap-6 py-4').style('padding:1rem'):
        
        # ===== TIÊU ĐỀ TRANG =====
        with ui.column().classes('gap-1 mb-4'):
            ui.label('Dự báo thời tiết chi tiết').style('font-size:2rem;font-weight:700;color:#fff')
            ui.label(f'Thông tin khí tượng chuyên sâu 7 ngày tới tại {city_name}, Việt Nam').classes('opacity-75 text-sm')

        # ===== HỆ THỐNG THẺ CARD 7 NGÀY =====
        with ui.element('div').classes('grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3 w-full'):
            for idx, day in enumerate(daily_list[:7]):
                day_name = day.get('day_name', f'Ngày {idx+1}')
                display_name = 'Hôm nay' if idx == 0 else day_name
                
                is_selected = (selected_day_index.value == idx)
                card_style = (
                    'border: 2px solid #4facfe; background: rgba(79, 172, 254, 0.15);' 
                    if is_selected 
                    else 'border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05);'
                )

                with ui.card().classes('p-3 flex flex-col items-center gap-2 cursor-pointer transition-all duration-200 hover:scale-[1.03] rounded-xl text-center') \
                        .style(card_style) \
                        .on('click', lambda _, i=idx: selected_day_index.set_value(i)):
                    
                    ui.label(display_name).classes('text-xs font-semibold uppercase text-white/80')
                    ui.label(day.get('date', '')[5:].replace('-', '/')).classes('text-[0.7rem] opacity-50 -mt-2')
                    
                    ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud'))).style('font-size: 32px; color: #fff;')
                    
                    with ui.row().classes('gap-2 justify-center text-xs mt-1'):
                        ui.label(f"{round(day.get('temp_max', 0))}°").classes('font-bold text-white')
                        ui.label(f"{round(day.get('temp_min', 0))}°").classes('opacity-60')
                    
                    with ui.row().classes('items-center gap-0.5 opacity-70 text-[0.7rem]'):
                        ui.icon('umbrella').style('font-size: 11px; color: #3b82f6')
                        ui.label(f"{day.get('pop_max', 0)}%")

        # ===== PHẦN PHÂN TÍCH: TRỢ LÝ + BIỂU ĐỒ CHI TIẾT =====
        current_selected_data = daily_list[selected_day_index.value]
        
        with ui.element('div').style('display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1rem;width:100%;margin-top:2rem'):
            
            # KHỐI 1: TRỢ LÝ THỜI TIẾT
            with ui.element('div').classes('card').style('padding:1.25rem;display:flex;flex-direction:column;gap:1rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:0.75rem;justify-content:space-between'):
                with ui.column().classes('gap-1'):
                    with ui.row().classes('items-center gap-2').style('color:#4facfe;margin-bottom:0.5rem'):
                        ui.icon('psychology')
                        ui.label('Trợ lý thời tiết').style('font-weight:600;font-size:0.875rem')
                    
                    ui.label(f"Nhận xét ngày {current_selected_data.get('day_name')}:").style('font-size:0.75rem;font-weight:600;opacity:0.6;text-transform:uppercase')
                    ui.label(current_selected_data.get('desc', 'Bầu trời thay đổi')).style('font-size:1.25rem;font-weight:700;color:#fff')
                
                recommendation = generate_weather_insight(current_selected_data)
                with ui.element('div').style('padding:0.75rem;background:rgba(255,255,255,0.05);border-radius:0.5rem;border:1px solid rgba(255,255,255,0.05)'):
                    ui.label(recommendation).style('font-size:0.875rem;line-height:1.5;color:#93c5fd')

            # KHỐI 2: BIỂU ĐỒ CHI TIẾT (Max/Min)
            with ui.element('div').classes('card').style('padding:1.25rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:0.75rem'):
                with ui.row().classes('items-center gap-2').style('margin-bottom:0.5rem'):
                    ui.icon('thermostat')
                    ui.label('Chi tiết - Cao nhất & Thấp nhất').style('font-size:1rem;margin:0;font-weight:600')
                plotly_chart(charts.get('detailed'))

        # ===== PHẦN BIỂU ĐỒ: 2 CHART TOÀN TUẦN (Trend + Precip) =====
        with ui.element('div').style('display:grid;grid-template-columns:repeat(auto-fit,minmax(500px,1fr));gap:1rem;width:100%;margin-top:2rem'):
            
            # BIỂU ĐỒ: Xu hướng nhiệt độ
            with ui.element('div').classes('card').style('padding:1.25rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:0.75rem'):
                with ui.row().classes('items-center gap-2').style('margin-bottom:0.5rem'):
                    ui.icon('trending_up')
                    ui.label('Xu hướng - Biến thiên nhiệt độ 7 ngày').style('font-size:1rem;margin:0;font-weight:600')
                plotly_chart(charts.get('temp_trend'))
            
            # BIỂU ĐỒ: Lượng mưa
            with ui.element('div').classes('card').style('padding:1.25rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:0.75rem'):
                with ui.row().classes('items-center gap-2').style('margin-bottom:0.5rem'):
                    ui.icon('cloud_queue')
                    ui.label('Lượng mưa - Khả năng xuất hiện mưa 7 ngày').style('font-size:1rem;margin:0;font-weight:600')
                plotly_chart(charts.get('precip'))


def render_daily_cards(daily: list):
    """Render danh sách thẻ từng ngày (Backup - không dùng)"""
    with ui.element(_TAG).style('display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem;width:100%'):
        for i, day in enumerate(daily[:7]):
            with ui.element(_TAG).classes('card').style('padding:1rem;border-radius:0.75rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1)'):
                with ui.row().classes('w-full justify-between items-center').style('margin-bottom:0.75rem'):
                    ui.label('Hôm nay' if i == 0 else day['day_name']).style('font-weight:600;font-size:0.875rem')
                    ui.label(day['date']).style('opacity:0.6;font-size:0.75rem')
                
                with ui.column().classes('items-center gap-2'):
                    ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud'))).style('font-size:64px;color:#4facfe')
                    
                    with ui.row().classes('gap-2'):
                        ui.label(f'{round(day["temp_max"])}°').style('font-weight:700;font-size:2rem')
                        ui.label(f'{round(day["temp_min"])}°').style('font-size:2rem;opacity:0.6')
                    
                    ui.label(day['description'].capitalize()).style('opacity:0.8;font-size:0.875rem')
                
                with ui.row().classes('w-full justify-around').style('margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid rgba(255,255,255,0.1)'):
                    with ui.row().classes('items-center gap-1').style('font-size:0.75rem'):
                        ui.icon('opacity')
                        ui.label(f'{day["humidity_avg"]}%')
                    
                    with ui.row().classes('items-center gap-1').style('font-size:0.75rem'):
                        ui.icon('air')
                        ui.label(f'{day["wind_avg"]} m/s')