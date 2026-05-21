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
        days = [d['date'][5:] for d in daily[:7]]
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=days,
            y=[round(d['temp_min']) for d in daily[:7]],
            name='Thấp nhất',
            marker_color='rgba(96, 165, 250, 0.8)',  # xanh nhạt
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
        fig1.update_layout(chart_layout(
            height=250,
            barmode='group',          # đứng cạnh nhau, click 1 lần là ẩn/hiện
            bargap=0.2,
            bargroupgap=0.05,
            legend=dict(
                font=dict(color='#fff', size=12),
                orientation='h',
                y=1.12,
                x=0,
                bgcolor='rgba(0,0,0,0)',
            ),
        ))
        charts['monthly'] = fig1

    # ── 2. AQI pie chart ──────────────────────────────────────
    if aqi:
        val = aqi['val'] / 20
        labels = ['Tốt', 'Trung bình', 'Kém']
        values = [1, 0, 0] if val <= 2 else ([0, 1, 0] if val == 3 else [0, 0, 1])
        fig2 = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=0.6,
            marker=dict(colors=['#4ade80', '#facc15', '#f87171']),
            textinfo='none',
        )])
        fig2.update_layout(chart_layout(
            height=220, showlegend=True,
            legend=dict(font=dict(color='#fff'), orientation='h', y=-0.15),
        ))
        charts['aqi_dist'] = fig2

    # ── 3. Xác suất mưa theo giờ ─────────────────────────────
    if hourly:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=[f'+{i * 3}h' for i in range(len(hourly[:8]))],
            y=[h['pop'] for h in hourly[:8]],
            mode='lines+markers',
            name='Xác suất mưa (%)',
            line=dict(color='#facc15', width=3),
            fill='tozeroy',
            fillcolor='rgba(250, 204, 21, 0.1)',
            hovertemplate='%{y}%<extra></extra>',
        ))
        fig3.update_layout(chart_layout(
            height=280,
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.08)',
                range=[0, 100],
                ticksuffix='%',
            ),
        ))
        charts['events'] = fig3

    # ── 4. Xu hướng nhiệt độ (line chart) ────────────────────
    if daily:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=[d['date'][5:] for d in daily[:7]],
            y=[round((d['temp_max'] + d['temp_min']) / 2) for d in daily[:7]],
            mode='lines+markers',
            name='Nhiệt độ TB',
            line=dict(color='#f97316', width=3),
            fill='tozeroy',
            fillcolor='rgba(249,115,22,0.08)',
            hovertemplate='%{y}°C<extra>TB</extra>',
        ))
        fig4.update_layout(chart_layout(
            height=220,
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.08)',
                ticksuffix='°',
            ),
        ))
        charts['trend'] = fig4

    return charts
