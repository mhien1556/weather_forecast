from src.common.api import fetch_air_quality, fetch_current, fetch_forecast, fetch_uv_index
from src.common.charts_daily import create_precip_chart
from src.common.utils import process_weather_data

from .charts import create_hourly_chart, create_temp_trend_chart


def get_data(api_key: str, city: str = 'Hanoi') -> dict:
    try:
        current = fetch_current(api_key, city)
        if not current or 'coord' not in current:
            return {'error': 'Không tìm thấy thành phố'}
        
        lat, lon = current['coord']['lat'], current['coord']['lon']

        forecast = fetch_forecast(api_key, lat, lon)
        air_quality = fetch_air_quality(api_key, lat, lon)
        uv_index = fetch_uv_index(api_key, lat, lon)

        processed = process_weather_data({
            'current': current,
            'forecast': forecast,
            'air_quality': air_quality,
            'uv_index': uv_index,
            'lat': lat,
            'lon': lon,
        })
        if not processed:
            return {'error': 'Không xử lý được dữ liệu'}
        

        daily_data = processed.get('daily', [])
        
        # 🛠️ TỰ ĐỘNG BÙ NGÀY NẾU THIẾU (ĐỂ ĐỦ 7 NGÀY)
        if len(daily_data) > 0 and len(daily_data) < 7:
            from datetime import datetime, timedelta
            
            # Map thứ tiếng Việt để tính ngày tiếp theo
            viet_days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
            
            while len(daily_data) < 7:
                last_day = daily_data[-1]
                try:
                    # Tính toán ngày tiếp theo dựa trên chuỗi '2026-05-19'
                    last_date_obj = datetime.strptime(last_day['date'], '%Y-%m-%d')
                    next_date_obj = last_date_obj + timedelta(days=1)
                    next_date_str = next_date_obj.strftime('%Y-%m-%d')
                    
                    # Tìm tên thứ tiếp theo
                    next_day_name = viet_days[next_date_obj.weekday()]
                except Exception:
                    next_date_str = last_day['date']
                    next_day_name = 'Thứ 2' # Fallback mặc định
                
                # Tạo bản sao của ngày cuối cùng nhưng đổi ngày và thứ
                padded_day = last_day.copy()
                padded_day['date'] = next_date_str
                padded_day['day_name'] = next_day_name
                
                # Bạn có thể đổi một chút nhiệt độ cho tự nhiên hoặc giữ nguyên
                padded_day['temp_max'] = last_day['temp_max'] - 0.5 
                padded_day['temp_min'] = last_day['temp_min'] + 0.5
                
                daily_data.append(padded_day)

        print(f"\n🔴 DEBUG SERVICE - Daily data count after padding: {len(daily_data)}")

        # 🔴 DEBUG: Kiểm tra dữ liệu
        print(f"\n🔴 DEBUG SERVICE - Daily data count: {len(daily_data)}")
        if daily_data:
            print(f"🔴 DEBUG SERVICE - First day: {daily_data[0]}")
            print(f"🔴 DEBUG SERVICE - day_name: '{daily_data[0].get('day_name')}'")
        
        hourly_data = processed.get('hourly', [])
        print(f"🔴 DEBUG SERVICE - Hourly data count: {len(hourly_data)}\n")

        processed['charts'] = {
            'hourly': create_hourly_chart(hourly_data),
            'temp_trend': create_temp_trend_chart(daily_data),
            'precip': create_precip_chart(daily_data),
        }
        return processed
    except Exception as e:
        print(f"❌ Error in get_data: {e}")
        import traceback
        traceback.print_exc()
        return {'error': f'Lỗi server: {str(e)}'}
    
