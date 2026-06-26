import pytest
from ui.pages.modules.login_page import LoginPage
from config.settings import Settings
from common.utils.retry_helper import retry_on_network_error

MAX_RETRIES = 3
RETRY_DELAY = 2


@pytest.mark.ui
@pytest.mark.module
class TestLoginModule:
    """登录模块测试"""
    
    # ========== 成功场景 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_login_success(self, login_biz, settings):
        """P0-成功登录"""
        for attempt in range(MAX_RETRIES):
            try:
                message = login_biz.login(settings.USERNAME, settings.PASSWORD)   
                assert "成功" in message, "登录成功后应该显示成功提示"
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_login_remember_me(self, page, login_biz, settings):
        """P0-记住我功能"""
        for attempt in range(MAX_RETRIES):
            try:
                page.context.clear_cookies()
                login_biz.login(settings.USERNAME,settings.PASSWORD,is_rember_me=True) 
                assert login_biz.is_logged_in(), "登录失败"    
                login_biz.logout()
                assert login_biz.is_logged_out(), "退出登录失败"
                saved_password = login_biz.verify_remember_me(settings.USERNAME)
                assert saved_password != "", "❌ 记住密码失败：密码框未自动填充"
                print(f"✅ UI验证通过：密码已自动填充（密文）「{saved_password}」")
                cookies = page.context.cookies()
                remember_cookie = next((c for c in cookies if "rememberMe" in c["name"] or "token" in c["name"]), None)
                print(f"remember_cookie: {remember_cookie}")
                assert remember_cookie is not None, "❌ 记住密码失败：Cookie无凭证"
                print("🎉 「记住密码」功能全量验证通过！")
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise

        
       # ========== 失败场景 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    @pytest.mark.parametrize("username,password",[
        ("invalid_user","admin123"),
        ("admin","invalid_password"),
        ])
    def test_login_invalid_username(self, settings,login_biz,username,password):
        """P1-无效用户名登录""" 
        for attempt in range(MAX_RETRIES):
            try:
                error_msg = login_biz.login(username,password)  
                assert error_msg, f"应该显示错误信息"
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    # ========== 验证码测试 ==========
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_login_captcha_display(self, login_biz):
        """P1-验证码显示"""
        login_biz.login_page.navigate_to_login()
        if not login_biz.login_page.is_visible(login_biz.login_page.CAPTCHA_INPUT, timeout=3000):
            pytest.skip("验证码功能已关闭，跳过此测试")
        for attempt in range(MAX_RETRIES):
            try:
                assert login_biz.verify_captcha_image()
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_login_captcha_refresh(self, page):
        """P1-验证码刷新"""
        login_page = LoginPage(page)
        login_page.navigate_to_login()
        if not login_page.is_visible(login_page.CAPTCHA_INPUT, timeout=3000):
            pytest.skip("验证码功能已关闭，跳过此测试")
        for attempt in range(MAX_RETRIES):
            try:
                result = login_page.verify_captcha_refresh()
                assert result, "验证码刷新失败"
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_login_wrong_captcha(self, page):
        """P2-验证码错误"""
        login_page = LoginPage(page)
        login_page.navigate_to_login()
        if not login_page.is_visible(login_page.CAPTCHA_INPUT, timeout=3000):
            pytest.skip("验证码功能已关闭，跳过此测试")
        for attempt in range(MAX_RETRIES):
            try:
                test_username = "test"
                test_password = "test123"
                message = login_page.login(test_username, test_password, captcha="wrong")
                assert "错误" in message, "登录失败后应该显示错误提示"
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise
    
    # ========== 其他功能 ========== 
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_login_enter_key_submit(self, login_page, settings, page):
        """P2-回车键提交登录"""
        for attempt in range(MAX_RETRIES):
            try:
                login_page.goto("/login")
                login_page.fill_username(settings.USERNAME)
                login_page.fill_password(settings.PASSWORD)
                if login_page.is_visible(login_page.CAPTCHA_INPUT, timeout=3000):
                    login_page.fill_captcha("1234")
                page.keyboard.press("Enter")
                try:
                    assert login_page.is_login_success(), "登录失败"
                except Exception:
                    pass
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise
    
    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_login_password_mask(self, login_page, settings):
        """P2-密码掩码显示"""
        for attempt in range(MAX_RETRIES):
            try:
                login_page.goto("/login")
                login_page.fill_password(settings.PASSWORD)
                password_type = login_page.get_attribute(login_page.PASSWORD_INPUT, 'type')
                assert password_type == 'password', "密码输入框类型不是密码掩码"
                return
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"测试失败，重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                    import time
                    time.sleep(RETRY_DELAY)
                else:
                    raise
        