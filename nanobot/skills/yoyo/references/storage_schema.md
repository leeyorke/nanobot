# 存储格式规范

## 目录结构
```
{data_dir}/
├── 01-Inbox/                  # 收件箱，新记录默认存这里
├── 02-Tasks/                  # GTD待办事项分类
│   ├── Pending/                # 待分类处理的待办
│   ├── Now/                    # 立即做（2小时内能完成的紧急任务）
│   ├── Next/                   # 下一步（有明确下一步动作的任务）
│   ├── Calendar/               # 日程（有明确时间的安排）
│   ├── Waiting/                # 等待中（需要等待他人或外部条件的任务）
│   ├── Projects/               # 项目（需要多步骤完成的大项目）
│   ├── Someday/                # 将来做（未来某一天要做的任务）
│   ├── Completed/              # 已完成（已经完成的任务归档）
│   └── Deleted/                # 已删除（取消/删除的任务归档）
├── 03-Notes/                  # 笔记分类
│   ├── Memo/                   # 随想/灵感/句子/摘录
│   ├── Daily/                  # 日记
│   └── Learn/                  # 学习笔记
├── 04-Events/                  # 习惯及活动分类
│   ├── habits.md               # 习惯跟踪（固定文件）
│   ├── hello.md                # 每日语录（固定文件）
│   └── Activities/             # 活动/出行/聚会/纪念日记录
├── 05-Resources/               # 资源收藏分类
│   ├── Links/                  # 网页链接/GitHub仓库/文章帖子
│   ├── Scripts/                # 各类脚本
│   ├── Assets/                 # 截图/图片/文件等二进制资源
│   └── Docs/                   # Markdown文档/电子书等
├── 06-Tags/                    # 自动生成的标签索引
├── 07-Reports/                 # 自动生成的报告
│   ├── Daily/                  # 每日日报
│   ├── Weekly/                 # 每周周报/回顾
│   ├── Monthly/                # 每月月报
│   └── Review/                 # 各类回顾报告
├── 📋 kanban.md               # GTD看板文件（兼容Obsidian Kanban插件）
└── ⚙️ .metadata/              # 系统配置目录（隐藏）
    ├── category_rules.json     # 内容分类规则
    ├── schedule_config.json    # 定时提醒配置
    ├── gtd_config.json        # GTD分类规则配置
    └── backups/                # 自动备份目录
```

## 文件命名规则
### 动态生成文件
`{父目录名}-10位时间戳.后缀名`
- 示例：`Memo-1719389286.md`、`Link-1719389286.md`
- 时间戳为Unix时间戳（秒级），保证文件名唯一性
- 分类名对应所属目录的分类：Inbox/Memo/Daily/Task/Link等

### 固定文件
- habits.md：习惯跟踪
- hello.md：每日语录
- 📋 kanban.md：GTD看板

## 记录文件格式
每条记录为独立的Markdown文件，包含YAML frontmatter和正文内容：

```markdown
---
id: uuid-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
timestamp: 2026-04-07T10:30:00+08:00
content_type: todo # 可选值：todo/note/link/event/resource
source: user_input # 来源：user_input/auto_generated/imported
status: unclassified # 状态：unclassified/pending/processing/completed/deleted
priority: high # 优先级：high/medium/low（待办/日程专有）
due_date: 2026-04-08T15:00:00+08:00 # 待办/日程专有，截止时间
tags: [工作, 会议, 项目A] # 标签列表
---

# 待办：明天下午3点开需求评审会

- [ ] 明天下午3点和产品团队开需求评审会，记得准备PPT
```

### 元数据字段说明
| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 全局唯一UUID |
| timestamp | string | 是 | ISO格式的创建时间（带时区） |
| content_type | string | 是 | 内容类型：todo/note/link/event/resource |
| source | string | 是 | 记录来源 |
| status | string | 是 | 记录状态 |
| priority | string | 否 | 优先级（仅待办/日程） |
| due_date | string | 否 | 截止时间（仅待办/日程，ISO格式） |
| tags | array | 否 | 标签列表 |

## 元数据配置文件格式
### category_rules.json（内容分类规则）
```json
{
  "content_types": {
    "todo": ["todo", "待办", "任务", "需要做"],
    "note": ["笔记", "记录", "想法", "灵感"],
    "link": ["http://", "https://", "网址", "链接"],
    "event": ["会议", "约会", "聚会", "活动"],
    "resource": ["资源", "资料", "文档", "工具"]
  }
}
```

### schedule_config.json（定时提醒配置）
```json
{
  "remind_morning": "08:00",
  "remind_evening": "21:00",
  "remind_long_term_days": 3,
  "remind_weekly": "Sunday 20:00",
  "auto_backup": true
}
```

### gtd_config.json（GTD分类规则配置）
```json
{
  "classification_rules": {
    "Now": {"max_duration": 120, "priority": "high"},
    "Next": {"has_next_action": true},
    "Calendar": {"has_due_date": true},
    "Waiting": {"depend_on_others": true},
    "Projects": {"needs_multiple_steps": true},
    "Someday": {"no_clear_time": true}
  }
}
```
