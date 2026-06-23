from typing import Dict, Any, List
from api.clients.base_client import BaseClient
from api.models.base import BaseResponse, PaginatedResponse, DataResponse
from api.models.user import UserResponse, UserListResponse, UserProfileResponse


class UserClient(BaseClient):
    """用户API客户端"""
    
    def get_user_list(self, page: int = 1, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """获取用户列表"""
        endpoint = "/system/user/list"
        params = {
            "pageNum": page,
            "pageSize": limit,
            **kwargs
        }
        return self.get(endpoint, params)
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """根据ID获取用户"""
        endpoint = f"/system/user/{user_id}"
        return self.get(endpoint)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        endpoint = "/system/user"
        return self.post(endpoint, user_data)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户"""
        endpoint = "/system/user"
        # 添加userId到请求体
        user_data["userId"] = user_id
        response = self.put(endpoint, json=user_data)
        return self.validate_response(response, BaseResponse)
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """删除用户"""
        endpoint = f"/system/user/{user_id}"
        return self.delete(endpoint)
        # return self.validate_response(response, BaseResponse)
    
    def batch_delete_users(self, user_ids: List[int]) -> Dict[str, Any]:
        """批量删除用户"""
        endpoint = f"/system/user/{','.join(map(str, user_ids))}"
        return self.delete(endpoint)
    
    def change_status(self, user_id: int, status: str) -> Dict[str, Any]:
        """修改用户状态"""
        endpoint = "/system/user/changeStatus"
        data = {
            "userId": user_id,
            "status": status
        }
        return self.put(endpoint, json=data)
    
    def reset_password(self, user_id: int, password: str) -> Dict[str, Any]:
        """重置用户密码"""
        endpoint = "/system/user/resetPwd"
        data = {
            "userId": user_id,
            "password": password
        }
        return self.put(endpoint, json=data)
    
    def assign_roles(self, user_id: int, role_ids: List[int]) -> Dict[str, Any]:
        """分配用户角色"""
        endpoint = "/system/user/role"
        data = {
            "userId": user_id,
            "roleIds": role_ids
        }
        return self.post(endpoint, data)

    def get_user_profile(self):
        """获取用户个人信息"""
        url = f"/system/user/profile"
        response = self.get(url)
        return self.validate_response(response, UserProfileResponse)

    def update_user_profile(self, profile_data):
        """更新用户个人信息"""
        url = f"/system/user/profile"
        response = self.put(url, json=profile_data)
        return self.validate_response(response, BaseResponse)

    def reset_profile_password(self, old_password, new_password):
        """重置用户个人密码"""
        url = f"/system/user/profile/updatePwd"
        response = self.put(url, json={"oldPassword": old_password, "newPassword": new_password})
        return self.validate_response(response, BaseResponse)

    def upload_profile_avatar(self, avatar_file):
        """上传用户个人头像"""
        url = f"/system/user/profile/avatar"
        response = self.post(url, files={"avatar": avatar_file})
        return self.validate_response(response, BaseResponse)

    
    def get_auth_user_role(self, userId):
        """获取当前认证用户的角色"""
        url = f"/system/user/authRole/{userId}"
        response = self.get(url)
        return self.validate_response(response, DataResponse)

    def add_auth_role(self, userId, roleIds):
        """添加认证用户角色"""
        url = f"/system/user/authRole"
        response = self.put(url, json={"userId": userId, "roleIds": roleIds})
        return self.validate_response(response, BaseResponse)
    
    def get_dept_tree(self):
        """获取部门树"""
        url = f"/system/user/deptTree"
        response = self.get(url)
        return self.validate_response(response, DataResponse)
