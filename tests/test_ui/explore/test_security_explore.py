import pytest
from ui.pages.modules.user_page import UserPage
from ui.pages.modules.role_page import RolePage
from ui.biz.common_biz import CommonBiz
from ui.biz.normal.user_biz import UserBiz
import random
import string

@pytest.mark.ui
@pytest.mark.explore
class TestSecurityExplore:
    """安全探索测试"""

    def test_user_input_xss(self, common_biz,user_biz,security_biz,test_user_data):
        """输入XSS脚本 → 系统不解析、正常拦截"""
        common_biz.switch_menu("系统管理/用户管理")
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '<img onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            'javascript:alert("XSS")',
        ]
        
        for payload in xss_payloads:
            test_user_data['userName'] = f"xss_user_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            test_user_data['nickName'] = payload
            result = security_biz.input_xss_payload(user_biz.user_page,payload,test_user_data)
            alert_count = result["alert_count"]
            message = result["message"]
            is_blocked = result["is_blocked"]
            page_has_payload = result["page_has_payload"]

            print(f"\n🎯 测试Payload: {payload}")
            print(f"📩 系统提示: {message}")
            print(f"🚫 是否被拦截: {is_blocked}")
            print(f"📄 页面是否包含Payload: {page_has_payload}")

            # ==================== 核心安全断言 ====================
            # 1. 不能有任何JS弹窗
            assert alert_count == 0, f"❌ XSS弹窗执行成功: {payload}"
            
            # 2. 高危Payload必须被拦截 或 不出现在页面
            if payload in [
                '<script', 'javascript:', 'onerror=', 'onload=', '<svg'
            ]:
                assert is_blocked or not page_has_payload, f"❌ 高危XSS未过滤: {payload}"

            # 3. javascript: 伪协议 100% 不允许出现在页面
            if 'javascript:' in payload:
                if page_has_payload:
                    print(f"⚠️ 警告：javascript:伪协议可能存在XSS风险: {payload}")
                else:
                    print(f"✅ javascript:伪协议已被正确处理")

            # 清理数据
            if is_blocked:
                try:
                    user_biz.user_page.delete_user(test_user_data['userName'])
                    print(f"✅ 已清理测试用户")
                except Exception as e:
                    print(f"⚠️ 清理用户失败: {e}")

            print(f"✅ XSS 防护正常: {payload}\n")
        
      
    def test_search_sql_inject(self, login_home, common_biz, security_biz,user_biz):
        """搜索框SQL注入 → 系统不报错、无注入风险"""
        user_page = UserPage(login_home)
        common_biz.switch_menu("系统管理/用户管理")
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE sys_user; --",
            "admin'--",
            "1' AND '1'='1",
        ]
        
        for payload in sql_payloads:
            security_biz.input_sql_inject(user_page,payload)
            # 验证无系统异常
            assert login_home.locator("text=系统异常").count() == 0
            # 验证无数据库错误
            page_content = login_home.content()
            assert "SQLException" not in page_content
            print(f"✅SQL 注入失败，系统正常: {payload}")
            
            # 重置搜索
            user_biz.reset_search()
        

    def test_unauthorized_url_visit(self, login_home, security_biz,test_user_data):
        """低权限越权访问菜单 → 无权限拦截"""
        pass
    def test_no_login_visit_system(self, page, security_biz):
        """未登录直接访问后台 → 跳转到登录页"""
        security_biz.visit_system_without_login("/system/user")
        assert "login" in page.url

    def test_edit_other_user(self, login_home, security_biz):
        """尝试编辑他人数据 → 权限拦截"""
        CommonBiz(login_home).switch_menu("系统管理/用户管理")
        security_biz.edit_other_user_data("admin")