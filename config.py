import os
from pathlib import Path
from dotenv import load_dotenv

# Tìm đường dẫn đến thư mục chứa file config.py hiện tại
# Dù bạn đứng ở bất cứ đâu chạy lệnh, nó cũng sẽ tìm đúng file .env nằm cùng thư mục với config.py
BASE_DIR = Path(__file__).resolve().parent

# Chỉ định rõ đường dẫn file .env
env_path = BASE_DIR / '.env'

# Load file
load_dotenv(dotenv_path=env_path)

# Lấy biến
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5"
# Test thử
if API_KEY:
   print(API_KEY)
else:
    print(f"❌ Không tìm thấy API Key tại: {env_path}")