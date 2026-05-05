# weather_forecast
A Python-based weather app featuring a professional modular architecture. It integrates OpenWeatherMap API for real-time data, uses Streamlit for an interactive UI, and is structured for scalability with dedicated modules for data fetching, processing, and future ML integration. Perfect for tracking live weather and learning system design.

# Giải thích ý nghĩa từng file 
env và .env.example
.env: Chứa API key thật của bạn. File này KHÔNG được push lên GitHub. Mỗi thành viên tự tạo file này trên máy mình.
.env.example: Chỉ là bản mẫu (template), không có key thật. File này được push lên GitHub để các thành viên biết cần điền gì vào .env.
# .env.example (push lên GitHub)
OPENWEATHER_API_KEY=your_api_key_here

config.py
File này đọc API key từ .env và định nghĩa các hằng số cấu hình dùng chung cho cả project như BASE_URL. Các file khác import từ đây thay vì hardcode trực tiếp.

requirements.txt
Liệt kê tất cả thư viện Python cần cài. Khi thêm thư viện mới, cần cập nhật file này bằng lệnh:
pip freeze > requirements.txt
Người mới pull về chỉ cần chạy một lệnh để cài đủ thư viện:
pip install -r requirements.txt

src/__init__.py
File rỗng, không cần viết gì. Sự tồn tại của file này giúp Python hiểu rằng folder src là một package, cho phép các file khác import từ src.fetch hay src.process.

src/fetch.py
Phụ trách toàn bộ việc giao tiếp với API OpenWeatherMap. File này chứa các hàm gọi HTTP, xử lý lỗi kết nối, và trả về dữ liệu thô dạng JSON.

src/process.py
Nhận dữ liệu JSON thô từ fetch.py, trích xuất thông tin cần thiết, và chuyển đổi thành các cấu trúc dữ liệu dễ dùng hơn như dict hoặc DataFrame của pandas.

app.py
File chính của giao diện người dùng, sử dụng Streamlit. Import và gọi các hàm từ src/fetch.py và src/process.py, sau đó hiển thị kết quả bằng biểu đồ và bảng dữ liệu.
 
# Để code sạch hơn tránh xung đột tui mình sẽ code trên nhanh develop nha
# Anh em nhập lệnh này vào teminal thì sao này anh em push lên code sẽ push lên nhánh develop nha sao khi code ổn định thì mình sẽ đưa nó về nhánh main 
git fetch
git checkout develop