"""异常业务场景测试:连续点击、刷新、重复提交、弱网"""
from ui.pages.modules.user_page import UserPage
from ui.biz.common_biz import CommonBiz
class AbnormalBiz:
    def __init__(self, page):
        self.page = page
        self.common_biz = CommonBiz(page)
        self.user_page = UserPage(page)

    # ==================== 异常：连续快速点击 ====================
    def repeat_click_btn(self, page_obj, btn_attr, times=3):
        """连续点击按钮，测试防重复提交"""
        btn_loc = getattr(page_obj, btn_attr)
        print(f"点击按钮: {btn_loc} {times} 次")
        for i in range(times):
            try:
                page_obj.click(btn_loc)
                print(f"✅第{i+1}次点击成功")
            except Exception as e:
                print(f"⚠️第{i+1}次点击失败: {e}")
            import time
            time.sleep(0.5)

    # ==================== 异常：流程中刷新页面 ====================
    def refresh_in_operation(self, page_obj, btn_attr):
        """操作中刷新页面"""
        btn_loc = getattr(page_obj, btn_attr)
        page_obj.click(btn_loc)
        page_obj.fill_username("testuser")
        page_obj.refresh_page()

    # ==================== 异常：空表单直接提交 ====================
    def submit_empty_form(self, page_obj,btn_attr):
        """不填任何内容直接提交表单"""
        btn_loc = getattr(page_obj, btn_attr)
        page_obj.click(btn_loc)
        page_obj.click_save_user()  # 直接提交空表单

    # ==================== 特殊：模拟弱网操作 ====================
    def submit_with_slow_network(self, page_obj,btn_attr,test_user_data):
        """弱网下提交表单"""
        btn_loc = getattr(page_obj, btn_attr)
        page_obj.click(btn_loc)
        page_obj.fill_username(test_user_data["userName"])
        page_obj.fill_nickname(test_user_data["nickName"])
        page_obj.fill_password(test_user_data["password"])
        # 模拟弱网：添加网络延迟
        def slow_route(route):
            import time
            time.sleep(2)  # 2秒延迟
            route.continue_()
        
        self.page.route("**/*", slow_route)
        page_obj.click_save_user()  # 提交表单
        #验证系统不奔溃
        is_visible = page_obj.is_visible(page_obj.TABLE_LIST)
        print(f"🔍表格是否可见: {is_visible}")
        return is_visible

    # ==================== 异常：强制关闭弹窗 ====================
    def close_dialog_by_force(self, page_obj, btn_attr):
        """点击右上角关闭弹窗"""
        btn_loc = getattr(page_obj, btn_attr)
        #打开弹窗
        page_obj.click(btn_loc)
        try:
            # 尝试点击取消按钮
            cancel_btn_loc = getattr(page_obj, 'USER_CANCEL_BUTTON')
            self.common_biz.cancel_dialog(cancel_btn_loc)
        except Exception as e:
            print(f"关闭弹窗失败: {e}")

