"""L1: 用户接口单接口测试"""
import pytest
from api.clients.user_client import UserClient
from common.utils.data_factory import DataFactory


class TestUserApi:
    """用户API测试类"""
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_user_list(self, user_client):
        """P0-获取用户列表"""
        response = user_client.get_user_list()
        # print(f"获取用户列表响应: {response}")
        assert response.get("code") == 200
        assert response.get("total") > 0
        # 检查列表中是否有用户的userName为admin
        user_names = [user.get("userName") for user in response.get("rows", [])]
        assert "admin" in user_names

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_user_list_with_filter(self, user_client):
        """P0-带条件查询用户列表"""
        response = user_client.get_user_list(userName="admin")
        # print(f"获取用户列表响应: {response}")
        assert response.get("code") == 200
        assert response.get("total") == 1
        assert "admin"==response.get("rows")[0].get("userName")
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_create_user(self, user_client, test_user_data):
        """P0-创建用户成功"""
        response = user_client.create_user(test_user_data)
        print(f"创建用户响应: {response}")

        response = user_client.get_user_list(userName=test_user_data.get("userName"))   
        assert response.get("rows")[0].get("nickName") == test_user_data.get("nickName")
        # 清理
        user_id = response.get("rows")[0].get("userId") 
        user_client.delete_user(user_id)

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_user_duplicate(self, user_client, test_user_data):
        """P1-创建重复用户"""   
        # 先创建一个
        user_client.create_user(test_user_data)
        
        # 再创建同名用户
        result = user_client.create_user(test_user_data)
        print(f"创建重复用户响应: {result}")
        
        assert result['code'] == 500
        assert '已存在' in result.get('msg', '')

        response = user_client.get_user_list(userName=test_user_data.get("userName"))   
        assert response.get("rows")[0].get("nickName") == test_user_data.get("nickName")
        # 清理
        user_id = response.get("rows")[0].get("userId") 
        user_client.delete_user(user_id)

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_update_user(self, user_client, created_user, test_user_data):
        """P0-更新用户成功"""
        user_id = created_user
        # 使用更短的昵称，避免超过30个字符限制
        updated_data = {
            "userName": test_user_data.get('userName'),
            "nickName": f"测试用户_更新",
            "email": f"updated_{test_user_data.get('email')}"
        }
        response = user_client.update_user(user_id, updated_data)
        # 检查响应是否为BaseResponse对象
        if hasattr(response, 'code'):
            assert response.code == 200
        else:
            assert response.get("code") == 200
        
        # 检查更新后的用户信息
        user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
        assert user_list_response.get("code") == 200
        assert user_list_response.get("total") == 1
        assert user_list_response.get("rows")[0].get("nickName") == updated_data.get("nickName")
        # 清理
        user_id = user_list_response.get("rows")[0].get("userId") 
        user_client.delete_user(user_id)
        
        
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_delete_user(self, user_client, test_user_data):
        """P0-删除用户成功"""
        # 创建用户
        create_response = user_client.create_user(test_user_data)
        assert create_response.get("code") == 200
        
        # 通过用户名查询获取用户ID
        user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
        assert user_list_response.get("code") == 200
        assert len(user_list_response.get("rows", [])) > 0
        user_id = user_list_response.get("rows")[0].get("userId")
        assert user_id
        
        # 删除用户
        delete_response = user_client.delete_user(user_id)
        assert delete_response.get("code") == 200

        # 检查用户是否已被删除
        user_list_response = user_client.get_user_list(userName=test_user_data.get("userName"))
        print(f"🔍删除用户后查询用户列表响应: {user_list_response}")
        assert user_list_response.get("code") == 200
        assert user_list_response.get("total") == 0
        
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_user_by_id(self, user_client, created_user):
        """P0-根据ID获取用户成功"""
        user_id = created_user
        response = user_client.get_user_by_id(user_id)
        assert response.get("code") == 200
        assert response.get("data", {}).get("userId") == user_id
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_reset_user_password(self, user_client, created_user):
        """P1-重置用户密码"""
        user_id = created_user
        result = user_client.reset_password(user_id, 'New@123456')
        print(f"重置用户密码响应: {result}")
        assert result.get("code") == 200

        #TODO: 验证重置密码后，用户是否可以登录
   
        
    
    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_change_user_status(self, user_client, created_user):
        """P1-修改用户状态"""
        user_id = created_user
        result = user_client.change_status(user_id, '1')  # 禁用
        print(f"修改用户状态响应: {result}")
        assert result.get("code") == 200

