# WeatherNow - Nền tảng Dự báo Thời tiết Thông minh 🌤️

WeatherNow là một nền tảng dự báo thời tiết trực quan, hiện đại được thiết kế theo phong cách **Cinematic Glassmorphism**. Toàn bộ dự án được xây dựng 100% bằng **Python** thông qua thư viện **NiceGUI** kết hợp với **Plotly** để vẽ biểu đồ và **Leaflet** cho bản đồ.

---

## 🌟 Các tính năng nổi bật

- **Trang chủ (Home):** Tổng quan thời tiết tại khu vực được chọn, xu hướng nhiệt độ trong ngày, chất lượng không khí (AQI).
- **Dự báo (Forecast):** Cung cấp thông tin dự báo chi tiết cho 7 ngày tiếp theo với độ chính xác cao.
- **Bản đồ (Map):** Bản đồ vệ tinh tương tác nhiều lớp dữ liệu như nhiệt độ, mây, lượng mưa, áp suất (thời gian thực).
- **Phân tích chuyên sâu (Analysis):** Biểu đồ so sánh nhiệt độ, lượng mưa, độ ẩm và các chỉ số môi trường khác qua các ngày.
- **Tùy chỉnh (Settings):** Cài đặt cá nhân hóa về giao diện và đơn vị đo lường.
- **Tài khoản (Login):** Giao diện đăng nhập và đăng ký trực quan.

---

## 📂 Kiến trúc Dự án (Feature-based Architecture)

Dự án áp dụng kiến trúc Module theo tính năng, phân tách rõ ràng từng khối chức năng để đảm bảo khả năng bảo trì và nâng cấp (Scale) tốt nhất.

```text
WeatherNow/
├── server.py                 # File khởi chạy ứng dụng
├── requirements.txt          # Các thư viện phụ thuộc
├── .env                      # File cấu hình (chứa OPENWEATHER_API_KEY)
└── src/
    ├── app.py                # Khởi tạo và cấu hình ứng dụng NiceGUI
    ├── common/               # Các module và components dùng chung
    │   ├── config.py         # Quản lý API key, trạng thái toàn cục (thành phố...)
    │   ├── api.py            # Gọi và giao tiếp với OpenWeatherMap API
    │   ├── utils.py          # Hàm tiện ích xử lý dữ liệu thời tiết
    │   ├── theme.py          # Quản lý CSS, bộ màu (Dark mode)
    │   ├── components.py     # Components dùng chung (Navbar, Footer, Search)
    │   ├── charts_base.py    # Cấu hình chung cho biểu đồ Plotly
    │   └── charts_daily.py   # Các biểu đồ dùng chung
    └── features/             # Chứa toàn bộ các trang (mỗi tính năng = 1 thư mục độc lập)
        ├── home/             # Trang chủ (/)
        ├── forecast/         # Trang dự báo chi tiết (/forecast)
        ├── map/              # Trang bản đồ tương tác (/map)
        ├── analysis/         # Trang biểu đồ phân tích (/analysis)
        ├── settings/         # Trang cấu hình hệ thống (/settings)
        └── login/            # Trang đăng nhập và đăng ký (/login)
```
*(Mỗi thư mục trong `features/` đều chứa `page.py` để khai báo route, `service.py` xử lý logic lấy dữ liệu riêng, `widgets.py`/`ui.py` để chứa giao diện đặc thù và `charts.py` cho biểu đồ tùy chỉnh)*

---

## 🚀 Hướng dẫn cài đặt & Chạy ứng dụng

### 1. Cài đặt thư viện

Bạn cần đảm bảo hệ thống đã cài đặt Python 3.10 trở lên, sau đó cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 2. Thiết lập API Key

Tạo một file `.env` ở thư mục gốc (ngang hàng với `server.py`) và thêm mã API từ OpenWeatherMap của bạn:

```env
OPENWEATHER_API_KEY=your_api_key_here
FLASK_SECRET_KEY=weathernow-dev-secret
```

### 3. Khởi động ứng dụng

Chạy file `server.py` bằng Python:

```bash
python server.py
```

