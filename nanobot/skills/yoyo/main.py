#!/usr/bin/env python3
"""
私人秘书技能主入口
"""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from loguru import logger

from .scripts.content_classifier import ContentClassifier
from .scripts.gtd_classifier import GTDClassifier
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


def _init_instances(config):
    """初始化所有实例"""
    global inbox_ops, content_classifier, gtd_classifier, todo_generator, review_reminder
    if inbox_ops is None:
        inbox_ops = InboxOperations(config)
        content_classifier = ContentClassifier(inbox_ops.data_dir, config)
        gtd_classifier = GTDClassifier(inbox_ops.data_dir, config)
        todo_generator = TodoGenerator(inbox_ops.data_dir, config)
        review_reminder = ReviewReminder(inbox_ops.data_dir, config)


def first_check(context):
    def is_directory_empty(path):
        directory = Path(path)
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
        logger.info(f"[yoyo] 返回初次配置提示")
        return hint

    # 从context获取config（first_check已加载并存入）
    config = context.get("config")
    _init_instances(config)

    message_lower = message.lower()

    # 去掉开头的 "yoyo" 前缀（不区分大小写），保留剩余部分做匹配
    msg_stripped = re.sub(r"^yoyo[，,\s]+", "", message_lower, flags=re.IGNORECASE)
    msg_original_stripped = re.sub(r"^yoyo[，,\s]+", "", message, flags=re.IGNORECASE)

    # 1. 记录功能 - 多种自然表达方式
    # 模式：关键字在任意位置 "保存到 inbox"、"记录"、"帮我把这个保存到 inbox" 等
    # 注意：如果消息包含"习惯"相关关键词且"记一下"后面没有内容，优先走习惯处理
    record_keywords = [
        "保存到 inbox", "保存到inbox", "记录", "记下", "帮我记一下",
        "我要记", "记一下", "记住", "帮我把这个保存到 inbox"
    ]
    content = None
    is_habit_intent = "习惯" in msg_stripped or "养成" in msg_stripped
    for kw in record_keywords:
        if kw in msg_stripped:
            # 找到关键字位置，内容 = 关键字之后的所有文字
            idx = msg_stripped.find(kw) + len(kw)
            after_keyword = msg_original_stripped[idx:].strip()
            # 如果"记一下"后面没有内容，且包含习惯关键词，跳过记录走习惯处理
            if not after_keyword and is_habit_intent:
                break
            content = after_keyword
            break

    if content:
        if not content:
            logger.info("[yoyo] 记录内容为空，要求补充")
            return "请告诉我你要记录的内容哦😊"

        # 分类内容
        classify_result = content_classifier.classify(content)
        logger.info(f"[yoyo] 记录内容: type={classify_result['content_type']}, content={content[:30]}...")

        # 添加到收件箱
        file_path = inbox_ops.add_record(
            content=content,
            content_type=classify_result["content_type"],
            priority=classify_result["priority"],
            due_date=classify_result["due_date"],
            tags=classify_result["tags"],
        )

        response = f"✅ 已成功记录到收件箱！\n"
        response += f"📝 内容：{content[:50]}{'...' if len(content) > 50 else ''}\n"
        response += f"🏷️ 类型：{classify_result['content_type']} (置信度: {classify_result['confidence']:.2f})\n"

        if classify_result["due_date"]:
            response += f"⏰ 时间：{classify_result['due_date'].strftime('%Y-%m-%d %H:%M')}\n"
        if classify_result["tags"]:
            response += f"🔖 标签：{', '.join(classify_result['tags'])}\n"

        response += f"📂 文件路径：{file_path}"

        # 如果是待办，移动到Pending目录待GTD分类
        if classify_result["content_type"] == "todo":
            inbox_ops.move_record(str(file_path), "02-Tasks/Pending")
            gtd_classifier.process_pending_todos()
            response += "\n🚀 已自动识别为待办事项，将进行GTD分类并同步到Kanban"

        logger.info(f"[yoyo] 回复: {response[:80]}...")
        return response

    # 2. 查询今日待办
    if re.match(r"^(我的)?(今日|今天)(任务|待办|清单)", msg_stripped):
        logger.info("[yoyo] 匹配到查询今日待办")
        briefing = todo_generator.get_daily_morning_briefing()
        return briefing

    # 3. 查询历史记录
    search_keywords = ["搜索", "查询", "找"]
    for kw in search_keywords:
        if kw in msg_stripped:
            # 内容 = 关键字之后的所有文字
            idx = msg_stripped.find(kw) + len(kw)
            query = msg_original_stripped[idx:].strip()
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
                content_line = content_line.lstrip("#").strip()[:30] + "..." if len(content_line) > 30 else content_line

                response += f"{i}. [{time_str}] [{frontmatter.get('content_type', 'note')}] {content_line}\n"

            return response

    # 4. 记录习惯
    habit_keywords = ["习惯", "养成", "每天"]
    for kw in habit_keywords:
        if kw in msg_stripped and ("养成" in msg_stripped or "习惯" in msg_stripped):
            logger.info(f"[yoyo] 匹配到习惯意图")

            # 提取习惯描述 - 优先匹配"养成xxx的习惯"或"每天xxx"模式
            habit_content = None

            # 尝试匹配"养成xxx的习惯"
            habit_match = re.search(r"养成\s*(.+?)\s*(的习惯|习惯[,，]|$)", msg_original_stripped)
            if habit_match:
                habit_content = habit_match.group(1).strip()
            else:
                # 尝试匹配"每天xxx"
                habit_match2 = re.search(r"每天\s*(.+?)\s*[,，]?(?!.*每天)", msg_original_stripped)
                if habit_match2:
                    habit_content = habit_match2.group(1).strip()

            if habit_content:
                logger.info(f"[yoyo] 提取到习惯内容: {habit_content}")
                # 读取 habits.md 并追加
                habits_file = Path(inbox_ops.data_dir) / "04-Events" / "habits.md"
                if habits_file.exists():
                    content = habits_file.read_text(encoding="utf-8")
                    # 追加到每日习惯列表
                    if "## 每日习惯" in content:
                        # 检查是否已存在
                        if habit_content not in content:
                            content = content.replace(
                                "## 每日习惯\n",
                                f"## 每日习惯\n- [ ] {habit_content}\n"
                            )
                            habits_file.write_text(content, encoding="utf-8")
                            logger.info(f"[yoyo] 习惯已写入 habits.md: {habit_content}")
                            response = f"✅ 已帮你记录到习惯跟踪：\n📋 **{habit_content}**\n\n从明天开始执行，加油坚持！💪"
                            logger.info(f"[yoyo] 回复: {response[:60]}...")
                            return response
                        else:
                            logger.info(f"[yoyo] 习惯已存在: {habit_content}")
                            return f"这个习惯已经记录过了哦：{habit_content}"
                    else:
                        logger.warning("[yoyo] habits.md 格式异常，缺少 ## 每日习惯")
                        return "⚠️ 习惯文件格式不对，请检查 04-Events/habits.md"
                else:
                    logger.warning(f"[yoyo] 习惯文件不存在: {habits_file}")
                    return f"⚠️ 习惯文件不存在：{habits_file}"
            break

    # 5. 标记任务完成
    complete_keywords = ["完成", "搞定", "做完了"]
    for kw in complete_keywords:
        if kw in msg_stripped:
            logger.info(f"[yoyo] 匹配到标记完成意图: keyword={kw}")
            # 关键字之后、可能末尾的"任务/事情"之前的内容
            idx = msg_stripped.find(kw) + len(kw)
            task_keyword = msg_original_stripped[idx:].strip()
            # 去掉末尾可能的"任务"或"事情"
            task_keyword = re.sub(r"(任务|事情)$", "", task_keyword).strip()
            if not task_keyword:
                return "请告诉我你完成的任务关键词哦😊"

            # 搜索匹配的待办
            pending_tasks = inbox_ops.search_records(query=task_keyword, content_type="todo", limit=5)

            pending_tasks = [
                t for t in pending_tasks if t.get("frontmatter", {}).get("status") != "completed"
            ]

            if not pending_tasks:
                return f"没有找到包含 '{task_keyword}' 的待完成任务"

            # 取第一个匹配的任务
            task = pending_tasks[0]
            task_path = task["path"]
            logger.info(f"[yoyo] 标记任务完成: {task_keyword} -> {task_path}")

            # 移动到已完成目录
            target_path = inbox_ops.move_record(task_path, "02-Tasks/Completed")

            # 更新frontmatter
            import yaml

            content = target_path.read_text(encoding="utf-8")
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                else:
                    frontmatter = {}
                    body = content
            else:
                frontmatter = {}
                body = content

            frontmatter["status"] = "completed"
            frontmatter["completed_at"] = datetime.now(TZ).isoformat()

            # 更新任务内容中的复选框
            body = body.replace("- [ ]", "- [x]", 1)

            # 重新写入
            yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{yaml_content}---\n{body}"
            target_path.write_text(new_content, encoding="utf-8")

            # 更新Kanban
            gtd_classifier.update_kanban()

            return f"✅ 已标记任务为完成！\n📝 任务内容：{task['content'][:50]}...\n📂 已归档到：{target_path}"

    # 6. 生成日报
    if re.match(r"^(今日|今天)(日报|回顾|总结)", msg_stripped):
        logger.info("[yoyo] 生成日报")
        report_content, report_path = review_reminder.generate_daily_report()
        response = f"📰 今日日报已生成！\n📂 文件路径：{report_path}\n\n"
        # 返回报告摘要
        lines = report_content.split("\n")[:30]
        response += "\n".join(lines)
        if len(report_content.split("\n")) > 30:
            response += "\n...（更多内容请查看完整报告）"
        return response

    # 默认回复
    logger.info(f"[yoyo] 未匹配任何意图，返回默认帮助信息")
    return (
        "🤖 我是你的私人秘书，我可以帮你：\n"
        '1. 记录内容：对我说"记录 明天下午3点开评审会"\n'
        '2. 查看今日待办：对我说"今日任务"\n'
        '3. 搜索记录：对我说"搜索 项目需求"\n'
        '4. 标记任务完成：对我说"完成 需求评审"\n'
        '5. 记录习惯：对我说"养成每天走8000步的习惯"\n'
        '6. 生成日报：对我说"今日日报"\n\n'
        "有什么需要帮忙的吗？"
    )


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

    # 每分钟检查即将到期的任务
    tasks.append(
        {
            "interval": 60,
            "name": "personal-secretary-check-upcoming",
            "description": "私人秘书检查即将到期的任务",
            "handler": lambda context: _check_upcoming_tasks(context),
        }
    )

    return tasks


