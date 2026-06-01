# Cấu hình lớp bản đồ — gradient khớp thang màu tile OpenWeather

LAYER_CONFIG = {

    'temp_new': {

        'label': 'Nhiệt độ',

        'label_en': 'Temperature',

        'icon': 'thermostat',

        'unit': '°C',

        'gradient': (

            'linear-gradient(to right, '

            '#4a148c, #1565c0, #00838f, #43a047, #c0ca33, #ffb300, #f4511e, #b71c1c)'

        ),

        'legend_min': '-70°C',

        'legend_max': '50°C',

        'field': 'temp',

        'tile_opacity': 1.0,

    },

    'pressure_new': {

        'label': 'Áp suất',

        'label_en': 'Pressure',

        'icon': 'speed',

        'unit': 'hPa',

        'gradient': (

            'linear-gradient(to right, '

            '#0d1b4d, #1565c0, #26c6da, #66bb6a, #ffee58, #ff7043, #c62828)'

        ),

        'legend_min': '950 hPa',

        'legend_max': '1050 hPa',

        'field': 'pressure',

        'tile_opacity': 1.0,

    },

    'wind_new': {

        'label': 'Tốc độ gió',

        'label_en': 'Wind speed',

        'icon': 'air',

        'unit': 'm/s',

        'gradient': (

            'linear-gradient(to right, '

            'rgba(255,255,255,0), #eecece, #b364bc, #744c8e, #3f2173)'

        ),

        'legend_min': '0 m/s',

        'legend_max': '79 m/s',

        'field': 'wind_speed',

        'tile_opacity': 1.0,

    },

    'precipitation_new': {

        'label': 'Lượng mưa',

        'label_en': 'Precipitation',

        'icon': 'grain',

        'unit': 'mm/h',

        'gradient': (

            'linear-gradient(to right, '

            '#e0f7fa, #26c6da, #66bb6a, #ffee58, #ffa726, #ef5350, #ab47bc, #6a1b9a)'

        ),

        'legend_min': '0 mm/h',

        'legend_max': '40 mm/h',

        'field': 'rain',

        'tile_opacity': 1.0,

    },

    'clouds_new': {

        'label': 'Mây',

        'label_en': 'Clouds',

        'icon': 'cloud',

        'unit': '%',

        'gradient': (

            'linear-gradient(to right, '

            'rgba(255,255,255,0.0), rgba(255,255,255,0.35), #ffffff, #cfd8dc, #90a4ae, #546e7a)'

        ),

        'legend_min': '0%',

        'legend_max': '100%',

        'field': 'clouds',

        'tile_opacity': 1.0,

    },

}

