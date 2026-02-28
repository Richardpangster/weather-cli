"""
天气查询核心模块
"""
import requests


def get_coordinates(city: str) -> tuple[float, float]:
    """
    获取城市经纬度

    Args:
        city: 城市名称

    Returns:
        (latitude, longitude) 元组

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
    return result["latitude"], result["longitude"]


def get_weather(lat: float, lon: float) -> dict:
    """
    获取天气数据

    Args:
        lat: 纬度
        lon: 经度

    Returns:
        天气数据字典，包含 temperature 和 weather_code
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
    }


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
