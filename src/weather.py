"""
天气查询核心模块
"""
import requests


def get_coordinates(city: str) -> dict:
    """
    获取城市信息（坐标、国家等）

    Args:
        city: 城市名称

    Returns:
        包含 latitude, longitude, country, name 的字典

    Raises:
        ValueError: 找不到城市时抛出
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError(f"找不到城市: {city}")

    result = data["results"][0]
    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country", "未知"),
        "name": result.get("name", city),
    }


def get_weather(lat: float, lon: float) -> dict:
    """
    获取当前天气数据

    Args:
        lat: 纬度
        lon: 经度

    Returns:
        天气数据字典，包含 temperature, weather_code, time
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,weather_code"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "weather_code": current.get("weather_code"),
        "time": current.get("time"),
    }


def get_forecast(lat: float, lon: float, days: int = 3) -> list[dict]:
    """
    获取未来天气预报

    Args:
        lat: 纬度
        lon: 经度
        days: 预报天数（默认 3 天）

    Returns:
        预报数据列表，每项包含 date, max_temp, min_temp, weather_code
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=temperature_2m_max,temperature_2m_min,weather_code&"
        f"forecast_days={days}"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    daily = data.get("daily", {})
    forecasts = []
    for i in range(len(daily.get("time", []))):
        forecasts.append({
            "date": daily["time"][i],
            "max_temp": daily["temperature_2m_max"][i],
            "min_temp": daily["temperature_2m_min"][i],
            "weather_code": daily["weather_code"][i],
        })

    return forecasts


def parse_weather_code(code: int) -> str:
    """
    将 WMO 天气代码转换为中文描述

    Args:
        code: WMO 天气代码

    Returns:
        中文天气描述
    """
    weather_map = {
        0: "晴朗",
        1: "基本晴朗",
        2: "多云",
        3: "阴天",
        45: "雾",
        48: "雾凇",
        51: "小毛毛雨",
        53: "中毛毛雨",
        55: "大毛毛雨",
        56: "冻毛毛雨",
        57: "大冻毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        66: "冻雨",
        67: "大冻雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "小阵雨",
        81: "中阵雨",
        82: "大阵雨",
        85: "小阵雪",
        86: "大阵雪",
        95: "雷暴",
        96: "雷暴伴小冰雹",
        99: "雷暴伴大冰雹",
    }
    return weather_map.get(code, f"未知天气代码({code})")
