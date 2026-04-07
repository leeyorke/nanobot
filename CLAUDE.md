# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 常用命令
### 开发环境搭建
```bash
# 安装开发版本（包含所有依赖）
pip install -e ".[dev]"

# 初始化配置和工作区
nanobot onboard
```

### 代码质量检查
```bash
# Lint检查
ruff check .

# 自动修复Lint问题
ruff check . --fix

# 代码格式化
ruff format .
```

### 测试命令
```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=nanobot

# 运行指定测试文件
pytest tests/path/to/test_file.py

# 运行单个测试用例
pytest tests/path/to/test_file.py::TestClass::test_method
```

### 构建与发布
```bash
# 构建Python包
hatch build
```

### 运行命令
```bash
# 本地交互式Agent
nanobot agent

# 启动网关（对接所有聊天渠道）
nanobot gateway

# 启动OpenAI兼容API服务
nanobot serve

# 查看系统状态
nanobot status

# 渠道登录（微信/WhatsApp等）
nanobot channels login <channel-name>
```

## 高等级架构
### 项目核心定位
nanobot是**完全自主研发的超轻量级个人AI助手框架**，无LangChain/LlamaIndex等重型框架依赖，核心智能体代码仅几百行，主打极简、可扩展、易二次开发。

### 技术栈
- 语言：Python 3.11+
- 核心依赖：anthropic/openai官方SDK、pydantic、typer、httpx、ruff
- 无第三方智能体框架依赖，所有核心逻辑自研

### 核心模块结构
```
nanobot/
├── agent/          # 核心智能体运行时（LLM调用循环、工具执行、内存管理、技能加载）
├── skills/         # 内置技能库（tmux、github、天气等，支持动态扩展）
├── channels/       # 聊天渠道适配层（微信/飞书/Telegram/Discord等10+平台，插件化架构）
├── providers/      # LLM提供商适配层（OpenRouter/Anthropic/OpenAI/本地模型等，兼容OpenAI/Anthropic双格式）
├── config/         # 配置schema与加载逻辑
├── cli/            # 命令行入口
├── bus/            # 组件间消息路由
├── cron/           # 计划任务执行
├── heartbeat/      # 主动周期性任务调度
└── session/        # 对话会话管理
```

### 关键架构原则
1. **极简主义**：比同类框架少99%代码，无冗余抽象，直接对接LLM原生SDK
2. **提供商无关**：统一适配所有主流LLM提供商和本地模型，支持OpenAI/Anthropic双API格式
3. **渠道无关**：插件化渠道架构，新增聊天平台仅需实现少量接口
4. **MCP原生支持**：内置Model Context Protocol客户端，无缝对接外部工具服务器
5. **分层内存**：仅追加历史 + 长期记忆整合的双层内存体系

### 重要设计决策
- 移除litellm抽象层，直接对接各厂商原生SDK，减少依赖和问题排查复杂度
- 无GUI层设计，直接复用现有IM客户端或通用OpenAI前端，避免冗余开发
- 技能和渠道完全插件化，无需修改核心代码即可扩展功能
- 多实例原生支持，通过`--config`参数实现完全隔离的多实例部署

### 项目特有约定
- 分支策略：`main`为稳定发布分支，`nightly`为实验性功能分支
- 配置默认路径：`~/.nanobot/config.json`，支持多实例独立配置
- 技能默认存放路径：`~/.nanobot/workspace/skills/`，工作区独立
- 安全性：生产环境建议开启`tools.restrictToWorkspace: true`沙箱模式
