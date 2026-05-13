#!/usr/bin/env python3
"""
私人秘书技能主入口
"""

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from loguru import logger

from .scripts.content_classifier import ContentClassifier
from .scripts.gtd_classifier import GTDClassifier
from .scripts.helpers import dump_frontmatter, parse_frontmatter
from .scripts.inbox_operations import InboxOperations
from .scripts.review_reminder import ReviewReminder
from .scripts.todo_generator import TodoGenerator

# 北京时间时区
TZ = timezone(timedelta(hours=8))

# 全局实例
inbox_ops = None
content_classifier = None
gtd_classifier = None
todo_generator = None
review_reminder = None
_last_config = None


def _init_instances(config):
    """初始化所有实例，支持 config 变化时自动重新初始化"""
    global \
        inbox_ops, \
        content_classifier, \
        gtd_classifier, \
        todo_generator, \
        review_reminder, \
        _last_config

    # config 对象变化时（多实例场景），强制重新初始化
    if inbox_ops is not None and config is not _last_config:
        inbox_ops = None

    if inbox_ops is None:
        inbox_ops = InboxOperations(config)
        content_classifier = ContentClassifier(inbox_ops.data_dir, config)
        gtd_classifier = GTDClassifier(inbox_ops.data_dir, config)
        todo_generator = TodoGenerator(inbox_ops.data_dir, config)
        review_reminder = ReviewReminder(inbox_ops.data_dir, config)
        _last_config = config


def first_check(context):
    def is_directory_empty(path):
        directory = Path(path).expanduser().resolve()
        if not directory.exists():
            return True
        if not directory.is_dir():
            return True
        return len(list(directory.iterdir())) == 0

    # 获取config：优先从context获取，否则自己加载，并存回context
    config = context.get("config")
    if config is None:
        from nanobot.config.loader import load_config

        config = load_config()
        context["config"] = config  # 存回context供后续使用

    _init_instances(config)
    # 初次启用检查：若 data_dir 为默认路径且为空，先询问用户配置
    # config 可能是 dict 或 Pydantic 模型，需要兼容处理
    if hasattr(config, "personal_secretary"):
        ps = config.personal_secretary
        data_dir = str(ps.data_dir) if hasattr(ps, "data_dir") and ps.data_dir else ""
    elif isinstance(config, dict):
        ps_config = config.get("personal_secretary") or {}
        data_dir = ps_config.get("data_dir", "") if isinstance(ps_config, dict) else ""
    else:
        data_dir = ""
    default_dir = "~/.nanobot/workspace/personal-secretary/"

    resolved = str(Path(data_dir).expanduser().resolve()) if data_dir else ""
    if not resolved and not is_directory_empty(default_dir):
        return (
            "👋 初次启用yoyo私人秘书，请告诉我你希望数据保存在哪个目录？\n"
            "例如：`~/Documents/Obsidian/MyVault` 或直接回车使用默认路径 `~/.nanobot/workspace/personal-secretary/`"
        )


