from nicegui import ui
from src.common.components import (
    apply_theme, city_search_section, footer,
    hero_background, navbar, plotly_chart,
)
from src.common.config import API_KEY, get_city
from .service import get_data

_TAG = 'div'


def register():
    @ui.page('/analysis')
    def analysis_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}

        with ui.element(_TAG).classes('app-container'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/analysis')

            with ui.element(_TAG).classes('page-content content-wrapper'):
                if weather.get('error'):
                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
                else:
                    city_search_section('/analysis', weather)
                    _render_analysis(weather)

            footer()


def _render_analysis(weather: dict):
    charts = weather.get('charts', {})
    stats  = weather.get('stats', {})
    aqi    = weather.get('aqi')

    # ── Page header ───────────────────────────────────────────
    with ui.element(_TAG).classes('page-header'):
        ui.label('📊 Phân tích chuyên sâu').classes('text-h4').style('font-weight:700;margin:0')
        ui.label(f'Xu hướng & thống kê khí tượng tại {weather.get("city_name", "N/A")}') \
            .style('opacity:0.7;margin-top:0.3rem')

    # ── KPI row ───────────────────────────────────────────────
    with ui.element(_TAG).classes('analysis-kpi-row'):
        _kpi('🌡 Nhiệt độ TB', f'{stats.get("avg_temp", "--")}°C', '+1.2° so với tuần trước', 'up', '#4facfe')
        _kpi('🌧 Tổng lượng mưa', f'{stats.get("total_rain", "--")} mm', '-15% so với tuần trước', 'down', '#60a5fa')
        sunny_h = stats.get('sunny_days', 0) * 3 if stats else '--'
        _kpi('☀️ Số giờ nắng', f'{sunny_h}h', '+3h so với tuần trước', 'up', '#facc15')
        _kpi('💨 Gió hiện tại', f'{weather.get("wind", "--")} m/s', 'Ổn định', 'neutral', '#a78bfa')

    # ── Main charts row ───────────────────────────────────────
    with ui.element(_TAG).classes('analysis-row'):
        with ui.element(_TAG).classes('card'):
            ui.label('📈 So sánh nhiệt độ 7 ngày (°C)').style('font-weight:600;font-size:1rem;margin-bottom:1rem')
            plotly_chart(charts.get('monthly'))

        with ui.element(_TAG).classes('card'):
            ui.label('💨 Chất lượng không khí (AQI)').style('font-weight:600;font-size:1rem;margin-bottom:1rem')
            if aqi:
                _render_aqi_detail(aqi)
            else:
                plotly_chart(charts.get('aqi_dist'))

    # ── Events chart (full width) ─────────────────────────────
    with ui.element(_TAG).classes('card').style('margin-bottom:1.5rem'):
        ui.label('🌦 Xác suất mưa theo giờ (%)').style('font-weight:600;font-size:1rem;margin-bottom:1rem')
        plotly_chart(charts.get('events'))

    # ── Bottom: insights + stats ──────────────────────────────
    with ui.element(_TAG).classes('analysis-bottom'):
        with ui.element(_TAG).classes('card'):
            ui.label('💡 Nhận xét & Khuyến nghị').style('font-weight:600;font-size:1rem;margin-bottom:1rem')
            _render_insights(weather, stats, aqi)

        with ui.element(_TAG).classes('analysis-metrics'):
            _stat_card('Nhiệt độ trung bình', f'{stats.get("avg_temp", "--")}°C', '+1.2° so với tuần trước', True)
            _stat_card('Tổng lượng mưa', f'{stats.get("total_rain", "--")} mm', '-15% so với tuần trước', False)
            _stat_card('Số giờ nắng', f'{sunny_h}h', '+3h so với tuần trước', True)


def _kpi(label: str, value: str, change: str, trend: str, color: str):
    with ui.element('div').classes('card kpi-card'):
        ui.label(label).style('font-size:0.75rem;text-transform:uppercase;letter-spacing:0.8px;color:rgba(255,255,255,0.45);font-weight:600')
        ui.label(value).style(f'font-family:Outfit,sans-serif;font-size:2rem;font-weight:700;color:{color};line-height:1.1')
        badge_color = {'up': '#4ade80', 'down': '#f87171', 'neutral': '#facc15'}.get(trend, '#fff')
        bg = {'up': 'rgba(74,222,128,0.15)', 'down': 'rgba(248,113,113,0.15)', 'neutral': 'rgba(250,204,21,0.15)'}.get(trend, 'rgba(255,255,255,0.1)')
        arrow = {'up': '↑', 'down': '↓', 'neutral': '≈'}.get(trend, '')
        ui.label(f'{arrow} {change}').style(
            f'background:{bg};color:{badge_color};padding:0.2rem 0.6rem;border-radius:999px;font-size:0.75rem;font-weight:600;display:inline-block'
        )


def _render_aqi_detail(aqi: dict):
    with ui.element('div').style('display:flex;flex-direction:column;align-items:center;gap:1rem;padding:0.5rem 0'):
        # Gauge circle
        with ui.element('div').style(
            f'width:90px;height:90px;border-radius:50%;border:5px solid {aqi["color"]};'
            'display:flex;flex-direction:column;align-items:center;justify-content:center;'
        ):
            ui.label(str(aqi['val'])).style(f'font-size:1.6rem;font-weight:700;color:{aqi["color"]};line-height:1')
            ui.label('AQI').style('font-size:0.6rem;color:rgba(255,255,255,0.5)')

        # Badge + desc
        ui.label(aqi['label']).style(
            f'background:{aqi["color"]}22;color:{aqi["color"]};padding:0.25rem 1rem;border-radius:999px;font-weight:700'
        )
        ui.label(aqi['desc']).style('font-size:0.8rem;color:rgba(255,255,255,0.55);text-align:center')

        # Pollutant bars
        with ui.element('div').style('width:100%;display:flex;flex-direction:column;gap:0.6rem'):
            _pollutant_bar('PM2.5', aqi['pm25'], 'µg/m³', aqi['pm25_pct'], '#4facfe')
            _pollutant_bar('CO', aqi['co'], 'µg/m³', aqi['co_pct'], '#f87171')


def _pollutant_bar(name: str, val: float, unit: str, pct: float, color: str):
    with ui.element('div').style('display:flex;flex-direction:column;gap:0.25rem'):
        with ui.element('div').style('display:flex;justify-content:space-between;font-size:0.78rem'):
            ui.label(name).style('color:rgba(255,255,255,0.5)')
            ui.label(f'{val} {unit}').style('color:#fff;font-weight:600')
        with ui.element('div').style('height:4px;background:rgba(255,255,255,0.1);border-radius:2px'):
            ui.element('div').style(f'height:100%;width:{pct:.0f}%;background:{color};border-radius:2px')


def _render_insights(weather: dict, stats: dict, aqi):
    items = []
    avg = stats.get('avg_temp')
    if avg is not None:
        mood = 'Khá nóng ☀️' if avg > 30 else ('Mát mẻ 🌿' if avg < 22 else 'Dễ chịu 😊')
        items.append(f'🌡 Nhiệt độ TB {avg}°C — {mood}')

    rain = stats.get('total_rain')
    if rain is not None:
        items.append(f'🌧 Lượng mưa dự kiến {rain} mm trong 5 ngày tới')

    sunny = stats.get('sunny_days')
    if sunny is not None:
        items.append(f'☀️ Dự kiến {sunny} ngày nắng trong tuần')

    hum = weather.get('humidity')
    if hum is not None:
        comfort = 'Khô' if hum < 40 else ('Lý tưởng' if hum < 70 else 'Ẩm')
        items.append(f'💧 Độ ẩm {hum}% — {comfort}')

    uv = weather.get('uv_index')
    if uv is not None:
        uv_level = 'Nguy hiểm 🚨' if uv > 8 else ('Cao ⚠️' if uv > 5 else ('Trung bình' if uv > 2 else 'Thấp ✅'))
        items.append(f'🔆 Chỉ số UV: {uv} — {uv_level}')

    if aqi:
        items.append(f'💨 Chất lượng không khí: {aqi["label"]} — {aqi["desc"]}')

    for item in items:
        with ui.element('div').style(
            'display:flex;align-items:center;gap:0.75rem;padding:0.75rem 1rem;'
            'background:rgba(255,255,255,0.04);border-radius:12px;margin-bottom:0.5rem;'
            'border:1px solid rgba(255,255,255,0.06);font-size:0.88rem;color:rgba(255,255,255,0.85)'
        ):
            ui.label(item)


def _stat_card(label: str, value: str, change: str, up: bool):
    with ui.element('div').classes('card stat-card'):
        ui.label(label).classes('stat-label')
        ui.label(value).classes('stat-value')
        ui.label(change).classes('stat-change up' if up else 'stat-change down')
