"""Biểu đồ theo ngày — dùng chung cho Trang chủ & Dự báo."""

import plotly.graph_objects as go

from .charts_base import chart_layout
from src.common.units import convert_temp, get_units


def create_temp_trend_chart(daily_data):
    if not daily_data:
        return None
    labels = [d['day_name'][:3] for d in daily_data[:7]]
    temp_unit = get_units()['unit_temp']
    temp_suffix = '°F' if temp_unit == 'F' else '°C'
    temps = [
        convert_temp((d['temp_max'] + d['temp_min']) / 2, temp_unit)
        for d in daily_data[:7]
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=temps, mode='lines',
        line=dict(color='#4facfe', width=2, shape='spline'),
        hovertemplate=f'%{{y}}{temp_suffix}<extra></extra>',
    ))
    fig.update_layout(chart_layout(
        height=180, showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False),
    ))
    return fig


def create_precip_chart(daily_data):
    if not daily_data:
        return None
    labels = [d['date'][5:] for d in daily_data[:7]]
    pops = [d['pop_max'] for d in daily_data[:7]]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=pops, marker_color='rgba(79, 172, 254, 0.5)'))
    fig.update_layout(chart_layout(
        height=180, showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False),
    ))
    return fig
