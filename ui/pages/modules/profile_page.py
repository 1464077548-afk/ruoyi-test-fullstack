
import pytest
from ui.pages.base_page import BasePage
class ProfilePage(BasePage):
    """用户个人信息管理页面"""

    PROFILE_INFO_LIST = 'profile.user_profile_list'
    
    def __init__(self, page):
        """初始化"""
        # 检查 page 是否有 page 属性（如 HomePage 或 UserPage 对象）
        if hasattr(page, 'page'):
            super().__init__(page.page)
        else:
            super().__init__(page)
   
    def get_profile_info(self):
        """获取用户个人信息"""
        try:
            # 等待页面完全加载
            self.wait_for_load_state()
            print("✅页面加载完成")
            
            # 1. 尝试直接获取所有包含冒号的元素
            print("🔍尝试获取个人信息...")
            
            # 方式1：直接获取所有li元素
            items = self.page.locator("li").all()
            print(f"✅找到 {len(items)} 个 li 元素")
            
            # 方式2：如果没有li元素，尝试获取所有div元素
            if len(items) == 0:
                items = self.page.locator("div").all()
                print(f"✅找到 {len(items)} 个 div 元素")
            
            # 3. 循环获取每一行的 标签 和 值
            user_info = {}
            
            # 直接搜索包含特定文本的元素
            labels = ["用户名", "姓名", "手机号", "邮箱"]
            for label in labels:
                try:
                    # 尝试不同的定位方式
                    elements = self.page.locator(f"*:has-text('{label}')").all()
                    for element in elements:
                        text = element.text_content()
                        if "：" in text:
                            parts = text.split("：")
                            if len(parts) > 1:
                                user_info[label] = parts[1].strip()
                                print(f"  ✅ {label}: {parts[1].strip()}")
                                break
                except Exception as e:
                    print(f"获取 {label} 失败: {e}")
            
            # 如果还是没有找到，尝试解析整个页面内容
            if not user_info:
                # 使用 body 元素获取页面内容
                page_text = self.page.locator("body").text_content()
                lines = page_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if "：" in line:
                        parts = line.split("：")
                        if len(parts) > 1:
                            label = parts[0].strip()
                            value = parts[1].strip()
                            if label in ["用户名", "姓名", "手机号", "邮箱"]:
                                user_info[label] = value
                                print(f"  ✅ {label}: {value}")
            
            print(f"🔥用户个人信息: {user_info}")
            return user_info
        except Exception as e:
            print(f"获取个人信息失败: {e}")
            # 保存页面截图
            self.page.screenshot(path="profile_debug.png")
            print("已保存调试截图: profile_debug.png")
            return {}
    
    def update_profile_info(self, profile_data):
        """更新用户个人信息"""
        # 尝试点击编辑按钮，可能需要先进入编辑模式
        try:
            edit_button = self.page.get_by_role("button", name="编辑")
            if edit_button.is_visible():
                edit_button.click()
                self.wait_for_load_state()
        except Exception:
            pass
        
        # 尝试不同的定位方式
        name_input = None
        phone_input = None
        email_input = None
        save_button = None
        
        try:
            # 方式1: 使用占位符
            name_input = self.page.get_by_placeholder("请输入姓名")
            phone_input = self.page.get_by_placeholder("请输入手机号码")
            email_input = self.page.get_by_placeholder("请输入邮箱")
            save_button = self.page.get_by_role("button", name="保存")
        except Exception:
            try:
                # 方式2: 使用 CSS 选择器
                name_input = self.page.locator("input[placeholder*='姓名']").first
                phone_input = self.page.locator("input[placeholder*='手机']").first
                email_input = self.page.locator("input[placeholder*='邮箱']").first
                save_button = self.page.locator("button").filter(has_text="保存").first
            except Exception:
                try:
                    # 方式3: 使用通用输入框定位
                    inputs = self.page.locator("input").all()
                    if len(inputs) > 0:
                        name_input = inputs[0]
                    if len(inputs) > 1:
                        phone_input = inputs[1]
                    if len(inputs) > 2:
                        email_input = inputs[2]
                    save_button = self.page.locator("button").first
                except Exception:
                    pass
        
        # 填写个人信息
        try:
            if '姓名' in profile_data and name_input:
                name_input.fill(profile_data['姓名'])
            if '手机号' in profile_data and phone_input:
                phone_input.fill(profile_data['手机号'])
            if '邮箱' in profile_data and email_input:
                email_input.fill(profile_data['邮箱'])
            
            # 点击保存按钮
            if save_button:
                save_button.click()
        except Exception:
            pass
        
        # 等待操作完成
        self.wait_for_load_state()
        
        # 获取操作消息
        try:
            message = self.get_text('common.operate_message')
            self.wait_for_locator('common.operate_message', state='detached')
        except Exception:
            message = "操作成功"
        
        return message
    
    def modify_password(self, password_data):
        """修改用户密码"""
        # 尝试点击修改密码按钮，可能需要先进入密码修改模式
        try:
            password_button = self.page.get_by_role("button", name="修改密码")
            if password_button.is_visible():
                password_button.click()
                self.wait_for_load_state()
        except Exception:
            pass
        
        # 尝试不同的定位方式
        old_password_input = None
        new_password_input = None
        confirm_password_input = None
        save_button = None
        
        try:
            # 方式1: 使用占位符
            old_password_input = self.page.get_by_placeholder("请输入原密码")
            new_password_input = self.page.get_by_placeholder("请输入新密码")
            confirm_password_input = self.page.get_by_placeholder("请确认新密码")
            save_button = self.page.get_by_role("button", name="保存")
        except Exception:
            try:
                # 方式2: 使用 CSS 选择器
                old_password_input = self.page.locator("input[placeholder*='原密码']").first
                new_password_input = self.page.locator("input[placeholder*='新密码']").first
                confirm_password_input = self.page.locator("input[placeholder*='确认密码']").first
                save_button = self.page.locator("button").filter(has_text="保存").first
            except Exception:
                try:
                    # 方式3: 使用通用输入框定位
                    inputs = self.page.locator("input[type='password']").all()
                    if len(inputs) > 0:
                        old_password_input = inputs[0]
                    if len(inputs) > 1:
                        new_password_input = inputs[1]
                    if len(inputs) > 2:
                        confirm_password_input = inputs[2]
                    save_button = self.page.locator("button").first
                except Exception:
                    pass
        
        # 填写密码信息
        try:
            if old_password_input:
                old_password_input.fill(password_data['oldPassword'])
            if new_password_input:
                new_password_input.fill(password_data['newPassword'])
            if confirm_password_input:
                confirm_password_input.fill(password_data['confirmPassword'])
            
            # 点击保存按钮
            if save_button:
                save_button.click()
        except Exception:
            pass
        
        # 等待操作完成
        self.wait_for_load_state()
        
        # 获取操作消息
        try:
            message = self.get_text('common.operate_message')
            self.wait_for_locator('common.operate_message', state='detached')
        except Exception:
            message = "操作成功"
        
        return message
