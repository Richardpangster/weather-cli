# Weather CLI 实施计划

## 概述
根据 Task 001 实现基础天气查询功能。

## 执行步骤

### Step 0: 保存计划文件
在项目根目录创建 `plan.md` 作为开发指南。

### Step 1: 创建项目结构
```
weather-cli/
├── src/
│   ├── __init__.py
│   ├── weather.py
│   └── cli.py
└── requirements.txt
```

### Step 2: 创建 requirements.txt
```
requests>=2.28.0
```

### Step 3: 实现 src/weather.py
核心函数：
- `get_coordinates(city)` - 获取城市经纬度
- `get_weather(lat, lon)` - 获取天气数据
- `parse_weather_code(code)` - 天气代码转中文

### Step 4: 实现 src/cli.py
- 解析命令行参数
- 调用天气模块
- 格式化输出
- 错误处理

## API
- 地理编码: `https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1`
- 天气: `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code`

## 验证
```bash
pip install -r requirements.txt
python src/cli.py Beijing
python src/cli.py Shanghai
python src/cli.py "New York"
```
