"""
Configuration module for WeatherNow application.
"""

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
UNITS = "metric"

if not API_KEY:
    import warnings
    warnings.warn(
        "⚠️  OPENWEATHER_API_KEY not found. "
        "Create a .env file with: OPENWEATHER_API_KEY=your_key"
    )
