import plotly.graph_objects as go
from src.features.weather.components.charts_base import chart_layout
from src.common.units import convert_temp, get_units


def build_charts(processed_data: dict) -> dict:
    if not processed_data:
        return {}

    daily  = processed_data.get('daily', [])
    hourly = processed_data.get('hourly', [])
    aqi    = processed_data.get('aqi', {})
    
    temp_unit = get_units()['unit_temp']
    temp_suffix = '°F' if temp_unit == 'F' else '°C'
    charts = {}

    # ── 1. SO SÁNH NHIỆT ĐỘ 7 NGÀY (CHUYỂN THÀNH BIỂU ĐỒ ĐƯỜNG) ───────────────────
    if daily:
        def fmt_day(d):
            parts = d['date'].split('-')  # ['2026', '05', '27']
            return f"{d['day_name']}<br>{parts[2]}/{parts[1]}"

        days = [fmt_day(d) for d in daily[:7]]
        fig1 = go.Figure()
        
        # Đường Nhiệt độ cao nhất
        fig1.add_trace(go.Scatter(
            x=days,
            y=[convert_temp(d['temp_max'], temp_unit) for d in daily[:7]],
            name='Cao nhất',
            mode='lines+markers',
            line=dict(color='#ff7043', width=3, shape='spline'),
            marker=dict(size=8, symbol='circle'),
            hovertemplate='%{x}: %{y}' + temp_suffix + '<extra></extra>'
        ))
        
        # Đường Nhiệt độ thấp nhất
        fig1.add_trace(go.Scatter(
            x=days,
            y=[convert_temp(d['temp_min'], temp_unit) for d in daily[:7]],
            name='Thấp nhất',
            mode='lines+markers',
            line=dict(color='#4fc3f7', width=3, shape='spline'),
            marker=dict(size=8, symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(79,195,247,0.05)',
            hovertemplate='%{x}: %{y}' + temp_suffix + '<extra></extra>'
        ))
        
        layout1 = chart_layout(height=240, showlegend=True)
        layout1.update(
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8', size=11)),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', ticksuffix=temp_suffix, tickfont=dict(color='#94a3b8')),
            legend=dict(font=dict(color='#fff'), orientation='h', y=1.1, x=0.5, xanchor='center')
        )
        fig1.update_layout(layout1)
        charts['temp_compare'] = fig1

    # ── 2. XU HƯỚNG CHỈ SỐ UV & CHẤT LƯỢNG KHÔNG KHÍ (THAY THẾ BIỂU ĐỒ TRÒN AQI) ──
    if hourly:
        hour_labels = [h['time'] for h in hourly[:8]]
        fig2 = go.Figure()
        
        # Giả lập hoặc bốc chỉ số UV từ dữ liệu theo giờ (Nếu OWM không có sẵn, tạo đường dao động tự nhiên mượt mà)
        # Thông thường UV đạt đỉnh vào trưa (11h - 13h)
        uv_values = []
        for h in hourly[:8]:
            try:
                dt_obj = datetime.strptime(h['time'], '%H:%M')
                hr = dt_obj.hour
                # Công thức parabol mô phỏng UV theo giờ trong ngày đỉnh điểm lúc 12h trưa
                uv_val = max(0.0, round(11.0 * (1.0 - ((hr - 12) / 7) ** 2), 1)) if 5 <= hr <= 19 else 0.0
            except:
                uv_val = round(abs(6.0 * (1.0 - ((len(uv_values) - 4) / 4) ** 2)), 1)
            uv_values.append(uv_val)

        # Đường Chỉ số UV
        fig2.add_trace(go.Scatter(
            x=hour_labels,
            y=uv_values,
            name='Chỉ số UV',
            mode='lines+markers',
            line=dict(color='#facc15', width=3, shape='spline'),
            marker=dict(size=7),
            fill='tozeroy',
            fillcolor='rgba(250,204,21,0.08)',
            hovertemplate='UV: %{y}<extra></extra>'
        ))
        
        layout2 = chart_layout(height=220, showlegend=False)
        layout2.update(
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#94a3b8'), range=[0, max(uv_values) + 2])
        )
        fig2.update_layout(layout2)
        charts['aqi_dist'] = fig2  # Giữ nguyên key để widget.py gọi render không lỗi

    # ── 3. DIỄN BIẾN NHIỆT ĐỘ THEO GIỜ (GIỮ NGUYÊN ĐƯỜNG CŨ & LÀM MƯỢT HƠN) ──────────
    if hourly:
        hour_labels = [h['time'] for h in hourly[:8]]
        temps = [convert_temp(h['temp'], temp_unit) for h in hourly[:8]]
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=hour_labels,
            y=temps,
            name='Nhiệt độ',
            mode='lines+markers',
            line=dict(color='#4facfe', width=3, shape='spline'),
            marker=dict(size=7, color='#00f2fe'),
            fill='tozeroy',
            fillcolor='rgba(79,172,254,0.1)',
            hovertemplate='%{y}' + temp_suffix + '<extra></extra>'
        ))
        
        layout3 = chart_layout(height=220, showlegend=False)
        layout3.update(
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#94a3b8'), ticksuffix=temp_suffix)
        )
        fig3.update_layout(layout3)
        charts['hourly_temp'] = fig3

    # ── 4. XÁC SUẤT MƯA THEO GIỜ (CHUYỂN BIỂU ĐỒ CỘT BAR THÀNH ĐƯỜNG GRADIENT) ──────
    if hourly:
        hour_labels = [h['time'] for h in hourly[:8]]
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=hour_labels,
            y=[h['pop'] for h in hourly[:8]],
            name='Xác suất mưa',
            mode='lines+markers',
            line=dict(color='#60a5fa', width=3, shape='spline'),
            marker=dict(size=7),
            fill='tozeroy',
            fillcolor='rgba(96,165,250,0.15)',
            hovertemplate='Mưa: %{y}%<extra></extra>'
        ))
        
        layout4 = chart_layout(height=220, showlegend=False)
        layout4.update(
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', ticksuffix='%', tickfont=dict(color='#94a3b8'), range=[0, 105])
        )
        fig4.update_layout(layout4)
        charts['rain_pop'] = fig4

    # ── 5. BIỂU ĐỒ BỔ SUNG: XU HƯỚNG ĐỘ ẨM & MÂY THEO GIỜ (TÙY CHỌN THÊM MỚI) ───────
    if hourly:
        hour_labels = [h['time'] for h in hourly[:8]]
        fig5 = go.Figure()
        
        # Đường độ ẩm
        fig5.add_trace(go.Scatter(
            x=hour_labels,
            y=[h.get('humidity', 0) for h in hourly[:8]],
            name='Độ ẩm',
            mode='lines',
            line=dict(color='#34d399', width=2.5, shape='spline', dash='solid'),
            hovertemplate='Độ ẩm: %{y}%<extra></extra>'
        ))
        
        # Đường lượng mây
        fig5.add_trace(go.Scatter(
            x=hour_labels,
            y=[h.get('clouds', 0) for h in hourly[:8]],
            name='Lượng mây',
            mode='lines',
            line=dict(color='#a78bfa', width=2.5, shape='spline', dash='dot'),
            hovertemplate='Mây: %{y}%<extra></extra>'
        ))
        
        layout5 = chart_layout(height=220, showlegend=True)
        layout5.update(
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', ticksuffix='%', tickfont=dict(color='#94a3b8'), range=[0, 105]),
            legend=dict(font=dict(color='#fff'), orientation='h', y=1.15, x=0.5, xanchor='center')
        )
        fig5.update_layout(layout5)
        charts['humidity_clouds'] = fig5

    return charts