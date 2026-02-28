# Task 005: 添加日志记录功能

## 🎯 任务目标

为天气查询工具添加日志记录功能，方便调试和追踪问题。

## 📋 具体需求

### 功能要求

1. **日志级别支持**:
   - DEBUG: 详细的调试信息
   - INFO: 一般信息（默认）
   - WARNING: 警告信息
   - ERROR: 错误信息

2. **日志输出**:
   - 控制台输出（彩色）
   - 文件输出（`~/.weather-cli/weather.log`）

3. **日志格式**:
   ```
   [2026-03-01 10:30:45] [INFO] 查询北京天气
   [2026-03-01 10:30:46] [DEBUG] API 响应: {...}
   ```

4. **命令行参数**:
   ```bash
   python src/cli.py Beijing --verbose      # DEBUG 级别
   python src/cli.py Beijing --quiet        # WARNING 及以上
   ```

### 需要修改的文件

1. **src/logger.py**（新建）
   - 配置日志处理器
   - 支持彩色输出
   - 文件轮转（保留最近 7 天）

2. **src/cli.py**（修改）
   - 添加 `--verbose`, `--quiet` 参数
   - 在关键步骤记录日志

3. **src/weather.py**（修改）
   - 记录 API 调用
   - 记录错误信息

## 🔧 技术要求

1. 使用 Python 标准库 `logging`
2. 使用 `colorama` 实现跨平台彩色输出
3. 日志文件自动轮转（每天一个文件，保留 7 天）

## ✅ 验收标准

- [ ] `src/logger.py` 创建，包含完整的日志配置
- [ ] `src/cli.py` 支持 `--verbose` 和 `--quiet` 参数
- [ ] 日志正常输出到控制台和文件
- [ ] 日志格式符合要求
- [ ] 代码有完整类型注解和 docstring

## 🚀 提交要求

1. 实现所有功能
2. 测试通过
3. 提交信息: `feat: 添加日志记录功能`

---

**任务创建**: 全球虾 🦐  
**优先级**: P3  
**预计时间**: 30-45 分钟  
**状态**: ❌ 失败
**重试次数**: 1

**失败原因**: 语法错误无法自动修复
**问题**: src/logger.py:   File "/home/ecs-user/.openclaw/workspace-coder/weather-cli/.temp_validate.py", line...
