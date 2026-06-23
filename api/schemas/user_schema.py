from typing import Optional, List
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=1, max_length=50)
    nickname: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    sex: Optional[str] = Field(None, pattern="[012]")
    deptId: Optional[int] = None
    roleIds: Optional[List[int]] = None
    postIds: Optional[List[int]] = None
    remark: Optional[str] = None


class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., min_length=6, max_length=20)
    status: str = Field(..., pattern="[01]")


class UserUpdate(UserBase):
    """更新用户模型"""
    userId: int
    status: str = Field(..., pattern="[01]")


class UserStatusUpdate(BaseModel):
    """更新用户状态模型"""
    userId: int
    status: str = Field(..., pattern="[01]")


class UserPasswordReset(BaseModel):
    """重置用户密码模型"""
    userId: int
    password: str = Field(..., min_length=6, max_length=20)


class UserRoleAssign(BaseModel):
    """分配用户角色模型"""
    userId: int
    roleIds: List[int]


class UserResponse(UserBase):
    """用户响应模型"""
    userId: int
    status: str
    createTime: str
    updateTime: Optional[str] = None
    loginIp: Optional[str] = None
    loginDate: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应模型"""
    list: List[UserResponse]
    total: int
    pageNum: int
    pageSize: int
