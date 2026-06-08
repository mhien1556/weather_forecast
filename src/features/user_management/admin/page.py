from nicegui import ui, app
import json
from pathlib import Path
import hashlib
from src.database import user_store

# ── Palette ──────────────────────────────────────────────────────────────────
BG_PAGE    = '#0f1117'
BG_SIDEBAR = '#161b27'
BG_CARD    = '#1e2433'
BG_INPUT   = '#252b3b'
BORDER     = '#2d3448'
PRIMARY    = '#4f8ef7'
TEXT_MAIN  = '#f8fafc'
TEXT_SUB   = '#cbd5e1'
TEXT_MUTED = '#94a3b8'
SUCCESS    = '#22c55e'
WARNING    = '#f59e0b'
DANGER     = '#ef4444'

CARD_STYLE   = f'background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:20px;'
HEADER_STYLE = f'color:{TEXT_MAIN};font-weight:700;letter-spacing:.05em;'


def _inject_styles():
    ui.add_head_html(f'''<style>
      html, body {{ height:100%; margin:0; }}
      body, .q-page {{ background:{BG_PAGE} !important; color:{TEXT_MAIN}; }}
      .q-table {{ background:{BG_CARD} !important; color:{TEXT_MAIN}; }}
      .q-table thead tr {{ background:{BG_SIDEBAR} !important; }}
      .q-table tbody tr:hover {{ background:{BG_INPUT} !important; }}
      .q-table td, .q-table th {{ border-color:{BORDER} !important; color:{TEXT_MAIN} !important; }}
      .q-input .q-field__control,
      .q-select .q-field__control {{ background:{BG_INPUT} !important; border-color:{BORDER} !important; }}
      .q-input .q-field__native,
      .q-select .q-field__native {{ color:{TEXT_MAIN} !important; }}
      .q-field__label {{ color:{TEXT_SUB} !important; }}
      .q-menu {{ background:{BG_CARD} !important; color:{TEXT_MAIN} !important; }}
      .q-item {{ color:{TEXT_MAIN} !important; }}
      .q-dialog .q-card {{ background:{BG_CARD} !important; border:1px solid {BORDER}; }}
      ::-webkit-scrollbar {{ width:5px; }}
      ::-webkit-scrollbar-track {{ background:{BG_SIDEBAR}; }}
      ::-webkit-scrollbar-thumb {{ background:{BORDER}; border-radius:3px; }}
      .badge {{ display:inline-block;padding:2px 10px;border-radius:20px;font-size:.72rem;font-weight:600; }}
      .badge-super {{ background:rgba(245,158,11,.15);color:{WARNING}; }}
      .badge-admin {{ background:rgba(79,142,247,.15);color:{PRIMARY}; }}
      .badge-user  {{ background:rgba(136,146,164,.1);color:{TEXT_SUB}; }}
      .stat-card {{
        background:{BG_CARD};border:1px solid {BORDER};border-radius:14px;
        padding:22px;flex:1;min-width:150px;
        transition:transform .18s,box-shadow .18s;
      }}
      .stat-card:hover {{ transform:translateY(-3px);box-shadow:0 8px 28px rgba(0,0,0,.45); }}
      .nav-btn {{ border-radius:8px !important; transition:background .12s !important; }}
      .nav-btn:hover {{ background:{BG_INPUT} !important; }}
      .nav-active {{ background:{PRIMARY} !important; color:#fff !important; border-radius:8px !important; }}
      .act-btn {{ border-radius:6px !important; min-width:30px !important; }}
    </style>''')


