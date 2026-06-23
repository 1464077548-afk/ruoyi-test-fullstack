from typing import Optional, List
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """角色基础模型"""
    roleName: str = Field(..., min_length=1, max_length=50)
    roleKey: str = Field(..., min_length=1, max_length=50)
    roleSort: int = Field(..., ge=1, le=999)
    dataScope: Optional[str] = Field(None, pattern="[1234]")
    menuCheckStrictly: Optional[bool] = False
    deptCheckStrictly: Optional[bool] = False
    remark: Optional[str] = None


class RoleCreate(RoleBase):
    """创建角色模型"""
    status: str = Field(..., pattern="[01]")


class RoleUpdate(RoleBase):
    """更新角色模型"""
    roleId: int
    status: str = Field(..., pattern="[01]")


class RoleStatusUpdate(BaseModel):
    """更新角色状态模型"""
    roleId: int
    status: str = Field(..., pattern="[01]")


class RoleMenuAssign(BaseModel):
    """分配角色菜单权限模型"""
    roleId: int
    menuIds: List[int]


class RoleDeptAssign(BaseModel):
    """分配角色部门权限模型"""
    roleId: int
    deptIds: List[int]


class RoleResponse(RoleBase):
    """角色响应模型"""
    roleId: int
    status: str
    createTime: str
    updateTime: Optional[str] = None
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """角色列表响应模型"""
    list: List[RoleResponse]
    total: int
    pageNum: int
    pageSize: int
