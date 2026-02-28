"""
日志配置模块

提供统一的日志配置，支持控制台彩色输出和文件记录。
"""

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

# 日志目录和文件
LOG_DIR = Path.home() / ".weather-cli"
LOG_FILE = LOG_DIR / "weather.log"

# 日志格式
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ColoredFormatter(logging.Formatter):
    """
    彩色日志格式化器
    
    为不同级别的日志添加颜色。
    """
    
    # ANSI 颜色码
    COLORS = {
        'DEBUG': '\033[36m',     # 青色
        'INFO': '\033[32m',      # 绿色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',     # 红色
        'CRITICAL': '\033[35m',  # 紫色
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录，添加颜色"""
        # 保存原始级别名称
        orig_levelname = record.levelname
        
        # 添加颜色
        if record.levelname in self.COLORS:
            colored_level = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            record.levelname = colored_level
        
        # 格式化
        result = super().format(record)
        
        # 恢复原始级别名称
        record.levelname = orig_levelname
        
        return result


def setup_logger(
    level: int = logging.INFO,
    log_to_file: bool = True,
    use_color: bool = True
) -> logging.Logger:
    """
    配置并返回日志记录器
    
    Args:
        level: 日志级别，默认为 INFO
        log_to_file: 是否记录到文件，默认为 True
        use_color: 是否使用彩色输出，默认为 True
    
    Returns:
        配置好的日志记录器
    """
    # 创建日志目录
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 获取或创建日志记录器
    logger = logging.getLogger("weather-cli")
    logger.setLevel(level)
    
    # 清除已有处理器
    logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    if use_color:
        console_formatter = ColoredFormatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    else:
        console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（支持轮转）
    if log_to_file:
        file_handler = TimedRotatingFileHandler(
            LOG_FILE,
            when="midnight",  # 每天轮转
            interval=1,
            backupCount=7,     # 保留7天
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别
        file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger() -> logging.Logger:
    """
    获取默认日志记录器
    
    Returns:
        默认配置的日志记录器
    """
    return logging.getLogger("weather-cli")
