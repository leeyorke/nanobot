# {{report_type}}报告：{{date}}

## 📊 今日概览
- 新增记录：{{new_records_count}} 条
- 完成任务：{{completed_tasks_count}} 个
- 待完成任务：{{pending_tasks_count}} 个
- 待分类记录：{{unclassified_count}} 条

## ⚡ 今日待完成任务
{% for task in today_tasks %}
- [ ] {{task.content}} {% if task.due_date %}⏰ {{task.due_date.strftime('%Y-%m-%d %H:%M')}}{% endif %}
{% endfor %}

## ✅ 今日已完成任务
{% for task in completed_tasks %}
- [x] {{task.content}} ✅ {{task.completed_time.strftime('%Y-%m-%d %H:%M')}}
{% endfor %}

## 📝 今日新增记录
{% for record in new_records %}
- {{record.timestamp.strftime('%H:%M')}} [{{record.content_type}}] {{record.title}}
{% endfor %}

## 🎯 明日计划
{% for task in tomorrow_tasks %}
- [ ] {{task.content}} {% if task.due_date %}⏰ {{task.due_date.strftime('%Y-%m-%d %H:%M')}}{% endif %}
{% endfor %}

## 💡 总结与建议
{{summary}}
