from nicegui import ui

from .theme import STYLES
from .utils import lucide_to_material, is_raining
from .config import get_city, set_city, clear_city

NAV_ITEMS = [
    ('/', 'Trang chủ'),
    ('/forecast', 'Dự báo'),
    ('/map', 'Bản đồ'),
    ('/analysis', 'Phân tích'),
]

QUICK_CITIES = [
    ('Hanoi', 'Hà Nội'),
    ('Ho Chi Minh City', 'TP.HCM'),
    ('Da Nang', 'Đà Nẵng'),
]


def apply_theme():
    from src.common.units import get_units
    theme = get_units().get('theme', 'dark')
    ui.dark_mode(theme == 'dark')
    ui.add_css(STYLES)


def hero_background(weather):
    rain = weather and is_raining(weather.get('icon'))
    with ui.element('div').classes('hero-bg' + (' rain' if rain else '')):
        ui.element('div').classes('overlay')


def navbar(active_path: str):
    with ui.dialog() as profile_dialog:
        with ui.card().classes('card').style('min-width:320px;background:rgba(20,22,28,0.95);color:#fff'):
            ui.label('Tài khoản').classes('text-h6')
            with ui.element('div').style(
                'width:80px;height:80px;border-radius:50%;background:#e91e63;'
                'display:flex;align-items:center;justify-content:center;margin:1rem auto;font-size:2rem;font-weight:700;'
            ):
                ui.label('MH')
            ui.label('Minh Hiển').classes('text-center w-full font-bold')
            ui.label('minhhien@weathernow.vn').classes('text-center w-full').style('opacity:0.5')
            ui.button('Đăng xuất', icon='logout', color='red', on_click=lambda: ui.navigate.to('/login')).props('flat').classes('w-full q-mt-md')

    with ui.dialog().props('position=right') as settings_dialog:
        with ui.card().classes('card').style(
            'width: 450px; max-width: 100vw; height: 100vh; max-height: 100vh; '
            'margin: 0; border-radius: 0; background: rgba(20,22,28,0.95); '
            'backdrop-filter: blur(12px); padding: 1.5rem; overflow-y: auto;'
        ):
            with ui.row().classes('items-center justify-between w-full mb-4').style('position: sticky; top: 0; z-index: 10; background: rgba(20,22,28,0.95); padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1)'):
                ui.label('Cài đặt').classes('text-h5').style('font-weight: 700; margin: 0')
                ui.button(icon='close', on_click=settings_dialog.close).props('flat round dense')
            
            from src.features.settings.widgets import render_settings_content
            render_settings_content()


    with ui.element('nav').classes('navbar'):
        with ui.row().classes('nav-left items-center no-wrap').style('gap:3rem'):
            ui.link('WeatherNow', '/').classes('logo').on('click', lambda: clear_city() or ui.navigate.to('/'))
            with ui.row().classes('nav-links items-center no-wrap').style('gap:2rem'):
                def make_nav(p):
                    def nav_handler():
                        clear_city()
                        ui.navigate.to(p)
                    return nav_handler
                
                for path, label in NAV_ITEMS:
                    ui.label(label).classes('nav-link ' + ('active' if path == active_path else '')).on('click', make_nav(path))

        with ui.element('div').classes('nav-search'):
            with ui.element('div').classes('city-search-bar').style('max-width:100%;margin:0'):
                city_input = ui.input(placeholder='Tìm thành phố...').classes('flex-grow q-input-dark').props('dense borderless dark')
                city_input.value = get_city().split(',')[0] if get_city() else ''

                def nav_search():
                    if city_input.value:
                        set_city(city_input.value)
                        ui.navigate.to(active_path)

                ui.button(icon='search', on_click=nav_search).classes('icon-btn-round').props('flat round dense')

        with ui.row().classes('nav-right items-center no-wrap').style('gap:1.25rem'):
            ui.button(icon='settings', on_click=settings_dialog.open).classes('icon-btn-round').props('flat round')
            with ui.element('div').classes('profile-avatar').on('click', profile_dialog.open):
                ui.label('MH')


def city_search_section(target_path: str, weather):
    city_name = ''
    if weather and not weather.get('error'):
        city_name = weather.get('city_name', '').split(',')[0]

    with ui.element('div').classes('city-search-section'):
        with ui.row().classes('city-search-bar w-full').style('max-width:550px'):
            ui.icon('search').style('color:rgba(255,255,255,0.5)')
            city_input = ui.input(placeholder='Hà Nội', value=city_name).classes('flex-grow q-input-dark').props('borderless dense dark')

            def do_search():
                if city_input.value:
                    set_city(city_input.value)
                    ui.navigate.to(target_path)

            ui.button('Tìm', on_click=do_search).classes('q-btn-search').props('unelevated no-caps')

        with ui.row().classes('quick-cities'):
            ui.label('Gợi ý:').style('font-size:0.85rem;opacity:0.7')

            def go(c):
                set_city(c)
                ui.navigate.to(target_path)

            for city_id, label in QUICK_CITIES:
                ui.button(label, on_click=lambda c=city_id: go(c)).classes('quick-city-btn').props('flat no-caps')


def footer():
    with ui.element('footer').classes('app-footer'):
        with ui.element('div').classes('footer-container'):
            with ui.column().classes('footer-brand gap-4'):
                ui.label('WeatherNow').classes('footer-logo')
                ui.label(
                    'Giải pháp theo dõi thời tiết thông minh, cung cấp dữ liệu chính xác và trực quan.'
                ).style('color:rgba(255,255,255,0.6);line-height:1.8;max-width:350px')

            for title, links in [
                ('Sản phẩm', [('/', 'Trang chủ'), ('/forecast', 'Dự báo chi tiết'), ('/map', 'Bản đồ vệ tinh'), ('/analysis', 'Phân tích')]),
                ('Hỗ trợ', [('#', 'Trung tâm trợ giúp'), ('#', 'Dữ liệu API'), ('#', 'Báo cáo lỗi')]),
                ('Liên hệ', [('#', 'support@weathernow.vn'), ('#', 'Văn phòng đại diện')]),
            ]:
                with ui.element('div').classes('footer-column'):
                    ui.label(title).style('font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:1rem')
                    with ui.element('ul').classes('footer-list').style('list-style:none;padding:0;margin:0'):
                        for href, text in links:
                            with ui.element('li').style('margin-bottom:0.75rem'):
                                ui.link(text, href).style('color:rgba(255,255,255,0.6);text-decoration:none')

        with ui.element('div').classes('footer-bottom'):
            ui.label('© 2026 WeatherNow Inc. Thiết kế bởi Minh Hiển.').classes('footer-copy')


def metric_card(icon_name: str, label: str, value: str):
    with ui.element('div').classes('metric-card'):
        ui.icon(lucide_to_material(icon_name))
        ui.label(label).classes('metric-label')
        ui.label(value).classes('metric-value')


def plotly_chart(fig, height_class=''):
    if fig is None:
        ui.label('Không có dữ liệu').style('opacity:0.5;padding:2rem')
        return
    ui.plotly(fig).classes(f'w-full {height_class}').style('background:transparent')
