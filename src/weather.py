"""
天气查询核心模块

提供天气 API 调用和数据解析功能。
"""
import logging
from typing import Dict, Optional

import requests

# 配置模块级日志记录器
logger = logging.getLogger("weather-cli.weather")


def get_coordinates(city: str) -> Dict:
    """
    获取城市坐标信息。

    Args:
        city: 城市名称

    Returns:
        包含 latitude, longitude, country, name 的字典

    Raises:
        ValueError: 找不到城市时抛出
    """
    logger.debug(f"查询城市坐标: {city}")
    
    url = f"https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}
    
    try:
        logger.debug(f"API请求: {url}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            logger.warning(f"找不到城市: {city}")
            raise ValueError(f"找不到城市: {city}")
        
        result = data["results"][0]
        city_info = {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "country": result.get("country", "未知"),
            "name": result.get("name", city),
        }
        
        logger.debug(f"城市信息: {city_info}")
        return city_info
        
    except requests.exceptions.RequestException as e:
        logger.error(f"网络请求失败: {e}")
        raise ValueError(f"网络请求失败: {e}")


def get_weather(lat: float, lon: float) -> Dict:
    """
    获取当前天气数据。

    Args:
        lat: 纬度
        lon: 经度

    Returns:
        天气数据字典，包含 temperature, weather_code, time
    """
    logger.debug(f"获取天气: lat={lat}, lon={lon}")
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,weather_code"
    )
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        weather_data = {
            "temperature": current.get("temperature_2m"),
            "weather_code": current.get("weather_code"),
            "time": current.get("time"),
        }
        
        logger.debug(f"天气数据: {weather_data}")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"获取天气失败: {e}")
        raise ValueError(f"获取天气失败: {e}")


def get_forecast(lat: float, lon: float, days: int = 3) -> list:
    """
    获取未来天气预报。

    Args:
        lat: 纬度
        lon: 经度
        days: 预报天数，默认 3 天

    Returns:
        预报数据列表
    """
    logger.debug(f"获取预报: lat={lat}, lon={lon}, days={days}")
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=temperature_2m_max,temperature_2m_min,weather_code&"
        f"forecast_days={days}"
    )
    
    try:
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
        
        logger.debug(f"预报数据: {len(forecasts)} 条")
        return forecasts
        
    except requests.exceptions.RequestException as e:
        logger.error(f"获取预报失败: {e}")
        raise ValueError(f"获取预报失败: {e}")


def parse_weather_code(code: int) -> str:
    """
    将 WMO 天气代码转换为中文描述。

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
