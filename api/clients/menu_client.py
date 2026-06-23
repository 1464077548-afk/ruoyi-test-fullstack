from typing import Dict, Any, List
from api.clients.base_client import BaseClient


class MenuClient(BaseClient):
    """菜单API客户端"""
    
    def get_menu_list(self, **kwargs) -> Dict[str, Any]:
        """获取菜单列表"""
        endpoint = "/system/menu/list"
        return self.get(endpoint, kwargs)
    
    def get_menu_by_id(self, menu_id: int) -> Dict[str, Any]:
        """根据ID获取菜单"""
        endpoint = f"/system/menu/{menu_id}"
        return self.get(endpoint)
    
    def create_menu(self, menu_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建菜单"""
        endpoint = "/system/menu"
        return self.post(endpoint, menu_data)
    
    def update_menu(self, menu_id: int, menu_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新菜单"""
        endpoint = "/system/menu"
        return self.put(endpoint, menu_data)
    
    def delete_menu(self, menu_id: int) -> Dict[str, Any]:
        """删除菜单"""
        endpoint = f"/system/menu/{menu_id}"
        return self.delete(endpoint)
    
    def get_menu_tree(self) -> Dict[str, Any]:
        """获取菜单树"""
        endpoint = "/system/menu/treeselect"
        return self.get(endpoint)
    
    def get_role_menu_tree(self, role_id: int) -> Dict[str, Any]:
        """获取角色菜单树"""
        endpoint = f"/system/menu/roleMenuTreeselect/{role_id}"
        return self.get(endpoint)
    
    def get_user_menu_list(self) -> Dict[str, Any]:
        """获取用户菜单列表"""
        endpoint = "/getRouters"
        return self.get(endpoint)
