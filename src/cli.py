#!/usr/bin/env python3
"""
Weather CLI - 命令行天气查询工具
支持查询当前天气、天气预报，以及管理配置文件和日志。
"""
import argparse
import sys
from typing import Optional

# 导入配置模块
from config import (
    get_config,
    load_config,
    reset_config,
    set_config,
    show_config,
)

# 导入日志模块
from logger import setup_logger, LOG_FILE

# 导入天气模块
from weather import (
    get_coordinates,
    get_weather,
    get_forecast,
    parse_weather_code,
)

# 导入格式化模块
from formatter import (
    format_text_current,
    format_text_forecast,
    format_json,
)


def build_parser() -> argparse.ArgumentParser:
    """
    构建命令行参数解析器。

    Returns:
        argparse.ArgumentParser: 配置好的参数解析器。
    """
    # 加载配置获取默认值
    config = load_config()
    default_city: str = config.get("default_city", "")
    default_format: str = config.get("default_format", "text")

    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="天气查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "city",
        nargs="?",
        default=default_city,
        help="要查询的城市名称",
    )
    parser.add_argument(
        "-f", "--forecast",
        action="store_true",
        help="显示未来 3 天预报",
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="以 JSON 格式输出",
    )
    
    # 日志级别控制
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细日志 (DEBUG级别)",
    )
    log_group.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="只显示警告和错误",
    )
    
    # 配置命令
    parser.add_argument(
        "--config",
        metavar="KEY=VALUE",
        help="设置配置项",
    )
    parser.add_argument(
        "--config-show",
        action="store_true",
        help="显示当前配置",
    )
    parser.add_argument(
        "--config-reset",
        action="store_true",
        help="重置配置为默认值",
    )

    return parser


def run_config_command(args: argparse.Namespace) -> int:
    """
    处理配置相关命令。

    Args:
        args: 命令行参数。

    Returns:
        int: 退出码，0 表示成功。
    """
    if args.config_reset:
        reset_config()
        print("配置已重置为默认值")
        return 0

    if args.config_show:
        show_config()
        return 0

    if args.config:
        try:
            key, value = args.config.split("=", 1)
            set_config(key.strip(), value.strip())
            print(f"配置已更新: {key} = {value}")
            return 0
        except ValueError:
            print("错误: 配置格式应为 KEY=VALUE")
            return 1

    return -1  # 不是配置命令


def run_weather_query(args: argparse.Namespace) -> int:
    """
    执行天气查询。

    Args:
        args: 命令行参数。

    Returns:
        int: 退出码，0 表示成功。
    """
    city = args.city
    if not city:
        print("错误: 请指定城市名称")
        return 1

    # 获取日志记录器
    logger = setup_logger()
    logger.info(f"查询城市: {city}")

    try:
        # 获取城市坐标
        logger.debug(f"正在获取 {city} 的坐标")
        city_info = get_coordinates(city)
        lat = city_info["latitude"]
        lon = city_info["longitude"]
        city_name = city_info["name"]
        country = city_info["country"]
        
        logger.debug(f"坐标: {lat}, {lon}")

        # 获取当前天气
        logger.debug("正在获取天气数据")
        current = get_weather(lat, lon)
        logger.debug(f"天气数据: {current}")

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
        
        logger.info(f"查询完成: {city_name}")
        return 0

    except ValueError as e:
        logger.error(f"查询失败: {e}")
        print(f"错误: {e}")
        return 1
    except Exception as e:
        logger.exception(f"请求失败: {e}")
        print(f"请求失败: {e}")
        return 1


def main() -> int:
    """
    主入口函数。

    Returns:
        int: 程序退出码。
    """
    parser = build_parser()
    args = parser.parse_args()

    # 设置日志级别
    if args.verbose:
        setup_logger(level=10)  # DEBUG
    elif args.quiet:
        setup_logger(level=30)  # WARNING
    else:
        setup_logger(level=20)  # INFO

    # 处理配置命令
    config_result = run_config_command(args)
    if config_result >= 0:
        return config_result

    # 执行天气查询
    return run_weather_query(args)


if __name__ == "__main__":
    sys.exit(main())
