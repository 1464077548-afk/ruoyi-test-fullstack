from ui.pages.base_page import BasePage


class HeaderComponent(BasePage):
    """顶部导航组件"""

    def click_user_avatar(self, avatar_locator: str):
        """点击用户头像"""
        self.click(avatar_locator)

    def click_logout(self, logout_locator: str):
        """点击退出登录"""
        self.click(logout_locator)

    def click_notification(self, notification_locator: str):
        """点击通知"""
        self.click(notification_locator)

    def click_home(self, home_locator: str):
        """点击首页"""
        self.click(home_locator)