async def _classify_intent(message: str, context: dict) -> dict:
    """LLM 判断意图及提取参数，返回 dict {"intent": "...", ...}"""

    try:
        provider = context["loop"].provider
        model = context["loop"].model
    except (KeyError, AttributeError):
        return {"intent": "ask_user"}

    # 读取已定义的习惯名称，帮助 LLM 识别打卡
    habit_names = ", ".join(todo_generator.get_habit_definitions()) if todo_generator else ""

    prompt = f"""你是一个意图路由器，根据用户消息判断意图并提取参数。

可用意图及对应参数：
- record: 记录内容到收件箱。返回 content（用户要记的内容）。
  例："记录明天下午3点开会" → {{"intent": "record", "content": "明天下午3点开会"}}
- query_today: 查看今日待办。无额外参数。
- search: 搜索历史。返回 query（搜索词）。
  例："搜索上周的会议笔记" → {{"intent": "search", "query": "上周的会议笔记"}}
- view_habits: 查看今日习惯完成情况。无额外参数。
  例："我今天完成了哪些习惯"
- record_habit: 添加新习惯。返回 habit（习惯名）。
  例："养成每天跑步的习惯" → {{"intent": "record_habit", "habit": "每天跑步"}}
- habit_checkin: 打卡完成习惯。返回 habits（习惯名列表，可多个）。
  注意：habits 中的名称必须从"已定义的习惯"列表中选取，不能自己缩写。
  例：如果已定义的习惯是["每天吃一个鸡蛋", "阅读"]，用户说"鸡蛋吃过了"→{{"intent": "habit_checkin", "habits": ["每天吃一个鸡蛋"]}}
- habit_stats: 查看习惯统计。无额外参数。
- mark_done: 标记任务完成。返回 tasks（任务关键词列表，可多个）。
  例："完成了会议纪要" → {{"intent": "mark_done", "tasks": ["会议纪要"]}}
  例："会议纪要、需求文档都搞定了" → {{"intent": "mark_done", "tasks": ["会议纪要", "需求文档"]}}
- generate_report: 生成日报。无额外参数。
- ask_user: 以上都不匹配时返回此值。

已定义的习惯（必须使用这里面的完整名称）：{habit_names}

用户消息：{message}

返回纯 JSON，不要 markdown 包裹。"""

    try:
        response = await provider.chat(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0,
            max_tokens=2048,
        )
        logger.debug(
            f"[yoyo] LLM 原始响应: content={response.content!r}, finish_reason={response.finish_reason!r}"
        )
        text = (response.content or "").strip()
        # 适配可能的 markdown 代码块
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        result = json.loads(text)
        intent = result.get("intent", "ask_user")
        valid = {
            "record",
            "query_today",
            "search",
            "view_habits",
            "record_habit",
            "habit_checkin",
            "habit_stats",
            "mark_done",
            "generate_report",
            "ask_user",
        }
        if intent not in valid:
            return {"intent": "ask_user"}

        # 校验各意图的必填参数
        if intent == "habit_checkin":
            habits = result.get("habits", [])
            if isinstance(habits, list) and habits:
                return {"intent": "habit_checkin", "habits": habits}
            return {"intent": "ask_user"}

        if intent == "record":
            content = (result.get("content") or "").strip()
            if content:
                return {"intent": "record", "content": content}
            return {"intent": "ask_user"}

        if intent == "search":
            query = (result.get("query") or "").strip()
            if query:
                return {"intent": "search", "query": query}
            return {"intent": "ask_user"}

        if intent == "record_habit":
            habit = (result.get("habit") or "").strip()
            if habit:
                return {"intent": "record_habit", "habit": habit}
            return {"intent": "ask_user"}

        if intent == "mark_done":
            tasks = result.get("tasks", [])
            if isinstance(tasks, list) and tasks:
                return {"intent": "mark_done", "tasks": tasks}
            return {"intent": "ask_user"}

        return {"intent": intent}
    except Exception as e:
        logger.warning(f"[yoyo] LLM 意图分类失败: {e}")
        return {"intent": "ask_user"}


