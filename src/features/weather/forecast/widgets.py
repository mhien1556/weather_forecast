from nicegui import ui
from datetime import datetime
from src.common.units import format_temp, format_wind_from_ms, get_units
from src.common.utils import get_weather_color

# Modern free-style CSS: cleaner, softer glass, subtle gradients, per-card accents
FC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

/* Global wrap */
.fc-wrap { 
  max-width: 1250px; margin: 24px auto; padding: 20px; 
  font-family: 'Outfit', sans-serif;
  color: var(--text-primary);
}

/* Title */
.fc-title-block {
  text-align: left;
  padding: 18px 8px 12px;
  display:flex;
  align-items: center;
  gap:12px;
}
.fc-city-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-secondary);
  display:flex;
  align-items:center;
  gap:8px;
}
.fc-heading {
  font-size: 1.6rem;
  font-weight: 800;
  line-height: 1;
  color: var(--text-primary);
}
.fc-heading span { 
  background: linear-gradient(90deg, var(--accent-color), #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Card base */
.fc-card {
  position: relative;
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 0;
  background: var(--card-bg-solid);
  border-radius: 20px;
  border: 1px solid var(--card-border);
  padding: 18px;
  margin-bottom: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.body--dark .fc-card { box-shadow: 0 6px 18px rgba(0,0,0,0.4); }
.fc-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.1);
  border-color: var(--accent-color);
}
.body--dark .fc-card:hover { box-shadow: 0 18px 40px rgba(0,0,0,0.7); }

/* Accent strip (left) */
.fc-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 6px; height: 100%;
  background: var(--accent-1);
  opacity: 0.95;
}