async def _send_morning_brief(context):
    """发送早报"""
    _init_instances(context.get("config", {}))
    briefing = todo_generator.get_daily_morning_briefing()
    await context["send_message"](briefing)


async def _send_evening_brief(context):
    """发送晚报"""
    _init_instances(context.get("config", {}))
    briefing = todo_generator.get_daily_evening_briefing()
    await context["send_message"](briefing)
    # 生成日报
    review_reminder.generate_daily_report()


async def _send_long_term_review(context):
    """发送长期事项回顾"""
    _init_instances(context.get("config", {}))
    msg, _ = review_reminder.get_long_term_review_reminder()
    await context["send_message"](msg)


async def _send_weekly_review(context):
    """发送周度回顾提醒"""
    _init_instances(context.get("config", {}))
    msg = review_reminder.get_weekly_review_reminder()
    await context["send_message"](msg)
    # 生成周报
    review_reminder.generate_weekly_report()


async def _do_monthly_backup(context):
    """月度备份和月报生成"""
    _init_instances(context.get("config", {}))
    # 生成月报
    review_reminder.generate_monthly_report()
    # 备份数据
    backup_path = review_reminder.backup_data()
    await context["send_message"](f"📦 月度数据备份已完成，备份文件：{backup_path}")


async def _check_upcoming_tasks(context):
    """检查即将到期的任务"""
    _init_instances(context.get("config", {}))
    upcoming_tasks = todo_generator.get_upcoming_tasks()
    for task in upcoming_tasks:
        msg = todo_generator.generate_reminder_message(task)
        await context["send_message"](msg)
        todo_generator.mark_as_reminded(task["file_path"])