async def handle(message, context):
    """
    处理用户消息
    :param message: 用户输入的消息文本
    :param context: 上下文对象，包含config、send_message等方法
    :return: 回复消息
    """
    logger.info(f"[yoyo] 收到消息: {message[:50]}...")

    # first_check 会处理 config 加载并存入context
    hint = first_check(context)
    if hint:
        logger.info("[yoyo] 返回初次配置提示")
        return hint

    # 从context获取config（first_check已加载并存入）
    config = context.get("config")
    _init_instances(config)

    message_lower = message.lower()

    # 去掉开头的 "yoyo" 前缀（不区分大小写），保留剩余部分做匹配
    msg_stripped = re.sub(r"^yoyo[，,\s]+", "", message_lower, flags=re.IGNORECASE)
    msg_original_stripped = re.sub(r"^yoyo[，,\s]+", "", message, flags=re.IGNORECASE)

    # LLM 意图分类
    result = await _classify_intent(message, context)
    intent = result["intent"]
    logger.info(f"[yoyo] 意图分类: {intent}")

    # ---- record: 记录内容到收件箱 ----
    if intent == "record":
        content = result.get("content", msg_original_stripped.strip())
        if not content:
            logger.info("[yoyo] 记录内容为空，要求补充")
            return "请告诉我你要记录的内容哦😊"

        classify_result = content_classifier.classify(content)
        logger.info(
            f"[yoyo] 记录内容: type={classify_result['content_type']}, content={content[:30]}..."
        )

        file_path = inbox_ops.add_record(
            content=content,
            content_type=classify_result["content_type"],
            priority=classify_result["priority"],
            due_date=classify_result["due_date"],
            tags=classify_result["tags"],
        )

        response = "✅ 已成功记录到收件箱！\n"
        response += f"📝 内容：{content[:50]}{'...' if len(content) > 50 else ''}\n"
        response += f"🏷️ 类型：{classify_result['content_type']} (置信度: {classify_result['confidence']:.2f})\n"
        if classify_result["due_date"]:
            response += f"⏰ 时间：{classify_result['due_date'].strftime('%Y-%m-%d %H:%M')}\n"
        if classify_result["tags"]:
            response += f"🔖 标签：{', '.join(classify_result['tags'])}\n"
        response += f"📂 文件路径：{file_path}"
        if classify_result["content_type"] == "todo":
            inbox_ops.move_record(str(file_path), "02-Tasks/Pending")
            gtd_classifier.process_pending_todos()
            response += "\n🚀 已自动识别为待办事项，将进行GTD分类并同步到Kanban"

        logger.info(f"[yoyo] 回复: {response[:80]}...")
        return response

    # ---- query_today: 查询今日待办 ----
    if intent == "query_today":
        logger.info("[yoyo] 查询今日待办")
        briefing = todo_generator.get_daily_morning_briefing()
        return briefing

    # ---- search: 搜索历史记录 ----
    if intent == "search":
        query = result.get("query", "").strip()
        if not query:
            return "请告诉我你要搜索的关键词哦😊"

        logger.info(f"[yoyo] 搜索记录: query={query}")
        records = inbox_ops.search_records(query=query, limit=10)
        if not records:
            return f"🔍 没有找到包含 '{query}' 的记录"

        response = f"🔍 找到 {len(records)} 条相关记录：\n\n"
        for i, record in enumerate(records, 1):
            frontmatter = record.get("frontmatter", {})
            try:
                timestamp = datetime.fromisoformat(frontmatter.get("timestamp", "")).astimezone(TZ)
                time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = "未知时间"
            rec_content = record.get("content", "")
            content_line = rec_content.split("\n")[0].strip()
            content_line = (
                content_line.lstrip("#").strip()[:30] + "..."
                if len(content_line) > 30
                else content_line
            )
            response += (
                f"{i}. [{time_str}] [{frontmatter.get('content_type', 'note')}] {content_line}\n"
            )
        return response

    # ---- view_habits: 查看今日习惯完成状态 ----
    if intent == "view_habits":
        habits = todo_generator.get_habit_definitions()
        if not habits:
            return '📋 还没有记录任何习惯，告诉我"养成跑步的习惯"来添加吧！'

        today = datetime.now(TZ).strftime("%Y-%m-%d")
        done_set = todo_generator.habit_tracker.get_done_today(today)

        response = "📋 **今日习惯完成情况**\n\n"
        done_count = 0
        for h in habits:
            if h in done_set:
                response += f"- [x] {h} ✅\n"
                done_count += 1
            else:
                response += f"- [ ] {h}\n"

        if done_count > 0:
            response += f"\n今日已完成 {done_count}/{len(habits)} 个习惯！"
        else:
            response += '\n今天还没打卡，加油！完成后告诉我（如"做了跑步"）'
        return response

    # ---- record_habit: 记录新习惯 ----
    if intent == "record_habit":
        habit_content = result.get("habit", "").strip()
        if not habit_content:
            return "请告诉我你想养成的习惯，例如「养成每天跑步的习惯」或「每天阅读30分钟」"

        logger.info(f"[yoyo] 提取到习惯内容: {habit_content}")
        habits_file = Path(inbox_ops.data_dir) / "04-Events" / "habits.md"
        if habits_file.exists():
            content = habits_file.read_text(encoding="utf-8")
            if "## 每日习惯" in content:
                if habit_content not in content:
                    content = content.replace(
                        "## 每日习惯\n", f"## 每日习惯\n- [ ] {habit_content}\n"
                    )
                    habits_file.write_text(content, encoding="utf-8")
                    logger.info(f"[yoyo] 习惯已写入 habits.md: {habit_content}")
                    return f"✅ 已帮你记录到习惯跟踪：\n📋 **{habit_content}**\n\n从明天开始执行，加油坚持！💪"
                else:
                    return f"这个习惯已经记录过了哦：{habit_content}"
            else:
                return "⚠️ 习惯文件格式不对，请检查 04-Events/habits.md"
        else:
            return f"⚠️ 习惯文件不存在：{habits_file}"

    # ---- habit_checkin: 打卡完成习惯 ----
    if intent == "habit_checkin":
        all_habits = set(todo_generator.get_habit_definitions())
        habit_names = result.get("habits", [])

        # 过滤：只保留存在于定义中的习惯名（LLM 可能返回缩写）
        valid_names = [n for n in habit_names if n in all_habits]
        if not valid_names:
            all_list = "、".join(all_habits)
            return f"没有识别出你要打卡哪个习惯。已定义的习惯：{all_list}"

        today = datetime.now(TZ).strftime("%Y-%m-%d")
        now_iso = datetime.now(TZ).isoformat()
        for name in valid_names:
            todo_generator.habit_tracker.log_done(today, name, now_iso)
            logger.info(f"[yoyo] 习惯打卡完成: {name}")

        if len(valid_names) == 1:
            return f"✅ 习惯打卡完成：**{valid_names[0]}**，继续保持！"
        return f"✅ 已打卡 {len(valid_names)} 个习惯：**{'**、**'.join(valid_names)}**，继续保持！"

    # ---- habit_stats: 习惯统计查询 ----
    if intent == "habit_stats":
        stats = todo_generator.habit_tracker.get_stats(days=30)
        if not stats:
            return "📊 还没有习惯执行记录，先记录一些习惯吧！"

        response = "📊 **习惯执行统计（近30天）**\n\n"
        sorted_stats = sorted(stats.items(), key=lambda x: x[1]["rate"], reverse=True)
        for name, data in sorted_stats:
            bar_len = 10
            filled = round(data["rate"] * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            emoji = "✅" if data["rate"] >= 0.8 else ("⚠️" if data["rate"] >= 0.5 else "❌")
            response += (
                f"{emoji} **{name}**\n"
                f"  {bar} {data['done']}/{data['total']}天 ({data['rate']:.0%})\n"
                f"  🔥 连续打卡 {data['streak']} 天\n\n"
            )
        return response

    # ---- mark_done: 标记任务完成 ----
    if intent == "mark_done":
        task_keywords = result.get("tasks", [])
        if not task_keywords:
            return "请告诉我你完成的任务关键词哦😊"

        done_count = 0
        for task_keyword in task_keywords:
            logger.info(f"[yoyo] 标记任务完成: keyword={task_keyword}")
            pending = inbox_ops.search_records(query=task_keyword, content_type="todo", limit=5)
            pending = [t for t in pending if t.get("frontmatter", {}).get("status") != "completed"]

            if not pending:
                continue

            task = pending[0]
            target_path = inbox_ops.move_record(task["path"], "02-Tasks/Completed")
            content = target_path.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)
            frontmatter["status"] = "completed"
            frontmatter["completed_at"] = datetime.now(TZ).isoformat()
            body = body.replace("- [ ]", "- [x]", 1)
            target_path.write_text(dump_frontmatter(frontmatter, body), encoding="utf-8")
            done_count += 1

        gtd_classifier.update_kanban()

        if done_count == 0:
            return f"没有找到包含这些关键词的待完成任务：{'、'.join(task_keywords)}"
        return f"✅ 已完成 {done_count} 个任务！"

    # ---- generate_report: 生成日报 ----
    if intent == "generate_report":
        logger.info("[yoyo] 生成日报")
        report_content, report_path = review_reminder.generate_daily_report()
        response = f"📰 今日日报已生成！\n📂 文件路径：{report_path}\n\n"
        lines = report_content.split("\n")[:30]
        response += "\n".join(lines)
        if len(report_content.split("\n")) > 30:
            response += "\n...（更多内容请查看完整报告）"
        return response

    # LLM 区分不了意图 -> 反问用户
    # if intent == "ask_user":
    #     return "🤔 我没有完全理解你的意思。能说得更准确一些吗？"

    # 默认回复 - 返回 None 让消息继续走到 LLM 处理
    logger.info("[yoyo] 未匹配任何意图，返回 None 继续由 LLM 处理")
    return None


