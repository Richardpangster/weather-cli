import pytest
from src.weather import parse_weather_code, get_coordinates

def test_parse_weather_code_sunny():
    """测试晴朗天气代码"""
    assert parse_weather_code(0) == "晴朗"

def test_parse_weather_code_cloudy():
    """测试多云天气代码"""
    assert parse_weather_code(2) == "多云"

def test_parse_weather_code_rain():
    """测试雨天天气代码"""
    assert parse_weather_code(61) == "小雨"

def test_parse_weather_code_unknown():
    """测试未知天气代码"""
    assert "未知" in parse_weather_code(999)