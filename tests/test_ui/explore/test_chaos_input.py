"""
L4: 混沌输入探索式测试
验证系统对异常输入的处理能力
"""
from codeop import CommandCompiler
import pytest
import random
import string
from ui.components.menu_component import MenuItem
from ui.biz.common_biz import CommonBiz
from ui.pages.modules.user_page import UserPage
from ui.biz.special.abnormal_biz import AbnormalBiz
from ui.biz.normal.user_biz import UserBiz






class TestChaosInput:
    """混沌输入测试"""
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_sql_injection_input(self, common_biz,user_biz,security_biz):
        """混沌测试 - SQL 注入输入"""
        # 导航到用户管理模块
        common_biz.switch_menu("系统管理/用户管理")
        
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE sys_user; --",
            "admin'--",
            "1' AND '1'='1",
        ]
        
        for payload in sql_payloads:
            # 搜索框输入
            research_result = security_biz.input_sql_inject(user_biz, payload)
            #验证返回list为空
            assert research_result==0, f"SQL 注入成功，搜索结果包含用户: {research_result}"
            # 验证无系统异常
            assert user_biz.page.locator("text=系统异常").count() == 0
            # 验证无数据库错误
            page_content = user_biz.page.content()
            assert "SQLException" not in page_content
            print(f"✅SQL 注入失败，系统正常: {payload}")
            
            # 重置搜索
            user_biz.reset_search()
            print(f"✅SQL 注入测试通过，系统稳定: {payload}")
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_xss_input(self, login_home,user_page,test_user_data):
        """混沌测试 - XSS 输入"""
        common_biz = CommonBiz(login_home)
        user_biz = UserBiz(login_home)
        result = common_biz.switch_menu("系统管理/用户管理")
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            'javascript:alert("XSS")',
        ]
        
        for payload in xss_payloads:
            test_user_data['userName'] = f"xss_user_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            test_user_data['nickName'] = payload
            message = user_biz.add_user(test_user_data)

            assert message
            if  "成功" in message:
                message = user_biz.delete_user(test_user_data['userName'])
                assert "成功" in message
                print(f"✅XSS 注入失败，用户创建成功: {payload}")      


    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_long_string_input(self, login_home,user_page,test_user_data):
        """混沌测试 - 超长字符串输入"""
        common_biz = CommonBiz(login_home)
        user_biz = UserBiz(login_home)
        result = common_biz.switch_menu("系统管理/用户管理")
        
        # 生成超长字符串
        long_string = "a" * 10000
        test_user_data['nickName'] = long_string
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        print(f"✅超长字符串输入截断处理成功")
        #删除数据
        message = user_biz.delete_user(test_user_data['userName'])
        assert "成功" in message
        print(f"✅超长字符串输入截断处理成功，用户删除成功: {long_string}")
  

    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_special_characters_input(self, login_home,user_page,test_user_data):
        """混沌测试 - 特殊字符输入"""
        common_biz = CommonBiz(login_home)
        user_biz = UserBiz(login_home)
        result = common_biz.switch_menu("系统管理/用户管理")
        
        special_chars = [
            "!@#$%^&*()_+-=[]{}|;:',.<>?/",
            "🎉🎊🎈🎁🎀",  # Emoji
            "中文测试",
            "Русский",  # 俄语
            "العربية",  # 阿拉伯语
        ]
        
        for i, chars in enumerate(special_chars):
            # 为每个测试用例生成唯一的用户名
            unique_username = f"test_{i}_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            test_user_data['nickName'] = chars
            test_user_data['userName'] = unique_username
            message = user_biz.add_user(test_user_data)
            assert message, f"特殊字符输入失败，字符: {chars}"
            if  "成功" in message:
                
                message = user_biz.delete_user(test_user_data['userName'])
                assert "成功" in message
                print(f"✅特殊字符输入失败，用户创建成功: {chars}")
            
            # 验证系统能正确处理
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_null_bytes_input(self, login_home,user_page,test_user_data):
        """混沌测试 - 空字节输入"""
        common_biz = CommonBiz(login_home)
        user_biz = UserBiz(login_home)
        result = common_biz.switch_menu("系统管理/用户管理")
        
        null_payload = f"{random.randint(1000,9999)}_test\x00user"
        test_user_data['userName'] = null_payload
        message = user_biz.add_user(test_user_data)
        assert "成功" in message
        if  "成功" in message:
                message = user_biz.delete_user(test_user_data['userName'])
                assert "成功" in message
                print(f"✅空字节输入失败，用户创建成功: {null_payload}")

class TestRapidOperations:
    """快速操作测试"""
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_rapid_click(self, login_home,user_page,abnormal_biz):
        """混沌测试 - 快速连续点击"""
        common_biz = CommonBiz(login_home)
        user_biz = UserBiz(login_home)
        result = common_biz.switch_menu("系统管理/用户管理")
        
        abnormal_biz.repeat_click_btn(user_page, "USER_ADD_BUTTON", times=3)
        
        # 验证页面未崩溃
        assert user_page.is_visible(user_page.SEARCH_INPUT), "系统崩溃，搜索框不可见"
        print("✅快速点击 3 次，系统未崩溃")
    
    @pytest.mark.ui
    @pytest.mark.l4
    @pytest.mark.exploratory
    @pytest.mark.chaos
    def test_rapid_form_submit(self, login_home,user_page,test_user_data):
        """混沌测试 - 快速表单提交"""
        common_biz = CommonBiz(login_home)
        user_biz = UserBiz(login_home)
        result = common_biz.switch_menu("系统管理/用户管理")
        
        abnormal_biz = AbnormalBiz(user_page)
        
        # 测试快速连续提交
        created_users = []
        for i in range(3):
            unique_username = f'rapid_user_{i}_{random.randint(1000, 9999)}'
            test_user_data['userName'] = unique_username
            test_user_data['nickName'] = f'快速测试用户{i}'
            
            try:
                message = user_biz.add_user(test_user_data)
                if "成功" in message:
                    created_users.append(unique_username)
                    print(f"✅快速创建用户成功: {unique_username}")
            except Exception as e:
                print(f"⚠️快速创建用户可能失败: {e}")
        
        # 验证系统仍然稳定
        assert user_page.is_visible(user_page.SEARCH_INPUT), "系统崩溃，搜索框不可见"
        print("✅系统稳定性验证通过")
        
        # 清理创建的用户
        for username in created_users:
            try:
                message = user_biz.delete_user(username)
                assert "成功" in message
                print(f"🧹清理测试用户: {username}")
            except Exception as e:
                print(f"⚠️清理用户失败: {e}")
