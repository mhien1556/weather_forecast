from nicegui import ui
from datetime import datetime, timedelta
import plotly.graph_objects as go
import random
import math

from src.common.units import format_temp, format_wind_from_ms, get_units, convert_temp, convert_pressure

_TAG = 'div'

def dynamic_range(values, padding_ratio=0.15, min_padding=2):
    if not values:
        return 0, 100, 10
    mn, mx = min(values), max(values)
    spread = mx - mn
    if spread < 0.5:
        lo, hi = mn - min_padding, mx + min_padding
    else:
        pad = max(spread * padding_ratio, min_padding)
        lo, hi = mn - pad, mx + pad
    span = hi - lo
    if span <= 2:    dt = 0.2
    elif span <= 5:  dt = 0.5
    elif span <= 10: dt = 1
    elif span <= 20: dt = 2
    elif span <= 50: dt = 5
    else:            dt = 10
    return lo, hi, dt

# Cố định mốc thời gian 24 điểm (điểm cuối là 23:59)
TIME_SLOTS = [f"{i:02d}:00" for i in range(23)] + ['23:59']
# Nhãn hiển thị trên trục X cho gọn (mỗi 3 tiếng)
TICK_VALS = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '23:59']

def render_analysis_page(weather: dict):
    daily = weather.get('daily', [])
    hourly = weather.get('hourly', [])
    city_name = weather.get('city_name', 'Hà Nội')

    units = get_units()
    temp_unit = units.get('unit_temp', 'C')
    temp_suffix = '°F' if temp_unit == 'F' else '°C'
    wind_unit = units.get('unit_wind', 'km/h')
    pressure_unit = units.get('unit_pressure', 'hPa')
    pressure_suffix = 'hPa' if pressure_unit == 'hPa' else 'mmHg'
    theme = units.get('theme', 'dark')

    if not daily:
        ui.label('Không tìm thấy dữ liệu phân tích.').classes('opacity-50 p-5')
        return

    while len(daily) < 7:
        last = daily[-1]
        new_day = last.copy()
        try:
            last_date = datetime.strptime(last.get('date', '2026-06-06'), '%Y-%m-%d')
            next_date = last_date + timedelta(days=1)
            new_day['date'] = next_date.strftime('%Y-%m-%d')
            weekdays = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
            new_day['day_name'] = weekdays[next_date.weekday()]
        except:
            pass
        daily.append(new_day)

    selected_index = {'value': 0}

    def get_day_name(day, idx):
        if idx == 0: return 'Hôm nay'
        dn = day.get('day_name', '')
        if not dn:
            try:
                d = datetime.strptime(day.get('date', ''), '%Y-%m-%d')
                return ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'][d.weekday()]
            except Exception:
                return f'Ngày {idx+1}'
        if 'chủ nhật' in dn.lower(): return 'CN'
        if 'thứ 7' in dn.lower(): return 'T7'
        return dn.replace('Thứ ', 'T')

    def get_date_display(day, idx):
        parts = day.get('date', '').split('-')
        if len(parts) == 3: return f"{parts[2]}/{parts[1]}"
        return ''

    CHART_H = 200

    def make_fig(times, values, color, y_label='', is_bar=False):
        if not values or len(values) == 0: return go.Figure()
        
        if y_label == '%':
            lo, hi, dt = 0, 100, 25
            t_fmt = '.0f'
            suf = '%'
        else:
            lo, hi, dt = dynamic_range(values)
            t_fmt = '.1f'
            if y_label == 'UV':
                lo = max(0, lo)
                suf = ''
            elif y_label in ['km/h', 'mph', 'm/s']:
                lo = max(0, lo)
                suf = f' {y_label}'
            elif y_label in ['°C', '°F']:
                suf = y_label
            else:
                suf = f' {y_label}'
                t_fmt = '.0f' 

        if is_bar and lo > 0:
            lo = 0

        fig = go.Figure()
        
        if is_bar:
            fig.add_trace(go.Bar(
                x=times, y=values,
                marker_color=color, opacity=0.85,
                marker_line_width=0,
                hovertemplate='%{x}: <b>%{y}</b> ' + y_label + '<extra></extra>'
            ))
        else:
            try:
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                fill_color = f'rgba({r},{g},{b},0.08)'
            except:
                fill_color = 'rgba(79,172,254,0.08)'
                
            fig.add_trace(go.Scatter(
                x=times, y=values, mode='lines+markers',
                line=dict(color=color, width=2.5, shape='spline'),
                marker=dict(color=color, size=4, symbol='circle'),
                fill='tozeroy', fillcolor=fill_color,
                hovertemplate='%{x}: <b>%{y}</b> ' + y_label + '<extra></extra>'
            ))
        
        fig.update_layout(
            height=CHART_H, margin=dict(l=65, r=20, t=15, b=35),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8' if theme == 'dark' else '#475569', size=9),
            showlegend=False,
            xaxis=dict(
                type='category', # Ép kiểu category để các cột dàn đều chính xác
                gridcolor='rgba(255,255,255,0.03)' if theme == 'dark' else 'rgba(0,0,0,0.03)',
                showgrid=False, tickfont=dict(size=9), tickmode='array',
                tickvals=TICK_VALS, ticktext=TICK_VALS, tickangle=0,
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.06)' if theme == 'dark' else 'rgba(0,0,0,0.06)',
                tickfont=dict(size=9), range=[lo, hi], dtick=dt, 
                tickformat=t_fmt, ticksuffix=suf, title=None,
            ),
            bargap=0.3 if is_bar else None
        )
        return fig

    def generate_24h_data(day, is_today=False):
        bmax = convert_temp(day.get('temp_max', 30), temp_unit)
        bmin = convert_temp(day.get('temp_min', 25), temp_unit)
        base_rain = day.get('pop_max', 0)
        base_uv = day.get('uvi', 5)
        base_wind = day.get('wind_avg', 3)
        base_press = convert_pressure(day.get('pressure', 1013), pressure_unit)
        base_hum = day.get('humidity_avg', 75)
        
        temps, rains, hums, press, uvs, winds = [], [], [], [], [], []
        
        for i in range(24):
            t_ratio = math.sin(math.pi * (i - 4) / 14) if 4 <= i <= 18 else (math.sin(math.pi * (i + 10) / 14) * 0.5 + 0.5)
            temps.append(round(bmin + (bmax-bmin) * max(0, min(1, t_ratio)) + random.uniform(-0.4, 0.4), 1))
            
            rains.append(min(100, max(0, round(base_rain * (0.4 + 0.6 * math.sin(i)) + random.uniform(-3, 3), 1))))
            hums.append(min(100, max(20, round(base_hum + 15 * math.cos(math.pi * (i-4)/12) + random.uniform(-2, 2)))))
            press.append(round(base_press + 2 * math.sin(i/3) + random.uniform(-0.5, 0.5), 1))
            
            if 6 <= i <= 18:
                uvs.append(max(0, round(base_uv * math.sin(math.pi * (i-6)/12) + random.uniform(-0.3, 0.3), 1)))
            else:
                uvs.append(0)
                
            w = max(0, base_wind + 1.5 * math.sin(i/4) + random.uniform(-0.5, 0.5))
            if wind_unit == 'km/h': w_v = round(w * 3.6, 1)
            elif wind_unit == 'mph': w_v = round(w * 2.23694, 1)
            else: w_v = round(w, 1)
            winds.append(w_v)
            
        if is_today and hourly:
            first_hour = None
            for h in hourly:
                t_str = h.get('time', '')
                if not t_str: continue
                
                try: hour_int = int(t_str.split(':')[0])
                except: continue
                    
                if first_hour is None: first_hour = hour_int
                if hour_int < first_hour: break
                
                if 0 <= hour_int < 24:
                    idx = hour_int
                    temps[idx] = round(convert_temp(h.get('temp', temps[idx]), temp_unit), 1)
                    rains[idx] = h.get('pop', rains[idx])
                    
                    w = h.get('wind_speed', base_wind)
                    if wind_unit == 'km/h': winds[idx] = round(w * 3.6, 1)
                    elif wind_unit == 'mph': winds[idx] = round(w * 2.23694, 1)
                    else: winds[idx] = round(w, 1)
                    
                    uvs[idx] = max(0, min(12, h.get('uvi', uvs[idx])))
                    hums[idx] = h.get('humidity', hums[idx])
                    if h.get('pressure'):
                        press[idx] = round(convert_pressure(h.get('pressure'), pressure_unit), 1)

        return TIME_SLOTS, temps, rains, hums, press, uvs, winds

    def create_charts(day_idx):
        day = daily[day_idx] if daily else {}
        t, temps, rains, hums, press, uvs, winds = generate_24h_data(day, is_today=(day_idx == 0))

        return {
            'temp': make_fig(t, temps, '#f97316', temp_suffix, is_bar=False),
            'rain': make_fig(t, rains, '#3b82f6', '%', is_bar=True),
            'hum': make_fig(t, hums, '#0ea5e9', '%', is_bar=False),
            'press': make_fig(t, press, '#a855f7', pressure_suffix, is_bar=False),
            'uv': make_fig(t, uvs, '#eab308', 'UV', is_bar=True),
            'wind': make_fig(t, winds, '#10b981', wind_unit, is_bar=False),
        }

    def render_day_info(day_idx):
        if day_idx >= len(daily): return
        day = daily[day_idx]
        tmax = convert_temp(day.get('temp_max', 0), temp_unit)
        tmin = convert_temp(day.get('temp_min', 0), temp_unit)
        rain = day.get('pop_max', 0)
        hum = day.get('humidity_avg', 0)
        wind_raw = day.get('wind_avg', 0)
        
        if wind_unit == 'km/h': wind_speed, wind_suffix = wind_raw * 3.6, 'km/h'
        elif wind_unit == 'mph': wind_speed, wind_suffix = wind_raw * 2.23694, 'mph'
        else: wind_speed, wind_suffix = wind_raw, 'm/s'
            
        pressure = convert_pressure(day.get('pressure', 1013), pressure_unit)
        uv = day.get('uvi', 5)
        aqi_val = day.get('aqi', {}).get('val', 25) if isinstance(day.get('aqi'), dict) else 25
        desc = day.get('description', 'Có mây')

        uv_c = '#eab308' if uv >= 6 else '#facc15' if uv >= 3 else '#4ade80'
        aqi_c = '#4ade80' if aqi_val <= 50 else '#facc15' if aqi_val <= 100 else '#f97316'

        with ui.element('div').style(
            'width:100%; background:var(--card-bg); border-radius:16px; '
            'padding:14px 20px; margin-bottom:14px; box-sizing:border-box; '
            'border:1px solid var(--card-border); box-shadow:0 2px 10px rgba(0,0,0,0.3);'
        ):
            with ui.row().classes('items-center gap-2').style('margin-bottom:10px'):
                ui.label('📌').style('font-size:15px')
                ui.label(get_day_name(day, day_idx)).style('font-weight:800; color:#fff; font-size:16px')
                if day_idx == 0:
                    ui.label('HÔM NAY').style('background:#4facfe; border-radius:20px; padding:3px 12px; font-size:11px; color:#fff; font-weight:600')

            stats = [
                ('thermostat', f'{tmax:.1f}{temp_suffix} / {tmin:.1f}{temp_suffix}', '#fca5a5'),
                ('umbrella', f'{rain}%', '#3b82f6'),
                ('water_drop', f'{hum}%', '#0ea5e9'),
                ('air', f'{wind_speed:.1f} {wind_suffix}', '#10b981'),
                ('compress', f'{pressure:.0f} {pressure_suffix}', '#a855f7'),
                ('wb_sunny', f'UV {uv}', uv_c),
                ('monitoring', f'AQI {aqi_val}', aqi_c),
                ('cloud', desc.capitalize(), '#cbd5e1'),
            ]
            
            with ui.element('div').style(
                'display:grid; grid-template-columns:repeat(auto-fit, minmax(110px, 1fr)); gap:10px; width:100%;'
            ):
                for icon, label, color in stats:
                    with ui.element('div').style(
                        'display:flex; align-items:center; gap:6px; '
                        'background:rgba(255,255,255,0.05); border-radius:10px; padding:8px 10px; overflow:hidden;'
                    ):
                        ui.icon(icon).style(f'font-size:16px; color:{color}; flex-shrink:0')
                        ui.label(label).style(
                            f'font-size:12px; font-weight:600; color:{color}; '
                            'white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'
                        )

    CHART_CARD = 'width:100%; background:var(--card-bg); border-radius:16px; padding:12px 14px; border:1px solid var(--card-border); box-sizing:border-box;'

    def chart_card(icon, label, color):
        with ui.element('div').style(CHART_CARD):
            with ui.row().classes('items-center gap-2').style('margin-bottom:6px'):
                ui.icon(icon).style(f'font-size:15px; color:{color}')
                ui.label(label).style(f'font-weight:700; color:{color}; font-size:11px; letter-spacing: 0.5px;')
            plotly_instance = ui.plotly(go.Figure()).style(f'width:100%; height:{CHART_H}px')
            return plotly_instance

    def update_charts_optimized(idx, plotly_store):
        figs = create_charts(idx)
        for key, plot_element in plotly_store.items():
            if key in figs:
                plot_element.update_figure(figs[key])

    day_buttons = []
    _c = {}
    _plotly_elements = {}

    S_ACTIVE = 'background:#4facfe; color:#fff; box-shadow:0 4px 12px rgba(79,172,254,0.4); border-radius:40px; padding:8px 10px; text-align:center; cursor:pointer; transition:all 0.2s; flex:1; min-width:0;'
    S_INACTIVE = 'background:rgba(79,172,254,0.15); color:#fff; border-radius:40px; padding:8px 10px; text-align:center; cursor:pointer; transition:all 0.2s; flex:1; min-width:0;'

    def on_select(idx):
        prev = selected_index['value']
        if prev == idx: return
        
        if prev < len(day_buttons):
            day_buttons[prev].run_method('setAttribute', 'style', S_INACTIVE)
        if idx < len(day_buttons):
            day_buttons[idx].run_method('setAttribute', 'style', S_ACTIVE)
            
        selected_index['value'] = idx
        
        _c['info'].clear()
        with _c['info']: 
            render_day_info(idx)
            
        update_charts_optimized(idx, _plotly_elements)

    with ui.element('div').style('width:100%; padding:0 0 2rem 0; box-sizing:border-box'):
        with ui.element('div').style('width:100%; background:var(--card-bg); border-radius:16px; padding:14px 20px; margin-bottom:1rem; box-sizing:border-box; border:1px solid var(--card-border); box-shadow:0 2px 10px rgba(0,0,0,0.3); text-align:center;'):
            ui.label('🔬 Phân tích thời tiết chuyên sâu').style('font-size:1.4rem; font-weight:700; color:#fff; display:block')
            ui.label(f'{city_name}, Việt Nam').style('font-size:0.8rem; opacity:0.6; margin-top:2px; display:block')

        with ui.element('div').style('display:flex; gap:6px; width:100%; box-sizing:border-box; background:rgba(0,0,0,0.45); padding:10px 12px; border-radius:50px; border:1px solid rgba(79,172,254,0.2); margin-bottom:14px; flex-wrap:wrap; justify-content:center;'):
            for idx in range(7):
                if idx >= len(daily): break
                day = daily[idx]
                btn = ui.element('div').style(S_ACTIVE if idx == 0 else S_INACTIVE)
                btn.on('click', lambda i=idx: on_select(i))
                day_buttons.append(btn)
                with btn:
                    ui.label(get_day_name(day, idx)).style('font-weight:700; font-size:12px; display:block')
                    if d:=get_date_display(day, idx): ui.label(d).style('font-size:9px; opacity:0.65; display:block; margin-top:1px')
                    ui.label(f"{convert_temp(day.get('temp_max', 0), temp_unit):.0f}{temp_suffix}").style('font-size:13px; font-weight:800; display:block; margin-top:2px')

        _c['info'] = ui.element('div').style('width:100%')
        _c['charts'] = ui.element('div').style('width:100%')

        with _c['charts']:
            # Dòng 1: Nhiệt độ - Độ ẩm
            with ui.element('div').style('display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px;'):
                _plotly_elements['temp'] = chart_card('thermostat', 'XU HƯỚNG NHIỆT ĐỘ', '#f97316')
                _plotly_elements['hum'] = chart_card('water_drop', 'BIẾN ĐỔI ĐỘ ẨM', '#0ea5e9')
            # Dòng 2: Mưa - UV (Cùng hàng biểu đồ cột)
            with ui.element('div').style('display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px;'):
                _plotly_elements['rain'] = chart_card('umbrella', 'XÁC SUẤT MƯA THEO GIỜ', '#3b82f6')
                _plotly_elements['uv'] = chart_card('wb_sunny', 'DIỄN BIẾN CHỈ SỐ UV', '#eab308')
            # Dòng 3: Áp suất - Gió
            with ui.element('div').style('display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px;'):
                _plotly_elements['press'] = chart_card('compress', 'ÁP SUẤT KHÍ QUYỂN', '#a855f7')
                _plotly_elements['wind'] = chart_card('air', f'TỐC ĐỘ GIÓ ({wind_unit.upper()})', '#10b981')

    with _c['info']: 
        render_day_info(0)
    update_charts_optimized(0, _plotly_elements)
    