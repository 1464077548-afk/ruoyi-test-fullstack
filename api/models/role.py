from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Role:
    """角色模型"""
    roleId: Optional[int] = None
    roleName: Optional[str] = None
    roleKey: Optional[str] = None
    roleSort: Optional[int] = None
    dataScope: Optional[str] = None
    menuCheckStrictly: Optional[bool] = None
    deptCheckStrictly: Optional[bool] = None
    status: Optional[str] = None
    delFlag: Optional[str] = None
    createBy: Optional[str] = None
    createTime: Optional[str] = None
    updateBy: Optional[str] = None
    updateTime: Optional[str] = None
    remark: Optional[str] = None
    menuIds: Optional[List[int]] = None
    deptIds: Optional[List[int]] = None


@dataclass
class RoleQuery:
    """角色查询模型"""
    pageNum: int = 1
    pageSize: int = 10
    roleName: Optional[str] = None
    roleKey: Optional[str] = None
    status: Optional[str] = None
    beginTime: Optional[str] = None
    endTime: Optional[str] = None
