from typing import Optional, Dict, Any
from playwright.sync_api import Page, Locator
from config.settings import Settings
from config.locator_map import LocatorMap
from common.logger import Logger
from playwright.sync_api import expect


class BasePage:
    """基础Page类"""
    
    def __init__(self, page: Page):
        """初始化"""
        self.page = page
        self.settings = Settings()
        self.locator_map = LocatorMap()
        self.logger = Logger(__name__)
        self.timeout = self.settings.UI_TIMEOUT
    
    @property
    def keyboard(self):
        """代理 Playwright page.keyboard"""
        return self.page.keyboard
    
    @property
    def context(self):
        """代理 Playwright page.context"""
        return self.page.context
    
    def content(self):
        """代理 Playwright page.content()"""
        return self.page.content()
    
    def wait_for_function(self, function, **kwargs):
        """代理 Playwright page.wait_for_function"""
        return self.page.wait_for_function(function, **kwargs)
    
    def wait_for_timeout(self, timeout):
        """代理 Playwright page.wait_for_timeout"""
        return self.page.wait_for_timeout(timeout)
    
    @property
    def url(self):
        """代理 Playwright page.url"""
        return self.page.url
    
    def get_by_role(self, role, **kwargs):
        """代理 Playwright page.get_by_role"""
        return self.page.get_by_role(role, **kwargs)
    
    def get_by_text(self, text, **kwargs):
        """代理 Playwright page.get_by_text"""
        return self.page.get_by_text(text, **kwargs)
    
    def get_by_label(self, text, **kwargs):
        """代理 Playwright page.get_by_label"""
        return self.page.get_by_label(text, **kwargs)
    
    def reload(self, **kwargs):
        """代理 Playwright page.reload"""
        return self.page.reload(**kwargs)
    
    def screenshot(self, **kwargs):
        """代理 Playwright page.screenshot"""
        return self.page.screenshot(**kwargs)
    
    def get_locator(self, locator_key: str, **kwargs) -> Locator:

        return self.locator_map.create_locator(self.page, locator_key, **kwargs)
    
    def goto(self, url: Optional[str] = None):
        """打开页面"""
        if url:
            if url.startswith('/'):
                # 相对路径，拼接完整URL
                target_url = f"{self.settings.BASE_URL.rstrip('/')}{url}"
            else:
                target_url = url
        else:
            target_url = self.settings.BASE_URL
        
        self.logger.info(f"打开页面: {target_url}")
        self.logger.debug(f"超时时间: {self.timeout}ms")
        
        # 确保使用正确的超时时间
        self.page.goto(target_url, timeout=self.timeout)

        return self.page
    def refresh_page(self):
        """刷新页面"""
        self.logger.info("刷新页面")
        self.page.reload(timeout=self.timeout)
        
    def click(self, locator_key: str, **kwargs):
        """点击元素"""
        self.logger.info(f"点击元素: {locator_key}")
        locator = self.get_locator(locator_key, **kwargs)
        # 添加 force=True 来处理遮罩层拦截点击的问题
        locator.click(timeout=self.timeout, force=True)
        return locator
    
    def fill(self, locator_key: str, value: str, retries: int = 2):
        """填写输入框（带重试机制）"""
        self.logger.info(f"填写元素: {locator_key}, 值: {value}")
        last_error = None
        
        for attempt in range(retries + 1):
            try:
                locator = self.get_locator(locator_key)
                # 先等待元素可见
                locator.wait_for(state="visible", timeout=10000)
                # 然后填写
                locator.fill(value, timeout=10000)
                return locator
            except Exception as e:
                last_error = e
                if attempt < retries:
                    print(f"填写元素失败，尝试重试 ({attempt + 1}/{retries}): {locator_key}")
                    self.page.wait_for_timeout(1000)
                    continue
                else:
                    self.logger.error(f"填写元素失败：{locator_key}，错误：{last_error}")
                    raise last_error
    
    def get_text(self, locator_key: str) -> str:
        """获取元素文本"""
        locator = self.get_locator(locator_key)
        return locator.text_content(timeout=self.timeout).strip()
    
    def get_value(self, locator_key: str) -> str:
        """获取输入框值"""
        locator = self.get_locator(locator_key)
        return locator.input_value(timeout=self.timeout)
    def get_attribute(self, locator_key: str, attribute: str) -> str:
        """获取元素属性"""
        locator = self.get_locator(locator_key)
        return locator.get_attribute(attribute)
    
    def is_visible(self, locator_key: str, timeout: int = None) -> bool:
        """判断元素是否可见"""
        locator = self.get_locator(locator_key)
        wait_timeout = timeout or self.timeout
        try:
            return locator.is_visible(timeout=wait_timeout)
        except Exception:
            try:
                # 如果匹配到多个元素，只检查第一个
                return locator.first.is_visible(timeout=wait_timeout)
            except Exception:
                return False
    
    def is_enabled(self, locator_key: str) -> bool:
        """判断元素是否可用"""
        locator = self.get_locator(locator_key)
        return locator.is_enabled(timeout=self.timeout)
    
    def wait_for_load_state(self, state: str = 'load', timeout: Optional[int] = None):
        """等待页面加载完成"""
        wait_timeout = timeout or self.timeout
        self.page.wait_for_load_state(state, timeout=wait_timeout)
    
    def wait_for_locator(self, locator_key: str, state="visible",timeout: Optional[int] = None):
        """等待元素出现"""
        try:
            locator = self.get_locator(locator_key)
            wait_timeout = timeout or self.timeout
            locator.wait_for(timeout=wait_timeout, state=state)
        except Exception as e:
            print(f"等待元素失败: {locator_key}, 错误: {e}")
            # 如果等待失败，尝试刷新页面
            self.page.reload()
            # 再次尝试等待
            locator = self.get_locator(locator_key)
            locator.wait_for(timeout=wait_timeout, state=state)
    
    def take_screenshot(self, path: str):
        """截图"""
        self.page.screenshot(path=path)
    
    def switch_to_frame(self, locator_key: str):
        """切换到iframe"""
        locator = self.get_locator(locator_key)
        frame = locator.content_frame()
        if not frame:
            raise ValueError(f"未找到iframe: {locator_key}")
        return frame
    
    def press_key(self, key: str):
        """模拟按键"""
        self.logger.info(f"模拟按键: {key}")
        self.page.keyboard.press(key)
    
    def execute_script(self, script: str, *args) -> Any:
        """执行JavaScript"""
        return self.page.evaluate(script, *args)
    
    def scroll_to(self, locator_key: str):
        """滚动到元素"""
        locator = self.get_locator(locator_key)
        locator.scroll_into_view_if_needed(timeout=self.timeout)
    
    def assert_toast_message(self, message: str, locator_key: str = 'common.toast_message'):
        """Toast 断言"""
        self.logger.info(f"断言Toast消息: {message}")
        self.wait_for_locator(locator_key, state="visible")
        actual_message = self.get_text(locator_key)
        assert message in actual_message, f"期望Toast消息: {message}, 实际消息: {actual_message}"
        # 等待Toast消失
        self.wait_for_locator(locator_key, state="detached")
    
    def confirm_dialog(self, confirm_button_locator: str = 'common.confirm_button'):
        """确认弹窗"""
        self.logger.info("确认弹窗")
        self.wait_for_locator(confirm_button_locator, state="visible")
        self.click(confirm_button_locator)
    
    def close_dialog(self, cancel_button_locator: str = 'common.cancel_button'):
        """关闭弹窗"""
        self.logger.info("关闭弹窗")
        self.wait_for_locator(cancel_button_locator, state="visible")
        self.click(cancel_button_locator)
    
    def select_option(self, select_locator: str, option_locator: str):
        """选择下拉选项"""
        self.logger.info("选择下拉选项")
        self.click(select_locator)
        self.wait_for_locator(option_locator, state="visible")
        self.click(option_locator)
    
    def hover(self, locator_key: str):
        """悬停元素"""
        self.logger.info(f"悬停元素: {locator_key}")
        locator = self.get_locator(locator_key)
        locator.hover(timeout=self.timeout)
    
    def double_click(self, locator_key: str):
        """双击元素"""
        self.logger.info(f"双击元素: {locator_key}")
        locator = self.get_locator(locator_key)
        locator.dblclick(timeout=self.timeout)
    
    def right_click(self, locator_key: str):
        """右键点击元素"""
        self.logger.info(f"右键点击元素: {locator_key}")
        locator = self.get_locator(locator_key)
        locator.click(button="right", timeout=self.timeout)
    
    def drag_and_drop(self, source_locator: str, target_locator: str):
        """拖拽元素"""
        self.logger.info(f"拖拽元素: {source_locator} 到 {target_locator}")
        source = self.get_locator(source_locator)
        target = self.get_locator(target_locator)
        source.drag_to(target, timeout=self.timeout)
    
    def wait_for_selector(self, selector: str, state: str = "visible"):
        """等待选择器"""
        self.logger.info(f"等待选择器: {selector}")
        self.page.wait_for_selector(selector, state=state, timeout=self.timeout)

    def pause(self):
        """暂停执行"""
        self.logger.info("暂停执行")
        self.page.pause()
    
    def locator(self, selector: str):
        """获取元素定位器（直接使用Playwright的locator方法）"""
        return self.page.locator(selector)
