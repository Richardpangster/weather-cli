```python
"""
日志模块测试
"""

import logging
import os
import tempfile
from unittest.mock import patch

import pytest

from src.logger import setup_logger, get_logger, ColoredFormatter


class TestSetupLogger:
    """测试 setup_logger 函数"""

    def test_returns_logger(self):
        """测试返回日志记录器"""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logger(
                name="test_logger_1",
                level=logging.INFO,
                log_dir=tmpdir,
            )
            assert isinstance(logger, logging.Logger)

    def test_logger_level(self):
        """测试日志级别设置"""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logger(
                name="test_logger_2",
                level=logging.DEBUG,
                log_dir=tmpdir,
            )
            assert logger.level == logging.DEBUG

    def test_creates_log_file(self):
        """测试创建日志文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            setup_logger(
                name="test_logger_3",
                level=logging.INFO,
                log_dir=tmpdir,
            )
            log_file = os.path.join(tmpdir, "weather.log")
            assert os.path.exists(log_file)

    def test_has_two_handlers(self):
        """测试有两个处理器（控制台和文件）"""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logger(
                name="test_logger_4",
                level=logging.INFO,
                log_dir=tmpdir,
            )
            assert len(logger.handlers) == 2

    def test_