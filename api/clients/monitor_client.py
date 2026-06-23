from typing import Dict, Any
from api.clients.base_client import BaseClient


class MonitorClient(BaseClient):
    """监控API客户端"""
    
    def get_server_info(self) -> Dict[str, Any]:
        """获取服务器信息"""
        endpoint = "/monitor/server"
        return self.get(endpoint)
    
    def get_jvm_info(self) -> Dict[str, Any]:
        """获取JVM信息"""
        endpoint = "/monitor/jvm"
        return self.get(endpoint)
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        endpoint = "/monitor/cache"
        return self.get(endpoint)
    
    def clear_cache(self) -> Dict[str, Any]:
        """清理缓存"""
        endpoint = "/monitor/cache/clearCacheAll"
        return self.delete(endpoint)
    
    def get_druid_info(self) -> Dict[str, Any]:
        """获取Druid监控信息"""
        endpoint = "/monitor/druid"
        return self.get(endpoint)
    
    def get_redis_info(self) -> Dict[str, Any]:
        """获取Redis监控信息"""
        endpoint = "/monitor/redis"
        return self.get(endpoint)
    
    def get_log_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取日志列表"""
        endpoint = "/monitor/log/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_oper_log_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取操作日志列表"""
        endpoint = "/monitor/operlog/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
