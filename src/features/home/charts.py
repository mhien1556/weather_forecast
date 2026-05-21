import plotly.graph_objects as go
from datetime import datetime

from src.common.charts_base import chart_layout

def format_day_name_full(day_name_short):
    if not day_name_short:
        return ""
    
    # Ép kiểu chuỗi và xóa khoảng trắng thừa ở 2 đầu
    day_name_short = str(day_name_short).strip()
    print(f"DEBUG: Input day_name = '{day_name_short}'")  
    
    day_map = {
        'Thứ 2': 'Thứ 2', 'T2': 'Thứ 2',
        'Thứ 3': 'Thứ 3', 'T3': 'Thứ 3',
        'Thứ 4': 'Thứ 4', 'T4': 'Thứ 4',
        'Thứ 5': 'Thứ 5', 'T5': 'Thứ 5',
        'Thứ 6': 'Thứ 6', 'T6': 'Thứ 6',
        'Thứ 7': 'Thứ 7', 'T7': 'Thứ 7',
        'Chủ nhật': 'Chủ nhật', 'Chủ': 'Chủ nhật', 'CN': 'Chủ nhật'
    }
    
    # Nếu text truyền vào chỉ vỏn vẹn là "Thứ", có thể log data từ hệ thống đang bị lỗi cắt chuỗi
    if day_name_short == 'Thứ':
        return 'Thứ ?' # Để nhận biết lỗi từ đâu
        
    result = day_map.get(day_name_short, day_name_short)
    print(f"DEBUG: Output = '{result}'")  
    return result


def create_hourly_chart(hourly_data):
    if not hourly_data:
        return None
    times = [h['time'] for h in hourly_data]
    temps = [h['temp'] for h in hourly_data]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times, y=temps, mode='lines+markers', name='Nhiệt độ',
        line=dict(color='#4facfe', width=3),
        fill='tozeroy', fillcolor='rgba(79, 172, 254, 0.2)',
        marker=dict(size=8, color='#4facfe'),
    ))
    fig.update_layout(chart_layout(
        height=250, showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    ))
    return fig


def create_temp_trend_chart(daily_data):
    if not daily_data:
        return None
    
    # Giữ nguyên logic lấy ngày
    days = [format_day_name_full(d.get('day_name', f'Ngày {i+1}')) for i, d in enumerate(daily_data)]
    temps_max = [d['temp_max'] for d in daily_data]
    temps_min = [d['temp_min'] for d in daily_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=temps_max, mode='lines+markers', name='Cao nhất',
        line=dict(color='#ef4444', width=2),
        marker=dict(size=6, color='#ef4444'),
    ))
    fig.add_trace(go.Scatter(
        x=days, y=temps_min, mode='lines+markers', name='Thấp nhất',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=6, color='#3b82f6'),
    ))
    
    fig.update_layout(chart_layout(
        height=250, showlegend=True,
        # 🛠️ SỬA TẠI ĐÂY: Ép xaxis kiểu 'category' để hiện đầy đủ tất cả các thứ riêng biệt
        xaxis=dict(type='category', showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    ))
    return fig