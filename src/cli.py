#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weather CLI - 命令行天气查询工具
"""
import sys
import io
import argparse
from weather import get_coordinates, get_weather, get_forecast
from formatter import (
    format_text_current,
    format_text_forecast,
    format_json,
    format_error_json,
)

# 修复 Windows 终端中文编码问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="天气查询工具 - 查询全球城市当前天气和预报",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py Beijing              查询北京当前天气
  python cli.py Beijing -f           查询北京天气预报
  python cli.py Beijing --json       以 JSON 格式输出
  python cli.py "New York" -f -j     查询纽约预报，JSON 格式
        """,
    )

    parser.add_argument(
        "city",
        help="要查询的城市名称（如：Beijing, Shanghai, \"New York\"）"
    )
    parser.add_argument(
        "-f", "--forecast",
        action="store_true",
        help="显示未来 3 天预报"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="以 JSON 格式输出"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        # 获取城市信息
        city_info = get_coordinates(args.city)
        lat = city_info["latitude"]
        lon = city_info["longitude"]
        city_name = city_info["name"]
        country = city_info["country"]

        # 获取当前天气
        current = get_weather(lat, lon)

        # 根据参数输出
        if args.json:
            if args.forecast:
                forecasts = get_forecast(lat, lon)
                print(format_json(city_name, country, lat, lon, current, forecasts))
            else:
                print(format_json(city_name, country, lat, lon, current))
        else:
            if args.forecast:
                forecasts = get_forecast(lat, lon)
                print(format_text_forecast(
                    city_name, country, lat, lon, current, forecasts
                ))
            else:
                print(format_text_current(city_name, country, lat, lon, current))

    except ValueError as e:
        if args.json:
            print(format_error_json(str(e)))
        else:
            print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(format_error_json(f"请求失败: {e}"))
        else:
            print(f"请求失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
