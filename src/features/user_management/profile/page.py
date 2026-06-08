from nicegui import ui
from src.common.components import apply_theme, hero_background, navbar, footer
from src.common.config import get_current_user, set_current_user, logout_user
from src.database.user_store import (
    update_profile, change_password,
    get_history, clear_history,
    get_favorites, add_favorite, remove_favorite,
)
from datetime import datetime

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');

.pf-page {
    max-width: 800px; 
    margin: 0 auto;
    padding: 2rem 1rem 5rem;
    font-family: 'Outfit', sans-serif;
    position: relative;
    z-index: 10;
}

/* ── Hero card ── */
.pf-hero {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1.5rem;
    padding: 1.5rem 2rem;
    background: rgba(18, 19, 28, 0.95);
    border: 1px solid #2d3139;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}

.pf-avatar-wrap {
    width: 70px; height: 70px;
    border-radius: 50%;
    border: 2px solid #4facfe;
    padding: 2px;
    flex-shrink: 0;
}

.pf-avatar {
    width: 100%; height: 100%; border-radius: 50%;
    background: #4facfe;
    color: #fff; font-size: 1.6rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
}

.pf-name  { font-size: 1.3rem; font-weight: 700; color: #fff; line-height: 1.2; }
.pf-email { font-size: 0.85rem; color: #a0aec0; margin-top: 3px; }
.pf-user  { font-size: 0.8rem; color: #718096; margin-top: 2px; }

/* ── Tabs ── */
.pf-tabs {
    display: flex; gap: 8px;
    background: rgba(18, 19, 28, 0.95);
    border: 1px solid #2d3139;
    border-radius: 12px; 
    padding: 6px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
}

.pf-tab {
    flex: 1 !important; border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    color: #a0aec0 !important;
    min-height: 40px !important;
    transition: all 0.2s !important;
}

.pf-tab-on {
    background: #2d3139 !important;
    color: #4facfe !important;
    box-shadow: 0 0 0 1px rgba(79,172,254,0.4) !important;
}

/* ── Content Card ── */
.pf-card {
    background: rgba(18, 19, 28, 0.95) !important;
    border: 1px solid #2d3139 !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin-bottom: 1.5rem !important;
    width: 100% !important;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

.pf-section-title {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: #4facfe !important;
    margin-bottom: 1.5rem !important;
    display: block !important;
}

.pf-inp .q-field__control {
    background: #1a1c24 !important;
    border: 1px solid #3f444e !important;
    border-radius: 8px !important;
}
.pf-inp .q-field__control:hover  { border-color: #4facfe !important; }
.pf-inp .q-field__native  { color: #ffffff !important; font-size: 0.95rem !important; }
.pf-inp .q-field__label   { color: #a0aec0 !important; }

.pf-btn-primary {
    background: #4facfe !important;
    color: #fff !important; font-weight: 600 !important;
    border-radius: 8px !important; height: 42px !important;
    padding: 0 1.5rem !important;
}

.pf-btn-danger {
    background: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid rgba(239, 68, 68, 0.4) !important;
    color: #f87171 !important; font-weight: 500 !important;
    border-radius: 8px !important;
}

.pf-btn-logout { color: #a0aec0 !important; font-weight: 500 !important; font-size: 0.85rem !important; }
.pf-btn-logout:hover { color: #f87171 !important; }

.pf-row, .pf-fav-row {
    display: flex !important; align-items: center !important;
    justify-content: space-between !important;
    padding: 1rem 1.25rem !important;
    background: #1a1c24 !important;
    border: 1px solid #2d3139 !important;
    border-radius: 10px !important;
    margin-bottom: 0.6rem !important;
    width: 100% !important;
}

.pf-sep { background: rgba(255,255,255,0.08) !important; margin: 1.5rem 0 !important; }
.pf-note-ok  { color: #4ade80 !important; font-size: 0.85rem !important; font-weight: 500; }
.pf-note-err { color: #f87171 !important; font-size: 0.85rem !important; font-weight: 500; }
.pf-empty    { color: #a0aec0 !important; font-size: 0.9rem !important; padding: 1rem 0; }
"""

def register():
    @ui.page('/profile')
    def page():
        apply_theme()
        ui.add_css(CSS)

        user = get_current_user()
        if not user:
            ui.navigate.to('/login')
            return

        uname = user['username']
        tab = ui.context.client.request.query_params.get('tab', 'info')

        with ui.element('div').classes('app-container'):
            hero_background(None)
            navbar('/profile')

            with ui.element('div').classes('pf-page'):
                # Hero Card
                with ui.element('div').classes('pf-hero'):
                    avatar_data = user.get('avatar', '?')
                    with ui.element('div').classes('pf-avatar-wrap'):
                        with ui.element('div').classes('pf-avatar'):
                            if avatar_data.startswith('data:image') or avatar_data.startswith('http'):
                                ui.image(avatar_data).style('width:100%;height:100%;object-fit:cover;')
                            else:
                                ui.label(user.get('name', '?')[0].upper())

                    with ui.column().style('gap:4px'):
                        ui.label(user.get('name','')).classes('pf-name')
                        ui.label(user.get('email','')).classes('pf-email')
                        ui.label(f'@{uname}').classes('pf-user')

                    ui.button('Đăng xuất', icon='logout',
                        on_click=lambda: [logout_user(), ui.navigate.to('/')]) \
                        .classes('pf-btn-logout').props('flat no-caps')

                # Tabs Navigation
                with ui.row().classes('pf-tabs w-full'):
                    tabs_config = [
                        ('info', 'person', 'Cá nhân'),
                        ('history', 'history', 'Lịch sử'),
                        ('favorites', 'star_border', 'Yêu thích')
                    ]
                    for key, icon_name, lbl in tabs_config:
                        cls = 'pf-tab pf-tab-on' if tab == key else 'pf-tab'
                        with ui.button(on_click=lambda k=key: ui.navigate.to(f'/profile?tab={k}')) \
                                .classes(cls).props('flat no-caps'):
                            with ui.row().classes('items-center gap-2 justify-center w-full'):
                                ui.icon(icon_name, size='20px')
                                ui.label(lbl)

                # Content Area
                with ui.column().classes('w-full').style('gap:0'):
                    if   tab == 'info':          _info(uname, user)
                    elif tab == 'history':       _history(uname)
                    elif tab == 'favorites':     _favorites(uname)

            footer()

def _info(uname, user):
    with ui.element('div').classes('pf-card'):
        ui.label('Thông tin cá nhân').classes('pf-section-title')
        f_name  = ui.input('Họ và tên', value=user.get('name','')).classes('pf-inp w-full mb-4').props('outlined dark')
        f_email = ui.input('Email',     value=user.get('email','')).classes('pf-inp w-full mb-4').props('outlined dark')
        note = ui.label('').classes('pf-note-ok')
        def save():
            if not f_name.value.strip():
                note.classes(remove='pf-note-ok').classes(add='pf-note-err'); note.set_text('❌ Tên không được để trống!'); return
            update_profile(uname, f_name.value, f_email.value)
            set_current_user({**user, 'name': f_name.value.strip(), 'email': f_email.value.strip()})
            note.classes(remove='pf-err').classes(add='pf-note-ok'); note.set_text('✅ Đã lưu thành công!')
        ui.button('Lưu thay đổi', on_click=save).classes('pf-btn-primary').props('unelevated no-caps')

    with ui.element('div').classes('pf-card'):
        ui.label('Đổi mật khẩu').classes('pf-section-title')
        p_old  = ui.input('Mật khẩu hiện tại', password=True, password_toggle_button=True).classes('pf-inp w-full mb-4').props('outlined dark')
        p_new  = ui.input('Mật khẩu mới', password=True, password_toggle_button=True).classes('pf-inp w-full mb-4').props('outlined dark')
        p_cf   = ui.input('Xác nhận mật khẩu', password=True, password_toggle_button=True).classes('pf-inp w-full mb-4').props('outlined dark')
        pnote  = ui.label('').classes('pf-note-ok')
        def chpass():
            if p_new.value != p_cf.value: pnote.classes(remove='pf-note-ok').classes(add='pf-note-err'); pnote.set_text('❌ Mật khẩu mới xác nhận không khớp!'); return
            if change_password(uname, p_old.value, p_new.value): pnote.set_text('✅ Đổi mật khẩu thành công!')
            else: pnote.classes(remove='pf-note-ok').classes(add='pf-note-err'); pnote.set_text('❌ Mật khẩu hiện tại sai!')
        ui.button('Đổi mật khẩu', on_click=chpass).classes('pf-btn-primary').props('unelevated no-caps')

def _history(uname):
    with ui.element('div').classes('pf-card'):
        with ui.row().style('justify-content:space-between;align-items:center;margin-bottom:1.5rem;width:100%'):
            ui.label('Lịch sử truy cập').classes('pf-section-title').style('margin-bottom:0')
            ui.button('🗑 Xóa tất cả', on_click=lambda: [clear_history(uname), ui.navigate.to('/profile?tab=history')]).classes('pf-btn-danger').props('flat no-caps')
        items = get_history(uname)
        if not items: ui.label('Chưa có lịch sử truy cập nào.').classes('pf-empty')
        else:
            for h in items:
                with ui.element('div').classes('pf-row'):
                    with ui.row().style('align-items:center;gap:0.75rem'):
                        ui.icon('location_on', size='20px').style('color:#4facfe'); ui.label(h.get('city','')).style('color:#ffffff;font-weight:600')
                    ui.label(h.get('time','')).style('color:#a0aec0;font-size:0.8rem')

def _favorites(uname):
    with ui.element('div').classes('pf-card'):
        ui.label('Thành phố yêu thích').classes('pf-section-title')
        favs = get_favorites(uname)
        if not favs: ui.label('Danh sách yêu thích đang trống.').classes('pf-empty')
        else:
            for city in favs:
                with ui.element('div').classes('pf-fav-row'):
                    with ui.row().style('align-items:center;gap:0.75rem'):
                        ui.icon('star', size='20px').style('color:#facc15'); ui.label(city).style('color:#ffffff;font-weight:600')
                    ui.button(icon='close', on_click=lambda c=city: [remove_favorite(uname, c), ui.navigate.to('/profile?tab=favorites')]).props('flat round dense').style('color:#f87171')

# ──────────────────────────── THÔNG BÁO ──────────────────────────────────────

@ui.refreshable
def notification_list(username: str):
    """Danh sách lịch sử thông báo, tự động refresh khi gọi .refresh()"""
    history = get_notification_history(username)
    if not history:
        ui.label('Chưa có thông báo nào được ghi nhận.').classes('pf-empty')
    else:
        with ui.column().classes('w-full').style('gap:10px'):
            for msg in history:
                ui.chat_message(
                    text=msg['content'],
                    name='Hệ thống',
                    stamp=msg['created_at'],
                    sent=True
                ).classes('w-full')

def _notifications(uname):
    # --- Phần cài đặt thông báo hàng ngày ---
    with ui.element('div').classes('pf-card'):
        ui.label('Cài đặt thông báo hàng ngày').classes('pf-section-title')
        notif_settings = get_notifications(uname)
        daily_switch = ui.switch('Gửi báo cáo thời tiết mỗi ngày', value=notif_settings['daily'])
        time_input = ui.input('Giờ gửi (HH:MM)', value=notif_settings['daily_time']).props('mask="##:##"')
        daily_switch.bind_value_to(time_input, 'visible')
        
        async def save_notif_settings():
            new_settings = {
                'daily': daily_switch.value,
                'daily_time': time_input.value if daily_switch.value else '07:00',
                'rain': notif_settings.get('rain', True),
                'extreme': notif_settings.get('extreme', True),
            }
            update_notifications(uname, new_settings)
            ui.notify('Đã lưu cài đặt thông báo', type='positive', position='top')
        
        ui.button('Lưu cài đặt', on_click=save_notif_settings).classes('pf-btn-primary mt-2')

    # --- Phần lịch sử thông báo + real-time + nút test ---
    with ui.element('div').classes('pf-card'):
        with ui.row().style('justify-content:space-between;align-items:center;margin-bottom:1rem;width:100%'):
            ui.label('Lịch sử thông báo').classes('pf-section-title').style('margin-bottom:0')
            async def clear_history():
                delete_all_notification_history(uname)
                notification_list.refresh()
                ui.notify('Đã xóa toàn bộ lịch sử thông báo', type='positive', position='top')
            ui.button('🗑 Xóa tất cả', on_click=clear_history).classes('pf-btn-danger').props('flat no-caps')
        
        # Nút test thử
        async def send_test():
            from datetime import datetime
            test_content = f"🔔 Thông báo thử lúc {datetime.now().strftime('%H:%M:%S')}"
            save_notification_history(uname, test_content)
            # Cập nhật last_seen để client nhận ngay
            update_last_notification_seen(uname, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            notification_list.refresh()
            ui.notify("✅ Đã gửi thông báo thử!", type='positive', position='top')
        ui.button('📨 Gửi thông báo thử', on_click=send_test).classes('pf-btn-primary mt-1').props('flat')
        
        # Danh sách refreshable
        notification_list(uname)

    # --- Timer kiểm tra thông báo mới (real-time notify) ---
    last_seen = get_last_notification_seen(uname) or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    async def check_new_notifications():
        nonlocal last_seen
        new_msgs = get_new_notifications_since(uname, last_seen)
        if new_msgs:
            # Cập nhật last_seen thành thời gian mới nhất
            latest_time = max(msg['created_at'] for msg in new_msgs)
            last_seen = latest_time
            update_last_notification_seen(uname, latest_time)
            # Hiển thị notify cho từng tin nhắn mới
            for msg in new_msgs:
                ui.notify(msg['content'], type='info', position='top', timeout=5000)
            # Làm mới danh sách lịch sử
            notification_list.refresh()
    
    ui.timer(3, check_new_notifications)