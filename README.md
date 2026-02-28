# Weather CLI

命令行天气查询工具，支持查询全球城市当前天气和未来预报。

## 📋 项目结构

```
weather-cli/
├── docs/               # 设计文档
│   └── architecture.md # 架构设计
├── tasks/              # 任务列表
├── reviews/            # 代码审查
├── src/                # 源代码
│   ├── weather.py      # 天气 API 模块
│   ├── formatter.py    # 输出格式化模块
│   └── cli.py          # 命令行入口
└── README.md
```

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Richardpangster/weather-cli.git
cd weather-cli

# 安装依赖
pip install -r requirements.txt
```

### 使用

```bash
# 查询当前天气
python src/cli.py Beijing

# 查询天气预报
python src/cli.py Beijing --forecast
python src/cli.py Beijing -f

# JSON 格式输出
python src/cli.py Beijing --json
python src/cli.py Beijing -j

# 组合使用
python src/cli.py Beijing -f -j
python src/cli.py "New York" --forecast --json

# 查看帮助
python src/cli.py --help
```

## 📖 输出示例

### 当前天气

```
城市: Beijing (China)
坐标: 39.91, 116.40

当前天气:
  温度: 1.7°C
  天气: 阴天
```

### 天气预报

```
城市: Beijing (China)

当前天气:
  温度: 1.7°C
  天气: 阴天

未来 3 天预报:
  2026-02-28: -0.0°C ~ 2.5°C, 小阵雪
  2026-03-01: 0.2°C ~ 5.8°C, 阴天
  2026-03-02: 2.4°C ~ 7.5°C, 小毛毛雨
```

### JSON 输出

```json
{
  "city": "Beijing",
  "country": "China",
  "coordinates": {
    "latitude": 39.9075,
    "longitude": 116.39723
  },
  "current": {
    "temperature": 1.7,
    "weather": "阴天",
    "weather_code": 3,
    "time": "2026-02-28T14:30"
  },
  "forecast": [
    {
      "date": "2026-02-28",
      "max_temp": 2.5,
      "min_temp": -0.0,
      "weather": "小阵雪",
      "weather_code": 85
    }
  ]
}
```

## 📚 文档

- [架构设计](docs/architecture.md)
- [任务列表](tasks/)

## 🤝 协作流程

1. 查看 `tasks/` 目录下的任务文档
2. 在本地实现功能
3. 提交代码并推送
4. 等待代码审查

## API

本工具使用 [Open-Meteo](https://open-meteo.com/) 免费天气 API。

## 许可证

MIT

---

**Powered by OpenClaw** 🦐
