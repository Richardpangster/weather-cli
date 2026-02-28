#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weather CLI - 命令行天气查询工具
"""
import sys
import io
from weather import get_coordinates, get_weather, parse_weather_code

# 修复 Windows 终端中文编码问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("用法: python cli.py <城市名称>")
        print("示例: python cli.py Beijing")
        sys.exit(1)

    city = sys.argv[1]

    try:
        # 获取城市坐标
        lat, lon = get_coordinates(city)

        # 获取天气数据
        weather_data = get_weather(lat, lon)

        # 解析天气代码
        weather_desc = parse_weather_code(weather_data["weather_code"])

        # 输出结果
        print(f"\n城市: {city}")
        print(f"坐标: {lat:.2f}, {lon:.2f}")
        print(f"温度: {weather_data['temperature']}°C")
        print(f"天气: {weather_desc}\n")

    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"请求失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
