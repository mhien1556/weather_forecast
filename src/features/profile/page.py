"""Trang /profile - thông tin cá nhân, lịch sử, yêu thích, thông báo."""
from nicegui import ui
from src.common.components import apply_theme, hero_background, navbar, footer
from src.common.config import get_current_user, set_current_user, logout_user
from src.common.user_store import (
    update_profile,
    get_history,
    clear_history,
    get_favorites,
    add_favorite,
    remove_favorite,
    get_notifications,
    update_notifications,
)

PROFILE_CSS = """
.profile-page {
    width: 100%;
    max-width: 950px;
    margin: 0 auto;
    padding: 2rem 1rem 4rem;
}

.profile-hero {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
    padding: 2rem;
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    backdrop-filter: blur(20px);
}

.profile-avatar-big {
    width: 80px;
    height: 80px;
    border-radius: 999px;
    background: linear-gradient(135deg, #e91e63, #9c27b0);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
}

.profile-tabs {
    width: 100%;
    display: flex;
    gap: .5rem;
    margin-bottom: 1.5rem;
}

.profile-card {
    width: 100%;
    background: rgba(15,23,42,0.55) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(20px);
    padding: 1.5rem !important;
}

.profile-input .q-field__control {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
}

.q-card {
    background: transparent !important;
    box-shadow: none !important;
}
"""

def register():

    @ui.page('/profile')
    def profile_page():

        apply_theme()
        ui.add_css(PROFILE_CSS)

        user = get_current_user()

        if not user:
            ui.navigate.to('/login')
            return

        username = user.get('username', '')
        tab = ui.context.client.request.query_params.get('tab', 'info')

        with ui.column().classes('app-container w-full'):
            hero_background(None)
            navbar('/profile')

            with ui.column().classes('profile-page w-full'):

                with ui.card().classes('profile-hero w-full'):

                    with ui.element('div').classes('profile-avatar-big'):
                        ui.label(
                            user.get('avatar')
                            or user.get('name', '?')[:1].upper()
                        )

                    with ui.column().style('gap:0.25rem;flex:1'):

                        ui.label(
                            user.get('name', 'Unknown')
                        ).style(
                            'font-size:1.7rem;font-weight:700;color:white'
                        )

                        ui.label(
                            user.get('email', '')
                        ).style(
                            'color:rgba(255,255,255,.6)'
                        )

                        ui.label(
                            f'@{username}'
                        ).style(
                            'color:rgba(255,255,255,.35)'
                        )

                    ui.button(
                        'Đăng xuất',
                        icon='logout',
                        on_click=lambda: [
                            logout_user(),
                            ui.navigate.to('/')
                        ]
                    ).props('outline')

                with ui.row().classes('profile-tabs'):

                    tabs = [
                        ('info', '👤 Cá nhân'),
                        ('history', '📍 Lịch sử'),
                        ('favorites', '⭐ Yêu thích'),
                        ('notifs', '🔔 Thông báo'),
                    ]

                    for tab_name, label in tabs:

                        color = 'primary' if tab == tab_name else 'grey'

                        ui.button(
                            label,
                            color=color,
                            on_click=lambda t=tab_name:
                            ui.navigate.to(f'/profile?tab={t}')
                        ).props('unelevated')

                if tab == 'info':
                    render_info(username, user)

                elif tab == 'history':
                    render_history(username)

                elif tab == 'favorites':
                    render_favorites(username)

                elif tab == 'notifs':
                    render_notifs(username)

            footer()

def render_info(username, user):

    with ui.card().classes('profile-card'):

        ui.label('Thông tin cá nhân').style(
            'font-size:1.2rem;font-weight:700;color:white'
        )

        name_input = ui.input(
            'Họ và tên',
            value=user.get('name', '')
        ).classes('profile-input w-full').props('outlined dark')

        email_input = ui.input(
            'Email',
            value=user.get('email', '')
        ).classes('profile-input w-full').props('outlined dark')

        status = ui.label()

        def save_profile():

            ok = update_profile(
                username,
                name_input.value,
                email_input.value
            )

            if ok:

                set_current_user({
                    **user,
                    'name': name_input.value,
                    'email': email_input.value,
                    'avatar': name_input.value[:1].upper()
                })

                status.set_text('✅ Đã lưu')
                status.style('color:#4ade80')

            else:

                status.set_text('❌ Lỗi cập nhật')
                status.style('color:#f87171')

        ui.button(
            'Lưu thay đổi',
            on_click=save_profile
        ).props('unelevated color=primary')


def render_history(username):

    history = get_history(username) or []

    with ui.card().classes('profile-card'):

        with ui.row().classes('w-full items-center justify-between'):

            ui.label('Lịch sử tìm kiếm').style(
                'font-size:1.1rem;font-weight:700;color:white'
            )

            ui.button(
                'Xóa tất cả',
                icon='delete',
                on_click=lambda: [
                    clear_history(username),
                    ui.navigate.reload()
                ]
            ).props('outline color=red')

        if not history:

            ui.label(
                'Chưa có lịch sử'
            ).style('color:rgba(255,255,255,.5)')

        else:

            for item in history:

                with ui.card().classes('w-full q-mt-sm'):

                    ui.label(str(item))


def render_favorites(username):

    favorites = get_favorites(username) or []

    with ui.card().classes('profile-card'):

        ui.label('Yêu thích').style(
            'font-size:1.1rem;font-weight:700;color:white'
        )

        city_input = ui.input(
            placeholder='Nhập tên thành phố...'
        ).classes('profile-input w-full').props('outlined dark')

        def add_city():

            if city_input.value:

                add_favorite(username, city_input.value)
                ui.navigate.reload()

        ui.button(
            '+ Thêm',
            on_click=add_city
        ).props('unelevated color=primary')

        for city in favorites:

            with ui.row().classes(
                'w-full items-center justify-between q-mt-sm'
            ):

                ui.label(city).style('color:white')

                ui.button(
                    icon='delete',
                    on_click=lambda c=city: [
                        remove_favorite(username, c),
                        ui.navigate.reload()
                    ]
                ).props('flat round color=red')


def render_notifs(username):

    settings = get_notifications(username) or {}

    with ui.card().classes('profile-card'):

        ui.label('Thông báo').style(
            'font-size:1.1rem;font-weight:700;color:white'
        )

        email_toggle = ui.switch(
            'Thông báo email',
            value=settings.get('email', True)
        )

        rain_toggle = ui.switch(
            'Cảnh báo mưa',
            value=settings.get('rain', True)
        )

        severe_toggle = ui.switch(
            'Cảnh báo thời tiết xấu',
            value=settings.get('severe', True)
        )

        def save_notifs():

            update_notifications(username, {
                'email': email_toggle.value,
                'rain': rain_toggle.value,
                'severe': severe_toggle.value,
            })

            ui.notify('Đã lưu cài đặt')

        ui.button(
            'Lưu cài đặt',
            on_click=save_notifs
        ).props('unelevated color=primary')
