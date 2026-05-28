from nicegui import ui

from .theme import STYLES
from .utils import lucide_to_material, is_raining
from .config import get_city, set_city, clear_city, get_current_user, logout_user

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
    ui.dark_mode(True)
    ui.add_css(STYLES)


def hero_background(weather):
    rain = weather and is_raining(weather.get('icon'))
    with ui.element('div').classes('hero-bg' + (' rain' if rain else '')):
        ui.element('div').classes('overlay')


def navbar(active_path: str):
    user = get_current_user()

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
            ui.button(icon='settings', on_click=lambda: ui.navigate.to('/settings')).classes('icon-btn-round').props('flat round')

            if user:
                _user_menu(user)
            else:
                ui.button('Đăng nhập', icon='login', on_click=lambda: ui.navigate.to('/login')) \
                    .classes('q-btn-login').props('unelevated no-caps')


def _user_menu(user: dict):
    with ui.element('div').classes('user-menu-wrapper'):
        avatar_label = user.get('avatar', '?')
        with ui.element('div').classes('profile-avatar').style('cursor:pointer;position:relative'):
            avatar_el = ui.label(avatar_label)

        with ui.menu().classes('user-dropdown-menu') as menu:
            with ui.element('div').classes('user-menu-header'):
                with ui.element('div').classes('user-menu-avatar'):
                    ui.label(avatar_label)
                with ui.column().style('gap:0.1rem'):
                    ui.label(user.get('name', '')).style('font-weight:700;font-size:0.95rem;color:#fff')
                    ui.label(user.get('email', '')).style('font-size:0.78rem;color:rgba(255,255,255,0.45)')

            ui.separator().style('background:rgba(255,255,255,0.08);margin:0.4rem 0')

            # Fix: navigate tới /profile thay vì notify
            ui.menu_item('👤  Thông tin cá nhân',
                on_click=lambda: ui.navigate.to('/profile')).classes('user-menu-item')
            ui.menu_item('📍  Lịch sử truy cập',
                on_click=lambda: ui.navigate.to('/profile?tab=history')).classes('user-menu-item')
            ui.menu_item('⭐  Thành phố yêu thích',
                on_click=lambda: ui.navigate.to('/profile?tab=favorites')).classes('user-menu-item')
            ui.menu_item('🔔  Thông báo',
                on_click=lambda: ui.navigate.to('/profile?tab=notifs')).classes('user-menu-item')

            ui.separator().style('background:rgba(255,255,255,0.08);margin:0.4rem 0')

            def do_logout():
                logout_user()
                ui.navigate.to('/')

            ui.menu_item('🚪  Đăng xuất', on_click=do_logout).classes('user-menu-item user-menu-logout')

        avatar_el.on('click', menu.open)


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
                ui.label('Giải pháp theo dõi thời tiết thông minh, cung cấp dữ liệu chính xác và trực quan.') \
                    .style('color:rgba(255,255,255,0.6);line-height:1.8;max-width:350px')

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
            ui.label('© 2026 WeatherNow. Thiết kế bởi Nhóm 25.').classes('footer-copy')


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
