<div align="center">
  <img src="nanobot_logo.png" alt="nanobot" width="500">
  <h1>nanobot: 超轻量级个人AI助手</h1>
  <p>
    <a href="https://pypi.org/project/nanobot-ai/"><img src="https://img.shields.io/pypi/v/nanobot-ai" alt="PyPI"></a>
    <a href="https://pepy.tech/project/nanobot-ai"><img src="https://static.pepy.tech/badge/nanobot-ai" alt="下载量"></a>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python版本"></a>
    <img src="https://img.shields.io/badge/license-MIT-green" alt="许可证"></a>
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/飞书-交流群-E9DBFC?style=flat&logo=feishu&logoColor=white" alt="飞书交流群"></a>
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/微信-交流群-C5EAB4?style=flat&logo=wechat&logoColor=white" alt="微信交流群"></a>
    <a href="https://discord.gg/MnCvHqpUGB"><img src="https://img.shields.io/badge/Discord-社区-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord社区"></a>
  </p>
</div>

🐈 **nanobot** 是一款受 [OpenClaw](https://github.com/openclaw/openclaw) 启发的**超轻量级**个人AI助手。

⚡️ 仅用比OpenClaw少**99%**的代码量实现核心智能体功能。

📏 实时代码行数统计：随时运行 `bash core_agent_lines.sh` 验证。

## 📢 最新动态

- **2026-04-02** 🧱 **长时任务**运行更可靠 — 核心运行时加固。
- **2026-04-01** 🔑 GitHub Copilot认证恢复；更严格的工作区路径校验；OpenRouter Claude缓存修复。
- **2026-03-31** 🛰️ 微信多模态对齐，Discord/Matrix体验优化，Python SDK外观，MCP和工具修复。
- **2026-03-30** 🧩 OpenAI兼容API收紧；可组合的智能体生命周期钩子。
- **2026-03-29** 💬 微信语音、输入状态、二维码/媒体恢复；固定会话的OpenAI兼容API。
- **2026-03-28** 📚 提供商文档更新；技能模板 wording 修复。
- **2026-03-27** 🚀 发布 **v0.1.4.post6** — 架构解耦，移除litellm，端到端流式传输，微信渠道，以及安全修复。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post6)。
- **2026-03-26** 🏗️ 智能体运行器提取，生命周期钩子统一；边界处流增量合并。
- **2026-03-25** 🌏 阶跃星辰提供商，可配置时区，Gemini思考签名。
- **2026-03-24** 🔧 微信兼容性，飞书CardKit流式传输，测试套件重构。

<details>
<summary>更早的动态</summary>

