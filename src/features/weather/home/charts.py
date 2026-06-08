import plotly.graph_objects as go

from src.features.weather.components.charts_base import chart_layout
from src.common.units import convert_temp, get_units


_HOUR_ORDER = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '23:59']


def _normalize_pop(val):
    if val is None:
        return 0
    return round(val * 100) if val <= 1.0 else int(val)


def create_hourly_chart(hourly_data):
    if not hourly_data:
        return None

    # Helper đổi giờ thành phút để tính toán khoảng cách
    def to_min(t_str):
        try:
            h, m = map(int, t_str.split(':'))
            return h * 60 + m
        except: return 0

    # Ánh xạ dữ liệu API (thường lệch giờ) về các mốc cố định: 0:00, 3:00... 23:59
    lookup = {}
    for slot in _HOUR_ORDER:
        slot_min = to_min(slot)
        best_h, min_diff = None, 1440
        for h in hourly_data:
            diff = abs(slot_min - to_min(h.get('time', '')))
            if diff < min_diff:
                min_diff = diff
                best_h = h
        if best_h:
            lookup[slot] = best_h

    ordered = [t for t in _HOUR_ORDER if t in lookup]

    times = ordered
    pop   = [_normalize_pop(lookup[t].get('pop', 0)) for t in times]
    sun   = [max(0, 100 - p) for p in pop]

    temp_unit   = get_units()['unit_temp']
    temp_suffix = '°F' if temp_unit == 'F' else '°C'
    temps = [convert_temp(lookup[t].get('temp', 0), temp_unit) for t in times]

    t_min = min(temps) - 2
    t_max = max(temps) + 2

    fig = go.Figure()

    # Cột nắng (cam)
    fig.add_trace(go.Bar(
        x=times, y=sun,
        name='Nắng (%)',
        yaxis='y',
        marker=dict(color='rgba(251,146,60,0.8)', line=dict(color='rgba(251,146,60,1)', width=1)),
        hovertemplate='%{x}<br>Nắng: %{y}%<extra></extra>',
    ))

    # Cột mưa (xanh)
    fig.add_trace(go.Bar(
        x=times, y=pop,
        name='Xác suất mưa (%)',
        yaxis='y',
        marker=dict(color='rgba(79,172,254,0.8)', line=dict(color='rgba(79,172,254,1)', width=1)),
        hovertemplate='%{x}<br>Mưa: %{y}%<extra></extra>',
    ))

    # Đường nhiệt độ (trục phải)
    fig.add_trace(go.Scatter(
        x=times, y=temps,
        mode='lines+markers',
        name=f'Nhiệt độ ({temp_suffix})',
        yaxis='y2',
        line=dict(color='#f87171', width=2.5),
        marker=dict(size=6, color='#f87171', line=dict(color='#fff', width=1)),
        hovertemplate=f'%{{x}}<br>%{{y}}{temp_suffix}<extra>Nhiệt độ</extra>',
    ))

    base = chart_layout(
        height=300, showlegend=True,
        xaxis=dict(
            showgrid=False,
            type='category',
            categoryorder='array',
            categoryarray=_HOUR_ORDER,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)',
            range=[0, 100],
            ticksuffix='%',
            title=dict(text='Nắng / Mưa (%)', font=dict(size=11)),
        ),
    )
    base.update(
        barmode='stack',
        yaxis2=dict(
            overlaying='y',
            side='right',
            range=[t_min - 5, t_max + 5],
            showgrid=False,
            ticksuffix=temp_suffix,
            title=dict(text=f'Nhiệt độ ({temp_suffix})', font=dict(size=11)),
        ),
        legend=dict(
            orientation='h', x=0, y=1.13,
            font=dict(size=11),
            bgcolor='rgba(0,0,0,0)',
        ),
    )

    fig.update_layout(base)
    return fig


def create_temp_trend_chart(daily_data):
    if not daily_data:
        return None
    temp_unit = get_units()['unit_temp']
    temp_suffix = '°F' if temp_unit == 'F' else '°C'
    dates = [d['date'] for d in daily_data]
    temp_max = [convert_temp(d['temp_max'], temp_unit) for d in daily_data]
    temp_min = [convert_temp(d['temp_min'], temp_unit) for d in daily_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=temp_max, mode='lines+markers', name='Nhiệt độ cao nhất',
        line=dict(color='#ff6b6b', width=2),
        marker=dict(size=6, color='#ff6b6b'),
        hovertemplate=f'%{{y}}{temp_suffix}<extra>Cao nhất</extra>',
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=temp_min, mode='lines+markers', name='Nhiệt độ thấp nhất',
        line=dict(color='#4facfe', width=2),
        marker=dict(size=6, color='#4facfe'),
        fill='tonexty', fillcolor='rgba(79, 172, 254, 0.1)',
        hovertemplate=f'%{{y}}{temp_suffix}<extra>Thấp nhất</extra>',
    ))
    
    fig.update_layout(chart_layout(
        height=250, showlegend=True,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    ))
    return fig