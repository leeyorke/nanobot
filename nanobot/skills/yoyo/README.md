# 私人秘书技能

全能私人秘书技能，基于nanobot框架实现"想法随时记录→自动组织→每日提醒→定期回顾→历史查询"完整工作流，完全兼容Obsidian知识库和GTD工作流。

## 功能特性

### ✨ 核心能力
1. **随时记录**：支持自然语言记录任何内容（想法、待办、灵感、链接、资源等）
2. **自动分类**：基于GTD工作流自动分类待办事项，支持6类任务划分
3. **智能提醒**：每日早报/晚报、待办到期提醒、定期回顾提醒
4. **历史查询**：多维度搜索历史记录（关键词、时间、分类、标签、状态）
5. **Obsidian兼容**：存储格式完全兼容Obsidian知识库，支持双链、Kanban、标签等特性

### 📅 自动提醒
- **每日8:00**：推送当日待办清单
- **每日21:00**：推送当日日报和未完成任务处理提醒
- **每3天**：长期事项回顾提醒
- **每周日20:00**：周度回顾提醒
- **待办到期前30分钟**：自动提醒
- **日程开始前1小时**：自动提醒
- **每月1日**：自动数据备份和月报生成

### 📁 存储结构
完全兼容Obsidian目录结构，可以直接作为Obsidian库目录使用：
```
~/.nanobot/workspace/personal-secretary/
├── 01-Inbox/                  # 收件箱
├── 02-Tasks/                  # GTD待办分类
├── 03-Notes/                  # 笔记分类
├── 04-Events/                 # 活动和习惯
├── 05-Resources/              # 资源收藏
├── 06-Tags/                   # 标签索引
├── 07-Reports/                # 自动生成的报告
└── 📋 kanban.md               # GTD看板（兼容Obsidian Kanban插件）
```

## 安装使用

### 1. 安装依赖
```bash
pip install pyyaml jinja2
```

### 2. 配置（可选）
在`~/.nanobot/config.json`中添加配置：
```json
{
  "personal_secretary": {
    "data_dir": "~/Documents/Obsidian/MyVault",  # 自定义存储路径，可选，默认是~/.nanobot/workspace/personal-secretary/
    "auto_classify_delay": 5,
    "remind_time_morning": "08:00",
    "remind_time_evening": "21:00"
  }
}
```

### 3. 使用示例
```
> 帮我记一下明天下午3点开需求评审会，准备PPT
✅ 已成功记录到收件箱！
📝 内容：明天下午3点开需求评审会，准备PPT
🏷️ 类型：todo (置信度: 0.90)
⏰ 时间：2026-04-08 15:00
🚀 已自动识别为待办事项，将进行GTD分类并同步到Kanban

> 今日任务
🌞 早上好！今天是 2026-04-07 Sunday

📋 今日待办清单：

📅 今日日程（共1个）：
1. 明天下午3点开需求评审会，准备PPT ⏰ 15:00

💪 今日共有 1 个待办任务，加油！

> 完成 需求评审
✅ 已标记任务为完成！
📝 任务内容：- [ ] 明天下午3点开需求评审会，准备PPT...
📂 已归档到：~/.nanobot/workspace/personal-secretary/02-Tasks/Completed/Inbox-1719389286.md

> 搜索 需求
🔍 找到 2 条相关记录：

1. [2026-04-07 10:30] [todo] 待办：明天下午3点开需求评审...
2. [2026-04-05 16:20] [note] 笔记：需求文档评审会议记录...

> 今日日报
📰 今日日报已生成！
📂 文件路径：~/.nanobot/workspace/personal-secretary/07-Reports/Daily/Report-Daily-2026-04-07.md

# 日报：2026-04-07

## 📊 概览
- 新增记录：3 条
- 完成任务：1 个
- 待完成任务：0 个
...
```

## GTD工作流
支持6类任务自动分类：
- ⚡ **立即做**：2小时内能完成的紧急任务
- 🚶 **下一步行动**：有明确下一步动作的任务
- 📅 **日程**：有具体日期时间的安排
- ⏳ **等待中**：需要等待他人或外部条件的任务
- 📦 **项目**：需要多步骤完成的大项目
- 🔮 **将来做**：未来某一天要做的，暂无明确时间的任务

所有任务会自动同步到`📋 kanban.md`文件，完全兼容Obsidian Kanban插件，可以直接在Obsidian中拖拽修改任务状态，系统会自动双向同步。

## 目录说明
```
personal-secretary/
├── SKILL.md              # 技能配置文件
├── README.md             # 说明文档
├── main.py               # 主入口文件
├── __init__.py           # 包初始化
├── scripts/              # 功能模块
│   ├── inbox_operations.py    # 收件箱增删改查
│   ├── content_classifier.py  # 内容分类和元数据提取
│   ├── gtd_classifier.py      # GTD待办分类和Kanban同步
│   ├── todo_generator.py      # 待办生成和提醒
│   └── review_reminder.py     # 报告生成和回顾提醒
├── references/           # 参考文档
│   ├── storage_schema.md      # 存储格式规范
│   ├── gtd_workflow.md        # GTD工作流说明
│   └── kanban_format.md       # Kanban格式规范
└── assets/               # 模板文件
    ├── kanban_template.md     # Kanban模板
    └── report_template.md     # 报告模板
```
