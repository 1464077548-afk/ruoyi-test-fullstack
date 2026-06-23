import requests
import json
from typing import Type,Dict, Any, Optional, Union
from config.settings import Settings
from common.logger import Logger
from pydantic import BaseModel
from common.utils.retry_helper import (
    safe_request,
    retry_on_requests_error,
    RetryConfig,
)


class BaseClient:
    """基础API客户端（带网络错误重试机制）"""
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        """初始化客户端
        
        Args:
            base_url: API基础URL
            token: 认证令牌（可选）
        """
        print(f"=============== BaseClient __init__ 初始化=================")
        self.settings = Settings()
        self.base_url = self.settings.API_BASE_URL
        self.logger = Logger(__name__)
        self.session = requests.Session()
        self.token = token
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        if token:
            self.set_token(token)
        
        self.max_retries = getattr(self.settings, 'API_MAX_RETRIES', RetryConfig.DEFAULT_MAX_RETRIES)
        self.retry_delay = getattr(self.settings, 'API_RETRY_DELAY', RetryConfig.DEFAULT_DELAY)
 
    
    def set_token(self, token: str):
        """设置认证令牌"""
        self.token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def remove_token(self):
        """移除认证令牌"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """发送GET请求（带网络错误重试）"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"GET {url} params={params}")
        
        try:
            response = safe_request(
                self.session,
                'GET',
                url,
                max_retries=self.max_retries,
                delay=self.retry_delay,
                params=params,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET请求失败: {e}")
            raise
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """发送POST请求（带网络错误重试）"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"POST {url} data={data}")
        
        try:
            response = safe_request(
                self.session,
                'POST',
                url,
                max_retries=self.max_retries,
                delay=self.retry_delay,
                json=data,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POST请求失败: {e}")
            raise
    
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """发送PUT请求（带网络错误重试）"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"PUT {url} json={json}")
        
        try:
            response = safe_request(
                self.session,
                'PUT',
                url,
                max_retries=self.max_retries,
                delay=self.retry_delay,
                json=json,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PUT请求失败: {e}")
            raise
    
    def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """发送DELETE请求（带网络错误重试）"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"DELETE {url} data={data} params={params}")
        
        try:
            response = safe_request(
                self.session,
                'DELETE',
                url,
                max_retries=self.max_retries,
                delay=self.retry_delay,
                json=data,
                params=params,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"DELETE请求失败: {e}")
            raise
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """发送PATCH请求（带网络错误重试）"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"PATCH {url} data={data}")
        
        try:
            response = safe_request(
                self.session,
                'PATCH',
                url,
                max_retries=self.max_retries,
                delay=self.retry_delay,
                json=data,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PATCH请求失败: {e}")
            raise
    
    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """通用请求方法（带网络错误重试）"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"{method.upper()} {url}")
        
        try:
            response = safe_request(
                self.session,
                method,
                url,
                max_retries=self.max_retries,
                delay=self.retry_delay,
                **kwargs
            )
            # 记录响应
            self.logger.debug(f"Response: {response.status_code} - {response.text[:200]}")
            # 捕获 401 错误并抛出更详细的异常
            if response.status_code == 401:
                self.logger.error(f"[Auth Failed] {method} {url} | Response: {response.text}")
                import traceback
                self.logger.error(traceback.format_stack())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{method.upper()}请求失败: {e}")
            raise

    def validate_response(self, response: Union[Dict[str, Any], requests.Response], model: Type[BaseModel]) -> BaseModel:
        """使用Pydantic模型校验响应
        
        Args:
            response: API响应
            model: Pydantic模型类
            
        Returns:
            校验后的模型实例
        """
        if isinstance(response, requests.Response):
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                raise ValueError(f"响应不是有效的JSON格式: {response.text}")
        else:
            response_data = response
        
        try:
            # 尝试使用指定的模型进行校验
            return model(**response_data)
        except Exception as e:
            # 如果校验失败，尝试使用BaseResponse模型
            from api.models.base import BaseResponse
            try:
                return BaseResponse(**response_data)
            except Exception:
                # 如果BaseResponse也校验失败，抛出原始错误
                raise ValueError(f"响应校验失败: {e}")