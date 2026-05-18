"""
WeatherNow — Ứng dụng dự báo thời tiết (100% Python + NiceGUI).

Chạy:  python server.py
Mở:    http://localhost:5000
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dotenv import load_dotenv

load_dotenv()

from src.app import run

if __name__ == '__main__':
    print('WeatherNow (Python + NiceGUI): http://localhost:5000')
    print('  /          - Home')
    print('  /forecast  - Forecast')
    print('  /map       - Map')
    print('  /analysis  - Analysis')
    run()
