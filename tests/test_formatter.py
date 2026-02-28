import pytest
from src.formatter import format_text_current, format_json

def test_format_text_current():
    """测试当前天气文本格式"""
    result = format_text_current(
        "Beijing", "China", 39.9, 116.4,
        {"temperature": 25, "weather_code": 0}
    )
    assert "Beijing" in result
    assert "25°C" in result

def test_format_json():
    """测试 JSON 格式输出"""
    result = format_json(
        "Beijing", "China", 39.9, 116.4,
        {"temperature": 25, "weather_code": 0}
    )
    assert '"city": "Beijing"' in result
    assert '"temperature": 25' in result