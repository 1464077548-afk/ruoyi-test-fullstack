from typing import Dict, Any, List
from api.clients.base_client import BaseClient


class ConfigClient(BaseClient):
    """配置管理API客户端"""
    
    def get_config_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取参数列表"""
        endpoint = "/system/config/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_config(self, config_id: int) -> Dict[str, Any]:
        """获取参数详情"""
        endpoint = f"/system/config/{config_id}"
        return self.get(endpoint)
    
    def get_config_by_key(self, config_key: str) -> Dict[str, Any]:
        """根据参数键名获取参数值"""
        endpoint = f"/system/config/configKey/{config_key}"
        return self.get(endpoint)
    
    def create_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """新增参数配置"""
        endpoint = "/system/config"
        return self.post(endpoint, config_data)
    
    def update_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """修改参数配置"""
        endpoint = "/system/config"
        return self.put(endpoint, json=config_data)
    
    def delete_config(self, config_id: int) -> Dict[str, Any]:
        """删除参数配置"""
        endpoint = f"/system/config/{config_id}"
        return self.delete(endpoint)
    
    def refresh_config_cache(self) -> Dict[str, Any]:
        """刷新参数缓存"""
        endpoint = "/system/config/refreshCache"
        return self.delete(endpoint)