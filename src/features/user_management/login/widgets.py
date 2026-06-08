from nicegui import ui
from src.common.config import set_current_user
from src.database.user_store import (
    login, register, verify_security, reset_password,
    get_security_question, SECURITY_QUESTIONS,
)

# BỘ CSS MỚI: Siêu phẳng, tối giản, loại bỏ hoàn toàn dải màu gradient và shadow nặng
LOGIN_CSS = """
.auth-page-wrap {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    width: 100%;
    box-sizing: border-box;
}

.auth-glass-card {
    width: 100%;
    max-width: 400px;
    background: #121318 !important; 
    border: 1px solid #22252a !important; 
    border-radius: 12px !important; 
    padding: 2rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.15) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.auth-glass-card > * {
    width: 100%;
}

.auth-icon-wrap {
    width: 48px; height: 48px; 
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem;
}

.auth-title {
    font-family: sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    text-align: center;
    color: #fff !important;
    margin-bottom: 0.2rem !important;
}

.auth-subtitle {
    text-align: center;
    font-size: 0.85rem;
    color: #6c727f;
    margin-bottom: 1.5rem;
}

.auth-tabs-wrap {
    display: flex !important;
    justify-content: center !important;
    border-bottom: 1px solid #22252a;
    padding-bottom: 6px;
    margin-bottom: 1.5rem;
    gap: 0 !important;
}

.auth-tab-btn {
    flex: 1 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 0.4rem 0.2rem !important;
    color: #4e5361 !important;
    min-height: unset !important;
}

.auth-tab-btn.is-active {
    color: #4facfe !important; 
    font-weight: 600 !important;
}

.auth-input {
    margin-bottom: 1rem !important;
    width: 100% !important;
}

.auth-input .q-field__control {
    background: #1a1c23 !important;
    border: 1px solid #2d3139 !important;
    border-radius: 8px !important;
    padding: 0 0.85rem !important;
    height: 46px !important;
}

.auth-input .q-field__control:hover {
    border-color: #4facfe !important;
}

.auth-input .q-field__native { color: #fff !important; font-size: 0.9rem !important; }
.auth-input .q-field__bottom { display: none !important; }

.auth-submit-btn {
    width: 100% !important;
    height: 46px !important;
    border-radius: 8px !important;
    background: #4facfe !important; 
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-top: 0.5rem !important;
}

.auth-error {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    color: #ef4444;
    font-size: 0.8rem;
    margin-bottom: 0.75rem;
}

.auth-success {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    color: #22c55e;
    font-size: 0.8rem;
    margin-bottom: 0.75rem;
}

.forgot-link-btn {
    color: #6c727f !important;
    font-size: 0.8rem !important;
    margin-top: -0.5rem !important;
    margin-bottom: 0.75rem !important;
    padding: 0 !important;
    min-height: unset !important;
    margin-left: auto !important;
}
.forgot-link-btn:hover { color: #4facfe !important; }

.back-link {
    color: #6c727f !important;
    font-size: 0.8rem;
    cursor: pointer;
    text-align: center;
    margin-top: 1rem;
}
.back-link:hover { color: #fff !important; }
"""