def get_scheduled_tasks():
    """
    获取定时任务配置
    :return: 定时任务列表
    """
    tasks = []

    # 每日8:00 早报推送
    tasks.append(
        {
            "cron": "0 8 * * *",
            "name": "personal-secretary-morning-brief",
            "description": "私人秘书每日早报推送",
            "handler": lambda context: _send_morning_brief(context),
        }
    )

    # 每日21:00 晚报推送
    tasks.append(
        {
            "cron": "0 21 * * *",
            "name": "personal-secretary-evening-brief",
            "description": "私人秘书每日晚报推送",
            "handler": lambda context: _send_evening_brief(context),
        }
    )

    # 每3天 长期事项回顾
    tasks.append(
        {
            "cron": "0 19 */3 * *",
            "name": "personal-secretary-long-term-review",
            "description": "私人秘书长期事项回顾提醒",
            "handler": lambda context: _send_long_term_review(context),
        }
    )

    # 每周日20:00 周度回顾提醒
    tasks.append(
        {
            "cron": "0 20 * * 0",
            "name": "personal-secretary-weekly-review",
            "description": "私人秘书周度回顾提醒",
            "handler": lambda context: _send_weekly_review(context),
        }
    )

    # 每月1日3:00 数据备份和月报生成
    tasks.append(
        {
            "cron": "0 3 1 * *",
            "name": "personal-secretary-monthly-backup",
            "description": "私人秘书月度数据备份和月报生成",
            "handler": lambda context: _do_monthly_backup(context),
        }
    )

    # 每300秒检查即将到期的任务
    tasks.append(
        {
            "interval": 300,
            "name": "personal-secretary-check-upcoming",
            "description": "私人秘书检查即将到期的任务",
            "handler": lambda context: _check_upcoming_tasks(context),
        }
    )

    # 每小时检查习惯完成情况
    tasks.append(
        {
            "interval": 3600,
            "name": "personal-secretary-habit-check",
            "description": "私人秘书习惯执行检查",
            "handler": lambda context: _check_habits(context),
        }
    )

    return tasks


