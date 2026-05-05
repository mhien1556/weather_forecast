import pandas as pd

def parse_current(data: dict) -> dict:
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
        "pressure": data["main"]["pressure"],
    }

def parse_forecast(data: dict) -> pd.DataFrame:
    records = []
    for item in data["list"]:
        records.append({
            "datetime": item["dt_txt"],
            "temp": item["main"]["temp"],
            "feels_like": item["main"]["feels_like"],
            "humidity": item["main"]["humidity"],
            "description": item["weather"][0]["description"],
            "wind_speed": item["wind"]["speed"],
            "icon": item["weather"][0]["icon"],
        })
    df = pd.DataFrame(records)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df