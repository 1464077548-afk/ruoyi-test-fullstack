"""UI与API数据一致性测试"""
from this import s
import pytest
from ui.pages.modules.login_page import LoginPage
from ui.pages.modules.user_page import UserPage
from api.clients.user_client import UserClient
from config.settings import Settings


class TestUiApiSync:
    """UI与API数据一致性测试类"""
    @pytest.mark.integration
    @pytest.mark.p0
    @pytest.mark.serial  # 串行执行，避免并行执行时数据竞争
    def test_user_data_consistency(self, user_biz, common_biz, user_client):
        """P0-用户数据一致性"""
        try:
            # 1.导航到用户管理页面
            common_biz.switch_menu("系统管理/用户管理")
            
            # 2. 重置搜索条件，确保显示所有用户
            user_biz.reset_search()
            
            # 3. UI获取所有用户（处理分页）
            ui_user_list = user_biz.get_user_list(get_all=True)
            print(f"UI用户列表（共{len(ui_user_list)}个）: {ui_user_list}")
            
            # 4. API获取所有用户（处理分页）
            api_user_list = []
            page_num = 1
            page_size = 100
            while True:
                try:
                    api_response = user_client.get_user_list(page=page_num, limit=page_size)
                    rows = api_response.get("rows", [])
                    if not rows:
                        break
                    api_user_list.extend([user.get("userName") for user in rows])
                    if len(rows) < page_size:
                        break
                    page_num += 1
                except Exception as e:
                    print(f"API请求失败，跳过此页: {e}")
                    break
            print(f"API用户列表（共{len(api_user_list)}个）: {api_user_list}")
            
            # 5. 验证数据一致性（UI用户应在API用户列表中）
            for ui_user in ui_user_list:
                assert ui_user in api_user_list, f"UI用户 {ui_user} 不在API用户列表中"
        except Exception as e:
            print(f"测试执行失败: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    @pytest.mark.integration
    @pytest.mark.p0
    def test_user_list_consistency(self, user_biz, common_biz, user_client):
        """P0-用户列表数据一致性"""
        # 1. 导航到用户管理页面并重置搜索条件
        common_biz.switch_menu("系统管理/用户管理")
        user_biz.reset_search()
        
        # 2. 通过 UI 获取所有用户（处理分页）
        ui_users = user_biz.get_user_list(get_all=True)
        print(f"UI用户数量: {len(ui_users)}")
        
        # 3. 通过 API 获取所有用户（处理分页）
        api_users = {}
        page_num = 1
        page_size = 100
        while True:
            api_result = user_client.get_user_list(page=page_num, limit=page_size)
            rows = api_result.get("rows", [])
            if not rows:
                break
            for u in rows:
                api_users[u['userName']] = u
            if len(rows) < page_size:
                break
            page_num += 1
        print(f"API用户数量: {len(api_users)}")
        
        # 4. 验证数据一致
        assert len(api_users) == len(ui_users), f"用户数量不一致: API有{len(api_users)}个，UI有{len(ui_users)}个"
    
    @pytest.mark.integration
    @pytest.mark.p0
    def test_user_create_sync(self, user_biz, user_client, test_user_data):
        """P0-用户创建数据同步"""
        # 1. 通过 UI 创建用户
        result = user_biz.add_user(test_user_data)
        print(f"UI创建用户结果: {result}")
        
        # 2. 通过 API 验证用户存在
        api_result = user_client.get_user_list(userName=test_user_data['userName'])
        print(f"API响应: {api_result}")
        
        # 3. 验证用户创建成功
        assert api_result['total'] >= 1, f"用户创建失败，API未找到用户: {test_user_data['userName']}"
        assert api_result['rows'][0]['userName'] == test_user_data['userName'], f"API用户 {api_result['rows'][0]['userName']} 与UI用户 {test_user_data['userName']} 不一致"
        #删除用户
        result = user_biz.delete_user(test_user_data['userName'])
        print(f"UI删除用户结果: {result}")
        assert "成功" in result, "用户删除失败"
        
    @pytest.mark.integration
    @pytest.mark.p1
    def test_user_delete_sync(self, user_biz, common_biz, user_client, test_user_data):
        """P1-用户删除数据同步"""
        # 1. 通过 API 创建用户
        create_result = user_client.create_user(test_user_data)
        print(f"API创建用户结果: {create_result}")
        #2.查询获取用户id
        users_list = user_client.get_user_list(userName=test_user_data['userName'])
        print(f"API查询用户结果: {users_list}")
        user_id = users_list['rows'][0]['userId']
        assert user_id is not None, "用户ID为空"
        
        # 3. 通过 UI 删除用户
        common_biz.switch_menu("系统管理/用户管理")
        result = user_biz.delete_user(test_user_data['userName'])
        print(f"UI删除用户结果: {result}")
        assert "成功" in result, "用户删除失败"
        
        # 4. 通过 API 验证用户已删除（系统使用软删除）
        api_result = user_client.get_user_by_id(user_id)
        print(f"API查询用户详情结果: {api_result}")
        user_data = api_result.get('data', {})
        del_flag = user_data.get('delFlag', '0')
        assert del_flag == '2', f"用户 {user_id} 未被软删除，当前delFlag={del_flag}"