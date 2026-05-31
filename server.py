"""
WeatherNow — Ứng dụng dự báo thời tiết (100% Python + NiceGUI).

Chạy:  python server.py
Mở:    http://localhost:8080  (hoặc PORT trong .env, mặc định 8080)
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dotenv import load_dotenv

load_dotenv()

from src.app import run

if __name__ in {'__main__', '__mp_main__'}:
    print('WeatherNow (Python + NiceGUI)')
    print('  /          - Home')
    print('  /forecast  - Forecast')
    print('  /map       - Map')
    print('  /analysis  - Analysis')
    run()

