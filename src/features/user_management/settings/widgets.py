from nicegui import app, ui
from src.common.units import _DEFAULTS, RefreshRegistry
from src.common.config import get_current_user
from src.database.user_store import (
    get_notifications, update_notifications,
    get_user_settings, update_user_settings,
)


def render_settings_content(compact: bool = False, parent_dialog_card=None):
    user = get_current_user()
    username = user['username'] if user else None

    # Đọc cài đặt: ưu tiên từ DB (nếu đã đăng nhập), fallback về storage
    if username:
        db_settings = get_user_settings(username)
        for key, val in db_settings.items():
            if key not in app.storage.user or app.storage.user.get(key) == _DEFAULTS.get(key):
                app.storage.user[key] = val

    current_units = {
        'unit_temp':       app.storage.user.get('unit_temp',       _DEFAULTS['unit_temp']),
        'unit_wind':       app.storage.user.get('unit_wind',       _DEFAULTS['unit_wind']),
        'unit_pressure':   app.storage.user.get('unit_pressure',   _DEFAULTS['unit_pressure']),
        'unit_visibility': app.storage.user.get('unit_visibility', _DEFAULTS['unit_visibility']),
        'theme':           app.storage.user.get('theme',           _DEFAULTS['theme']),
        'dynamic_bg':      app.storage.user.get('dynamic_bg',      True),
    }

    db_notifications = get_notifications(username) if username else {'rain': True, 'extreme': True, 'daily': False}

    gap = '0.75rem' if compact else '1.5rem'
    max_width = '100%' if compact else '820px'
    top_margin = '0rem' if compact else '2rem'

    card_style = (
        'background: transparent !important; border: none !important; '
        'box-shadow: none !important; padding: 0.5rem 0;'
    )
    section_icon_style = 'color:var(--accent-color);font-size:22px'

    with ui.element('div').style(
        f'display:flex;flex-direction:column;gap:{gap};margin-top:{top_margin};'
        f'max-width:{max_width};width:100%;'
    ):

        # ── KHỐI 1: ĐƠN VỊ ĐO LƯỜNG ──────────────────────────────────────────
        with ui.card().style(card_style).classes('w-full'):
            with ui.row().classes('items-center gap-2 mb-3'):
                ui.icon('straighten').style(section_icon_style)
                ui.label('Đơn vị đo lường').classes('text-h6').style('margin:0;font-weight:600;')

            with ui.row().classes('justify-between items-center w-full py-1'):
                ui.label('Nhiệt độ').style('font-weight:500;')
                temp_radio = ui.radio(
                    {'C': '°C (Celsius)', 'F': '°F (Fahrenheit)'},
                    value=current_units['unit_temp']
                ).props('inline')
                temp_radio.on_value_change(lambda e: current_units.update({'unit_temp': e.value}))

            ui.separator().style('opacity:0.1;margin:0.4rem 0')

            with ui.row().classes('justify-between items-center w-full py-1'):
                ui.label('Tốc độ gió').style('font-weight:500;')
                wind_radio = ui.radio(
                    {'km/h': 'km/h', 'm/s': 'm/s', 'mph': 'mph'},
                    value=current_units['unit_wind']
                ).props('inline')
                wind_radio.on_value_change(lambda e: current_units.update({'unit_wind': e.value}))

            ui.separator().style('opacity:0.1;margin:0.4rem 0')

            with ui.row().classes('justify-between items-center w-full py-1'):
                ui.label('Áp suất').style('font-weight:500;')
                pressure_radio = ui.radio(
                    {'hPa': 'hPa', 'mmHg': 'mmHg'},
                    value=current_units['unit_pressure']
                ).props('inline')
                pressure_radio.on_value_change(lambda e: current_units.update({'unit_pressure': e.value}))

            ui.separator().style('opacity:0.1;margin:0.4rem 0')

            with ui.row().classes('justify-between items-center w-full py-1'):
                ui.label('Tầm nhìn').style('font-weight:500;')
                visibility_radio = ui.radio(
                    {'km': 'km', 'miles': 'Miles'},
                    value=current_units['unit_visibility']
                ).props('inline')
                visibility_radio.on_value_change(lambda e: current_units.update({'unit_visibility': e.value}))



        # ── KHỐI 3: THÔNG BÁO & CẢNH BÁO ─────────────────────────────────────
        if username:
            with ui.card().style(card_style).classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('notifications_active').style(section_icon_style)
                    ui.label('Thông báo & Cảnh báo').classes('text-h6').style('margin:0;font-weight:600;')

                with ui.row().classes('justify-between items-center w-full py-1'):
                    with ui.column().classes('gap-0'):
                        ui.label('Cảnh báo mưa').style('font-weight:500;')
                        ui.label('Nhắc nhở mang ô khi trời sắp mưa').style('font-size:0.8rem;opacity:0.6;')
                    ui.switch(
                        value=db_notifications.get('rain', True),
                        on_change=lambda e: db_notifications.update({'rain': e.value})
                    ).props('color="blue"')

                ui.separator().style('opacity:0.1;margin:0.4rem 0')

                with ui.row().classes('justify-between items-center w-full py-1'):
                    with ui.column().classes('gap-0'):
                        ui.label('Thời tiết cực đoan').style('font-weight:500;')
                        ui.label('Cảnh báo nắng nóng gay gắt, rét đậm, gió lốc').style('font-size:0.8rem;opacity:0.6;')
                    ui.switch(
                        value=db_notifications.get('extreme', True),
                        on_change=lambda e: db_notifications.update({'extreme': e.value})
                    ).props('color="blue"')

                ui.separator().style('opacity:0.1;margin:0.4rem 0')

                with ui.row().classes('justify-between items-center w-full py-1'):
                    with ui.column().classes('gap-0'):
                        ui.label('Báo cáo hàng ngày').style('font-weight:500;')
                        ui.label('Tóm tắt nhanh tình hình thời tiết mỗi buổi sáng').style('font-size:0.8rem;opacity:0.6;')
                    ui.switch(
                        value=db_notifications.get('daily', False),
                        on_change=lambda e: db_notifications.update({'daily': e.value})
                    ).props('color="blue"')

        # ── NÚT ÁP DỤNG ───────────────────────────────────────────────────────────
        def save_all_settings():
            try:
                # Lưu vào storage (session)
                for key, val in current_units.items():
                    app.storage.user[key] = val

                # Lưu vào DB nếu đã đăng nhập
                if username:
                    update_user_settings(username, current_units)
                    update_notifications(username, db_notifications)

                ui.notify('Cài đặt đã được áp dụng thành công!', type='positive', position='top-right')
                RefreshRegistry.trigger(ui.context.client.id)

                # Khi ở trong dialog, cần đóng dialog trước khi reload
                if compact and parent_dialog_card is not None:
                    try:
                        parent_dialog_card.close()
                    except Exception:
                        pass
                    ui.timer(0.2, lambda: ui.navigate.reload(), once=True)
                else:
                    ui.navigate.reload()
            except Exception as e:
                ui.notify(f'Lỗi khi lưu cài đặt: {e}', type='negative', position='top-right')

        with ui.row().classes('w-full justify-end mt-2'):
            ui.button('Áp dụng thay đổi', icon='check', on_click=save_all_settings).props(
                'unelevated no-caps'
            ).style(
                'background: var(--accent-color);'
                'color:#ffffff; font-weight:600; border-radius:8px;'
                'padding: 0.6rem 1.5rem; font-size: 0.95rem;'
            )