import plotly.graph_objects as go
from src.common.charts_base import chart_layout


def build_charts(processed_data: dict) -> dict:
    if not processed_data:
        return {}

    daily  = processed_data.get('daily', [])
    hourly = processed_data.get('hourly', [])
    aqi    = processed_data.get('aqi')
    charts = {}

    # ── 1. So sánh nhiệt độ 7 ngày ───────────────────────────
    if daily:
        # Đổi format ngày: '2026-05-27' → 'T3\n27/05' để tránh Plotly tự parse
        def fmt_day(d):
            parts = d['date'].split('-')  # ['2026', '05', '27']
            return f"{d['day_name']}\n{parts[2]}/{parts[1]}"

        days = [fmt_day(d) for d in daily[:7]]
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=days,
            y=[round(d['temp_min']) for d in daily[:7]],
            name='Thấp nhất',
            marker_color='rgba(96,165,250,0.85)',
            marker_line=dict(width=0),
            hovertemplate='%{y}°C<extra>Thấp nhất</extra>',
        ))
        fig1.add_trace(go.Bar(
            x=days,
            y=[round(d['temp_max']) for d in daily[:7]],
            name='Cao nhất',
            marker_color='#4facfe',
            marker_line=dict(width=0),
            hovertemplate='%{y}°C<extra>Cao nhất</extra>',
        ))
        layout1 = chart_layout(height=280, barmode='group', bargap=0.25, bargroupgap=0.05)
        layout1['legend'] = dict(
            font=dict(color='#fff', size=12),
            orientation='h', y=1.1, x=0,
            bgcolor='rgba(0,0,0,0)',
        )
        layout1['xaxis'] = dict(
            tickfont=dict(color='rgba(255,255,255,0.7)', size=11),
        )
        layout1['yaxis'] = dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.07)',
            ticksuffix='°C',
            tickfont=dict(color='rgba(255,255,255,0.6)'),
        )
        fig1.update_layout(layout1)
        charts['monthly'] = fig1

    # ── 2. Dự báo nhiệt độ theo giờ ──────────────────────────
    if hourly:
        hour_labels = [h['time'] for h in hourly[:8]]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=hour_labels,
            y=[h['temp'] for h in hourly[:8]],
            mode='lines+markers',
            name='Nhiệt độ (°C)',
            line=dict(color='#f97316', width=3),
            marker=dict(size=8, color='#f97316'),
            fill='tozeroy',
            fillcolor='rgba(249,115,22,0.08)',
            hovertemplate='%{x}: %{y}°C<extra></extra>',
        ))
        layout2 = chart_layout(height=260)
        layout2['yaxis'] = dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.07)',
            ticksuffix='°C',
            tickfont=dict(color='rgba(255,255,255,0.6)'),
        )
        layout2['xaxis'] = dict(tickfont=dict(color='rgba(255,255,255,0.7)'))
        fig2.update_layout(layout2)
        charts['hourly_temp'] = fig2

    # ── 3. AQI pie chart ──────────────────────────────────────
    if aqi:
        val = aqi['val'] / 20
        labels = ['Tốt', 'Trung bình', 'Kém']
        values = [1, 0, 0] if val <= 2 else ([0, 1, 0] if val == 3 else [0, 0, 1])
        fig3 = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=0.6,
            marker=dict(colors=['#4ade80', '#facc15', '#f87171']),
            textinfo='none',
        )])
        layout3 = chart_layout(height=220, showlegend=True)
        layout3['legend'] = dict(font=dict(color='#fff'), orientation='h', y=-0.15)
        fig3.update_layout(layout3)
        charts['aqi_dist'] = fig3

    # ── 4. Xác suất mưa theo giờ ─────────────────────────────
    if hourly:
        hour_labels = [h['time'] for h in hourly[:8]]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=hour_labels,
            y=[h['pop'] for h in hourly[:8]],
            name='Xác suất mưa (%)',
            marker_color='rgba(79,172,254,0.7)',
            marker_line=dict(width=0),
            hovertemplate='%{x}: %{y}%<extra></extra>',
        ))
        layout4 = chart_layout(height=260)
        layout4['yaxis'] = dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.07)',
            range=[0, 100],
            ticksuffix='%',
            tickfont=dict(color='rgba(255,255,255,0.6)'),
        )
        layout4['xaxis'] = dict(tickfont=dict(color='rgba(255,255,255,0.7)'))
        fig4.update_layout(layout4)
        charts['events'] = fig4

    return charts
