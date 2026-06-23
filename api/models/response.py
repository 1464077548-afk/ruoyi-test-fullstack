from typing import Optional, Any, List
from dataclasses import dataclass


@dataclass
class ApiResponse:
    """API响应模型"""
    code: int
    msg: str
    data: Optional[Any] = None


@dataclass
class PageData:
    """分页数据模型"""
    list: List[Any]
    total: int
    pageNum: int
    pageSize: int


@dataclass
class LoginResponse:
    """登录响应模型"""
    token: str
    user: dict


@dataclass
class UserInfoResponse:
    """用户信息响应模型"""
    roles: List[str]
    permissions: List[str]
    user: dict
