from nicegui import ui

def render_login_content():
    with ui.element('div').style('display:flex; justify-content:center; align-items:center; min-height:60vh; w-full'):
        with ui.card().classes('card').style('width:100%; max-width:400px; padding:2rem;'):
            ui.label('Đăng nhập').classes('text-h5 text-center w-full font-bold mb-6')
            
            ui.input('Email').classes('w-full mb-4 q-input-dark').props('outlined dark')
            ui.input('Mật khẩu', password=True, password_toggle_button=True).classes('w-full mb-6 q-input-dark').props('outlined dark')
            
            def do_login():
                ui.notify('Đăng nhập thành công!', type='positive')
                ui.navigate.to('/')
                
            ui.button('Đăng nhập', on_click=do_login).classes('w-full q-btn-search mb-4').props('unelevated no-caps')
            
            with ui.row().classes('w-full justify-center'):
                ui.label('Chưa có tài khoản?').style('opacity:0.7')
                ui.link('Đăng ký ngay', '#').style('color:#4facfe; margin-left:0.5rem; text-decoration:none;')
