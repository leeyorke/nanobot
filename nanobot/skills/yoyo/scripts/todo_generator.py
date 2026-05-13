#!/usr/bin/env python3
"""
待办生成和提醒模块：动态检查待办到期时间，发送提醒通知
"""
import re
from datetime import datetime, timezone, timedelta
from .helpers import get_timezone, parse_frontmatter, dump_frontmatter
from pathlib import Path
from .inbox_operations import InboxOperations
from .habit_tracker import HabitTracker

# 北京时间时区

class TodoGenerator:
    def __init__(self, data_dir=None, config=None):
        """
        初始化待办生成器
        :param data_dir: 数据存储目录
        """
        self.inbox_ops = InboxOperations(config)
        self.data_dir = self.inbox_ops.data_dir
        self.habit_tracker = HabitTracker(self.data_dir)

    def get_upcoming_tasks(self, time_window_minutes=60):
        """
        获取即将到期的任务
        :param time_window_minutes: 未来多久内的任务需要提醒，默认60分钟
        :return: 即将到期的任务列表
        """
        now = datetime.now(TZ)
        time_window = now + timedelta(minutes=time_window_minutes)

        # 搜索所有待办任务（排除已完成和已删除的）
        pending_categories = ['Now', 'Next', 'Calendar', 'Waiting', 'Projects']
        upcoming_tasks = []

        for category in pending_categories:
            dir_path = self.data_dir / '02-Tasks' / category
            if not dir_path.exists():
                continue

            for md_file in dir_path.glob('*.md'):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    frontmatter, body = parse_frontmatter(content)
                    body = body.strip()

                    # 只处理有截止时间的任务
                    due_date_str = frontmatter.get('due_date')
                    if not due_date_str:
                        continue

                    try:
                        due_date = datetime.fromisoformat(due_date_str).astimezone(self._tz)
                    except:
                        continue

                    # 检查是否在提醒时间窗口内
                    if now <= due_date <= time_window:
                        # 提取任务内容
                        task_content = self._extract_task_content(body)

                        # 计算提前提醒时间
                        is_calendar = category == 'Calendar'
                        remind_before = 60 if is_calendar else 30  # 日程提前1小时提醒，待办提前30分钟
                        remind_time = due_date - timedelta(minutes=remind_before)

                        # 检查是否到了提醒时间
                        if now >= remind_time:
                            # 检查是否已经提醒过
                            if frontmatter.get('reminded', False):
                                continue

                            upcoming_tasks.append({
                                'id': frontmatter.get('id'),
                                'content': task_content,
                                'due_date': due_date,
                                'category': category,
                                'priority': frontmatter.get('priority', 'medium'),
                                'file_path': str(md_file),
                                'remind_before': remind_before,
                                'is_calendar': is_calendar
                            })

                except Exception as e:
                    print(f"读取任务文件 {md_file} 失败: {e}")
                    continue

        return upcoming_tasks

    def _extract_task_content(self, body):
        """从正文中提取任务内容"""
        lines = body.split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- ['):
                # 去掉任务列表标记
                return re.sub(r'^\s*-\s*\[\s*(x| )\s*\]\s*', '', stripped).strip()
        # 如果没有任务列表，取第一个非标题行
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                return stripped
        return "未命名任务"

    def mark_as_reminded(self, task_file_path):
        """标记任务已经提醒过，避免重复提醒"""
        file_path = Path(task_file_path)
        if not file_path.exists():
            return False

        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, body = parse_frontmatter(content)

            # 更新frontmatter
            frontmatter['reminded'] = True
            frontmatter['reminded_at'] = datetime.now(TZ).isoformat()

            # 重新写入文件
            file_path.write_text(dump_frontmatter(frontmatter, body), encoding='utf-8')

            return True
        except Exception as e:
            print(f"标记任务提醒失败 {task_file_path}: {e}")
            return False

    def get_habit_definitions(self):
        """从 habits.md 获取所有习惯名称"""
        habits_file = self.data_dir / '04-Events' / 'habits.md'
        if not habits_file.exists():
            return []

        content = habits_file.read_text(encoding='utf-8')
        habits = []
        for line in content.split('\n'):
            m = re.match(r'^-\s*\[\s*\]\s+(.+)', line.strip())
            if not m:
                m = re.match(r'^-\s*\[x\]\s+(.+)', line.strip())
            if m:
                name = m.group(1).strip()
                if name:
                    habits.append(name)
        return habits

    def get_unchecked_habits(self):
        """查询 SQLite：今天还没打卡的习惯"""
        today = datetime.now(TZ).strftime('%Y-%m-%d')
        done_set = self.habit_tracker.get_done_today(today)
        all_habits = self.get_habit_definitions()
        return [h for h in all_habits if h not in done_set]

    def generate_reminder_message(self, task):
        """生成提醒消息"""
        now = datetime.now(TZ)
        time_left = task['due_date'] - now
        minutes_left = int(time_left.total_seconds() / 60)

        if minutes_left <= 0:
            time_str = "已经到期"
        elif minutes_left < 60:
            time_str = f"还有 {minutes_left} 分钟"
        else:
            hours_left = minutes_left // 60
            mins_left = minutes_left % 60
            time_str = f"还有 {hours_left} 小时 {mins_left} 分钟" if mins_left > 0 else f"还有 {hours_left} 小时"

        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(task['priority'], '🟡')

        category_name = {
            'Now': '立即做',
            'Next': '下一步',
            'Calendar': '日程',
            'Waiting': '等待中',
            'Projects': '项目'
        }.get(task['category'], task['category'])

        if task['is_calendar']:
            title = "📅 日程提醒"
        else:
            title = "⏰ 待办提醒"

        message = f"""{title}：{priority_emoji}
任务：{task['content']}
时间：{task['due_date'].strftime('%Y-%m-%d %H:%M')}
分类：{category_name}
{time_str}，请及时处理！"""

        return message

    def get_daily_morning_briefing(self):
        """生成每日早报内容（当日待办清单）"""
        now = datetime.now(TZ)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 获取今日所有待办
        all_tasks = self.inbox_ops.search_records(
            content_type='todo',
            start_date=today_start,
            end_date=today_end
        )

        # 按分类分组
        categories = {
            'Now': [],
            'Next': [],
            'Calendar': [],
            'Waiting': [],
            'Projects': []
        }

        for task in all_tasks:
            frontmatter = task.get('frontmatter', {})
            category = frontmatter.get('gtd_category', 'Next')
            if category in categories:
                task_content = self._extract_task_content(task.get('content', ''))
                due_date = frontmatter.get('due_date')
                if due_date:
                    try:
                        due_date_dt = datetime.fromisoformat(due_date).astimezone(self._tz)
                        task_content += f" ⏰ {due_date_dt.strftime('%H:%M')}"
                    except:
                        pass
                categories[category].append(task_content)

        # 生成消息
        message = f"🌞 早上好！今天是 {now.strftime('%Y-%m-%d %A')}\n\n"
        message += "📋 今日待办清单：\n\n"

        category_order = [
            ('Now', '⚡ 立即做'),
            ('Calendar', '📅 今日日程'),
            ('Next', '🚶 下一步行动'),
            ('Waiting', '⏳ 等待中'),
            ('Projects', '📦 进行中项目')
        ]

        total_count = 0
        for cat_key, cat_name in category_order:
            tasks = categories.get(cat_key, [])
            if tasks:
                message += f"{cat_name}（共{len(tasks)}个）：\n"
                for i, task in enumerate(tasks, 1):
                    message += f"{i}. {task}\n"
                message += "\n"
                total_count += len(tasks)

        if total_count == 0:
            message += "🎉 今天没有待办任务，好好享受一天吧！\n"
        else:
            message += f"💪 今日共有 {total_count} 个待办任务，加油！\n"

        # 今日习惯清单（从 SQLite 查状态，habits.md 只提供名称）
        habits = self.get_habit_definitions()
        if habits:
            today_s = now.strftime('%Y-%m-%d')
            done_set = self.habit_tracker.get_done_today(today_s)
            message += f"\n🎯 今日习惯（共{len(habits)}个）：\n"
            for h in habits:
                status = 'x' if h in done_set else ' '
                message += f"- [{status}] {h}\n"
            message += "\n"

        # 添加每日寄语
        hello_file = self.data_dir / '04-Events' / 'hello.md'
        if hello_file.exists():
            hello_content = hello_file.read_text(encoding='utf-8').strip()
            # 去掉标题
            hello_content = re.sub(r'^#.*\n', '', hello_content).strip()
            if hello_content:
                message += f"\n💡 今日寄语：{hello_content}\n"

        return message

    def get_daily_evening_briefing(self):
        """生成每日晚报内容（当日完成情况）"""
        now = datetime.now(TZ)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # 今日完成的任务
        completed_tasks = self.inbox_ops.search_records(
            content_type='todo',
            status='completed',
            start_date=today_start,
            end_date=today_end
        )

        # 今日未完成的任务
        pending_tasks = self.inbox_ops.search_records(
            content_type='todo',
            start_date=today_start,
            end_date=today_end
        )
        # 过滤掉已完成的
        pending_tasks = [t for t in pending_tasks if t.get('frontmatter', {}).get('status') != 'completed']

        # 生成消息
        message = f"🌙 晚上好！今天是 {now.strftime('%Y-%m-%d')}\n\n"
        message += "📊 今日完成情况：\n\n"

        message += f"✅ 已完成任务：{len(completed_tasks)} 个\n"
        if completed_tasks:
            for i, task in enumerate(completed_tasks, 1):
                task_content = self._extract_task_content(task.get('content', ''))
                message += f"{i}. {task_content}\n"
        message += "\n"

        message += f"⏳ 未完成任务：{len(pending_tasks)} 个\n"
        if pending_tasks:
            for i, task in enumerate(pending_tasks, 1):
                task_content = self._extract_task_content(task.get('content', ''))
                frontmatter = task.get('frontmatter', {})
                due_date = frontmatter.get('due_date')
                if due_date:
                    try:
                        due_date_dt = datetime.fromisoformat(due_date).astimezone(self._tz)
                        task_content += f" ⏰ {due_date_dt.strftime('%H:%M')}"
                    except:
                        pass
                message += f"{i}. {task_content}\n"
        message += "\n"

        if pending_tasks:
            message += "❓ 未完成的任务需要如何处理？（回复序号+处理方式：延期/立即完成/删除）\n"
        else:
            message += "🎉 今日任务全部完成！太棒了，好好休息吧！\n"

        return message

if __name__ == "__main__":
    # 测试代码
    import sys
    generator = TodoGenerator()

    if len(sys.argv) < 2:
        print("用法:")
        print("  todo_generator.py check-upcoming  # 检查即将到期的任务")
        print("  todo_generator.py morning-brief   # 生成每日早报")
        print("  todo_generator.py evening-brief   # 生成每日晚报")
        sys.exit(1)

    if sys.argv[1] == 'check-upcoming':
        tasks = generator.get_upcoming_tasks()
        print(f"找到 {len(tasks)} 个即将到期的任务：")
        for task in tasks:
            print(f"\n{generator.generate_reminder_message(task)}")
            # 标记为已提醒
            generator.mark_as_reminded(task['file_path'])

    elif sys.argv[1] == 'morning-brief':
        msg = generator.get_daily_morning_briefing()
        print(msg)

    elif sys.argv[1] == 'evening-brief':
        msg = generator.get_daily_evening_briefing()
        print(msg)
