#!/usr/bin/env python3
"""
yoyo技能通用工具函数
"""
from pathlib import Path
from datetime import timezone, timedelta


def get_config_value(config, key_path, default=None):
    """
    安全获取配置值，支持dict和pydantic model嵌套路径

    Args:
        config: 配置对象（dict或pydantic model）
        key_path: 配置键路径，如'personal_secretary.data_dir'或['personal_secretary', 'data_dir']
        default: 默认值

    Returns:
        配置值或默认值
    """
    if config is None:
        return default

    # 解析路径
    if isinstance(key_path, str):
        keys = key_path.split('.')
    else:
        keys = key_path

    # 递归获取值
    current = config
    for key in keys:
        if current is None:
            return default

        if hasattr(current, key):
            current = getattr(current, key)
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return default

    return current if current is not None else default


def get_timezone(config=None):
    """
    获取时区配置，优先使用配置时区，其次使用系统时区

    Args:
        config: 配置对象

    Returns:
        timezone对象
    """
    # 从配置获取
    tz_str = get_config_value(config, 'personal_secretary.timezone', None)
    if tz_str:
        try:
            # 支持IANA时区标识：Asia/Shanghai
            from zoneinfo import ZoneInfo
            return ZoneInfo(tz_str)
        except Exception:
            pass

    # 回退到系统时区或默认北京时间
    try:
        return datetime.now().astimezone().tzinfo
    except Exception:
        return timezone(timedelta(hours=8))


def get_data_dir(config=None):
    """
    获取数据存储目录路径

    Args:
        config: 配置对象

    Returns:
        Path对象
    """
    raw_path = get_config_value(
        config,
        'personal_secretary.data_dir',
        '~/.nanobot/workspace/personal-secretary/'
    )
    return Path(raw_path).expanduser().resolve()


class PersonalSecretaryError(Exception):
    """yoyo技能基础异常类"""
    pass


class FileOperationError(PersonalSecretaryError):
    """文件操作异常"""
    pass


class ValidationError(PersonalSecretaryError):
    """数据验证异常"""
    pass
