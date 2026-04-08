---
name: yoyo
description: 全能私人秘书 yoyo
metadata: '{"type": "python_module", "module": "nanobot.skills.yoyo", "entry_points": {"handle": "handle", "scheduled_tasks": "get_scheduled_tasks"}}'
---

## 脚本调用帮助

使用方式：`python3 -m nanobot.skills.yoyo --help`

## 检查配置（非常重要）

你需要先检查 `~/.nanobot/config.json` 的 `personal_secretary.data_dir` 配置是否是合法路径。

如果不合法则询问用户 "是否需要配置自定义事项存储目录？"。
用户回答：
- 是或表达肯定。则先检查自定义目录是否有效，无效提醒用户重新设置一个有效合法的目录，
  有效则将用户配置写入`personal_secretary.data_dir`，然后正常走下一步流程。
- 否/或表达否定。则配置默认目录 `~/.nanobot/workspace/personal-secretary/`。

## 配置项参考

可在 `~/.nanobot/config.json` 的 `personal_secretary` 中设置：

| 字段 | 默认值 | 说明 |
|-----|-------|-----|
| data_dir | ~/.nanobot/workspace/personal-secretary/ | 数据存储目录 |
| remind_time_morning | "08:00" | 早报推送时间 |
| remind_time_evening | "21:00" | 晚报推送时间 |
| auto_classify_delay | 5 | 自动分类延迟（分钟） |
| remind_long_term_interval | 3 | 长期事项回顾间隔（天） |
| remind_weekly_time | "星期日 20:00" | 周度回顾时间 |
| auto_backup | true | 是否自动备份 |

## 消息处理（handle函数）

handle 函数会自动从消息中识别用户意图并分发处理。消息可以包含前缀 `yoyo`，handle 会自动忽略。

### 支持的意图

| 用户意图 | 触发关键词示例 | 处理结果 |
|---------|--------------|---------|
| **记录内容** | `记录 xxx`、`记下 xxx`、`保存到 inbox xxx`、`帮我把这个保存到 inbox xxx` | 保存到收件箱，自动分类（todo/note/link等） |
| **查看今日待办** | `今日待办`、`今日任务`、`我的今日待办`、`今天任务` | 返回今日任务清单 |
| **搜索记录** | `搜索 xxx`、`查询 xxx`、`找 xxx` | 返回匹配的记录列表 |
| **标记任务完成** | `完成 xxx`、`搞定 xxx`、`做完了 xxx` | 标记任务为已完成 |
| **记录习惯** | `养成 xxx 习惯`、`习惯 xxx`、`每天 xxx` | 保存到 `04-Events/habits.md` 的每日习惯列表 |
| **生成日报** | `今日日报`、`今天日报`、`今日回顾` | 生成并保存日报到 `07-Reports/Daily/` |
| **生成周报** | `本周周报`、`周报` | 生成并保存周报到 `07-Reports/Weekly/` |

### 重要说明

1. **yoyo 前缀**：用户消息可以以 `yoyo`、`yoyo，`、`yoyo：` 等开头，handle 会自动去除后再匹配
2. **关键词位置**：关键词可以在消息任意位置，不需要在开头
3. **data_dir 配置**：所有文件会保存到 `~/.nanobot/config.json` 中 `personal_secretary.data_dir` 指定的目录
4. **自动分类**：记录内容时会根据关键词自动识别为 todo/note/link/event 等类型

## 定时任务（get_scheduled_tasks）

| 触发时间 | 任务名 | 处理函数 |
|---------|-------|---------|
| 每日8:00 | morning-brief | _send_morning_brief |
| 每日21:00 | evening-brief | _send_evening_brief + generate_daily_report |
| 每3天19:00 | long-term-review | _send_long_term_review |
| 每周日20:00 | weekly-review | _send_weekly_review + generate_weekly_report |
| 每月1日3:00 | monthly-backup | generate_monthly_report + backup_data |
| 每分钟 | check-upcoming | 检查到期任务并发提醒 |

## 详细参考

- **存储格式规范**: See [references/storage_schema.md](references/storage_schema.md)
- **GTD工作流说明**: See [references/gtd_workflow.md](references/gtd_workflow.md)
- **Kanban格式规范**: See [references/kanban_format.md](references/kanban_format.md)
