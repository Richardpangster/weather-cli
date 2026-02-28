# Task 002: 添加天气预报和 JSON 输出功能

## 🎯 任务目标

在基础天气查询功能上，添加天气预报和多种输出格式支持。

## 📋 具体需求

### 功能 1: 未来天气预报

**命令格式**:
```bash
python src/cli.py Beijing --forecast
# 或
python src/cli.py Beijing -f
```

**输出示例**:
```
城市: Beijing

当前天气:
  温度: 25°C
  天气: 晴朗

未来 3 天预报:
  2026-03-01: 22°C ~ 28°C, 多云
  2026-03-02: 20°C ~ 25°C, 小雨
  2026-03-03: 18°C ~ 23°C, 晴朗
```

**API 参考**:
```
https://api.open-meteo.com/v1/forecast?
    latitude={lat}&longitude={lon}
    &daily=temperature_2m_max,temperature_2m_min,weather_code
    &forecast_days=3
```

---

### 功能 2: JSON 格式输出

**命令格式**:
```bash
python src/cli.py Beijing --json
python src/cli.py Beijing --forecast --json
```

**输出示例**:
```json
{
  "city": "Beijing",
  "country": "China",
  "current": {
    "temperature": 25,
    "weather": "晴朗",
    "weather_code": 0,
    "time": "2026-02-28T14:00"
  },
  "forecast": [
    {
      "date": "2026-03-01",
      "max_temp": 28,
      "min_temp": 22,
      "weather": "多云",
      "weather_code": 2
    }
  ]
}
```

---

### 功能 3: 帮助信息

**命令格式**:
```bash
python src/cli.py --help
python src/cli.py -h
```

**输出示例**:
```
用法: cli.py [选项] <城市名称>

位置参数:
  city          要查询的城市名称（如：Beijing, Shanghai）

可选参数:
  -h, --help    显示帮助信息
  -f, --forecast  显示未来 3 天预报
  -j, --json    以 JSON 格式输出

示例:
  python cli.py Beijing              查询北京当前天气
  python cli.py Beijing -f           查询北京天气预报
  python cli.py Beijing --json       以 JSON 格式输出
  python cli.py "New York" -f -j     查询纽约预报，JSON 格式
```

---

## 🔧 技术要点

### 需要修改的模块

#### 1. 修改 src/weather.py

添加新函数:
```python
def get_forecast(lat: float, lon: float, days: int = 3) -> list[dict]:
    """
    获取未来天气预报
    
    Args:
        lat: 纬度
        lon: 经度
        days: 预报天数（默认 3 天）
    
    Returns:
        预报数据列表，每项包含 date, max_temp, min_temp, weather_code
    """
    pass
```

#### 2. 修改 src/cli.py

使用 `argparse` 替代 `sys.argv`:
```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='天气查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python cli.py Beijing              查询北京当前天气
  python cli.py Beijing -f           查询北京天气预报
  python cli.py Beijing --json       以 JSON 格式输出
        '''
    )
    
    parser.add_argument('city', help='城市名称')
    parser.add_argument('-f', '--forecast', action='store_true', 
                       help='显示未来 3 天预报')
    parser.add_argument('-j', '--json', action='store_true',
                       help='以 JSON 格式输出')
    
    args = parser.parse_args()
    # ... 处理逻辑
```

#### 3. 创建 src/formatter.py（可选，推荐）

将格式化逻辑分离:
```python
import json

def format_text_current(city: str, country: str, weather: dict) -> str:
    """格式化当前天气为文本"""
    pass

def format_text_forecast(city: str, forecasts: list[dict]) -> str:
    """格式化预报为文本"""
    pass

def format_json(city: str, country: str, current: dict, 
                forecast: list[dict] | None) -> str:
    """格式化为 JSON"""
    pass
```

---

## 📝 开发规范

1. **保持代码风格一致** - 参考已有的 weather.py 和 cli.py
2. **添加类型注解** - 所有函数参数和返回值都要有类型提示
3. **编写 docstring** - 函数必须有文档字符串
4. **错误处理** - 网络错误、API 错误要有友好提示
5. **测试** - 在本地测试所有命令组合

---

## ✅ 验收标准

- [ ] `--forecast` 参数可以显示 3 天预报
- [ ] `--json` 参数可以输出 JSON 格式
- [ ] `--help` 显示完整的帮助信息
- [ ] 可以同时使用 `-f` 和 `-j`（预报 + JSON）
- [ ] 城市不存在时显示友好的 JSON 错误信息（使用 `--json` 时）
- [ ] 代码通过代码审查

---

## 🚀 提交要求

1. 修改 `src/weather.py` - 添加 `get_forecast()` 函数
2. 修改 `src/cli.py` - 使用 argparse，支持新参数
3. 创建 `src/formatter.py` - 格式化输出（可选）
4. 更新 `README.md` - 添加新功能的使用说明
5. 测试所有功能后提交到 Git
6. 提交信息示例: `feat: 添加天气预报和 JSON 输出功能`

---

## 💡 提示

- 先实现 `--forecast`，再实现 `--json`
- `argparse` 文档: https://docs.python.org/3/library/argparse.html
- 可以用 `python cli.py --help` 测试帮助信息
- JSON 输出用 `json.dumps(data, ensure_ascii=False, indent=2)`

---

**任务创建**: 全球虾 🦐  
**优先级**: P1  
**预计时间**: 45-90 分钟  
**依赖**: Task 001 ✅ 已完成
