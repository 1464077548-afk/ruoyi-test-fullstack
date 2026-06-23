from pydantic import BaseModel, Field
from typing import Any, Optional, Generic, TypeVar, List

T = TypeVar('T')


class BaseResponse(BaseModel):
    """基础响应模型"""
    code: Optional[int] = Field(None, description="响应状态码")
    msg: Optional[str] = Field(None, description="响应消息")


class DataResponse(BaseResponse, Generic[T]):
    """带数据的响应模型"""
    data: Optional[T] = Field(None, description="响应数据")


class PaginatedData(BaseModel, Generic[T]):
    """分页数据模型"""
    total: Optional[int] = Field(None, description="总记录数")
    rows: Optional[List[T]] = Field(None, description="数据列表")


class PaginatedResponse(BaseResponse):
    """分页响应模型"""
    data: Optional[PaginatedData] = Field(None, description="分页数据")


class LoginResponse(BaseResponse):
    """登录响应模型"""
    token: Optional[str] = Field(None, description="认证令牌")


class CaptchaResponse(BaseResponse):
    """验证码响应模型"""
    img: Optional[str] = Field(None, description="验证码图片Base64编码")
    uuid: Optional[str] = Field(None, description="验证码UUID")
