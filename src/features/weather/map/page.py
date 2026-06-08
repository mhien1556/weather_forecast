from datetime import datetime

from nicegui import app, ui

from src.common.components import apply_theme, navbar
from src.common.config import API_KEY, get_city

from .constants import MAP_LAYERS
from .layer_config import LAYER_CONFIG
from .particles import PARTICLES_SCRIPT
from .service import (
    BASE_TILE_URL,
    DARK_BASE_TILE_URL,
    LABELS_TILE_URL,
    build_timeline,
    build_weather_tile_url,
    default_timeline_index,
    fetch_hourly_forecast,
    format_timeline_label,
    get_hourly_weather,
    is_timestamp_in_owm_range,
    resolve_snapshot,
)
from .widgets import create_location_panel

_TAG = 'div'
_DEFAULT_OPACITY = 0.75
_LAYER_CLASS_PREFIX = 'map-layer-'


def register():
    @ui.page('/map')
    def map_page():
        apply_theme()
        ui.add_body_html(f'<script>{PARTICLES_SCRIPT}</script>')

        ui.add_head_html('''
        <style>
            .map-hidden { display: none !important; }
            .timeline-time-label.out-of-range {
                color: #ff7043 !important;
            }
            .timeline-time-label.out-of-range::after {
                content: ' ⚠';
            }
        </style>
        ''')

        city = get_city()
        weather = get_hourly_weather(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
        lat = weather.get('lat', 21.0285) if not weather.get('error') else 21.0285
        lon = weather.get('lon', 105.8542) if not weather.get('error') else 105.8542

        timeline = build_timeline(weather.get('hourly', []), API_KEY or '')
        timeline_labels = [format_timeline_label(ts) for ts in timeline]
        default_idx = default_timeline_index(timeline)

        active_layer = app.storage.user.get('active_map_layer', 'temp_new')
        layer_state = {'name': active_layer, 'time_idx': default_idx}
        chrome_state = {'visible': True}
        map_ref = {
            'leaflet': None,
            'weather_layer': None,
            'base_layer': None,
            'labels_layer': None,
            'marker': None,
            'ready': False,
        }
        sel_state = {
            'lat': lat,
            'lon': lon,
            'hourly': weather.get('hourly', []) if not weather.get('error') else [],
        }

        def current_timestamp() -> int:
            return timeline[layer_state['time_idx']]

        def weather_url(layer_key: str | None = None) -> str:
            key = layer_key or layer_state['name']
            if not API_KEY:
                return ''
            return build_weather_tile_url(key, API_KEY, current_timestamp())

        def tile_opacity(layer_key: str | None = None) -> float:
            key = layer_key or layer_state['name']
            return LAYER_CONFIG.get(key, {}).get('tile_opacity', _DEFAULT_OPACITY)

        def apply_layer_stage_class(layer_key: str):
            for key in LAYER_CONFIG:
                map_stage.classes(remove=f'{_LAYER_CLASS_PREFIX}{key.replace("_new", "")}')
            short = layer_key.replace('_new', '')
            map_stage.classes(add=f'{_LAYER_CLASS_PREFIX}{short}')

        def refresh_weather_tiles(layer_key: str | None = None):
            if not API_KEY:
                return
            key = layer_key or layer_state['name']
            url = weather_url(key)
            opacity = tile_opacity(key)
            wl = map_ref['weather_layer']
            if wl is None:
                return
            if map_ref['ready']:
                wl.run_method('setUrl', url)
                wl.run_method('setOpacity', opacity)
                wl.run_method('redraw')

        update_location = None

        def refresh_location_panel():
            if update_location is None:
                return
            ts = current_timestamp()
            snap = resolve_snapshot(sel_state['lat'], sel_state['lon'], ts, sel_state['hourly'])
            update_location(snap, sel_state['lat'], sel_state['lon'], layer_state['name'])

        def update_legend(layer_key: str):
            cfg = LAYER_CONFIG[layer_key]
            
            from src.common.units import get_units, convert_temp, convert_wind_from_ms, convert_pressure
            u = get_units()
            
            min_str = cfg['legend_min']
            max_str = cfg['legend_max']
            field = cfg.get('field', '')
            
            if field == 'temp':
                min_val = convert_temp(-70, u['unit_temp'])
                max_val = convert_temp(50, u['unit_temp'])
                unit = '°F' if u['unit_temp'] == 'F' else '°C'
                min_str = f"{min_val}{unit}"
                max_str = f"{max_val}{unit}"
            elif field == 'wind_speed':
                min_val = convert_wind_from_ms(0, u['unit_wind'])
                max_val = convert_wind_from_ms(79, u['unit_wind'])
                min_str = f"{min_val} {u['unit_wind']}"
                max_str = f"{max_val} {u['unit_wind']}"
            elif field == 'pressure':
                min_val = convert_pressure(950, u['unit_pressure'])
                max_val = convert_pressure(1050, u['unit_pressure'])
                min_str = f"{min_val} {u['unit_pressure']}"
                max_str = f"{max_val} {u['unit_pressure']}"

            legend_title.set_text(f"{cfg['label']}   {min_str} … {max_str}")
            legend_gradient.style(f"background: {cfg['gradient']}")
            legend_min.set_text(min_str)
            legend_max.set_text(max_str)

        def on_map_ready():
            map_ref['ready'] = True
            apply_layer_stage_class(layer_state['name'])
            refresh_weather_tiles(layer_state['name'])
            refresh_location_panel()
            
            # CHỐT HẠ FIX: Ép thanh màu cập nhật đơn vị chuẩn ngay khi load/reload bản đồ xong!
            update_legend(layer_state['name'])
            
            ui.run_javascript('''
                window.weatherMapParticles?.init();
                const el = document.querySelector('.map-stage .leaflet-container');
                if (el) {
                    for (const k of Object.keys(el)) {
                        const v = el[k];
                        if (v && v.latLngToContainerPoint && v.getBounds) {
                            window.__niceguiLeafletMap = v;
                            break;
                        }
                    }
                }
                window.weatherMapParticles?.onMapMove();
            ''')

        def update_time_label_style(idx: int):
            ts = timeline[max(0, min(idx, len(timeline) - 1))]
            if is_timestamp_in_owm_range(ts):
                time_label.classes(remove='out-of-range')
            else:
                time_label.classes(add='out-of-range')

        def on_timeline_change(idx: int):
            idx = max(0, min(int(idx), len(timeline) - 1))
            layer_state['time_idx'] = idx
            update_time_label_style(idx)
            refresh_weather_tiles()
            refresh_location_panel()

        def move_marker(new_lat: float, new_lon: float):
            mk = map_ref['marker']
            if mk is not None:
                mk.run_method('setLatLng', [new_lat, new_lon])

        def select_location(new_lat: float, new_lon: float):
            sel_state['lat'] = new_lat
            sel_state['lon'] = new_lon
            if API_KEY:
                sel_state['hourly'] = fetch_hourly_forecast(API_KEY, new_lat, new_lon)
            move_marker(new_lat, new_lon)
            refresh_location_panel()

        def on_map_click(e):
            latlng = e.args.get('latlng')
            if not latlng:
                return
            if isinstance(latlng, dict):
                click_lat, click_lon = latlng.get('lat'), latlng.get('lng')
            else:
                click_lat, click_lon = latlng[0], latlng[1]
            if click_lat is not None and click_lon is not None:
                select_location(float(click_lat), float(click_lon))

        cfg0 = LAYER_CONFIG[layer_state['name']]
        menu_items: list = []

        def set_layer(layer_key, btn_el):
            app.storage.user['active_map_layer'] = layer_key
            layer_state['name'] = layer_key
            
            update_legend(layer_key)
            apply_layer_stage_class(layer_key)
            for item in menu_items:
                item.classes(remove='active')
            btn_el.classes(add='active')
            refresh_weather_tiles(layer_key)
            refresh_location_panel()

        def toggle_chrome():
            chrome_state['visible'] = not chrome_state['visible']
            if chrome_state['visible']:
                map_chrome_panels.classes(remove='map-chrome-panels--hidden')
                eye_btn.props('icon=visibility')
            else:
                map_chrome_panels.classes(add='map-chrome-panels--hidden')
                eye_btn.props('icon=visibility_off')

        with ui.element(_TAG).classes('app-container map-app'):
            navbar('/map')

            if not API_KEY:
                with ui.row().classes('w-full justify-center').style(
                    'position:relative;z-index:2000;background:#b71c1c;color:#fff;padding:0.5rem 1rem;font-size:0.9rem'
                ):
                    ui.label(
                        'Thiếu OPENWEATHER_API_KEY trong file .env — bản đồ màu không hiển thị. '
                        'Thêm key rồi restart server.'
                    )

            with ui.element(_TAG).classes('page-content map-page-wrapper'):
                map_stage = ui.element(_TAG).classes(f"map-stage map-layer-{layer_state['name'].replace('_new', '')}")
                with map_stage:
                    m = ui.leaflet(
                        center=(lat, lon),
                        zoom=5,
                        options={'zoomControl': False},
                    ).classes('map-leaflet-fill')
                    map_ref['leaflet'] = m
                    m.on('init', on_map_ready)
                    m.on('map-click', on_map_click)
                    m.on('map-moveend', lambda _: ui.run_javascript('window.weatherMapParticles?.onMapMove()'))
                    m.on('map-zoomend', lambda _: ui.run_javascript('window.weatherMapParticles?.onMapMove()'))
                    m.clear_layers()
                    _tile_opts = {'maxZoom': 19, 'subdomains': 'abcd'}
                    if API_KEY:
                        map_ref['base_layer'] = m.tile_layer(
                            url_template=DARK_BASE_TILE_URL,
                            options={
                                **_tile_opts,
                                'attribution': '&copy; OpenStreetMap &copy; CARTO',
                            },
                        )
                        map_ref['weather_layer'] = m.tile_layer(
                            url_template=build_weather_tile_url(
                                layer_state['name'], API_KEY, timeline[default_idx]
                            ),
                            options={'opacity': 1.0, 'maxZoom': 19},
                        )
                        map_ref['labels_layer'] = m.tile_layer(
                            url_template=LABELS_TILE_URL,
                            options={**_tile_opts, 'opacity': 1.0},
                        )
                    else:
                        map_ref['base_layer'] = m.tile_layer(
                            url_template=BASE_TILE_URL,
                            options={
                                **_tile_opts,
                                'attribution': '&copy; OpenStreetMap &copy; CARTO',
                            },
                        )
                    map_ref['marker'] = m.marker(latlng=(lat, lon))

                    with ui.element(_TAG).classes('map-ui-layer'):
                        with ui.element(_TAG).classes('map-float map-view-float'):
                            eye_btn = ui.button(icon='visibility', on_click=toggle_chrome).classes(
                                'round-icon-btn'
                            ).props('flat round')

                        map_chrome_panels = ui.element(_TAG).classes('map-chrome-panels')
                        with map_chrome_panels:
                            with ui.element(_TAG).classes('map-float map-sidebar-float'):
                                with ui.element(_TAG).classes('map-menu-card'):
                                    for i, (key, label, icon, _range) in enumerate(MAP_LAYERS):
                                        item = ui.element(_TAG).classes(
                                            'map-menu-item' + (' active' if key == layer_state['name'] else '')
                                        )
                                        menu_items.append(item)
                                        with item:
                                            with ui.row().classes('items-center gap-3 no-wrap'):
                                                ui.icon(icon)
                                                ui.label(label)
                                        item.on('click', lambda k=key, el=item: set_layer(k, el))

                            with ui.element(_TAG).classes('map-float map-location-float'):
                                update_location = create_location_panel()

                            with ui.element(_TAG).classes('map-float map-timeline-float'):
                                with ui.element(_TAG).classes('timeline-card'):
                                    def step_time(delta: int):
                                        new_idx = max(0, min(int(slider.value) + delta, len(timeline) - 1))
                                        slider.set_value(new_idx)
                                        on_timeline_change(new_idx)

                                    ui.button(icon='chevron_left', on_click=lambda: step_time(-1)).props(
                                        'flat round dense'
                                    ).classes('timeline-nav-btn')
                                    slider = ui.slider(
                                        min=0,
                                        max=max(len(timeline) - 1, 0),
                                        value=default_idx,
                                        step=1,
                                    ).classes('map-timeline-slider').style('flex:1;min-width:120px').props(
                                        'snap color=orange'
                                    )
                                    ui.button(icon='chevron_right', on_click=lambda: step_time(1)).props(
                                        'flat round dense'
                                    ).classes('timeline-nav-btn')
                                    time_label = ui.label(timeline_labels[default_idx]).classes(
                                        'timeline-time-label'
                                    )
                                    time_label.bind_text_from(
                                        slider,
                                        'value',
                                        backward=lambda i: timeline_labels[
                                            max(0, min(int(i), len(timeline_labels) - 1))
                                        ],
                                    )

                                    def on_slider_event(e):
                                        on_timeline_change(e.args)

                                    slider.on('update:model-value', on_slider_event, throttle=0)

                            with ui.element(_TAG).classes('map-float map-legend-float'):
                                with ui.element(_TAG).classes('legend-card'):
                                    legend_title = ui.label(cfg0['label']).classes('legend-title')
                                    legend_gradient = ui.element(_TAG).classes('legend-gradient')
                                    legend_gradient.style(f"background: {cfg0['gradient']}")
                                    with ui.row().classes('legend-labels w-full justify-between'):
                                        legend_min = ui.label(cfg0['legend_min']).classes('legend-end-label')
                                        legend_max = ui.label(cfg0['legend_max']).classes('legend-end-label')

        def draw_content():
            apply_theme()
            refresh_location_panel()
            update_legend(layer_state['name'])

        from src.common.units import RefreshRegistry
        client_id = ui.context.client.id
        RefreshRegistry.register(client_id, draw_content)
        ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))