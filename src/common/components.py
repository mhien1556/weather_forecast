from nicegui import app, ui

from .theme import STYLES
from .utils import lucide_to_material, is_raining, get_weather_color
from .config import get_city, set_city, clear_city, get_current_user, logout_user

NAV_ITEMS = [('/', 'Trang chủ'), ('/forecast', 'Dự báo'), ('/map', 'Bản đồ'), ('/analysis', 'Phân tích')]


def apply_theme(weather=None):
    """Áp dụng CSS và chế độ tối/sáng.
    Tự động đồng bộ cài đặt từ DB vào Session Storage khi người dùng đăng nhập.
    """
    try:
        from src.common.units import get_units
        user = get_current_user()
        
        # Nếu đã đăng nhập và cần đồng bộ cài đặt (chưa sync hoặc vừa lưu mới)
        if user and not app.storage.user.get('_settings_synced'):
            from src.database.user_store import get_user_settings
            username = user['username']
            
            # Lấy cài đặt đơn vị, theme & language từ DB
            db_settings = get_user_settings(username)
            for key, val in db_settings.items():
                app.storage.user[key] = val
            
            app.storage.user['_settings_synced'] = True
            print(f"[SYSTEM] Đã đồng bộ cài đặt từ DB cho user: {username}")

        units = get_units()
        is_dark = units.get('theme', 'dark') == 'dark'
    except Exception:
        is_dark = True
    ui.dark_mode(is_dark)
    ui.add_css(STYLES)

    # 🌈 ĐỒNG BỘ MÀU SẮC THEO ICON THỜI TIẾT
    if weather and not weather.get('error'):
        icon = weather.get('icon')
        accent_color = get_weather_color(icon)
        ui.add_css(f':root {{ --accent-color: {accent_color} !important; }}')


