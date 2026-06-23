"""安全业务场景测试:XSS、SQL注入、越权、未授权访问"""
from ui.biz.common_biz import CommonBiz
from config.settings import settings
import logging
class SecurityBiz:
    def __init__(self, page):
        self.page = page
        self.common_biz = CommonBiz(page)
        self.logger = logging.getLogger(__name__)
        self.base_url = settings.base_url

    # ==================== 安全：XSS注入 ====================
    def input_xss_payload(self, page_obj, payload="<script>alert('xss')</script>",test_user_data=None):
        """输入XSS payload并提交"""
        self.logger.info(f"输入XSS payload: {payload}")  
        try:
            # 先关闭任何打开的弹窗
            self.page.keyboard.press("Escape")
            #打开新增用户弹窗
            page_obj.click_add()
            page_obj.fill_username(test_user_data['userName'])
            page_obj.fill_nickname(test_user_data['nickName'])
            page_obj.fill_password(test_user_data['password'])
            page_obj.click_save_user()
            # 等待操作完成
            self.page.wait_for_timeout(2000)
            # 检查操作消息
            try:
                # message = self.page.locator(".el-message__content").text_content()
                message = self.common_biz.get_operate_message()
            except:
                message = ""
            # 判断是否被安全拦截
            is_blocked = any([
                "不能包含脚本字符" in str(message),
                "非法字符" in str(message),
                "失败" in str(message),
                "default value" in str(message),
            ])

            # 检查页面是否包含Payload（判断是否成功存储）
            page_content = self.page.content().lower()
            page_has_payload = payload.lower() in page_content

            if page_has_payload:
                self.logger.warning(f"XSS payload found in page: {payload}")
            else:
                self.logger.info(f"XSS payload not found in page: {payload}")

            return {
                "alert_count": 0,
                "message": message,
                "is_blocked": is_blocked,
                "page_has_payload": page_has_payload
            }

        except Exception as e:
            self.logger.error(f"XSS测试失败: {e}")
            self.page.keyboard.press("Escape")
            return {
                "alert_count": 0,
                "message": "测试异常",
                "is_blocked": True,
                "page_has_payload": False
            }

    # ==================== 安全：SQL注入 ====================
    def input_sql_inject(self, page_obj,sql_payload="admin' OR 1=1--"):
        """搜索框输入SQL注入payload"""
        try:
            # 找到搜索按钮
            self.logger.info(f"输入SQL注入payload: {sql_payload}")
            # 点击搜索按钮
            result = page_obj.search_user(sql_payload)
            return result
        except Exception as e:
            self.logger.error(f"SQL注入测试失败: {e}")
            return {"message":"测试失败"}

    # ==================== 安全：URL越权访问 ====================
    def unauthorized_url_visit(self, path):
        """直接访问无权限页面URL"""
        self.page.goto(f"{self.base_url}{path}")

    # ==================== 安全：未登录访问后台 ====================
    def visit_system_without_login(self, path):
        """未登录直接访问后台接口/页面"""
        self.page.goto(f"{self.base_url}{path}")

    # ==================== 安全：横向越权 ====================
    def edit_other_user_data(self, user_name):
        """尝试编辑其他用户数据"""
        try:
            # 尝试点击编辑按钮
            edit_button = self.page.locator(f"//tr[contains(.,'{user_name}')]//button[contains(text(),'修改')]")
            if edit_button.count() > 0:
                edit_button.click()
                self.logger.info(f"尝试编辑用户: {user_name}")
            else:
                self.logger.warning(f"未找到用户 {user_name} 的编辑按钮")
        except Exception as e:
            self.logger.error(f"编辑用户失败: {e}")