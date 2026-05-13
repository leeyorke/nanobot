#!/usr/bin/env python3
"""
通用内容分类模块：自动识别内容类型，提取元数据（时间、优先级、标签等）
"""
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from .helpers import get_timezone

class ContentClassifier:
    def __init__(self, data_dir, config=None):
        """
        初始化分类器
        :param data_dir: 数据存储目录，用于读取分类规则
        :param config: 配置对象，用于获取时区
        """
        self.data_dir = Path(data_dir)
        self._tz = get_timezone(config)
        self.rules = self._load_rules()

    def _load_rules(self):
        """加载分类规则"""
        rules_file = self.data_dir / '.metadata' / 'category_rules.json'
        if rules_file.exists():
            return json.loads(rules_file.read_text(encoding='utf-8'))
        else:
            # 默认规则
            return {
                "content_types": {
                    "todo": ["todo", "待办", "任务", "需要做", "要完成", "记得", "别忘了", "必须", "应该", "要去"],
                    "note": ["笔记", "记录", "想法", "灵感", "随想", "感想", "突然想到", "今天"],
                    "link": ["http://", "https://", "www.", "网址", "链接", "网页", "网站"],
                    "event": ["会议", "约会", "聚会", "活动", "纪念日", "日程", "安排", "和谁", "见谁", "去"],
                    "resource": ["资源", "资料", "文档", "电子书", "工具", "下载", "推荐", "好用的"]
                },
                "priority_keywords": {
                    "high": ["紧急", "重要", "马上", "立刻", "尽快", "必须", "高优", "优先级高"],
                    "medium": ["中等", "中优", "优先级中"],
                    "low": ["不急", "有空", "慢慢", "优先级低", "低优"]
                },
                "time_patterns": [
                    # 绝对时间
                    r"(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2})[:点](\d{1,2})?",
                    r"(\d{1,2})月(\d{1,2})日\s*(\d{1,2})[:点](\d{1,2})?",
                    r"(\d{1,2})[:点](\d{1,2})",

                    # 相对时间
                    r"明天\s*(\d{1,2})?[:点]?(\d{1,2})?",
                    r"后天\s*(\d{1,2})?[:点]?(\d{1,2})?",
                    r"下周(一|二|三|四|五|六|日|天)\s*(\d{1,2})?[:点]?(\d{1,2})?",
                    r"下周一\s*(\d{1,2})?[:点]?(\d{1,2})?",
                    r"这(周|个)(一|二|三|四|五|六|日|天)\s*(\d{1,2})?[:点]?(\d{1,2})?",
                    r"(\d+)分钟后",
                    r"(\d+)小时后",
                    r"(\d+)天后",
                ]
            }

    def classify(self, content):
        """
        对内容进行分类，提取元数据
        :param content: 输入内容文本
        :return: 分类结果字典，包含content_type, priority, due_date, tags, confidence等字段
        """
        result = {
            "content_type": "note",  # 默认是笔记类型
            "priority": "medium",
            "due_date": None,
            "tags": [],
            "confidence": 0.5,
            "extracted_info": {}
        }

        content_lower = content.lower()

        # 1. 识别内容类型
        type_scores = {}
        for content_type, keywords in self.rules.get('content_types', {}).items():
            score = 0
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
            if score > 0:
                type_scores[content_type] = score

        if type_scores:
            # 取得分最高的类型
            max_score = max(type_scores.values())
            best_types = [t for t, s in type_scores.items() if s == max_score]
            result['content_type'] = best_types[0]
            result['confidence'] = min(1.0, max_score / 3.0)  # 最多3个关键词匹配，置信度最高1.0

        # 2. 识别优先级
        priority_scores = {}
        for priority, keywords in self.rules.get('priority_keywords', {}).items():
            score = 0
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
            if score > 0:
                priority_scores[priority] = score

        if priority_scores:
            max_score = max(priority_scores.values())
            best_priorities = [p for p, s in priority_scores.items() if s == max_score]
            result['priority'] = best_priorities[0]

        # 3. 提取标签（#标签格式）
        tags = re.findall(r'#(\w+)', content)
        result['tags'] = list(set(tags))

        # 4. 提取时间信息
        due_date = self._extract_time(content)
        if due_date:
            result['due_date'] = due_date
            # 如果有明确的时间，且是待办类型，提升置信度
            if result['content_type'] == 'todo':
                result['confidence'] = min(1.0, result['confidence'] + 0.2)

        # 5. 提取URL链接
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', content)
        if urls:
            result['extracted_info']['urls'] = urls
            # 如果有链接，且不是明确的其他类型，识别为link类型
            if result['content_type'] == 'note' and result['confidence'] < 0.7:
                result['content_type'] = 'link'
                result['confidence'] = 0.8

        # 6. 提取@提及的人
        mentions = re.findall(r'@(\w+)', content)
        if mentions:
            result['extracted_info']['mentions'] = mentions
            # 如果有@提及，可能是等待中类型的待办
            if result['content_type'] == 'todo':
                result['extracted_info']['need_wait'] = True

        return result

    def _extract_time(self, content):
        """
        从内容中提取时间信息
        :param content: 输入文本
        :return: datetime对象或None
        """
        now = datetime.now(self._tz)
        content_lower = content.lower()

        # 1. 匹配 "明天下午3点" 这种格式
        match = re.search(r"明天\s*(上午|下午|晚上|凌晨)?\s*(\d{1,2})?[:点]?(\d{1,2})?", content_lower)
        if match:
            period = match.group(1) or '上午'
            hour = int(match.group(2)) if match.group(2) else 9
            minute = int(match.group(3)) if match.group(3) else 0

            # 处理上午/下午
            if period == '下午' and hour < 12:
                hour += 12
            elif period == '晚上' and hour < 12:
                hour += 12
            elif period == '凌晨' and hour > 6:
                hour = hour  # 凌晨保持不变

            due_date = now + timedelta(days=1)
            due_date = due_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return due_date

        # 2. 匹配 "后天上午10点"
        match = re.search(r"后天\s*(上午|下午|晚上|凌晨)?\s*(\d{1,2})?[:点]?(\d{1,2})?", content_lower)
        if match:
            period = match.group(1) or '上午'
            hour = int(match.group(2)) if match.group(2) else 9
            minute = int(match.group(3)) if match.group(3) else 0

            if period == '下午' and hour < 12:
                hour += 12
            elif period == '晚上' and hour < 12:
                hour += 12

            due_date = now + timedelta(days=2)
            due_date = due_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return due_date

        # 3. 匹配 "X分钟后"
        match = re.search(r"(\d+)分钟后", content_lower)
        if match:
            minutes = int(match.group(1))
            due_date = now + timedelta(minutes=minutes)
            due_date = due_date.replace(second=0, microsecond=0)
            return due_date

        # 4. 匹配 "X小时后"
        match = re.search(r"(\d+)小时后", content_lower)
        if match:
            hours = int(match.group(1))
            due_date = now + timedelta(hours=hours)
            due_date = due_date.replace(second=0, microsecond=0)
            return due_date

        # 5. 匹配 "X天后"
        match = re.search(r"(\d+)天后", content_lower)
        if match:
            days = int(match.group(1))
            due_date = now + timedelta(days=days)
            due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)
            return due_date

        # 6. 匹配具体时间 "15:30" 或 "下午3点"
        match = re.search(r"(上午|下午|晚上|凌晨)?\s*(\d{1,2})[:点](\d{1,2})?", content_lower)
        if match:
            period = match.group(1) or '上午'
            hour = int(match.group(2))
            minute = int(match.group(3)) if match.group(3) else 0

            if period == '下午' and hour < 12:
                hour += 12
            elif period == '晚上' and hour < 12:
                hour += 12
            elif period == '凌晨' and hour > 6:
                hour = hour

            # 如果时间已经过了今天，默认是明天
            due_date = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if due_date < now:
                due_date += timedelta(days=1)

            return due_date

        # 7. 匹配完整日期 "2026年4月8日15:30"
        match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:点]?(\d{1,2})?", content)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4)) if match.group(4) else 9
            minute = int(match.group(5)) if match.group(5) else 0

            try:
                due_date = datetime(year, month, day, hour, minute, tzinfo=self._tz)
                return due_date
            except ValueError:
                pass

        return None

if __name__ == "__main__":
    # 测试代码
    import sys
    if len(sys.argv) < 2:
        print("用法: content_classifier.py <内容文本>")
        sys.exit(1)

    # 临时用当前目录作为data_dir
    classifier = ContentClassifier('.')
    result = classifier.classify(sys.argv[1])

    print("分类结果：")
    print(f"内容类型: {result['content_type']} (置信度: {result['confidence']:.2f})")
    print(f"优先级: {result['priority']}")
    print(f"截止时间: {result['due_date'].isoformat() if result['due_date'] else '无'}")
    print(f"标签: {', '.join(result['tags']) if result['tags'] else '无'}")
    print(f"提取信息: {result['extracted_info']}")