def open_settings_dialog():
    from src.features.user_management.settings.widgets import render_settings_content
    with ui.dialog() as dialog, ui.card().classes('settings-dialog-card'):
        with ui.row().classes('items-center justify-between w-full mb-2'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('settings').style('color:var(--accent-color);font-size:24px')
                ui.label('Cài đặt').classes('text-h6').style('margin:0;font-weight:700;')
            ui.button(icon='close', on_click=dialog.close).classes('icon-btn-round').props('flat round dense')
        render_settings_content(compact=True, parent_dialog_card=dialog)
    dialog.open()


def hero_background(_=None):
    with ui.element('div').classes('hero-bg'):
        ui.element('div').classes('overlay')


def navbar(active_path: str):
    user = get_current_user()
    with ui.element('nav').classes('navbar'):
        with ui.row().classes('nav-left items-center no-wrap').style('gap:3rem'):
            ui.link('WeatherForecast', '/').classes('logo-gradient').on(
                'click', lambda: clear_city() or ui.navigate.to('/')
            )
            with ui.row().classes('nav-links items-center no-wrap').style('gap:1.8rem'):
                for path, label in NAV_ITEMS:
                    ui.label(label).classes(
                        'nav-link ' + ('active' if path == active_path else '')
                    ).on('click', lambda p=path: (clear_city(), ui.navigate.to(p)))

        with ui.element('div').classes('nav-search'):
            with ui.element('div').classes('city-search-bar'):
                city_input = ui.input(
                    placeholder='Tìm thành phố...'
                ).classes('flex-grow q-input-dark').props('dense borderless')
                
                city_input.value = get_city().split(',')[0] if get_city() else ''

                def nav_search():
                    if city_input.value:
                        set_city(city_input.value)
                        ui.navigate.to(active_path)

                city_input.on('keydown.enter', nav_search)
                ui.button(icon='search', on_click=nav_search).classes('icon-btn-round').props('flat round dense')

        with ui.row().classes('nav-right items-center no-wrap').style('gap:1.25rem'):
            ui.button(icon='settings', on_click=open_settings_dialog).classes('icon-btn-round').props('flat round')
            if user and user.get('username') != 'guest':
                _user_menu(user)
            else:
                ui.button(
                    'Đăng nhập', icon='login',
                    on_click=lambda: ui.navigate.to('/login')
                ).classes('q-btn-login').props('unelevated no-caps')

def _user_menu(user: dict):
    """Menu user — màu sắc hoàn toàn từ CSS variables, không hard-code."""
    with ui.element('div').classes('user-menu-wrapper'):
        avatar_data = user.get('avatar', '?')

        with ui.element('div').classes('profile-avatar').style(
            'cursor:pointer;position:relative;overflow:hidden;'
            'display:flex;align-items:center;justify-content:center;'
        ):
            if avatar_data.startswith('data:image') or avatar_data.startswith('http'):
                ui.image(avatar_data).style('width:100%;height:100%;object-fit:cover;')
            else:
                ui.label(avatar_data)

        with ui.menu().classes('user-dropdown-menu') as menu:
            with ui.element('div').classes('user-menu-header'):
                with ui.element('div').classes('user-menu-avatar').style(
                    'overflow:hidden;display:flex;align-items:center;justify-content:center;'
                ):
                    if avatar_data.startswith('data:image') or avatar_data.startswith('http'):
                        ui.image(avatar_data).style('width:100%;height:100%;object-fit:cover;')
                    else:
                        ui.label(avatar_data)
                with ui.column().style('gap:0.1rem'):
                    ui.label(user.get('name', '')).style(
                        'font-weight:700;font-size:0.95rem;color:var(--menu-text-name)'
                    )
                    ui.label(user.get('email', '')).style(
                        'font-size:0.78rem;color:var(--menu-text-email)'
                    )

            ui.separator().style('background:var(--menu-separator);margin:0.4rem 0')

            with ui.menu_item(on_click=lambda: ui.navigate.to('/profile')).classes('user-menu-item'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('person', size='18px').style('color:var(--accent-color)')
                    ui.label('Thông tin cá nhân')

            with ui.menu_item(on_click=lambda: ui.navigate.to('/profile?tab=history')).classes('user-menu-item'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('history', size='18px').style('color:var(--accent-color)')
                    ui.label('Lịch sử truy cập')

            with ui.menu_item(on_click=lambda: ui.navigate.to('/profile?tab=favorites')).classes('user-menu-item'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('star_border', size='18px').style('color:var(--accent-color)')
                    ui.label('Thành phố yêu thích')

            ui.separator().style('background:var(--menu-separator);margin:0.4rem 0')

            with ui.menu_item(
                on_click=lambda: (logout_user(), ui.navigate.to('/'))
            ).classes('user-menu-item user-menu-logout'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('logout', size='18px').style('color:var(--danger-text)')
                    ui.label('Đăng xuất')

        avatar_el = ui.element('div').style('position:absolute;inset:0;cursor:pointer;')
        avatar_el.on('click', menu.open)


def footer():
    """Footer — dùng CSS classes, màu từ CSS variables (.body--dark / .body--light)."""
    footer_links = [
        ('Sản phẩm', [
            ('/', 'Trang chủ'),
            ('/forecast', 'Dự báo chi tiết'),
            ('/map', 'Bản đồ vệ tinh'),
            ('/analysis', 'Phân tích'),
        ]),
        ('Hỗ trợ', [
            ('#', 'Trung tâm trợ giúp'),
            ('#', 'Dữ liệu API'),
            ('#', 'Báo cáo lỗi'),
        ]),
        ('Liên hệ', [
            ('#', 'support@weathernow.vn'),
            ('#', 'Văn phòng đại diện'),
        ]),
    ]

    with ui.element('footer').classes('app-footer'):
        with ui.element('div').classes('footer-container'):
            # Cột thương hiệu
            with ui.column().classes('footer-brand gap-4'):
                ui.label('WeatherForecast').classes('footer-logo')
                ui.label(
                    'Giải pháp theo dõi thời tiết thông minh, '
                    'cung cấp dữ liệu chính xác và trực quan.'
                ).style('color:var(--footer-text);line-height:1.8;max-width:350px;font-size:0.95rem;')

            # Các cột link
            for title, links in footer_links:
                with ui.element('div').classes('footer-column'):
                    ui.label(title).style(
                        'font-weight:700;text-transform:uppercase;letter-spacing:1px;'
                        'margin-bottom:1.2rem;color:var(--footer-heading);font-size:1rem;'
                    )
                    with ui.element('ul').classes('footer-list'):
                        for href, text in links:
                            with ui.element('li').style('margin-bottom:0.85rem'):
                                ui.link(text, href).style(
                                    'color:var(--footer-link);text-decoration:none;'
                                    'font-size:0.95rem;font-weight:500;'
                                )

        with ui.element('div').classes('footer-bottom'):
            ui.label('© 2026 WeatherForecast. Thiết kế bởi Nhóm 25.').classes('footer-copy')


def metric_card(icon_name: str, label: str, value: str):
    with ui.element('div').classes('metric-card'):
        ui.icon(icon_name)
        ui.label(label).classes('metric-label')
        ui.label(value).classes('metric-value')


def plotly_chart(fig, height_class=''):
    if fig is None:
        ui.label('Không có dữ liệu').style('opacity:0.5;padding:2rem')
        return
    ui.plotly(fig).classes(f'w-full {height_class}').style('background:transparent')