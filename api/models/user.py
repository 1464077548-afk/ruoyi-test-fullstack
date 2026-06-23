from typing import Optional, List
from dataclasses import dataclass


@dataclass
class User:
    """用户模型"""
    userId: Optional[int] = None
    deptId: Optional[int] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    status: Optional[str] = None
    delFlag: Optional[str] = None
    loginIp: Optional[str] = None
    loginDate: Optional[str] = None
    createBy: Optional[str] = None
    createTime: Optional[str] = None
    updateBy: Optional[str] = None
    updateTime: Optional[str] = None
    remark: Optional[str] = None
    dept: Optional[dict] = None
    roles: Optional[List[dict]] = None
    roleIds: Optional[List[int]] = None
    postIds: Optional[List[int]] = None


@dataclass
class UserQuery:
    """用户查询模型"""
    pageNum: int = 1
    pageSize: int = 10
    username: Optional[str] = None
    nickname: Optional[str] = None
    status: Optional[str] = None
    deptId: Optional[int] = None
    beginTime: Optional[str] = None
    endTime: Optional[str] = None
    
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseResponse, PaginatedResponse, PaginatedData


class UserBase(BaseModel):
    """用户基础模型"""
    userName: Optional[str] = Field(None, description="用户名")
    nickName: Optional[str] = Field(None, description="昵称")
    email: Optional[str] = Field(None, description="邮箱")
    phonenumber: Optional[str] = Field(None, description="手机号码")
    sex: Optional[str] = Field(None, description="性别")
    avatar: Optional[str] = Field(None, description="头像")
    status: Optional[str] = Field(None, description="状态")
    deptId: Optional[int] = Field(None, description="部门ID")


class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """更新用户模型"""
    userId: int = Field(..., description="用户ID")
    userName: Optional[str] = Field(None, description="用户名")
    nickName: Optional[str] = Field(None, description="昵称")
    email: Optional[str] = Field(None, description="邮箱")
    phonenumber: Optional[str] = Field(None, description="手机号码")
    sex: Optional[str] = Field(None, description="性别")
    avatar: Optional[str] = Field(None, description="头像")
    status: Optional[str] = Field(None, description="状态")
    deptId: Optional[int] = Field(None, description="部门ID")


class UserResponse(UserBase):
    """用户响应模型"""
    userId: Optional[int] = Field(None, description="用户ID")
    createBy: Optional[str] = Field(None, description="创建人")
    createTime: Optional[datetime] = Field(None, description="创建时间")
    updateBy: Optional[str] = Field(None, description="更新人")
    updateTime: Optional[datetime] = Field(None, description="更新时间")
    remark: Optional[str] = Field(None, description="备注")
    delFlag: Optional[str] = Field(None, description="删除标志")
    loginIp: Optional[str] = Field(None, description="登录IP")
    loginDate: Optional[datetime] = Field(None, description="登录时间")
    pwdUpdateDate: Optional[datetime] = Field(None, description="密码更新时间")


class UserInfoResponse(BaseResponse):
    """用户信息响应模型"""
    user: Optional[UserResponse] = Field(None, description="用户信息")
    roles: Optional[List[str]] = Field(None, description="角色列表")
    permissions: Optional[List[str]] = Field(None, description="权限列表")


class UserListResponse(PaginatedResponse):
    """用户列表响应模型"""
    data: Optional[PaginatedData[UserResponse]] = Field(None, description="用户列表数据")


class UserProfileResponse(BaseResponse):
    """用户个人信息响应模型"""
    data: Optional[UserResponse] = Field(None, description="用户信息")
