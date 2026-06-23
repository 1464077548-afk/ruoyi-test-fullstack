from typing import Dict, Any, List
from api.clients.base_client import BaseClient


class DictClient(BaseClient):
    """字典API客户端"""
    
    def get_dict_type_list(self, page: int = 1, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """获取字典类型列表"""
        endpoint = "/system/dict/type/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_dict_type(self, dict_id: int) -> Dict[str, Any]:
        """获取字典类型详情"""
        endpoint = f"/system/dict/type/{dict_id}"
        return self.get(endpoint)
    
    def create_dict_type(self, dict_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建字典类型"""
        endpoint = "/system/dict/type"
        return self.post(endpoint, dict_data)
    
    def update_dict_type(self, dict_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新字典类型"""
        endpoint = "/system/dict/type"
        return self.put(endpoint, json=dict_data)
    
    def delete_dict_type(self, dict_id: int) -> Dict[str, Any]:
        """删除字典类型"""
        endpoint = f"/system/dict/type/{dict_id}"
        return self.delete(endpoint)
    
    def refresh_dict_cache(self) -> Dict[str, Any]:
        """刷新字典缓存"""
        endpoint = "/system/dict/type/refreshCache"
        return self.delete(endpoint)
    
    def get_dict_type_options(self) -> Dict[str, Any]:
        """获取字典选择框列表"""
        endpoint = "/system/dict/type/optionselect"
        return self.get(endpoint)
    
    def get_dict_data_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取字典数据列表"""
        endpoint = "/system/dict/data/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_dict_data(self, dict_code: int) -> Dict[str, Any]:
        """获取字典数据详情"""
        endpoint = f"/system/dict/data/{dict_code}"
        return self.get(endpoint)
    
    def get_dicts_by_type(self, dict_type: str) -> Dict[str, Any]:
        """根据字典类型获取字典数据"""
        endpoint = f"/system/dict/data/type/{dict_type}"
        return self.get(endpoint)
    
    def create_dict_data(self, dict_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建字典数据"""
        endpoint = "/system/dict/data"
        return self.post(endpoint, dict_data)
    
    def update_dict_data(self, dict_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新字典数据"""
        endpoint = "/system/dict/data"
        return self.put(endpoint, json=dict_data)
    
    def delete_dict_data(self, dict_code: int) -> Dict[str, Any]:
        """删除字典数据"""
        endpoint = f"/system/dict/data/{dict_code}"
        return self.delete(endpoint)