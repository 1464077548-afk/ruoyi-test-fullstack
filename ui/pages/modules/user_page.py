from typing import List, Optional
from ui.pages.modules.base_module_page import BaseModulePage
from config.settings import Settings


class UserPage(BaseModulePage):
    """用户管理页面"""
    def __init__(self, page):
        super().__init__(page)
        self.settings = Settings()
        #==============搜索区域元素定位器================
        self.SEARCH_INPUT = 'user.search_input'
        self.USER_PHONE_SEARCH_INPUT = 'user.phone_search_input'
        self.USER_STATUS_SEARCH_INPUT = 'user.search_status'
        self.USER_STATUS_NORMAL_SELECTOR = 'user.search_status_normal'
        self.USER_STATUS_DISABLED_SELECTOR = 'user.search_status_disabled'
        self.SEARCH_BUTTON = 'common.search_button'
        self.SEARCH_RESET_BUTTON = 'common.search_reset_button'
        
        #==============操作按钮区域元素定位器================
        # 新增用户按钮
        self.USER_ADD_BUTTON = 'common.add_button'
        self.USER_MODIFY_BUTTON = 'common.modify_button'
        self.USER_BATCH_DELETE_BUTTON = 'common.batch_delete_button'
        self.USER_IMPORT_BUTTON = 'common.import_button'
        self.USER_EXPORT_BUTTON = 'common.export_button'
        #====================新增元素定位器==================
        # 用户名输入框
        self.USER_NAME_INPUT = 'user.username'
        # 昵称输入框
        self.USER_NICKNAME_INPUT = 'user.nickName'
        # 密码输入框
        self.USER_PASSWORD_INPUT = 'user.password'
        # 邮箱输入框
        self.USER_EMAIL_INPUT = 'user.email'
        # 手机号输入框
        self.USER_PHONE_INPUT = 'user.phone'
        # 角色选择器
        self.USER_ROLE_INPUT = 'user.roleselect'
        # 表单错误提示
        self.FORM_ITEM_ERROR = 'user.form_item_error'
        # 保存按钮
        self.USER_SAVE_BUTTON = 'user.save_button'
        # 取消 新增用户弹窗按钮
        self.USER_CANCEL_BUTTON = 'user.cancel_button'
        
        #=====================系统弹窗元素定位器==================
        # 新增用户弹窗
        self.USER_ADD_DIALOG = 'user.add_dialog'
        # 编辑用户弹窗
        self.USER_EDIT_DIALOG = 'user.edit_dialog'    
        # 错误消息
        self.ERROR_MESSAGE = 'user.error_message'
        # 操作提示
        self.OPER_MESSAGE = 'common.operate_message'
        # 系统提示
        self.SYS_PROMOPT = 'common.sys_prompt'
        # 系统提示确定按钮
        self.SYS_PROMOPT_CONFIRM = 'common.sys_prompt_confirm'
        # 系统提示取消按钮
        self.SYS_PROMOPT_CANCEL = 'common.sys_prompt_cancel'


        #====================编辑用户元素定位器==================    
        # 编辑昵称输入框
        self.EDIT_NICKNAME_INPUT = 'user.edit_nickName'
        # 编辑保存按钮
        self.USER_EDIT_SAVE_BUTTON = 'user.edit_save_button'
        # 编辑取消按钮
        self.USER_EDIT_CANCEL_BUTTON = 'user.edit_cancel_button'

        #====================表格区域元素定位器==================
        self.TABLE_LIST = 'common.table_list'
        # 切换状态按钮
        self.SWITCH_STATUS_BUTTON = 'user.switch_status_button'
        # 更多操作按钮
        self.MORE_BUTTON = 'user.more_button'
        # 重置密码按钮
        self.RESET_PASSWORD_BUTTON = 'user.reset_password_button'
        # 重置密码输入框
        self.RESET_PASSWORD_INPUT = 'user.reset_password_input'
        # 重置确认按钮
        self.RESET_CONFIRM_BUTTON = 'user.reset_confirm_button'
        # 重置取消按钮
        self.RESET_CANCEL_BUTTON = 'user.reset_cancel_button'
        # 分配角色按钮
        self.ASSIGN_ROLE_BUTTON = 'user.assign_role_button'
        # 提交按钮
        self.USER_SUBMIT_BUTTON = 'user.submit_button'
        #删除用户-取消按钮
        self.USER_DELETE_CANCEL_BUTTON = 'user.delete_cancel_button'
        # 角色分配确认按钮
        self.ROLE_ASSIGN_CONFIRM_BUTTON = 'user.role_assign_confirm_button'
    
   

    def goto_user_management(self):
        """导航到用户管理页面"""
        self.goto("/system/user")
        # 等待页面加载完成，使用'domcontentloaded'状态，更可靠
        self.wait_for_load_state('domcontentloaded')
        # 等待用户搜索输入框可见，确保页面完全加载
        try:
            self.wait_for_locator(self.SEARCH_INPUT, state="visible", timeout=15000)
        except Exception as e:
            print(f"等待用户搜索输入框失败: {e}")
            # 如果等待失败，尝试刷新页面
            self.refresh_page()
            self.wait_for_locator(self.SEARCH_INPUT, state="visible", timeout=15000)
    def clear_search_input(self):
        """清空搜索输入框"""
        self.fill(self.SEARCH_INPUT, "")
    def click_add(self):
        """点击新增用户按钮"""
        # 等待页面完全加载
        self.wait_for_load_state("domcontentloaded")
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass
        
        # 等待新增按钮可见
        self.wait_for_locator(self.USER_ADD_BUTTON, state="visible", timeout=10000)
        
        # 点击新增按钮
        self.click(self.USER_ADD_BUTTON)
        
        # 等待对话框打开（增加等待时间）
        try:
            dialog_locator = self.get_locator(self.USER_ADD_DIALOG)
            dialog_locator.wait_for(state="visible", timeout=30000)
            return dialog_locator
        except Exception as e:
            print(f"等待添加用户对话框超时: {e}")
            # 尝试使用其他方式查找弹窗
            fallback_locator = self.page.locator(".el-dialog").first
            if fallback_locator.is_visible():
                print("使用备用定位器找到弹窗")
                return fallback_locator
            raise
    def clear_username_search_input(self):
        """清空用户名搜索输入框"""
        self.fill(self.SEARCH_INPUT, "")
    def fill_search_phone(self, phone: str):
        """填写手机号搜索"""
        self.fill(self.USER_PHONE_SEARCH_INPUT, phone)
    def click_search(self):
        """点击搜索按钮"""
        self.click(self.SEARCH_BUTTON)
        # 等待页面加载
        self.wait_for_load_state()
    def fill_username(self, username: str):
        """填写用户名"""
        self.fill(self.USER_NAME_INPUT, username)
    def fill_nickname(self, nickname: str):
        """填写昵称"""
        self.fill(self.USER_NICKNAME_INPUT, nickname)
    def fill_password(self, password: str):
        """填写密码"""
        self.fill(self.USER_PASSWORD_INPUT, password)
    def fill_email(self, email: str):
        """填写邮箱"""
        self.fill(self.USER_EMAIL_INPUT, email)
    def fill_phone(self, phone: str):
        """填写手机号"""
        self.fill(self.USER_PHONE_INPUT, phone)
    def click_batch_delete(self):
        """点击批量删除按钮"""
        self.click(self.USER_BATCH_DELETE_BUTTON)
    def select_status(self):
        """选择状态"""
        self.click(self.USER_STATUS_SEARCH_INPUT)
    def click_status(self, status: str):
        """点击状态"""
        if status == "正常":
            self.click(self.USER_STATUS_NORMAL_SELECTOR)
        elif status == "停用":
            self.click(self.USER_STATUS_DISABLED_SELECTOR)
    def check_role(self, role_name: str):
        """填写角色"""
        try:
            self.click(self.USER_ROLE_INPUT)
            # 更精确的定位，只匹配下拉菜单中的角色选项
            role_option = self.page.locator(".el-select-dropdown__item").filter(has_text=role_name)
            if role_option.count() > 0:
                role_option.click()
            else:
                print(f"未找到角色: {role_name}")
            #模拟键盘ESC键关闭弹窗
            self.page.keyboard.press("Escape")
        except Exception as e:
            print(f"勾选角色失败: {e}")
            # 尝试关闭弹窗
            self.page.keyboard.press("Escape")
    
    def check_role_in_assign_dialog(self, role_name: str):
        """在分配角色弹窗中选择角色"""
        try:
            # 等待分配角色窗口出现
            self.wait_for_load_state('domcontentloaded')
            
            # 尝试多次查找和选择角色
            for attempt in range(3):
                try:
                    # 查找角色分配弹窗中的角色
                    role_element = self.locator(".el-tree").get_by_text(role_name)
                    if role_element.count() > 0:
                        # 滚动到元素位置
                        role_element.scroll_into_view_if_needed()
                        # 点击角色名称旁边的复选框
                        checkbox = role_element.locator("..").locator(".el-checkbox__input")
                        if checkbox.count() > 0:
                            # 等待元素稳定
                            checkbox.wait_for(state="stable", timeout=5000)
                            checkbox.click()
                            print(f"✅成功选择角色: {role_name}")
                            return True
                        else:
                            print(f"角色 {role_name} 的复选框不可见")
                    else:
                        print(f"角色 {role_name} 不可见")
                except Exception as e:
                    print(f"第 {attempt + 1} 次尝试选择角色 {role_name} 失败: {e}")
                    # 等待一段时间后重试
                    self.page.wait_for_timeout(500)
            
            # 如果多次尝试都失败，尝试展开菜单树
            try:
                expand_buttons = self.locator(".el-tree-node__expand-icon")
                if expand_buttons.count() > 0:
                    for i in range(expand_buttons.count()):
                        try:
                            expand_button = expand_buttons.nth(i)
                            if expand_button.is_visible():
                                expand_button.click()
                                self.page.wait_for_timeout(300)
                        except Exception:
                            pass
                
                # 再次尝试选择角色
                role_element = self.locator(".el-tree").get_by_text(role_name)
                if role_element.count() > 0:
                    role_element.scroll_into_view_if_needed()
                    checkbox = role_element.locator("..").locator(".el-checkbox__input")
                    if checkbox.count() > 0:
                        checkbox.wait_for(state="stable", timeout=5000)
                        checkbox.click()
                        print(f"✅成功选择角色: {role_name}")
                        return True
            except Exception as e:
                print(f"展开菜单树后选择角色 {role_name} 失败: {e}")
                
        except Exception as e:
            print(f"选择角色 {role_name} 失败: {e}")
        
        return False

    
   
  
    def check_is_form_error(self) -> bool:
        """检查是否有表单错误"""
        #检查用户名输入框是否有错误提示 
        if self.is_visible(self.FORM_ITEM_ERROR):
            error_text = self.get_text(self.FORM_ITEM_ERROR)
            print(f"❌添加用户表单中错误提示: {error_text}")
            #关闭弹窗
            self.click_cancel_user()
            print("✅表单有错误提示，关闭添加用户弹窗")
            return error_text
        else:
            return ""


    
    def create_user(self, user_data: dict):
        """创建用户"""
        self.click_add()
        print(f"打开添加用户窗口")
        # 等待弹窗完全加载
        self.wait_for_locator(self.USER_NAME_INPUT, state="visible")
        
        # 调试：打印用户数据
        print(f"用户数据: {user_data}")
        
        error_text = self.fill_user_form(
            username=user_data['userName'],
            nickname=user_data['nickName'],
            password=user_data['password'],
            email=user_data.get('email', ''),
            phone=user_data.get('phonenumber', ''),
            role_name=user_data.get('roleName', ''),
        )
        
        if error_text:
            return error_text
        
        self.click_save_user()
        
        # 等待操作消息，增加容错处理  
        message = self.get_oper_message()
        return message
    
    def create_and_get_result(self, user_data: dict):
        """创建用户并返回结果（用于测试）"""
        self.click_add()
        self.wait_for_timeout(1000)
        
        # 填写表单
        try:
            self.fill_username(user_data.get('userName', ''))
            self.fill_nickname(user_data.get('nickName', ''))
            self.fill_password(user_data.get('password', ''))
            self.fill_email(user_data.get('email', ''))
            self.fill_phone(user_data.get('phonenumber', ''))
        except Exception as e:
            print(f"填写表单失败: {e}")
            return str(e)
        
        # 检查表单错误
        error_text = self.check_is_form_error()
        if error_text:
            return error_text
        
        # 点击保存
        try:
            self.click_save_user()
            self.wait_for_timeout(2000)
        except Exception as e:
            print(f"点击保存失败: {e}")
            return str(e)
        
        # 获取操作消息
        message = self.get_oper_message()
        if message == "操作消息未显示":
            # 检查是否有表单错误
            form_error = self.check_is_form_error()
            if form_error:
                return form_error
            # 检查对话框是否仍然打开
            if self.is_visible(self.USER_ADD_DIALOG):
                return "对话框仍然打开，可能验证失败"
        
        return message
    def get_oper_message(self):
        """获取操作消息"""
        try:
            # 等待操作消息显示
            self.wait_for_locator(self.OPER_MESSAGE, state="visible", timeout=5000)
            message = self.get_text(self.OPER_MESSAGE)
            if "成功" not in message:
                print(f"❌操作失败，消息: {message}")
                self.click_cancel_user()
                return message
            else:
                print(f"🔥操作成功消息: {message}")
                # 等待消息从DOM中移除
                self.wait_for_locator(self.OPER_MESSAGE, state="detached", timeout=5000)
                return message
        except Exception as e:
            print(f"获取操作消息失败: {e}")
            # 尝试直接获取消息，即使它可能已经消失
            try:
                if self.is_visible(self.OPER_MESSAGE):
                    message = self.get_text(self.OPER_MESSAGE)
                    print(f"🔥操作消息: {message}")
                    return message
            except Exception:
                pass
            print(f"❌操作消息未显示")
            return "操作消息未显示"
    def fill_user_form(self, username: str, nickname: str, password: str, email: str = '', phone: str = '', role_name: str = ''):
        """填写用户表单"""

        self.fill(self.USER_NAME_INPUT, username)
        self.fill(self.USER_NICKNAME_INPUT, nickname)
        self.fill(self.USER_PASSWORD_INPUT, password)
        if email:
            self.fill(self.USER_EMAIL_INPUT, email)
        if phone:
            self.fill(self.USER_PHONE_INPUT, phone)
        if role_name:
            self.click(self.USER_ROLE_INPUT)
            # self.page.get_by_role("listitem").filter(has_text=role_name).click()
            self.page.get_by_text(role_name).click()
            #模拟键盘ESC键关闭弹窗
            self.page.keyboard.press("Escape")
        #检查用户名输入框是否有错误提示
        error_text =self.check_is_form_error()
        return error_text
        
    
    def click_save_user(self):
        """点击保存用户"""
        self.click(self.USER_SAVE_BUTTON)
        # 等待保存完成和页面刷新
        self.page.wait_for_timeout(3000)
    
    def click_cancel_user(self):
        """点击取消"""
        self.logger.info("🚀 点击「取消」按钮关闭添加用户弹窗")    
        self.click(self.USER_CANCEL_BUTTON)
         # 等待弹窗消失
        self.wait_for_locator(self.USER_ADD_DIALOG, state="detached")
        self.logger.info("✅ 点击「取消」按钮成功关闭添加用户弹窗")
    
    def search_user(self, keyword: str):
        """搜索用户"""
        print(f"🔍开始搜索用户: {keyword}")
        self.search(keyword, self.SEARCH_INPUT, self.SEARCH_BUTTON)
        # 等待表格加载完成
        self.page.wait_for_timeout(2000)
    def click_search_reset(self):
        """点击重置搜索"""
        self.click(self.SEARCH_RESET_BUTTON)

    def get_user_list(self) -> List[str]:
        """获取用户列表"""
        user_list = []
        try:
            
            # 查找包含用户数据的表格行
            rows = self.page.locator('tbody tr').all()
            
            for row in rows:
                # 获取所有td元素
                cells = row.locator('td').all()
                
                if len(cells) >= 3:
                    # 尝试不同的列索引，找到用户名
                    for j in range(1, min(4, len(cells))):  # 尝试第2-4列
                        try:
                            cell_content = cells[j].text_content()
                            # 用户名通常不是纯数字，且长度合理
                            if cell_content and cell_content.strip() and not cell_content.strip().isdigit():
                                user_list.append(cell_content.strip())
                                break  # 找到用户名后退出循环
                        except Exception:
                            continue
        except Exception as e:
            print(f"获取用户列表失败: {e}")
        
        return user_list
    
    def delete_user(self, username: str) -> str:
        """删除用户"""
        return self.delete(username, "button:has-text('删除')")
    def click_edit_user(self,username):
        """点击编辑用户"""
        modify_button =self.get_locator(self.TABLE_LIST).filter(has_text=f"{username}").locator('.el-button').filter(has_text="修改")       
        modify_button.click()
        # 等待编辑用户弹窗出现
        self.wait_for_locator(self.USER_EDIT_DIALOG, state="visible")
        return self.get_locator(self.USER_EDIT_DIALOG)
    def click_edit_submit(self):
        """点击编辑用户提交按钮"""
        self.click(self.USER_EDIT_SAVE_BUTTON)
    def click_reset_password_button(self):
        """点击重置密码按钮"""
        self.click(self.RESET_PASSWORD_BUTTON)
        # 等待重置密码弹窗出现
        self.wait_for_locator(self.RESET_PASSWORD_INPUT, state="visible")
    def fill_reset_password(self, new_password: str):
        """填写重置密码"""
        self.fill(self.RESET_PASSWORD_INPUT, new_password)
    def click_reset_confirm_button(self):
        """点击重置确认按钮"""
        self.click(self.RESET_CONFIRM_BUTTON)
    def click_sys_confirm_button(self):
        """点击系统确认按钮"""
        self.click(self.SYS_PROMOPT_CONFIRM)
    def edit_user(self, username: str, nickname,new_nickname: str):
        """编辑用户"""
        try:
            # 搜索用户
            self.search_user(username)
            print(f"🔍找到用户: {username}")
            
            # 查找行中的修改按钮
            self.click_edit_user(username)
    
            # 直接使用编辑弹窗的昵称输入框
            self.fill(self.EDIT_NICKNAME_INPUT, new_nickname)
            self.click_edit_submit()
            form_message = self.check_is_form_error()
            if form_message:
                return form_message
            message = self.get_oper_message()
            return message
        except Exception as e:
            print(f"编辑用户失败: {e}")
            return "编辑用户失败"
    

    def _locate_user_operation_button(self, username: str, button_text: str):
        """定位用户操作按钮"""
        # 搜索用户
        self.search_user(username)
        # 等待表格加载完成
        self.wait_for_load_state()
        # 找到包含指定用户名的行
        rows = self.get_locator(self.TABLE_LIST).filter(has_text=f"{username}")
        more_button = rows.locator("button").filter(has_text=f"{button_text}")
        more_button.click()
        self.wait_for_load_state()
        return more_button
    def find_keyword_row(self, keyword: str):
        """查找包含关键字的行"""
        # 查找包含关键字的行     
        row =self.get_locator(self.TABLE_LIST).filter(has_text=f"{keyword}")
        if row.count() == 0:
            print(f"❌未找到包含关键字 {keyword} 的行")
            return None
        return row
    def click_row_more_button(self,row):
        """点击包含关键字的行的更多按钮"""
        more_button = row.locator('button:has-text("更多")')
        more_button.click()

    def find_user_row(self, username: str):
        """查找用户行"""
        # 搜索用户
        self.search_user(username)
        
        # 等待页面加载
        self.wait_for_load_state()
        
        # 查找包含用户名的行     
        row =self.get_locator(self.TABLE_LIST).filter(has_text=f"{username}")
        if row.count() == 0:
            print(f"❌未找到包含用户名 {username} 的行")
            return None
        #获取行的文本内容
        row_text = row.text_content()
        print(f"内容: {row_text[:100]}...")
        if username in row_text:
            print(f"🔍找到包含用户名 {username} 的行")
            return row

        print(f"未找到包含用户名 {username} 的行")
        return None
    
    def get_input_error_messages(self):
        """获取输入框错误消息"""
        error_messages = []
        error_elements = self.page.locator('.el-form-item__error').all()
        for element in error_elements:
            error_messages.append(element.text_content().strip())
        return error_messages
    def click_cancel_user_dialog(self):
        """点击取消用户弹窗"""
        try:
            self.logger.info("🚀 点击「取消」按钮关闭添加用户弹窗")    
            self.click(self.USER_CANCEL_BUTTON)
            # 等待弹窗消失
            self.wait_for_locator(self.USER_ADD_DIALOG, state="detached")
            self.logger.info("✅ 点击「取消」按钮成功关闭添加用户弹窗")
        except Exception as e:
            print(f"点击取消用户弹窗失败: {e}")
            # 使用CSS选择器直接定位关闭按钮
            try:
                close_button = self.page.locator(".el-dialog__close").first
                close_button.click()
            except Exception as e2:
                print(f"点击关闭按钮失败: {e2}")
                # 尝试按ESC键关闭弹窗
                self.page.keyboard.press("Escape")
    
    def click_row_status_button(self, keyword: str):
        """点击行状态按钮"""
        try:
            row = self.get_locator(self.TABLE_LIST).filter(has_text=f"{keyword}")
            status_button = row.locator('.el-switch').first
            if status_button.count() > 0 and status_button.is_visible():
                status_button.click()
                # 等待确认弹窗出现
                self.wait_for_timeout(500)
            else:
                print(f"❌未找到包含关键字 {keyword} 的行或状态按钮不可见")
        except Exception as e:
            print(f"❌点击状态按钮失败: {e}")
           
    def click_edit_button(self, username: str):
        """点击编辑按钮"""
        # 查找用户行
        self.search_user(username)
        # 等待系统提示消失
        try:
            self.wait_for_locator(self.OPER_MESSAGE, state="detached", timeout=10000)
        except Exception as e:
            print(f"等待系统提示消失失败: {e}")
        # 找到修改按钮
        edit_button = self.get_locator(self.TABLE_LIST).filter(has_text=f"{username}").locator('.el-button').filter(has_text="修改")
        print("找到修改按钮")
        edit_button.click()
        # 等待编辑弹窗出现
        self.wait_for_locator(self.USER_EDIT_DIALOG, state="visible")
    def locate_switch_status_button(self, user_row_locator):
        """定位切换状态按钮"""
        status_button = user_row_locator.locator('.el-switch').first
        return status_button

    def batch_delete(self, keyword: str) -> str:
        """批量删除用户"""
        try:
            # 查找所有包含关键字的行
            self.search_user(keyword)
            
            # 直接使用JavaScript来选择所有包含关键字的行并点击删除按钮
            try:
                print("✅开始进行批量删除")
                checkboxes = self.page.locator('.cell').first
                checkboxes.click()
                print("✅选中复选框")

                
                # 查找并点击批量删除按钮
                delete_button = self.get_locator(self.USER_BATCH_DELETE_BUTTON)
                delete_button.click()
                print("✅点击批量删除按钮")
                
                self.wait_for_load_state()
                
                
                
                # # 执行JavaScript来选择所有包含关键字的行
                # self.page.evaluate("""
                #     (keyword) => {
                #         // 查找所有行
                #         const rows = document.querySelectorAll('tbody tr');
                #         console.log('找到 ' + rows.length + ' 行');
                        
                #         // 选择包含关键字的行
                #         let selectedCount = 0;
                #         rows.forEach(row => {
                #             if (row.textContent.includes(keyword)) {
                #                 // 查找行中的复选框并点击
                #                 const checkbox = row.querySelector('.el-checkbox__input');
                #                 if (checkbox) {
                #                     checkbox.click();
                #                     selectedCount++;
                #                 }
                #             }
                #         });
                #         console.log('选中 ' + selectedCount + ' 行');
                        
                #         // 查找并点击批量删除按钮
                #         const deleteButtons = document.querySelectorAll('.el-button--danger');
                #         console.log('找到 ' + deleteButtons.length + ' 个危险按钮');
                        
                #         // 尝试点击第一个危险按钮
                #         if (deleteButtons.length > 0) {
                #             // 移除禁用属性
                #             deleteButtons[0].removeAttribute('disabled');
                #             deleteButtons[0].classList.remove('is-disabled');
                #             // 点击按钮
                #             deleteButtons[0].click();
                #             console.log('点击了批量删除按钮');
                #         }
                #     }
                # """, keyword)
                
                # # 等待一下，确保操作有时间执行
                # self.page.wait_for_timeout(2000)
            except Exception as e:
                print(f"使用JavaScript实现批量删除失败: {e}")
            
            # 等待确认弹窗并确认         
            self.wait_for_locator(self.SYS_PROMOPT, state="visible", timeout=10000)
            self.click(self.SYS_PROMOPT_CONFIRM)
            print("点击确认删除按钮")
            
            
            # 等待操作完成
            try:
                self.wait_for_locator(self.OPER_MESSAGE, state="visible", timeout=10000)
                message = self.get_text(self.OPER_MESSAGE)
                print(f"🔥批量删除用户消息: {message}")
                # 等待消息消失
                self.wait_for_locator(self.OPER_MESSAGE, state="detached")                                       
                return message
            except:
                # 如果没有找到操作消息，返回默认成功消息
                print("未找到操作消息，返回默认失败消息")
                return "失败"
        except Exception as e:
            print(f"批量删除用户失败: {e}")
            return "失败"
    
    def get_user_info(self, username: str) -> dict:
        """获取用户信息"""
        try:
            # 查找用户行
            self.search_user(username)
            print(f"🔍找到用户: {username}")
            # 等待表格加载
            self.wait_for_load_state()
            # 查找包含用户名的行
            user_row = self.get_locator(self.TABLE_LIST).filter(has_text=f"{username}")
            
            # 检查用户是否存在
            if user_row.count() == 0:
                print(f"❌未找到用户: {username}")
                # 尝试再次搜索
                self.search_user(username)
                user_row = self.get_locator(self.TABLE_LIST).filter(has_text=f"{username}")
                if user_row.count() == 0:
                    return None
            
            user_info = {
                'userName': '',
                'nickName': '',  # 确保包含nickName键
                'phonenumber': '',
                'status': ''
            }
            
            # 尝试不同的列索引，确保能找到正确的列
            try:
                user_info['userName'] = user_row.locator('td:nth-child(3)').text_content().strip()
                user_info['nickName'] = user_row.locator('td:nth-child(4)').text_content().strip()
                user_info['phonenumber'] = user_row.locator('td:nth-child(6)').text_content().strip()
                user_info['status'] = "1" if user_row.locator('.el-switch').get_attribute('aria-checked') == "true" else "0"
            except Exception as e:
                print(f"获取用户信息列失败: {e}")
                # 尝试使用不同的方法获取用户信息
                row_text = user_row.text_content()
                print(f"行文本: {row_text[:100]}...")
                # 从行文本中提取信息
                if username in row_text:
                    user_info['userName'] = username
                    # 尝试提取其他信息
                    user_info['nickName'] = "未知"
                    user_info['phonenumber'] = "未知"
                    user_info['status'] = "1"
            
            print(f"🔥获取到的用户信息: {user_info}")
            return user_info
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            return None
    
    def search_by_phone(self, phone: str) -> dict:
        """通过手机号搜索用户"""
        try:
            # 清空用户名搜索框
            self.fill(self.SEARCH_INPUT, '')
            # 输入手机号
            self.fill(self.USER_PHONE_SEARCH_INPUT, phone)
            self.wait_for_load_state()
            print(f"🔍输入手机号: {phone}")
            # 点击搜索按钮
            self.click(self.SEARCH_BUTTON)
            print(f"🔍点击搜索按钮")
            # 等待页面加载
            self.wait_for_load_state()
       
            # 查找包含手机号的行并返回用户名
            row = self.get_locator(self.TABLE_LIST).filter(has_text=f"{phone}").first
            print(f"🔍找到的行: {row}")
            # 尝试获取用户名
            try:
                username = row.locator('td:nth-child(3)').text_content().strip()
                user_info = self.get_user_info(username)
                if user_info:
                    return user_info
            except Exception as e:
                print(f"获取用户名失败: {e}")
            
            # 如果无法获取用户名，返回一个包含手机号的字典
            return {
                'userName': '未知',
                'nickName': '未知',
                'phonenumber': phone,
                'status': '1'
            }
        except Exception as e:
            print(f"通过手机号搜索用户失败: {e}")
            return {
                'userName': '未知',
                'nickName': '未知',
                'phonenumber': phone,
                'status': '1'
            }
    
    
    def click_import(self):
        """点击导入按钮"""
        try:
            # 查找导入按钮并点击
            self.click(self.USER_IMPORT_BUTTON)
            
            # 等待导入弹窗出现
            # 等待一下，确保弹窗完全加载
            self.page.wait_for_timeout(2000)
            
            return True
        except Exception as e:
            print(f"点击导入按钮失败: {e}")
            return True
    def fill_search_input(self, keyword: str):
        """填充搜索框"""
        self.fill(self.SEARCH_INPUT, keyword)
        print(f"🔍输入搜索关键词: {keyword}")
   
    
    def click_export(self):
        """点击导出按钮"""
        try:
            # 点击导出按钮
            self.click(self.USER_EXPORT_BUTTON)
            # 等待导出完成
            # 这里可以根据实际情况添加等待逻辑
            self.page.wait_for_timeout(3000)
        except Exception as e:
            print(f"点击导出按钮失败: {e}")
    
    def click_delete_user(self, username: str):
        """点击删除用户"""
        try:
            # 查找用户行
            user_row = self.find_user_row(username)
            if not user_row:
                print(f"未找到用户: {username}")
                return False
            
            # 尝试直接点击行中的删除按钮
            try:
                # 查找包含"删除"文本的按钮
                delete_button = user_row.locator('.el-button').filter(has_text="删除").first
                if delete_button.is_visible():
                    print("找到删除按钮")
                    delete_button.click()
                    # 等待确认弹窗出现
                    try:
                        self.wait_for_locator(self.SYS_PROMOPT, state="visible", timeout=5000)
                        return True
                    except:
                        print("未找到确认弹窗，继续执行")
                        return True
            except Exception as e:
                print(f"直接查找删除按钮失败: {e}")
            
            # 尝试从更多按钮中查找删除按钮
            try:
                # 点击更多按钮
                more_button = user_row.locator('td:last-child .el-dropdown').first
                more_button.click()
                
                # 等待下拉菜单出现
                self.page.wait_for_timeout(1000)
                
                # 点击删除按钮
                delete_button = self.page.locator('.el-dropdown-menu__item').filter(has_text="删除").first
                delete_button.click()
                
                # 等待确认弹窗出现
                try:
                    self.wait_for_locator(self.SYS_PROMOPT, state="visible", timeout=5000)
                    return True
                except:
                    print("未找到确认弹窗，继续执行")
                    return True
            except Exception as e:
                print(f"从更多按钮中查找删除按钮失败: {e}")
            
            print("未找到删除按钮")
            return False
        except Exception as e:
            print(f"点击删除用户失败: {e}")
            return False
    
    def fill_user_nickname(self, nickname: str):
        """填写用户昵称"""
        try:
            # 填写昵称输入框
            self.fill(self.EDIT_NICKNAME_INPUT, nickname)
        except Exception as e:
            print(f"❌填写用户昵称失败: {e}")
    
    def click_edit_cancel_button(self):
        """点击编辑弹窗的取消按钮"""
        try:
            # 直接点击取消按钮，不需要等待系统提示
            self.click(self.USER_EDIT_CANCEL_BUTTON)
            # 等待编辑弹窗消失
            self.wait_for_locator(self.USER_EDIT_DIALOG, state="detached")
           
        except Exception as e:
            print(f"点击编辑取消按钮失败: {e}")
    
    def click_delete_cancel_button(self):
        """点击删除用户弹窗的取消按钮"""
        try:
            # 先等待确认弹窗出现
            self.wait_for_locator(self.SYS_PROMOPT, state="visible", timeout=5000)
            
            # 尝试使用更通用的取消按钮定位器
            try:
                # 方式1: 使用系统提示取消按钮定位器
                cancel_button = self.get_locator(self.SYS_PROMOPT_CANCEL)
                if cancel_button.is_visible():
                    cancel_button.click()
                else:
                    # 方式2: 使用用户删除取消按钮定位器
                    self.click(self.USER_DELETE_CANCEL_BUTTON)
            except Exception:
                # 方式3: 直接查找包含"取消"文本的按钮
                cancel_button = self.page.get_by_role("button", name="取消")
                if cancel_button.is_visible():
                    cancel_button.click()
            
            # 等待弹窗消失
            self.wait_for_locator(self.SYS_PROMOPT, state="detached", timeout=5000)
        except Exception as e:
            print(f"点击取消按钮失败: {e}")

    def check_role_in_table(self, role_name: str):
        """检查角色是否被选中"""
        try:
            checkboxes = self.get_locator(self.TABLE_LIST).filter(has=self.page.locator("td:nth-child(4)").filter(has_text=f"{role_name}")).first         
            checkbox = checkboxes.locator('td:nth-child(2)')
            checkbox.scroll_into_view_if_needed()
            checkbox.click()
        except Exception as e:
            print(f"检查角色失败: {e}")
    def click_role_assign_confirm_button(self):
        """点击角色分配确认按钮"""
        try:
            self.click(self.ROLE_ASSIGN_CONFIRM_BUTTON)
        except Exception as e:
            print(f"点击角色分配确认按钮失败: {e}")
    def click_assign_role_button(self):
        """点击分配角色按钮"""
        try:
            self.click(self.ASSIGN_ROLE_BUTTON)
        except Exception as e:
            print(f"点击分配角色按钮失败: {e}")
    
    def get_dialog_number(self):
        """获取新增用户弹窗数量"""
        try:
            return self.get_locator(self.USER_ADD_DIALOG).count()
        except Exception as e:
            print(f"获取弹窗数量失败: {e}")
            return 0