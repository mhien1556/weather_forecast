from nicegui import ui
from src.common.config import set_current_user
from src.common.user_store import (
    login, register, verify_security, reset_password,
    get_security_question, SECURITY_QUESTIONS,
)

LOGIN_CSS = """
.auth-page-wrap {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    width: 100%;
    box-sizing: border-box;
}

.auth-glass-card {
    width: 100%;
    max-width: 440px;
    background: rgba(10, 12, 20, 0.75) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 28px !important;
    padding: 2.5rem 2.5rem 2rem !important;
    backdrop-filter: blur(30px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08);
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.auth-glass-card > * {
    width: 100%;
}

.auth-icon-wrap {
    width: 64px; height: 64px; border-radius: 20px;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1.25rem;
    box-shadow: 0 8px 25px rgba(79,172,254,0.35);
}

.auth-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    text-align: center;
    color: #fff !important;
    margin-bottom: 0.3rem !important;
}

.auth-subtitle {
    text-align: center;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.45);
    margin-bottom: 2rem;
}

.auth-tabs-wrap {
    display: flex !important;
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 4px;
    gap: 4px !important;
    margin-bottom: 1.75rem;
}

.auth-tab-btn {
    flex: 1 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem !important;
    transition: all 0.25s !important;
    color: rgba(255,255,255,0.45) !important;
    min-height: unset !important;
    white-space: nowrap !important;
}

.auth-tab-btn.is-active {
    background: rgba(79,172,254,0.2) !important;
    color: #4facfe !important;
    box-shadow: 0 2px 10px rgba(79,172,254,0.15) !important;
}

.auth-input {
    margin-bottom: 0.85rem !important;
    width: 100% !important;
}

.auth-input .q-field__control {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    padding: 0 1rem !important;
    height: 52px !important;
    transition: all 0.2s !important;
}

.auth-input .q-field__control:hover {
    border-color: rgba(79,172,254,0.4) !important;
    background: rgba(255,255,255,0.08) !important;
}

.auth-input .q-field__label {
    font-size: 0.88rem !important;
    color: rgba(255,255,255,0.45) !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
}

.auth-input.q-field--float .q-field__label {
    top: 8px !important;
    transform: none !important;
    font-size: 0.75rem !important;
}

.auth-input .q-field__native { color: #fff !important; font-size: 0.95rem !important; }
.auth-input .q-field__bottom { display: none !important; }

.auth-submit-btn {
    width: 100% !important;
    height: 52px !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
    color: #0a0c10 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    margin-top: 0.5rem !important;
    box-shadow: 0 6px 20px rgba(79,172,254,0.3) !important;
}

.auth-submit-btn:hover {
    box-shadow: 0 10px 30px rgba(79,172,254,0.45) !important;
}

.auth-error {
    background: rgba(248,113,113,0.12);
    border: 1px solid rgba(248,113,113,0.25);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    color: #f87171;
    font-size: 0.83rem;
    margin-bottom: 0.75rem;
}

.auth-success {
    background: rgba(74,222,128,0.12);
    border: 1px solid rgba(74,222,128,0.25);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    color: #4ade80;
    font-size: 0.83rem;
    margin-bottom: 0.75rem;
}

.forgot-link-btn {
    color: rgba(79,172,254,0.8) !important;
    font-size: 0.83rem !important;
    text-align: right !important;
    margin-top: -0.4rem !important;
    margin-bottom: 0.75rem !important;
    padding: 0 !important;
    min-height: unset !important;
    align-self: flex-end !important;
    display: block !important;
    margin-left: auto !important;
}
.forgot-link-btn:hover { color: #4facfe !important; }

.forgot-link {
    color: rgba(79,172,254,0.8) !important;
    font-size: 0.83rem;
    cursor: pointer;
    text-align: right;
    margin-top: -0.4rem;
    margin-bottom: 0.75rem;
    transition: color 0.2s;
}
.forgot-link:hover { color: #4facfe !important; }

.back-link {
    color: rgba(255,255,255,0.45) !important;
    font-size: 0.83rem;
    cursor: pointer;
    text-align: center;
    margin-top: 0.75rem;
    transition: color 0.2s;
}
.back-link:hover { color: #fff !important; }

.security-q-label {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.7);
    margin-bottom: 0.5rem;
    padding: 0.75rem 1rem;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    line-height: 1.4;
}
"""


