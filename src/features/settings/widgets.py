from nicegui import ui

def render_settings_content():
    with ui.element('div').classes('settings-grid').style('display: flex; flex-direction: column; gap: 2rem; margin-top: 2rem; max-width: 800px;'):
        with ui.card().classes('card w-full'):
            ui.label('Giao diện').classes('text-h6 mb-4')
            ui.switch('Chế độ Tối (Dark Mode)', value=True).props('color="blue"')
            ui.switch('Ảnh nền động (Dynamic Background)', value=True).props('color="blue"')
            
        with ui.card().classes('card w-full'):
            ui.label('Đơn vị đo lường').classes('text-h6 mb-4')
            with ui.row().classes('items-center gap-4'):
                ui.label('Nhiệt độ:')
                ui.radio(['C (Celsius)', 'F (Fahrenheit)'], value='C (Celsius)').props('inline')
            with ui.row().classes('items-center gap-4 mt-2'):
                ui.label('Tốc độ gió:')
                ui.radio(['km/h', 'm/s', 'mph'], value='km/h').props('inline')
                
        with ui.card().classes('card w-full'):
            ui.label('Thông báo').classes('text-h6 mb-4')
            ui.switch('Cảnh báo thời tiết nguy hiểm', value=True).props('color="red"')
            ui.switch('Bản tin dự báo buổi sáng', value=False).props('color="blue"')
            
        ui.button('Lưu cài đặt', on_click=lambda: ui.notify('Đã lưu cài đặt thành công!', type='positive')).classes('w-full mt-4 q-btn-search').props('unelevated no-caps')