async def _send_morning_brief(context):
    """发送早报"""
    try:
        _init_instances(context.get("config", {}))
        briefing = todo_generator.get_daily_morning_briefing()
        await context["send_message"](briefing)
    except Exception as e:
        logger.error(f"[yoyo] 发送早报失败: {e}")


async def _send_evening_brief(context):
    """发送晚报"""
    try:
        _init_instances(context.get("config", {}))
        briefing = todo_generator.get_daily_evening_briefing()
        await context["send_message"](briefing)
        # 生成日报
        review_reminder.generate_daily_report()
    except Exception as e:
        logger.error(f"[yoyo] 发送晚报失败: {e}")


async def _send_long_term_review(context):
    """发送长期事项回顾"""
    try:
        _init_instances(context.get("config", {}))
        msg, _ = review_reminder.get_long_term_review_reminder()
        await context["send_message"](msg)
    except Exception as e:
        logger.error(f"[yoyo] 发送长期事项回顾失败: {e}")


async def _send_weekly_review(context):
    """发送周度回顾提醒"""
    try:
        _init_instances(context.get("config", {}))
        msg = review_reminder.get_weekly_review_reminder()
        await context["send_message"](msg)
        # 生成周报
        review_reminder.generate_weekly_report()
    except Exception as e:
        logger.error(f"[yoyo] 发送周度回顾失败: {e}")


async def _do_monthly_backup(context):
    """月度备份和月报生成"""
    try:
        _init_instances(context.get("config", {}))
        # 生成月报
        review_reminder.generate_monthly_report()
        # 备份数据
        backup_path = review_reminder.backup_data()
        await context["send_message"](f"📦 月度数据备份已完成，备份文件：{backup_path}")
    except Exception as e:
        logger.error(f"[yoyo] 月度备份失败: {e}")


async def _check_upcoming_tasks(context):
    """检查即将到期的任务"""
    try:
        _init_instances(context.get("config", {}))
        upcoming_tasks = todo_generator.get_upcoming_tasks()
        for task in upcoming_tasks:
            msg = todo_generator.generate_reminder_message(task)
            await context["send_message"](msg)
            todo_generator.mark_as_reminded(task["file_path"])
    except Exception as e:
        logger.error(f"[yoyo] 检查到期任务失败: {e}")


async def _check_habits(context):
    """每小时检查习惯完成情况，未完成的习惯主动提醒"""
    try:
        _init_instances(context.get("config", {}))
        now = datetime.now(TZ)
        # 只在 8:00-22:00 之间提醒
        if now.hour < 8 or now.hour >= 22:
            return

        unchecked = todo_generator.get_unchecked_habits()
        if unchecked:
            msg = "⏰ 习惯提醒时间！\n\n今天还有以下习惯未完成：\n"
            for h in unchecked:
                msg += f"- [ ] {h}\n"
            msg += '\n完成后告诉我（如"做了跑步"），我来帮你打卡！'
            await context["send_message"](msg)
            logger.info(f"[yoyo] 推送习惯提醒: {unchecked}")
    except Exception as e:
        logger.error(f"[yoyo] 习惯检查失败: {e}")
