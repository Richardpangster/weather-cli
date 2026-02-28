"""
天气查询命令行工具入口

支持查询当前天气、天气预报，以及管理配置文件。
"""

import argparse
import json
import sys
from typing import Optional

# 尝试导入配置模块
try:
    from config import (
        get_config,
        load_config,
        parse_config_assignment,
        reset_config,
        set_config,
        show_config,
    )
except ImportError:
    # 兼容直接运行和作为模块运行
    from src.config import (  # type: ignore[no-redef]
        get_config,
        load_config,
        parse_config_assignment,
        reset_config,
        set_config,
        show_config,
    )


def build_parser() -> argparse.ArgumentParser:
    """
    构建命令行参数解析器。

    Returns:
        argparse.ArgumentParser: 配置好的参数解析器。
    """
    # 从配置文件读取默认值
    default_city: str = get_config("default_city", "")
    default_format: str = get_config("default_format", "text")
    forecast_days: int = get_config("forecast_days", 3)

    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="🌤  天气查询命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python src/cli.py Beijing                        # 查询北京天气
  python src/cli.py --forecast 5 Shanghai          # 查询上海5天预报
  python src/cli.py --format json Tokyo            # JSON格式输出
  python src/cli.py --config default_city=Beijing  # 设置默认城市
  python src/cli.py --config-show                  # 查看当前配置
  python src/cli.py --config-reset                 # 重置配置
        """,
    )

    # ── 天气查询参数 ──────────────────────────────────────────────
    parser.add_argument(
        "city",
        nargs="?",
        default=default_city if default_city else None,
        help=f"要查询的城市名称（默认: {default_city or '无'}）",
    )

    parser.add_argument(
        "--forecast",
        "-f",
        type=int,
        metavar="DAYS",
        default=None,
        help=f"查询未来 N 天的天气预报（1-7，配置默认: {forecast_days}）",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default=default_format,
        dest="output_format",
        help=f"输出格式（默认: {default_format}）",
    )

    # ── 配置管理参数 ──────────────────────────────────────────────
    config_group = parser.add_argument_group("配置管理")

    config_group.add_argument(
        "--config",
        metavar="KEY=VALUE",
        help="设置配置项，例如: --config default_city=Beijing",
    )

    config_group.add_argument(
        "--config-show",
        action="store_true",
        default=False,
        help="显示当前所有配置项",
    )

    config_group.add_argument(
        "--config-reset",
        action="store_true",
        default=False,
        help="重置配置文件为默认值",
    )

    return parser


def handle_config_commands(args: argparse.Namespace) -> bool:
    """
    处理配置相关命令。

    Args:
        args (argparse.Namespace): 解析后的命令行参数。

    Returns:
        bool: 如果处理了配置命令则返回 True，否则返回 False。
    """
    if args.config_show:
        print(show_config())
        return True

    if args.config_reset:
        reset_config()
        print("✅ 配置已重置为默认值。")
        print(show_config())
        return True

    if args.config:
        try:
            key, value = parse_config_assignment(args.config)
            set_config(key, value)
            print(f"✅ 配置项 '{key}' 已设置为: {value!r}")
        except ValueError as e:
            print(f"❌ 配置错误: {e}", file=sys.stderr)
            sys.exit(1)
        return True

    return False


def format_weather_text(city: str, weather_data: dict) -> str:
    """
    将天气数据格式化为可读文本。

    Args:
        city (str): 城市名称。
        weather_data (dict): 天气数据字典。

    Returns:
        str: 格式化后的天气信息字符串。
    """
    lines = [
        f"🌍 城市: {city}",
        f"🌡  温度: {weather_data.get('temperature', 'N/A')}°C",
        f"💧 湿度: {weather_data.get('humidity', 'N/A')}%",
        f"🌬  风速: {weather_data.get('wind_speed', 'N/A')} km/h",
        f"☁  天气: {weather_data.get('description', 'N/A')}",
    ]
    return "\n".join(lines)


def format_forecast_text(city: str, forecast_list: list) -> str:
    """
    将预报数据格式化为可读文本。

    Args:
        city (str): 城市名称。
        forecast_list (list): 预报数据列表，每项为一天的天气字典。

    Returns:
        str: 格式化后的预报信息字符串。
    """
    lines = [f"🌍 城市: {city} — {len(forecast_list)} 天天气预报", "─" * 40]
    for i, day in enumerate(forecast_list, start=1):
        lines.append(
            f"第 {i} 天 | {day.get('date', 'N/A')} | "
            f"{day.get('description', 'N/A')} | "
            f"{day.get('temp_min', 'N/A')}~{day.get('temp_max', 'N/A')}°C"
        )
    return "\n".join(lines)


def mock_get_weather(city: str) -> dict:
    """
    模拟获取当前天气数据（占位实现）。

    Args:
        city (str): 城市名称。

    Returns:
        dict: 模拟的天气数据。
    """
    # 实际项目中应调用真实天气 API
    return {
        "city": city,
        "temperature": 22,
        "humidity": 65,
        "wind_speed": 15,
        "description": "晴转多云",
    }


def mock_get_forecast(city: str, days: int) -> list:
    """
    模拟获取天气预报数据（占位实现）。

    Args:
        city (str): 城市名称。
        days (int): 预报天数。

    Returns:
        list: 模拟的预报数据列表。
    """
    # 实际项目中应调用真实天气 API
    from datetime import date, timedelta

    forecast = []
    today = date.today()
    descriptions = ["晴", "多云", "小雨", "阴", "大风", "雷阵雨", "雪"]
    for i in range(days):
        forecast.append(
            {
                "date": str(today + timedelta(days=i)),
                "description": descriptions[i % len(descriptions)],
                "temp_min": 15 + i,
                "temp_max": 25 + i,
            }
        )
    return forecast


def run_weather_query(args: argparse.Namespace) -> None: