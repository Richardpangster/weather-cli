# 天气查询工具 - 架构设计

## 📋 项目概述

一个命令行天气查询工具，支持查询全球城市天气信息。

## 🎯 功能需求

### 核心功能
1. **查询当前天气** - 输入城市名，返回温度、天气状况
2. **查询未来预报** - 支持 3 天天气预报
3. **多种输出格式** - 支持文本、JSON 格式
4. **配置管理** - 支持设置默认城市

### 命令示例
```bash
# 查询当前天气
weather Beijing
weather "New York"

# 查询预报
weather Beijing --forecast

# JSON 输出
weather Beijing --json

# 设置默认城市
weather --config default_city=Beijing
```

## 🏗️ 技术架构

### 技术栈
- **语言**: Python 3.10+
- **依赖管理**: pip + requirements.txt
- **API**: Open-Meteo (免费，无需 API Key)
- **CLI 框架**: argparse (标准库)

### 项目结构
```
weather-cli/
├── src/
│   ├── __init__.py
│   ├── cli.py          # 命令行入口
│   ├── weather.py      # 天气查询逻辑
│   ├── formatter.py    # 输出格式化
│   └── config.py       # 配置管理
├── tests/
│   └── test_weather.py
├── requirements.txt
├── setup.py
└── README.md
```

### 模块职责

#### 1. cli.py - 命令行入口
- 解析命令行参数
- 调用 weather 模块查询
- 输出结果

#### 2. weather.py - 核心逻辑
- 调用 Open-Meteo API
- 处理响应数据
- 错误处理

#### 3. formatter.py - 格式化输出
- 文本格式（表格/列表）
- JSON 格式

#### 4. config.py - 配置管理
- 读取/写入配置文件
- 默认城市设置

## 🔌 API 设计

### 天气 API
- **服务**: Open-Meteo (https://open-meteo.com/)
- **优点**: 免费、无需注册、支持全球

### 主要接口
```python
GET https://api.open-meteo.com/v1/forecast
    ?latitude={lat}
    &longitude={lon}
    &current=temperature_2m,weather_code
    &daily=temperature_2m_max,temperature_2m_min
```

### 地理编码
```python
GET https://geocoding-api.open-meteo.com/v1/search
    ?name={city_name}
    &count=1
```

## 📊 数据结构

### 天气响应
```python
{
    "city": "Beijing",
    "country": "China",
    "current": {
        "temperature": 25,
        "weather": "晴朗",
        "time": "2026-02-28 14:00"
    },
    "forecast": [
        {
            "date": "2026-03-01",
            "max_temp": 26,
            "min_temp": 15,
            "weather": "多云"
        }
    ]
}
```

## 🚀 实现步骤

### Phase 1: 基础功能 (MVP)
1. [ ] 创建项目结构
2. [ ] 实现地理编码（城市名 → 经纬度）
3. [ ] 实现当前天气查询
4. [ ] 实现文本格式输出
5. [ ] 添加错误处理

### Phase 2: 增强功能
1. [ ] 实现天气预报功能
2. [ ] 实现 JSON 格式输出
3. [ ] 添加配置管理
4. [ ] 添加单元测试

### Phase 3: 完善
1. [ ] 添加更多输出格式（CSV、Markdown）
2. [ ] 支持多语言
3. [ ] 添加缓存机制

## 📝 开发规范

### 代码风格
- 遵循 PEP 8
- 使用类型注解
- 函数必须有 docstring

### 测试要求
- 核心函数必须有单元测试
- 使用 pytest 框架
- 覆盖率 > 80%

### 提交规范
```
feat: 添加城市查询功能
fix: 修复温度显示错误
docs: 更新 README
test: 添加天气查询测试
```

## ✅ 验收标准

- [ ] 可以查询任意城市的当前天气
- [ ] 温度显示准确
- [ ] 错误提示友好（城市不存在、网络错误等）
- [ ] 代码有测试覆盖
- [ ] README 包含安装和使用说明

---

**设计者**: 全球虾 🦐  
**日期**: 2026-02-28  
**版本**: v1.0
