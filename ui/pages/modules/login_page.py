from ast import And
from ui.pages.base_page import BasePage
from config.settings import Settings


class LoginPage(BasePage):
    """登录页面"""
    #==============公共定位器================
    SYS_PROMPT = 'common.sys_prompt'
    SYS_PROMPT_CONFIRM = 'common.sys_prompt_confirm'
    USER_LOGIN_PROMPT = 'common.user_login_prompt'
    USER_LOGIN_PROMPT_CANCEL = 'common.user_login_prompt_cancel'

    #==============元素定位器================
    USERNAME_INPUT = 'login.username_input'
    PASSWORD_INPUT = 'login.password_input'
    CAPTCHA_INPUT = 'login.captcha_input'
    SUBMIT_BUTTON = 'login.submit_button'
    ERROR_MESSAGE = 'login.error_message'
    USER_INFO = 'home.user_info'
    LOGOUT_BUTTON ='home.logout_button'
    INDEX ='home.menu'
    REMEMBER_ME = 'login.remember_me'
    CAPTCHA_IMAGE = 'login.captcha_image'
    
    def navigate_to_login(self):
        """导航到登录页面"""
        self.goto("/login")
    def click_submit_button(self):
        """点击登录按钮"""
        self.click(self.SUBMIT_BUTTON)

    def login(self, username: str, password: str,captcha:str ='skip_captcha',is_rember_me=False,auto_refresh_captcha=False):
        """登录操作"""
        print(f"开始登录用户: {username}")
        
        # 先检查是否已经在登录状态
        current_url = self.page.url
        print(f"当前URL: {current_url}")
        if "/index" in current_url or ("/login" not in current_url and self.is_visible(self.USER_INFO, timeout=3000)):
            print("✅用户已登录，无需重复登录")
            return "登录成功"
        
        # 打开登录页面
        self.goto("/login")
        
        # 等待登录页面完全加载（使用domcontentloaded，更适合SPA）
        self.wait_for_load_state("domcontentloaded")
        print(f"登录页面DOM加载完成，当前URL: {self.page.url}")
        
        # 等待网络请求完成
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            print("网络请求完成")
        except:
            print("网络请求等待超时，继续执行")
        
        # 截图保存，以便查看页面的实际情况
        self.page.screenshot(path=f"login_page_before_login_{username}.png")
        print("已保存登录页面截图")
        
        try:
            # 等待用户名输入框可见（增加超时时间）
            print("等待用户名输入框可见...")
            self.wait_for_locator(self.USERNAME_INPUT, state="visible", timeout=30000)
            print("用户名输入框可见")
            
            # 等待密码输入框可见
            self.wait_for_locator(self.PASSWORD_INPUT, state="visible", timeout=10000)
            print("密码输入框可见")
            
            # 清空并填写用户名
            self.fill(self.USERNAME_INPUT, "")
            print("清空用户名输入框")
            self.fill(self.USERNAME_INPUT, username)
            print(f"填写用户名: {username}")
            
            # 清空并填写密码
            self.fill(self.PASSWORD_INPUT, "")
            print("清空密码输入框")
            self.fill(self.PASSWORD_INPUT, password)
            print("填写密码")
            
            # 自动刷新验证码
            if auto_refresh_captcha:
                print("刷新验证码...")
                self.click(self.CAPTCHA_IMAGE)
                # 等待验证码刷新完成
                self.wait_for_attribute_change(self.CAPTCHA_IMAGE, "src", "")
                print("验证码刷新完成")
            
            # 填写验证码（只有当验证码输入框可见时）
            if self.is_visible(self.CAPTCHA_INPUT, timeout=3000):
                self.fill(self.CAPTCHA_INPUT, captcha)
                print(f"填写验证码: {captcha}")
            
            if is_rember_me:
                self.check_remember_me()
            
            # 点击登录按钮
            print("点击登录按钮...")
            self.click(self.SUBMIT_BUTTON)
            print("登录按钮点击完成")
            
            # 等待页面加载
            self.wait_for_load_state("domcontentloaded", timeout=30000)
            print("登录后页面DOM加载完成")
            
            # 等待网络请求完成
            try:
                self.page.wait_for_load_state("networkidle", timeout=15000)
                print("登录后网络请求完成")
            except:
                print("登录后网络请求等待超时")
            
            # 处理安全提示弹窗
            if self.is_visible(self.USER_LOGIN_PROMPT, timeout=5000):
                self.click(self.USER_LOGIN_PROMPT_CANCEL)
                self.wait_for_load_state()
            
            # 检查登录是否成功
            if self.is_login_success():
                print("✅登录成功")
                return "登录成功"
            else:
                # 尝试获取错误信息
                message = self.get_error_message()
                print(f"获取到的错误信息: {message}")
                self.logger.error(f"登录失败，错误信息: {message}")
                print(f"登录失败，错误信息: {message}")
                return message
        except Exception as e:
            print(f"登录过程出错: {e}")
            import traceback
            traceback.print_exc()
            # 截图保存
            self.page.screenshot(path=f"login_error_{username}.png")
            print("已保存登录错误截图")
        
            print("登录失败")
            return "登录失败"
    

    def fill_username(self, username: str):
        """填写用户名"""
        self.fill(self.USERNAME_INPUT, username)
    def get_username_locator(self):
        """获取用户名输入框定位器"""
        return self.get_locator(self.USERNAME_INPUT)
    def get_password_locator(self):
        """获取密码输入框定位器"""
        return self.get_locator(self.PASSWORD_INPUT)
    def fill_password(self, password: str):
        """填写密码"""
        self.fill(self.PASSWORD_INPUT, password)
    
    def fill_captcha(self, captcha: str):
        """填写验证码"""
        self.fill(self.CAPTCHA_INPUT, captcha)
    def click_remember_me(self):
        """点击记住我"""
        self.click(self.REMEMBER_ME)
    def click_user_info(self, timeout: int = 10000):
        """点击用户信息"""
        try:
            # 先关闭安全提示弹窗
            if self.is_visible_user_login_prompt():
                self.click_user_login_prompt_cancel()
                # 等待弹窗消失
                self.wait_for_locator(self.USER_LOGIN_PROMPT, state="detached", timeout=3000)
            
            # 点击用户信息
            self.click(self.USER_INFO)
            print("点击用户信息")
            return True
        except Exception as e:
            print(f"点击用户信息失败: {e}")
            # 尝试关闭安全提示弹窗
            try:
                if self.is_visible_user_login_prompt():
                    self.click_user_login_prompt_cancel()
                    # 等待弹窗消失
                    self.wait_for_locator(self.USER_LOGIN_PROMPT, state="detached", timeout=3000)
                self.click(self.USER_INFO)
                return True
            except Exception as e2:
                print(f"再次点击用户信息失败: {e2}")
                # 尝试直接导航到登录页面
                self.goto("/login")
                return False
    def click_logout(self):
        """点击退出登录"""
        self.click(self.LOGOUT_BUTTON)
        self.page.wait_for_timeout(3000)
        print("点击退出登录按钮")



    def is_visible_user_login_prompt(self, timeout: int = 3000) -> bool:
        """判断用户登录弹窗是否可见"""
        try:
            return self.is_visible(self.USER_LOGIN_PROMPT)
        except:
            return False
    def click_user_login_prompt_cancel(self):
        """点击用户登录弹窗取消按钮"""
        self.click(self.USER_LOGIN_PROMPT_CANCEL)
  
    def username_is_visible(self, timeout: int = 10000) -> bool:
        """判断用户名输入框是否可见"""
        try:
            self.wait_for_locator(self.USERNAME_INPUT, state="visible", timeout=timeout)
            return True
        except:
            return False
    def password_is_visible(self, timeout: int = 10000) -> bool:
        """判断密码输入框是否可见"""
        try:
            self.wait_for_locator(self.PASSWORD_INPUT, state="visible", timeout=timeout)
            return True
        except:
            return False
    def submit_button_is_visible(self, timeout: int = 10000) -> bool:
        """判断登录按钮是否可见"""
        try:
            self.wait_for_locator(self.SUBMIT_BUTTON, state="visible", timeout=timeout)
            return True
        except:
            return False
    def get_error_message(self) -> str:
        """获取登录错误信息"""
        # 尝试多种方式获取错误信息
        error_message = ""
        
        # 方式1：使用ERROR_MESSAGE定位器（前端验证错误）
        try:
            if self.is_visible(self.ERROR_MESSAGE):
                message = self.get_text(self.ERROR_MESSAGE)
                if message and not self._is_internal_error(message):
                    print(f"⚠️登录失败，获取登录错误信息: {message}")
                    self.logger.info(f"⚠️登录失败，登录错误信息: {message}")
                    return message
        except Exception as e:
            print(f"获取错误信息方式1失败: {e}")
        
        # 方式2：尝试获取弹窗提示（系统提示）
        try:
            if self.is_visible(self.SYS_PROMPT):
                message = self.get_text(self.SYS_PROMPT)
                if message and not self._is_internal_error(message):
                    print(f"⚠️登录失败，获取弹窗错误信息: {message}")
                    self.logger.info(f"⚠️登录失败，弹窗错误信息: {message}")
                    # 点击确认按钮关闭弹窗
                    self.click(self.SYS_PROMPT_CONFIRM)
                    return message
        except Exception as e:
            print(f"获取错误信息方式2失败: {e}")
        
        # 方式3：尝试通过CSS选择器获取所有可能的错误信息元素
        try:
            # 等待页面加载完成
            self.page.wait_for_load_state()
            # 尝试常见的错误信息选择器
            error_selectors = [
                ".el-form-item__error",  # 表单验证错误
                ".el-message__content",  # 消息提示错误
                ".el-alert__title",      # 警告框错误
                ".alert",                 # 通用警告
                ".el-message-box__content" # 消息框内容
            ]
            for selector in error_selectors:
                try:
                    error_elements = self.page.locator(selector)
                    if error_elements.count() > 0:
                        message = error_elements.first.text_content().strip()
                        if message and not self._is_internal_error(message):
                            print(f"⚠️登录失败，通过CSS选择器获取错误信息: {message}")
                            self.logger.info(f"⚠️登录失败，CSS选择器错误信息: {message}")
                            return message
                except:
                    pass
        except Exception as e:
            print(f"获取错误信息方式3失败: {e}")
        
        # 方式4：尝试获取页面上所有可能的错误文本（谨慎使用）
        try:
            # 等待一小段时间让错误信息有机会显示
            self.page.wait_for_timeout(2000)
            # 搜索包含错误关键词的元素
            error_keywords = ["用户名或密码错误", "验证码错误", "密码错误", "用户名不存在", "账号已停用"]
            for keyword in error_keywords:
                try:
                    error_elements = self.page.locator(f"text={keyword}")
                    if error_elements.count() > 0:
                        message = error_elements.first.text_content().strip()
                        if message:
                            print(f"⚠️登录失败，通过关键词获取错误信息: {message}")
                            self.logger.info(f"⚠️登录失败，关键词错误信息: {message}")
                            return message
                except:
                    pass
        except Exception as e:
            print(f"获取错误信息方式4失败: {e}")
        
        # 所有尝试都失败，返回空字符串
        print("⚠️登录失败，未获取到错误信息")
        return error_message
    
    def _is_internal_error(self, message: str) -> bool:
        """判断是否为内部错误信息（不应作为登录失败原因返回）"""
        internal_error_keywords = [
            "空指针异常", "空指针", "NullPointerException", 
            "无法获取错误信息", "内部错误", "系统异常"
        ]
        for keyword in internal_error_keywords:
            if keyword in message:
                print(f"检测到内部错误信息，跳过: {message}")
                return True
        return False
    
    def wait_for_attribute_change(self, locator_key: str, attribute: str, old_value: str, timeout: int = 10000):
        """等待元素属性变化"""
        try:
            # 简化实现，使用简单的轮询
            import time
            start_time = time.time()
            locator = self.get_locator(locator_key)
            
            while time.time() - start_time < timeout / 1000:
                new_value = locator.get_attribute(attribute)
                if new_value != old_value:
                    return
                time.sleep(0.1)
        except Exception as e:
            print(f"等待属性变化失败: {e}")
    
    def is_login_success(self) -> bool:
        """判断登录是否成功"""
        self.wait_for_load_state()
        try:
            # 检查URL是否不再是登录页面
            print(f"当前URL: {self.page.url}")
            # 等待几秒钟让页面完全跳转
            self.page.wait_for_timeout(2000)
            
            # 检查是否跳转到了首页或其他非登录页面
            if "/login" in self.page.url:
                print("URL仍然是登录页面，登录失败")
                return False
            
            # 检查是否跳转到了首页
            if "/index" in self.page.url:
                print("URL包含/index，登录成功")
                return True
            
            # 检查是否显示用户信息或菜单（作为备用检查）
            user_info_visible = self.is_visible(self.USER_INFO, timeout=10000)
            print(f"用户信息可见性: {user_info_visible}")
            
            # 检查是否显示首页菜单
            menu_visible = self.is_visible(self.INDEX, timeout=5000)
            print(f"首页菜单可见性: {menu_visible}")
            
            # 如果URL不是登录页面，或者用户信息或菜单可见，都认为登录成功
            return "/login" not in self.page.url or user_info_visible or menu_visible
       
        except Exception as e:
            print(f"检查登录成功失败: {e}")
            # 如果发生异常，但URL已经不是登录页面，也认为登录成功
            result = "/login" not in self.page.url
            print(f"异常情况下的登录结果: {result}")
            return result
               
    def verify_captcha_image(self):
        """验证验证码图片显示"""
        self.navigate_to_login()
        return self.is_visible(self.CAPTCHA_IMAGE)

    def verify_captcha_refresh(self):
        """验证验证码刷新"""
        self.navigate_to_login()
        if self.is_visible(self.CAPTCHA_IMAGE):
            # 获取初始src
            src = self.get_attribute(self.CAPTCHA_IMAGE, "src")
            print(f"初始验证码src: {src}")
            
            # 点击刷新
            self.click(self.CAPTCHA_IMAGE)
            print("点击验证码图片进行刷新")
            
            # 等待一段时间让验证码刷新
            self.page.wait_for_timeout(2000)
            
            # 获取新的src
            new_src = self.get_attribute(self.CAPTCHA_IMAGE, "src")
            print(f"刷新后验证码src: {new_src}")
            
            # 验证src是否变化
            result = src != new_src
            print(f"验证码刷新结果: {result}")
            return result
        else:
            print("验证码图片不可见")
            self.wait_for_timeout(2000)
            print("等待2秒后检查验证码图片是否可见")
            return self.verify_captcha_image()
    
    def is_login_page_visible(self) -> bool:
        """判断登录页面是否可见"""
        try:
            self.wait_for_load_state()
            # 检查登录页面的关键元素是否可见
            username_visible = self.is_visible(self.USERNAME_INPUT)
            password_visible = self.is_visible(self.PASSWORD_INPUT)
            submit_visible = self.is_visible(self.SUBMIT_BUTTON)
            return username_visible and password_visible and submit_visible
        except Exception as e:
            print(f"检查登录页面可见性失败: {e}")
            return False
    
    def logout(self):
        """退出登录"""
        print("开始退出登录...")
        try:
            # 点击退出登录按钮
            result = self.click(self.USER_INFO)
            if not result:
                self.logger.warning("点击用户信息失败")
                return "点击用户信息失败"
            self.click(self.LOGOUT_BUTTON)
            print("✅点击退出登录按钮")
            
            # 等待退出登录弹窗出现
            self.wait_for_locator(self.SYS_PROMPT, state="visible", timeout=10000)
            print("退出登录弹窗可见")
            
            # 点击确认退出按钮
            self.click(self.SYS_PROMPT_CONFIRM)
            print("点击确认退出按钮")
            
            # 等待页面加载完成
            self.wait_for_load_state()
            print("退出登录后页面加载完成")
            
            # 检查是否跳转到登录页面
            if self.is_login_page_visible():
                print("✅退出登录成功，跳转到登录页面")
                return "退出登录成功"
            else:
                print("⚠️退出登录失败，未跳转到登录页面")
                return "退出登录失败"
                
        except Exception as e:
            print(f"退出登录过程出错: {e}")
            import traceback
            traceback.print_exc()
            # 截图保存
            self.page.screenshot(path="logout_error.png")
           
    def session_timeout(self):
        """模拟会话超时"""
        print("模拟会话超时...")
        # 清除所有cookies
        self.page.context.clear_cookies()
        print("✅会话已模拟超时")
    def is_login_page(self) -> bool:
        """判断是否在登录页面"""
        self.wait_for_load_state()
        return "/login" in self.page.url
    
    def go_to_user_manage(self):
        """导航到用户管理页面"""
        from ui.pages.modules.user_page import UserPage
        self.goto("/system/user")
        self.wait_for_load_state()
        return UserPage(self.page)