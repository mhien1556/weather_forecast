import pandas as pd
import math


# ─────────────────────────────────────────────
# Current weather parsing
# ─────────────────────────────────────────────

def parse_current(data: dict) -> dict:
    wind_deg = data["wind"].get("deg", 0)
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
        "temp": round(data["main"]["temp"], 1),
        "feels_like": round(data["main"]["feels_like"], 1),
        "feels_delta": round(data["main"]["feels_like"] - data["main"]["temp"], 1),
        "temp_min": round(data["main"]["temp_min"], 1),
        "temp_max": round(data["main"]["temp_max"], 1),
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
        "wind_deg": wind_deg,
        "wind_dir": _deg_to_compass(wind_deg),
        "visibility": data.get("visibility", None),
        "cloudiness": data["clouds"]["all"],
        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"],
    }


def _deg_to_compass(deg: float) -> str:
    directions = ["Bắc", "Đông Bắc", "Đông", "Đông Nam",
                  "Nam", "Tây Nam", "Tây", "Tây Bắc"]
    idx = round(deg / 45) % 8
    return directions[idx]


# ─────────────────────────────────────────────
# Forecast parsing
# ─────────────────────────────────────────────

def parse_forecast(data: dict) -> pd.DataFrame:
    records = []
    for item in data["list"]:
        records.append({
            "datetime": item["dt_txt"],
            "temp": round(item["main"]["temp"], 1),
            "feels_like": round(item["main"]["feels_like"], 1),
            "temp_min": round(item["main"]["temp_min"], 1),
            "temp_max": round(item["main"]["temp_max"], 1),
            "humidity": item["main"]["humidity"],
            "pressure": item["main"]["pressure"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
            "wind_speed": item["wind"]["speed"],
            "wind_deg": item["wind"].get("deg", 0),
            "cloudiness": item["clouds"]["all"],
            "rain_3h": item.get("rain", {}).get("3h", 0),
            "pop": round(item.get("pop", 0) * 100),  # probability of precipitation %
        })
    df = pd.DataFrame(records)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    return df


def get_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate hourly forecast into daily min/max/avg."""
    daily = df.groupby("date").agg(
        temp_min=("temp", "min"),
        temp_max=("temp", "max"),
        temp_avg=("temp", "mean"),
        humidity_avg=("humidity", "mean"),
        rain_total=("rain_3h", "sum"),
        pop_max=("pop", "max"),
        description=("description", "first"),
        icon=("icon", "first"),
    ).reset_index()
    daily["temp_avg"] = daily["temp_avg"].round(1)
    daily["humidity_avg"] = daily["humidity_avg"].round(0).astype(int)
    daily["rain_total"] = daily["rain_total"].round(1)
    return daily


# ─────────────────────────────────────────────
# Air Quality Index helpers
# ─────────────────────────────────────────────

AQI_LABELS = {
    1: ("Tốt", "#00e400"),
    2: ("Khá", "#ffff00"),
    3: ("Trung bình", "#ff7e00"),
    4: ("Kém", "#ff0000"),
    5: ("Rất kém", "#8f3f97"),
}


def parse_aqi(data: dict) -> dict | None:
    try:
        item = data["list"][0]
        aqi = item["main"]["aqi"]
        label, color = AQI_LABELS.get(aqi, ("N/A", "#aaaaaa"))
        components = item["components"]
        return {
            "aqi": aqi,
            "label": label,
            "color": color,
            "pm2_5": components.get("pm2_5", 0),
            "pm10": components.get("pm10", 0),
            "o3": components.get("o3", 0),
            "no2": components.get("no2", 0),
            "co": components.get("co", 0),
        }
    except Exception:
        return None


# ─────────────────────────────────────────────
# UV Index helpers
# ─────────────────────────────────────────────

def uv_category(uvi: float) -> tuple[str, str]:
    if uvi is None:
        return "N/A", "#aaaaaa"
    if uvi < 3:
        return "Thấp", "#289500"
    elif uvi < 6:
        return "Trung bình", "#f7e400"
    elif uvi < 8:
        return "Cao", "#f85900"
    elif uvi < 11:
        return "Rất cao", "#d8001d"
    else:
        return "Cực kỳ cao", "#6b49c8"