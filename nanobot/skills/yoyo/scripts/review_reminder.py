#!/usr/bin/env python3
"""
回顾提醒和报告生成模块：生成日报、周报、月报等各类回顾报告，定期提醒用户回顾
"""
import json
from datetime import datetime, timezone, timedelta
from .helpers import get_timezone, parse_frontmatter
from pathlib import Path
from jinja2 import Template
from .inbox_operations import InboxOperations
from .todo_generator import TodoGenerator

# 北京时间时区
TZ = timezone(timedelta(hours=8))

class ReviewReminder:
    def __init__(self, data_dir=None, config=None):
        """
        初始化回顾提醒器
        """
        self.inbox_ops = InboxOperations(config)
        self.todo_generator = TodoGenerator(None, config)
        self.data_dir = self.inbox_ops.data_dir
        self._tz = get_timezone(config) or TZ
        self.reports_dir = self.data_dir / '07-Reports'

        # 加载报告模板
        template_path = Path(__file__).parent.parent / 'assets' / 'report_template.md'
        if template_path.exists():
            self.report_template = Template(template_path.read_text(encoding='utf-8'))
        else:
            # 默认模板
            self.report_template = Template("""
# {{report_type}}报告：{{date}}

## 📊 概览
- 新增记录：{{new_records_count}} 条
- 完成任务：{{completed_tasks_count}} 个
- 待完成任务：{{pending_tasks_count}} 个

## ✅ 已完成任务
{% for task in completed_tasks %}
- [x] {{task.content}} ✅ {{task.completed_time.strftime('%Y-%m-%d %H:%M')}}
{% endfor %}

## 📝 新增记录
{% for record in new_records %}
- {{record.timestamp.strftime('%Y-%m-%d %H:%M')}} [{{record.content_type}}] {{record.title}}
{% endfor %}
""")

    def generate_daily_report(self, date=None):
        """生成日报"""
        if date is None:
            date = datetime.now(TZ)
        date_str = date.strftime('%Y-%m-%d')

        # 时间范围
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)

        # 统计数据
        new_records = self.inbox_ops.search_records(
            start_date=start_time,
            end_date=end_time,
            limit=None
        )

        completed_tasks = self.inbox_ops.search_records(
            content_type='todo',
            status='completed',
            start_date=start_time,
            end_date=end_time,
            limit=None
        )

        pending_tasks = self.inbox_ops.search_records(
            content_type='todo',
            start_date=start_time,
            end_date=end_time,
            limit=None
        )
        pending_tasks = [t for t in pending_tasks if t.get('frontmatter', {}).get('status') != 'completed']

        # 格式化数据
        formatted_records = []
        for record in new_records:
            frontmatter = record.get('frontmatter', {})
            try:
                timestamp = datetime.fromisoformat(frontmatter.get('timestamp', '')).astimezone(self._tz)
            except:
                timestamp = datetime.fromtimestamp(Path(record['path']).stat().st_mtime, self._tz)

            # 提取标题
            content = record.get('content', '')
            lines = content.split('\n')
            title = lines[0].strip() if lines else '无标题'
            title = title.lstrip('#').strip()

            formatted_records.append({
                'timestamp': timestamp,
                'content_type': frontmatter.get('content_type', 'note'),
                'title': title
            })

        formatted_completed = []
        for task in completed_tasks:
            content = task.get('content', '')
            task_content = self.todo_generator._extract_task_content(content)
            mtime = datetime.fromtimestamp(Path(task['path']).stat().st_mtime, self._tz)
            formatted_completed.append({
                'content': task_content,
                'completed_time': mtime
            })

        # 渲染报告
        report_content = self.report_template.render(
            report_type='日报',
            date=date_str,
            new_records_count=len(new_records),
            completed_tasks_count=len(completed_tasks),
            pending_tasks_count=len(pending_tasks),
            completed_tasks=formatted_completed,
            new_records=formatted_records,
            today_tasks=[],
            tomorrow_tasks=[],
            summary=f"今日共记录 {len(new_records)} 条内容，完成 {len(completed_tasks)} 个任务，继续加油！"
        )

        # 保存报告
        report_dir = self.reports_dir / 'Daily'
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"Report-Daily-{date_str}.md"
        report_file.write_text(report_content, encoding='utf-8')

        return report_content, str(report_file)

    def generate_weekly_report(self, year=None, week=None):
        """生成周报"""
        now = datetime.now(TZ)
        if year is None:
            year = now.year
        if week is None:
            week = now.isocalendar()[1]

        # 计算本周的开始和结束时间（周一到周日）
        start_time = datetime.fromisocalendar(year, week, 1).replace(tzinfo=TZ)
        end_time = start_time + timedelta(days=7)
        date_str = f"{year}年第{week}周"

        # 统计数据（和日报类似，时间范围是一周）
        new_records = self.inbox_ops.search_records(
            start_date=start_time,
            end_date=end_time,
            limit=None
        )

        completed_tasks = self.inbox_ops.search_records(
            content_type='todo',
            status='completed',
            start_date=start_time,
            end_date=end_time,
            limit=None
        )

        pending_tasks = self.inbox_ops.search_records(
            content_type='todo',
            start_date=start_time,
            end_date=end_time,
            limit=None
        )
        pending_tasks = [t for t in pending_tasks if t.get('frontmatter', {}).get('status') != 'completed']

        # 按日期分组统计
        daily_stats = {}
        for record in new_records:
            try:
                ts = datetime.fromisoformat(record['frontmatter'].get('timestamp', '')).astimezone(self._tz)
                day_str = ts.strftime('%Y-%m-%d')
                if day_str not in daily_stats:
                    daily_stats[day_str] = {'records': 0, 'completed': 0}
                daily_stats[day_str]['records'] += 1
            except:
                pass

        for task in completed_tasks:
            try:
                ts = datetime.fromtimestamp(Path(task['path']).stat().st_mtime, self._tz)
                day_str = ts.strftime('%Y-%m-%d')
                if day_str not in daily_stats:
                    daily_stats[day_str] = {'records': 0, 'completed': 0}
                daily_stats[day_str]['completed'] += 1
            except:
                pass

        # 格式化完成任务
        formatted_completed = []
        for task in completed_tasks:
            content = task.get('content', '')
            task_content = self.todo_generator._extract_task_content(content)
            mtime = datetime.fromtimestamp(Path(task['path']).stat().st_mtime, self._tz)
            formatted_completed.append({
                'content': task_content,
                'completed_time': mtime
            })

        # 渲染报告
        report_content = f"""# 周报：{date_str}

## 📊 本周概览
- 新增记录：{len(new_records)} 条
- 完成任务：{len(completed_tasks)} 个
- 待完成任务：{len(pending_tasks)} 个

## 📈 每日统计
| 日期 | 新增记录 | 完成任务 |
|------|----------|----------|
"""
        for day in sorted(daily_stats.keys()):
            stats = daily_stats[day]
            report_content += f"| {day} | {stats['records']} | {stats['completed']} |\n"

        report_content += """
## ✅ 本周完成任务
"""
        for task in formatted_completed:
            report_content += f"- [x] {task['content']} ✅ {task['completed_time'].strftime('%Y-%m-%d')}\n"

        report_content += f"""
## 💡 周度总结
本周共完成 {len(completed_tasks)} 个任务，平均每天完成 {len(completed_tasks)/7:.1f} 个任务，继续保持！
"""

        # 保存报告
        report_dir = self.reports_dir / 'Weekly'
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"Report-Weekly-{year}-W{week:02d}.md"
        report_file.write_text(report_content, encoding='utf-8')

        return report_content, str(report_file)

    def generate_monthly_report(self, year=None, month=None):
        """生成月报"""
        now = datetime.now(TZ)
        if year is None:
            year = now.year
        if month is None:
            month = now.month

        # 计算本月开始和结束时间
        start_time = datetime(year, month, 1, tzinfo=TZ)
        if month == 12:
            end_time = datetime(year + 1, 1, 1, tzinfo=TZ)
        else:
            end_time = datetime(year, month + 1, 1, tzinfo=TZ)
        date_str = f"{year}年{month}月"

        # 统计数据
        new_records = self.inbox_ops.search_records(
            start_date=start_time,
            end_date=end_time,
            limit=None
        )

        completed_tasks = self.inbox_ops.search_records(
            content_type='todo',
            status='completed',
            start_date=start_time,
            end_date=end_time,
            limit=None
        )

        # 按周统计
        weekly_stats = {}
        for record in new_records:
            try:
                ts = datetime.fromisoformat(record['frontmatter'].get('timestamp', '')).astimezone(self._tz)
                week = ts.isocalendar()[1]
                if week not in weekly_stats:
                    weekly_stats[week] = {'records': 0, 'completed': 0}
                weekly_stats[week]['records'] += 1
            except:
                pass

        for task in completed_tasks:
            try:
                ts = datetime.fromtimestamp(Path(task['path']).stat().st_mtime, self._tz)
                week = ts.isocalendar()[1]
                if week not in weekly_stats:
                    weekly_stats[week] = {'records': 0, 'completed': 0}
                weekly_stats[week]['completed'] += 1
            except:
                pass

        # 内容类型分布
        content_type_dist = {}
        for record in new_records:
            ct = record['frontmatter'].get('content_type', 'note')
            content_type_dist[ct] = content_type_dist.get(ct, 0) + 1

        report_content = f"""# 月报：{date_str}

## 📊 本月概览
- 新增记录：{len(new_records)} 条
- 完成任务：{len(completed_tasks)} 个

## 📈 内容类型分布
"""
        for ct, count in content_type_dist.items():
            percentage = count / len(new_records) * 100 if new_records else 0
            report_content += f"- {ct}: {count} 条 ({percentage:.1f}%)\n"

        report_content += """
## 📅 每周统计
| 周数 | 新增记录 | 完成任务 |
|------|----------|----------|
"""
        for week in sorted(weekly_stats.keys()):
            stats = weekly_stats[week]
            report_content += f"| 第{week}周 | {stats['records']} | {stats['completed']} |\n"

        report_content += f"""
## 💡 月度总结
本月共记录 {len(new_records)} 条内容，完成 {len(completed_tasks)} 个任务，效率不错，下个月继续加油！
"""

        # 保存报告
        report_dir = self.reports_dir / 'Monthly'
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"Report-Monthly-{year}-{month:02d}.md"
        report_file.write_text(report_content, encoding='utf-8')

        return report_content, str(report_file)

    def get_long_term_review_reminder(self):
        """生成长期事项回顾提醒（每3天提醒一次）"""
        # 获取长期任务：等待中、项目、将来做
        long_term_categories = ['Waiting', 'Projects', 'Someday']
        long_term_tasks = []

        for category in long_term_categories:
            dir_path = self.data_dir / '02-Tasks' / category
            if not dir_path.exists():
                continue

            for md_file in dir_path.glob('*.md'):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    frontmatter, _ = parse_frontmatter(content)

                    content = self.todo_generator._extract_task_content(content)
                    long_term_tasks.append({
                        'content': content,
                        'category': category,
                        'path': str(md_file)
                    })
                except:
                    continue

        # 生成提醒消息
        message = "🔍 长期事项回顾提醒\n\n"
        message += "以下是长期待办事项，请检查是否需要调整：\n\n"

        category_names = {
            'Waiting': '⏳ 等待中',
            'Projects': '📦 进行中项目',
            'Someday': '🔮 将来做'
        }

        for category in long_term_categories:
            tasks = [t for t in long_term_tasks if t['category'] == category]
            if tasks:
                message += f"{category_names[category]}（共{len(tasks)}个）：\n"
                for i, task in enumerate(tasks, 1):
                    message += f"{i}. {task['content']}\n"
                message += "\n"

        message += "请告知需要如何处理这些任务（继续等待/调整优先级/标记完成/删除）。"

        return message, long_term_tasks

    def get_weekly_review_reminder(self):
        """生成周度回顾提醒"""
        now = datetime.now(TZ)
        week = now.isocalendar()[1]

        message = f"📋 周度回顾提醒（第{week}周）\n\n"
        message += "又到周日啦，本周的工作生活都顺利吗？请花10分钟时间回顾一下本周：\n\n"
        message += "1. 检查收件箱是否还有未分类的内容\n"
        message += "2. 整理已完成的任务和项目\n"
        message += "3. 规划下周的重点任务和目标\n"
        message += "4. 清理不需要的待办和记录\n\n"
        message += '需要我帮你生成本周的周报吗？回复"是"即可生成。'

        return message

    def backup_data(self):
        """数据自动备份"""
        import shutil
        now = datetime.now(TZ)
        backup_dir = self.data_dir / '.metadata' / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"backup-{now.strftime('%Y%m%d-%H%M%S')}.tar.gz"

        # 打包数据目录（排除备份目录本身）
        shutil.make_archive(
            str(backup_file.with_suffix('')),
            'gztar',
            root_dir=self.data_dir,
            exclude=lambda x: x.startswith('.metadata/backups')
        )

        # 只保留最近7个备份
        backups = sorted(backup_dir.glob('*.tar.gz'), key=lambda x: x.stat().st_mtime, reverse=True)
        if len(backups) > 7:
            for old_backup in backups[7:]:
                old_backup.unlink()

        return str(backup_file)

if __name__ == "__main__":
    import sys
    reviewer = ReviewReminder()

    if len(sys.argv) < 2:
        print("用法:")
        print("  review_reminder.py daily-report   # 生成今日日报")
        print("  review_reminder.py weekly-report  # 生成本周周报")
        print("  review_reminder.py monthly-report # 生成本月月报")
        print("  review_reminder.py long-term      # 生成长期事项提醒")
        print("  review_reminder.py backup         # 备份数据")
        sys.exit(1)

    if sys.argv[1] == 'daily-report':
        content, path = reviewer.generate_daily_report()
        print(f"日报已生成：{path}")
        print("\n内容预览：")
        print(content[:500] + "..." if len(content) > 500 else content)

    elif sys.argv[1] == 'weekly-report':
        content, path = reviewer.generate_weekly_report()
        print(f"周报已生成：{path}")

    elif sys.argv[1] == 'monthly-report':
        content, path = reviewer.generate_monthly_report()
        print(f"月报已生成：{path}")

    elif sys.argv[1] == 'long-term':
        msg, tasks = reviewer.get_long_term_review_reminder()
        print(msg)

    elif sys.argv[1] == 'backup':
        backup_path = reviewer.backup_data()
        print(f"数据已备份到：{backup_path}")
