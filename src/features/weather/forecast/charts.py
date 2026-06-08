import plotly.graph_objects as go

from src.features.weather.components.charts_base import chart_layout
from src.common.units import convert_temp, get_units


def create_detailed_chart(daily_data):
    if not daily_data:
        return None
    slice_data = daily_data[:7]
    temp_unit = get_units()['unit_temp']
    temp_suffix = '°F' if temp_unit == 'F' else '°C'
    labels = [d['day_name'] for d in slice_data]
    max_temps = [convert_temp(d['temp_max'], temp_unit) for d in slice_data]
    min_temps = [convert_temp(d['temp_min'], temp_unit) for d in slice_data]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=max_temps, mode='lines+markers', name='Cao nhất',
        line=dict(color='#4facfe', width=3),
        hovertemplate=f'%{{y}}{temp_suffix}<extra>Cao nhất</extra>',
    ))
    fig.add_trace(go.Scatter(
        x=labels, y=min_temps, mode='lines+markers', name='Thấp nhất',
        line=dict(color='#f87171', width=3),
        hovertemplate=f'%{{y}}{temp_suffix}<extra>Thấp nhất</extra>',
    ))
    fig.update_layout(chart_layout(
        height=400,
        margin=dict(l=40, r=20, t=40, b=40),
        legend=dict(
            font=dict(color='#fff'), orientation='h',
            yanchor='bottom', y=1.02, xanchor='right', x=1,
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    ))
    return fig