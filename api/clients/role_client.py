from typing import Dict, Any, List
from api.clients.base_client import BaseClient


class RoleClient(BaseClient):
    """角色API客户端"""
    
    def get_role_list(self, page: int = 1, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """获取角色列表"""
        endpoint = "/system/role/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_role_by_id(self, role_id: int) -> Dict[str, Any]:
        """根据ID获取角色"""
        endpoint = f"/system/role/{role_id}"
        return self.get(endpoint)
    
    def create_role(self, role_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建角色"""
        endpoint = "/system/role"
        # 添加默认的 menuIds 字段，避免 "Cannot read the array length because "<local4>" is null" 错误
        if "menuIds" not in role_data:
            role_data["menuIds"] = []
        return self.post(endpoint, role_data)
    
    def update_role(self, role_id: int, role_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新角色"""
        endpoint = "/system/role"
        # 添加 roleId 到请求体
        role_data["roleId"] = role_id
        # 添加默认的 menuIds 字段
        if "menuIds" not in role_data:
            role_data["menuIds"] = []
        return self.put(endpoint, json=role_data)
    
    def delete_role(self, role_id: int) -> Dict[str, Any]:
        """删除角色"""
        endpoint = f"/system/role/{role_id}"
        return self.delete(endpoint)
    
    def batch_delete_roles(self, role_ids: List[int]) -> Dict[str, Any]:
        """批量删除角色"""
        endpoint = f"/system/role/{','.join(map(str, role_ids))}"
        return self.delete(endpoint)

    def change_status(self, role_id: int, status: str) -> Dict[str, Any]:
        """修改角色状态"""
        endpoint = "/system/role/changeStatus"
        data = {
            "roleId": role_id,
            "status": status
        }
        return self.put(endpoint, data)

    def get_role_menus(self, role_id: int) -> Dict[str, Any]:
        """获取角色菜单权限"""
        endpoint = f"/system/menu/roleMenuTreeselect/{role_id}"
        return self.get(endpoint)

    def assign_menus(self, role_id: int, menu_ids: List[int]) -> Dict[str, Any]:
        """分配角色菜单权限"""
        # First get the role details
        role_detail = self.get_role_by_id(role_id)
        if role_detail.get("code") != 200:
            return role_detail
        
        # Update the role with menuIds
        role_data = role_detail.get("data", {})
        role_data["menuIds"] = menu_ids
        
        endpoint = "/system/role"
        return self.put(endpoint, json=role_data)
    
    def get_role_depts(self, role_id: int) -> Dict[str, Any]:
        """获取角色部门权限"""
        endpoint = f"/system/role/dept/{role_id}"
        return self.get(endpoint)
    
    def assign_depts(self, role_id: int, dept_ids: List[int]) -> Dict[str, Any]:
        """分配角色部门权限"""
        endpoint = "/system/role/dept"
        data = {
            "roleId": role_id,
            "deptIds": dept_ids
        }
        return self.put(endpoint, data)
    
    def assign_users(self, role_id: int, user_ids: List[int]) -> Dict[str, Any]:
        """分配角色用户"""
        endpoint = "/system/role/authUser/selectAll"
        data = {
            "roleId": role_id,
            "userIds": user_ids
        }
        return self.put(endpoint, data)
