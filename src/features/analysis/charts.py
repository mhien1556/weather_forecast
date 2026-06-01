import plotly.graph_objects as go

from src.common.charts_base import chart_layout
from src.common.units import get_units, convert_temp


def build_charts(processed_data: dict) -> dict:
    if not processed_data:
        return {}

    u_temp = get_units()['unit_temp']
    daily = processed_data.get('daily', [])
    hourly = processed_data.get('hourly', [])
    aqi = processed_data.get('aqi')
    charts = {}

    if daily:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=[d['date'][5:] for d in daily[:7]],
            y=[round(convert_temp(d['temp_min'], u_temp)) for d in daily[:7]],
            name='Thấp nhất', marker_color='rgba(255,255,255,0.2)',
        ))
        fig1.add_trace(go.Bar(
            x=[d['date'][5:] for d in daily[:7]],
            y=[round(convert_temp(d['temp_max'], u_temp)) for d in daily[:7]],
            name='Cao nhất', marker_color='#4facfe',
        ))
        fig1.update_layout(chart_layout(
            height=220, barmode='overlay',
            legend=dict(font=dict(color='#fff'), orientation='h', y=1.1),
        ))
        charts['monthly'] = fig1

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

    if hourly:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=[f'+{i * 3}h' for i in range(len(hourly[:8]))],
            y=[h['pop'] for h in hourly[:8]],
            mode='lines+markers', name='Xác suất mưa (%)',
            line=dict(color='#facc15', width=3),
            fill='tozeroy', fillcolor='rgba(250, 204, 21, 0.1)',
        ))
        fig3.update_layout(chart_layout(
            height=320,
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        ))
        charts['events'] = fig3

    return charts