def render_login_content():
    ui.add_css(LOGIN_CSS)

    with ui.card().classes('auth-glass-card').style('color:#fff'):

        # Icon
        with ui.element('div').classes('auth-icon-wrap'):
            ui.icon('cloud').style('font-size:28px;color:#0a0c10')

        title_el    = ui.label('Chào mừng trở lại').classes('auth-title')
        subtitle_el = ui.label('Đăng nhập để lưu thành phố yêu thích').classes('auth-subtitle')

        # Tab switcher (ẩn khi đang ở màn quên mật khẩu)
        with ui.row().classes('auth-tabs-wrap') as tabs_row:
            login_btn = ui.button('Đăng nhập', on_click=lambda: _switch('login')) \
                .classes('auth-tab-btn is-active').props('flat no-caps')
            reg_btn   = ui.button('Đăng ký',   on_click=lambda: _switch('register')) \
                .classes('auth-tab-btn').props('flat no-caps')

        # Thông báo chung
        err = ui.label('').classes('auth-error').style('display:none')
        suc = ui.label('').classes('auth-success').style('display:none')

        # ── 1. Login form ──────────────────────────────────
        with ui.element('div') as login_form:
            l_user = ui.input('Tên đăng nhập').classes('auth-input q-input-dark').props('outlined dark')
            l_pass = ui.input('Mật khẩu', password=True, password_toggle_button=True) \
                .classes('auth-input q-input-dark').props('outlined dark')

            # Link quên mật khẩu
            ui.button('Quên mật khẩu?', on_click=lambda: _switch('forgot_step1')) \
                .classes('forgot-link-btn').props('flat no-caps dense')

            def do_login():
                _hide_all(err, suc)
                user = login(l_user.value.strip(), l_pass.value)
                if user:
                    set_current_user(user)
                    ui.notify(f'Chào mừng, {user["name"]}! 👋', type='positive', position='top')
                    ui.navigate.to('/')
                else:
                    _show_err(err, '❌ Sai tên đăng nhập hoặc mật khẩu!')

            ui.button('Đăng nhập', on_click=do_login).classes('auth-submit-btn').props('unelevated no-caps')

        # ── 2. Register form ───────────────────────────────
        with ui.element('div').style('display:none') as reg_form:
            r_name  = ui.input('Họ và tên').classes('auth-input q-input-dark').props('outlined dark')
            r_user  = ui.input('Tên đăng nhập').classes('auth-input q-input-dark').props('outlined dark')
            r_email = ui.input('Email').classes('auth-input q-input-dark').props('outlined dark')
            r_pass  = ui.input('Mật khẩu', password=True, password_toggle_button=True) \
                .classes('auth-input q-input-dark').props('outlined dark')

            # Câu hỏi bảo mật khi đăng ký
            ui.label('Câu hỏi bảo mật (dùng khi quên mật khẩu)') \
                .style('font-size:0.8rem;color:rgba(255,255,255,0.45);margin-bottom:0.4rem')
            r_question = ui.select(SECURITY_QUESTIONS, value=SECURITY_QUESTIONS[0]) \
                .classes('auth-input q-input-dark').props('outlined dark')
            r_answer = ui.input('Câu trả lời bảo mật').classes('auth-input q-input-dark').props('outlined dark')

            def do_register():
                _hide_all(err, suc)
                if not r_name.value or not r_user.value or not r_pass.value:
                    _show_err(err, '❌ Vui lòng điền đầy đủ thông tin!')
                    return
                if not r_answer.value:
                    _show_err(err, '❌ Vui lòng điền câu trả lời bảo mật!')
                    return
                user = register(
                    r_user.value.strip(), r_name.value.strip(),
                    r_email.value.strip(), r_pass.value,
                    r_question.value, r_answer.value,
                )
                if user:
                    set_current_user(user)
                    ui.notify(f'Tạo tài khoản thành công! Chào {user["name"]} 🎉', type='positive', position='top')
                    ui.navigate.to('/')
                else:
                    _show_err(err, '❌ Tên đăng nhập đã tồn tại!')

            ui.button('Tạo tài khoản', on_click=do_register).classes('auth-submit-btn').props('unelevated no-caps')

        # ── 3. Quên mật khẩu - Bước 1: nhập username ──────
        with ui.element('div').style('display:none') as forgot1_form:
            f_user = ui.input('Nhập tên đăng nhập của bạn').classes('auth-input q-input-dark').props('outlined dark')

            def do_forgot1():
                _hide_all(err, suc)
                username = f_user.value.strip()
                q = get_security_question(username)
                if not q:
                    _show_err(err, '❌ Tên đăng nhập không tồn tại hoặc chưa thiết lập câu hỏi bảo mật!')
                    return
                # Lưu username tạm để dùng ở bước 2
                forgot_state['username'] = username
                forgot_state['question'] = q
                _switch('forgot_step2')

            ui.button('Tiếp theo', on_click=do_forgot1).classes('auth-submit-btn').props('unelevated no-caps')
            ui.label('← Quay lại đăng nhập').classes('back-link').on('click', lambda: _switch('login'))

        # ── 4. Quên mật khẩu - Bước 2: trả lời + mật khẩu mới
        with ui.element('div').style('display:none') as forgot2_form:
            question_label = ui.label('').classes('security-q-label')
            f_answer  = ui.input('Câu trả lời').classes('auth-input q-input-dark').props('outlined dark')
            f_newpass = ui.input('Mật khẩu mới', password=True, password_toggle_button=True) \
                .classes('auth-input q-input-dark').props('outlined dark')
            f_confirm = ui.input('Xác nhận mật khẩu mới', password=True, password_toggle_button=True) \
                .classes('auth-input q-input-dark').props('outlined dark')

            def do_reset():
                _hide_all(err, suc)
                username = forgot_state.get('username', '')
                if not f_answer.value:
                    _show_err(err, '❌ Vui lòng nhập câu trả lời!')
                    return
                if f_newpass.value != f_confirm.value:
                    _show_err(err, '❌ Mật khẩu xác nhận không khớp!')
                    return
                if len(f_newpass.value) < 6:
                    _show_err(err, '❌ Mật khẩu phải có ít nhất 6 ký tự!')
                    return
                if not verify_security(username, f_answer.value):
                    _show_err(err, '❌ Câu trả lời bảo mật không đúng!')
                    return
                reset_password(username, f_newpass.value)
                _show_suc(suc, '✅ Đặt lại mật khẩu thành công! Vui lòng đăng nhập lại.')
                f_answer.set_value('')
                f_newpass.set_value('')
                f_confirm.set_value('')
                import asyncio
                async def go_login():
                    await asyncio.sleep(2)
                    _switch('login')
                ui.timer(2.0, lambda: _switch('login'), once=True)

            ui.button('Đặt lại mật khẩu', on_click=do_reset).classes('auth-submit-btn').props('unelevated no-caps')
            ui.label('← Quay lại').classes('back-link').on('click', lambda: _switch('forgot_step1'))

        # ── State & switch logic ───────────────────────────
        forgot_state = {}

        def _switch(tab: str):
            _hide_all(err, suc)
            forms = {
                'login':        login_form,
                'register':     reg_form,
                'forgot_step1': forgot1_form,
                'forgot_step2': forgot2_form,
            }
            for name, form in forms.items():
                form.style('display:block' if name == tab else 'display:none')

            # Tabs chỉ hiện ở login/register
            tabs_row.style('display:flex' if tab in ('login', 'register') else 'display:none')

            if tab == 'login':
                login_btn.classes(add='is-active'); reg_btn.classes(remove='is-active')
                title_el.set_text('Chào mừng trở lại')
                subtitle_el.set_text('Đăng nhập để lưu thành phố yêu thích')
            elif tab == 'register':
                reg_btn.classes(add='is-active'); login_btn.classes(remove='is-active')
                title_el.set_text('Tạo tài khoản')
                subtitle_el.set_text('Tham gia WeatherNow hoàn toàn miễn phí')
            elif tab == 'forgot_step1':
                title_el.set_text('Quên mật khẩu')
                subtitle_el.set_text('Nhập tên đăng nhập để tiếp tục')
                f_user.set_value('')
            elif tab == 'forgot_step2':
                title_el.set_text('Xác minh danh tính')
                subtitle_el.set_text('Trả lời câu hỏi bảo mật để đặt lại mật khẩu')
                question_label.set_text(f'🔐 {forgot_state.get("question", "")}')


def _show_err(el, msg):
    el.set_text(msg); el.style('display:block')

def _show_suc(el, msg):
    el.set_text(msg); el.style('display:block')

def _hide_all(*els):
    for el in els:
        el.set_text(''); el.style('display:none')
