from ui.pages.modules.login_page import LoginPage
from ui.biz.common_biz import CommonBiz
from config.settings import Settings
from playwright.sync_api import expect
from common.utils.retry_helper import (
    retry_on_network_error,
    safe_navigation,
    safe_reload,
    is_network_error,
    RetryConfig,
)

class LoginBiz():
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.common_biz = CommonBiz(page)
        self.setting = Settings()
    def navigate_to(self,endpoint="/login"):
        """导航到登录页面"""
        self.common_biz.navigate_to(endpoint)
        
    def login(self, username=None, password=None, is_rember_me=False, max_retries: int = 3):
        """管理员正常登录（带增强的网络错误处理和重试机制）"""
        import time
        login_username = username or self.setting.USERNAME
        login_password = password or self.setting.PASSWORD
        
        for attempt in range(max_retries + 1):
            try:
                # 确保在登录页面
                if "login" not in self.page.url:
                    print(f"导航到登录页面...")
                    safe_navigation(self.page, self.setting.BASE_URL + "/login", max_retries=2)
                
                # 等待页面DOM加载完成
                print("等待页面DOM加载...")
                self.page.wait_for_load_state("domcontentloaded", timeout=30000)
                
                # 等待网络空闲（SPA应用需要等待JS执行完成）
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                    print("网络请求完成")
                except:
                    print("网络请求等待超时，继续执行")
                
                # 额外等待确保React/Vue渲染完成
                self.page.wait_for_timeout(2000)
                
                # 截图查看页面状态
                self.page.screenshot(path=f"login_attempt_{attempt}.png")
                print(f"已保存登录页面截图: login_attempt_{attempt}.png")
                
                # 检查页面是否包含登录表单的关键元素
                try:
                    username_input = self.page.locator("input[placeholder*='账号']")
                    if username_input.count() == 0:
                        print("⚠️ 未找到用户名输入框，等待后重试...")
                        self.page.wait_for_timeout(3000)
                        if username_input.count() == 0:
                            print("❌ 仍然未找到用户名输入框")
                            if attempt < max_retries:
                                continue
                            else:
                                return "登录失败: 页面未正确加载"
                except Exception as check_error:
                    print(f"检查页面元素时出错: {check_error}")
                
                # 填写表单
                print("开始填写登录表单...")
                self.login_page.fill_username(login_username)
                print("✅ 用户名填写完成")
                
                self.login_page.fill_password(login_password)
                print("✅ 密码填写完成")
                
                if self.login_page.is_visible(self.login_page.CAPTCHA_INPUT, timeout=3000):
                    self.login_page.fill_captcha('skip_captcha')
                    print("✅ 验证码填写完成")
                else:
                    print("ℹ️ 验证码输入框不可见，跳过填写")
                
                if is_rember_me:
                    self.check_remember_me()
                
                # 点击登录按钮
                print("点击登录按钮...")
                self.login_page.click_submit_button()

                # 等待页面跳转
                print("等待页面跳转...")
                self.login_page.wait_for_load_state("domcontentloaded", timeout=30000)
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                except:
                    pass
                
                # 处理安全提示弹窗
                if self.login_page.is_visible_user_login_prompt():
                    self.login_page.click_user_login_prompt_cancel()
                
                # 检查登录结果
                result = self.is_logged_in()
                if "成功" in result:
                    return result
                    
                if attempt < max_retries:
                    print(f"⚠️ 登录失败，尝试重试 ({attempt + 1}/{max_retries})")
                    time.sleep(3)
                    safe_reload(self.page, max_retries=2)
                    self.login_page.wait_for_load_state()
                else:
                    return result
                    
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ 登录过程异常: {error_msg}")
                
                if is_network_error(e):
                    print("❌ 检测到网络错误")
                    print(f"   后端地址: {self.setting.API_BASE_URL}")
                    print(f"   前端地址: {self.setting.BASE_URL}")
                
                if attempt < max_retries:
                    print(f"等待3秒后重试 ({attempt + 1}/{max_retries})")
                    time.sleep(3)
                    try:
                        safe_reload(self.page, max_retries=2)
                    except Exception as reload_error:
                        print(f"刷新页面失败，尝试重新导航: {reload_error}")
                        safe_navigation(self.page, self.setting.BASE_URL + "/login", max_retries=2)
                    self.login_page.wait_for_load_state()
                else:
                    return f"登录失败: {error_msg}"
        
        return "登录失败"
        
    def logout(self, max_retries: int = 3):
        """用户正常退出（带增强的网络错误处理和重试机制）"""
        for attempt in range(max_retries + 1):
            try:
                if "/login" in self.page.url or self.is_logged_out():
                    print("✅已经在登录页面，无需退出")
                    return "退出登录成功"
                
                user_info_clicked = self._click_user_info_with_retry()
                
                if user_info_clicked:
                    logout_clicked = self._click_logout_with_retry()
                    
                    if logout_clicked:
                        self.page.wait_for_timeout(1000)
                        
                        confirm_clicked = self._confirm_logout_with_retry()
                        if confirm_clicked:
                            print("✅点击确认退出按钮")
                        
                        self.login_page.wait_for_load_state("networkidle")
                        self.page.wait_for_timeout(2000)
                
                current_url = self.login_page.page.url
                print(f"退出后当前URL: {current_url}")
                
                if "/login" in current_url or self.is_logged_out():
                    print("✅退出登录成功，跳转到登录页面")
                    return "退出登录成功"
                else:
                    print(f"⚠️退出登录失败，未跳转到登录页面，当前URL: {current_url}")
                    
                    if attempt < max_retries:
                        print(f"⚠️ 重试退出登录 ({attempt + 1}/{max_retries})")
                        safe_navigation(self.page, self.setting.BASE_URL + "/login", max_retries=2)
                        self.page.wait_for_load_state("networkidle")
                    else:
                        self.page.screenshot(path="logout_not_redirected.png")
                        return "退出登录失败"
                        
            except Exception as e:
                print(f"退出登录过程出错: {e}")
                import traceback
                traceback.print_exc()
                
                if attempt < max_retries:
                    print(f"⚠️ 重试退出登录 ({attempt + 1}/{max_retries})")
                    try:
                        safe_reload(self.page, max_retries=2)
                    except:
                        safe_navigation(self.page, self.setting.BASE_URL + "/login", max_retries=2)
                    self.login_page.wait_for_load_state("networkidle")
                else:
                    self.page.screenshot(path="logout_error.png")
                    try:
                        safe_navigation(self.page, self.setting.BASE_URL + "/login", max_retries=2)
                        if "/login" in self.login_page.page.url or self.is_logged_out():
                            print("✅通过直接导航退出登录成功")
                            return "退出登录成功"
                    except:
                        pass
                    return "退出登录失败"
    
    def _click_user_info_with_retry(self) -> bool:
        """多种方式点击用户信息按钮"""
        selectors = [
            ".user-nickname",
            "//span[contains(@class, 'user-nickname')]",
            "//*[contains(text(), 'admin')]",
            "//div[@class='avatar-wrapper']",
        ]
        
        for selector in selectors:
            try:
                element = self.page.locator(selector)
                if element.count() > 0 and element.first.is_visible():
                    element.first.click()
                    print(f"✅点击用户信息按钮成功，选择器: {selector}")
                    self.page.wait_for_timeout(500)
                    return True
            except Exception as e:
                print(f"尝试选择器 {selector} 失败: {e}")
        
        # 最后尝试使用配置的定位器
        try:
            result = self.login_page.click_user_info()
            if result:
                print("✅使用配置的定位器点击用户信息按钮成功")
                return True
        except Exception as e:
            print(f"使用配置定位器失败: {e}")
        
        return False
    
    def _click_logout_with_retry(self) -> bool:
        """多种方式点击退出按钮"""
        selectors = [
            "//li[contains(text(), '退出登录')]",
            "//span[contains(text(), '退出登录')]",
            ".el-dropdown-menu__item:has-text('退出登录')",
        ]
        
        for selector in selectors:
            try:
                element = self.page.locator(selector)
                if element.count() > 0 and element.first.is_visible():
                    element.first.click()
                    print(f"✅点击退出登录按钮成功，选择器: {selector}")
                    self.page.wait_for_timeout(500)
                    return True
            except Exception as e:
                print(f"尝试选择器 {selector} 失败: {e}")
        
        # 最后尝试使用配置的定位器
        try:
            self.login_page.click_logout()
            print("✅使用配置的定位器点击退出登录按钮成功")
            return True
        except Exception as e:
            print(f"使用配置定位器失败: {e}")
        
        return False
    
    def _confirm_logout_with_retry(self) -> bool:
        """多种方式确认退出弹窗"""
        try:
            # 尝试使用公共业务方法
            result = self.common_biz.system_prompt_confirm(
                self.login_page.SYS_PROMPT, 
                self.login_page.SYS_PROMPT_CONFIRM
            )
            if result:
                return True
        except Exception as e:
            print(f"使用公共业务方法失败: {e}")
        
        # 尝试其他方式
        confirm_selectors = [
            "//button[contains(text(), '确定')]",
            "//button[contains(text(), '确认')]",
            ".el-dialog__footer button.el-button--primary",
            self.page.get_by_role("button", name="确定"),
            self.page.get_by_role("button", name="确认"),
        ]
        
        for selector in confirm_selectors:
            try:
                if isinstance(selector, str):
                    element = self.page.locator(selector)
                else:
                    element = selector
                
                if element.count() > 0 and element.first.is_visible():
                    element.first.click()
                    print(f"✅点击确认按钮成功")
                    self.page.wait_for_timeout(500)
                    return True
            except Exception as e:
                print(f"尝试确认选择器失败: {e}")
        
        return False
    
    def is_logged_out(self, timeout: int = 5000) -> bool:
        """判断登录页面是否可见（增强版）"""
        try:
            # 首先检查URL
            if "/login" in self.login_page.page.url:
                print("✅URL包含/login，认为已退出登录")
                return True
            
            # 检查登录页面的关键元素是否可见
            self.login_page.wait_for_load_state()
            
            # 使用多种方式检查登录页面元素
            checks = [
                ("用户名输入框", self.login_page.username_is_visible(timeout=timeout)),
                ("密码输入框", self.login_page.password_is_visible(timeout=timeout)),
                ("登录按钮", self.login_page.submit_button_is_visible(timeout=timeout)),
            ]
            
            # 如果有2个以上元素可见，认为在登录页面
            visible_count = sum(1 for _, visible in checks if visible)
            
            if visible_count >= 2:
                print(f"✅检测到 {visible_count} 个登录页面元素，认为已退出登录")
                return True
            
            # 额外检查：是否存在登录相关的placeholder
            try:
                placeholder_check = self.page.locator("input[placeholder*='账号'], input[placeholder*='密码'], input[placeholder*='验证码']")
                if placeholder_check.count() >= 2:
                    print("✅检测到登录输入框，认为已退出登录")
                    return True
            except:
                pass
            
            print(f"❌未检测到足够的登录页面元素（{visible_count}/3）")
            return False
            
        except Exception as e:
            print(f"❌is_logged_out 检查失败: {e}")
            return False

    def is_logged_in(self):
        """检查是否已登录"""
        result = self.login_page.is_login_success()
        if result:
            print("✅登录成功")
            return "登录成功"
        else:
            # 使用page对象进行截图
            self.page.screenshot(path="login_failed.png")
            error_message = self.login_page.get_error_message()
            print(f"❌登录失败: {error_message}")
            return f"登录失败: {error_message}"
    def is_login_page(self) -> bool:
        """判断是否在登录页面"""
        self.login_page.wait_for_load_state()
        return "/login" in self.login_page.page.url

    def session_timeout(self):
        """模拟会话超时（通过清除cookies）"""
        print("模拟会话超时，清除所有cookies...")
        self.page.context.clear_cookies()
        print("✅ 会话超时模拟完成")
        

    def verify_captcha_image(self):
        """验证验证码图片显示"""
        self.login_page.navigate_to_login()
        return self.login_page.is_visible(self.login_page.CAPTCHA_IMAGE)

    def check_remember_me(self):
        """勾选记住我"""
        try:
            self.login_page.click_remember_me()
        except Exception as e:
            print(f"直接点击失败，尝试点击父元素: {e}")
            # 对于Element Plus的复选框，需要点击整个组件
            try:
                # 尝试通过CSS选择器点击
                checkbox_wrapper = self.page.locator(".el-checkbox")
                if checkbox_wrapper:
                    checkbox_wrapper.click()
                    print("通过CSS选择器点击记住密码")
            except Exception as e3:
                print(f"所有尝试都失败: {e3}")
    def verify_remember_me(self,username: str):
        """验证记住我勾选状态"""
        username_input = self.login_page.get_username_locator()
        expect(username_input).to_have_value(username)
        password_input = self.login_page.get_password_locator()
        save_password = password_input.input_value()
        return save_password
    