"""
输出格式化模块
"""
import json
from weather import parse_weather_code


def format_text_current(
    city: str, country: str, lat: float, lon: float, weather: dict
) -> str:
    """
    格式化当前天气为文本

    Args:
        city: 城市名称
        country: 国家名称
        lat: 纬度
        lon: 经度
        weather: 当前天气数据

    Returns:
        格式化的文本输出
    """
    weather_desc = parse_weather_code(weather["weather_code"])
    lines = [
        f"\n城市: {city} ({country})",
        f"坐标: {lat:.2f}, {lon:.2f}",
        "",
        "当前天气:",
        f"  温度: {weather['temperature']}°C",
        f"  天气: {weather_desc}",
        "",
    ]
    return "\n".join(lines)


def format_text_forecast(
    city: str, country: str, lat: float, lon: float,
    current: dict, forecasts: list[dict]
) -> str:
    """
    格式化天气预报为文本

    Args:
        city: 城市名称
        country: 国家名称
        lat: 纬度
        lon: 经度
        current: 当前天气数据
        forecasts: 预报数据列表

    Returns:
        格式化的文本输出
    """
    current_desc = parse_weather_code(current["weather_code"])
    lines = [
        f"\n城市: {city} ({country})",
        "",
        "当前天气:",
        f"  温度: {current['temperature']}°C",
        f"  天气: {current_desc}",
        "",
        "未来 3 天预报:",
    ]

    for f in forecasts:
        weather_desc = parse_weather_code(f["weather_code"])
        lines.append(
            f"  {f['date']}: {f['min_temp']}°C ~ {f['max_temp']}°C, {weather_desc}"
        )

    lines.append("")
    return "\n".join(lines)


def format_json(
    city: str,
    country: str,
    lat: float,
    lon: float,
    current: dict,
    forecasts: list[dict] | None = None,
) -> str:
    """
    格式化为 JSON

    Args:
        city: 城市名称
        country: 国家名称
        lat: 纬度
        lon: 经度
        current: 当前天气数据
        forecasts: 预报数据列表（可选）

    Returns:
        格式化的 JSON 字符串
    """
    data = {
        "city": city,
        "country": country,
        "coordinates": {
            "latitude": lat,
            "longitude": lon,
        },
        "current": {
            "temperature": current["temperature"],
            "weather": parse_weather_code(current["weather_code"]),
            "weather_code": current["weather_code"],
            "time": current.get("time"),
        },
    }

    if forecasts:
        data["forecast"] = [
            {
                "date": f["date"],
                "max_temp": f["max_temp"],
                "min_temp": f["min_temp"],
                "weather": parse_weather_code(f["weather_code"]),
                "weather_code": f["weather_code"],
            }
            for f in forecasts
        ]

    return json.dumps(data, ensure_ascii=False, indent=2)


def format_error_json(message: str) -> str:
    """
    格式化错误信息为 JSON

    Args:
        message: 错误信息

    Returns:
        格式化的 JSON 字符串
    """
    return json.dumps({"error": message}, ensure_ascii=False, indent=2)
