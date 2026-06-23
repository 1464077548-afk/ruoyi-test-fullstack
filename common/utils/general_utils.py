"""纯工具函数，与页面无关，全项目（UI / 接口 / 性能）都能用"""
import random
import string
import time
from datetime import datetime, timedelta


def generate_random_string(length: int = 8) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email() -> str:
    """生成随机邮箱"""
    username = generate_random_string(10)
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', '163.com', 'qq.com']
    domain = random.choice(domains)
    return f"{username}@{domain}"


def generate_random_phone() -> str:
    """生成随机手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '170', '171', '172', '173', '175', '176', '177', '178',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}{suffix}"


def get_current_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_formatted_date(days: int = 0) -> str:
    """获取格式化的日期"""
    target_date = datetime.now() + timedelta(days=days)
    return target_date.strftime('%Y-%m-%d')


def wait_for_seconds(seconds: int = 1) -> None:
    """等待指定秒数"""
    time.sleep(seconds)


def format_dict_to_string(data: dict) -> str:
    """将字典格式化为字符串"""
    return ', '.join([f"{key}={value}" for key, value in data.items()])


def is_valid_email(email: str) -> bool:
    """验证邮箱格式是否有效"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """验证手机号格式是否有效"""
    import re
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def convert_to_int(value, default: int = 0) -> int:
    """将值转换为整数"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def convert_to_float(value, default: float = 0.0) -> float:
    """将值转换为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
