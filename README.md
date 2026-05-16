# WeatherNow - Ứng dụng Dự báo Thời tiết Hiện đại 🌤️

WeatherNow là một nền tảng dự báo thời tiết trực quan với thiết kế **Cinematic Glassmorphism**. Dự án được xây dựng trên nền tảng Python (Flask) kết hợp với các công nghệ web hiện đại để mang lại trải nghiệm người dùng sống động và dữ liệu chính xác theo thời gian thực từ OpenWeatherMap API.

---

## ✨ Các Chức năng Chính

1. **Trang chủ (Dashboard):**
   - Theo dõi thời tiết hiện tại: Nhiệt độ, cảm giác thực tế, độ ẩm, tốc độ gió, áp suất và tầm nhìn.
   - Tìm kiếm thành phố toàn cầu với hệ thống gợi ý nhanh.
   - Hiển thị Chất lượng Không khí (AQI) chi tiết kèm các thông số bụi mịn (PM2.5, CO).
   - Biểu đồ biến thiên nhiệt độ hàng giờ sinh động.

2. **Dự báo 5 Ngày (Forecast):**
   - Xem chi tiết thời tiết trong 5 ngày tới với độ chính xác cao.
   - Biểu đồ nhiệt độ chi tiết (Min/Max) giúp người dùng dễ dàng theo dõi xu hướng.
   - Thông tin mô tả thời tiết trực quan (Mưa, Nắng, Mây...).

3. **Bản đồ Thời tiết (Interactive Map):**
   - Bản đồ tương tác sử dụng Leaflet.js.
   - Các lớp dữ liệu thời tiết trực quan: Nhiệt độ, Lượng mưa, Tốc độ gió, Mây, Áp suất và Radar.
   - Hiệu ứng gió (Wind particles) sống động.

4. **Phân tích Dữ liệu (Weather Analysis):**
   - Thống kê so sánh nhiệt độ giữa các ngày.
   - Phân tích biểu đồ phân phối chất lượng không khí.
   - Dự báo xác suất mưa trong ngày dưới dạng biểu đồ diện tích (Area chart).

---

## 📂 Cấu trúc Dự án

```text
WeatherNow/
├── server.py               # File khởi chạy ứng dụng chính
├── requirements.txt        # Danh sách thư viện cần thiết
├── .env                    # Lưu trữ API Key (OpenWeatherMap)
└── src/
    └── web/
        ├── app.py          # Cấu hình Flask routes và logic API
        ├── charts.py       # Logic tạo biểu đồ động (Plotly)
        ├── utils.py        # Hàm hỗ trợ xử lý dữ liệu và định dạng
        ├── static/         # Chứa CSS, Images và các tài nguyên tĩnh
        └── pages/          # Chứa các trang HTML theo module
            ├── home/       # Trang chủ (index.html, logic backend riêng)
            ├── forecast/   # Trang dự báo (forecast.html)
            ├── map/        # Trang bản đồ (map.html)
            └── analysis/   # Trang phân tích (analysis.html)
```

---

## 🚀 Hướng dẫn Cài đặt & Chạy

1. **Cài đặt môi trường:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình API Key:**
   - Đăng ký lấy key tại [OpenWeatherMap](https://openweathermap.org/api).
   - Điền key vào file `.env`: `OPENWEATHER_API_KEY=your_api_key_here`.

3. **Chạy ứng dụng:**
   ```bash
   python server.py
   ```
   Sau đó truy cập: `http://localhost:5000`

---

## 📅 Lộ trình Phát triển Tiếp theo (Roadmap)

Dưới đây là các yêu cầu nâng cấp tính năng và tối ưu hóa giao diện đang được triển khai:

### 1. Trang chủ (Home)
- **Tối ưu bố cục**: Chỉnh sửa giao diện nhỏ gọn, vuông vức và cân đối hơn.
- **Xử lý dữ liệu**: Hiển thị trạng thái "Không có dữ liệu" chuyên nghiệp cho các trường thông tin trống.
- **Nâng cấp AQI**: Bổ sung thêm các chỉ số phụ và thông tin sức khỏe cho phần Chất lượng không khí.
- *File tác động:* `src/web/pages/home/index.html`, `src/web/static/css/style.css`.

### 2. Trang Dự báo (Forecast)
- **Chi tiết hàng ngày**: Khi nhấn vào một ngày bất kỳ, hiển thị thông tin chi tiết của ngày đó (nhiệt độ theo giờ, độ ẩm, gió...).
- **Hoàn thiện UI**: Kiểm tra lỗi hiển thị và nâng cấp tính năng tương tác.
- *File tác động:* `src/web/pages/forecast/forecast.html`, `src/web/static/css/style.css`.

### 3. Trang Bản đồ (Map)
- **Điều khiển thời gian**: Cải thiện hiển thị nút tùy chỉnh theo giờ ở góc trái dưới.
- **Tìm kiếm vị trí**: Thêm chức năng kính lúp cho phép tìm kiếm địa điểm trực tiếp trên bản đồ.
- **Thanh thông số động**: Tự động thay đổi chú thích (legend) dựa trên lớp bản đồ đang chọn (Nhiệt độ, Mưa, Mây...).
- **Chế độ Focus**: Nút "Con mắt" ở góc phải để ẩn/hiện các công cụ UI, chỉ để lại bản đồ và header.
- *File tác động:* `src/web/pages/map/map.html`, `src/web/pages/map/map.py`.

### 4. Trang Phân tích (Analysis)
- **Thiết kế lại**: Xây dựng lại hoàn toàn giao diện phân tích cho chuyên nghiệp hơn.
- **Tính năng bổ sung**: Thêm các biểu đồ so sánh lịch sử và dự báo xu hướng dài hạn.
- *File tác động:* `src/web/pages/analysis/analysis.html`, `src/web/pages/analysis/analysis.py`.

### 5. Hệ thống Người dùng (Auth) & Cài đặt
- **Đăng nhập Dynamic**: Navbar tự động chuyển đổi giữa nút "Đăng nhập" và "Tên người dùng" kèm Avatar sau khi đăng nhập thành công.
- **Dropdown chức năng**: Menu xổ xuống khi bấm vào User (Sửa thông tin, Lịch sử truy cập, Đăng xuất).
- **Cài đặt nâng cao**: Tùy chỉnh Giao diện (Theme) và thiết lập "Thành phố mặc định".
- *File tác động:* `src/web/app.py`, `src/web/pages/auth/auth.py`, `src/web/pages/home/index.html`.

---

## 🛠 Công nghệ Sử dụng

- **Backend:** Python (Flask), Requests.
- **Frontend:** HTML5, Vanilla CSS, JavaScript (ES6+).
- **Thư viện Biểu đồ:** Plotly.js.
- **Bản đồ:** Leaflet.js, OpenWeatherMap Tile Layers.
- **Icons:** Lucide Icons.

---
*© 2024 WeatherNow Team - Được phát triển cho trải nghiệm dự báo thời tiết chuyên nghiệp.*
