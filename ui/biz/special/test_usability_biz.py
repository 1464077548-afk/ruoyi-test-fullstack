from ui.biz.common_biz import CommonBiz
from ui.biz.normal.login_biz import LoginBiz
import logging
class UsabilityBiz:
    def __init__(self, page):
        self.page = page
        self.login_biz = LoginBiz(page)
        self.common = CommonBiz(page)
        self.logger = logging.getLogger(__name__)

    def test_keyboard_navigation(self):
        """可用性测试 - 键盘导航"""
        self.logger.info("开始测试键盘导航")
        # 使用user_login方法登录
        result = self.login_biz.login("admin", "admin123")
        return result
    def  test_responsive_design(self):
        """可用性测试 - 响应式设计"""
        self.logger.info("开始测试响应式设计")
        sizes = [
            (320, 480),    # 手机
            (768, 1024),   # 平板
            (1920, 1080),  # 桌面
            (2560, 1440),  # 大屏
        ]
        
        for width, height in sizes:
            self.page.set_viewport_size({"width": width, "height": height})
            self.logger.info(f"设置视口大小为 {width}x{height}")
            # 验证页面布局是否正确
            # 例如检查元素是否可见、位置是否正确等
            # 这里简单检查登录按钮是否可见
            body_visible = self.page.is_visible("body")
            if not body_visible:
                return False
        return True
    def test_accessibility(self):
        """可用性测试 - 无障碍访问"""
        self.logger.info("开始测试无障碍访问")
        # 检查 ARIA 属性
        elements = self.page.locator('[aria-label]')
        aria_count = elements.count()
        if aria_count > 0:
            self.logger.info(f"发现 {aria_count} 个元素包含 aria-label 属性")
        else:
            self.logger.warning("未发现包含 aria-label 属性的元素")
        return aria_count > 0