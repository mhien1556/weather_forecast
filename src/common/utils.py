from datetime import datetime
import requests

WEEKDAY_VI = ['Chủ nhật', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7']

ICON_TO_MATERIAL = {
    'sun': 'wb_sunny',
    'cloud-sun': 'wb_cloudy',
    'cloud': 'cloud',
    'cloud-rain': 'grain',
    'cloud-lightning': 'thunderstorm',
    'cloud-snow': 'ac_unit',
    'cloud-fog': 'foggy',
}


def icon_to_lucide(icon_code):
    if not icon_code:
        return 'cloud'
    code = icon_code[:2]
    mapping = {
        '01': 'sun',
        '02': 'cloud-sun',
        '03': 'cloud',
        '04': 'cloud',
        '09': 'cloud-rain',
        '10': 'cloud-rain',
        '11': 'cloud-lightning',
        '13': 'cloud-snow',
        '50': 'cloud-fog',
    }
    return mapping.get(code, 'cloud')


def lucide_to_material(name):
    return ICON_TO_MATERIAL.get(name, 'cloud')


def aqi_info(aqi_val):
    if aqi_val <= 2:
        return {
            'label': 'Tốt',
            'desc': 'Không khí trong lành và tốt cho sức khỏe.',
            'color': '#4ade80',
        }
    if aqi_val == 3:
        return {
            'label': 'Khá',
            'desc': 'Chất lượng không khí ở mức chấp nhận được.',
            'color': '#facc15',
        }
    return {
        'label': 'Kém',
        'desc': 'Có thể gây ảnh hưởng đến sức khỏe.',
        'color': '#f87171',
    }


def format_time(ts):
    if not ts:
        return '--:--'
    return datetime.fromtimestamp(ts).strftime('%H:%M')


def parse_daily(forecast_list):
    if not forecast_list:
        return []

    by_date = {}
    for item in forecast_list:
        date = item['dt_txt'].split(' ')[0]
        if date not in by_date:
            by_date[date] = {
                'date': date,
                'temp_max': item['main']['temp_max'],
                'temp_min': item['main']['temp_min'],
                'humidity': [item['main']['humidity']],
                'wind': [item.get('wind', {}).get('speed', 0)],
                'pop': [round(item.get('pop', 0) * 100)],
                'descriptions': [item['weather'][0]['description']],
                'icon': item['weather'][0]['icon'],
            }
        else:
            d = by_date[date]
            d['temp_max'] = max(d['temp_max'], item['main']['temp_max'])
            d['temp_min'] = min(d['temp_min'], item['main']['temp_min'])
            d['humidity'].append(item['main']['humidity'])
            d['wind'].append(item.get('wind', {}).get('speed', 0))
            d['pop'].append(round(item.get('pop', 0) * 100))
            d['descriptions'].append(item['weather'][0]['description'])

    result = []
    for date, d in by_date.items():
        dt_obj = datetime.strptime(date, '%Y-%m-%d')
        py_weekday = dt_obj.weekday()
        vi_weekday = WEEKDAY_VI[(py_weekday + 1) % 7]
        result.append({
            'date': date,
            'day_name': vi_weekday,
            'temp_max': d['temp_max'],
            'temp_min': d['temp_min'],
            'humidity_avg': round(sum(d['humidity']) / len(d['humidity'])),
            'wind_avg': round(sum(d['wind']) / len(d['wind']), 1),
            'pop_max': max(d['pop']),
            'description': d['descriptions'][len(d['descriptions']) // 2],
            'icon': d['icon'],
            'lucide_icon': icon_to_lucide(d['icon']),
        })
    return result


def parse_hourly(forecast_list, limit=8):
    if not forecast_list:
        return []
    result = []
    for item in forecast_list[:limit]:
        result.append({
            'time': item['dt_txt'].split(' ')[1][:5],
            'temp': round(item['main']['temp']),
            'pop': round(item.get('pop', 0) * 100),
            'icon': item['weather'][0]['icon'],
            'lucide_icon': icon_to_lucide(item['weather'][0]['icon']),
        })
    return result


def get_current_date_vi():
    now = datetime.now()
    day = WEEKDAY_VI[(now.weekday() + 1) % 7]
    return f'{day}, {now.day} Tháng {now.month} • {now.strftime("%H:%M")}'


def process_weather_data(data):
    if not data or 'current' not in data:
        return None

    current = data['current']
    forecast = data.get('forecast', {})
    aqi = data.get('air_quality', {})

    processed_aqi = None
    if aqi and 'list' in aqi and len(aqi['list']) > 0:
        aqi_item = aqi['list'][0]
        val = aqi_item['main']['aqi']
        info = aqi_info(val)
        processed_aqi = {
            'val': val * 20,
            'label': info['label'],
            'desc': info['desc'],
            'color': info['color'],
            'pm25': round(aqi_item['components']['pm2_5'], 1),
            'co': round(aqi_item['components']['co'], 1),
            'pm25_pct': min((aqi_item['components']['pm2_5'] / 75) * 100, 100),
            'co_pct': min((aqi_item['components']['co'] / 15000) * 100, 100),
        }

    daily = parse_daily(forecast.get('list', []))
    hourly = parse_hourly(forecast.get('list', []), 8)

    stats = {}
    if daily:
        stats['avg_temp'] = round(
            sum((d['temp_max'] + d['temp_min']) / 2 for d in daily) / len(daily), 1
        )
        stats['total_rain'] = round(
            sum(item.get('rain', {}).get('3h', 0) for item in forecast.get('list', [])), 1
        )
        stats['sunny_days'] = len([d for d in daily if d['icon'].startswith('01')])

    icon = current['weather'][0]['icon']
    return {
        'city_name': f"{current['name']}, {current['sys']['country']}",
        'temp': round(current['main']['temp']),
        'desc': current['weather'][0]['description'],
        'feels_like': round(current['main']['feels_like']),
        'humidity': current['main']['humidity'],
        'wind': current.get('wind', {}).get('speed', 0),
        'pressure': current['main']['pressure'],
        'visibility': round(current.get('visibility', 0) / 1000, 1),
        'dew_point': round(current['main']['temp'] - (100 - current['main']['humidity']) / 5),
        'sunrise': format_time(current['sys'].get('sunrise')),
        'sunset': format_time(current['sys'].get('sunset')),
        'icon': icon,
        'lucide_icon': icon_to_lucide(icon),
        'uv_index': round(data.get('uv_index', 0), 1) if data.get('uv_index') is not None else None,
        'aqi': processed_aqi,
        'daily': daily,
        'hourly': hourly,
        'stats': stats,
        'date_str': get_current_date_vi(),
        'lat': data.get('lat'),
        'lon': data.get('lon'),
    }


def get_location_by_ip():
    try:
        response = requests.get('http://ip-api.com/json', timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data['city']
    except Exception as e:
        print(f'Lỗi khi định vị IP: {e}')
    return 'Ho Chi Minh City'


def is_raining(icon):
    return icon and icon[:2] in ('09', '10', '11')
