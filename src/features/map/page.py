from nicegui import ui

from src.common.components import apply_theme, hero_background, navbar
from src.common.config import API_KEY, get_city

from .constants import MAP_LAYERS
from .service import get_data

_TAG = 'div'


def register():
    @ui.page('/map')
    def map_page():
        apply_theme()
        city = get_city()
        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
        lat = weather.get('lat', 21.0285) if not weather.get('error') else 21.0285
        lon = weather.get('lon', 105.8542) if not weather.get('error') else 105.8542

        layer_state = {'name': 'temp_new', 'label': 'Nhiệt độ', 'range': '-70°C ... 50°C'}
        map_ref = {'leaflet': None, 'weather_layer': None}

        with ui.element(_TAG).classes('app-container'):
            hero_background(weather if not weather.get('error') else None)
            navbar('/map')

            with ui.element(_TAG).classes('page-content map-page-wrapper'):
                with ui.element(_TAG).classes('map-container-full'):
                    m = ui.leaflet(center=(lat, lon), zoom=5).classes('map-leaflet w-full h-full')
                    map_ref['leaflet'] = m
                    m.tile_layer(
                        url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                        options={'maxZoom': 18},
                    )
                    if API_KEY:
                        wl = m.tile_layer(
                            url_template=f'https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
                            options={'opacity': 0.6},
                        )
                        map_ref['weather_layer'] = wl
                    m.marker(latlng=(lat, lon))

                    legend_label = ui.label(layer_state['label'])
                    legend_range = ui.label(layer_state['range'])

                    def set_layer(layer_key, label, range_text, btn_el):
                        layer_state['name'] = layer_key
                        layer_state['label'] = label
                        layer_state['range'] = range_text
                        legend_label.set_text(label)
                        legend_range.set_text(range_text)
                        for item in menu_items:
                            item.classes(remove='active')
                        btn_el.classes(add='active')
                        if API_KEY and map_ref['leaflet']:
                            if map_ref['weather_layer']:
                                map_ref['weather_layer'].delete()
                            map_ref['weather_layer'] = map_ref['leaflet'].tile_layer(
                                url_template=f'https://tile.openweathermap.org/map/{layer_key}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
                                options={'opacity': 0.6},
                            )

                    with ui.element(_TAG).classes('map-overlay map-search-float'):
                        ui.button(icon='search').classes('round-icon-btn').props('flat round')

                    with ui.element(_TAG).classes('map-overlay map-view-float'):
                        ui.button(icon='visibility').classes('round-icon-btn').props('flat round')

                    menu_items = []
                    with ui.element(_TAG).classes('map-overlay map-sidebar-float'):
                        with ui.element(_TAG).classes('map-menu-card'):
                            for i, (key, label, icon, range_text) in enumerate(MAP_LAYERS):
                                item = ui.element(_TAG).classes('map-menu-item' + (' active' if i == 0 else ''))
                                menu_items.append(item)
                                with item:
                                    with ui.row().classes('items-center gap-3 no-wrap'):
                                        ui.icon(icon)
                                        ui.label(label)
                                item.on('click', lambda k=key, l=label, r=range_text, el=item: set_layer(k, l, r, el))

                            ui.element(_TAG).classes('map-menu-divider')
                            with ui.element(_TAG).classes('map-menu-footer'):
                                ui.label('Hiệu ứng gió')
                                ui.switch(value=True)

                    with ui.element(_TAG).classes('map-overlay map-timeline-float'):
                        with ui.element(_TAG).classes('timeline-card w-full'):
                            ui.button(icon='play_arrow').props('flat round').classes('text-white')
                            with ui.column().classes('flex-grow gap-2'):
                                ui.slider(min=0, max=100, value=50).classes('w-full')
                                ui.label('2026-05-16 13:00').style('font-size:0.8rem;opacity:0.6;font-family:monospace')

                    with ui.element(_TAG).classes('map-overlay map-legend-float'):
                        with ui.element(_TAG).classes('legend-card w-full'):
                            with ui.row().classes('legend-header w-full justify-between'):
                                legend_label
                                legend_range
                            ui.element(_TAG).classes('legend-gradient')
                            with ui.row().classes('legend-labels w-full justify-between'):
                                ui.label('Thấp').style('font-size:0.7rem;opacity:0.4')
                                ui.label('Trung bình').style('font-size:0.7rem;opacity:0.4')
                                ui.label('Cao').style('font-size:0.7rem;opacity:0.4')
