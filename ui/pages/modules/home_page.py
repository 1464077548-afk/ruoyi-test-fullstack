from ui.pages.base_page import BasePage
from typing import List
import random


class HomePage(BasePage):
    """首页"""
    MENU_SYSMANAGE = 'home.menu_sysmanage'
    MENU_ITEM= 'home.menu_item'
    EL_MENU_ITEM = '.el-menu-item'

    USER_INFO = 'home.user_info'
    LOGOUT_BUTTON ='home.logout_button'

    CONFIRM_BUTTON = 'common.sys_prompt_confirm'
    CANCEL_BUTTON = 'common.sys_prompt_cancel'
    OPER_MESSAGE = 'home.oper_message'

    MENU_LIST = 'home.menu_list'

    def navigate_to(self,endpoint="/index"):
        """导航到首页"""
        self.goto(endpoint)
    def is_menu_visible(self) -> bool:
        """判断菜单是否可见"""
        return self.is_visible(self.MENU_LIST)
    
    def click_btn(self, btn_locator):
        """点击按钮"""
        if isinstance(btn_locator, str):
            self.click(btn_locator)
        else:
            # 如果已经是Locator对象，直接点击
            btn_locator.click(timeout=self.timeout)
     

    def get_welcome_message(self) -> str:
        """获取欢迎信息"""
        return self.get_text('home.welcome')
    
    def click_user_management(self):
        """点击用户管理"""
        self.click('home.user_management')
        self.wait_for_load_state()
    
    def click_role_management(self):
        """点击角色管理"""
        self.click('home.role_management')
        self.wait_for_load_state()
    
    def click_menu_management(self):
        """点击菜单管理"""
        self.click('home.menu_management')
        self.wait_for_load_state()
    
    def click_logout(self):
        """点击退出登录"""
        try:
            # 先点击用户信息，打开下拉菜单
            self.click('home.user_info')
            # 等待退出按钮出现
            self.wait_for_locator('home.logout', state="visible", timeout=10000)
            # 然后点击退出按钮
            self.click('home.logout')
            # 等待页面跳转
            self.wait_for_load_state()
        except Exception as e:
            # 如果点击失败，直接导航到登录页面
            self.goto("/login")
    
    def is_logout_success(self) -> bool:
        """判断退出登录是否成功"""
        # 检查是否跳转到登录页面
        return "/login" in self.page.url
    def get_all_menu_names(self) -> List[str]:
        """获取所有菜单名称"""
        try:
            #关闭界面上的所有弹窗
            self.press_key("Escape")
            #先展开所有菜单
            #1.获取所有可展开的元素
            expandable_items = self.page.get_by_role("menuitem").filter(has=self.page.locator("[aria-haspopup='true']")).all()
            #2.点击所有可展开的元素
            for item in expandable_items:
                item.click()
            # self.click(self.MENU_SYSMANAGE)
            # 等待菜单展开
            # 方法1: 尝试通过系统管理菜单获取
            menus = self.get_locator(self.MENU_ITEM).all()
            return menus
        except Exception as e:
            print(f"获取所有菜单名称失败: {e}")
            return []
        
   
    def random_click_menu(self,menu_items: List[str]):
        """随机点击菜单"""
        menu_items = self.get_all_menu_names()
        if not menu_items:
            print("未找到任何菜单，无法随机点击")
            return False
        # 随机点击10次菜单
        for _ in range(10):
            menu = random.choice(menu_items)
            menu.click()
            self.wait_for_load_state()
            # 验证页面未崩溃
            return not self.evaluate('window.jsErrors && window.jsErrors.length > 0')
    
    def go_to_user_manage(self):
        """导航到用户管理页面"""
        from ui.pages.modules.user_page import UserPage
        self.goto("/system/user")
        self.wait_for_load_state()
        return UserPage(self.page)
