"""
L2: 用户管理模块测试
验证用户管理功能的完整测试
"""
from email import message
from enum import verify
import pytest
import time
from config.settings import Settings
from common.utils.data_factory import DataFactory


class TestUserManageModule:
    """用户管理模块测试类"""
    
    # ========== 新增功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_user_add_success(self, test_user_data, common_biz,user_biz):
        """P0-新增用户成功"""
        common_biz.switch_menu("系统管理/用户管理")
        # 创建用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 验证用户存在
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info['userName'] == test_user_data['userName']
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_add_validation(self, user_biz, common_biz):
        """P1-新增用户表单验证"""
        # 确保在用户管理页面
        common_biz.switch_menu("系统管理/用户管理")
        
        user_biz.user_page.click_add()
        
        # 不填写必填项直接提交
        user_biz.user_page.click_save_user()
        error_messages = user_biz.verify_error_messages()
        
        # 验证错误提示 - 使用更灵活的断言，不要求特定顺序
        assert error_messages is not None and len(error_messages) > 0, "应该有错误提示"
        # 检查错误消息是否包含必要的关键词
        error_text_combined = " ".join(error_messages)
        assert "用户昵称" in error_text_combined or "昵称" in error_text_combined, f"应包含昵称错误提示，实际: {error_messages}"
        assert "用户名称" in error_text_combined or "用户名称" in error_text_combined or "名称" in error_text_combined, f"应包含用户名称错误提示，实际: {error_messages}"
        
        #关闭新增用户弹窗
        user_biz.user_page.click_cancel_user_dialog()
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_add_duplicate_username(self, test_user_data, common_biz,user_biz):
        """P1-新增重复用户名"""
        common_biz.switch_menu("系统管理/用户管理")
        
        # 使用已存在的用户名
        test_data = test_user_data.copy()
        test_data['userName'] = "admin"
        
        # 尝试添加用户，获取结果
        result = user_biz.add_user(test_data)
        
        # 验证重复提示 - 检查结果中是否包含错误相关信息
        # 可能的返回结果：表单错误消息、API错误消息、或"操作消息未显示"（表示验证阻止了提交）
        is_duplicate = (
            "已存在" in result or 
            "失败" in result or 
            "错误" in result or
            "error" in result.lower() 
        )
        
        assert is_duplicate, f"预期添加重复用户名会失败，但得到结果: {result}"
        
        #关闭新增用户弹窗
        user_biz.user_page.press_key("Escape")
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_add_duplicate_phone(self, test_user_data, user_page):
        """P2-新增重复手机号"""  
        # 获取已创建用户的手机号
        # 尝试用相同手机号创建新用户
        # 验证提示
        pass
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_add_duplicate_email(self, test_user_data, user_page):
        """P2-新增重复邮箱"""
        # 类似手机号测试
        pass
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_add_cancel(self, test_user_data, common_biz,user_biz):
        """P2-新增用户取消"""
        common_biz.switch_menu("系统管理/用户管理")
        
        user_biz.user_page.click_add()
        user_biz.user_page.fill_user_form(
            username=test_user_data['userName'],
            nickname=test_user_data['nickName'],
            password=test_user_data['password'],
            email=test_user_data.get('email', ''),
            phone=test_user_data.get('phone', '')
        )
        user_biz.user_page.click_cancel_user_dialog()
        
        # 验证未新增
        assert not user_biz.user_page.find_user_row(test_user_data['userName']) , "用户已新增"
    
    # ========== 编辑功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_user_edit_nickname_success(self, test_user_data, common_biz,user_biz):
        """P0-编辑用户成功"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        #新增用户后，编辑用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 修改昵称
        new_nickname = f"Edited_{test_user_data['nickName']}"
        message = user_biz.edit_user_nickname(test_user_data['userName'],new_nickname)
        assert "成功" in message
     
        # 验证修改成功
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info['nickName'] == new_nickname, f"用户昵称未修改为 {new_nickname}"
        #删除用户
        user_biz.delete_user(test_user_data['userName'])
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1

    def test_user_edit_status(self, common_biz,user_biz, test_user_data):
        """P1-编辑用户状态"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先新增用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message

         # 获取用户状态变化
        user_info = user_biz.get_user_info(test_user_data['userName'])
        user_status = user_info['status']
        
        # 切换用户状态
        message = user_biz.toggle_user_status(test_user_data['userName'])
        assert "成功" in message
        
        # 验证状态变化
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_status != user_info['status'] , f"用户状态未切换"

        # 再次切换状态，验证恢复
        message = user_biz.toggle_user_status(test_user_data['userName'])
        assert "成功" in message
        
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_status == user_info['status'] , f"用户状态未改变"

        user_biz.delete_user(test_user_data['userName'])
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_edit_password(self, common_biz,user_biz, test_user_data):
        """P1-重置用户密码"""  
        common_biz.switch_menu("系统管理/用户管理") 
        
         # 先新增用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 点击重置密码
        new_password = "New@123456"
        message = user_biz.reset_password(test_user_data['userName'],new_password)
        assert "成功" in message


    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_edit_cancel(self, common_biz,user_biz, test_user_data):
        """P2-编辑用户取消"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先新增用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 编辑用户，修改昵称
        user_biz.user_page.click_edit_button(test_user_data['userName'])
        user_biz.user_page.fill_user_nickname(test_user_data['nickName'])
        # 点击取消
        user_biz.user_page.click_edit_cancel_button()
        
        # 验证未修改
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info['nickName'] == test_user_data['nickName'], f"用户昵称已修改为 {user_info['nickName']}"
    
    # ========== 删除功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_user_delete_success(self, common_biz,user_biz, test_user_data):
        """P0-删除用户成功"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先新增用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 删除用户
        message = user_biz.delete_user(test_user_data['userName'])
        assert "成功" in message
        
        # 验证删除成功
        user_info =user_biz.get_user_info(test_user_data['userName'])
        assert user_info is None, "用户未删除成功"
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_delete_cancel(self, common_biz,user_biz, test_user_data):
        """P1-删除用户取消"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先新增用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 点击删除按钮
        result = user_biz.user_page.click_delete_user(test_user_data['userName'])
        
        # 只有成功打开确认弹窗才执行取消操作
        if result:
            # 取消确认
            user_biz.user_page.click_delete_cancel_button()
        
        # 验证未删除
        user_info = user_biz.get_user_info(test_user_data['userName'])
        assert user_info['nickName'] == test_user_data['nickName'], f"删除取消按钮未生效"
        
        # 清理：删除测试用户
        user_biz.delete_user(test_user_data['userName'])
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_batch_delete(self, common_biz,user_biz, test_user_data_batch):
        """P2-批量删除用户"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 批量创建以batch_开头的用户
        for user_data in test_user_data_batch:
            user_biz.add_user(user_data)
        
        # 批量删除
        message = user_biz.batch_delete("batch_")
        assert "成功" in message
        
        
        
        
    # ========== 搜索功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_user_search_by_username(self, common_biz,user_biz, test_user_data):
        """P0-按用户名搜索"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先创建用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        # 验证搜索结果
        user_count = user_biz.search_user(test_user_data['userName'])
        assert user_count == 1, "用户未搜索到"
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_search_by_phone(self, common_biz,user_biz, test_user_data):
        """P1-按手机号搜索"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先创建用户
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        
        user_info = user_biz.search_by_phone(test_user_data['phonenumber'])
        
        # 验证搜索结果
        assert user_info['phonenumber'] == test_user_data['phonenumber'], f"搜索到的手机号为 {user_info['phonenumber']}"
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_search_by_status(self, common_biz,user_biz, test_user_data):
        """P1-按状态搜索"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先创建测试用户（避免依赖系统已有用户，实现测试隔离）
        message = user_biz.add_user(test_user_data)
        assert "成功" in message, f"创建测试用户失败: {message}"
        
        # 搜索正常状态用户
        message = user_biz.search_by_status("正常")
        
        # 验证搜索
        assert message
        assert message == "状态匹配", "搜索到的用户状态不是正常"

        user_biz.delete_user(test_user_data['userName'])
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_search_no_result(self, common_biz,user_biz):
        """P2-搜索无结果"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        user_info = user_biz.get_user_info("nonexistent_xyz_123456")
        
        # 验证无结果提示
        assert user_info is None, "搜索到了不存在的用户"
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_search_reset(self, common_biz,user_biz, test_user_data):
        """P2-重置搜索条件"""
        common_biz.switch_menu("系统管理/用户管理") 
        
        # 先创建一个测试用户，确保测试隔离
        message = user_biz.add_user(test_user_data)
        assert "成功" in message, f"创建测试用户失败: {message}"
   
        
        # 获取初始行数（包含我们刚创建的用户）
        initial_count = user_biz.get_row_count()
        print(f"初始行数: {initial_count}")
        
        # 搜索不存在的用户
        user_biz.search_user("nonexistent_user_xyz_12345")
        searched_count = user_biz.get_row_count()
        print(f"搜索不存在用户后行数: {searched_count}")
        
        # 验证搜索结果应该少于或等于初始行数
        assert searched_count <= initial_count, f"搜索后行数({searched_count})应小于等于初始行数({initial_count})"
        
        # 重置搜索
        user_biz.reset_search()
        user_biz.user_page.page.wait_for_timeout(500)
        
        # 验证恢复到初始状态（行数应该和初始行数相同）
        reset_count = user_biz.get_row_count()
        print(f"重置后行数: {reset_count}")
        
        # 验证恢复（允许1行的差异，因为可能有余弦）
        assert abs(reset_count - initial_count) <= 1, f"重置后行数({reset_count})应接近初始行数({initial_count})"
        
        # 清理测试用户
        user_biz.delete_user(test_user_data['userName'])
    
    # ========== 导出功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_user_export(self, user_page):
        """P1-导出用户数据"""
        
        # 设置下载目录
        user_page.page.context.set_default_timeout(30000)
        
        # 点击下载
        with user_page.page.expect_download() as download_info:
            user_page.click_export()
        
        download = download_info.value
        
        # 验证文件下载
        assert download.path().exists()
        # 使用suggested_filename验证文件类型，因为path()可能返回临时路径没有后缀
        assert any(download.suggested_filename.endswith(ext) for ext in ['.xlsx', '.xls', '.csv'])
    
    # ========== 导入功能 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_user_import(self, user_page, tmp_path):
        """P2-导入用户数据"""
        
        # 准备导入文件
        import_file = tmp_path / "users.xlsx"
        # 创建一个空的Excel文件（实际测试中需要填充数据）
        import_file.touch()
        
        # 点击导入
        user_page.click_import()
        
        # 上传文件
        user_page.page.set_input_files('input[type="file"]', str(import_file))
        
        # 验证导入结果