def render_login_content():
    ui.add_css(LOGIN_CSS)

    with ui.element('div').classes('auth-page-wrap').style('min-height: 90vh'):
        with ui.card().classes('auth-glass-card').style('color:#fff'):

            with ui.element('div').classes('auth-icon-wrap'):
                ui.icon('cloud', size='32px').style('color:#4facfe')

            title_el    = ui.label('WeatherForecast').classes('auth-title')
            subtitle_el = ui.label('Đăng nhập hoặc chọn Bỏ qua để sử dụng ngay').classes('auth-subtitle')

            with ui.row().classes('auth-tabs-wrap') as tabs_row:
                login_btn = ui.button('Đăng nhập', on_click=lambda: _switch('login')) \
                    .classes('auth-tab-btn is-active').props('flat no-caps')
                reg_btn   = ui.button('Đăng ký',   on_click=lambda: _switch('register')) \
                    .classes('auth-tab-btn').props('flat no-caps')

            err = ui.label('').classes('auth-error').style('display:none')
            suc = ui.label('').classes('auth-success').style('display:none')

            # ── Giao diện Login ──────────────────────────────────
            with ui.element('div') as login_form:
                l_user = ui.input('Tên đăng nhập').classes('auth-input').props('outlined dark')
                l_pass = ui.input('Mật khẩu', password=True, password_toggle_button=True) \
                    .classes('auth-input').props('outlined dark')

                ui.button('Quên mật khẩu?', on_click=lambda: _switch('forgot_step1')) \
                    .classes('forgot-link-btn').props('flat no-caps dense')

                def do_login():
                    _hide_all(err, suc)
                    user = login(l_user.value.strip(), l_pass.value)
                    if user:
                        set_current_user(user)
                        ui.notify('Đăng nhập thành công! 👋', type='positive', position='top')
                        ui.navigate.to('/')
                    else:
                        _show_err(err, 'Sai tên đăng nhập hoặc mật khẩu!')

                ui.button('Đăng nhập', on_click=do_login).classes('auth-submit-btn').props('unelevated no-caps')
                
                # ✨ NÚT BẤM BYPASS: Bấm phát ăn ngay, vào thẳng app làm khách
                ui.button('Bỏ qua đăng nhập ➔', on_click=lambda: _bypass_login()) \
                    .classes('w-full mt-3 text-gray-400 text-xs text-center block hover:text-white').props('flat no-caps')

            # ── Giao diện Đăng ký ──────────────────
            with ui.element('div').style('display:none') as reg_form:
                r_name  = ui.input('Họ và tên').classes('auth-input').props('outlined dark')
                r_user  = ui.input('Tên đăng nhập').classes('auth-input').props('outlined dark')
                r_email = ui.input('Email').classes('auth-input').props('outlined dark')
                r_pass  = ui.input('Mật khẩu', password=True, password_toggle_button=True).classes('auth-input').props('outlined dark')

                r_question = ui.select(SECURITY_QUESTIONS, value=SECURITY_QUESTIONS[0]).classes('auth-input').props('outlined dark')
                r_answer = ui.input('Câu trả lời bảo mật').classes('auth-input').props('outlined dark')

                def do_register():
                    _hide_all(err, suc)
                    if not r_name.value or not r_user.value or not r_pass.value or not r_answer.value:
                        _show_err(err, 'Vui lòng điền đầy đủ thông tin!')
                        return
                    user = register(r_user.value.strip(), r_name.value.strip(), r_email.value.strip(), r_pass.value, r_question.value, r_answer.value)
                    if user:
                        _switch('login')
                        _show_suc(suc, 'Đăng ký tài khoản thành công!')
                    else:
                        _show_err(err, 'Tên đăng nhập đã tồn tại!')

                ui.button('Tạo tài khoản', on_click=do_register).classes('auth-submit-btn').props('unelevated no-caps')

            # ── Quên mật khẩu - Bước 1 ──────
            with ui.element('div').style('display:none') as forgot1_form:
                f_user = ui.input('Nhập tên đăng nhập').classes('auth-input').props('outlined dark')

                def do_forgot1():
                    _hide_all(err, suc)
                    username = f_user.value.strip()
                    q = get_security_question(username)
                    if not q:
                        _show_err(err, 'Tài khoản không tồn tại!')
                        return
                    forgot_state['username'] = username
                    forgot_state['question'] = q
                    _switch('forgot_step2')

                ui.button('Tiếp theo', on_click=do_forgot1).classes('auth-submit-btn').props('unelevated no-caps')
                ui.label('← Quay lại đăng nhập').classes('back-link').on('click', lambda: _switch('login'))

            # ── Quên mật khẩu - Bước 2 ──────
            with ui.element('div').style('display:none') as forgot2_form:
                question_label = ui.label('').classes('text-xs text-gray-400 mb-2 block')
                f_answer  = ui.input('Câu trả lời').classes('auth-input').props('outlined dark')
                f_newpass = ui.input('Mật khẩu mới', password=True, password_toggle_button=True).classes('auth-input').props('outlined dark')
                f_confirm = ui.input('Xác nhận mật khẩu mới', password=True, password_toggle_button=True).classes('auth-input').props('outlined dark')

                def do_reset():
                    _hide_all(err, suc)
                    username = forgot_state.get('username', '')
                    if f_newpass.value != f_confirm.value:
                        _show_err(err, 'Mật khẩu xác nhận không khớp!')
                        return
                    if not verify_security(username, f_answer.value):
                        _show_err(err, 'Câu trả lời bảo mật không chính xác!')
                        return
                    reset_password(username, f_newpass.value)
                    _show_suc(suc, 'Cập nhật mật khẩu mới thành công!')
                    ui.timer(1.5, lambda: _switch('login'), once=True)

                ui.button('Đặt lại mật khẩu', on_click=do_reset).classes('auth-submit-btn').props('unelevated no-caps')
                ui.label('← Quay lại').classes('back-link').on('click', lambda: _switch('forgot_step1'))

        # ── State & switch logic ───────────────────────────
        forgot_state = {}

        def _bypass_login():
            set_current_user({"name": "Khách", "username": "guest", "email": ""})
            ui.navigate.to('/')

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

            tabs_row.style('display:flex' if tab in ('login', 'register') else 'display:none')

            if tab == 'login':
                login_btn.classes(add='is-active'); reg_btn.classes(remove='is-active')
                title_el.set_text('WeatherForecast')
                subtitle_el.set_text('Đăng nhập hoặc chọn Bỏ qua để sử dụng ngay')
            elif tab == 'register':
                reg_btn.classes(add='is-active'); login_btn.classes(remove='is-active')
                title_el.set_text('Đăng ký')
                subtitle_el.set_text('Tạo tài khoản mới hoàn toàn miễn phí')
            elif tab == 'forgot_step1':
                title_el.set_text('Khôi phục')
                subtitle_el.set_text('Nhập tài khoản để lấy lại mật khẩu')
            elif tab == 'forgot_step2':
                title_el.set_text('Xác minh')
                subtitle_el.set_text('Vui lòng trả lời câu hỏi bảo mật dưới đây')
                question_label.set_text(f'📌 Câu hỏi: {forgot_state.get("question", "")}')

def _show_err(el, msg): el.set_text(msg); el.style('display:block')
def _show_suc(el, msg): el.set_text(msg); el.style('display:block')
def _hide_all(*els):
    for el in els: el.set_text(''); el.style('display:none')