class AdminPage:
    def __init__(self):
        pass

    def create(self):
        _inject_styles()
        if not app.storage.user.get('admin_logged_in'):
            self._login_page()
            return
        if not self._is_admin():
            ui.navigate.to('/')
            return
        self._layout()

    # ── Login ─────────────────────────────────────────────────────────────
    def _login_page(self):
        with ui.column().classes('items-center justify-center w-full').style(
                f'min-height:100vh;background:{BG_PAGE};'):
            with ui.card().style(f'width:420px;{CARD_STYLE}box-shadow:0 24px 64px rgba(0,0,0,.7);'):
                with ui.column().classes('items-center w-full').style('gap:4px;margin-bottom:20px;'):
                    ui.label('QUẢN TRỊ HỆ THỐNG').style(
                        f'color:{TEXT_MAIN};font-size:1.05rem;font-weight:700;letter-spacing:.12em;')
                    ui.label('WeatherForecast Admin').style(f'color:{TEXT_MUTED};font-size:.78rem;')

                ui.separator().style(f'background:{BORDER};margin-bottom:18px;')

                uname = ui.input('Tên đăng nhập').props('outlined dense').classes('w-full').style('margin-bottom:10px;')
                pwd   = ui.input('Mật khẩu', password=True, password_toggle_button=True).props('outlined dense').classes('w-full').style('margin-bottom:14px;')
                err   = ui.label().style(f'color:{DANGER};font-size:.78rem;text-align:center;width:100%;margin-bottom:8px;')
                err.visible = False

                def do_login():
                    err.visible = False
                    try:
                        user = user_store.get_user(uname.value)
                        if user:
                            hashed = hashlib.sha256(pwd.value.encode()).hexdigest()
                            if user.get('password') == hashed and user.get('role') in ['admin', 'super_admin']:
                                app.storage.user['admin_logged_in'] = True
                                app.storage.user['admin_username']  = uname.value
                                app.storage.user['admin_role']      = user.get('role')
                                app.storage.user.setdefault('admin_tab', 'dashboard')
                                ui.navigate.to('/admin')
                                return
                        err.set_text('Sai tên đăng nhập hoặc mật khẩu')
                        err.visible = True
                    except Exception as e:
                        err.set_text(f'Lỗi: {e}')
                        err.visible = True

                pwd.on('keydown.enter', do_login)
                ui.button('ĐĂNG NHẬP', on_click=do_login).props('unelevated').classes('w-full').style(
                    f'background:{PRIMARY};border-radius:8px;font-weight:700;height:42px;')


    def _is_admin(self):
        return app.storage.user.get('admin_role') in ['admin', 'super_admin']

    def _is_super(self):
        return app.storage.user.get('admin_role') == 'super_admin'

    # ── Layout ────────────────────────────────────────────────────────────
    def _layout(self):
        admin_user = app.storage.user.get('admin_username', 'Admin')
        role       = app.storage.user.get('admin_role', 'admin')
        current    = app.storage.user.get('admin_tab', 'dashboard')

        with ui.row().classes('w-full').style(f'height:100vh;background:{BG_PAGE};gap:0;overflow:hidden;'):
            # Sidebar
            with ui.column().style(
                    f'width:230px;min-width:230px;height:100vh;background:{BG_SIDEBAR};'
                    f'border-right:1px solid {BORDER};padding:18px 10px;gap:0;overflow:hidden;'):

                with ui.column().style('padding:0 8px;margin-bottom:20px;gap:2px;'):
                    ui.label('WeatherForecast').style(f'color:{TEXT_MAIN};font-weight:700;font-size:.95rem;')
                    ui.label('Admin Panel').style(f'color:{TEXT_MUTED};font-size:.72rem;')

                ui.separator().style(f'background:{BORDER};margin-bottom:14px;')
                ui.label('MENU').style(
                    f'color:{TEXT_MUTED};font-size:.62rem;letter-spacing:.12em;padding:0 8px;margin-bottom:6px;')

                self._nav('space_dashboard', 'Tổng quan',           'dashboard', current)
                self._nav('group',           'Quản lý người dùng',   'users',     current)

                ui.element('div').style('flex:1;min-height:0;')
                ui.separator().style(f'background:{BORDER};margin:14px 0;')

                badge_cls = 'badge-super' if role == 'super_admin' else 'badge-admin'
                with ui.column().style('gap:5px;padding:0 8px;'):
                    ui.label(admin_user).style(f'color:{TEXT_MAIN};font-weight:600;font-size:.88rem;')
                    ui.html(f'<span class="badge {badge_cls}">{role}</span>')

                ui.button('Đăng xuất', on_click=self._logout).props('flat no-caps').style(
                    f'color:{DANGER};width:100%;margin-top:8px;border-radius:8px;'
                    f'border:1px solid rgba(239,68,68,.25);font-size:.82rem;')

            # Main
            with ui.column().classes('col items-center').style(f'height:100vh;overflow-y:auto;padding:28px;gap:0;'):
                with ui.column().classes('w-full').style('max-width: 1200px;'):
                    if current == 'dashboard':
                        self._dashboard()
                    elif current == 'users':
                        self._users()

    def _nav(self, icon, text, tab, current):
        active = current == tab
        btn = ui.button(text, icon=icon, on_click=lambda t=tab: self._switch(t)).classes(
            'nav-active' if active else 'nav-btn').style(
            f'width:100%;text-align:left;justify-content:flex-start;'
            f'color:{"#ffffff !important" if active else TEXT_SUB};margin-bottom:3px;padding:8px 12px;font-size:.86rem;')
        btn.props('flat no-caps' if not active else 'unelevated no-caps text-color="white"')

    def _switch(self, tab):
        app.storage.user['admin_tab'] = tab
        ui.navigate.to('/admin')

    # ── Dashboard ─────────────────────────────────────────────────────────
    def _dashboard(self):
        users   = self._get_users()
        total   = len(users)
        admins  = sum(1 for u in users.values() if u.get('role') in ['admin', 'super_admin'])

        ui.label('Tổng quan').style(f'{HEADER_STYLE}font-size:1.35rem;margin-bottom:2px;')
        ui.label('Thống kê hệ thống WeatherForecast').style(f'color:{TEXT_MUTED};font-size:.82rem;margin-bottom:22px;')

        with ui.row().classes('w-full').style('gap:14px;flex-wrap:wrap;margin-bottom:28px;'):
            self._stat('group', str(total),        'Tổng người dùng', PRIMARY)
            self._stat('admin_panel_settings', str(admins),        'Quản trị viên',   WARNING)
            self._stat('person', str(total - admins), 'Người dùng',      SUCCESS)

        ui.label('NGƯỜI DÙNG GẦN ĐÂY').style(
            f'color:{TEXT_MUTED};font-size:.65rem;letter-spacing:.1em;margin-bottom:10px;')

        recent = list(users.items())[-5:]
        with ui.column().classes('w-full').style(f'{CARD_STYLE} padding: 0; overflow: hidden;'):
            with ui.row().classes('w-full items-center').style(f'background: #1e293b; padding: 10px 16px; border-bottom: 1px solid {BORDER};'):
                ui.label('TÀI KHOẢN').style(f'flex: 2; font-size: 0.75rem; font-weight: 700; color: {TEXT_MUTED};')
                ui.label('HỌ TÊN').style(f'flex: 2; font-size: 0.75rem; font-weight: 700; color: {TEXT_MUTED};')
                ui.label('VAI TRÒ').style(f'flex: 1.5; font-size: 0.75rem; font-weight: 700; color: {TEXT_MUTED};')
            
            if not recent:
                ui.label('Không có người dùng nào').style(f'padding: 16px; text-align: center; color: {TEXT_SUB}; w-full')
            
            for i, (u, info) in enumerate(recent):
                bg = 'transparent' if i % 2 == 0 else '#1e293b40'
                with ui.row().classes('w-full items-center').style(f'padding: 10px 16px; background: {bg}; border-bottom: 1px solid {BORDER};'):
                    ui.label(u).style(f'flex: 2; font-weight: 600; color: {TEXT_MAIN}; font-size: 0.85rem;')
                    ui.label(info.get('name', '-')).style(f'flex: 2; color: {TEXT_MAIN}; font-size: 0.85rem;')
                    role = info.get('role', 'user')
                    role_color = '#ef4444' if role == 'super_admin' else '#f59e0b' if role == 'admin' else '#3b82f6'
                    with ui.row().style('flex: 1.5;'):
                        ui.label(role).style(f'background: {role_color}20; color: {role_color}; padding: 2px 6px; border-radius: 8px; font-size: 0.7em; text-transform: uppercase; font-weight: 700; border: 1px solid {role_color}40;')

    def _stat(self, icon, value, label, color):
        with ui.element('div').classes('stat-card'):
            ui.icon(icon, size='1.8rem').style(f'color:{color};margin-bottom:8px;')
            ui.label(value).style(f'color:{color};font-size:1.9rem;font-weight:700;line-height:1;')
            ui.label(label).style(f'color:{TEXT_SUB};font-size:.8rem;margin-top:4px;')

    # ── Users ─────────────────────────────────────────────────────────────
    def _users(self):
        users = self._get_users()

        with ui.row().classes('w-full items-center').style('margin-bottom:22px;'):
            with ui.column().style('gap:2px;flex:1;'):
                ui.label('Quản lý người dùng').style(f'{HEADER_STYLE}font-size:1.35rem;')
                ui.label(f'{len(users)} người dùng trong hệ thống').style(f'color:{TEXT_MUTED};font-size:.82rem;')
            if self._is_super():
                ui.button('+ Thêm', on_click=self._add_dialog).props('unelevated no-caps').style(
                    f'background:{PRIMARY};border-radius:8px;font-weight:600;')

        ui.input('🔍  Tìm kiếm...').props('outlined dense').classes('w-full').style(
            f'margin-bottom:14px;max-width:380px;')

        def confirm_action(title, message, on_confirm):
            with ui.dialog() as dlg, ui.card().style(CARD_STYLE + "width: 400px;"):
                ui.label(title).style(f'{HEADER_STYLE}font-size: 1.15rem; color: {PRIMARY}; margin-bottom: 8px;')
                ui.label(message).style(f'color: {TEXT_MAIN}; font-size: 0.95rem; margin-bottom: 16px;')
                with ui.row().classes('w-full justify-end mt-2').style('gap: 8px;'):
                    ui.button('Hủy', on_click=dlg.close).props('flat no-caps').style(f'color: {TEXT_SUB};')
                    def _confirm():
                        dlg.close()
                        on_confirm()
                    ui.button('Đồng ý', on_click=_confirm).props('unelevated no-caps').style(f'background: {PRIMARY}; border-radius: 6px;')
            dlg.open()

        def do_reset(u):
            user = user_store.get_user(u)
            if user and user.get('role') != 'super_admin':
                import random, string
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                hashed = hashlib.sha256(new_password.encode()).hexdigest()
                user['password'] = hashed
                user_store.save_user(user)
                with ui.dialog() as dlg, ui.card().style(CARD_STYLE + "width: 350px; text-align: center; align-items: center;"):
                    ui.icon('check_circle', color='positive', size='3rem').style('margin-bottom: 8px;')
                    ui.label('Cấp lại thành công').style(f'{HEADER_STYLE}font-size: 1.1rem; color: {TEXT_MAIN}; margin-bottom: 4px;')
                    ui.label(f'Mật khẩu mới của {u} là:').style(f'color: {TEXT_SUB}; font-size: 0.9rem;')
                    ui.label(new_password).style(f'font-size: 1.4rem; font-family: monospace; font-weight: bold; color: #eab308; background: #1f2937; padding: 12px; border-radius: 8px; margin: 12px 0; letter-spacing: 2px;')
                    ui.button('Đóng', on_click=lambda: (dlg.close(), ui.navigate.to('/admin'))).props('unelevated no-caps').classes('w-full').style(f'background: {PRIMARY}; border-radius: 6px; margin-top: 8px;')
                dlg.open()
            else:
                ui.notify('Không thể reset mật khẩu Super Admin', type='negative')

        def do_toggle_admin(u):
            user = user_store.get_user(u)
            if user and user.get('role') != 'super_admin':
                if user.get('role') == 'admin':
                    user['role'] = 'user'
                    msg = f"Đã hủy quyền Admin của {u}"
                else:
                    user['role'] = 'admin'
                    msg = f"Đã cấp quyền Admin cho {u}"
                user_store.save_user(user)
                ui.notify(msg, type='positive')
                ui.navigate.to('/admin')
            else:
                ui.notify('Không thể thay đổi quyền của Super Admin', type='negative')

        def do_delete(u):
            user = user_store.get_user(u)
            if user and user.get('role') != 'super_admin':
                user_store.delete_user(u)
                ui.notify(f"Đã xóa người dùng {u}", type='positive')
                ui.navigate.to('/admin')
            else:
                ui.notify('Không thể xóa Super Admin', type='negative')

        with ui.column().classes('w-full').style(f'{CARD_STYLE} padding: 0; overflow: hidden;'):
            # Header
            with ui.row().classes('w-full items-center').style(f'background: #1e293b; padding: 12px 16px; border-bottom: 1px solid {BORDER};'):
                ui.label('TÀI KHOẢN').style(f'flex: 2; font-size: 0.8rem; font-weight: 700; color: {TEXT_MUTED};')
                ui.label('HỌ TÊN').style(f'flex: 2; font-size: 0.8rem; font-weight: 700; color: {TEXT_MUTED};')
                ui.label('EMAIL').style(f'flex: 3; font-size: 0.8rem; font-weight: 700; color: {TEXT_MUTED};')
                ui.label('VAI TRÒ').style(f'flex: 1.5; font-size: 0.8rem; font-weight: 700; color: {TEXT_MUTED};')
                ui.label('THAO TÁC').style(f'flex: 2; text-align: center; font-size: 0.8rem; font-weight: 700; color: {TEXT_MUTED};')
            
            # Rows
            if not users:
                ui.label('Không có người dùng nào').style(f'padding: 24px; text-align: center; color: {TEXT_SUB}; w-full')
            
            for i, (u, info) in enumerate(users.items()):
                bg = 'transparent' if i % 2 == 0 else '#1e293b40'
                with ui.row().classes('w-full items-center').style(f'padding: 12px 16px; background: {bg}; border-bottom: 1px solid {BORDER}; transition: background 0.2s;'):
                    ui.label(u).style(f'flex: 2; font-weight: 600; color: {TEXT_MAIN};')
                    ui.label(info.get('name', '-')).style(f'flex: 2; color: {TEXT_MAIN}; font-size: 0.9rem;')
                    ui.label(info.get('email', '-')).style(f'flex: 3; color: {TEXT_SUB}; font-size: 0.85rem; word-break: break-all;')
                    
                    role = info.get('role', 'user')
                    role_color = '#ef4444' if role == 'super_admin' else '#f59e0b' if role == 'admin' else '#3b82f6'
                    with ui.row().style('flex: 1.5;'):
                        ui.label(role).style(f'background: {role_color}20; color: {role_color}; padding: 3px 8px; border-radius: 12px; font-size: 0.75em; text-transform: uppercase; font-weight: 700; border: 1px solid {role_color}40;')

                    with ui.row().style('flex: 2; justify-content: center; gap: 4px;'):
                        ui.button(icon='visibility', on_click=lambda u=u: ui.navigate.to(f'/admin/user/{u}')).props('flat dense round size=sm').style('color: #4f8ef7;').tooltip('Xem chi tiết')
                        ui.button(icon='edit', on_click=lambda u=u: ui.navigate.to(f'/admin/edit/{u}')).props('flat dense round size=sm').style('color: #f59e0b;').tooltip('Sửa thông tin')
                        ui.button(icon='lock_reset', on_click=lambda u=u: confirm_action('Cấp lại mật khẩu', f'Bạn có chắc muốn cấp lại mật khẩu ngẫu nhiên cho người dùng "{u}"?', lambda u=u: do_reset(u))).props('flat dense round size=sm').style('color: #38bdf8;').tooltip('Cấp lại mật khẩu')
                        
                        if role == 'admin':
                            ui.button(icon='remove_moderator', on_click=lambda u=u: confirm_action('Hủy quyền Admin', f'Bạn có muốn hủy quyền Admin của "{u}"?', lambda u=u: do_toggle_admin(u))).props('flat dense round size=sm').style('color: #ef4444;').tooltip('Hủy quyền Admin')
                        else:
                            ui.button(icon='add_moderator', on_click=lambda u=u: confirm_action('Cấp quyền Admin', f'Bạn có muốn thăng cấp "{u}" thành Admin?', lambda u=u: do_toggle_admin(u))).props('flat dense round size=sm').style('color: #22c55e;').tooltip('Cấp quyền Admin')
                        
                        ui.button(icon='delete', on_click=lambda u=u: confirm_action('Xóa người dùng', f'Bạn có chắc chắn muốn xóa "{u}" khỏi hệ thống? Hành động này không thể hoàn tác.', lambda u=u: do_delete(u))).props('flat dense round size=sm').style('color: #ef4444;').tooltip('Xóa người dùng')

    # ── Add dialog ────────────────────────────────────────────────────────
    def _add_dialog(self):
        with ui.dialog() as dialog, ui.card().style(f'width:460px;{CARD_STYLE}'):
            ui.label('Thêm người dùng mới').style(f'{HEADER_STYLE}font-size:1.05rem;margin-bottom:14px;')
            uname = ui.input('Tên đăng nhập *').props('outlined dense').classes('w-full')
            fname = ui.input('Họ và tên').props('outlined dense').classes('w-full')
            email = ui.input('Email').props('outlined dense').classes('w-full')
            pwd   = ui.input('Mật khẩu *', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            role  = ui.select(['user', 'admin'], value='user', label='Vai trò').props('outlined dense').classes('w-full')

            def save():
                if not uname.value.strip() or not pwd.value:
                    ui.notify('Vui lòng nhập tên đăng nhập và mật khẩu!', type='warning')
                    return
                if user_store.get_user(uname.value.strip()):
                    ui.notify('Tên đăng nhập đã tồn tại!', type='negative')
                    return
                hashed = hashlib.sha256(pwd.value.encode()).hexdigest()
                new_user = {
                    'username': uname.value.strip(), 'name': fname.value or uname.value.strip(),
                    'email': email.value, 'password': hashed, 'role': role.value,
                    'avatar': uname.value[0].upper(), 'favorites': [], 'history': [],
                    'notifications': {'rain': True, 'extreme': True, 'daily': False},
                }
                user_store.save_user(new_user)
                ui.notify(f'Đã thêm: {uname.value}', type='positive')
                dialog.close()
                ui.navigate.to('/admin')

            with ui.row().classes('w-full justify-end').style('gap:8px;margin-top:14px;'):
                ui.button('Hủy', on_click=dialog.close).props('flat no-caps').style(f'color:{TEXT_SUB};')
                ui.button('Lưu', on_click=save).props('unelevated no-caps').style(
                    f'background:{PRIMARY};border-radius:8px;')
        dialog.open()

    # ── View user ─────────────────────────────────────────────────────────
    def view_user_detail(self, username: str):
        _inject_styles()
        users = self._get_users()
        user  = users.get(username)
        if not user:
            ui.navigate.to('/admin')
            return
        with ui.column().classes('items-center w-full').style(f'max-width:600px;margin:32px auto;padding:0 16px;gap:16px;'):
            ui.button('← Quay lại', on_click=lambda: ui.navigate.to('/admin')).props('flat no-caps').classes('self-start').style(
                f'color:{TEXT_SUB};margin-bottom:4px;')
            with ui.element('div').classes('w-full').style(CARD_STYLE):
                ui.label(f'Thông tin: {username}').style(
                    f'color:{PRIMARY};font-weight:700;font-size:1rem;margin-bottom:12px;')
                ui.separator().style(f'background:{BORDER};margin-bottom:12px;')
                for lbl, key in [('Họ tên','name'),('Email','email'),('Vai trò','role')]:
                    with ui.row().style('gap:8px;margin-bottom:6px;'):
                        ui.label(f'{lbl}:').style(f'color:{TEXT_MUTED};width:80px;font-size:.85rem;')
                        ui.label(user.get(key,'-')).style(f'color:{TEXT_MAIN};font-size:.85rem;')
            for title, key, empty in [
                ('Lịch sử tìm kiếm','history','Chưa có lịch sử'),
                ('Thành phố yêu thích','favorites','Chưa có thành phố yêu thích'),
            ]:
                with ui.element('div').classes('w-full').style(CARD_STYLE):
                    ui.label(title).style(f'color:{TEXT_MAIN};font-weight:600;margin-bottom:10px;')
                    items = user.get(key, [])
                    if items:
                        for item in (items[-10:] if key=='history' else items):
                            text = (f'{item.get("city","-")} — {item.get("time","-")}' if key=='history' else item)
                            ui.label(text).style(f'color:{TEXT_SUB};font-size:.82rem;')
                    else:
                        ui.label(empty).style(f'color:{TEXT_MUTED};font-size:.82rem;font-style:italic;')

    def edit_user_dialog(self, username: str):
        _inject_styles()
        users = self._get_users()
        user  = users.get(username)
        if not user:
            ui.navigate.to('/admin')
            return
        with ui.column().style(f'max-width:600px;margin:80px auto;padding:0 16px;'):
            with ui.element('div').style(CARD_STYLE):
                ui.label(f'Sửa thông tin: {username}').style(
                    f'{HEADER_STYLE}font-size:1.15rem;margin-bottom:14px;')
                name  = ui.input('Họ tên', value=user.get('name','')).props('outlined dense').classes('w-full')
                email = ui.input('Email',  value=user.get('email','')).props('outlined dense').classes('w-full').style('margin-top: 8px;')
                
                ui.input('Vai trò', value=user.get('role','user')).props('outlined dense disable').classes('w-full').style('margin-top: 8px;')
                ui.label('Không thể sửa vai trò từ đây. Hãy dùng nút Cấp/Hủy quyền Admin.').style(f'color:{TEXT_MUTED};font-size:.76rem;margin-top:4px;')

                def save():
                    user['name']  = name.value
                    user['email'] = email.value
                    user_store.save_user(user)
                    ui.notify('Đã cập nhật!', type='positive')
                    ui.navigate.to('/admin')

                with ui.row().classes('w-full justify-end').style('gap:8px;margin-top:20px;'):
                    ui.button('Hủy', on_click=lambda: ui.navigate.to('/admin')).props('flat no-caps').style(f'color:{TEXT_SUB};')
                    ui.button('Lưu thay đổi', on_click=save).props('unelevated no-caps').style(
                        f'background:{PRIMARY};border-radius:8px;')



    # ── Data ──────────────────────────────────────────────────────────────
    def _get_users(self) -> dict:
        return user_store.get_all_users()

    def _logout(self):
        app.storage.user.clear()
        ui.navigate.to('/admin')