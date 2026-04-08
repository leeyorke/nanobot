"""
私人秘书技能
实现"想法随时记录→自动组织→每日提醒→定期回顾→历史查询"完整工作流
"""

__version__ = "1.0.0"
__author__ = "leeyorke"

from .main import handle, get_scheduled_tasks
from .cli import main