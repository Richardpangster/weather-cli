# Task 003: 添加单元测试

## 🎯 任务目标

为天气查询工具添加单元测试，确保核心功能稳定可靠。

## 📋 具体需求

### 需要测试的模块

1. **test_weather.py** - 测试 weather.py
   - `get_coordinates()` - 测试城市查询
   - `get_weather()` - 测试天气获取
   - `get_forecast()` - 测试预报获取
   - `parse_weather_code()` - 测试天气代码解析

2. **test_formatter.py** - 测试 formatter.py
   - `format_text_current()` - 测试当前天气文本格式
   - `format_text_forecast()` - 测试预报文本格式
   - `format_json()` - 测试 JSON 格式

### 测试框架

使用 `pytest`：
```bash
pip install pytest pytest-mock
```

### 测试文件结构

```
tests/
├── __init__.py
├── test_weather.py
└── test_formatter.py
```

### 示例测试代码

```python
# tests/test_weather.py
import pytest
from src.weather import parse_weather_code, get_coordinates

def test_parse_weather_code():
    """测试天气代码解析"""
    assert parse_weather_code(0) == "晴朗"
    assert parse_weather_code(1) == "基本晴朗"
    assert parse_weather_code(95) == "雷暴"
    assert parse_weather_code(999) == "未知天气代码(999)"

def test_get_coordinates_mock(mocker):
    """测试城市查询（使用 mock）"""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "results": [{
            "latitude": 39.9042,
            "longitude": 116.4074,
            "country": "China",
            "name": "Beijing"
        }]
    }
    mocker.patch('requests.get', return_value=mock_response)
    
    result = get_coordinates("Beijing")
    assert result["latitude"] == 39.9042
    assert result["country"] == "China"
```

## 🔧 技术要求

1. 使用 `pytest` 框架
2. 使用 `pytest-mock` 来 mock API 调用（避免真实网络请求）
3. 测试覆盖率 > 80%
4. 所有测试用例必须通过

## 📝 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_weather.py

# 显示覆盖率
pytest tests/ --cov=src --cov-report=html
```

## ✅ 验收标准

- [ ] `tests/` 目录创建
- [ ] `test_weather.py` 包含至少 4 个测试函数
- [ ] `test_formatter.py` 包含至少 3 个测试函数
- [ ] 所有测试通过 (`pytest` 显示绿色)
- [ ] 更新 `requirements.txt` 添加测试依赖
- [ ] 更新 `README.md` 添加测试说明

## 🚀 提交要求

1. 创建 `tests/` 目录和所有测试文件
2. 确保所有测试通过
3. 提交信息: `test: 添加单元测试`

---

**任务创建**: 全球虾 🦐  
**优先级**: P2  
**预计时间**: 30-45 分钟  
**状态**: 🆕 待处理
