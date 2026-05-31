from nicegui import ui

from src.common.components import apply_theme, navbar
from src.common.config import API_KEY, get_city

from .constants import MAP_LAYERS
from .layer_config import LAYER_CONFIG
from .service import (
    BASE_TILE_URL,
    build_timeline,
    build_weather_tile_url,
    default_timeline_index,
    fetch_hourly_forecast,
    format_timeline_label,
    get_hourly_weather,
    resolve_snapshot,
)
from .widgets import create_location_panel

_TAG = 'div'
_WEATHER_OPACITY = 0.75


def register():
    @ui.page('/map')
    def map_page():
        apply_theme()
        city = get_city()
        weather = get_hourly_weather(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
        lat = weather.get('lat', 21.0285) if not weather.get('error') else 21.0285
        lon = weather.get('lon', 105.8542) if not weather.get('error') else 105.8542

        timeline = build_timeline(weather.get('hourly', []))
        timeline_labels = [format_timeline_label(ts) for ts in timeline]
        default_idx = default_timeline_index(timeline)

        layer_state = {'name': 'temp_new', 'time_idx': default_idx}
        chrome_state = {'visible': True}
        map_ref = {'leaflet': None, 'weather_layer': None, 'marker': None, 'ready': False}
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

        def refresh_weather_tiles(layer_key: str | None = None):
            if not API_KEY or not map_ref['ready'] or not map_ref['leaflet']:
                return
            url = weather_url(layer_key)
            wl = map_ref['weather_layer']
            if wl is not None:
                wl.run_method('setUrl', url)
                wl.run_method('setOpacity', _WEATHER_OPACITY)
                wl.run_method('redraw')
            else:
                map_ref['weather_layer'] = map_ref['leaflet'].tile_layer(
                    url_template=url,
                    options={'opacity': _WEATHER_OPACITY},
                )

        update_location = None

        def refresh_location_panel():
            if update_location is None:
                return
            ts = current_timestamp()
            snap = resolve_snapshot(sel_state['lat'], sel_state['lon'], ts, sel_state['hourly'])
            update_location(snap, sel_state['lat'], sel_state['lon'], layer_state['name'])

        def on_map_ready():
            map_ref['ready'] = True
            if API_KEY:
                refresh_weather_tiles('temp_new')
            refresh_location_panel()

        def update_legend(layer_key: str):
            cfg = LAYER_CONFIG[layer_key]
            legend_gradient.style(f"background: {cfg['gradient']}")
            legend_min.set_text(cfg['legend_min'])
            legend_max.set_text(cfg['legend_max'])

        def on_timeline_change(idx: int):
            idx = max(0, min(int(idx), len(timeline) - 1))
            layer_state['time_idx'] = idx
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

        cfg0 = LAYER_CONFIG['temp_new']
        menu_items: list = []

        def set_layer(layer_key, btn_el):
            layer_state['name'] = layer_key
            update_legend(layer_key)
            for item in menu_items:
                item.classes(remove='active')
            btn_el.classes(add='active')
            wl = map_ref['weather_layer']
            if wl is not None:
                wl.delete()
                map_ref['weather_layer'] = None
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

            with ui.element(_TAG).classes('page-content map-page-wrapper'):
                with ui.element(_TAG).classes('map-stage'):
                    m = ui.leaflet(
                        center=(lat, lon),
                        zoom=5,
                        options={'zoomControl': False},
                    ).classes('map-leaflet-fill')
                    map_ref['leaflet'] = m
                    m.on('init', on_map_ready)
                    m.on('map-click', on_map_click)
                    m.clear_layers()
                    m.tile_layer(
                        url_template=BASE_TILE_URL,
                        options={
                            'maxZoom': 19,
                            'subdomains': 'abcd',
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
                                            'map-menu-item' + (' active' if i == 0 else '')
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
                                    legend_gradient = ui.element(_TAG).classes('legend-gradient')
                                    legend_gradient.style(f"background: {cfg0['gradient']}")
                                    with ui.row().classes('legend-labels w-full justify-between'):
                                        legend_min = ui.label(cfg0['legend_min']).classes('legend-end-label')
                                        legend_max = ui.label(cfg0['legend_max']).classes('legend-end-label')