Truy cập ứng dụng tại trình duyệt: **[http://localhost:5000](http://localhost:5000)**

---

## 🛠 Công nghệ sử dụng

| Thành phần        | Công nghệ / Thư viện                     |
|-------------------|----------------------------------------|
| **Core & Backend**| Python                                 |
| **Frontend UI**   | NiceGUI (Vue.js, Tailwind CSS)         |
| **Biểu đồ**       | Plotly (Python Plotly Graph Objects)   |
| **Bản đồ**        | Leaflet (NiceGUI UI Leaflet)           |
| **Dữ liệu API**   | OpenWeatherMap (Current, Forecast, AQI)|

---

*© 2026 WeatherNow — Phát triển và Thiết kế bởi Minh Hiển.*


---
## 🔍 Bảng So Sánh Chi Tiết Mã Nguồn (Line-by-Line Code Changes)
Dưới đây là chi tiết so sánh các dòng mã nguồn đã thay đổi giữa bản nâng cấp `weather_forecast` (A) và bản cơ bản `weather_forecast-WeatherNow` (B).

### 📂 1. Các tệp tin thêm mới hoặc bị loại bỏ
- **Các tệp chỉ có trong bản Nâng cấp `weather_forecast` (Được thêm mới để phục vụ cấu hình đơn vị & bản đồ hạt gió nâng cao):**
  * `[NEW]` [src\common\units.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/common/units.py)
  * `[NEW]` [src\features\map\layer_config.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/map/layer_config.py)
  * `[NEW]` [src\features\map\particles.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/map/particles.py)
  * `[NEW]` [src\features\map\widgets.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/map/widgets.py)

- **Các tệp chỉ có trong bản Cơ bản `weather_forecast-WeatherNow`:**
  * (Không có)

---
### 🛠 2. Chi tiết các dòng code được sửa đổi từng file
> **Chú giải ký hiệu:**
> - Dòng bắt đầu bằng `-` (Màu đỏ/Trừ): Dòng code trong bản Nâng cấp `weather_forecast` (A)
> - Dòng bắt đầu bằng `+` (Màu xanh/Cộng): Dòng code trong bản Cơ bản `weather_forecast-WeatherNow` (B)

#### 📄 Tệp: [server.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/server.py)
```diff
--- weather_forecast/server.py
+++ weather_forecast-WeatherNow/server.py
@@ -2,7 +2,7 @@
 WeatherNow — Ứng dụng dự báo thời tiết (100% Python + NiceGUI).
 
 Chạy:  python server.py
-Mở:    http://localhost:8080  (hoặc PORT trong .env, mặc định 8080)
+Mở:    http://localhost:5000
 """
 
 import os
@@ -18,11 +18,10 @@
 
 from src.app import run
 
-if __name__ in {'__main__', '__mp_main__'}:
-    print('WeatherNow (Python + NiceGUI)')
+if __name__ == '__main__':
+    print('WeatherNow (Python + NiceGUI): http://localhost:5000')
     print('  /          - Home')
     print('  /forecast  - Forecast')
     print('  /map       - Map')
     print('  /analysis  - Analysis')
     run()
-
```

#### 📄 Tệp: [src\app.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/app.py)
```diff
--- weather_forecast/src\app.py
+++ weather_forecast-WeatherNow/src\app.py
@@ -1,51 +1,19 @@
 import os
-import socket
 
 from nicegui import app, ui
 
 from .features import register_all
 
-_FALLBACK_PORTS = (8080, 5001, 5050, 8765, 8888)
-
-
-def pick_port(preferred: int) -> int:
-    """Chọn cổng trống; tránh WinError 10013/10048 khi 5000 bị chiếm hoặc bị chặn."""
-    candidates = [preferred, *_FALLBACK_PORTS]
-    seen: set[int] = set()
-    for port in candidates:
-        if port in seen:
-            continue
-        seen.add(port)
-        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
-            try:
-                sock.bind(('0.0.0.0', port))
-                return port
-            except OSError:
-                continue
-    raise RuntimeError(
-        'No free port. Close other apps or set PORT env (e.g. PORT=9000).'
-    )
-
-
 def run():
     static_dir = os.path.join(os.path.dirname(__file__), 'static')
     app.add_static_files('/static', static_dir)
-
+    
     register_all()
-    preferred = int(os.getenv('PORT', '8080'))
-    port = int(os.getenv('WEATHERNOW_PORT') or 0)
-    if not port:
-        port = pick_port(preferred)
-        os.environ['WEATHERNOW_PORT'] = str(port)
-    if port != preferred:
-        print(f'Port {preferred} busy, using http://localhost:{port}')
-
     secret = os.getenv('FLASK_SECRET_KEY', 'weathernow-dev-secret')
-    print(f'WeatherNow: http://localhost:{port}')
     ui.run(
         title='WeatherNow | Du bao thoi tiet',
-        port=port,
-        reload=True,
+        port=5000,
+        reload=False,
         storage_secret=secret,
         dark=True,
     )
```

#### 📄 Tệp: [src\common\charts_daily.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/common/charts_daily.py)
```diff
--- weather_forecast/src\common\charts_daily.py
+++ weather_forecast-WeatherNow/src\common\charts_daily.py
@@ -3,15 +3,13 @@
 import plotly.graph_objects as go
 
 from .charts_base import chart_layout
-from .units import get_units, convert_temp
 
 
 def create_temp_trend_chart(daily_data):
     if not daily_data:
         return None
-    u_temp = get_units()['unit_temp']
     labels = [d['day_name'][:3] for d in daily_data[:7]]
-    temps = [round(convert_temp((d['temp_max'] + d['temp_min']) / 2, u_temp)) for d in daily_data[:7]]
+    temps = [round((d['temp_max'] + d['temp_min']) / 2) for d in daily_data[:7]]
     fig = go.Figure()
     fig.add_trace(go.Scatter(
         x=labels, y=temps, mode='lines',
```

#### 📄 Tệp: [src\common\components.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/common/components.py)
```diff
--- weather_forecast/src\common\components.py
+++ weather_forecast-WeatherNow/src\common\components.py
@@ -19,9 +19,7 @@
 
 
 def apply_theme():
-    from src.common.units import get_units
-    theme = get_units().get('theme', 'dark')
-    ui.dark_mode(theme == 'dark')
+    ui.dark_mode(True)
     ui.add_css(STYLES)
 
 
@@ -43,20 +41,6 @@
             ui.label('Minh Hiển').classes('text-center w-full font-bold')
             ui.label('minhhien@weathernow.vn').classes('text-center w-full').style('opacity:0.5')
             ui.button('Đăng xuất', icon='logout', color='red', on_click=lambda: ui.navigate.to('/login')).props('flat').classes('w-full q-mt-md')
-
-    with ui.dialog().props('position=right') as settings_dialog:
-        with ui.card().classes('card').style(
-            'width: 450px; max-width: 100vw; height: 100vh; max-height: 100vh; '
-            'margin: 0; border-radius: 0; background: rgba(20,22,28,0.95); '
-            'backdrop-filter: blur(12px); padding: 1.5rem; overflow-y: auto;'
-        ):
-            with ui.row().classes('items-center justify-between w-full mb-4').style('position: sticky; top: 0; z-index: 10; background: rgba(20,22,28,0.95); padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1)'):
-                ui.label('Cài đặt').classes('text-h5').style('font-weight: 700; margin: 0')
-                ui.button(icon='close', on_click=settings_dialog.close).props('flat round dense')
-            
-            from src.features.settings.widgets import render_settings_content
-            render_settings_content()
-
 
     with ui.element('nav').classes('navbar'):
         with ui.row().classes('nav-left items-center no-wrap').style('gap:3rem'):
@@ -84,7 +68,7 @@
                 ui.button(icon='search', on_click=nav_search).classes('icon-btn-round').props('flat round dense')
 
         with ui.row().classes('nav-right items-center no-wrap').style('gap:1.25rem'):
-            ui.button(icon='settings', on_click=settings_dialog.open).classes('icon-btn-round').props('flat round')
+            ui.button(icon='settings', on_click=lambda: ui.navigate.to('/settings')).classes('icon-btn-round').props('flat round')
             with ui.element('div').classes('profile-avatar').on('click', profile_dialog.open):
                 ui.label('MH')
 
```

#### 📄 Tệp: [src\common\config.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/common/config.py)
```diff
--- weather_forecast/src\common\config.py
+++ weather_forecast-WeatherNow/src\common\config.py
@@ -1,15 +1,13 @@
 import os
-from pathlib import Path
 
 from dotenv import load_dotenv
 from nicegui import app
 
 from .utils import get_location_by_ip
 
-_ROOT = Path(__file__).resolve().parents[2]
-load_dotenv(_ROOT / '.env')
+load_dotenv()
 
-API_KEY = os.getenv('OPENWEATHER_API_KEY', '').strip()
+API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
 
 
 def get_city() -> str:
```

#### 📄 Tệp: [src\common\theme.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/common/theme.py)
```diff
--- weather_forecast/src\common\theme.py
+++ weather_forecast-WeatherNow/src\common\theme.py
@@ -210,202 +210,50 @@
 .stat-change.up { color: var(--success-color); font-size: 0.85rem; font-weight: 600; }
 .stat-change.down { color: var(--danger-text); font-size: 0.85rem; font-weight: 600; }
 
-.map-app .page-content { padding: 0 !important; max-width: none !important; margin: 0 !important; }
-.map-page-wrapper { position: relative; height: calc(100vh - 64px); min-height: 500px; overflow: hidden; background: #0a0c10; }
-.map-stage { position: relative; width: 100%; height: 100%; }
-.map-wind-particles {
-    position: absolute; inset: 0; z-index: 480;
-    pointer-events: none; width: 100%; height: 100%;
-}
-/* Tile màu OpenWeather — không filter để màu khớp legend */
-.map-stage[class*="map-layer-"] .leaflet-tile-pane img.leaflet-tile {
-    opacity: 1 !important;
-}
-.legend-title {
-    font-size: 0.82rem; font-weight: 700; color: rgba(255,255,255,0.97);
-    margin-bottom: 0.45rem; letter-spacing: 0.02em; text-shadow: 0 1px 4px rgba(0,0,0,0.4);
+.map-page-wrapper { position: relative; height: calc(100vh - 60px); overflow: hidden; }
+.map-container-full { position: relative; width: 100%; height: 100%; }
+.map-leaflet { width: 100%; height: 100%; z-index: 1; }
+.map-overlay { position: absolute; z-index: 100; }
+.map-search-float { top: 20px; left: 20px; }
+.map-view-float { top: 20px; right: 20px; }
+.map-sidebar-float { top: 100px; left: 20px; width: 220px; }
+.map-timeline-float { bottom: 30px; left: 20px; width: 350px; }
+.map-legend-float { bottom: 30px; right: 20px; width: 250px; }
+
+.map-menu-card {
+    background: rgba(15,15,20,0.7); backdrop-filter: blur(20px);
+    border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 0.5rem;
+    display: flex; flex-direction: column; gap: 0.25rem;
+}
+.map-menu-item {
+    display: flex; align-items: center; gap: 1rem; padding: 0.8rem 1.2rem;
+    color: rgba(255,255,255,0.7); border-radius: 8px; cursor: pointer; font-size: 0.95rem;
+}
+.map-menu-item:hover { background: rgba(255,255,255,0.05); color: #fff; }
+.map-menu-item.active { background: #ff5722; color: #fff; font-weight: 600; }
+.map-menu-divider { height: 1px; background: rgba(255,255,255,0.1); margin: 0.5rem 0; }
+.map-menu-footer { padding: 0.8rem 1.2rem; display: flex; align-items: center; justify-content: space-between; font-size: 0.85rem; color: rgba(255,255,255,0.6); }
+
+.round-icon-btn {
+    width: 45px; height: 45px; background: rgba(15,15,20,0.7); backdrop-filter: blur(10px);
+    border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff;
+}
+.timeline-card {
+    background: rgba(15,15,20,0.8); backdrop-filter: blur(20px);
+    border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem;
+    display: flex; align-items: center; gap: 1.25rem;
+}
+.legend-card {
+    background: rgba(15,15,20,0.8); backdrop-filter: blur(20px);
+    border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem;
 }
 .legend-gradient {
-    height: 12px; width: 100%; border-radius: 6px;
-    transition: background 0.25s ease; margin-bottom: 0.5rem;
-}
-.map-leaflet-fill,
-.map-stage .nicegui-leaflet {
-    position: absolute !important; inset: 0 !important;
-    width: 100% !important; height: 100% !important; z-index: 1 !important;
-}
-.map-ui-layer {
-    position: absolute; inset: 0; z-index: 500;
-    pointer-events: none; overflow: visible;
-}
-.map-float { position: absolute; pointer-events: auto; }
-.map-view-float { top: 16px; right: 16px; z-index: 600; }
-.map-chrome-panels {
-    position: absolute; inset: 0; pointer-events: none;
-}
-.map-chrome-panels > .map-float { pointer-events: auto; }
-.map-chrome-panels--hidden {
-    opacity: 0 !important; visibility: hidden !important; pointer-events: none !important;
-}
-.map-stage .leaflet-control-zoom { display: none !important; }
-.map-sidebar-float { top: 80px; left: 16px; width: 200px; }
-.map-location-float {
-    top: 80px; right: 16px; width: 300px; max-width: calc(100vw - 32px);
-    overflow: visible;
-}
-.map-location-float .map-location-card { max-width: 100%; }
-.map-timeline-float {
-    bottom: 20px; left: 50%; transform: translateX(-50%);
-    width: min(640px, calc(100vw - 40px));
-    z-index: 650;
-    pointer-events: auto;
-}
-.map-legend-float { bottom: 20px; right: 16px; width: 300px; max-width: calc(100vw - 32px); }
-
-.map-menu-card {
-    background: rgba(20, 34, 60, 0.58); backdrop-filter: blur(20px) saturate(1.5);
-    border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 0.35rem;
-    display: flex; flex-direction: column; gap: 0.15rem;
-    box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08);
-}
-.map-menu-item {
-    display: flex; align-items: center; gap: 0.75rem; padding: 0.65rem 1rem;
-    color: rgba(255,255,255,0.75); border-radius: 10px; cursor: pointer; font-size: 0.9rem;
-    transition: background 0.2s ease, color 0.2s ease;
-}
-.map-menu-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
-.map-menu-item.active { background: #ff5722; color: #fff; font-weight: 600; }
-.map-menu-divider { height: 1px; background: rgba(255,255,255,0.1); margin: 0.35rem 0.5rem; }
-.map-menu-footer {
-    padding: 0.65rem 1rem; display: flex; align-items: center;
-    justify-content: space-between; font-size: 0.82rem; color: rgba(255,255,255,0.55);
-}
-
-.map-location-card {
-    background: rgba(20, 34, 60, 0.58); backdrop-filter: blur(20px) saturate(1.5);
-    border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 1.1rem 1.25rem;
-    box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08);
-    overflow: hidden; position: relative; isolation: isolate;
-    width: 100%; box-sizing: border-box;
-}
-.map-location-title { font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 0.2rem; }
-.map-location-coords { font-size: 0.78rem; color: rgba(255,255,255,0.45); font-family: monospace; margin-bottom: 1rem; }
-.map-location-main {
-    display: flex !important; flex-direction: row !important; align-items: center !important;
-    gap: 0.85rem; width: 100%; margin-bottom: 0.75rem; box-sizing: border-box;
-}
-.map-location-icon-wrap {
-    flex: 0 0 56px; width: 56px; height: 56px; position: relative;
-    display: flex !important; align-items: center !important; justify-content: center !important;
-    border-radius: 14px; overflow: hidden;
-    background: linear-gradient(145deg, rgba(255, 183, 77, 0.22), rgba(255, 152, 0, 0.08));
-    border: 1px solid rgba(255, 183, 77, 0.25);
-}
-.map-location-icon-wrap > * {
-    display: flex !important; align-items: center !important; justify-content: center !important;
-    width: 100%; height: 100%; margin: 0 !important; padding: 0 !important;
-}
-.map-location-weather-glyph {
-    font-size: 2.1rem !important; line-height: 1 !important;
-}
-.map-location-weather-glyph.icon-sunny {
-    color: #ffca28 !important;
-    text-shadow: 0 0 12px rgba(255, 202, 40, 0.35);
-}
-.map-location-weather-glyph.icon-night {
-    color: #90caf9 !important;
-    text-shadow: 0 0 10px rgba(144, 202, 249, 0.35);
-}
-.map-location-weather-glyph.icon-rain {
-    color: #4fc3f7 !important;
-    text-shadow: 0 0 10px rgba(79, 195, 247, 0.35);
-}
-.map-location-weather-glyph.icon-cloud {
-    color: #b0bec5 !important;
-}
-.map-location-weather-glyph.icon-storm {
-    color: #ce93d8 !important;
-}
-.map-location-weather-glyph.icon-snow {
-    color: #e3f2fd !important;
-}
-.map-location-weather-glyph.icon-fog {
-    color: #cfd8dc !important;
-}
-.map-location-metric-wrap {
-    display: flex !important; flex-direction: row !important; align-items: baseline !important;
-    gap: 0.35rem; flex: 1 1 auto; min-width: 0;
-}
-.map-location-main-value {
-    font-size: 2.35rem; font-weight: 700; font-family: var(--font-heading);
-    line-height: 1; color: #fff; white-space: nowrap;
-}
-.map-location-main-unit {
-    font-size: 1.05rem; color: rgba(255,255,255,0.55); white-space: nowrap;
-}
-.map-location-details { display: flex; flex-direction: column; gap: 0.45rem; padding-top: 0.75rem; border-top: 1px solid rgba(148,187,255,0.18); }
-.map-location-row-label { font-size: 0.82rem; color: rgba(200,220,255,0.65); }
-.map-location-row-value { font-size: 0.82rem; color: rgba(255,255,255,0.97); font-weight: 600; }
-
-
-/* Glassmorphism round icon button for map floating actions */
-.round-icon-btn {
-    width: 52px;
-    height: 52px;
-    border-radius: 16px;
-    background: rgba(20, 34, 60, 0.65);
-    backdrop-filter: blur(20px) saturate(1.5);
-    border: 1px solid rgba(148,187,255,0.22);
-    color: white;
-    box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08);
-    min-width: unset !important;
-    padding: 0 !important;
-    transition: all 0.35s ease;
-}
-.round-icon-btn .q-btn__content {
-    background: transparent !important;
-}
-.round-icon-btn::before,
-.round-icon-btn::after {
-    display: none !important;
-}
-
-/* Base map nhạt — lớp thời tiết nổi bật */
-.map-leaflet .leaflet-tile-pane:first-child .leaflet-tile {
-    filter: brightness(1.08) saturate(0.78) contrast(0.92);
-}
-.map-leaflet .leaflet-overlay-pane .leaflet-tile {
-    filter: none;
-    transition: opacity 0.2s ease;
-}
-.map-timeline-slider .q-slider__track-container--h { height: 5px; }
-.map-timeline-slider .q-slider__thumb { width: 16px; height: 16px; }
-.timeline-card {
-    background: rgba(20, 34, 60, 0.58); backdrop-filter: blur(20px) saturate(1.5);
-    border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 0.75rem 1rem;
-    display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
-    align-items: center; gap: 0.65rem; width: 100%;
-    box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08);
-}
-.timeline-nav-btn { color: rgba(255,255,255,0.85) !important; min-width: 36px !important; }
-.timeline-time-label {
-    font-size: 0.8rem; color: rgba(255,255,255,0.9); font-family: monospace;
-    white-space: nowrap; min-width: 130px; text-align: right; font-weight: 500;
-}
-.legend-card {
-    background: rgba(20, 34, 60, 0.58); backdrop-filter: blur(20px) saturate(1.5);
-    border: 1px solid rgba(148,187,255,0.22); border-radius: 14px; padding: 0.85rem 1rem;
-    box-shadow: 0 8px 32px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.08);
-}
-.legend-labels { display: flex; justify-content: space-between; }
-.legend-end-label { font-size: 0.72rem; color: rgba(255,255,255,0.7); font-family: monospace; font-weight: 500; }
-
-@media (max-width: 900px) {
-    .map-location-float { width: 260px; top: 72px; right: 8px; }
-    .map-legend-float { width: 260px; bottom: 88px; right: 8px; }
-    .map-timeline-float { width: calc(100vw - 32px); bottom: 12px; }
-    .map-sidebar-float { width: 180px; }
-}
+    height: 8px; width: 100%;
+    background: linear-gradient(to right, #4527a0, #311b92, #1976d2, #4caf50, #ffeb3b, #fb8c00, #f44336);
+    border-radius: 4px;
+}
+.legend-header { display: flex; justify-content: space-between; font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 0.75rem; }
+.legend-labels { display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.7rem; color: rgba(255,255,255,0.4); }
 
 .app-footer {
     position: relative; margin-top: 6rem; padding: 4rem 2rem 3rem;
```

#### 📄 Tệp: [src\common\utils.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/common/utils.py)
```diff
--- weather_forecast/src\common\utils.py
+++ weather_forecast-WeatherNow/src\common\utils.py
@@ -7,7 +7,7 @@
     'sun': 'wb_sunny',
     'cloud-sun': 'wb_cloudy',
     'cloud': 'cloud',
-    'cloud-rain': 'water_drop',
+    'cloud-rain': 'grain',
     'cloud-lightning': 'thunderstorm',
     'cloud-snow': 'ac_unit',
     'cloud-fog': 'foggy',
```

#### 📄 Tệp: [src\features\analysis\charts.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/analysis/charts.py)
```diff
--- weather_forecast/src\features\analysis\charts.py
+++ weather_forecast-WeatherNow/src\features\analysis\charts.py
@@ -1,14 +1,12 @@
 import plotly.graph_objects as go
 
 from src.common.charts_base import chart_layout
-from src.common.units import get_units, convert_temp
 
 
 def build_charts(processed_data: dict) -> dict:
     if not processed_data:
         return {}
 
-    u_temp = get_units()['unit_temp']
     daily = processed_data.get('daily', [])
     hourly = processed_data.get('hourly', [])
     aqi = processed_data.get('aqi')
@@ -18,12 +16,12 @@
         fig1 = go.Figure()
         fig1.add_trace(go.Bar(
             x=[d['date'][5:] for d in daily[:7]],
-            y=[round(convert_temp(d['temp_min'], u_temp)) for d in daily[:7]],
+            y=[round(d['temp_min']) for d in daily[:7]],
             name='Thấp nhất', marker_color='rgba(255,255,255,0.2)',
         ))
         fig1.add_trace(go.Bar(
             x=[d['date'][5:] for d in daily[:7]],
-            y=[round(convert_temp(d['temp_max'], u_temp)) for d in daily[:7]],
+            y=[round(d['temp_max']) for d in daily[:7]],
             name='Cao nhất', marker_color='#4facfe',
         ))
         fig1.update_layout(chart_layout(
```

#### 📄 Tệp: [src\features\analysis\page.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/analysis/page.py)
```diff
--- weather_forecast/src\features\analysis\page.py
+++ weather_forecast-WeatherNow/src\features\analysis\page.py
@@ -5,11 +5,9 @@
     hero_background, navbar, plotly_chart,
 )
 from src.common.config import API_KEY, get_city
-from src.common.units import RefreshRegistry, get_units, convert_temp
 
 from .service import get_data
 from .widgets import render_stat_card
-from .charts import build_charts
 
 _TAG = 'div'
 
@@ -25,76 +23,47 @@
             hero_background(weather if not weather.get('error') else None)
             navbar('/analysis')
 
-            content_container = ui.element(_TAG).classes('w-full')
-            with content_container:
-                @ui.refreshable
-                def draw_content():
-                    nonlocal weather
-                    current_city = get_city()
-                    # If user updated default city in settings drawer, reload weather data
-                    if not weather.get('error') and weather.get('city_name', '').split(',')[0].strip().lower() != current_city.split(',')[0].strip().lower():
-                        weather = get_data(API_KEY, current_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
-                    
-                    # Re-apply theme
-                    apply_theme()
+            with ui.element(_TAG).classes('page-content content-wrapper'):
+                if weather.get('error'):
+                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
+                else:
+                    city_search_section('/analysis', weather)
+                    with ui.element(_TAG).classes('page-header'):
+                        ui.label('Phân tích chuyên sâu').classes('text-h4').style('font-weight:700;margin:0')
+                        ui.label(
+                            f'Xu hướng và thống kê khí tượng tại {weather.get("city_name", "N/A")}'
+                        ).style('opacity:0.7')
 
-                    with ui.element(_TAG).classes('page-content content-wrapper'):
-                        if weather.get('error'):
-                            ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
-                        else:
-                            city_search_section('/analysis', weather)
-                            with ui.element(_TAG).classes('page-header'):
-                                ui.label('Phân tích chuyên sâu').classes('text-h4').style('font-weight:700;margin:0')
-                                ui.label(
-                                    f'Xu hướng và thống kê khí tượng tại {weather.get("city_name", "N/A")}'
-                                ).style('opacity:0.7')
+                    charts = weather.get('charts', {})
+                    stats = weather.get('stats', {})
 
-                            # Re-generate analysis charts with active temperature unit
-                            charts = build_charts(weather)
-                            stats = weather.get('stats', {})
+                    with ui.element(_TAG).classes('analysis-row'):
+                        with ui.element(_TAG).classes('card'):
+                            ui.label('So sánh nhiệt độ (7 ngày)').classes('text-h6 mb-4')
+                            plotly_chart(charts.get('monthly'))
+                        with ui.element(_TAG).classes('card'):
+                            ui.label('Phân bổ chất lượng không khí').classes('text-h6 mb-4')
+                            plotly_chart(charts.get('aqi_dist'))
 
-                            with ui.element(_TAG).classes('analysis-row'):
-                                with ui.element(_TAG).classes('card'):
-                                    ui.label('So sánh nhiệt độ (7 ngày)').classes('text-h6 mb-4')
-                                    plotly_chart(charts.get('monthly'))
-                                with ui.element(_TAG).classes('card'):
-                                    ui.label('Phân bổ chất lượng không khí').classes('text-h6 mb-4')
-                                    plotly_chart(charts.get('aqi_dist'))
+                    with ui.element(_TAG).classes('card'):
+                        ui.label('Xác suất hiện tượng thời tiết đặc biệt').classes('text-h6 mb-4')
+                        plotly_chart(charts.get('events'))
 
-                            with ui.element(_TAG).classes('card'):
-                                ui.label('Xác suất hiện tượng thời tiết đặc biệt').classes('text-h6 mb-4')
-                                plotly_chart(charts.get('events'))
+                    with ui.element(_TAG).classes('analysis-metrics'):
+                        render_stat_card(
+                            'Nhiệt độ trung bình',
+                            f'{stats.get("avg_temp", "--")}°C',
+                            '+1.2° so với tuần trước', True,
+                        )
+                        render_stat_card(
+                            'Tổng lượng mưa dự kiến',
+                            f'{stats.get("total_rain", "--")} mm',
+                            '-15% so với tuần trước', False,
+                        )
+                        sunny_h = stats.get('sunny_days', 0) * 3 if stats else '--'
+                        render_stat_card(
+                            'Số giờ nắng dự kiến', f'{sunny_h}h',
+                            '+3h so với tuần trước', True,
+                        )
 
-                            u_temp = get_units()['unit_temp']
-                            avg_temp_raw = stats.get("avg_temp", "--")
-                            if avg_temp_raw != "--" and avg_temp_raw is not None:
-                                avg_temp_val = convert_temp(avg_temp_raw, u_temp)
-                            else:
-                                avg_temp_val = "--"
-                            temp_sym = '°F' if u_temp == 'F' else '°C'
-
-                            with ui.element(_TAG).classes('analysis-metrics'):
-                                render_stat_card(
-                                    'Nhiệt độ trung bình',
-                                    f'{avg_temp_val}{temp_sym}',
-                                    '+1.2° so với tuần trước', True,
-                                )
-                                render_stat_card(
-                                    'Tổng lượng mưa dự kiến',
-                                    f'{stats.get("total_rain", "--")} mm',
-                                    '-15% so với tuần trước', False,
-                                )
-                                sunny_h = stats.get('sunny_days', 0) * 3 if stats else '--'
-                                render_stat_card(
-                                    'Số giờ nắng dự kiến', f'{sunny_h}h',
-                                    '+3h so với tuần trước', True,
-                                )
-
-                    footer()
-
-                draw_content()
-
-            # Register for real-time UI updates
-            client_id = ui.context.client.id
-            RefreshRegistry.register(client_id, draw_content.refresh)
-            ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
+            footer()
```

#### 📄 Tệp: [src\features\forecast\charts.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/forecast/charts.py)
```diff
--- weather_forecast/src\features\forecast\charts.py
+++ weather_forecast-WeatherNow/src\features\forecast\charts.py
@@ -1,17 +1,15 @@
 import plotly.graph_objects as go
 
 from src.common.charts_base import chart_layout
-from src.common.units import get_units, convert_temp
 
 
 def create_detailed_chart(daily_data):
     if not daily_data:
         return None
-    u_temp = get_units()['unit_temp']
     slice_data = daily_data[:7]
     labels = [d['day_name'] for d in slice_data]
-    max_temps = [round(convert_temp(d['temp_max'], u_temp)) for d in slice_data]
-    min_temps = [round(convert_temp(d['temp_min'], u_temp)) for d in slice_data]
+    max_temps = [round(d['temp_max']) for d in slice_data]
+    min_temps = [round(d['temp_min']) for d in slice_data]
     fig = go.Figure()
     fig.add_trace(go.Scatter(
         x=labels, y=max_temps, mode='lines+markers', name='Cao nhất',
```

#### 📄 Tệp: [src\features\forecast\page.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/forecast/page.py)
```diff
--- weather_forecast/src\features\forecast\page.py
+++ weather_forecast-WeatherNow/src\features\forecast\page.py
@@ -5,11 +5,9 @@
     hero_background, navbar, plotly_chart,
 )
 from src.common.config import API_KEY, get_city
-from src.common.units import RefreshRegistry
 
 from .service import get_data
 from .widgets import render_daily_cards
-from .charts import create_detailed_chart
 
 _TAG = 'div'
 
@@ -25,43 +23,19 @@
             hero_background(weather if not weather.get('error') else None)
             navbar('/forecast')
 
-            content_container = ui.element(_TAG).classes('w-full')
-            with content_container:
-                @ui.refreshable
-                def draw_content():
-                    nonlocal weather
-                    current_city = get_city()
-                    # If user updated default city in settings drawer, reload weather data
-                    if not weather.get('error') and weather.get('city_name', '').split(',')[0].strip().lower() != current_city.split(',')[0].strip().lower():
-                        weather = get_data(API_KEY, current_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
-                    
-                    # Re-apply theme
-                    apply_theme()
+            with ui.element(_TAG).classes('page-content content-wrapper'):
+                if weather.get('error'):
+                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
+                else:
+                    city_search_section('/forecast', weather)
+                    with ui.element(_TAG).classes('page-header'):
+                        ui.label('Dự báo chi tiết').classes('text-h4').style('font-weight:700;margin:0')
+                        ui.label(
+                            f'Thông tin thời tiết chuyên sâu cho 7 ngày tới tại {weather.get("city_name", "N/A")}'
+                        ).style('opacity:0.7')
+                    render_daily_cards(weather.get('daily', []))
+                    with ui.element(_TAG).classes('card'):
+                        ui.label('Biến thiên nhiệt độ & Lượng mưa').classes('text-h6 mb-4')
+                        plotly_chart(weather.get('charts', {}).get('detailed'))
 
-                    with ui.element(_TAG).classes('page-content content-wrapper'):
-                        if weather.get('error'):
-                            ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
-                        else:
-                            city_search_section('/forecast', weather)
-                            with ui.element(_TAG).classes('page-header'):
-                                ui.label('Dự báo chi tiết').classes('text-h4').style('font-weight:700;margin:0')
-                                ui.label(
-                                    f'Thông tin thời tiết chuyên sâu cho 7 ngày tới tại {weather.get("city_name", "N/A")}'
-                                ).style('opacity:0.7')
-                            
-                            render_daily_cards(weather.get('daily', []))
-                            
-                            # Re-generate detailed forecast chart with the active temperature unit
-                            detailed_chart = create_detailed_chart(weather.get('daily', []))
-                            with ui.element(_TAG).classes('card'):
-                                ui.label('Biến thiên nhiệt độ & Lượng mưa').classes('text-h6 mb-4')
-                                plotly_chart(detailed_chart)
-
-                    footer()
-
-                draw_content()
-
-            # Register for real-time UI updates
-            client_id = ui.context.client.id
-            RefreshRegistry.register(client_id, draw_content.refresh)
-            ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
+            footer()
```

#### 📄 Tệp: [src\features\forecast\widgets.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/forecast/widgets.py)
```diff
--- weather_forecast/src\features\forecast\widgets.py
+++ weather_forecast-WeatherNow/src\features\forecast\widgets.py
@@ -1,7 +1,6 @@
 from nicegui import ui
 
 from src.common.utils import lucide_to_material
-from src.common.units import format_temp, format_wind_from_ms
 
 _TAG = 'div'
 
@@ -16,8 +15,8 @@
                 with ui.column().classes('detail-body items-center'):
                     ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud'))).style('font-size:64px;color:#4facfe')
                     with ui.row().classes('temp-range'):
-                        ui.label(format_temp(day["temp_max"])).style('font-weight:700;font-size:2rem')
-                        ui.label(format_temp(day["temp_min"])).classes('min').style('font-size:2rem;opacity:0.6')
+                        ui.label(f'{round(day["temp_max"])}°').style('font-weight:700;font-size:2rem')
+                        ui.label(f'{round(day["temp_min"])}°').classes('min').style('font-size:2rem;opacity:0.6')
                     ui.label(day['description'].capitalize()).style('opacity:0.8')
                 with ui.row().classes('detail-footer w-full justify-around'):
                     with ui.row().classes('footer-stat items-center gap-1'):
@@ -25,4 +24,4 @@
                         ui.label(f'{day["humidity_avg"]}%')
                     with ui.row().classes('footer-stat items-center gap-1'):
                         ui.icon('air')
-                        ui.label(format_wind_from_ms(day["wind_avg"]))
+                        ui.label(f'{day["wind_avg"]} m/s')
```

#### 📄 Tệp: [src\features\home\charts.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/home/charts.py)
```diff
--- weather_forecast/src\features\home\charts.py
+++ weather_forecast-WeatherNow/src\features\home\charts.py
@@ -1,19 +1,16 @@
 import plotly.graph_objects as go
 
 from src.common.charts_base import chart_layout
-from src.common.units import get_units, convert_temp
 
 
 def create_hourly_chart(hourly_data):
     if not hourly_data:
         return None
-    u_temp = get_units()['unit_temp']
     times = [h['time'] for h in hourly_data]
-    temps = [convert_temp(h['temp'], u_temp) for h in hourly_data]
-    temp_sym = '°F' if u_temp == 'F' else '°C'
+    temps = [h['temp'] for h in hourly_data]
     fig = go.Figure()
     fig.add_trace(go.Scatter(
-        x=times, y=temps, mode='lines+markers', name=f'Nhiệt độ ({temp_sym})',
+        x=times, y=temps, mode='lines+markers', name='Nhiệt độ',
         line=dict(color='#4facfe', width=3),
         fill='tozeroy', fillcolor='rgba(79, 172, 254, 0.2)',
         marker=dict(size=8, color='#4facfe'),
```

#### 📄 Tệp: [src\features\home\page.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/home/page.py)
```diff
--- weather_forecast/src\features\home\page.py
+++ weather_forecast-WeatherNow/src\features\home\page.py
@@ -5,12 +5,9 @@
     hero_background, navbar,
 )
 from src.common.config import API_KEY, get_city
-from src.common.units import RefreshRegistry
 
 from .service import get_data
 from .widgets import render_dashboard, render_hero, render_metrics
-from .charts import create_hourly_chart
-from src.common.charts_daily import create_temp_trend_chart, create_precip_chart
 
 _TAG = 'div'
 
@@ -26,39 +23,13 @@
             hero_background(weather if not weather.get('error') else None)
             navbar('/')
 
-            content_container = ui.element(_TAG).classes('w-full')
-            with content_container:
-                @ui.refreshable
-                def draw_content():
-                    nonlocal weather
-                    current_city = get_city()
-                    # If user updated default city in settings drawer, reload weather data
-                    if not weather.get('error') and weather.get('city_name', '').split(',')[0].strip().lower() != current_city.split(',')[0].strip().lower():
-                        weather = get_data(API_KEY, current_city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
-                    
-                    # Re-apply theme and dynamic background state
-                    apply_theme()
+            with ui.element(_TAG).classes('page-content content-wrapper'):
+                if weather.get('error'):
+                    ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
+                else:
+                    city_search_section('/', weather)
+                    render_hero(weather)
+                    render_metrics(weather)
+                    render_dashboard(weather)
 
-                    with ui.element(_TAG).classes('page-content content-wrapper'):
-                        if weather.get('error'):
-                            ui.label(f'Lỗi: {weather["error"]}').style('color:#f87171;padding:2rem')
-                        else:
-                            # Re-generate home charts with the active units
-                            if 'charts' in weather:
-                                weather['charts']['hourly'] = create_hourly_chart(weather.get('hourly', []))
-                                weather['charts']['temp_trend'] = create_temp_trend_chart(weather.get('daily', []))
-                                weather['charts']['precip'] = create_precip_chart(weather.get('daily', []))
-                            
-                            city_search_section('/', weather)
-                            render_hero(weather)
-                            render_metrics(weather)
-                            render_dashboard(weather)
-                    
-                    footer()
-
-                draw_content()
-
-            # Register for real-time UI updates
-            client_id = ui.context.client.id
-            RefreshRegistry.register(client_id, draw_content.refresh)
-            ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
+            footer()
```

#### 📄 Tệp: [src\features\home\widgets.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/home/widgets.py)
```diff
--- weather_forecast/src\features\home\widgets.py
+++ weather_forecast-WeatherNow/src\features\home\widgets.py
@@ -3,7 +3,6 @@
 from src.common.components import metric_card, plotly_chart
 from src.common.config import API_KEY
 from src.common.utils import lucide_to_material
-from src.common.units import format_temp, format_wind_from_ms, format_pressure, format_visibility
 
 
 def render_hero(weather: dict):
@@ -17,20 +16,20 @@
         with ui.element('div').classes('current-temp-large'):
             with ui.element('div').classes('temp-row'):
                 ui.icon(lucide_to_material(weather.get('lucide_icon', 'cloud'))).style('font-size:80px;color:#fff')
-                ui.label(format_temp(weather.get("temp", "--"))).classes('temp-value')
+                ui.label(f'{weather.get("temp", "--")}°C').classes('temp-value')
             with ui.element('div').classes('condition-info'):
                 ui.label(weather.get('desc', ''))
                 ui.label(' • ').style('opacity:0.5')
-                ui.label(f'Cảm giác như {format_temp(weather.get("feels_like", "--"))}')
+                ui.label(f'Cảm giác như {weather.get("feels_like", "--")}°C')
 
 
 def render_metrics(weather: dict):
     with ui.element('div').classes('metrics-grid'):
         metric_card('droplets', 'Độ ẩm', f'{weather.get("humidity", "--")}%')
-        metric_card('wind', 'Gió', format_wind_from_ms(weather.get("wind", "--")))
-        metric_card('gauge', 'Áp suất', format_pressure(weather.get("pressure", "--")))
-        metric_card('eye', 'Tầm nhìn', format_visibility(weather.get("visibility", "--")))
-        metric_card('thermometer-snowflake', 'Điểm sương', format_temp(weather.get("dew_point", "--")))
+        metric_card('wind', 'Gió', f'{weather.get("wind", "--")} km/h')
+        metric_card('gauge', 'Áp suất', f'{weather.get("pressure", "--")} hPa')
+        metric_card('eye', 'Tầm nhìn', f'{weather.get("visibility", "--")} km')
+        metric_card('thermometer-snowflake', 'Điểm sương', f'{weather.get("dew_point", "--")}°C')
         metric_card('sunrise', 'Bình minh', weather.get('sunrise', '--'))
         metric_card('sunset', 'Hoàng hôn', weather.get('sunset', '--'))
         uv = weather.get('uv_index')
@@ -128,5 +127,5 @@
                     ui.icon(lucide_to_material(day.get('lucide_icon', 'cloud')))
                     ui.label(f'{day["pop_max"]}%').style('font-size:0.8rem;opacity:0.6')
                 with ui.row().classes('forecast-temps justify-end'):
-                    ui.label(format_temp(day["temp_max"])).style('font-weight:600')
-                    ui.label(format_temp(day["temp_min"])).classes('min')
+                    ui.label(f'{round(day["temp_max"])}°').style('font-weight:600')
+                    ui.label(f'{round(day["temp_min"])}°').classes('min')
```

#### 📄 Tệp: [src\features\map\constants.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/map/constants.py)
```diff
--- weather_forecast/src\features\map\constants.py
+++ weather_forecast-WeatherNow/src\features\map\constants.py
@@ -1,6 +1,7 @@
-from .layer_config import LAYER_CONFIG
-
 MAP_LAYERS = [
-    (key, cfg['label'], cfg['icon'], f"{cfg['legend_min']} ... {cfg['legend_max']}")
-    for key, cfg in LAYER_CONFIG.items()
+    ('temp_new', 'Nhiệt độ', 'thermostat', '-70°C ... 50°C'),
+    ('pressure_new', 'Áp suất', 'speed', '950 ... 1050 hPa'),
+    ('wind_new', 'Tốc độ gió', 'air', '0 ... 100 m/s'),
+    ('precipitation_new', 'Lượng mưa', 'grain', '0 ... 10 mm'),
+    ('clouds_new', 'Mây', 'cloud', '0 ... 100%'),
 ]
```

#### 📄 Tệp: [src\features\map\page.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/map/page.py)
```diff
--- weather_forecast/src\features\map\page.py
+++ weather_forecast-WeatherNow/src\features\map\page.py
@@ -1,339 +1,103 @@
 from nicegui import ui
 
-from src.common.components import apply_theme, navbar
+from src.common.components import apply_theme, hero_background, navbar
 from src.common.config import API_KEY, get_city
 
 from .constants import MAP_LAYERS
-from .layer_config import LAYER_CONFIG
-from .particles import PARTICLES_SCRIPT
-from .service import (
-    BASE_TILE_URL,
-    DARK_BASE_TILE_URL,
-    LABELS_TILE_URL,
-    build_timeline,
-    build_weather_tile_url,
-    default_timeline_index,
-    fetch_hourly_forecast,
-    format_timeline_label,
-    get_hourly_weather,
-    resolve_snapshot,
-)
-from .widgets import create_location_panel
+from .service import get_data
 
 _TAG = 'div'
-_DEFAULT_OPACITY = 0.75
-_LAYER_CLASS_PREFIX = 'map-layer-'
 
 
 def register():
     @ui.page('/map')
     def map_page():
         apply_theme()
-        ui.add_body_html(f'<script>{PARTICLES_SCRIPT}</script>')
-
         city = get_city()
-        weather = get_hourly_weather(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
+        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
         lat = weather.get('lat', 21.0285) if not weather.get('error') else 21.0285
         lon = weather.get('lon', 105.8542) if not weather.get('error') else 105.8542
 
-        timeline = build_timeline(weather.get('hourly', []))
-        timeline_labels = [format_timeline_label(ts) for ts in timeline]
-        default_idx = default_timeline_index(timeline)
+        layer_state = {'name': 'temp_new', 'label': 'Nhiệt độ', 'range': '-70°C ... 50°C'}
+        map_ref = {'leaflet': None, 'weather_layer': None}
 
-        layer_state = {'name': 'temp_new', 'time_idx': default_idx, 'particles': True}
-        chrome_state = {'visible': True}
-        map_ref = {
-            'leaflet': None,
-            'weather_layer': None,
-            'base_layer': None,
-            'labels_layer': None,
-            'marker': None,
-            'ready': False,
-        }
-        sel_state = {
-            'lat': lat,
-            'lon': lon,
-            'hourly': weather.get('hourly', []) if not weather.get('error') else [],
-        }
-
-        def current_timestamp() -> int:
-            return timeline[layer_state['time_idx']]
-
-        def weather_url(layer_key: str | None = None) -> str:
-            key = layer_key or layer_state['name']
-            if not API_KEY:
-                return ''
-            return build_weather_tile_url(key, API_KEY, current_timestamp())
-
-        def tile_opacity(layer_key: str | None = None) -> float:
-            key = layer_key or layer_state['name']
-            return LAYER_CONFIG.get(key, {}).get('tile_opacity', _DEFAULT_OPACITY)
-
-        def sync_particles(wind_deg: int = 180):
-            active = layer_state['particles'] and layer_state['name'] == 'wind_new'
-            enabled = 'true' if active else 'false'
-            ui.run_javascript(
-                f'window.weatherMapParticles?.apply({{'
-                f'layer: "wind_new", enabled: {enabled}, windDeg: {wind_deg}'
-                f'}})'
-            )
-
-        def apply_layer_stage_class(layer_key: str):
-            for key in LAYER_CONFIG:
-                map_stage.classes(remove=f'{_LAYER_CLASS_PREFIX}{key.replace("_new", "")}')
-            short = layer_key.replace('_new', '')
-            map_stage.classes(add=f'{_LAYER_CLASS_PREFIX}{short}')
-
-        def refresh_weather_tiles(layer_key: str | None = None):
-            if not API_KEY:
-                return
-            key = layer_key or layer_state['name']
-            url = weather_url(key)
-            opacity = tile_opacity(key)
-            wl = map_ref['weather_layer']
-            if wl is None:
-                return
-            if map_ref['ready']:
-                wl.run_method('setUrl', url)
-                wl.run_method('setOpacity', opacity)
-                wl.run_method('redraw')
-
-        update_location = None
-
-        def refresh_location_panel():
-            if update_location is None:
-                return
-            ts = current_timestamp()
-            snap = resolve_snapshot(sel_state['lat'], sel_state['lon'], ts, sel_state['hourly'])
-            update_location(snap, sel_state['lat'], sel_state['lon'], layer_state['name'])
-            wind_deg = int(snap.get('wind_deg', 180) or 180)
-            sync_particles(wind_deg)
-
-        def on_map_ready():
-            map_ref['ready'] = True
-            apply_layer_stage_class(layer_state['name'])
-            refresh_weather_tiles(layer_state['name'])
-            refresh_location_panel()
-            ui.run_javascript('''
-                window.weatherMapParticles?.init();
-                const el = document.querySelector('.map-stage .leaflet-container');
-                if (el) {
-                    for (const k of Object.keys(el)) {
-                        const v = el[k];
-                        if (v && v.latLngToContainerPoint && v.getBounds) {
-                            window.__niceguiLeafletMap = v;
-                            break;
-                        }
-                    }
-                }
-                window.weatherMapParticles?.onMapMove();
-            ''')
-
-        def update_legend(layer_key: str):
-            cfg = LAYER_CONFIG[layer_key]
-            legend_title.set_text(f"{cfg['label']}   {cfg['legend_min']} … {cfg['legend_max']}")
-            legend_gradient.style(f"background: {cfg['gradient']}")
-            legend_min.set_text(cfg['legend_min'])
-            legend_max.set_text(cfg['legend_max'])
-
-        def on_timeline_change(idx: int):
-            idx = max(0, min(int(idx), len(timeline) - 1))
-            layer_state['time_idx'] = idx
-            refresh_weather_tiles()
-            refresh_location_panel()
-
-        def move_marker(new_lat: float, new_lon: float):
-            mk = map_ref['marker']
-            if mk is not None:
-                mk.run_method('setLatLng', [new_lat, new_lon])
-
-        def select_location(new_lat: float, new_lon: float):
-            sel_state['lat'] = new_lat
-            sel_state['lon'] = new_lon
-            if API_KEY:
-                sel_state['hourly'] = fetch_hourly_forecast(API_KEY, new_lat, new_lon)
-            move_marker(new_lat, new_lon)
-            refresh_location_panel()
-
-        def on_map_click(e):
-            latlng = e.args.get('latlng')
-            if not latlng:
-                return
-            if isinstance(latlng, dict):
-                click_lat, click_lon = latlng.get('lat'), latlng.get('lng')
-            else:
-                click_lat, click_lon = latlng[0], latlng[1]
-            if click_lat is not None and click_lon is not None:
-                select_location(float(click_lat), float(click_lon))
-
-        cfg0 = LAYER_CONFIG['temp_new']
-        menu_items: list = []
-
-        def set_layer(layer_key, btn_el):
-            layer_state['name'] = layer_key
-            update_legend(layer_key)
-            apply_layer_stage_class(layer_key)
-            for item in menu_items:
-                item.classes(remove='active')
-            btn_el.classes(add='active')
-            refresh_weather_tiles(layer_key)
-            refresh_location_panel()
-            if layer_key != 'wind_new':
-                ui.run_javascript('window.weatherMapParticles?.apply({enabled: false})')
-
-        def toggle_chrome():
-            chrome_state['visible'] = not chrome_state['visible']
-            if chrome_state['visible']:
-                map_chrome_panels.classes(remove='map-chrome-panels--hidden')
-                eye_btn.props('icon=visibility')
-            else:
-                map_chrome_panels.classes(add='map-chrome-panels--hidden')
-                eye_btn.props('icon=visibility_off')
-
-        def toggle_particles(e):
-            layer_state['particles'] = bool(e.value)
-            ts = current_timestamp()
-            snap = resolve_snapshot(sel_state['lat'], sel_state['lon'], ts, sel_state['hourly'])
-            sync_particles(int(snap.get('wind_deg', 180) or 180))
-
-        with ui.element(_TAG).classes('app-container map-app'):
+        with ui.element(_TAG).classes('app-container'):
+            hero_background(weather if not weather.get('error') else None)
             navbar('/map')
 
-            if not API_KEY:
-                with ui.row().classes('w-full justify-center').style(
-                    'position:relative;z-index:2000;background:#b71c1c;color:#fff;padding:0.5rem 1rem;font-size:0.9rem'
-                ):
-                    ui.label(
-                        'Thiếu OPENWEATHER_API_KEY trong file .env — bản đồ màu không hiển thị. '
-                        'Thêm key rồi restart server.'
+            with ui.element(_TAG).classes('page-content map-page-wrapper'):
+                with ui.element(_TAG).classes('map-container-full'):
+                    m = ui.leaflet(center=(lat, lon), zoom=5).classes('map-leaflet w-full h-full')
+                    map_ref['leaflet'] = m
+                    m.tile_layer(
+                        url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
+                        options={'maxZoom': 18},
                     )
+                    if API_KEY:
+                        wl = m.tile_layer(
+                            url_template=f'https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
+                            options={'opacity': 0.6},
+                        )
+                        map_ref['weather_layer'] = wl
+                    m.marker(latlng=(lat, lon))
 
-            with ui.element(_TAG).classes('page-content map-page-wrapper'):
-                map_stage = ui.element(_TAG).classes('map-stage map-layer-temp')
-                with map_stage:
-                    m = ui.leaflet(
-                        center=(lat, lon),
-                        zoom=5,
-                        options={'zoomControl': False},
-                    ).classes('map-leaflet-fill')
-                    map_ref['leaflet'] = m
-                    m.on('init', on_map_ready)
-                    m.on('map-click', on_map_click)
-                    m.on('map-moveend', lambda _: ui.run_javascript('window.weatherMapParticles?.onMapMove()'))
-                    m.on('map-zoomend', lambda _: ui.run_javascript('window.weatherMapParticles?.onMapMove()'))
-                    m.clear_layers()
-                    _tile_opts = {'maxZoom': 19, 'subdomains': 'abcd'}
-                    if API_KEY:
-                        map_ref['base_layer'] = m.tile_layer(
-                            url_template=DARK_BASE_TILE_URL,
-                            options={
-                                **_tile_opts,
-                                'attribution': '&copy; OpenStreetMap &copy; CARTO',
-                            },
-                        )
-                        map_ref['weather_layer'] = m.tile_layer(
-                            url_template=build_weather_tile_url(
-                                'temp_new', API_KEY, timeline[default_idx]
-                            ),
-                            options={'opacity': 1.0, 'maxZoom': 19},
-                        )
-                        map_ref['labels_layer'] = m.tile_layer(
-                            url_template=LABELS_TILE_URL,
-                            options={**_tile_opts, 'opacity': 1.0},
-                        )
-                    else:
-                        map_ref['base_layer'] = m.tile_layer(
-                            url_template=BASE_TILE_URL,
-                            options={
-                                **_tile_opts,
-                                'attribution': '&copy; OpenStreetMap &copy; CARTO',
-                            },
-                        )
-                    map_ref['marker'] = m.marker(latlng=(lat, lon))
-                    ui.element('canvas').classes('map-wind-particles')
+                    legend_label = ui.label(layer_state['label'])
+                    legend_range = ui.label(layer_state['range'])
 
-                    with ui.element(_TAG).classes('map-ui-layer'):
-                        with ui.element(_TAG).classes('map-float map-view-float'):
-                            eye_btn = ui.button(icon='visibility', on_click=toggle_chrome).classes(
-                                'round-icon-btn'
-                            ).props('flat round')
+                    def set_layer(layer_key, label, range_text, btn_el):
+                        layer_state['name'] = layer_key
+                        layer_state['label'] = label
+                        layer_state['range'] = range_text
+                        legend_label.set_text(label)
+                        legend_range.set_text(range_text)
+                        for item in menu_items:
+                            item.classes(remove='active')
+                        btn_el.classes(add='active')
+                        if API_KEY and map_ref['leaflet']:
+                            if map_ref['weather_layer']:
+                                map_ref['weather_layer'].delete()
+                            map_ref['weather_layer'] = map_ref['leaflet'].tile_layer(
+                                url_template=f'https://tile.openweathermap.org/map/{layer_key}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}',
+                                options={'opacity': 0.6},
+                            )
 
-                        map_chrome_panels = ui.element(_TAG).classes('map-chrome-panels')
-                        with map_chrome_panels:
-                            with ui.element(_TAG).classes('map-float map-sidebar-float'):
-                                with ui.element(_TAG).classes('map-menu-card'):
-                                    for i, (key, label, icon, _range) in enumerate(MAP_LAYERS):
-                                        item = ui.element(_TAG).classes(
-                                            'map-menu-item' + (' active' if i == 0 else '')
-                                        )
-                                        menu_items.append(item)
-                                        with item:
-                                            with ui.row().classes('items-center gap-3 no-wrap'):
-                                                ui.icon(icon)
-                                                ui.label(label)
-                                        item.on('click', lambda k=key, el=item: set_layer(k, el))
+                    with ui.element(_TAG).classes('map-overlay map-search-float'):
+                        ui.button(icon='search').classes('round-icon-btn').props('flat round')
 
-                                    ui.element(_TAG).classes('map-menu-divider')
-                                    with ui.element(_TAG).classes('map-menu-footer'):
-                                        ui.label('Hạt gió')
-                                        wind_switch = ui.switch(value=True)
-                                        wind_switch.on_value_change(toggle_particles)
+                    with ui.element(_TAG).classes('map-overlay map-view-float'):
+                        ui.button(icon='visibility').classes('round-icon-btn').props('flat round')
 
-                            with ui.element(_TAG).classes('map-float map-location-float'):
-                                update_location = create_location_panel()
+                    menu_items = []
+                    with ui.element(_TAG).classes('map-overlay map-sidebar-float'):
+                        with ui.element(_TAG).classes('map-menu-card'):
+                            for i, (key, label, icon, range_text) in enumerate(MAP_LAYERS):
+                                item = ui.element(_TAG).classes('map-menu-item' + (' active' if i == 0 else ''))
+                                menu_items.append(item)
+                                with item:
+                                    with ui.row().classes('items-center gap-3 no-wrap'):
+                                        ui.icon(icon)
+                                        ui.label(label)
+                                item.on('click', lambda k=key, l=label, r=range_text, el=item: set_layer(k, l, r, el))
 
-                            with ui.element(_TAG).classes('map-float map-timeline-float'):
-                                with ui.element(_TAG).classes('timeline-card'):
-                                    def step_time(delta: int):
-                                        new_idx = max(0, min(int(slider.value) + delta, len(timeline) - 1))
-                                        slider.set_value(new_idx)
-                                        on_timeline_change(new_idx)
+                            ui.element(_TAG).classes('map-menu-divider')
+                            with ui.element(_TAG).classes('map-menu-footer'):
+                                ui.label('Hiệu ứng gió')
+                                ui.switch(value=True)
 
-                                    ui.button(icon='chevron_left', on_click=lambda: step_time(-1)).props(
-                                        'flat round dense'
-                                    ).classes('timeline-nav-btn')
-                                    slider = ui.slider(
-                                        min=0,
-                                        max=max(len(timeline) - 1, 0),
-                                        value=default_idx,
-                                        step=1,
-                                    ).classes('map-timeline-slider').style('flex:1;min-width:120px').props(
-                                        'snap color=orange'
-                                    )
-                                    ui.button(icon='chevron_right', on_click=lambda: step_time(1)).props(
-                                        'flat round dense'
-                                    ).classes('timeline-nav-btn')
-                                    time_label = ui.label(timeline_labels[default_idx]).classes(
-                                        'timeline-time-label'
-                                    )
-                                    time_label.bind_text_from(
-                                        slider,
-                                        'value',
-                                        backward=lambda i: timeline_labels[
-                                            max(0, min(int(i), len(timeline_labels) - 1))
-                                        ],
-                                    )
+                    with ui.element(_TAG).classes('map-overlay map-timeline-float'):
+                        with ui.element(_TAG).classes('timeline-card w-full'):
+                            ui.button(icon='play_arrow').props('flat round').classes('text-white')
+                            with ui.column().classes('flex-grow gap-2'):
+                                ui.slider(min=0, max=100, value=50).classes('w-full')
+                                ui.label('2026-05-16 13:00').style('font-size:0.8rem;opacity:0.6;font-family:monospace')
 
-                                    def on_slider_event(e):
-                                        on_timeline_change(e.args)
-
-                                    slider.on('update:model-value', on_slider_event, throttle=0)
-
-                            with ui.element(_TAG).classes('map-float map-legend-float'):
-                                with ui.element(_TAG).classes('legend-card'):
-                                    legend_title = ui.label(cfg0['label']).classes('legend-title')
-                                    legend_gradient = ui.element(_TAG).classes('legend-gradient')
-                                    legend_gradient.style(f"background: {cfg0['gradient']}")
-                                    with ui.row().classes('legend-labels w-full justify-between'):
-                                        legend_min = ui.label(cfg0['legend_min']).classes('legend-end-label')
-                                        legend_max = ui.label(cfg0['legend_max']).classes('legend-end-label')
-
-        def draw_content():
-            apply_theme()
-            refresh_location_panel()
-
-        from src.common.units import RefreshRegistry
-        client_id = ui.context.client.id
-        RefreshRegistry.register(client_id, draw_content)
-        ui.context.client.on_disconnect(lambda: RefreshRegistry.clear(client_id))
-
+                    with ui.element(_TAG).classes('map-overlay map-legend-float'):
+                        with ui.element(_TAG).classes('legend-card w-full'):
+                            with ui.row().classes('legend-header w-full justify-between'):
+                                legend_label
+                                legend_range
+                            ui.element(_TAG).classes('legend-gradient')
+                            with ui.row().classes('legend-labels w-full justify-between'):
+                                ui.label('Thấp').style('font-size:0.7rem;opacity:0.4')
+                                ui.label('Trung bình').style('font-size:0.7rem;opacity:0.4')
+                                ui.label('Cao').style('font-size:0.7rem;opacity:0.4')
```

#### 📄 Tệp: [src\features\map\service.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/map/service.py)
```diff
--- weather_forecast/src\features\map\service.py
+++ weather_forecast-WeatherNow/src\features\map\service.py
@@ -1,303 +1,14 @@
-import hashlib
-import math
-from datetime import datetime, timedelta
-
-import requests
-
 from src.common.api import fetch_current
-from src.common.utils import icon_to_lucide, lucide_to_material, process_weather_data
-
-from .layer_config import LAYER_CONFIG
-
-_hourly_cache: dict = {}
-_location_cache: dict = {}
-_cache_expiry = timedelta(minutes=10)
-
-BASE_TILE_URL = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
-DARK_BASE_TILE_URL = 'https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png'
-LABELS_TILE_URL = 'https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png'
-WEATHER_OVERLAY_LAYERS = frozenset(LAYER_CONFIG.keys())
-MAP_STEP_SECONDS = 3 * 3600
-
-_COMPASS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
+from src.common.utils import process_weather_data
 
 
-def build_weather_tile_url(layer_key: str, api_key: str, unix_ts: int | None = None) -> str:
-    url = (
-        f'https://tile.openweathermap.org/map/{layer_key}/{{z}}/{{x}}/{{y}}.png'
-        f'?appid={api_key}'
-    )
-    if unix_ts is not None:
-        url += f'&date={unix_ts}&_t={unix_ts}'
-    return url
-
-
-def round_map_timestamp(unix_ts: int) -> int:
-    return (unix_ts // MAP_STEP_SECONDS) * MAP_STEP_SECONDS
-
-
-def format_timeline_label(unix_ts: int) -> str:
-    return datetime.fromtimestamp(unix_ts).strftime('%Y-%m-%d %H:%M')
-
-
-def _now_ts() -> int:
-    return round_map_timestamp(int(datetime.now().timestamp()))
-
-
-def build_timeline(hourly: list) -> list[int]:
-    """Các mốc thời gian quanh thời điểm hiện tại (giờ địa phương, bước 3h)."""
-    now = _now_ts()
-    if hourly:
-        times = sorted({round_map_timestamp(int(h['dt'])) for h in hourly})
-        if times:
-            return times
-    past_steps, future_steps = 8, 31
-    start = now - past_steps * MAP_STEP_SECONDS
-    return [start + i * MAP_STEP_SECONDS for i in range(past_steps + 1 + future_steps)]
-
-
-def default_timeline_index(timeline: list[int]) -> int:
-    if not timeline:
-        return 0
-    now = _now_ts()
-    return min(range(len(timeline)), key=lambda i: abs(timeline[i] - now))
-
-
-def fetch_hourly_forecast(api_key: str, lat: float, lon: float) -> list:
-    cache_key = f'{lat:.2f},{lon:.2f}'
-    now = datetime.utcnow()
-    if cache_key in _location_cache:
-        cached = _location_cache[cache_key]
-        if now - cached['time'] < _cache_expiry:
-            return cached['hourly']
-    url = (
-        f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}'
-        f'&exclude=minutely,daily,alerts&units=metric&appid={api_key}'
-    )
-    resp = requests.get(url, timeout=8)
-    hourly: list = []
-    if resp.status_code == 200:
-        hourly = resp.json().get('hourly', [])
-    if not hourly:
-        # Fallback 1: dùng forecast 5 ngày / bước 3 giờ
-        hourly = fetch_forecast3h_by_coords(api_key, lat, lon)
-    if not hourly:
-        # Fallback khi One Call không trả hourly (quota/gói API):
-        # dùng current weather để panel bên phải vẫn có số liệu.
-        current = fetch_current_by_coords(api_key, lat, lon)
-        if current:
-            hourly = [snapshot_from_current(current)]
-    if hourly:
-        _location_cache[cache_key] = {'time': now, 'hourly': hourly}
-    return hourly
-
-
-def fetch_forecast3h_by_coords(api_key: str, lat: float, lon: float) -> list:
-    try:
-        resp = requests.get(
-            'https://api.openweathermap.org/data/2.5/forecast',
-            params={'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric', 'lang': 'vi'},
-            timeout=8,
-        )
-        if not resp.ok:
-            return []
-        rows = resp.json().get('list', [])
-        hourly: list = []
-        for row in rows:
-            hourly.append({
-                'dt': int(row.get('dt', 0)),
-                'temp': row.get('main', {}).get('temp', 0),
-                'feels_like': row.get('main', {}).get('feels_like', 0),
-                'wind_speed': row.get('wind', {}).get('speed', 0),
-                'wind_deg': row.get('wind', {}).get('deg', 0),
-                'humidity': row.get('main', {}).get('humidity', 0),
-                'clouds': row.get('clouds', {}).get('all', 0),
-                'pressure': row.get('main', {}).get('pressure', 0),
-                'rain': {'1h': (row.get('rain') or {}).get('3h', 0) / 3},
-                'weather': row.get('weather') or [{'icon': '01d'}],
-            })
-        return hourly
-    except Exception:
-        return []
-
-
-def fetch_current_by_coords(api_key: str, lat: float, lon: float) -> dict | None:
-    try:
-        resp = requests.get(
-            'https://api.openweathermap.org/data/2.5/weather',
-            params={'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric', 'lang': 'vi'},
-            timeout=8,
-        )
-        if resp.ok:
-            return resp.json()
-    except Exception:
-        return None
-    return None
-
-
-def snapshot_from_current(current: dict) -> dict:
-    return {
-        'dt': int(current.get('dt', datetime.now().timestamp())),
-        'temp': current.get('main', {}).get('temp', 0),
-        'feels_like': current.get('main', {}).get('feels_like', 0),
-        'wind_speed': current.get('wind', {}).get('speed', 0),
-        'wind_deg': current.get('wind', {}).get('deg', 0),
-        'humidity': current.get('main', {}).get('humidity', 0),
-        'clouds': current.get('clouds', {}).get('all', 0),
-        'pressure': current.get('main', {}).get('pressure', 0),
-        'rain': {'1h': (current.get('rain') or {}).get('1h', 0)},
-        'weather': current.get('weather') or [{'icon': '01d'}],
-    }
-
-
-def find_hourly_at(hourly: list, unix_ts: int) -> dict | None:
-    if not hourly:
-        return None
-    target = round_map_timestamp(unix_ts)
-    return min(hourly, key=lambda h: abs(int(h['dt']) - target))
-
-
-def wind_direction_label(deg: int) -> str:
-    ix = int((deg % 360) / 22.5 + 0.5) % 16
-    return f'{deg}° {_COMPASS[ix]}'
-
-
-def snapshot_is_empty(snap: dict) -> bool:
-    return snap.get('temp') == '--'
-
-
-def weather_material_icon(owm_icon: str, rain_mm: float = 0, clouds: int = 0) -> str:
-    """Icon Material: nắng = mặt trời, mưa = giọt nước, ..."""
-    code = (owm_icon or '01d')[:2]
-    if rain_mm > 0.3 or code in ('09', '10'):
-        return 'water_drop'
-    if code == '11':
-        return 'thunderstorm'
-    if code == '13':
-        return 'ac_unit'
-    if code == '50':
-        return 'foggy'
-    if code in ('03', '04') or clouds > 70:
-        return 'cloud'
-    if code == '02':
-        return 'wb_cloudy'
-    if code == '01':
-        return 'nights_stay' if str(owm_icon).endswith('n') else 'wb_sunny'
-    return lucide_to_material(icon_to_lucide(owm_icon))
-
-
-def _pseudo_random(seed: int, slot: int) -> float:
-    x = (seed ^ (slot * 2654435761)) & 0xFFFFFFFF
-    return (x % 10000) / 10000.0
-
-
-def synthetic_snapshot(lat: float, lon: float, unix_ts: int) -> dict:
-    """Số liệu giả lập ổn định theo vị trí + thời gian (đổi khi kéo timeline / bấm map)."""
-    digest = hashlib.md5(f'{lat:.4f},{lon:.4f},{unix_ts}'.encode()).digest()
-    seed = int.from_bytes(digest[:4], 'big')
-    rnd = lambda slot: _pseudo_random(seed, slot)
-
-    dt = datetime.fromtimestamp(unix_ts)
-    hour, month = dt.hour, dt.month
-
-    base_temp = 27 - abs(lat - 16) * 0.42 + (rnd(1) - 0.5) * 5
-    seasonal = 5 * math.sin((month - 4) * math.pi / 6)
-    diurnal = 7 * math.sin((hour - 7) * math.pi / 12)
-    temp = round(max(-12, min(44, base_temp + seasonal + diurnal)), 1)
-
-    feels = round(temp + (rnd(2) - 0.5) * 6, 1)
-    humidity = int(40 + rnd(3) * 55)
-    clouds = int(rnd(4) * 100)
-    rain = round((rnd(5) * 6 if clouds > 55 else rnd(5) * 1.5), 1)
-    wind = round(0.8 + rnd(6) * 15, 1)
-    deg = int(rnd(7) * 360)
-    pressure = int(995 + rnd(8) * 35)
-
-    if rain > 2.5:
-        icon = '10d'
-    elif clouds > 75:
-        icon = '04d'
-    elif clouds > 35:
-        icon = '03d'
-    else:
-        icon = '01d' if 6 <= hour <= 18 else '01n'
-
-    snap = {
-        'dt': unix_ts,
-        'temp': temp,
-        'feels_like': feels,
-        'wind_speed': wind,
-        'wind_deg': deg,
-        'humidity': humidity,
-        'clouds': clouds,
-        'pressure': pressure,
-        'rain': {'1h': rain},
-        'weather': [{'icon': icon}],
-    }
-    snap['material_icon'] = weather_material_icon(icon, rain, clouds)
-    return hourly_snapshot(snap)
-
-
-def resolve_snapshot(lat: float, lon: float, unix_ts: int, hourly: list) -> dict:
-    snap = hourly_snapshot(find_hourly_at(hourly, unix_ts))
-    if snapshot_is_empty(snap):
-        snap = synthetic_snapshot(lat, lon, unix_ts)
-    return snap
-
-
-def hourly_snapshot(hourly_item: dict | None) -> dict:
-    if not hourly_item:
-        return {
-            'temp': '--', 'feels_like': '--', 'wind_speed': '--', 'wind_deg': 0,
-            'wind_dir': '--', 'humidity': '--', 'clouds': '--', 'pressure': '--',
-            'rain': 0, 'icon': '01d', 'material_icon': 'wb_sunny',
-        }
-    rain = hourly_item.get('rain') or {}
-    rain_mm = rain.get('1h', 0) if isinstance(rain, dict) else float(rain or 0)
-    icon = (hourly_item.get('weather') or [{}])[0].get('icon', '01d')
-    clouds = int(hourly_item.get('clouds', 0))
-    deg = int(hourly_item.get('wind_deg', 0))
-    return {
-        'temp': round(hourly_item.get('temp', 0), 1),
-        'feels_like': round(hourly_item.get('feels_like', 0), 1),
-        'wind_speed': round(hourly_item.get('wind_speed', 0), 1),
-        'wind_deg': deg,
-        'wind_dir': wind_direction_label(deg),
-        'humidity': int(hourly_item.get('humidity', 0)),
-        'clouds': clouds,
-        'pressure': int(hourly_item.get('pressure', 0)),
-        'rain': round(rain_mm, 1),
-        'icon': icon,
-        'material_icon': weather_material_icon(icon, rain_mm, clouds),
-    }
-
-
-def main_metric_value(snapshot: dict, layer_key: str) -> tuple[str, str]:
-    cfg = LAYER_CONFIG[layer_key]
-    field = cfg['field']
-    val = snapshot.get(field, '--')
-    if val == '--':
-        return '--', cfg['unit']
-    if field == 'pressure':
-        return str(val), 'hPa'
-    if field == 'rain':
-        return str(val), 'mm'
-    if field == 'clouds':
-        return str(val), '%'
-    return str(val), cfg['unit']
-
-
-def get_hourly_weather(api_key: str, city: str = 'Hanoi') -> dict:
+def get_data(api_key: str, city: str = 'Hanoi') -> dict:
     try:
         current = fetch_current(api_key, city)
         lat, lon = current['coord']['lat'], current['coord']['lon']
         processed = process_weather_data({'current': current, 'lat': lat, 'lon': lon})
         if not processed:
             return {'error': 'Không xử lý được dữ liệu'}
-        hourly = fetch_hourly_forecast(api_key, lat, lon)
-        processed['lat'] = lat
-        processed['lon'] = lon
-        processed['hourly'] = hourly
         return processed
     except Exception as e:
         return {'error': str(e)}
```

#### 📄 Tệp: [src\features\settings\__init__.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/settings/__init__.py)
```diff
--- weather_forecast/src\features\settings\__init__.py
+++ weather_forecast-WeatherNow/src\features\settings\__init__.py
@@ -1,3 +1 @@
 from .page import register
-
-__all__ = ['register']
```

#### 📄 Tệp: [src\features\settings\page.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/settings/page.py)
```diff
--- weather_forecast/src\features\settings\page.py
+++ weather_forecast-WeatherNow/src\features\settings\page.py
@@ -1,31 +1,22 @@
 from nicegui import ui
 
-from src.common.components import (
-    apply_theme, footer, hero_background, navbar,
-)
-from src.common.config import API_KEY, get_city
-from src.features.home.service import get_data
-
+from src.common.components import apply_theme, footer, hero_background, navbar
 from .widgets import render_settings_content
-
-_TAG = 'div'
-
 
 def register():
     @ui.page('/settings')
     def settings_page():
         apply_theme()
-        city = get_city()
-        weather = get_data(API_KEY, city) if API_KEY else {'error': 'Thiếu OPENWEATHER_API_KEY'}
-
-        with ui.element(_TAG).classes('app-container'):
-            hero_background(weather if not weather.get('error') else None)
+        
+        with ui.element('div').classes('app-container'):
+            hero_background(None)
             navbar('/settings')
-
-            with ui.element(_TAG).classes('page-content content-wrapper'):
-                with ui.element(_TAG).classes('page-header'):
-                    ui.label('Cấu hình ứng dụng').classes('text-h4').style('font-weight:700;margin:0')
-                    ui.label('Tùy chỉnh đơn vị, giao diện và thiết lập cá nhân').style('opacity:0.7')
+            
+            with ui.element('div').classes('page-content content-wrapper'):
+                with ui.element('div').classes('page-header'):
+                    ui.label('Cài đặt hệ thống').classes('text-h4').style('font-weight:700;margin:0')
+                    ui.label('Tùy chỉnh giao diện và sở thích cá nhân.').style('opacity:0.7')
+                
                 render_settings_content()
-
+                
             footer()
```

#### 📄 Tệp: [src\features\settings\widgets.py](file:///c:/Users/asus/Downloads/Hieplol/weather_forecast/src/features/settings/widgets.py)
```diff
--- weather_forecast/src\features\settings\widgets.py
+++ weather_forecast-WeatherNow/src\features\settings\widgets.py
@@ -1,161 +1,24 @@
-from nicegui import app, ui
-
-from src.common.config import get_city, set_city
-from src.common.units import _DEFAULTS, RefreshRegistry
-
-
-def _save(key: str, value):
-    """Lưu ngay vào storage và kích hoạt làm mới UI tức thì."""
-    if app.storage.user.get(key) != value:
-        app.storage.user[key] = value
-        RefreshRegistry.trigger(ui.context.client.id)
-
+from nicegui import ui
 
 def render_settings_content():
-    # Đọc giá trị hiện tại
-    def val(key):
-        return app.storage.user.get(key, _DEFAULTS[key])
-
-    with ui.element('div').style(
-        'display:flex;flex-direction:column;gap:2rem;margin-top:2rem;max-width:820px'
-    ):
-        # ── 1. Đơn vị đo lường ─────────────────────────────────────────────
+    with ui.element('div').classes('settings-grid').style('display: flex; flex-direction: column; gap: 2rem; margin-top: 2rem; max-width: 800px;'):
         with ui.card().classes('card w-full'):
-            with ui.row().classes('items-center gap-2 mb-4'):
-                ui.icon('straighten').style('color:#4facfe;font-size:22px')
-                ui.label('Đơn vị đo lường').classes('text-h6').style('margin:0')
-
-            # Nhiệt độ
-            with ui.row().classes('items-center gap-4 mb-2'):
-                ui.label('🌡 Nhiệt độ:').style('min-width:130px;font-weight:500')
-                temp_radio = ui.radio(
-                    {'C': '°C (Celsius)', 'F': '°F (Fahrenheit)'},
-                    value=val('unit_temp'),
-                ).props('inline')
-                temp_radio.on_value_change(lambda e: _save('unit_temp', e.value))
-
-            ui.separator().style('margin:0.5rem 0')
-
-            # Tốc độ gió
-            with ui.row().classes('items-center gap-4 mb-2'):
-                ui.label('💨 Tốc độ gió:').style('min-width:130px;font-weight:500')
-                wind_radio = ui.radio(
-                    {'km/h': 'km/h', 'm/s': 'm/s', 'mph': 'mph (dặm/giờ)'},
-                    value=val('unit_wind'),
-                ).props('inline')
-                wind_radio.on_value_change(lambda e: _save('unit_wind', e.value))
-
-            ui.separator().style('margin:0.5rem 0')
-
-            # Áp suất
-            with ui.row().classes('items-center gap-4 mb-2'):
-                ui.label('📊 Áp suất:').style('min-width:130px;font-weight:500')
-                pressure_radio = ui.radio(
-                    {'hPa': 'hPa', 'mmHg': 'mmHg (milimét thuỷ ngân)'},
-                    value=val('unit_pressure'),
-                ).props('inline')
-                pressure_radio.on_value_change(lambda e: _save('unit_pressure', e.value))
-
-            ui.separator().style('margin:0.5rem 0')
-
-            # Tầm nhìn
+            ui.label('Giao diện').classes('text-h6 mb-4')
+            ui.switch('Chế độ Tối (Dark Mode)', value=True).props('color="blue"')
+            ui.switch('Ảnh nền động (Dynamic Background)', value=True).props('color="blue"')
+            
+        with ui.card().classes('card w-full'):
+            ui.label('Đơn vị đo lường').classes('text-h6 mb-4')
             with ui.row().classes('items-center gap-4'):
-                ui.label('👁 Tầm nhìn:').style('min-width:130px;font-weight:500')
-                visibility_radio = ui.radio(
-                    {'km': 'km', 'miles': 'Miles'},
-                    value=val('unit_visibility'),
-                ).props('inline')
-                visibility_radio.on_value_change(lambda e: _save('unit_visibility', e.value))
-
-            ui.label('✓ Thay đổi áp dụng ngay khi reload trang kế tiếp.').style(
-                'font-size:0.78rem;color:rgba(255,255,255,0.4);margin-top:0.75rem'
-            )
-
-        # ── 2. Giao diện / Theme ────────────────────────────────────────────
+                ui.label('Nhiệt độ:')
+                ui.radio(['C (Celsius)', 'F (Fahrenheit)'], value='C (Celsius)').props('inline')
+            with ui.row().classes('items-center gap-4 mt-2'):
+                ui.label('Tốc độ gió:')
+                ui.radio(['km/h', 'm/s', 'mph'], value='km/h').props('inline')
+                
         with ui.card().classes('card w-full'):
-            with ui.row().classes('items-center gap-2 mb-4'):
-                ui.icon('palette').style('color:#4facfe;font-size:22px')
-                ui.label('Giao diện (Theme)').classes('text-h6').style('margin:0')
-
-            with ui.row().classes('items-center gap-4 mb-3'):
-                ui.label('🎨 Chủ đề:').style('min-width:130px;font-weight:500')
-                theme_radio = ui.radio(
-                    {'dark': '🌙 Dark (Tối)', 'light': '☀️ Light (Sáng)'},
-                    value=val('theme'),
-                ).props('inline')
-
-                def on_theme_change(e):
-                    _save('theme', e.value)
-                    ui.dark_mode(e.value == 'dark')
-                    ui.notify(
-                        'Đã đổi giao diện — reload trang để thấy đầy đủ hiệu ứng.',
-                        type='info', position='top-right', timeout=3000,
-                    )
-
-                theme_radio.on_value_change(on_theme_change)
-
-            with ui.row().classes('items-center gap-4'):
-                ui.switch(
-                    'Ảnh nền động (Dynamic Background)',
-                    value=app.storage.user.get('dynamic_bg', True),
-                    on_change=lambda e: _save('dynamic_bg', e.value),
-                ).props('color="blue"')
-
-        # ── 3. Thành phố mặc định ───────────────────────────────────────────
-        with ui.card().classes('card w-full'):
-            with ui.row().classes('items-center gap-2 mb-4'):
-                ui.icon('place').style('color:#4facfe;font-size:22px')
-                ui.label('Thành phố mặc định').classes('text-h6').style('margin:0')
-
-            current_city = get_city()
-            city_label = ui.label(f'Thành phố hiện tại: {current_city}').style(
-                'font-size:0.9rem;color:rgba(255,255,255,0.55);margin-bottom:0.75rem'
-            )
-
-            with ui.row().classes('items-center gap-3 w-full').style('flex-wrap:nowrap'):
-                city_input = ui.input(
-                    placeholder='Ví dụ: Da Nang, Hanoi, Tokyo...',
-                    value=current_city,
-                ).props('outlined dense dark').style(
-                    'flex:1;min-width:200px;background:rgba(255,255,255,0.05);border-radius:8px'
-                )
-
-                def save_city():
-                    new_city = city_input.value.strip()
-                    if not new_city:
-                        ui.notify('Vui lòng nhập tên thành phố!', type='warning')
-                        return
-                    set_city(new_city)
-                    city_label.set_text(f'Thành phố hiện tại: {new_city}')
-                    ui.notify(
-                        f'✅ Đã đặt "{new_city}" làm thành phố mặc định!',
-                        type='positive', position='top-right', timeout=2000,
-                    )
-                    RefreshRegistry.trigger(ui.context.client.id)
-
-
-                ui.button('Đặt làm mặc định', icon='pin_drop', on_click=save_city).props(
-                    'unelevated no-caps'
-                ).style('background:#4facfe;color:#0a0c10;font-weight:600;border-radius:8px;white-space:nowrap')
-
-            ui.label('💡 Trang chủ và Dự báo sẽ tải thành phố này khi bạn mở lại.').style(
-                'font-size:0.78rem;color:rgba(255,255,255,0.4);margin-top:0.75rem'
-            )
-
-        # ── 4. Thông báo ────────────────────────────────────────────────────
-        with ui.card().classes('card w-full'):
-            with ui.row().classes('items-center gap-2 mb-4'):
-                ui.icon('notifications').style('color:#4facfe;font-size:22px')
-                ui.label('Thông báo').classes('text-h6').style('margin:0')
-
-            ui.switch(
-                'Cảnh báo thời tiết nguy hiểm',
-                value=app.storage.user.get('notif_alert', True),
-                on_change=lambda e: _save('notif_alert', e.value),
-            ).props('color="red"')
-
-            ui.switch(
-                'Bản tin dự báo buổi sáng',
-                value=app.storage.user.get('notif_morning', False),
-                on_change=lambda e: _save('notif_morning', e.value),
-            ).props('color="blue"').style('margin-top:0.5rem')
+            ui.label('Thông báo').classes('text-h6 mb-4')
+            ui.switch('Cảnh báo thời tiết nguy hiểm', value=True).props('color="red"')
+            ui.switch('Bản tin dự báo buổi sáng', value=False).props('color="blue"')
+            
+        ui.button('Lưu cài đặt', on_click=lambda: ui.notify('Đã lưu cài đặt thành công!', type='positive')).classes('w-full mt-4 q-btn-search').props('unelevated no-caps')
```

