"""
WeatherNow — Flask server (giao diện HTML + API).

Chạy:  python server.py
Mở:    http://localhost:5000

Giao diện nằm trong src/web/templates/ và src/web/static/
Logic trang: src/web/pages/  ↔  src/ui/*_page.py
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dotenv import load_dotenv

load_dotenv()

from src.web.app import create_app

app = create_app()

if __name__ == "__main__":
    print("WeatherNow: http://localhost:5000")
    print("  /          - Home")
    print("  /forecast  - Forecast")
    print("  /map         - Map")
    print("  /analysis    - Analysis")
    app.run(debug=True, port=5000)
