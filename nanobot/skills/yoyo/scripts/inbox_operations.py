#!/usr/bin/env python3
"""
收件箱操作模块：实现记录的增删改查功能
"""
import os
import json
import uuid
import time
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import yaml
from .helpers import get_data_dir, get_timezone, PersonalSecretaryError, FileOperationError

# 时区（从配置获取）
TZ = None  # 延迟到第一次使用时获取

class InboxOperations:
    def __init__(self, config=None):
        """
        初始化收件箱操作
        :param config: 配置对象，包含data_dir等配置
        """
        self.config = config or {}
        self.data_dir = get_data_dir(config)
        self._tz = get_timezone(config)
        self._init_directory_structure()

    def _init_directory_structure(self):
        """初始化目录结构，如果不存在则创建"""
        # 顶层目录
        dirs = [
            '01-Inbox',
            '02-Tasks/Pending',
            '02-Tasks/Now',
            '02-Tasks/Next',
            '02-Tasks/Calendar',
            '02-Tasks/Waiting',
            '02-Tasks/Projects',
            '02-Tasks/Someday',
            '02-Tasks/Completed',
            '02-Tasks/Deleted',
            '03-Notes/Memo',
            '03-Notes/Daily',
            '03-Notes/Learn',
            '04-Events/Activities',
            '05-Resources/Links',
            '05-Resources/Scripts',
            '05-Resources/Assets',
            '05-Resources/Docs',
            '06-Tags',
            '07-Reports/Daily',
            '07-Reports/Weekly',
            '07-Reports/Monthly',
            '07-Reports/Review',
            '.metadata/backups'
        ]

        for dir_path in dirs:
            full_path = self.data_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)

        # 创建默认的固定文件
        self._init_fixed_files()

    def _init_fixed_files(self):
        """初始化固定文件"""
        # habits.md
        habits_file = self.data_dir / '04-Events' / 'habits.md'
        if not habits_file.exists():
            habits_file.write_text("""# 习惯跟踪

## 每日习惯
- [ ] 早起（7点前）
- [ ] 运动30分钟
- [ ] 阅读1小时
- [ ] 写日记

## 每周习惯
- [ ] 周度回顾
- [ ] 大扫除
- [ ] 联系朋友
""")

        # hello.md
        hello_file = self.data_dir / '04-Events' / 'hello.md'
        if not hello_file.exists():
            hello_file.write_text("""# 每日寄语

今天又是充满希望的一天！加油！
""")

        # kanban.md
        kanban_file = self.data_dir / '📋 kanban.md'
        if not kanban_file.exists():
            kanban_template = Path(__file__).parent.parent / 'assets' / 'kanban_template.md'
            if kanban_template.exists():
                kanban_content = kanban_template.read_text()
                kanban_file.write_text(kanban_content)
            else:
                # 默认kanban模板
                kanban_file.write_text("""---
kanban-plugin: basic
---

## ⚡ 立即做

- [ ] 示例：2小时内能完成的紧急任务

## 🚶 下一步行动

- [ ] 示例：有明确下一步动作的任务

## 📅 日程

- [ ] 示例：有具体日期时间的安排

## ⏳ 等待中

- [ ] 示例：需要等待他人或外部条件的任务

## 📦 项目

- [ ] 示例：需要多步骤完成的大项目

## 🔮 将来做

- [ ] 示例：未来某一天要做的，暂无明确时间的任务

## ✅ 已完成

- [x] 示例：已经完成的任务
""")

        # 元数据配置文件
        metadata_files = [
            ('.metadata/category_rules.json', {
                "content_types": {
                    "todo": ["todo", "待办", "任务", "需要做", "要完成"],
                    "note": ["笔记", "记录", "想法", "灵感", "随想"],
                    "link": ["链接", "网址", "http", "https", "www."],
                    "event": ["会议", "约会", "聚会", "活动", "纪念日", "日程"],
                    "resource": ["资源", "资料", "文档", "电子书", "工具"]
                }
            }),
            ('.metadata/schedule_config.json', {
                "remind_morning": "08:00",
                "remind_evening": "21:00",
                "remind_long_term_days": 3,
                "remind_weekly": "Sunday 20:00",
                "auto_backup": True
            }),
            ('.metadata/gtd_config.json', {
                "classification_rules": {
                    "Now": {"max_duration": 120, "priority": "high"},
                    "Next": {"has_next_action": True},
                    "Calendar": {"has_due_date": True},
                    "Waiting": {"depend_on_others": True},
                    "Projects": {"needs_multiple_steps": True},
                    "Someday": {"no_clear_time": True}
                }
            })
        ]

        for file_path, default_content in metadata_files:
            full_path = self.data_dir / file_path
            if not full_path.exists():
                full_path.write_text(json.dumps(default_content, ensure_ascii=False, indent=2))

    def add_record(self, content, content_type=None, source="user_input", tags=None, priority=None, due_date=None):
        """
        添加新记录到收件箱
        :param content: 记录内容
        :param content_type: 内容类型：todo/note/link/event/resource，自动识别如果为None
        :param source: 记录来源
        :param tags: 标签列表
        :param priority: 优先级：high/medium/low
        :param due_date: 截止时间，datetime对象或字符串
        :return: 创建的记录文件路径
        """
        # 自动识别内容类型
        if not content_type:
            content_type = self._detect_content_type(content)

        # 处理待办内容，自动添加任务列表格式
        if content_type == 'todo' and not re.match(r'^\s*-\s*\[\s*(x| )\s*\]', content):
            content = f"- [ ] {content.lstrip()}"

        # 生成元数据
        record_id = str(uuid.uuid4())
        timestamp = datetime.now(self._tz)
        timestamp_str = timestamp.isoformat()
        timestamp_int = int(time.time())

        # 处理截止时间
        if due_date:
            if isinstance(due_date, str):
                due_date = datetime.fromisoformat(due_date).astimezone(self._tz)
            due_date_str = due_date.isoformat()
        else:
            due_date_str = None

        # 处理标签
        tags = tags or []
        # 自动从内容中提取标签（#标签格式）
        auto_tags = re.findall(r'#(\w+)', content)
        tags.extend(auto_tags)
        tags = list(set(tags))

        # 生成文件名
        filename = f"Inbox-{timestamp_int}.md"
        file_path = self.data_dir / '01-Inbox' / filename

        # 构建YAML frontmatter
        frontmatter = {
            'id': record_id,
            'timestamp': timestamp_str,
            'content_type': content_type,
            'source': source,
            'status': 'unclassified',
            'tags': tags
        }

        if priority:
            frontmatter['priority'] = priority
        if due_date_str:
            frontmatter['due_date'] = due_date_str

        # 构建文件内容
        yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        content_header = f"# {self._get_content_title(content_type, content)}"
        file_content = f"---\n{yaml_content}---\n\n{content_header}\n\n{content}\n"

        # 写入文件
        file_path.write_text(file_content, encoding='utf-8')

        return file_path

    def _detect_content_type(self, content):
        """自动识别内容类型"""
        content_lower = content.lower()

        # 加载分类规则
        rules_file = self.data_dir / '.metadata' / 'category_rules.json'
        if rules_file.exists():
            rules = json.loads(rules_file.read_text())
            content_types = rules.get('content_types', {})
        else:
            content_types = {
                "todo": ["todo", "待办", "任务", "需要做", "要完成", "记得", "别忘了"],
                "note": ["笔记", "记录", "想法", "灵感", "随想", "感想"],
                "link": ["http://", "https://", "www.", "网址", "链接"],
                "event": ["会议", "约会", "聚会", "活动", "纪念日", "日程", "安排"],
                "resource": ["资源", "资料", "文档", "电子书", "工具", "下载"]
            }

        # 匹配规则
        for content_type, keywords in content_types.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return content_type

        # 默认是memo类型
        return "note"

    def _get_content_title(self, content_type, content):
        """获取内容标题"""
        titles = {
            "todo": "待办",
            "note": "笔记",
            "link": "链接",
            "event": "活动",
            "resource": "资源"
        }

        title_prefix = titles.get(content_type, "记录")
        # 取内容前20个字符作为标题
        content_plain = re.sub(r'^(\s*-\s*\[\s*(x| )\s*\]|\s*#+\s*)', '', content).strip()
        short_content = content_plain[:20] + "..." if len(content_plain) > 20 else content_plain

        return f"{title_prefix}：{short_content}"

    def search_records(self, query=None, content_type=None, tags=None, start_date=None, end_date=None, status=None, limit=20):
        """
        搜索记录
        :param query: 关键词查询
        :param content_type: 内容类型过滤
        :param tags: 标签列表过滤
        :param start_date: 开始时间，datetime对象
        :param end_date: 结束时间，datetime对象
        :param status: 状态过滤
        :param limit: 返回结果数量限制
        :return: 记录列表，每个记录包含元数据和内容
        """
        records = []

        # 遍历所有可能的目录
        search_dirs = [
            '01-Inbox',
            '02-Tasks',
            '03-Notes',
            '04-Events',
            '05-Resources'
        ]

        for base_dir in search_dirs:
            full_base_dir = self.data_dir / base_dir
            for md_file in full_base_dir.rglob('*.md'):
                # 跳过固定文件
                if md_file.name in ['habits.md', 'hello.md', '📋 kanban.md']:
                    continue

                try:
                    # 读取文件内容
                    content = md_file.read_text(encoding='utf-8')

                    # 解析YAML frontmatter
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            frontmatter = yaml.safe_load(parts[1])
                            body = parts[2].strip()
                        else:
                            frontmatter = {}
                            body = content
                    else:
                        frontmatter = {}
                        body = content

                    # 过滤条件
                    match = True

                    # 关键词过滤
                    if query and query.lower() not in body.lower() and query.lower() not in str(frontmatter).lower():
                        match = False

                    # 内容类型过滤
                    if content_type and frontmatter.get('content_type') != content_type:
                        match = False

                    # 标签过滤
                    if tags:
                        record_tags = frontmatter.get('tags', [])
                        if not any(tag in record_tags for tag in tags):
                            match = False

                    # 状态过滤
                    if status and frontmatter.get('status') != status:
                        match = False

                    # 时间范围过滤
                    if start_date or end_date:
                        record_ts = frontmatter.get('timestamp')
                        if record_ts:
                            try:
                                record_time = datetime.fromisoformat(record_ts).astimezone(self._tz)
                                if start_date and record_time < start_date:
                                    match = False
                                if end_date and record_time > end_date:
                                    match = False
                            except:
                                pass

                    if match:
                        records.append({
                            'path': str(md_file),
                            'frontmatter': frontmatter,
                            'content': body,
                            'mtime': md_file.stat().st_mtime
                        })

                except Exception as e:
                    print(f"读取文件 {md_file} 失败: {e}")
                    continue

        # 按修改时间倒序排序
        records.sort(key=lambda x: x['mtime'], reverse=True)

        # 限制返回数量
        if limit:
            records = records[:limit]

        return records

    def move_record(self, record_path, target_dir):
        """移动记录到目标目录"""
        source_path = Path(record_path)
        target_dir = self.data_dir / target_dir

        if not source_path.exists():
            raise FileNotFoundError(f"记录不存在：{record_path}")

        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / source_path.name

        # 移动文件
        source_path.rename(target_path)

        return target_path