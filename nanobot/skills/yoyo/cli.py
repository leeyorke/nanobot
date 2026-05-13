#!/usr/bin/env python3
"""
私人秘书 CLI - 可独立运行或通过 nanobot CLI 调用
用法:
    nanobot secret add "明天下午3点开评审会"
    nanobot secret today
    nanobot secret search "项目"
    nanobot secret done "评审会"
    nanobot secret report
    nanobot secret config --show
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .scripts.helpers import parse_frontmatter, dump_frontmatter

TZ = timezone(timedelta(hours=8))

# ---------------------------------------------------------------------------
# Config & instances
# ---------------------------------------------------------------------------

_config = None
_inbox_ops = None
_content_classifier = None
_gtd_classifier = None
_todo_generator = None
_review_reminder = None


def _load_config():
    """Load nanobot config (reads from default path)."""
    from nanobot.config.loader import load_config

    return load_config()


def _init_instances(config=None):
    global _inbox_ops, _content_classifier, _gtd_classifier, _todo_generator, _review_reminder
    if _inbox_ops is None:
        config = config or _load_config()
        from .scripts.content_classifier import ContentClassifier
        from .scripts.gtd_classifier import GTDClassifier
        from .scripts.inbox_operations import InboxOperations
        from .scripts.review_reminder import ReviewReminder
        from .scripts.todo_generator import TodoGenerator

        _inbox_ops = InboxOperations(config)
        _content_classifier = ContentClassifier(_inbox_ops.data_dir)
        _gtd_classifier = GTDClassifier(_inbox_ops.data_dir)
        _todo_generator = TodoGenerator(_inbox_ops.data_dir)
        _review_reminder = ReviewReminder(_inbox_ops.data_dir)


# ---------------------------------------------------------------------------
# First-run check
# ---------------------------------------------------------------------------


def _first_run_check(config):
    """检查是否初次运行，若是则提示用户配置 data_dir。"""

    def is_directory_empty(path):
        directory = Path(path).expanduser().resolve()
        if not directory.exists():
            return True
        if not directory.is_dir():
            return True
        return len(list(directory.iterdir())) == 0

    _init_instances(config)
    # 初次启用检查：若 data_dir 为默认路径且为空，先询问用户配置
    ps_config = config.get("personal_secretary") or {}
    data_dir = ps_config.get("data_dir", "")
    default_dir = "~/.nanobot/workspace/personal-secretary/"
    from pathlib import Path

    resolved = str(Path(data_dir).expanduser().resolve()) if data_dir else ""
    if not resolved and not is_directory_empty(default_dir):
        return (
            "👋 初次启用yoyo私人秘书，请告诉我你希望数据保存在哪个目录？\n"
            "例如：`~/Documents/Obsidian/MyVault` 或直接回车使用默认路径 `~/.nanobot/workspace/personal-secretary/`"
        )
    return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_add(args):
    """添加记录到收件箱."""
    _init_instances()
    content = args.content
    if not content:
        print("错误：请提供要记录的内容，用引号包裹", file=sys.stderr)
        return 1

    result = _content_classifier.classify(content)
    file_path = _inbox_ops.add_record(
        content=content,
        content_type=result["content_type"],
        priority=result["priority"],
        due_date=result["due_date"],
        tags=result["tags"],
    )

    print(f"✅ 已记录：{content[:50]}{'...' if len(content) > 50 else ''}")
    print(f"   类型：{result['content_type']}  置信度：{result['confidence']:.0%}")
    if result["due_date"]:
        print(f"   时间：{result['due_date'].strftime('%Y-%m-%d %H:%M')}")
    if result["tags"]:
        print(f"   标签：{', '.join(result['tags'])}")
    print(f"   路径：{file_path}")

    if result["content_type"] == "todo":
        _inbox_ops.move_record(str(file_path), "02-Tasks/Pending")
        _gtd_classifier.process_pending_todos()
        print("   🚀 已识别为待办，GTD分类完成")
    return 0


def cmd_today(args):
    """显示今日待办和日程."""
    _init_instances()
    briefing = _todo_generator.get_daily_morning_briefing()
    print(briefing)
    return 0


def cmd_search(args):
    """搜索历史记录."""
    _init_instances()
    if not args.query:
        print("错误：请提供搜索关键词", file=sys.stderr)
        return 1

    records = _inbox_ops.search_records(query=args.query, content_type=args.type, limit=args.limit)

    if not records:
        print(f"🔍 没有找到包含「{args.query}」的记录")
        return 0

    print(f"🔍 找到 {len(records)} 条记录：\n")
    for i, rec in enumerate(records, 1):
        fm = rec.get("frontmatter", {})
        try:
            ts = datetime.fromisoformat(fm.get("timestamp", "")).astimezone(TZ)
            time_str = ts.strftime("%Y-%m-%d %H:%M")
        except Exception:
            time_str = "未知时间"

        body = rec.get("content", "")
        preview = body.split("\n")[0].strip().lstrip("#").strip()[:40]
        ctype = fm.get("content_type", "note")
        status = fm.get("status", "")
        status_str = f" [{status}]" if status else ""

        print(f"  {i}. [{time_str}] [{ctype}]{status_str} {preview}")

    return 0


def cmd_done(args):
    """标记任务完成."""
    _init_instances()
    if not args.keyword:
        print("错误：请提供任务关键词", file=sys.stderr)
        return 1

    pending = _inbox_ops.search_records(query=args.keyword, content_type="todo", limit=10)
    pending = [t for t in pending if t.get("frontmatter", {}).get("status") != "completed"]

    if not pending:
        print(f"没有找到包含「{args.keyword}」的待完成任务")
        return 1

    if len(pending) > 1 and not args.yes:
        print(f"找到 {len(pending)} 个匹配任务，请确认：")
        for i, t in enumerate(pending, 1):
            print(f"  {i}. {t['content'][:50]}")
        print("\n使用 --yes 确认完成第1个，或用更精确的关键词")
        return 1

    task = pending[0]
    target = _inbox_ops.move_record(task["path"], "02-Tasks/Completed")

    text = target.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    fm["status"] = "completed"
    fm["completed_at"] = datetime.now(TZ).isoformat()
    body = body.replace("- [ ]", "- [x]", 1)

    target.write_text(dump_frontmatter(fm, body), encoding="utf-8")

    _gtd_classifier.update_kanban()
    print(f"✅ 已完成：{task['content'][:50]}")
    print(f"   归档：{target}")
    return 0


def cmd_report(args):
    """生成日报/周报/月报."""
    _init_instances()
    period = args.period or "daily"
    if period == "daily":
        content, path = _review_reminder.generate_daily_report()
    elif period == "weekly":
        content, path = _review_reminder.generate_weekly_report()
    elif period == "monthly":
        content, path = _review_reminder.generate_monthly_report()
    else:
        print(f"错误：未知周期 {period}", file=sys.stderr)
        return 1

    print(f"📰 {period} 报告已生成：{path}\n")
    # 打印前40行摘要
    lines = content.split("\n")[:40]
    print("\n".join(lines))
    if len(content.split("\n")) > 40:
        print("\n...（完整报告见文件）")
    return 0


def cmd_config(args):
    """查看或修改配置."""
    config = _load_config()
    ps = config.personal_secretary

    if args.show or (not args.data_dir and not args.morning and not args.evening):
        print("私人秘书配置：")
        print(f"  data_dir:              {ps.data_dir}")
        print(f"  remind_time_morning:   {ps.remind_time_morning}")
        print(f"  remind_time_evening:   {ps.remind_time_evening}")
        print(f"  remind_long_term_interval: {ps.remind_long_term_interval} 天")
        print(f"  remind_weekly_time:    {ps.remind_weekly_time}")
        print(f"  auto_backup:           {ps.auto_backup}")
        return 0

    changed = False
    if args.data_dir:
        ps.data_dir = str(Path(args.data_dir).expanduser())
        changed = True
    if args.morning:
        ps.remind_time_morning = args.morning
        changed = True
    if args.evening:
        ps.remind_time_evening = args.evening
        changed = True

    if changed:
        from nanobot.config.loader import save_config

        save_config(config)
        print("✅ 配置已保存")
    return 0


def cmd_list(args):
    """列出记录."""
    _init_instances()
    ctype = args.type or "all"
    data_dir = _inbox_ops.data_dir

    if ctype == "all" or ctype == "todo":
        print("\n📋 待办任务：")
        _list_dir(data_dir / "02-Tasks", args.limit)

    if ctype == "all" or ctype == "note":
        print("\n📝 笔记：")
        _list_dir(data_dir / "03-Notes", args.limit)

    if ctype == "all" or ctype == "inbox":
        print("\n📥 收件箱：")
        _list_dir(data_dir / "01-Inbox", args.limit)

    if ctype == "all" or ctype == "link":
        print("\n🔗 链接：")
        _list_dir(data_dir / "05-Resources/Links", args.limit)
    return 0


def _list_dir(dir_path: Path, limit: int = 20):
    if not dir_path.exists():
        print("  （空）")
        return
    files = sorted(dir_path.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    if not files:
        print("  （空）")
        return
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            preview = body.split("\n")[0].strip().lstrip("#").strip()[:40]
            ts = datetime.fromtimestamp(f.stat().st_mtime, tz=TZ).strftime("%m-%d %H:%M")
            status = fm.get("status", "")
            done = "✅ " if status == "completed" else "⬜ "
            print(f"  {done}[{ts}] {preview}")
        except Exception:
            print(f"  {f.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="nanobot secret",
        description="yoyo 私人秘书 - 记录、GTD任务管理、日报生成",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # nanobot secret add "内容"
    p_add = sub.add_parser("add", help="添加记录到收件箱")
    p_add.add_argument("content", help="要记录的内容（用引号包裹）")
    p_add.set_defaults(func=cmd_add)

    # nanobot secret today
    sub.add_parser("today", help="显示今日待办和日程").set_defaults(func=cmd_today)

    # nanobot secret search "关键词"
    p_search = sub.add_parser("search", help="搜索历史记录")
    p_search.add_argument("query", help="搜索关键词")
    p_search.add_argument(
        "--type", "-t", dest="type", default=None, help="筛选类型：todo/note/link/event"
    )
    p_search.add_argument("--limit", "-n", dest="limit", type=int, default=20)
    p_search.set_defaults(func=cmd_search)

    # nanobot secret done "关键词"
    p_done = sub.add_parser("done", help="标记任务完成")
    p_done.add_argument("keyword", help="任务关键词")
    p_done.add_argument("--yes", "-y", action="store_true", help="无需确认直接完成")
    p_done.set_defaults(func=cmd_done)

    # nanobot secret report
    p_report = sub.add_parser("report", help="生成报告")
    p_report.add_argument(
        "--period", "-p", dest="period", choices=["daily", "weekly", "monthly"], default="daily"
    )
    p_report.set_defaults(func=cmd_report)

    # nanobot secret config
    p_cfg = sub.add_parser("config", help="查看/修改配置")
    p_cfg.add_argument("--show", "-s", action="store_true", help="显示当前配置")
    p_cfg.add_argument("--data-dir", "-d", dest="data_dir", help="设置数据存储目录")
    p_cfg.add_argument("--morning", "-m", dest="morning", help="设置早报推送时间（如 08:00）")
    p_cfg.add_argument("--evening", "-e", dest="evening", help="设置晚报推送时间（如 21:00）")
    p_cfg.set_defaults(func=cmd_config)

    # nanobot secret list
    p_list = sub.add_parser("list", help="列出记录")
    p_list.add_argument(
        "--type",
        "-t",
        dest="type",
        default="all",
        choices=["all", "todo", "note", "inbox", "link"],
        help="列出哪类记录（默认 all）",
    )
    p_list.add_argument("--limit", "-n", dest="limit", type=int, default=20)
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args(argv)

    # 初次运行检查（add/today/search/done/report/list 需要初始化）
    if args.command in ("add", "today", "search", "done", "report", "list"):
        config = _load_config()
        hint = _first_run_check(config)
        if hint:
            print(hint)
            return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