/* Left column */
.fc-left {
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:10px;
  padding: 10px 20px;
  border-right: 1px solid var(--card-border);
}
.fc-day-name {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.fc-weather-icon {
  font-size: 2.5rem !important;
  line-height: 1;
}

/* Right grid */
.fc-right {
  display: grid;
  grid-template-columns: 1.6fr 0.9fr 0.9fr 1fr 1.1fr 0.8fr 0.8fr 1.4fr;
  gap: 20px;
  align-items: center;
  padding: 10px 24px;
}

/* Cells */
.fc-cell { display:flex; flex-direction:column; gap:6px; }
.fc-cell-label {
  font-size: 0.62rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.fc-cell-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

/* Temperature emphasis */
.fc-temp-cell .fc-temp-max {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-primary);
}
.fc-temp-cell .fc-temp-min {
  font-size: 0.82rem;
  color: var(--text-secondary);
}

/* Colored values */
 .fc-val-rain  { color: #3b82f6; }
 .fc-val-humid { color: #10b981; }
 .fc-val-wind  { color: var(--text-secondary); font-size: 0.82rem !important; }
 .fc-val-press { color: var(--text-secondary); }
 .fc-val-uv    { color: #f59e0b; }
 .fc-val-desc  { color: var(--text-secondary); font-size: 0.9rem; line-height:1.4; }

/* AQI badge */
.fc-aqi-badge {
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 0.72rem;
}
.fc-aqi-good    { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.18); }
.fc-aqi-moderate{ background: rgba(251,191,36,0.10); color: #fbbf24; border: 1px solid rgba(251,191,36,0.18); }
.fc-aqi-bad     { background: rgba(248,113,113,0.10); color: #f87171; border: 1px solid rgba(248,113,113,0.18); }

/* Rain bar */
.fc-rain-bar-wrap { width:100%; height:6px; background: rgba(255,255,255,0.03); border-radius:6px; overflow:hidden; margin-top:4px; }
.fc-rain-bar { height:100%; background: linear-gradient(90deg,#60a5fa,#818cf8); transition: width .6s ease; }

/* Responsive tweaks */
@media (max-width: 880px) {
  .fc-right { grid-template-columns: 1fr 0.8fr 0.8fr 0.9fr 1fr 0.8fr 0.8fr 1fr; }
  .fc-card { grid-template-columns: 120px 1fr; }
}
"""

# icon mapping
_ICON_MAP = {
    'mưa': 'rainy', 'rain': 'rainy',
    'nắng': 'wb_sunny', 'sunny': 'wb_sunny', 'clear': 'wb_sunny',
    'mây': 'cloud', 'cloud': 'cloud', 'overcast': 'cloud',
    'bão': 'thunderstorm', 'thunder': 'thunderstorm',
    'tuyết': 'ac_unit', 'snow': 'ac_unit',
    'sương': 'foggy', 'fog': 'foggy', 'mist': 'foggy',
    'gió': 'air', 'wind': 'air',
}

def _pick_icon(day: dict) -> str:
    desc = (day.get('description') or '').lower()
    pop  = day.get('pop_max', 0) or 0
    if pop > 60:
        return 'rainy'
    for kw, icon in _ICON_MAP.items():
        if kw in desc:
            return icon
    lucide = day.get('lucide_icon', '')
    if 'rain' in lucide: return 'rainy'
    if 'sun'  in lucide: return 'wb_sunny'
    if 'snow' in lucide: return 'ac_unit'
    if 'thunder' in lucide: return 'thunderstorm'
    return 'partly_cloudy_day'

def _aqi_class(val: int) -> str:
    if val <= 50:   return 'fc-aqi-good'
    if val <= 100:  return 'fc-aqi-moderate'
    return 'fc-aqi-bad'

def _icon_color(icon: str) -> str:
    # Sử dụng hàm tập trung từ utils
    return get_weather_color(icon)


def render_forecast_page(weather: dict):
    """
    Thiết kế lại giao diện: phong cách free-style, hiện đại.
    Yêu cầu hiện tại: hiển thị vị trí (city_name) trở lại ở tiêu đề, đồng thời giữ layout mới.
    """
    ui.add_css(FC_CSS)

    daily_list = weather.get('daily', [])
    city_name  = weather.get('city_name', '')  # sử dụng lại vị trí

    if not daily_list:
        with ui.element('div').classes('fc-wrap'):
            ui.label('Không có dữ liệu dự báo.').classes('text-center text-white')
        return

    p_unit = get_units().get('unit_pressure', 'hPa')

    with ui.element('div').classes('fc-wrap'):
        # TITLE (hiển thị location nếu có)
        with ui.element('div').classes('fc-title-block'):
            if city_name:
                # hiển thị icon location và tên thành phố
                with ui.row().classes('items-center gap-2').style('gap:8px'):
                    ui.icon('location_on').style('color:rgba(255,255,255,0.6);font-size:1rem')
                    ui.label(city_name).classes('fc-city-label')
            with ui.element('div').classes('fc-heading'):
                ui.html('Dự báo <span>7 ngày</span>')

        # CARDS: render up to 7 days
        for idx, day in enumerate(daily_list[:7]):
            is_today   = (idx == 0)
            day_label  = 'Hôm nay' if is_today else day.get('day_name', f'Ngày {idx+1}')
            rain_prob  = day.get('pop_max', 0) or 0
            aqi_val    = (day.get('aqi') or {}).get('val', 25)
            raw_pres   = day.get('pressure', 1013) or 1013
            display_p  = round(raw_pres * 0.750062, 1) if p_unit == 'mmHg' else raw_pres
            uvi        = day.get('uvi')
            desc       = (day.get('description') or '—').capitalize()
            icon       = _pick_icon(day)
            # Lấy màu dựa trên mã icon gốc từ API
            icon_color = get_weather_color(day.get('icon'))

            # All cards use the same base class; accent strip handled by CSS nth-child
            card_cls   = 'fc-card'

            with ui.element('div').classes(card_cls).style(f'--accent-1: {icon_color}'):
                # LEFT: day label + icon
                with ui.element('div').classes('fc-left'):
                    ui.label(day_label).classes('fc-day-name')
                    ui.icon(icon).classes('fc-weather-icon').style(f'color:{icon_color}')

                # RIGHT: data grid
                with ui.element('div').classes('fc-right'):
                    # 1. Temperature
                    with ui.element('div').classes('fc-cell fc-temp-cell'):
                        ui.label('Nhiệt độ').classes('fc-cell-label')
                        ui.label(format_temp(day.get('temp_max', 0))).classes('fc-temp-max fc-cell-value')
                        ui.label(format_temp(day.get('temp_min', 0))).classes('fc-temp-min')

                    # 2. Rain probability + bar
                    with ui.element('div').classes('fc-cell'):
                        ui.label('Mưa').classes('fc-cell-label')
                        ui.label(f'{rain_prob}%').classes('fc-cell-value fc-val-rain')
                        with ui.element('div').classes('fc-rain-bar-wrap'):
                            ui.element('div').classes('fc-rain-bar').style(f'width:{min(max(rain_prob,0),100)}%')

                    # 3. Humidity
                    with ui.element('div').classes('fc-cell'):
                        ui.label('Ẩm').classes('fc-cell-label')
                        ui.label(f"{day.get('humidity_avg', 0)}%").classes('fc-cell-value fc-val-humid')

                    # 4. Wind
                    with ui.element('div').classes('fc-cell'):
                        ui.label('Gió').classes('fc-cell-label')
                        ui.label(format_wind_from_ms(day.get('wind_avg', 0))).classes('fc-cell-value fc-val-wind')

                    # 5. Pressure
                    with ui.element('div').classes('fc-cell'):
                        ui.label('Áp suất').classes('fc-cell-label')
                        ui.label(f'{display_p} {p_unit}').classes('fc-cell-value fc-val-press')

                    # 6. UV index
                    with ui.element('div').classes('fc-cell'):
                        ui.label('UV').classes('fc-cell-label')
                        ui.label(str(uvi) if uvi is not None else '—').classes('fc-cell-value fc-val-uv')

                    # 7. AQI
                    with ui.element('div').classes('fc-cell'):
                        ui.label('AQI').classes('fc-cell-label')
                        aqi_cls = _aqi_class(aqi_val)
                        ui.label(str(aqi_val)).classes(f'fc-aqi-badge {aqi_cls}')

                    # 8. Description / status
                    with ui.element('div').classes('fc-cell'):
                        ui.label('Tình trạng').classes('fc-cell-label')
                        ui.label(desc).classes('fc-cell-value fc-val-desc')
