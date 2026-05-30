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
 note những file đã thay đổi
## `src/features/__init__.py`
- Thêm import và đăng ký route `register_profile()` vào `register_all()`

### `src/common/config.py`
- Thêm hàm `get_current_user()` — lấy user đang đăng nhập từ session
- Thêm hàm `set_current_user()` — lưu user vào session
- Thêm hàm `logout_user()` — xóa user khỏi session
- Sửa hàm `set_city()` — tự động lưu lịch sử tìm kiếm nếu đã đăng nhập

### `src/common/components.py`
- Sửa `navbar()` — hiện nút **Đăng nhập** khi chưa login, hiện **avatar + dropdown menu** khi đã login
- Dropdown menu có: Thông tin cá nhân, Lịch sử, Yêu thích, Thông báo, Đăng xuất
- Các mục dropdown navigate tới `/profile?tab=xxx`

### `src/common/api.py`
- Thêm hàm `_normalize_city()` — chuyển tên tỉnh thành tiếng Việt có dấu sang không dấu trước khi gọi API
- Map sẵn 60+ tỉnh thành phổ biến (Đồng Tháp → Dong Thap, Hà Nội → Hanoi...)

### `src/common/utils.py`
- Sửa `parse_hourly()` — parse giờ thực tế từ `dt_txt` thay vì tính tay

### `src/features/login/page.py`
- Bỏ navbar và footer khỏi trang login
- Căn giữa card bằng flexbox `100vh`

### `src/features/login/widgets.py`
- Thiết kế lại UI: glassmorphism card, tab Đăng nhập / Đăng ký
- Thêm câu hỏi bảo mật khi đăng ký (dùng để quên mật khẩu)
- Thêm flow **Quên mật khẩu** 2 bước: nhập username → trả lời câu hỏi bảo mật → đặt mật khẩu mới
- **Đăng ký xong** → chuyển về tab Đăng nhập thay vì vào thẳng trang chủ

### `src/features/home/page.py`
- Thêm redirect về `/login` nếu chưa đăng nhập

### `src/features/analysis/page.py`
- Thiết kế lại layout: 4 KPI cards, 2 chart chính, chart theo giờ, phần nhận xét
- Bỏ phần `stat_card` bị trùng lặp ở phía dưới

### `src/features/analysis/charts.py`
- Sửa format ngày trục X: `Thứ 3\n27/05` thay vì `05-27` (Plotly tự parse sai thành timestamp)
- Thêm chart **Dự báo nhiệt độ theo giờ** (line chart màu cam)
- Sửa chart **Xác suất mưa** dùng giờ thực tế từ API
- Sửa `barmode='group'` cho chart so sánh nhiệt độ — click 1 lần ẩn/hiện đúng

---
*© 2026 WeatherNow — Phát triển và Thiết kế bởi Minh Hiển.*
