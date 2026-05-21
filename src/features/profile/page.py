"""Trang /profile - thông tin cá nhân, lịch sử, yêu thích, thông báo."""
from nicegui import ui
from src.common.components import apply_theme, hero_background, navbar, footer
from src.common.config import get_current_user, set_current_user, logout_user
from src.common.user_store import (
    update_profile, change_password,
    get_history, clear_history,
    get_favorites, add_favorite, remove_favorite,
    get_notifications, update_notifications,
)

PROFILE_CSS = """
.profile-page { max-width: 900px; margin: 0 auto; padding: 2rem 1rem 4rem; }

.profile-hero {
    display: flex; align-items: center; gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding: 2rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    backdrop-filter: blur(20px);
}

.profile-avatar-big {
    width: 80px; height: 80px; border-radius: 50%;
    background: linear-gradient(135deg, #e91e63, #9c27b0);
    color: #fff; font-size: 2rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 8px 25px rgba(233,30,99,0.3);
}

.profile-tabs {
    display: flex; gap: 0.5rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 6px;
    margin-bottom: 1.5rem;
}

.profile-tab-btn {
    flex: 1 !important; border-radius: 10px !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    color: rgba(255,255,255,0.45) !important;
    min-height: 38px !important; white-space: nowrap !important;
}

.profile-tab-btn.tab-active {
    background: rgba(79,172,254,0.15) !important;
    color: #4facfe !important;
}

.profile-card {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    padding: 1.75rem !important;
    margin-bottom: 1rem;
}

.profile-input .q-field__control {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
.profile-input .q-field__control:hover {
    border-color: rgba(79,172,254,0.4) !important;
}
.profile-input .q-field__native { color: #fff !important; }
.profile-input .q-field__label { color: rgba(255,255,255,0.45) !important; }
.profile-input .q-field__bottom { display: none !important; }

.save-btn {
    background: linear-gradient(135deg, #4facfe, #00f2fe) !important;
    color: #0a0c10 !important; font-weight: 700 !important;
    border-radius: 12px !important; height: 46px !important;
}

.danger-btn {
    background: rgba(248,113,113,0.12) !important;
    border: 1px solid rgba(248,113,113,0.25) !important;
    color: #f87171 !important; font-weight: 600 !important;
    border-radius: 12px !important;
}

.fav-chip {
    background: rgba(79,172,254,0.12) !important;
    border: 1px solid rgba(79,172,254,0.25) !important;
    color: #4facfe !important; border-radius: 999px !important;
    padding: 0.3rem 0.9rem !important; font-size: 0.88rem !important;
    display: flex; align-items: center; gap: 0.5rem;
}

.history-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.75rem 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; margin-bottom: 0.5rem;
}

.notif-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.85rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.notif-row:last-child { border-bottom: none; }
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

        username = user['username']

        with ui.element('div').classes('app-container'):
            hero_background(None)
            navbar('/profile')

            with ui.element('div').classes('profile-page'):
                # ── Hero header ───────────────────────────────
                with ui.element('div').classes('profile-hero'):
                    with ui.element('div').classes('profile-avatar-big'):
                        avatar_label = ui.label(user.get('avatar', '?'))

                    with ui.column().style('gap:0.25rem;flex:1'):
                        name_display = ui.label(user.get('name', '')).style(
                            'font-family:Outfit,sans-serif;font-size:1.6rem;font-weight:700;color:#fff'
                        )
                        ui.label(user.get('email', '')).style('color:rgba(255,255,255,0.5);font-size:0.9rem')
                        ui.label(f'@{username}').style('color:rgba(255,255,255,0.3);font-size:0.85rem')

                    ui.button('Đăng xuất', icon='logout', on_click=_do_logout) \
                        .classes('danger-btn').props('flat no-caps')

                # ── Build tab panels TRƯỚC khi tạo nút tab ────
                with ui.element('div') as tab_info:
                    _render_info_tab(username, user, name_display, avatar_label)

                with ui.element('div').style('display:none') as tab_history:
                    _render_history_tab(username)

                with ui.element('div').style('display:none') as tab_favorites:
                    _render_favorites_tab(username)

                with ui.element('div').style('display:none') as tab_notifs:
                    _render_notifs_tab(username)

                tab_panels = [tab_info, tab_history, tab_favorites, tab_notifs]
                tab_names  = ['info', 'history', 'favorites', 'notifs']

                # ── Định nghĩa _switch_tab SAU khi có đủ biến ─
                def _switch_tab(name: str):
                    idx = tab_names.index(name)
                    for i, (panel, btn) in enumerate(zip(tab_panels, tabs)):
                        if i == idx:
                            panel.style('display:block')
                            btn.classes(add='tab-active')
                        else:
                            panel.style('display:none')
                            btn.classes(remove='tab-active')

                # ── Tabs (đặt DƯỚI panels để _switch_tab đã sẵn sàng) ──
                # Di chuyển tabs lên trên panels bằng CSS order
                with ui.row().classes('profile-tabs').style('order:-1;margin-bottom:1.5rem'):
                    t1 = ui.button('👤 Cá nhân',  on_click=lambda: _switch_tab('info')).classes('profile-tab-btn tab-active').props('flat no-caps')
                    t2 = ui.button('📍 Lịch sử',  on_click=lambda: _switch_tab('history')).classes('profile-tab-btn').props('flat no-caps')
                    t3 = ui.button('⭐ Yêu thích', on_click=lambda: _switch_tab('favorites')).classes('profile-tab-btn').props('flat no-caps')
                    t4 = ui.button('🔔 Thông báo', on_click=lambda: _switch_tab('notifs')).classes('profile-tab-btn').props('flat no-caps')

                tabs = [t1, t2, t3, t4]

            footer()


def _render_info_tab(username: str, user: dict, name_display, avatar_label):
    with ui.element('div').classes('profile-card'):
        ui.label('Thông tin cá nhân').style('font-weight:700;font-size:1.05rem;margin-bottom:1.25rem;color:#fff')
        n_name  = ui.input('Họ và tên', value=user.get('name', '')).classes('profile-input q-input-dark w-full mb-3').props('outlined dark')
        n_email = ui.input('Email',     value=user.get('email', '')).classes('profile-input q-input-dark w-full mb-4').props('outlined dark')

        msg = ui.label('').style('font-size:0.83rem;min-height:1rem;margin-bottom:0.5rem')

        def do_save():
            if not n_name.value.strip():
                msg.style('color:#f87171').set_text('❌ Tên không được để trống!')
                return
            ok = update_profile(username, n_name.value, n_email.value)
            if ok:
                set_current_user({**user, 'name': n_name.value.strip(), 'email': n_email.value.strip(),
                                  'avatar': n_name.value.strip()[0].upper()})
                name_display.set_text(n_name.value.strip())
                avatar_label.set_text(n_name.value.strip()[0].upper())
                msg.style('color:#4ade80').set_text('✅ Cập nhật thành công!')
            else:
                msg.style('color:#f87171').set_text('❌ Có lỗi xảy ra!')

        ui.button('Lưu thay đổi', on_click=do_save).classes('save-btn').props('unelevated no-caps')

    with ui.element('div').classes('profile-card'):
        ui.label('Đổi mật khẩu').style('font-weight:700;font-size:1.05rem;margin-bottom:1.25rem;color:#fff')
        p_old  = ui.input('Mật khẩu hiện tại', password=True, password_toggle_button=True).classes('profile-input q-input-dark w-full mb-3').props('outlined dark')
        p_new  = ui.input('Mật khẩu mới',      password=True, password_toggle_button=True).classes('profile-input q-input-dark w-full mb-3').props('outlined dark')
        p_conf = ui.input('Xác nhận mật khẩu', password=True, password_toggle_button=True).classes('profile-input q-input-dark w-full mb-4').props('outlined dark')

        pmsg = ui.label('').style('font-size:0.83rem;min-height:1rem;margin-bottom:0.5rem')

        def do_change_pass():
            if p_new.value != p_conf.value:
                pmsg.style('color:#f87171').set_text('❌ Mật khẩu xác nhận không khớp!')
                return
            if len(p_new.value) < 6:
                pmsg.style('color:#f87171').set_text('❌ Mật khẩu phải có ít nhất 6 ký tự!')
                return
            ok = change_password(username, p_old.value, p_new.value)
            if ok:
                pmsg.style('color:#4ade80').set_text('✅ Đổi mật khẩu thành công!')
                p_old.set_value(''); p_new.set_value(''); p_conf.set_value('')
            else:
                pmsg.style('color:#f87171').set_text('❌ Mật khẩu hiện tại không đúng!')

        ui.button('Đổi mật khẩu', on_click=do_change_pass).classes('save-btn').props('unelevated no-caps')


def _render_history_tab(username: str):
    with ui.element('div').classes('profile-card'):
        # Tạo history_container TRƯỚC, dùng trong do_clear
        with ui.element('div') as history_container:
            history = get_history(username)
            if not history:
                ui.label('Chưa có lịch sử truy cập.').style('color:rgba(255,255,255,0.4);padding:1rem 0')
            else:
                for h in history:
                    with ui.element('div').classes('history-item'):
                        with ui.column().style('gap:0.1rem'):
                            ui.label(f'📍 {h["city"]}').style('font-weight:600;color:#fff;font-size:0.95rem')
                            if h.get('brief'):
                                ui.label(h['brief']).style('color:rgba(255,255,255,0.5);font-size:0.8rem')
                        ui.label(h.get('time', '')).style('color:rgba(255,255,255,0.35);font-size:0.78rem;flex-shrink:0')

        def do_clear():
            clear_history(username)
            ui.notify('Đã xóa lịch sử!', type='positive')
            history_container.clear()
            with history_container:
                ui.label('Chưa có lịch sử truy cập.').style('color:rgba(255,255,255,0.4);padding:1rem 0')

        with ui.row().style('justify-content:space-between;align-items:center;margin-top:1rem'):
            ui.label('Lịch sử truy cập').style('font-weight:700;font-size:1.05rem;color:#fff')
            ui.button('Xóa tất cả', icon='delete', on_click=do_clear) \
                .classes('danger-btn').props('flat no-caps')


def _render_favorites_tab(username: str):
    with ui.element('div').classes('profile-card'):
        ui.label('Thành phố yêu thích').style('font-weight:700;font-size:1.05rem;margin-bottom:1.25rem;color:#fff')

        fav_container = ui.element('div').style('display:flex;flex-wrap:wrap;gap:0.75rem;margin-bottom:1.5rem')

        def refresh_favs():
            fav_container.clear()
            favs = get_favorites(username)
            if not favs:
                with fav_container:
                    ui.label('Chưa có thành phố yêu thích.').style('color:rgba(255,255,255,0.4)')
            else:
                for city in favs:
                    with fav_container:
                        with ui.element('div').classes('fav-chip'):
                            ui.label(city)
                            ui.button(icon='close', on_click=lambda c=city: _remove_fav(c)) \
                                .props('flat round dense').style('width:20px;height:20px;color:#4facfe;font-size:0.7rem')

        def _remove_fav(city: str):
            remove_favorite(username, city)
            ui.notify(f'Đã xóa {city}!', type='info')
            refresh_favs()

        refresh_favs()

        ui.separator().style('background:rgba(255,255,255,0.08);margin:0.5rem 0 1rem')
        with ui.row().style('gap:0.75rem;align-items:flex-start'):
            new_city = ui.input('Thêm thành phố...').classes('profile-input q-input-dark').props('outlined dark dense').style('flex:1')

            def do_add():
                city = new_city.value.strip()
                if not city:
                    return
                ok = add_favorite(username, city)
                if ok:
                    ui.notify(f'Đã thêm {city}!', type='positive')
                    new_city.set_value('')
                    refresh_favs()
                else:
                    ui.notify('Thành phố đã có trong danh sách!', type='warning')

            ui.button('Thêm', icon='add', on_click=do_add).classes('save-btn').props('unelevated no-caps')


def _render_notifs_tab(username: str):
    with ui.element('div').classes('profile-card'):
        ui.label('Cài đặt thông báo').style('font-weight:700;font-size:1.05rem;margin-bottom:1.25rem;color:#fff')

        notifs = get_notifications(username)

        items = [
            ('rain',    '🌧 Cảnh báo mưa',       'Thông báo khi có mưa lớn trong khu vực'),
            ('extreme', '⚠️ Thời tiết cực đoan',  'Bão, lũ lụt, nhiệt độ nguy hiểm'),
            ('daily',   '☀️ Báo cáo hàng ngày',   'Tóm tắt thời tiết lúc 7h sáng mỗi ngày'),
        ]

        switches = {}
        for key, label, desc in items:
            with ui.element('div').classes('notif-row'):
                with ui.column().style('gap:0.1rem'):
                    ui.label(label).style('font-weight:600;color:#fff;font-size:0.95rem')
                    ui.label(desc).style('color:rgba(255,255,255,0.45);font-size:0.8rem')
                switches[key] = ui.switch('', value=notifs.get(key, False)).props('color=cyan')

        nmsg = ui.label('').style('font-size:0.83rem;min-height:1rem;margin-top:0.75rem')

        def do_save_notifs():
            update_notifications(username, {k: s.value for k, s in switches.items()})
            nmsg.style('color:#4ade80').set_text('✅ Đã lưu cài đặt thông báo!')

        ui.button('Lưu cài đặt', on_click=do_save_notifs).classes('save-btn').props('unelevated no-caps').style('margin-top:1rem')


def _do_logout():
    logout_user()
    ui.navigate.to('/')
