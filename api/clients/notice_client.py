from typing import Dict, Any, List
from api.clients.base_client import BaseClient


class NoticeClient(BaseClient):
    """通知管理API客户端"""
    
    def get_notice_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取公告列表"""
        endpoint = "/system/notice/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_notice(self, notice_id: int) -> Dict[str, Any]:
        """获取公告详情"""
        endpoint = f"/system/notice/{notice_id}"
        return self.get(endpoint)
    
    def create_notice(self, notice_data: Dict[str, Any]) -> Dict[str, Any]:
        """新增公告"""
        endpoint = "/system/notice"
        return self.post(endpoint, notice_data)
    
    def update_notice(self, notice_data: Dict[str, Any]) -> Dict[str, Any]:
        """修改公告"""
        endpoint = "/system/notice"
        return self.put(endpoint, json=notice_data)
    
    def delete_notice(self, notice_id: int) -> Dict[str, Any]:
        """删除公告"""
        endpoint = f"/system/notice/{notice_id}"
        return self.delete(endpoint)