"""
登录页面（改进版）
基于BasePage增强，提供更可靠的元素定位和操作封装
"""
import time
import allure
from typing import Optional, Union
from playwright.sync_api import Page, expect as playwright_expect

from ui.pages.base_page import BasePage
from config.settings import Settings
from common.logger import Logger

class LoginPageImproved(BasePage):
    """
    登录页面（改进版）
    
    改进点：
    1. 更可靠的登录状态判断
    2. 完善错误处理
    3. 增加等待重试机制
    4. 更好的截图和日志
    5. 支持AI元素定位（可选）
    """
    
    # ==================== 元素定位器 ====================
    
    # 登录表单元素
    USERNAME_INPUT = 'login.username_input'
    PASSWORD_INPUT = 'login.password_input'
    CAPTCHA_INPUT = 'login.captcha_input'
    CAPTCHA_IMAGE = 'login.captcha_image'
    SUBMIT_BUTTON = 'login.submit_button'
    REMEMBER_ME = 'login.remember_me'
    
    # 错误提示元素
    ERROR_MESSAGE = 'login.error_message'
    USERNAME_ERROR = 'login.username_error'
    PASSWORD_ERROR = 'login.password_error'
    
    # 系统提示弹窗
    SYS_PROMPT = 'common.sys_prompt'
    SYS_PROMPT_CONFIRM = 'common.sys_prompt_confirm'
    USER_LOGIN_PROMPT = 'common.user_login_prompt'
    USER_LOGIN_PROMPT_CANCEL = 'common.user_login_prompt_cancel'
    
    # 登录成功后的元素
    USER_INFO = 'home.user_info'
    LOGOUT_BUTTON = 'home.logout_button'
    INDEX = 'home.menu'
    
    # ==================== 初始化 ====================
    
    def __init__(self, page: Page, use_ai_locator: bool = False):
        """
        初始化登录页面
        
        Args:
            page: Playwright Page对象
            use_ai_locator: 是否使用AI元素定位器（可选）
        """
        super().__init__(page)
        self.settings = Settings()
        self.logger = Logger(__name__)
        self.use_ai_locator = use_ai_locator
        
        # 登录结果
        self._last_login_result: Optional[str] = None
        self._last_error_message: Optional[str] = None
    
    # ==================== 页面导航 ====================
    
    def navigate_to_login(self) -> 'LoginPageImproved':
        """导航到登录页面"""
        self.logger.info("导航到登录页面")
        self.goto("/login")
        self.wait_for_page_load()
        return self
    
    def navigate_to_home(self) -> 'LoginPageImproved':
        """导航到首页"""
        self.logger.info("导航到首页")
        self.goto("/index")
        self.wait_for_page_load()
        return self
    
    # ==================== 登录操作 ====================
    
    @allure.step("执行登录操作")
    def login(
        self,
        username: str,
        password: str,
        captcha: str = "1234",
        remember_me: bool = False,
        retry_on_failure: bool = True,
        max_retries: int = 2
    ) -> bool:
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            captcha: 验证码（默认1234，适用于开发环境）
            remember_me: 是否记住我
            retry_on_failure: 失败时是否重试
            max_retries: 最大重试次数
            
        Returns:
            bool: 登录是否成功
        """
        self.logger.info(f"开始登录: username={username}")
        
        # 检查是否已登录
        if self.is_logged_in():
            self.logger.info("用户已登录，跳过登录")
            self._last_login_result = "already_logged_in"
            return True
        
        # 导航到登录页面
        self.navigate_to_login()
        
        # 填写表单
        self._fill_login_form(username, password, captcha, remember_me)
        
        # 点击登录按钮
        self._click_login_button()
        
        # 等待登录结果
        time.sleep(2)  # 等待页面响应
        
        # 判断登录结果
        success = self.is_login_success()
        
        if success:
            self.logger.info("✅ 登录成功")
            self._last_login_result = "success"
        else:
            self.logger.warning("❌ 登录失败")
            self._last_login_result = "failed"
            self._last_error_message = self.get_error_message()
            
            # 如果启用重试且失败
            if retry_on_failure and max_retries > 0:
                self.logger.info(f"重试登录 (剩余重试次数: {max_retries - 1})")
                return self.login(
                    username, password, captcha, remember_me,
                    retry_on_failure=True,
                    max_retries=max_retries - 1
                )
        
        return success
    
    def _fill_login_form(
        self,
        username: str,
        password: str,
        captcha: str,
        remember_me: bool
    ):
        """填写登录表单"""
        with allure.step("填写登录表单"):
            # 填写用户名
            self.fill(self.USERNAME_INPUT, username)
            self.logger.debug(f"已填写用户名: {username}")
            
            # 填写密码
            self.fill(self.PASSWORD_INPUT, password)
            self.logger.debug("已填写密码")
            
            # 填写验证码
            if self.is_visible(self.CAPTCHA_INPUT, timeout=2000):
                self.fill(self.CAPTCHA_INPUT, captcha)
                self.logger.debug(f"已填写验证码: {captcha}")
            
            # 记住我
            if remember_me:
                self.click(self.REMEMBER_ME)
                self.logger.debug("已勾选记住我")
    
    def _click_login_button(self):
        """点击登录按钮"""
        with allure.step("点击登录按钮"):
            self.logger.info("点击登录按钮")
            
            # 截图登录前状态
            self.take_screenshot("login_before_submit.png")
            
            # 点击按钮
            self.click(self.SUBMIT_BUTTON)
            
            # 等待页面响应
            self.wait_for_page_load()
            
            # 截图登录后状态
            self.take_screenshot("login_after_submit.png")
    
    # ==================== 登录状态判断 ====================
    
    @allure.step("验证登录状态")
    def is_login_success(self, timeout: int = 10000) -> bool:
        """
        判断登录是否成功（多维度判断）
        
        判断依据：
        1. URL跳转到首页（/index）
        2. 用户信息元素可见
        3. 首页菜单可见
        
        Args:
            timeout: 超时时间（毫秒）
            
        Returns:
            bool: 登录是否成功
        """
        try:
            # 等待页面加载
            self.wait_for_load_state('networkidle')
            
            # 方式1：检查URL
            current_url = self.page.url
            self.logger.debug(f"当前URL: {current_url}")
            
            if "/index" in current_url:
                self.logger.info("登录成功: URL跳转到/index")
                return True
            
            if "/login" in current_url and not self.is_visible(self.ERROR_MESSAGE, timeout=3000):
                # URL还在登录页，但错误信息不可见，可能登录成功
                if self.is_visible(self.USER_INFO, timeout=5000):
                    self.logger.info("登录成功: 检测到用户信息元素")
                    return True
            
            # 方式2：检查用户信息元素
            if self.is_visible(self.USER_INFO, timeout=timeout // 2):
                self.logger.info("登录成功: 用户信息元素可见")
                return True
            
            # 方式3：检查首页菜单
            if self.is_visible(self.INDEX, timeout=timeout // 2):
                self.logger.info("登录成功: 首页菜单可见")
                return True
            
            # 有错误信息表示登录失败
            if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
                error_msg = self.get_text(self.ERROR_MESSAGE)
                self.logger.warning(f"登录失败: {error_msg}")
                return False
            
            self.logger.warning("无法确定登录状态")
            return False
            
        except Exception as e:
            self.logger.error(f"判断登录状态异常: {e}")
            return False
    
    def is_logged_in(self) -> bool:
        """
        判断是否已登录（快速检查）
        
        Returns:
            bool: 是否已登录
        """
        try:
            # 检查URL
            if "/index" in self.page.url:
                return True
            
            # 检查用户信息元素
            if self.is_visible(self.USER_INFO, timeout=3000):
                return True
            
            return False
            
        except Exception:
            return False
    
    def is_on_login_page(self) -> bool:
        """
        判断是否在登录页面
        
        Returns:
            bool: 是否在登录页面
        """
        try:
            return self.is_visible(self.USERNAME_INPUT, timeout=5000)
        except Exception:
            return False
    
    # ==================== 错误处理 ====================
    
    @allure.step("获取错误信息")
    def get_error_message(self) -> str:
        """
        获取登录错误信息
        
        Returns:
            str: 错误信息
        """
        error_selectors = [
            (self.ERROR_MESSAGE, "表单错误"),
            (self.USERNAME_ERROR, "用户名错误"),
            (self.PASSWORD_ERROR, "密码错误"),
            ('common.toast_message', "Toast消息"),
            ('common.sys_prompt', "系统提示"),
        ]
        
        for selector, desc in error_selectors:
            try:
                if self.is_visible(selector, timeout=3000):
                    message = self.get_text(selector)
                    if message:
                        self.logger.info(f"获取到{desc}: {message}")
                        
                        # 如果是系统提示，点击确认按钮
                        if selector == 'common.sys_prompt':
                            self.click(self.SYS_PROMPT_CONFIRM)
                        
                        return message
            except Exception:
                continue
        
        self.logger.warning("未获取到错误信息")
        return ""
    
    def has_error_message(self) -> bool:
        """
        判断是否有错误提示
        
        Returns:
            bool: 是否有错误提示
        """
        return bool(self.get_error_message())
    
    # ==================== 退出登录 ====================
    
    @allure.step("执行退出登录")
    def logout(self) -> bool:
        """
        执行退出登录
        
        Returns:
            bool: 退出是否成功
        """
        self.logger.info("开始退出登录")
        
        try:
            # 截图退出前状态
            self.take_screenshot("logout_before.png")
            
            # 点击用户信息
            if self.is_visible(self.USER_INFO, timeout=5000):
                self.click(self.USER_INFO)
                self.wait_for_load_state('domcontentloaded')
            
            # 点击退出按钮
            if self.is_visible(self.LOGOUT_BUTTON, timeout=3000):
                self.click(self.LOGOUT_BUTTON)
            else:
                # 尝试通过文本定位
                self.page.get_by_text("退出", exact=False).click()
            
            # 等待确认弹窗
            self.wait_for_locator(self.SYS_PROMPT, state="visible", timeout=5000)
            
            # 点击确认
            self.click(self.SYS_PROMPT_CONFIRM)
            
            # 等待页面跳转
            self.wait_for_load_state('networkidle')
            time.sleep(1)
            
            # 截图退出后状态
            self.take_screenshot("logout_after.png")
            
            # 验证是否退出成功
            if self.is_on_login_page():
                self.logger.info("✅ 退出登录成功")
                return True
            else:
                self.logger.warning("⚠️ 退出登录后未回到登录页面")
                return False
                
        except Exception as e:
            self.logger.error(f"退出登录异常: {e}")
            self.take_screenshot("logout_error.png")
            return False
    
    # ==================== 验证码操作 ====================
    
    def get_captcha(self) -> Optional[bytes]:
        """
        获取验证码图片
        
        Returns:
            bytes: 验证码图片二进制数据
        """
        try:
            if self.is_visible(self.CAPTCHA_IMAGE, timeout=3000):
                screenshot = self.get_locator(self.CAPTCHA_IMAGE).screenshot()
                self.logger.info("获取验证码成功")
                return screenshot
        except Exception as e:
            self.logger.error(f"获取验证码失败: {e}")
        
        return None
    
    def refresh_captcha(self) -> bool:
        """
        刷新验证码
        
        Returns:
            bool: 是否刷新成功
        """
        try:
            if not self.is_visible(self.CAPTCHA_IMAGE, timeout=3000):
                self.logger.warning("验证码图片不可见")
                return False
            
            # 获取旧验证码
            old_captcha = self.get_attribute(self.CAPTCHA_IMAGE, "src")
            
            # 点击刷新
            self.click(self.CAPTCHA_IMAGE)
            
            # 等待验证码变化
            for _ in range(10):
                time.sleep(0.5)
                new_captcha = self.get_attribute(self.CAPTCHA_IMAGE, "src")
                if new_captcha and new_captcha != old_captcha:
                    self.logger.info("验证码刷新成功")
                    return True
            
            self.logger.warning("验证码刷新失败：未检测到变化")
            return False
            
        except Exception as e:
            self.logger.error(f"刷新验证码异常: {e}")
            return False
    
    # ==================== 验证操作 ====================
    
    @allure.step("验证页面元素")
    def verify_page_elements(self) -> dict:
        """
        验证登录页面所有关键元素
        
        Returns:
            dict: 元素验证结果
        """
        results = {
            "username_input": False,
            "password_input": False,
            "captcha_input": False,
            "captcha_image": False,
            "submit_button": False,
            "remember_me": False,
        }
        
        self.navigate_to_login()
        
        try:
            results["username_input"] = self.is_visible(self.USERNAME_INPUT, timeout=5000)
            results["password_input"] = self.is_visible(self.PASSWORD_INPUT, timeout=3000)
            results["captcha_input"] = self.is_visible(self.CAPTCHA_INPUT, timeout=3000)
            results["captcha_image"] = self.is_visible(self.CAPTCHA_IMAGE, timeout=3000)
            results["submit_button"] = self.is_visible(self.SUBMIT_BUTTON, timeout=3000)
            results["remember_me"] = self.is_visible(self.REMEMBER_ME, timeout=3000)
            
            self.logger.info(f"页面元素验证结果: {results}")
            
        except Exception as e:
            self.logger.error(f"验证页面元素异常: {e}")
        
        return results
    
    # ==================== 辅助方法 ====================
    
    def wait_for_page_load(self, timeout: int = 15000):
        """等待页面加载完成"""
        self.page.wait_for_load_state('domcontentloaded', timeout=timeout)
        self.page.wait_for_load_state('networkidle', timeout=timeout)
    
    def take_screenshot(self, name: str):
        """
        截图并保存
        
        Args:
            name: 文件名
        """
        try:
            self.page.screenshot(path=f"login_{name}", full_page=False)
            self.logger.debug(f"截图已保存: login_{name}")
        except Exception as e:
            self.logger.warning(f"截图失败: {e}")
    
    def get_last_login_result(self) -> Optional[str]:
        """获取上次登录结果"""
        return self._last_login_result
    
    def get_last_error_message(self) -> Optional[str]:
        """获取上次错误信息"""
        return self._last_error_message
    
    # ==================== 上下文管理器 ====================
    
    def __enter__(self):
        """进入上下文"""
        self.navigate_to_login()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        pass  # 不自动退出，保持登录状态


# ==================== 使用示例 ====================

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 使用改进版登录页面
        login_page = LoginPageImproved(page)
        
        # 方式1：直接使用
        login_page.login("admin", "admin123")
        
        # 方式2：上下文管理器
        with login_page as lp:
            lp.login("admin", "admin123")
            # 可以继续进行其他操作
        
        # 方式3：验证页面元素
        elements = login_page.verify_page_elements()
        print(f"页面元素验证: {elements}")
        
        # 退出登录
        login_page.logout()
        
        browser.close()
