from nicegui import app, ui

from src.common.config import get_city, set_city
from src.common.units import _DEFAULTS, RefreshRegistry


def _save(key: str, value):
    """Lưu ngay vào storage và kích hoạt làm mới UI tức thì."""
    if app.storage.user.get(key) != value:
        app.storage.user[key] = value
        RefreshRegistry.trigger(ui.context.client.id)


def render_settings_content():
    # Đọc giá trị hiện tại
    def val(key):
        return app.storage.user.get(key, _DEFAULTS[key])

    with ui.element('div').style(
        'display:flex;flex-direction:column;gap:2rem;margin-top:2rem;max-width:820px'
    ):
        # ── 1. Đơn vị đo lường ─────────────────────────────────────────────
        with ui.card().classes('card w-full'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('straighten').style('color:#4facfe;font-size:22px')
                ui.label('Đơn vị đo lường').classes('text-h6').style('margin:0')

            # Nhiệt độ
            with ui.row().classes('items-center gap-4 mb-2'):
                ui.label('🌡 Nhiệt độ:').style('min-width:130px;font-weight:500')
                temp_radio = ui.radio(
                    {'C': '°C (Celsius)', 'F': '°F (Fahrenheit)'},
                    value=val('unit_temp'),
                ).props('inline')
                temp_radio.on_value_change(lambda e: _save('unit_temp', e.value))

            ui.separator().style('margin:0.5rem 0')

            # Tốc độ gió
            with ui.row().classes('items-center gap-4 mb-2'):
                ui.label('💨 Tốc độ gió:').style('min-width:130px;font-weight:500')
                wind_radio = ui.radio(
                    {'km/h': 'km/h', 'm/s': 'm/s', 'mph': 'mph (dặm/giờ)'},
                    value=val('unit_wind'),
                ).props('inline')
                wind_radio.on_value_change(lambda e: _save('unit_wind', e.value))

            ui.separator().style('margin:0.5rem 0')

            # Áp suất
            with ui.row().classes('items-center gap-4 mb-2'):
                ui.label('📊 Áp suất:').style('min-width:130px;font-weight:500')
                pressure_radio = ui.radio(
                    {'hPa': 'hPa', 'mmHg': 'mmHg (milimét thuỷ ngân)'},
                    value=val('unit_pressure'),
                ).props('inline')
                pressure_radio.on_value_change(lambda e: _save('unit_pressure', e.value))

            ui.separator().style('margin:0.5rem 0')

            # Tầm nhìn
            with ui.row().classes('items-center gap-4'):
                ui.label('👁 Tầm nhìn:').style('min-width:130px;font-weight:500')
                visibility_radio = ui.radio(
                    {'km': 'km', 'miles': 'Miles'},
                    value=val('unit_visibility'),
                ).props('inline')
                visibility_radio.on_value_change(lambda e: _save('unit_visibility', e.value))

            ui.label('✓ Thay đổi áp dụng ngay khi reload trang kế tiếp.').style(
                'font-size:0.78rem;color:rgba(255,255,255,0.4);margin-top:0.75rem'
            )

        # ── 2. Giao diện / Theme ────────────────────────────────────────────
        with ui.card().classes('card w-full'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('palette').style('color:#4facfe;font-size:22px')
                ui.label('Giao diện (Theme)').classes('text-h6').style('margin:0')

            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('🎨 Chủ đề:').style('min-width:130px;font-weight:500')
                theme_radio = ui.radio(
                    {'dark': '🌙 Dark (Tối)', 'light': '☀️ Light (Sáng)'},
                    value=val('theme'),
                ).props('inline')

                def on_theme_change(e):
                    _save('theme', e.value)
                    ui.dark_mode(e.value == 'dark')
                    ui.notify(
                        'Đã đổi giao diện — reload trang để thấy đầy đủ hiệu ứng.',
                        type='info', position='top-right', timeout=3000,
                    )

                theme_radio.on_value_change(on_theme_change)

            with ui.row().classes('items-center gap-4'):
                ui.switch(
                    'Ảnh nền động (Dynamic Background)',
                    value=app.storage.user.get('dynamic_bg', True),
                    on_change=lambda e: _save('dynamic_bg', e.value),
                ).props('color="blue"')

        # ── 3. Thành phố mặc định ───────────────────────────────────────────
        with ui.card().classes('card w-full'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('place').style('color:#4facfe;font-size:22px')
                ui.label('Thành phố mặc định').classes('text-h6').style('margin:0')

            current_city = get_city()
            city_label = ui.label(f'Thành phố hiện tại: {current_city}').style(
                'font-size:0.9rem;color:rgba(255,255,255,0.55);margin-bottom:0.75rem'
            )

            with ui.row().classes('items-center gap-3 w-full').style('flex-wrap:nowrap'):
                city_input = ui.input(
                    placeholder='Ví dụ: Da Nang, Hanoi, Tokyo...',
                    value=current_city,
                ).props('outlined dense dark').style(
                    'flex:1;min-width:200px;background:rgba(255,255,255,0.05);border-radius:8px'
                )

                def save_city():
                    new_city = city_input.value.strip()
                    if not new_city:
                        ui.notify('Vui lòng nhập tên thành phố!', type='warning')
                        return
                    set_city(new_city)
                    city_label.set_text(f'Thành phố hiện tại: {new_city}')
                    ui.notify(
                        f'✅ Đã đặt "{new_city}" làm thành phố mặc định!',
                        type='positive', position='top-right', timeout=2000,
                    )
                    RefreshRegistry.trigger(ui.context.client.id)


                ui.button('Đặt làm mặc định', icon='pin_drop', on_click=save_city).props(
                    'unelevated no-caps'
                ).style('background:#4facfe;color:#0a0c10;font-weight:600;border-radius:8px;white-space:nowrap')

            ui.label('💡 Trang chủ và Dự báo sẽ tải thành phố này khi bạn mở lại.').style(
                'font-size:0.78rem;color:rgba(255,255,255,0.4);margin-top:0.75rem'
            )

        # ── 4. Thông báo ────────────────────────────────────────────────────
        with ui.card().classes('card w-full'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('notifications').style('color:#4facfe;font-size:22px')
                ui.label('Thông báo').classes('text-h6').style('margin:0')

            ui.switch(
                'Cảnh báo thời tiết nguy hiểm',
                value=app.storage.user.get('notif_alert', True),
                on_change=lambda e: _save('notif_alert', e.value),
            ).props('color="red"')

            ui.switch(
                'Bản tin dự báo buổi sáng',
                value=app.storage.user.get('notif_morning', False),
                on_change=lambda e: _save('notif_morning', e.value),
            ).props('color="blue"').style('margin-top:0.5rem')
