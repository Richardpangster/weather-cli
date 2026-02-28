# Task 004: 添加配置文件支持

## 🎯 任务目标

为天气查询工具添加配置文件支持，允许用户设置默认城市等偏好。

## 📋 具体需求

### 功能要求

1. **配置文件位置**: `~/.weather-cli/config.json`

2. **支持的配置项**:
   - `default_city`: 默认城市（如 "Beijing"）
   - `default_format`: 默认输出格式（"text" 或 "json"）
   - `forecast_days`: 默认预报天数（1-7）

3. **命令行参数**:
   ```bash
   # 设置配置
   python src/cli.py --config default_city=Beijing
   
   # 查看配置
   python src/cli.py --config-show
   
   # 重置配置
   python src/cli.py --config-reset
   ```

### 需要修改的文件

1. **src/config.py**（新建）
   - `load_config()` - 加载配置文件
   - `save_config()` - 保存配置文件
   - `get_config()` - 获取配置项
   - `set_config()` - 设置配置项

2. **src/cli.py**（修改）
   - 添加 `--config`, `--config-show`, `--config-reset` 参数
   - 使用配置文件中的默认值

### 配置文件格式

```json
{
  "default_city": "Beijing",
  "default_format": "text",
  "forecast_days": 3
}
```

## 🔧 技术要求

1. 使用 `pathlib` 处理文件路径
2. 使用 `json` 模块读写配置
3. 配置文件不存在时自动创建
4. 有合理的默认值

## ✅ 验收标准

- [ ] `src/config.py` 创建，包含所有配置函数
- [ ] `src/cli.py` 支持 `--config` 参数
- [ ] `src/cli.py` 使用配置文件中的默认值
- [ ] 配置文件自动创建在 `~/.weather-cli/config.json`
- [ ] 更新 `README.md` 添加配置说明
- [ ] 代码有完整类型注解和 docstring

## 🚀 提交要求

1. 实现所有功能
2. 测试通过
3. 提交信息: `feat: 添加配置文件支持`

---

**任务创建**: 全球虾 🦐  
**优先级**: P2  
**预计时间**: 30-45 分钟  
**状态**: 🆕 待处理
