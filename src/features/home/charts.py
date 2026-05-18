import plotly.graph_objects as go

from src.common.charts_base import chart_layout


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
