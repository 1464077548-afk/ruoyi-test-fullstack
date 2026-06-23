from typing import Dict, Any, List, Optional
from api.clients.base_client import BaseClient


class PostClient(BaseClient):
    """岗位管理API客户端"""

    def get_post_list(self, page: int = 1, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """获取岗位列表"""
        endpoint = "/system/post/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)

    def get_post_by_id(self, post_id: int) -> Dict[str, Any]:
        """根据ID获取岗位"""
        endpoint = f"/system/post/{post_id}"
        return self.get(endpoint)

    def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建岗位"""
        endpoint = "/system/post"
        return self.post(endpoint, post_data)

    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新岗位"""
        endpoint = "/system/post"
        post_data["postId"] = post_id
        return self.put(endpoint, json=post_data)

    def delete_post(self, post_id: int) -> Dict[str, Any]:
        """删除岗位"""
        endpoint = f"/system/post/{post_id}"
        return self.delete(endpoint)

    def batch_delete_posts(self, post_ids: List[int]) -> Dict[str, Any]:
        """批量删除岗位"""
        endpoint = f"/system/post/{','.join(map(str, post_ids))}"
        return self.delete(endpoint)

    def change_status(self, post_id: int, status: str) -> Dict[str, Any]:
        """修改岗位状态"""
        endpoint = "/system/post/changeStatus"
        data = {
            "postId": post_id,
            "status": status
        }
        return self.put(endpoint, data)

    def export_posts(self) -> bytes:
        """导出岗位数据"""
        endpoint = "/system/post/export"
        return self.get(endpoint, response_type="bytes")

    def query_post_by_name(self, post_name: str) -> Dict[str, Any]:
        """根据岗位名称查询"""
        endpoint = "/system/post/list"
        params = {
            "postName": post_name,
            "pageNum": 1,
            "pageSize": 10
        }
        return self.get(endpoint, params)

    def query_post_by_code(self, post_code: str) -> Dict[str, Any]:
        """根据岗位编码查询"""
        endpoint = "/system/post/list"
        params = {
            "postCode": post_code,
            "pageNum": 1,
            "pageSize": 10
        }
        return self.get(endpoint, params)

    def validate_post_name(self, post_name: str) -> Dict[str, Any]:
        """验证岗位名称是否唯一"""
        endpoint = "/system/post/checkPostNameUnique"
        params = {"postName": post_name}
        return self.get(endpoint, params)

    def validate_post_code(self, post_code: str) -> Dict[str, Any]:
        """验证岗位编码是否唯一"""
        endpoint = "/system/post/checkPostCodeUnique"
        params = {"postCode": post_code}
        return self.get(endpoint, params)
