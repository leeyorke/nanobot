#!/usr/bin/env python3
"""
GTD分类模块：对待办事项进行GTD分类，自动更新Kanban文件
"""
import json
import re
from datetime import datetime, timezone, timedelta
from .helpers import get_timezone, parse_frontmatter
from pathlib import Path
import yaml
from .inbox_operations import InboxOperations

# 北京时间时区

class GTDClassifier:
    def __init__(self, data_dir, config=None):
        """
        初始化GTD分类器
        :param data_dir: 数据存储目录
        """
        self.data_dir = Path(data_dir)
        self._tz = get_timezone(config)
        self.config = self._load_config()
        self.inbox_ops = InboxOperations(config)

        # GTD分类对应的目录和Kanban列名
        self.gtd_mapping = {
            "Now": {"dir": "02-Tasks/Now", "kanban_column": "⚡ 立即做"},
            "Next": {"dir": "02-Tasks/Next", "kanban_column": "🚶 下一步行动"},
            "Calendar": {"dir": "02-Tasks/Calendar", "kanban_column": "📅 日程"},
            "Waiting": {"dir": "02-Tasks/Waiting", "kanban_column": "⏳ 等待中"},
            "Projects": {"dir": "02-Tasks/Projects", "kanban_column": "📦 项目"},
            "Someday": {"dir": "02-Tasks/Someday", "kanban_column": "🔮 将来做"},
            "Completed": {"dir": "02-Tasks/Completed", "kanban_column": "✅ 已完成"},
            "Deleted": {"dir": "02-Tasks/Deleted", "kanban_column": "🗑️ 已删除"}
        }

    def _load_config(self):
        """加载GTD配置"""
        config_file = self.data_dir / '.metadata' / 'gtd_config.json'
        if config_file.exists():
            return json.loads(config_file.read_text(encoding='utf-8'))
        else:
            return {
                "classification_rules": {
                    "Now": {"max_duration": 120, "priority": "high"},
                    "Next": {"has_next_action": True},
                    "Calendar": {"has_due_date": True},
                    "Waiting": {"depend_on_others": True},
                    "Projects": {"needs_multiple_steps": True},
                    "Someday": {"no_clear_time": True}
                }
            }

    def classify_todo(self, todo_record):
        """
        对单个待办事项进行GTD分类
        :param todo_record: 待办记录，包含frontmatter和content字段
        :return: 分类结果（GTD分类名，置信度）
        """
        frontmatter = todo_record.get('frontmatter', {})
        content = todo_record.get('content', '').lower()
        scores = {}

        rules = self.config.get('classification_rules', {})

        # 1. 立即做（Now）：高优先级 + 2小时内能完成
        if frontmatter.get('priority') == 'high':
            # 简单判断：内容长度短，没有复杂描述，通常可以快速完成
            if len(content) < 100 or "马上" in content or "立刻" in content or "紧急" in content:
                scores['Now'] = 0.9

        # 2. 日程（Calendar）：有明确截止时间的
        if frontmatter.get('due_date'):
            scores['Calendar'] = 0.95

        # 3. 等待中（Waiting）：需要等待他人的
        if "@" in content or "等" in content or "等待" in content or "回复" in content or "审批" in content:
            scores['Waiting'] = 0.85

        # 4. 项目（Projects）：需要多个步骤，或提到"项目"、"开发"、"设计"、"规划"等关键词
        if "项目" in content or "开发" in content or "设计" in content or "规划" in content or "多个" in content or "步骤" in content:
            scores['Projects'] = 0.8

        # 5. 将来做（Someday）：没有明确时间，提到"以后"、"将来"、"有空"、"改天"等
        if "以后" in content or "将来" in content or "有空" in content or "改天" in content or "未来" in content:
            scores['Someday'] = 0.8

        # 6. 下一步行动（Next）：其他有明确动作的待办
        if not scores:
            scores['Next'] = 0.7

        # 取得分最高的分类
        max_score = max(scores.values())
        best_categories = [cat for cat, score in scores.items() if score == max_score]

        return best_categories[0], max_score

    def process_pending_todos(self):
        """处理Pending目录下所有待分类的待办"""
        pending_dir = self.data_dir / '02-Tasks' / 'Pending'
        if not pending_dir.exists():
            return []

        processed = []

        for md_file in pending_dir.glob('*.md'):
            try:
                # 读取记录
                content = md_file.read_text(encoding='utf-8')
                frontmatter, body = parse_frontmatter(content)
                body = body.strip()

                todo_record = {
                    'path': str(md_file),
                    'frontmatter': frontmatter,
                    'content': body
                }

                # 分类
                category, confidence = self.classify_todo(todo_record)

                if confidence >= 0.7:
                    # 移动到对应目录
                    target_dir = self.gtd_mapping[category]['dir']
                    target_path = self.inbox_ops.move_record(str(md_file), target_dir)

                    # 更新frontmatter的status和category
                    frontmatter['status'] = 'classified'
                    frontmatter['gtd_category'] = category
                    frontmatter['classification_confidence'] = confidence

                    # 重新写入文件
                    yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
                    new_content = f"---\n{yaml_content}---\n\n{body}\n"
                    target_path.write_text(new_content, encoding='utf-8')

                    processed.append({
                        'file': str(md_file),
                        'category': category,
                        'confidence': confidence,
                        'target_path': str(target_path)
                    })
                else:
                    # 置信度低，保留在Pending，后续需要询问用户
                    processed.append({
                        'file': str(md_file),
                        'category': 'Pending',
                        'confidence': confidence,
                        'note': '置信度低，需要用户确认分类'
                    })

            except Exception as e:
                print(f"处理待办 {md_file} 失败: {e}")
                continue

        # 更新Kanban文件
        self.update_kanban()

        return processed

    def update_kanban(self):
        """更新Kanban文件，保持与目录结构同步"""
        kanban_file = self.data_dir / '📋 kanban.md'

        # 读取现有的Kanban内容，保留frontmatter
        if kanban_file.exists():
            content = kanban_file.read_text(encoding='utf-8')
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    body = parts[2]
                else:
                    frontmatter = "kanban-plugin: basic"
                    body = content
            else:
                frontmatter = "kanban-plugin: basic"
                body = content
        else:
            frontmatter = "kanban-plugin: basic"
            body = ""

        # 按列收集所有任务
        kanban_columns = {}

        # 遍历每个GTD分类，收集任务
        for category, mapping in self.gtd_mapping.items():
            if category in ['Deleted']:
                continue  # 已删除的不显示在Kanban

            column_name = mapping['kanban_column']
            dir_path = self.data_dir / mapping['dir']

            tasks = []
            if dir_path.exists():
                for md_file in dir_path.glob('*.md'):
                    try:
                        file_content = md_file.read_text(encoding='utf-8')
                        frontmatter_task, task_body = parse_frontmatter(file_content)
                        task_body = task_body.strip()

                        # 提取任务内容（去掉标题，取第一个任务项）
                        task_lines = task_body.split('\n')
                        task_content = ""
                        for line in task_lines:
                            if line.strip().startswith('- ['):
                                task_content = line.strip()
                                break
                        if not task_content:
                            # 如果没有任务项，取第一行正文
                            task_content = task_lines[0].strip() if task_lines else md_file.stem

                        # 添加时间标记
                        due_date = frontmatter_task.get('due_date')
                        if due_date and category in ['Now', 'Next', 'Calendar']:
                            try:
                                if isinstance(due_date, str):
                                    due_date_dt = datetime.fromisoformat(due_date).astimezone(self._tz)
                                    task_content += f" ⏰ {due_date_dt.strftime('%Y-%m-%d %H:%M')}"
                            except:
                                pass

                        # 添加完成时间标记
                        if category == 'Completed':
                            mtime = datetime.fromtimestamp(md_file.stat().st_mtime, self._tz)
                            task_content = task_content.replace('- [ ]', '- [x]')
                            task_content += f" ✅ {mtime.strftime('%Y-%m-%d %H:%M')}"

                        tasks.append(task_content)

                    except Exception as e:
                        print(f"读取任务文件 {md_file} 失败: {e}")
                        continue

            kanban_columns[column_name] = tasks

        # 生成新的Kanban内容
        new_body = ""
        # 按顺序生成列
        column_order = [
            "⚡ 立即做",
            "🚶 下一步行动",
            "📅 日程",
            "⏳ 等待中",
            "📦 项目",
            "🔮 将来做",
            "✅ 已完成"
        ]

        for column_name in column_order:
            new_body += f"\n## {column_name}\n\n"
            tasks = kanban_columns.get(column_name, [])
            if tasks:
                for task in tasks:
                    new_body += f"{task}\n"
            else:
                new_body += "*暂无任务*\n"
            new_body += "\n"

        # 写入Kanban文件
        new_content = f"---\n{frontmatter}---\n{new_body}"
        kanban_file.write_text(new_content, encoding='utf-8')

        return kanban_file