- **2026-03-23** 🔧 命令路由重构以支持插件，WhatsApp/微信媒体，统一渠道登录CLI。
- **2026-03-22** ⚡ 端到端流式传输，微信渠道，Anthropic缓存优化，`/status` 命令。
- **2026-03-21** 🔒 用原生 `openai` + `anthropic` SDK 替换 `litellm`。详情请见 [commit](https://github.com/HKUDS/nanobot/commit/3dfdab7)。
- **2026-03-20** 🧙 交互式设置向导 — 选择提供商，模型自动补全，开箱即用。
- **2026-03-19** 💬 Telegram在高负载下更有弹性；飞书现在能正确渲染代码块。
- **2026-03-18** 📷 Telegram现在可以通过URL发送媒体。Cron计划显示可读的详细信息。
- **2026-03-17** ✨ 飞书格式优化，Slack完成后添加反应，自定义端点支持额外头部，图像处理更可靠。
- **2026-03-16** 🚀 发布 **v0.1.4.post5** — 专注于优化的版本，更强的可靠性和渠道支持，更稳定的日常使用体验。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post5)。
- **2026-03-15** 🧩 钉钉富媒体，更智能的内置技能，更清晰的模型兼容性。
- **2026-03-14** 💬 渠道插件，飞书回复，更稳定的MCP、QQ和媒体处理。
- **2026-03-13** 🌐 多提供商网页搜索，LangSmith，更广泛的可靠性改进。
- **2026-03-12** 🚀 火山引擎支持，Telegram回复上下文，`/restart`，更健壮的内存。
- **2026-03-11** 🔌 企业微信，Ollama，更清晰的发现，更安全的工具行为。
- **2026-03-10** 🧠 基于令牌的内存，共享重试，更清晰的网关和Telegram行为。
- **2026-03-09** 💬 Slack线程优化，更好的飞书音频兼容性。
- **2026-03-08** 🚀 发布 **v0.1.4.post4** — 可靠性满满的版本，更安全的默认值，更好的多实例支持，更健壮的MCP，主要的渠道和提供商改进。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post4)。
- **2026-03-07** 🚀 Azure OpenAI提供商，WhatsApp媒体，QQ群聊，更多Telegram/飞书优化。
- **2026-03-06** 🪄 更轻量的提供商，更智能的媒体处理，更健壮的内存和CLI兼容性。
- **2026-03-05** ⚡️ Telegram草稿流式传输，MCP SSE支持，更广泛的渠道可靠性修复。
- **2026-03-04** 🛠️ 依赖清理，更安全的文件读取，另一轮测试和Cron修复。
- **2026-03-03** 🧠 更清晰的用户消息合并，更安全的多模态保存，更强的Cron防护。
- **2026-03-02** 🛡️ 更安全的默认访问控制，更健壮的Cron重载，更清晰的Matrix媒体处理。
- **2026-03-01** 🌐 网页代理支持，更智能的Cron提醒，飞书富文本解析改进。
- **2026-02-28** 🚀 发布 **v0.1.4.post3** — 更清晰的上下文，加固的会话历史，更智能的智能体。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post3)。
- **2026-02-27** 🧠 实验性思考模式支持，钉钉媒体消息，飞书和QQ渠道修复。
- **2026-02-26** 🛡️ 会话投毒修复，WhatsApp去重，Windows路径防护，Mistral兼容性。
- **2026-02-25** 🧹 新的Matrix渠道，更清晰的会话上下文，自动工作区模板同步。
- **2026-02-24** 🚀 发布 **v0.1.4.post2** — 专注于可靠性的版本，重新设计的心跳，提示缓存优化，加固的提供商和渠道稳定性。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post2)。
- **2026-02-23** 🔧 虚拟工具调用心跳，提示缓存优化，Slack mrkdwn修复。
- **2026-02-22** 🛡️ Slack线程隔离，Discord输入状态修复，智能体可靠性改进。
- **2026-02-21** 🎉 发布 **v0.1.4.post1** — 新的提供商，跨渠道媒体支持，主要的稳定性改进。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post1)。
- **2026-02-20** 🐦 飞书现在可以接收用户的多模态文件。底层内存更可靠。
- **2026-02-19** ✨ Slack现在可以发送文件，Discord拆分长消息，子智能体在CLI模式下工作。
- **2026-02-18** ⚡️ nanobot现在支持火山引擎，MCP自定义认证头，以及Anthropic提示缓存。
- **2026-02-17** 🎉 发布 **v0.1.4** — MCP支持，进度流式传输，新的提供商，多个渠道改进。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4)。
- **2026-02-16** 🦞 nanobot现在集成了 [ClawHub](https://clawhub.ai) 技能 — 搜索和安装公共智能体技能。
- **2026-02-15** 🔑 nanobot现在支持带有OAuth登录的OpenAI Codex提供商。
- **2026-02-14** 🔌 nanobot现在支持MCP！详情请见 [MCP部分](#mcp-模型上下文协议)。
- **2026-02-13** 🎉 发布 **v0.1.3.post7** — 包括安全加固和多项改进。**请升级到最新版本以解决安全问题**。详情请见 [发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post7)。
- **2026-02-12** 🧠 重新设计的内存系统 — 更少的代码，更可靠。加入 [讨论](https://github.com/HKUDS/nanobot/discussions/566)！
- **2026-02-11** ✨ 增强的CLI体验，新增MiniMax支持！
- **2026-02-10** 🎉 发布 **v0.1.3.post6** 带来改进！查看更新 [说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post6) 和我们的 [路线图](https://github.com/HKUDS/nanobot/discussions/431)。
- **2026-02-09** 💬 新增Slack、Email和QQ支持 — nanobot现在支持多个聊天平台！
- **2026-02-08** 🔧 重构提供商 — 添加新的LLM提供商现在只需2个简单步骤！查看 [这里](#提供商)。
- **2026-02-07** 🚀 发布 **v0.1.3.post5** 带来通义千问支持和几项关键改进！详情查看 [这里](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post5)。
- **2026-02-06** ✨ 新增Moonshot/Kimi提供商，Discord集成，增强安全加固！
- **2026-02-05** ✨ 新增飞书渠道，DeepSeek提供商，增强计划任务支持！
- **2026-02-04** 🚀 发布 **v0.1.3.post4** 带来多提供商和Docker支持！详情查看 [这里](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post4)。
- **2026-02-03** ⚡ 集成vLLM支持本地LLM，改进自然语言任务调度！
- **2026-02-02** 🎉 nanobot正式发布！欢迎试用 🐈 nanobot！

</details>

> 🐈 nanobot仅用于教育、研究和技术交流目的。与加密货币无关，不涉及任何官方代币或硬币。

## nanobot的核心特性：

🪶 **超轻量级**：OpenClaw的超轻量级实现 — 小99%，速度显著更快。

🔬 **研究友好**：干净、可读的代码，易于理解、修改和扩展用于研究。

⚡️ **闪电快速**：极小的占用空间意味着更快的启动、更低的资源使用和更快的迭代。

💎 **易于使用**：一键部署，开箱即用。

## 🏗️ 架构

<p align="center">
  <img src="nanobot_arch.png" alt="nanobot架构" width="800">
</p>

## 目录

- [最新动态](#-最新动态)
- [核心特性](#nanobot的核心特性)
- [架构](#️-架构)
- [功能](#-功能)
- [安装](#-安装)
- [快速开始](#-快速开始)
- [聊天应用](#-聊天应用)
- [智能体社交网络](#-智能体社交网络)
- [配置](#️-配置)
- [多实例](#-多实例)
- [内存](#-内存)
- [CLI参考](#-cli参考)
- [聊天内命令](#-聊天内命令)
- [Python SDK](#-python-sdk)
- [OpenAI兼容API](#-openai兼容api)
- [Docker](#-docker)
- [Linux服务](#-linux服务)
- [项目结构](#-项目结构)
- [贡献与路线图](#-贡献与路线图)
- [星标历史](#-星标历史)

## ✨ 功能

<table align="center">
  <tr align="center">
    <th><p align="center">📈 24/7实时市场分析</p></th>
    <th><p align="center">🚀 全栈软件工程师</p></th>
    <th><p align="center">📅 智能日常日程管理</p></th>
    <th><p align="center">📚 个人知识助手</p></th>
  </tr>
  <tr>
    <td align="center"><p align="center"><img src="case/search.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/code.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/scedule.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/memory.gif" width="180" height="400"></p></td>
  </tr>
  <tr>
    <td align="center">发现 • 洞察 • 趋势</td>
    <td align="center">开发 • 部署 • 扩展</td>
    <td align="center">计划 • 自动化 • 组织</td>
    <td align="center">学习 • 记忆 • 推理</td>
  </tr>
</table>

## 📦 安装

> [!IMPORTANT]
> 本README可能描述了最新源代码中首先提供的功能。
> 如果您想要最新的功能和实验性更改，请从源代码安装。
> 如果您想要最稳定的日常使用体验，请从PyPI或使用`uv`安装。

**从源代码安装**（最新功能，实验性更改可能首先落地；推荐用于开发）

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
pip install -e .
```

**使用[uv](https://github.com/astral-sh/uv)安装**（稳定版本，快速）

```bash
uv tool install nanobot-ai
```

**从PyPI安装**（稳定版本）

```bash
pip install nanobot-ai
```

### 更新到最新版本

**PyPI / pip**

```bash
pip install -U nanobot-ai
nanobot --version
```

**uv**

```bash
uv tool upgrade nanobot-ai
nanobot --version
```

**使用WhatsApp？** 升级后重建本地桥接：

```bash
rm -rf ~/.nanobot/bridge
nanobot channels login whatsapp
```

## 🚀 快速开始

> [!TIP]
> 在`~/.nanobot/config.json`中设置您的API密钥。
> 获取API密钥：[OpenRouter](https://openrouter.ai/keys)（全球）
>
> 对于其他LLM提供商，请参见[提供商](#提供商)部分。
>
> 对于网页搜索功能设置，请参见[网页搜索](#网页搜索)。

**1. 初始化**

```bash
nanobot onboard
```

如果您想要交互式设置向导，请使用`nanobot onboard --wizard`。

**2. 配置** (`~/.nanobot/config.json`)

在配置中配置**这两部分**（其他选项有默认值）。

*设置您的API密钥*（例如OpenRouter，推荐全球用户使用）：
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  }
}
```

*设置您的模型*（可选择固定提供商 — 默认为自动检测）：
```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

**3. 聊天**

```bash
nanobot agent
```

就是这样！您只需2分钟就拥有了一个可用的AI助手。

## 💬 聊天应用

将nanobot连接到您最喜欢的聊天平台。想要构建自己的？请参见[渠道插件指南](./docs/CHANNEL_PLUGIN_GUIDE.md)。

| 渠道 | 需要的内容 |
|---------|---------------|
| **Telegram** | 来自@BotFather的机器人令牌 |
| **Discord** | 机器人令牌 + 消息内容权限 |
| **WhatsApp** | 二维码扫描 (`nanobot channels login whatsapp`) |
| **微信 (Weixin)** | 二维码扫描 (`nanobot channels login weixin`) |
| **飞书** | App ID + App Secret |
| **钉钉** | App Key + App Secret |
| **Slack** | 机器人令牌 + 应用级令牌 |
| **Matrix** |  homeserver URL + 访问令牌 |
| **Email** | IMAP/SMTP凭证 |
| **QQ** | App ID + App Secret |
| **企业微信** | 机器人ID + 机器人Secret |
| **Mochat** | Claw令牌（可自动设置） |

<details>
<summary><b>Telegram</b>（推荐）</summary>

**1. 创建机器人**
- 打开Telegram，搜索`@BotFather`
- 发送`/newbot`，按照提示操作
- 复制令牌

**2. 配置**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

> 您可以在Telegram设置中找到您的**用户ID**。显示为`@yourUserId`。
> 复制这个值**不带`@`符号**并粘贴到配置文件中。

**3. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Mochat (Claw IM)</b></summary>

默认使用**Socket.IO WebSocket**，带有HTTP轮询回退。

**1. 让nanobot为您设置Mochat**

只需向nanobot发送这条消息（将`xxx@xxx`替换为您的真实邮箱）：

```
Read https://raw.githubusercontent.com/HKUDS/MoChat/refs/heads/main/skills/nanobot/skill.md and register on MoChat. My Email account is xxx@xxx Bind me as your owner and DM me on MoChat.
```

nanobot会自动注册、配置`~/.nanobot/config.json`并连接到Mochat。

**2. 重启网关**

```bash
nanobot gateway
```

就是这样 — 剩下的交给nanobot处理！

<br>

<details>
<summary>手动配置（高级）</summary>

如果您更喜欢手动配置，将以下内容添加到`~/.nanobot/config.json`：

> 请保密`claw_token`。它只应在发送到您的Mochat API端点的`X-Claw-Token`头中使用。

```json
{
  "channels": {
    "mochat": {
      "enabled": true,
      "base_url": "https://mochat.io",
      "socket_url": "https://mochat.io",
      "socket_path": "/socket.io",
      "claw_token": "claw_xxx",
      "agent_user_id": "6982abcdef",
      "sessions": ["*"],
      "panels": ["*"],
      "reply_delay_mode": "non-mention",
      "reply_delay_ms": 120000
    }
  }
}
```

</details>

</details>

<details>
<summary><b>Discord</b></summary>

**1. 创建机器人**
- 访问 https://discord.com/developers/applications
- 创建应用 → 机器人 → 添加机器人
- 复制机器人令牌

**2. 启用权限**
- 在机器人设置中，启用**MESSAGE CONTENT INTENT**
- （可选）如果您计划使用基于成员数据的允许列表，请启用**SERVER MEMBERS INTENT**

**3. 获取您的用户ID**
- Discord设置 → 高级 → 启用**开发者模式**
- 右键点击您的头像 → **复制用户ID**

**4. 配置**

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

> `groupPolicy`控制机器人在群聊中的响应方式：
> - `"mention"`（默认） — 仅在被@提及时响应
> - `"open"` — 响应所有消息
> 私信始终在发送者在`allowFrom`中时响应。
> - 如果您将群组策略设置为open，请创建私人线程，然后@机器人进入其中。否则，线程本身和您产生它的频道都会生成一个机器人会话。

**5. 邀请机器人**
- OAuth2 → URL生成器
- 范围：`bot`
- 机器人权限：`Send Messages`、`Read Message History`
- 打开生成的邀请URL，将机器人添加到您的服务器

**6. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Matrix (Element)</b></summary>

首先安装Matrix依赖：

```bash
pip install nanobot-ai[matrix]
```

**1. 创建/选择Matrix账户**

- 在您的homeserver上创建或复用一个Matrix账户（例如`matrix.org`）。
- 确认您可以用Element登录。

**2. 获取凭证**

- 您需要：
  - `userId`（示例：`@nanobot:matrix.org`）
  - `accessToken`
  - `deviceId`（建议使用，以便同步令牌可以在重启后恢复）
- 您可以从您的homeserver登录API（`/_matrix/client/v3/login`）或客户端的高级会话设置中获取这些信息。

**3. 配置**

```json
{
  "channels": {
    "matrix": {
      "enabled": true,
      "homeserver": "https://matrix.org",
      "userId": "@nanobot:matrix.org",
      "accessToken": "syt_xxx",
      "deviceId": "NANOBOT01",
      "e2eeEnabled": true,
      "allowFrom": ["@your_user:matrix.org"],
      "groupPolicy": "open",
      "groupAllowFrom": [],
      "allowRoomMentions": false,
      "maxMediaBytes": 20971520
    }
  }
}
```

> 保留持久的`matrix-store`和稳定的`deviceId` — 如果这些在重启时更改，加密会话状态会丢失。

| 选项 | 描述 |
|--------|-------------|
| `allowFrom` | 允许交互的用户ID。空则拒绝所有；使用`["*"]`允许所有人。 |
| `groupPolicy` | `open`（默认）、`mention`或`allowlist`。 |
| `groupAllowFrom` | 房间允许列表（当策略为`allowlist`时使用）。 |
| `allowRoomMentions` | 在提及模式下接受`@room`提及。 |
| `e2eeEnabled` | 端到端加密支持（默认`true`）。纯文本模式请设置为`false`。 |
| `maxMediaBytes` | 最大附件大小（默认`20MB`）。设置为`0`阻止所有媒体。 |

**4. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>WhatsApp</b></summary>

需要**Node.js ≥18**。

**1. 链接设备**

```bash
nanobot channels login whatsapp
# 用WhatsApp扫描二维码 → 设置 → 链接设备
```

**2. 配置**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**3. 运行**（两个终端）

```bash
# 终端1
nanobot channels login whatsapp

# 终端2
nanobot gateway
```

> WhatsApp桥接更新不会自动应用于现有安装。
> 升级nanobot后，用以下命令重建本地桥接：
> `rm -rf ~/.nanobot/bridge && nanobot channels login whatsapp`

</details>

<details>
<summary><b>飞书</b></summary>

使用**WebSocket**长连接 — 无需公网IP。

**1. 创建飞书机器人**
- 访问 [飞书开放平台](https://open.feishu.cn/app)
- 创建新应用 → 启用**机器人**能力
- **权限**：
  - `im:message`（发送消息）和 `im:message.p2p_msg:readonly`（接收消息）
  - **流式回复**（nanobot默认）：添加 **`cardkit:card:write`**（在飞书开发者控制台通常标记为**创建和更新卡片**）。CardKit实体和流式助手文本需要此权限。旧应用可能没有 — 打开**权限管理**，启用该范围，如果控制台要求则**发布**新应用版本。
  - 如果您**无法**添加`cardkit:card:write`，请在`channels.feishu`下设置`"streaming": false`（见下文）。机器人仍然可以工作；回复使用普通交互卡片，没有逐令牌流式传输。
- **事件**：添加`im.message.receive_v1`（接收消息）
  - 选择**长连接**模式（需要先运行nanobot建立连接）
- 从"凭证与基础信息"获取**App ID**和**App Secret**
- 发布应用

**2. 配置**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": ["ou_YOUR_OPEN_ID"],
      "groupPolicy": "mention",
      "streaming": true
    }
  }
}
```

> `streaming`默认为`true`。如果您的应用没有**`cardkit:card:write`**权限（见上面的权限），请使用`false`。
> `encryptKey`和`verificationToken`对于长连接模式是可选的。
> `allowFrom`：添加您的open_id（当您向机器人发送消息时在nanobot日志中找到）。使用`["*"]`允许所有用户。
> `groupPolicy`：`"mention"`（默认 — 仅在被@提及时响应），`"open"`（响应所有群消息）。私聊始终响应。

**3. 运行**

```bash
nanobot gateway
```

> [!TIP]
> 飞书使用WebSocket接收消息 — 无需webhook或公网IP！

</details>

<details>
<summary><b>QQ (QQ单聊)</b></summary>

使用**botpy SDK**与WebSocket — 无需公网IP。目前仅支持**私聊**。

**1. 注册并创建机器人**
- 访问 [QQ开放平台](https://q.qq.com) → 注册为开发者（个人或企业）
- 创建新的机器人应用
- 进入**开发设置** → 复制**AppID**和**AppSecret**

**2. 设置沙箱进行测试**
- 在机器人管理控制台，找到**沙箱配置**
- 在**在消息列表配置**下，点击**添加成员**并添加您自己的QQ号
- 添加后，用手机QQ扫描机器人的二维码 → 打开机器人资料 → 点击"发消息"开始聊天

**3. 配置**

> - `allowFrom`：添加您的openid（当您向机器人发送消息时在nanobot日志中找到）。使用`["*"]`公开访问。
> - `msgFormat`：可选。使用`"plain"`（默认）以获得与旧版QQ客户端的最大兼容性，或使用`"markdown"`在新版客户端上获得更丰富的格式。
> - 生产环境：在机器人控制台提交审核并发布。完整发布流程请见 [QQ机器人文档](https://bot.q.qq.com/wiki/)。

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"],
      "msgFormat": "plain"
    }
  }
}
```

**4. 运行**

```bash
nanobot gateway
```

现在从QQ向机器人发送消息 — 它应该会回复！

</details>

<details>
<summary><b>钉钉</b></summary>

使用**流模式** — 无需公网IP。

**1. 创建钉钉机器人**
- 访问 [钉钉开放平台](https://open-dev.dingtalk.com/)
- 创建新应用 -> 添加**机器人**能力
- **配置**：
  - 开启**流模式**
- **权限**：添加发送消息所需的必要权限
- 从"凭证"获取**AppKey**（客户端ID）和**AppSecret**（客户端密钥）
- 发布应用

**2. 配置**

```json
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "YOUR_APP_KEY",
      "clientSecret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_STAFF_ID"]
    }
  }
}
```

> `allowFrom`：添加您的员工ID。使用`["*"]`允许所有用户。

**3. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Slack</b></summary>

使用**Socket模式** — 无需公网URL。

**1. 创建Slack应用**
- 访问 [Slack API](https://api.slack.com/apps) → **创建新应用** → "从头开始"
- 选择名称并选择您的工作区

**2. 配置应用**
- **Socket模式**：开启 → 生成带有`connections:write`范围的**应用级令牌** → 复制它（`xapp-...`）
- **OAuth与权限**：添加机器人范围：`chat:write`、`reactions:write`、`app_mentions:read`
- **事件订阅**：开启 → 订阅机器人事件：`message.im`、`message.channels`、`app_mention` → 保存更改
- **应用主页**：滚动到**显示选项卡** → 启用**消息选项卡** → 勾选**"允许用户从消息选项卡发送Slash命令和消息"**
- **安装应用**：点击**安装到工作区** → 授权 → 复制**机器人令牌**（`xoxb-...`）

**3. 配置nanobot**

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-...",
      "appToken": "xapp-...",
      "allowFrom": ["YOUR_SLACK_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

**4. 运行**

```bash
nanobot gateway
```

直接给机器人发私信或在频道中@提及它 — 它应该会回复！

> [!TIP]
> - `groupPolicy`：`"mention"`（默认 — 仅在被@提及时响应），`"open"`（响应所有频道消息），或`"allowlist"`（限制到特定频道）。
> - 私信策略默认为开放。设置`"dm": {"enabled": false}`禁用私信。

</details>

<details>
<summary><b>Email</b></summary>

给nanobot自己的电子邮件账户。它轮询**IMAP**获取传入邮件并通过**SMTP**回复 — 就像个人电子邮件助手。

**1. 获取凭证（Gmail示例）**
- 为您的机器人创建专用Gmail账户（例如`my-nanobot@gmail.com`）
- 启用两步验证 → 创建 [应用密码](https://myaccount.google.com/apppasswords)
- 将此应用密码用于IMAP和SMTP

**2. 配置**

> - `consentGranted`必须为`true`以允许邮箱访问。这是一个安全门 — 设置为`false`完全禁用。
> - `allowFrom`：添加您的电子邮件地址。使用`["*"]`接受来自任何人的电子邮件。
> - `smtpUseTls`和`smtpUseSsl`分别默认为`true`/`false`，这对于Gmail是正确的（端口587 + STARTTLS）。无需显式设置它们。
> - 如果您只想读取/分析电子邮件而不发送自动回复，请设置`"autoReplyEnabled": false`。

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "imapHost": "imap.gmail.com",
      "imapPort": 993,
      "imapUsername": "my-nanobot@gmail.com",
      "imapPassword": "your-app-password",
      "smtpHost": "smtp.gmail.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@gmail.com",
      "smtpPassword": "your-app-password",
      "fromAddress": "my-nanobot@gmail.com",
      "allowFrom": ["your-real-email@gmail.com"]
    }
  }
}
```

**3. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>微信</b></summary>

使用带有二维码登录的**HTTP长轮询**，通过ilinkai个人微信API。无需本地微信桌面客户端。

**1. 安装微信支持**

```bash
pip install "nanobot-ai[weixin]"
```

**2. 配置**

```json
{
  "channels": {
    "weixin": {
      "enabled": true,
      "allowFrom": ["YOUR_WECHAT_USER_ID"]
    }
  }
}
```

> - `allowFrom`：添加您在nanobot日志中看到的您微信账户的发送者ID。使用`["*"]`允许所有用户。
> - `token`：可选。如果省略，交互式登录，nanobot会为您保存令牌。
> - `routeTag`：可选。当您的上游微信部署需要请求路由时，nanobot会将其作为`SKRouteTag`头发送。
> - `stateDir`：可选。默认为nanobot的微信状态运行时目录。
> - `pollTimeout`：可选的长轮询超时（秒）。

**3. 登录**

```bash
nanobot channels login weixin
```

使用`--force`重新认证并忽略任何保存的令牌：

```bash
nanobot channels login weixin --force
```

**4. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>企业微信</b></summary>

> 这里我们使用 [wecom-aibot-sdk-python](https://github.com/chengyongru/wecom_aibot_sdk)（官方 [@wecom/aibot-node-sdk](https://www.npmjs.com/package/@wecom/aibot-node-sdk) 的社区Python版本）。
>
> 使用**WebSocket**长连接 — 无需公网IP。

**1. 安装可选依赖**

```bash
pip install nanobot-ai[wecom]
```

**2. 创建企业微信AI机器人**

进入企业微信管理后台 → 智能机器人 → 创建机器人 → 选择**API模式**带**长连接**。复制机器人ID和Secret。

**3. 配置**

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "your_bot_id",
      "secret": "your_bot_secret",
      "allowFrom": ["your_id"]
    }
  }
}
```

**4. 运行**

```bash
nanobot gateway
```

</details>

## 🌐 智能体社交网络

🐈 nanobot能够链接到智能体社交网络（智能体社区）。**只需发送一条消息，您的nanobot就会自动加入！**

| 平台 | 如何加入（向您的机器人发送此消息） |
|----------|-------------|
| [**Moltbook**](https://www.moltbook.com/) | `Read https://moltbook.com/skill.md and follow the instructions to join Moltbook` |
| [**ClawdChat**](https://clawdchat.ai/) | `Read https://clawdchat.ai/skill.md and follow the instructions to join ClawdChat` |

只需将上述命令发送给您的nanobot（通过CLI或任何聊天渠道），它会处理剩下的事情。

## ⚙️ 配置

配置文件：`~/.nanobot/config.json`

> [!NOTE]
> 如果您的配置文件比当前 schema 旧，您可以刷新它而不覆盖现有值：
> 运行`nanobot onboard`，然后在被问及是否覆盖配置时回答`N`。
> nanobot会合并缺失的默认字段并保留您当前的设置。

### 提供商

> [!TIP]
> - **Groq** 通过Whisper提供免费的语音转录。如果配置了，Telegram语音消息将被自动转录。
> - **MiniMax编码计划**：nanobot社区专属折扣链接：[海外](https://platform.minimax.io/subscribe/coding-plan?code=9txpdXw04g&source=link) · [中国大陆](https://platform.minimaxi.com/subscribe/token-plan?code=GILTJpMTqZ&source=link)
> - **MiniMax（中国大陆）**：如果您的API密钥来自MiniMax的中国大陆平台（minimaxi.com），请在您的minimax提供商配置中设置`"apiBase": "https://api.minimaxi.com/v1"`。
> - **火山引擎 / BytePlus编码计划**：使用专用提供商`volcengineCodingPlan`或`byteplusCodingPlan`，而不是按使用量付费的`volcengine`/`byteplus`提供商。
> - **智谱编码计划**：如果您使用智谱的编码计划，请在您的zhipu提供商配置中设置`"apiBase": "https://open.bigmodel.cn/api/coding/paas/v4"`。
> - **阿里云百炼**：如果您使用阿里云百炼的OpenAI兼容端点，请在您的dashscope提供商配置中设置`"apiBase": "https://dashscope.aliyuncs.com/compatible-mode/v1"`。
> - **阶跃星辰（中国大陆）**：如果您的API密钥来自阶跃星辰的中国大陆平台（stepfun.com），请在您的stepfun提供商配置中设置`"apiBase": "https://api.stepfun.com/v1"`。

| 提供商 | 用途 | 获取API密钥 |
|----------|---------|-------------|
| `custom` | 任何OpenAI兼容端点 | — |
| `openrouter` | LLM（推荐，可访问所有模型） | [openrouter.ai](https://openrouter.ai) |
| `volcengine` | LLM（火山引擎，按使用量付费） | [编码计划](https://www.volcengine.com/activity/codingplan?utm_campaign=nanobot&utm_content=nanobot&utm_medium=devrel&utm_source=OWO&utm_term=nanobot) · [volcengine.com](https://www.volcengine.com) |
| `byteplus` | LLM（火山引擎国际版，按使用量付费） | [编码计划](https://www.byteplus.com/en/activity/codingplan?utm_campaign=nanobot&utm_content=nanobot&utm_medium=devrel&utm_source=OWO&utm_term=nanobot) · [byteplus.com](https://www.byteplus.com) |
| `anthropic` | LLM（Claude直接） | [console.anthropic.com](https://console.anthropic.com) |
| `azure_openai` | LLM（Azure OpenAI） | [portal.azure.com](https://portal.azure.com) |
| `openai` | LLM（GPT直接） | [platform.openai.com](https://platform.openai.com) |
| `deepseek` | LLM（DeepSeek直接） | [platform.deepseek.com](https://platform.deepseek.com) |
| `groq` | LLM + **语音转录**（Whisper） | [console.groq.com](https://console.groq.com) |
| `minimax` | LLM（MiniMax直接） | [platform.minimaxi.com](https://platform.minimaxi.com) |
| `gemini` | LLM（Gemini直接） | [aistudio.google.com](https://aistudio.google.com) |
| `aihubmix` | LLM（API网关，可访问所有模型） | [aihubmix.com](https://aihubmix.com) |
| `siliconflow` | LLM（硅基流动） | [siliconflow.cn](https://siliconflow.cn) |
| `dashscope` | LLM（通义千问） | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |
| `moonshot` | LLM（Moonshot/Kimi） | [platform.moonshot.cn](https://platform.moonshot.cn) |
| `zhipu` | LLM（智谱GLM） | [open.bigmodel.cn](https://open.bigmodel.cn) |
| `mimo` | LLM（小米MiMo） | [platform.xiaomimimo.com](https://platform.xiaomimimo.com) |
| `ollama` | LLM（本地，Ollama） | — |
| `mistral` | LLM | [docs.mistral.ai](https://docs.mistral.ai/) |
| `stepfun` | LLM（阶跃星辰） | [platform.stepfun.com](https://platform.stepfun.com) |
| `ovms` | LLM（本地，OpenVINO模型服务器） | [docs.openvino.ai](https://docs.openvino.ai/2026/model-server/ovms_docs_llm_quickstart.html) |
| `vllm` | LLM（本地，任何OpenAI兼容服务器） | — |
| `openai_codex` | LLM（Codex，OAuth） | `nanobot provider login openai-codex` |
| `github_copilot` | LLM（GitHub Copilot，OAuth） | `nanobot provider login github-copilot` |

<details>
<summary><b>OpenAI Codex (OAuth)</b></summary>

Codex使用OAuth而不是API密钥。需要ChatGPT Plus或Pro账户。
`config.json`中不需要`providers.openaiCodex`块；`nanobot provider login`将OAuth会话存储在配置之外。

**1. 登录：**
```bash
nanobot provider login openai-codex
```

**2. 设置模型**（合并到`~/.nanobot/config.json`）：
```json
{
  "agents": {
    "defaults": {
      "model": "openai-codex/gpt-5.1-codex"
    }
  }
}
```

**3. 聊天：**
```bash
nanobot agent -m "Hello!"

# 本地定向到特定工作区/配置
nanobot agent -c ~/.nanobot-telegram/config.json -m "Hello!"

# 在该配置之上一次性覆盖工作区
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test -m "Hello!"
```

> Docker用户：使用`docker run -it`进行交互式OAuth登录。

</details>

<details>
<summary><b>GitHub Copilot (OAuth)</b></summary>

GitHub Copilot使用OAuth而不是API密钥。需要配置了计划的[GitHub账户](https://github.com/features/copilot/plans)。
`config.json`中不需要`providers.githubCopilot`块；`nanobot provider login`将OAuth会话存储在配置之外。

**1. 登录：**
```bash
nanobot provider login github-copilot
```

**2. 设置模型**（合并到`~/.nanobot/config.json`）：
```json
{
  "agents": {
    "defaults": {
      "model": "github-copilot/gpt-4.1"
    }
  }
}
```

**3. 聊天：**
```bash
nanobot agent -m "Hello!"

# 本地定向到特定工作区/配置
nanobot agent -c ~/.nanobot-telegram/config.json -m "Hello!"

# 在该配置之上一次性覆盖工作区
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test -m "Hello!"
```

> Docker用户：使用`docker run -it`进行交互式OAuth登录。

</details>

<details>
<summary><b>自定义提供商（任何OpenAI兼容API）</b></summary>

直接连接到任何OpenAI兼容端点 — LM Studio、llama.cpp、Together AI、Fireworks、Azure OpenAI或任何自托管服务器。模型名称按原样传递。

```json
{
  "providers": {
    "custom": {
      "apiKey": "your-api-key",
      "apiBase": "https://api.your-provider.com/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "your-model-name"
    }
  }
}
```

> 对于不需要密钥的本地服务器，将`apiKey`设置为任何非空字符串（例如`"no-key"`）。

</details>

<details>
<summary><b>Ollama (本地)</b></summary>

用Ollama运行本地模型，然后添加到配置：

**1. 启动Ollama**（示例）：
```bash
ollama run llama3.2
```

**2. 添加到配置**（部分 — 合并到`~/.nanobot/config.json`）：
```json
{
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434"
    }
  },
  "agents": {
    "defaults": {
      "provider": "ollama",
      "model": "llama3.2"
    }
  }
}
```

> 当配置了`providers.ollama.apiBase`时，`provider: "auto"`也可以工作，但设置`"provider": "ollama"`是最清晰的选项。

</details>

<details>
<summary><b>OpenVINO模型服务器（本地 / OpenAI兼容）</b></summary>

使用[OpenVINO模型服务器](https://docs.openvino.ai/2026/model-server/ovms_docs_llm_quickstart.html)在Intel GPU上本地运行LLM。OVMS在`/v3`处暴露OpenAI兼容API。

> 需要Docker和具有驱动程序访问权限的Intel GPU（`/dev/dri`）。

**1. 拉取模型**（示例）：

```bash
mkdir -p ov/models && cd ov

docker run -d \
  --rm \
  --user $(id -u):$(id -g) \
  -v $(pwd)/models:/models \
  openvino/model_server:latest-gpu \
  --pull \
  --model_name openai/gpt-oss-20b \
  --model_repository_path /models \
  --source_model OpenVINO/gpt-oss-20b-int4-ov \
  --task text_generation \
  --tool_parser gptoss \
  --reasoning_parser gptoss \
  --enable_prefix_caching true \
  --target_device GPU
```

> 这会下载模型权重。在继续之前等待容器完成。

**2. 启动服务器**（示例）：

```bash
docker run -d \
  --rm \
  --name ovms \
  --user $(id -u):$(id -g) \
  -p 8000:8000 \
  -v $(pwd)/models:/models \
  --device /dev/dri \
  --group-add=$(stat -c "%g" /dev/dri/render* | head -n 1) \
  openvino/model_server:latest-gpu \
  --rest_port 8000 \
  --model_name openai/gpt-oss-20b \
  --model_repository_path /models \
  --source_model OpenVINO/gpt-oss-20b-int4-ov \
  --task text_generation \
  --tool_parser gptoss \
  --reasoning_parser gptoss \
  --enable_prefix_caching true \
  --target_device GPU
```

**3. 添加到配置**（部分 — 合并到`~/.nanobot/config.json`）：

```json
{
  "providers": {
    "ovms": {
      "apiBase": "http://localhost:8000/v3"
    }
  },
  "agents": {
    "defaults": {
      "provider": "ovms",
      "model": "openai/gpt-oss-20b"
    }
  }
}
```

> OVMS是本地服务器 — 无需API密钥。支持工具调用（`--tool_parser gptoss`）、推理（`--reasoning_parser gptoss`）和流式传输。
> 更多详情请见 [官方OVMS文档](https://docs.openvino.ai/2026/model-server/ovms_docs_llm_quickstart.html)。
</details>

<details>
<summary><b>vLLM (本地 / OpenAI兼容)</b></summary>

用vLLM或任何OpenAI兼容服务器运行您自己的模型，然后添加到配置：

**1. 启动服务器**（示例）：
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

**2. 添加到配置**（部分 — 合并到`~/.nanobot/config.json`）：

*提供商（本地密钥可以是任何非空字符串）：*
```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  }
}
```

*模型：*
```json
{
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

</details>

<details>
<summary><b>添加新提供商（开发者指南）</b></summary>

nanobot使用**提供商注册表**（`nanobot/providers/registry.py`）作为单一事实来源。
添加新提供商只需**2步** — 无需修改if-elif链。

**步骤1.** 在`nanobot/providers/registry.py`的`PROVIDERS`中添加`ProviderSpec`条目：

```python
ProviderSpec(
    name="myprovider",                   # 配置字段名
    keywords=("myprovider", "mymodel"),  # 用于自动匹配的模型名称关键词
    env_key="MYPROVIDER_API_KEY",        # 环境变量名
    display_name="My Provider",          # 在`nanobot status`中显示
    default_api_base="https://api.myprovider.com/v1",  # OpenAI兼容端点
)
```

**步骤2.** 在`nanobot/config/schema.py`的`ProvidersConfig`中添加字段：

```python
class ProvidersConfig(BaseModel):
    ...
    myprovider: ProviderConfig = ProviderConfig()
```

就是这样！环境变量、模型路由、配置匹配和`nanobot status`显示都会自动工作。

**常见的`ProviderSpec`选项：**

| 字段 | 描述 | 示例 |
|-------|-------------|---------|
| `default_api_base` | OpenAI兼容基础URL | `"https://api.deepseek.com"` |
| `env_extras` | 要设置的额外环境变量 | `(("ZHIPUAI_API_KEY", "{api_key}"),)` |
| `model_overrides` | 每个模型的参数覆盖 | `(("kimi-k2.5", {"temperature": 1.0}),)` |
| `is_gateway` | 可以路由任何模型（如OpenRouter） | `True` |
| `detect_by_key_prefix` | 通过API密钥前缀检测网关 | `"sk-or-"` |
| `detect_by_base_keyword` | 通过API基础URL检测网关 | `"openrouter"` |
| `strip_model_prefix` | 发送到网关前剥离提供商前缀 | `True`（对于AiHubMix） |
| `supports_max_completion_tokens` | 使用`max_completion_tokens`而不是`max_tokens`；对于同时设置两者都会被拒绝的提供商是必需的（例如火山引擎） | `True` |

</details>

### 渠道设置

适用于所有渠道的全局设置。在`~/.nanobot/config.json`的`channels`部分下配置：

```json
{
  "channels": {
    "sendProgress": true,
    "sendToolHints": false,
    "sendMaxRetries": 3,
    "telegram": { ... }
  }
}
```

| 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| `sendProgress` | `true` | 将智能体的文本进度流式传输到渠道 |
| `sendToolHints` | `false` | 流式传输工具调用提示（例如`read_file("…")`） |
| `sendMaxRetries` | `3` | 每个出站消息的最大交付尝试次数，包括初始发送（配置0-10，实际至少尝试1次） |

#### 重试行为

重试设计得非常简单。

当渠道`send()`抛出异常时，nanobot在渠道管理器层重试。默认情况下，`channels.sendMaxRetries`为`3`，该计数包括初始发送。

- **尝试1**：立即发送
- **尝试2**：`1s`后重试
- **尝试3**：`2s`后重试
- **更高的重试预算**：回退继续为`1s`、`2s`、`4s`，然后保持上限为`4s`
- **瞬时故障**：网络中断和临时API限制通常在下一次尝试时恢复
- **永久性故障**：无效令牌、访问被撤销或渠道被封禁将耗尽重试预算并干净地失败

> [!NOTE]
> 这种设计是有意的：渠道实现应该在交付失败时抛出异常，渠道管理器拥有共享的重试策略。
>
> 一些渠道可能仍会在内部应用小型的API特定重试。例如，Telegram在向管理器暴露最终失败之前，会单独重试超时和流量控制错误。
>
> 如果渠道完全无法访问，nanobot无法通过同一渠道通知用户。查看日志中的`Failed to send to {channel} after N attempts`以发现持续的交付失败。

### 网页搜索

> [!TIP]
> 在`tools.web`中使用`proxy`将所有网页请求（搜索 + 获取）路由通过代理：
> ```json
> { "tools": { "web": { "proxy": "http://127.0.0.1:7890" } } }
> ```

nanobot支持多个网页搜索提供商。在`~/.nanobot/config.json`的`tools.web.search`下配置。

默认情况下，网页工具已启用，网页搜索使用`duckduckgo`，因此无需API密钥即可开箱即用。

如果您想完全禁用所有内置网页工具，请将`tools.web.enable`设置为`false`。这会从发送给LLM的工具列表中移除`web_search`和`web_fetch`。

如果您需要允许可信的私有范围，例如Tailscale / CGNAT地址，您可以使用`tools.ssrfWhitelist`明确豁免它们免受SSRF阻止：

```json
{
  "tools": {
    "ssrfWhitelist": ["100.64.0.0/10"]
  }
}
```

| 提供商 | 配置字段 | 环境变量回退 | 免费 |
|----------|--------------|------------------|------|
| `brave` | `apiKey` | `BRAVE_API_KEY` | 否 |
| `tavily` | `apiKey` | `TAVILY_API_KEY` | 否 |
| `jina` | `apiKey` | `JINA_API_KEY` | 免费层（10M令牌） |
| `searxng` | `baseUrl` | `SEARXNG_BASE_URL` | 是（自托管） |
| `duckduckgo`（默认） | — | — | 是 |

**禁用所有内置网页工具：**
```json
{
  "tools": {
    "web": {
      "enable": false
    }
  }
}
```

**Brave:**
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "BSA..."
      }
    }
  }
}
```

**Tavily:**
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "tavily",
        "apiKey": "tvly-..."
      }
    }
  }
}
```

**Jina**（免费层10M令牌）：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "jina",
        "apiKey": "jina_..."
      }
    }
  }
}
```

**SearXNG**（自托管，无需API密钥）：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "searxng",
        "baseUrl": "https://searx.example"
      }
    }
  }
}
```

**DuckDuckGo**（零配置）：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "duckduckgo"
      }
    }
  }
}
```

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `enable` | 布尔值 | `true` | 启用或禁用所有内置网页工具（`web_search` + `web_fetch`） |
| `proxy` | 字符串或null | `null` | 所有网页请求的代理，例如`http://127.0.0.1:7890` |

#### `tools.web.search`

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `provider` | 字符串 | `"duckduckgo"` | 搜索后端：`brave`、`tavily`、`jina`、`searxng`、`duckduckgo` |
| `apiKey` | 字符串 | `""` | Brave或Tavily的API密钥 |
| `baseUrl` | 字符串 | `""` | SearXNG的基础URL |
| `maxResults` | 整数 | `5` | 每次搜索的结果数（1–10） |

### MCP（模型上下文协议）

> [!TIP]
> 配置格式与Claude Desktop / Cursor兼容。您可以直接从任何MCP服务器的README复制MCP服务器配置。

nanobot支持[MCP](https://modelcontextprotocol.io/) — 连接外部工具服务器并将它们用作原生智能体工具。

将MCP服务器添加到您的`config.json`：

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
      },
      "my-remote-mcp": {
        "url": "https://example.com/mcp/",
        "headers": {
          "Authorization": "Bearer xxxxx"
        }
      }
    }
  }
}
```

支持两种传输模式：

| 模式 | 配置 | 示例 |
|------|--------|---------|
| **Stdio** | `command` + `args` | 通过`npx` / `uvx`的本地进程 |
| **HTTP** | `url` + `headers`（可选） | 远程端点（`https://mcp.example.com/sse`） |

使用`toolTimeout`为慢速服务器覆盖默认的30秒每次调用超时：

```json
{
  "tools": {
    "mcpServers": {
      "my-slow-server": {
        "url": "https://example.com/mcp/",
        "toolTimeout": 120
      }
    }
  }
}
```

使用`enabledTools`仅注册MCP服务器的部分工具：

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
        "enabledTools": ["read_file", "mcp_filesystem_write_file"]
      }
    }
  }
}
```

`enabledTools`接受原始MCP工具名称（例如`read_file`）或包装的nanobot工具名称（例如`mcp_filesystem_write_file`）。

- 省略`enabledTools`，或将其设置为`["*"]`，以注册所有工具。
- 将`enabledTools`设置为`[]`以不注册该服务器的任何工具。
- 将`enabledTools`设置为非空名称列表以仅注册该子集。

MCP工具在启动时自动发现和注册。LLM可以与内置工具一起使用它们 — 无需额外配置。

### 安全

> [!TIP]
> 对于生产部署，在配置中设置`"restrictToWorkspace": true`以沙箱化智能体。
> 在`v0.1.4.post3`及更早版本中，空`allowFrom`允许所有发送者。从`v0.1.4.post4`开始，空`allowFrom`默认拒绝所有访问。要允许所有发送者，请设置`"allowFrom": ["*"]`。

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `tools.restrictToWorkspace` | `false` | 当为`true`时，限制**所有**智能体工具（shell、文件读/写/编辑、列表）到工作区目录。防止路径遍历和范围外访问。 |
| `tools.exec.enable` | `true` | 当为`false`时，shell`exec`工具根本不注册。使用此选项完全禁用shell命令执行。 |
| `tools.exec.pathAppend` | `""` | 运行shell命令时附加到`PATH`的额外目录（例如`/usr/sbin`用于`ufw`）。 |
| `channels.*.allowFrom` | `[]`（拒绝所有） | 用户ID白名单。空则拒绝所有；使用`["*"]`允许所有人。 |

### 时区

时间是上下文。上下文应该精确。

默认情况下，nanobot使用`UTC`作为运行时时间上下文。如果您希望智能体以您的本地时间思考，请将`agents.defaults.timezone`设置为有效的[IANA时区名称](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)：

```json
{
  "agents": {
    "defaults": {
      "timezone": "Asia/Shanghai"
    }
  }
}
```

这会影响显示给模型的运行时时间字符串，例如运行时上下文和心跳提示。它也成为cron计划在cron表达式省略`tz`时的默认时区，以及ISO日期时间没有显式偏移时一次性`at`时间的默认时区。

常见示例：`UTC`、`America/New_York`、`America/Los_Angeles`、`Europe/London`、`Europe/Berlin`、`Asia/Tokyo`、`Asia/Shanghai`、`Asia/Singapore`、`Australia/Sydney`。

> 需要其他时区？浏览完整的[IANA时区数据库](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。

## 🧩 多实例

同时运行多个nanobot实例，使用独立的配置和运行时数据。使用`--config`作为主要入口点。在`onboard`期间可选传递`--workspace`，当您想要为特定实例初始化或更新保存的工作区时。

### 快速开始

如果您希望每个实例从一开始就有自己的专用工作区，请在引导过程中同时传递`--config`和`--workspace`。

**初始化实例：**

```bash
# 创建独立的实例配置和工作区
nanobot onboard --config ~/.nanobot-telegram/config.json --workspace ~/.nanobot-telegram/workspace
nanobot onboard --config ~/.nanobot-discord/config.json --workspace ~/.nanobot-discord/workspace
nanobot onboard --config ~/.nanobot-feishu/config.json --workspace ~/.nanobot-feishu/workspace
```

**配置每个实例：**

编辑`~/.nanobot-telegram/config.json`、`~/.nanobot-discord/config.json`等，使用不同的渠道设置。您在`onboard`期间传递的工作区会保存到每个配置中，作为该实例的默认工作区。

**运行实例：**

```bash
# 实例A - Telegram机器人
nanobot gateway --config ~/.nanobot-telegram/config.json

# 实例B - Discord机器人  
nanobot gateway --config ~/.nanobot-discord/config.json

# 实例C - 飞书机器人，使用自定义端口
nanobot gateway --config ~/.nanobot-feishu/config.json --port 18792
```

### 路径解析

使用`--config`时，nanobot从配置文件位置派生其运行时数据目录。工作区仍然来自`agents.defaults.workspace`，除非您用`--workspace`覆盖它。

要在本地打开针对其中一个实例的CLI会话：

```bash
nanobot agent -c ~/.nanobot-telegram/config.json -m "Hello from Telegram instance"
nanobot agent -c ~/.nanobot-discord/config.json -m "Hello from Discord instance"

# 可选的一次性工作区覆盖
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test
```

> `nanobot agent`使用选定的工作区/配置启动本地CLI智能体。它不会附加到或代理已经运行的`nanobot gateway`进程。

| 组件 | 解析来源 | 示例 |
|-----------|---------------|---------|
| **配置** | `--config`路径 | `~/.nanobot-A/config.json` |
| **工作区** | `--workspace`或配置 | `~/.nanobot-A/workspace/` |
| **Cron任务** | 配置目录 | `~/.nanobot-A/cron/` |
| **媒体 / 运行时状态** | 配置目录 | `~/.nanobot-A/media/` |

### 工作原理

- `--config`选择要加载的配置文件
- 默认情况下，工作区来自该配置中的`agents.defaults.workspace`
- 如果您传递`--workspace`，它会覆盖配置文件中的工作区

### 最小设置

1. 将您的基础配置复制到新的实例目录。
2. 为该实例设置不同的`agents.defaults.workspace`。
3. 使用`--config`启动实例。

示例配置：

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot-telegram/workspace",
      "model": "anthropic/claude-sonnet-4-6"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TELEGRAM_BOT_TOKEN"
    }
  },
  "gateway": {
    "port": 18790
  }
}
```

启动独立实例：

```bash
nanobot gateway --config ~/.nanobot-telegram/config.json
nanobot gateway --config ~/.nanobot-discord/config.json
```

需要时为一次性运行覆盖工作区：

```bash
nanobot gateway --config ~/.nanobot-telegram/config.json --workspace /tmp/nanobot-telegram-test
```

### 常见用例

- 为Telegram、Discord、飞书和其他平台运行独立的机器人
- 保持测试和生产实例隔离
- 为不同团队使用不同的模型或提供商
- 为多个租户提供独立的配置和运行时数据

### 注意事项

- 如果同时运行，每个实例必须使用不同的端口
- 如果您想要隔离的内存、会话和技能，请为每个实例使用不同的工作区
- `--workspace`覆盖配置文件中定义的工作区
- Cron任务和运行时媒体/状态从配置目录派生

## 🧠 内存

nanobot使用分层内存系统，旨在保持轻量实时和持久长期。

- `memory/history.jsonl`存储仅追加的摘要历史
- `SOUL.md`、`USER.md`和`memory/MEMORY.md`存储由Dream管理的长期知识
- `Dream`按计划运行，也可以手动触发
- 内存更改可以通过内置命令检查和恢复

如果您想要完整的设计，请参见[docs/MEMORY.md](docs/MEMORY.md)。

## 💻 CLI参考

| 命令 | 描述 |
|---------|-------------|
| `nanobot onboard` | 在`~/.nanobot/`初始化配置和工作区 |
| `nanobot onboard --wizard` | 启动交互式引导向导 |
| `nanobot onboard -c <config> -w <workspace>` | 初始化或刷新特定实例配置和工作区 |
| `nanobot agent -m "..."` | 与智能体聊天 |
| `nanobot agent -w <workspace>` | 针对特定工作区聊天 |
| `nanobot agent -w <workspace> -c <config>` | 针对特定工作区/配置聊天 |
| `nanobot agent` | 交互式聊天模式 |
| `nanobot agent --no-markdown` | 显示纯文本回复 |
| `nanobot agent --logs` | 聊天期间显示运行时日志 |
| `nanobot serve` | 启动OpenAI兼容API |
| `nanobot gateway` | 启动网关 |
| `nanobot status` | 显示状态 |
| `nanobot provider login openai-codex` | 提供商的OAuth登录 |
| `nanobot channels login <channel>` | 交互式认证渠道 |
| `nanobot channels status` | 显示渠道状态 |

交互式模式退出：`exit`、`quit`、`/exit`、`/quit`、`:q`或`Ctrl+D`。

## 💬 聊天内命令

这些命令在聊天渠道和交互式智能体会话中有效：

| 命令 | 描述 |
|---------|-------------|
| `/new` | 开始新对话 |
| `/stop` | 停止当前任务 |
| `/restart` | 重启机器人 |
| `/status` | 显示机器人状态 |
| `/dream` | 立即运行Dream内存整合 |
| `/dream-log` | 显示最新的Dream内存更改 |
| `/dream-log <sha>` | 显示特定的Dream内存更改 |
| `/dream-restore` | 列出最近的Dream内存版本 |
| `/dream-restore <sha>` | 将内存恢复到特定更改之前的状态 |
| `/help` | 显示可用的聊天内命令 |

<details>
<summary><b>心跳（周期性任务）</b></summary>

网关每30分钟唤醒一次并检查工作区（`~/.nanobot/workspace/HEARTBEAT.md`）中的`HEARTBEAT.md`。如果文件有任务，智能体执行它们并将结果交付到您最近活动的聊天渠道。

**设置：** 编辑`~/.nanobot/workspace/HEARTBEAT.md`（由`nanobot onboard`自动创建）：

```markdown
## 周期性任务

- [ ] 检查天气预报并发送摘要
- [ ] 扫描收件箱中的紧急电子邮件
```

智能体也可以自己管理这个文件 — 让它"添加一个周期性任务"，它会为您更新`HEARTBEAT.md`。

> **注意：** 网关必须正在运行（`nanobot gateway`），并且您必须至少与机器人聊过一次，以便它知道交付到哪个渠道。

</details>

## 🐍 Python SDK

将nanobot用作库 — 无需CLI，无需网关，只需Python：

```python
from nanobot import Nanobot

bot = Nanobot.from_config()
result = await bot.run("Summarize the README")
print(result.content)
```

每个调用携带一个`session_key`用于对话隔离 — 不同的密钥获得独立的历史：

```python
await bot.run("hi", session_key="user-alice")
await bot.run("hi", session_key="task-42")
```

添加生命周期钩子来观察或自定义智能体：

```python
from nanobot.agent import AgentHook, AgentHookContext

class AuditHook(AgentHook):
    async def before_execute_tools(self, ctx: AgentHookContext) -> None:
        for tc in ctx.tool_calls:
            print(f"[tool] {tc.name}")

result = await bot.run("Hello", hooks=[AuditHook()])
```

完整的SDK参考请见[docs/PYTHON_SDK.md](docs/PYTHON_SDK.md)。

## 🔌 OpenAI兼容API

nanobot可以暴露一个最小的OpenAI兼容端点用于本地集成：

```bash
pip install "nanobot-ai[api]"
nanobot serve
```

默认情况下，API绑定到`127.0.0.1:8900`。您可以在`config.json`中更改它。

### 行为

- 会话隔离：在请求体中传递`"session_id"`来隔离对话；省略则使用共享的默认会话（`api:default`）
- 单消息输入：每个请求必须恰好包含一条`user`消息
- 固定模型：省略`model`，或传递`/v1/models`显示的相同模型
- 无流式传输：不支持`stream=true`

### 端点

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

### curl

```bash
curl http://127.0.0.1:8900/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "hi"}],
    "session_id": "my-session"
  }'
```

### Python (`requests`)

```python
import requests

resp = requests.post(
    "http://127.0.0.1:8900/v1/chat/completions",
    json={
        "messages": [{"role": "user", "content": "hi"}],
        "session_id": "my-session",  # 可选：隔离对话
    },
    timeout=120,
)
resp.raise_for_status()
print(resp.json()["choices"][0]["message"]["content"])
```

### Python (`openai`)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8900/v1",
    api_key="dummy",
)

resp = client.chat.completions.create(
    model="MiniMax-M2.7",
    messages=[{"role": "user", "content": "hi"}],
    extra_body={"session_id": "my-session"},  # 可选：隔离对话
)
print(resp.choices[0].message.content)
```

## 🐳 Docker

> [!TIP]
> `-v ~/.nanobot:/root/.nanobot`标志将您的本地配置目录挂载到容器中，因此您的配置和工作区在容器重启后仍然存在。

### Docker Compose

```bash
docker compose run --rm nanobot-cli onboard   # 首次设置
vim ~/.nanobot/config.json                     # 添加API密钥
docker compose up -d nanobot-gateway           # 启动网关
```

```bash
docker compose run --rm nanobot-cli agent -m "Hello!"   # 运行CLI
docker compose logs -f nanobot-gateway                   # 查看日志
docker compose down                                      # 停止
```

### Docker

```bash
# 构建镜像
docker build -t nanobot .

# 初始化配置（仅首次）
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard

# 在主机上编辑配置添加API密钥
vim ~/.nanobot/config.json

# 运行网关（连接到启用的聊天渠道，例如Telegram/Discord/Mochat）
docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway

# 或运行单个命令
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot agent -m "Hello!"
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot status
```

## 🐧 Linux服务

将网关作为systemd用户服务运行，使其自动启动并在失败时重启。

**1. 找到nanobot二进制路径：**

```bash
which nanobot   # 例如 /home/user/.local/bin/nanobot
```

**2. 创建服务文件**到`~/.config/systemd/user/nanobot-gateway.service`（如果需要，替换`ExecStart`路径）：

```ini
[Unit]
Description=Nanobot Gateway
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h

[Install]
WantedBy=default.target
```

**3. 启用并启动：**

```bash
systemctl --user daemon-reload
systemctl --user enable --now nanobot-gateway
```

**常见操作：**

```bash
systemctl --user status nanobot-gateway        # 检查状态
systemctl --user restart nanobot-gateway       # 配置更改后重启
journalctl --user -u nanobot-gateway -f        # 跟踪日志
```

如果您编辑`.service`文件本身，请在重启前运行`systemctl --user daemon-reload`。

> **注意：** 用户服务仅在您登录时运行。要在注销后保持网关运行，请启用逗留：
>
> ```bash
> loginctl enable-linger $USER
> ```

## 📁 项目结构

```
nanobot/
├── agent/          # 🧠 核心智能体逻辑
│   ├── loop.py     #    智能体循环（LLM ↔ 工具执行）
│   ├── context.py  #    提示构建器
│   ├── memory.py   #    持久内存
│   ├── skills.py   #    技能加载器
│   ├── subagent.py #    后台任务执行
│   └── tools/      #    内置工具（包括spawn）
├── skills/         # 🎯 捆绑技能（github、weather、tmux...）
├── channels/       # 📱 聊天渠道集成（支持插件）
├── bus/            # 🚌 消息路由
├── cron/           # ⏰ 计划任务
├── heartbeat/      # 💓 主动唤醒
├── providers/      # 🤖 LLM提供商（OpenRouter等）
├── session/        # 💬 会话管理
├── config/         # ⚙️ 配置
└── cli/            # 🖥️ 命令
```

## 🤝 贡献与路线图

欢迎PR！代码库故意做得很小且可读。🤗

### 分支策略

| 分支 | 用途 |
|--------|---------|
| `main` | 稳定版本 — 错误修复和小改进 |
| `nightly` | 实验性功能 — 新功能和破坏性更改 |

**不确定要针对哪个分支？** 详情请见[CONTRIBUTING.md](./CONTRIBUTING.md)。

**路线图** — 选择一个项目并[提交PR](https://github.com/HKUDS/nanobot/pulls)！

- [ ] **多模态** — 视觉和听觉（图像、语音、视频）
- [ ] **长期记忆** — 永不忘记重要上下文
- [ ] **更好的推理** — 多步规划和反思
- [ ] **更多集成** — 日历等
- [ ] **自我改进** — 从反馈和错误中学习

### 贡献者

<a href="https://github.com/HKUDS/nanobot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/nanobot&max=100&columns=12&updated=20260210" alt="贡献者" />
</a>

## ⭐ 星标历史

<div align="center">
  <a href="https://star-history.com/#HKUDS/nanobot&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date" />
      <img alt="星标历史图表" src="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date" style="border-radius: 15px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);" />
    </picture>
  </a>
</div>

<p align="center">
  <em> 感谢访问 ✨ nanobot！</em><br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.nanobot&style=for-the-badge&color=00d4ff" alt="访问量">
</p>

<p align="center">
  <sub>nanobot仅用于教育、研究和技术交流目的</sub>
</p>
