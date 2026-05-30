from nicegui import ui
from src.common.components import apply_theme, hero_background, navbar, footer
from src.common.config import get_current_user, set_current_user, logout_user
from src.common.user_store import (
    update_profile, change_password,
    get_history, clear_history,
    get_favorites, add_favorite, remove_favorite,
    get_notifications, update_notifications,
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');

.pf-page {
    max-width: 960px; margin: 0 auto;
    padding: 2.5rem 1.5rem 5rem;
    font-family: 'Outfit', sans-serif;
}

/* ── Hero card ── */
.pf-hero {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1.5rem;
    padding: 1.75rem 2rem;
    background: rgba(10,14,26,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    backdrop-filter: blur(24px);
    margin-bottom: 1.75rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.pf-avatar {
    width: 72px; height: 72px; border-radius: 50%;
    background: linear-gradient(135deg, #e91e63 0%, #9c27b0 100%);
    color: #fff; font-size: 1.9rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 0 3px rgba(233,30,99,0.25), 0 6px 20px rgba(233,30,99,0.3);
    flex-shrink: 0;
}

.pf-name  { font-size: 1.45rem; font-weight: 700; color: #fff; line-height: 1.2; }
.pf-email { font-size: 0.85rem; color: rgba(255,255,255,0.5); margin-top: 3px; }
.pf-user  { font-size: 0.78rem; color: rgba(255,255,255,0.28); margin-top: 2px; }

/* ── Tabs ── */
.pf-tabs {
    display: flex; gap: 5px;
    background: rgba(10,14,26,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 5px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
}

.pf-tab {
    flex: 1 !important; border-radius: 11px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    color: rgba(255,255,255,0.38) !important;
    min-height: 38px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.2px !important;
}

.pf-tab-on {
    background: rgba(79,172,254,0.16) !important;
    color: #4facfe !important;
    box-shadow: 0 0 0 1px rgba(79,172,254,0.3) !important;
}

/* ── Cards ── */
.pf-card {
    background: rgba(10,14,26,0.55) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 20px !important;
    padding: 1.75rem !important;
    margin-bottom: 1rem !important;
    width: 100% !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
}

.pf-section-title {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: rgba(79,172,254,0.8) !important;
    margin-bottom: 1.25rem !important;
    display: block !important;
}

/* ── Inputs ── */
.pf-inp .q-field__control {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    transition: all 0.2s !important;
}
.pf-inp .q-field__control:hover  { border-color: rgba(79,172,254,0.4) !important; background: rgba(255,255,255,0.07) !important; }
.pf-inp.q-field--focused .q-field__control { border-color: rgba(79,172,254,0.6) !important; box-shadow: 0 0 0 3px rgba(79,172,254,0.1) !important; }
.pf-inp .q-field__native  { color: #fff !important; font-family: 'Outfit', sans-serif !important; }
.pf-inp .q-field__label   { color: rgba(255,255,255,0.38) !important; }
.pf-inp .q-field__bottom  { display: none !important; }

/* ── Buttons ── */
.pf-btn-primary {
    background: linear-gradient(135deg, #4facfe, #00f2fe) !important;
    color: #0a0c14 !important; font-weight: 700 !important;
    border-radius: 12px !important; height: 44px !important;
    font-family: 'Outfit', sans-serif !important;
    box-shadow: 0 4px 16px rgba(79,172,254,0.25) !important;
    transition: all 0.2s !important;
}
.pf-btn-primary:hover { box-shadow: 0 6px 22px rgba(79,172,254,0.4) !important; }

.pf-btn-danger {
    background: transparent !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    color: #f87171 !important; font-weight: 600 !important;
    border-radius: 11px !important;
    font-family: 'Outfit', sans-serif !important;
}
.pf-btn-danger:hover { background: rgba(248,113,113,0.1) !important; }

.pf-btn-logout {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.7) !important; font-weight: 600 !important;
    border-radius: 12px !important; font-size: 0.85rem !important;
    font-family: 'Outfit', sans-serif !important;
}
.pf-btn-logout:hover { background: rgba(255,255,255,0.1) !important; color: #fff !important; }

/* ── List rows ── */
.pf-row {
    display: flex !important; align-items: center !important;
    justify-content: space-between !important;
    padding: 0.8rem 1rem !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    margin-bottom: 0.45rem !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.pf-row:hover { background: rgba(255,255,255,0.06) !important; }

.pf-fav-row {
    display: flex !important; align-items: center !important;
    justify-content: space-between !important;
    padding: 0.8rem 1rem !important;
    background: rgba(79,172,254,0.06) !important;
    border: 1px solid rgba(79,172,254,0.15) !important;
    border-radius: 12px !important;
    margin-bottom: 0.45rem !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.pf-fav-row:hover { background: rgba(79,172,254,0.1) !important; }

.pf-notif-row {
    display: flex !important; align-items: center !important;
    justify-content: space-between !important;
    padding: 1rem 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.07) !important;
    width: 100% !important;
}
.pf-notif-row:last-of-type { border-bottom: none !important; }

.pf-sep { background: rgba(255,255,255,0.07) !important; margin: 1rem 0 !important; }

.pf-note-ok  { color: #4ade80 !important; font-size: 0.82rem !important; min-height: 1rem !important; margin-top: 0.4rem !important; }
.pf-note-err { color: #f87171 !important; font-size: 0.82rem !important; min-height: 1rem !important; margin-top: 0.4rem !important; }
.pf-empty    { color: rgba(255,255,255,0.35) !important; font-size: 0.88rem !important; padding: 0.75rem 0 !important; }
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
        tab   = ui.context.client.request.query_params.get('tab', 'info')

        with ui.element('div').classes('app-container'):
            hero_background(None)
            navbar('/profile')

            with ui.element('div').classes('pf-page'):

                # ── Hero ─────────────────────────────────────
                with ui.element('div').classes('pf-hero'):
                    with ui.element('div').classes('pf-avatar'):
                        ui.label(user.get('avatar', user.get('name','?')[0].upper()))

                    with ui.column().style('gap:1px'):
                        ui.label(user.get('name','')).classes('pf-name')
                        ui.label(user.get('email','')).classes('pf-email')
                        ui.label(f'@{uname}').classes('pf-user')

                    ui.button('Đăng xuất', icon='logout',
                        on_click=lambda: [logout_user(), ui.navigate.to('/')]) \
                        .classes('pf-btn-logout').props('flat no-caps')

                # ── Tabs ──────────────────────────────────────
                with ui.row().classes('pf-tabs'):
                    for key, lbl in [('info','👤 Cá nhân'),('history','📍 Lịch sử'),
                                     ('favorites','⭐ Yêu thích'),('notifs','🔔 Thông báo')]:
                        cls = 'pf-tab pf-tab-on' if tab == key else 'pf-tab'
                        ui.button(lbl,
                            on_click=lambda k=key: ui.navigate.to(f'/profile?tab={k}')) \
                            .classes(cls).props('flat no-caps')

                # ── Content ───────────────────────────────────
                if   tab == 'info':      _info(uname, user)
                elif tab == 'history':   _history(uname)
                elif tab == 'favorites': _favorites(uname)
                elif tab == 'notifs':    _notifs(uname)

            footer()


def _info(uname, user):
    with ui.element('div').classes('pf-card'):
        ui.label('Thông tin cá nhân').classes('pf-section-title')

        f_name  = ui.input('Họ và tên', value=user.get('name','')) \
                    .classes('pf-inp w-full mb-3').props('outlined dark')
        f_email = ui.input('Email',     value=user.get('email','')) \
                    .classes('pf-inp w-full mb-3').props('outlined dark')
        note = ui.label('').classes('pf-note-ok')

        def save():
            if not f_name.value.strip():
                note.classes(remove='pf-note-ok').classes(add='pf-note-err')
                note.set_text('❌ Tên không được để trống!'); return
            update_profile(uname, f_name.value, f_email.value)
            set_current_user({**user, 'name': f_name.value.strip(),
                              'email': f_email.value.strip(),
                              'avatar': f_name.value.strip()[0].upper()})
            note.classes(remove='pf-note-err').classes(add='pf-note-ok')
            note.set_text('✅ Đã lưu thành công!')

        ui.button('Lưu thay đổi', on_click=save) \
            .classes('pf-btn-primary').props('unelevated no-caps')

    with ui.element('div').classes('pf-card'):
        ui.label('Đổi mật khẩu').classes('pf-section-title')

        p_old  = ui.input('Mật khẩu hiện tại', password=True, password_toggle_button=True) \
                    .classes('pf-inp w-full mb-3').props('outlined dark')
        p_new  = ui.input('Mật khẩu mới',      password=True, password_toggle_button=True) \
                    .classes('pf-inp w-full mb-3').props('outlined dark')
        p_cf   = ui.input('Xác nhận mật khẩu', password=True, password_toggle_button=True) \
                    .classes('pf-inp w-full mb-3').props('outlined dark')
        pnote  = ui.label('').classes('pf-note-ok')

        def chpass():
            if p_new.value != p_cf.value:
                pnote.classes(remove='pf-note-ok').classes(add='pf-note-err')
                pnote.set_text('❌ Mật khẩu không khớp!'); return
            if len(p_new.value) < 6:
                pnote.classes(remove='pf-note-ok').classes(add='pf-note-err')
                pnote.set_text('❌ Tối thiểu 6 ký tự!'); return
            from src.common.user_store import change_password
            ok = change_password(uname, p_old.value, p_new.value)
            if ok:
                pnote.classes(remove='pf-note-err').classes(add='pf-note-ok')
                pnote.set_text('✅ Đổi mật khẩu thành công!')
                p_old.set_value(''); p_new.set_value(''); p_cf.set_value('')
            else:
                pnote.classes(remove='pf-note-ok').classes(add='pf-note-err')
                pnote.set_text('❌ Mật khẩu hiện tại không đúng!')

        ui.button('Đổi mật khẩu', on_click=chpass) \
            .classes('pf-btn-primary').props('unelevated no-caps')


def _history(uname):
    with ui.element('div').classes('pf-card'):
        with ui.row().style('justify-content:space-between;align-items:center;margin-bottom:1.25rem;width:100%'):
            ui.label('Lịch sử truy cập').classes('pf-section-title').style('margin-bottom:0')
            ui.button('🗑 Xóa tất cả', on_click=lambda: [
                clear_history(uname),
                ui.notify('Đã xóa lịch sử!', type='positive'),
                ui.navigate.to('/profile?tab=history')
            ]).classes('pf-btn-danger').props('flat no-caps')

        items = get_history(uname)
        if not items:
            ui.label('Chưa có lịch sử truy cập nào.').classes('pf-empty')
        else:
            for h in items:
                with ui.element('div').classes('pf-row'):
                    with ui.row().style('align-items:center;gap:0.75rem'):
                        ui.icon('location_on').style('color:#4facfe;font-size:1.1rem')
                        with ui.column().style('gap:1px'):
                            ui.label(h.get('city','')).style('color:#fff;font-weight:600;font-size:0.9rem')
                    ui.label(h.get('time','')).style('color:rgba(255,255,255,0.3);font-size:0.75rem')


def _favorites(uname):
    with ui.element('div').classes('pf-card'):
        ui.label('Thành phố yêu thích').classes('pf-section-title')

        favs = get_favorites(uname)
        if not favs:
            ui.label('Chưa có thành phố nào trong danh sách.').classes('pf-empty')
        else:
            for city in favs:
                with ui.element('div').classes('pf-fav-row'):
                    with ui.row().style('align-items:center;gap:0.6rem'):
                        ui.icon('star').style('color:#facc15;font-size:1rem')
                        ui.label(city).style('color:#fff;font-weight:600;font-size:0.9rem')
                    ui.button(icon='close', on_click=lambda c=city: [
                        remove_favorite(uname, c),
                        ui.notify(f'Đã xóa {c}', type='info'),
                        ui.navigate.to('/profile?tab=favorites')
                    ]).props('flat round dense').style('color:rgba(248,113,113,0.7);width:28px;height:28px')

        ui.element('div').classes('pf-sep')

        with ui.row().style('gap:0.75rem;align-items:center;width:100%'):
            inp = ui.input('Thêm thành phố mới...') \
                    .classes('pf-inp').props('outlined dark dense').style('flex:1')

            def add():
                c = inp.value.strip()
                if not c: return
                ok = add_favorite(uname, c)
                if ok:
                    ui.notify(f'Đã thêm {c}!', type='positive')
                    ui.navigate.to('/profile?tab=favorites')
                else:
                    ui.notify('Thành phố đã có trong danh sách!', type='warning')

            ui.button('+ Thêm', on_click=add) \
                .classes('pf-btn-primary').props('unelevated no-caps')


def _notifs(uname):
    with ui.element('div').classes('pf-card'):
        ui.label('Cài đặt thông báo').classes('pf-section-title')

        cfg = get_notifications(uname)
        rows = [
            ('rain',    '🌧', 'Cảnh báo mưa',      'Thông báo khi có mưa lớn trong khu vực'),
            ('extreme', '⚠️', 'Thời tiết cực đoan', 'Bão, lũ lụt, nhiệt độ nguy hiểm'),
            ('daily',   '☀️', 'Báo cáo hàng ngày',  'Tóm tắt thời tiết lúc 7h sáng'),
        ]
        sw = {}
        for k, icon, lbl, desc in rows:
            with ui.element('div').classes('pf-notif-row'):
                with ui.row().style('align-items:center;gap:0.75rem;flex:1'):
                    ui.label(icon).style('font-size:1.2rem;width:1.5rem')
                    with ui.column().style('gap:1px'):
                        ui.label(lbl).style('color:#fff;font-weight:600;font-size:0.9rem')
                        ui.label(desc).style('color:rgba(255,255,255,0.38);font-size:0.78rem')
                sw[k] = ui.switch('', value=cfg.get(k, False)).props('color=cyan')

        note = ui.label('').classes('pf-note-ok').style('margin-top:0.75rem')

        def save():
            update_notifications(uname, {k: s.value for k, s in sw.items()})
            note.set_text('✅ Đã lưu cài đặt!')

        ui.button('Lưu cài đặt', on_click=save) \
            .classes('pf-btn-primary').props('unelevated no-caps').style('margin-top:1.25rem')
