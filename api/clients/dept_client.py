from typing import Dict, Any, List
from api.clients.base_client import BaseClient


class DeptClient(BaseClient):
    """部门API客户端"""
    
    def get_dept_list(self, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """获取部门列表"""
        endpoint = "/system/dept/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_dept_list_exclude_child(self, dept_id: int) -> Dict[str, Any]:
        """获取部门列表（排除节点）"""
        endpoint = f"/system/dept/list/exclude/{dept_id}"
        return self.get(endpoint)
    
    def get_dept(self, dept_id: int) -> Dict[str, Any]:
        """获取部门详情"""
        endpoint = f"/system/dept/{dept_id}"
        return self.get(endpoint)
    
    def create_dept(self, dept_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建部门"""
        endpoint = "/system/dept"
        return self.post(endpoint, dept_data)
    
    def update_dept(self, dept_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新部门"""
        endpoint = "/system/dept"
        return self.put(endpoint, json=dept_data)
    
    def delete_dept(self, dept_id: int) -> Dict[str, Any]:
        """删除部门"""
        endpoint = f"/system/dept/{dept_id}"
        return self.delete(endpoint)