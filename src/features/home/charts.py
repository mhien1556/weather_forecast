import plotly.graph_objects as go

from src.common.charts_base import chart_layout
from src.common.units import get_units, convert_temp


def create_hourly_chart(hourly_data):
    if not hourly_data:
        return None
    u_temp = get_units()['unit_temp']
    times = [h['time'] for h in hourly_data]
    temps = [convert_temp(h['temp'], u_temp) for h in hourly_data]
    temp_sym = '°F' if u_temp == 'F' else '°C'
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times, y=temps, mode='lines+markers', name=f'Nhiệt độ ({temp_sym})',
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
