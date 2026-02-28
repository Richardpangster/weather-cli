"""
配置文件管理模块

负责加载、保存、获取和设置天气查询工具的配置项。
配置文件位置: ~/.weather-cli/config.json
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)

# 配置文件路径
CONFIG_DIR = Path.home() / ".weather-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 默认配置
DEFAULT_CONFIG: Dict[str, Any] = {
    "default_city": "",
    "default_format": "text",
    "forecast_days": 3,
}

# 合法的配置键及其类型
VALID_CONFIG_KEYS: Dict[str, type] = {
    "default_city": str,
    "default_format": str,
    "forecast_days": int,
}

# 合法的配置值约束
CONFIG_CONSTRAINTS: Dict[str, Any] = {
    "default_format": ["text", "json"],
    "forecast_days": range(1, 8),  # 1-7
}


def load_config() -> Dict[str, Any]:
    """
    加载配置文件。

    如果配置文件不存在，则自动创建并写入默认配置。

    Returns:
        Dict[str, Any]: 配置字典，包含所有配置项。

    Raises:
        json.JSONDecodeError: 配置文件格式错误时抛出。
    """
    if not CONFIG_FILE.exists():
        logger.info("配置文件不存在，创建默认配置: %s", CONFIG_FILE)
        save_config(DEFAULT_CONFIG.copy())
        return DEFAULT_CONFIG.copy()

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # 合并默认配置，确保所有键都存在
        config = DEFAULT_CONFIG.copy()
        config.update(data)
        return config
    except json.JSONDecodeError as e:
        logger.error("配置文件格式错误: %s", e)
        raise
    except OSError as e:
        logger.error("读取配置文件失败: %s", e)
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """
    保存配置到文件。

    如果配置目录不存在，则自动创建。

    Args:
        config (Dict[str, Any]): 要保存的配置字典。

    Raises:
        OSError: 写入文件失败时抛出。
    """
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        logger.info("配置已保存到: %s", CONFIG_FILE)
    except OSError as e:
        logger.error("保存配置文件失败: %s", e)
        raise


def get_config(key: str, default: Optional[Any] = None) -> Any:
    """
    获取指定配置项的值。

    Args:
        key (str): 配置项的键名。
        default (Optional[Any]): 键不存在时返回的默认值，默认为 None。

    Returns:
        Any: 配置项的值，若不存在则返回 default。
    """
    config = load_config()
    return config.get(key, default)


def set_config(key: str, value: Union[str, int, float]) -> None:
    """
    设置指定配置项的值并保存。

    Args:
        key (str): 配置项的键名。
        value (Union[str, int, float]): 要设置的值（字符串形式，会自动转换类型）。

    Raises:
        ValueError: 键名不合法或值不符合约束时抛出。
    """
    if key not in VALID_CONFIG_KEYS:
        raise ValueError(
            f"不支持的配置项: '{key}'。合法的配置项: {list(VALID_CONFIG_KEYS.keys())}"
        )

    # 类型转换
    expected_type = VALID_CONFIG_KEYS[key]
    try:
        typed_value: Any = expected_type(value)
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"配置项 '{key}' 的值类型错误，期望 {expected_type.__name__}: {e}"
        ) from e

    # 值约束检查
    if key in CONFIG_CONSTRAINTS:
        constraint = CONFIG_CONSTRAINTS[key]
        if typed_value not in constraint:
            raise ValueError(
                f"配置项 '{key}' 的值 '{typed_value}' 不合法。"
                f"合法值: {list(constraint)}"
            )

    config = load_config()
    config[key] = typed_value
    save_config(config)
    logger.info("配置项 '%s' 已设置为: %s", key, typed_value)


def reset_config() -> None:
    """
    重置配置文件为默认值。

    将所有配置项恢复为默认值并保存。
    """
    save_config(DEFAULT_CONFIG.copy())
    logger.info("配置已重置为默认值")


def show_config() -> str:
    """
    获取当前配置的可读字符串表示。

    Returns:
        str: 格式化后的配置信息字符串。
    """
    config = load_config()
    lines = [f"配置文件路径: {CONFIG_FILE}", "当前配置:"]
    for key, val in config.items():
        display_val = f'"{val}"' if isinstance(val, str) else str(val)
        lines.append(f"  {key} = {display_val}")
    return "\n".join(lines)


def parse_config_assignment(assignment: str) -> tuple[str, str]:
    """
    解析 'key=value' 格式的配置赋值字符串。

    Args:
        assignment (str): 形如 'key=value' 的字符串。

    Returns:
        tuple[str, str]: (key, value) 元组。

    Raises:
        ValueError: 格式不正确时抛出。
    """
    if "=" not in assignment:
        raise ValueError(
            f"配置格式错误: '{assignment}'。正确格式: key=value，例如: default_city=Beijing"
        )
    key, _, value = assignment.partition("=")
    key = key.strip()
    value = value.strip()
    if not key:
        raise ValueError(f"配置键名不能为空: '{assignment}'")
    return key, value