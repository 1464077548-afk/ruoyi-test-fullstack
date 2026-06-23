"""公共 UI 组件（顶部导航、侧边菜单、分页、弹窗）"""
from ui.pages.base_page import BasePage
class MenuItem(BasePage):
    """菜单项"""
    ALL_EXPAND_MENU = 'home.all_expand_menu'
    USER_MANAGEMENT = 'home.user_management'
    ROLE_MANAGEMENT = 'home.role_management'
    MENU_MANAGEMENT = 'home.menu_management'

    USER_MANAGEMENT_TAB = 'home.user_management_tab'
    ROLE_MANAGEMENT_TAB = 'home.role_management_tab'
    MENU_MANAGEMENT_TAB = 'home.menu_management_tab'
    PROFILE_MANAGEMENT_TAB = 'home.profile_management_tab'

    USER_INFO = 'home.user_info'
    PROFILE_INFO_BUTTON ='home.profile_info_button'
    
    def __init__(self, page):
        """初始化"""
        # 检查 page 是否有 page 属性（如 LoginPage 或 UserPage 对象）
        if hasattr(page, 'page'):
            super().__init__(page.page)
        else:
            super().__init__(page)
    def go_to_module(self, module_name: str):
        """导航到指定模块"""
        # 使用 first() 方法只点击第一个匹配的元素，避免匹配到面包屑导航中的链接
        locator = self.get_locator(module_name).first
        locator.click(timeout=self.timeout)
        self.wait_for_load_state()
        return self
    def expand_all_menu(self):
        """展开所有菜单"""
        # 使用 first() 方法只点击第一个匹配的元素
        locator = self.get_locator(self.ALL_EXPAND_MENU).first
        locator.click(timeout=self.timeout)
        self.wait_for_load_state()
        return self
    def goto_user_manage(self):
        """导航到用户管理模块"""
        # 扩展所有菜单
        self.expand_all_menu()
        # 导航到用户管理模块
        self.go_to_module(self.USER_MANAGEMENT)
        # 验证是否导航到用户管理模块
        result = self.is_navigated_to_module(self.USER_MANAGEMENT_TAB, "/user")
        return result

    def goto_role_manage(self):
        """导航到角色管理模块"""
        self.go_to_module(self.ROLE_MANAGEMENT)
        #验证是否导航到角色管理模块
        result = self.is_navigated_to_module(self.ROLE_MANAGEMENT_TAB, "/role")
        return result
    def goto_menu_manage(self):
        """导航到菜单管理模块"""
        self.go_to_module(self.MENU_MANAGEMENT)
        #验证是否导航到菜单管理模块
        result = self.is_navigated_to_module(self.MENU_MANAGEMENT_TAB, "/menu")
        return result
    def goto_profile_manage(self):
        """导航到用户个人信息管理模块"""
        self.click(self.USER_INFO)
        self.go_to_module(self.PROFILE_INFO_BUTTON)
        #验证是否导航到用户个人信息管理模块
        result = self.is_navigated_to_module(self.PROFILE_MANAGEMENT_TAB, "/profile")
        return result
    def is_navigated_to_module(self , menu_name: str,endpoint: str):
        """验证是否导航到指定模块"""
        locator = self.get_locator(menu_name)
        #验证url正确跳转
        current_url = self.page.url
        print(f"🏹当前URL: {current_url}")
        if endpoint in current_url and locator.is_visible():
            return self.page.url
        else:
            return False
    
    def logout(self):
        """退出登录"""
        try:
            # 尝试点击用户信息按钮
            try:
                self.click(self.USER_INFO)
            except Exception as e:
                print(f"点击用户信息按钮失败，尝试刷新页面: {e}")
                self.page.reload()
                self.wait_for_load_state()
                self.click(self.USER_INFO)
            
            # 点击退出登录按钮
            try:
                logout_button = self.page.get_by_text("退出登录")
                logout_button.click(timeout=10000)
            except Exception as e:
                print(f"点击退出登录按钮失败，尝试其他定位方式: {e}")
                # 尝试使用CSS选择器
                logout_button = self.page.locator(".el-dropdown-menu__item").filter(has_text="退出登录")
                logout_button.click(timeout=10000)
            
            self.wait_for_load_state()
        except Exception as e:
            print(f"退出登录失败: {e}")
            # 尝试直接导航到登录页面
            self.goto("/login")

# 为了兼容性，添加 MenuComponent 别名
MenuComponent = MenuItem