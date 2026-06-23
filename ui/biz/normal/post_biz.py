from ui.pages.modules.post_page import PostPage
from ui.biz.common_biz import CommonBiz
from playwright.sync_api import expect
import logging
import time


class PostBiz:
    def __init__(self, page):
        self.page = page
        self.post_page = PostPage(page)
        self.common = CommonBiz(page)
        self.logger = logging.getLogger(__name__)

    def create_post(self, post_data: dict):
        """创建岗位"""
        try:
            self.common.switch_menu("系统管理/岗位管理")
            message = self.post_page.create_post(post_data)
            self.logger.info(f"🔥创建岗位消息: {message}")
            if "成功" not in message:
                self.post_page.close_add_post_dialog()
            return message
        except Exception as e:
            self.logger.error(f"创建岗位失败: {e}")
            return f"创建失败: {str(e)}"
    def add_post(self, post_data: dict):
        self.post_page.click_add_post()
        self.post_page.fill_post_name(post_data['postName'])
        self.post_page.fill_post_code(post_data['postCode'])
        self.post_page.fill_post_sort(post_data['postSort'])
  
        self.post_page.click_save_post()
        message = self.common.get_operate_message()
        self.logger.info(f"🔥创建岗位: {post_data},🔥操作消息: {message}")
        if "成功" not in message:
            #关闭新增岗位的弹窗
            self.post_page.close_add_post_dialog()
        return message

    def edit_post(self, post_name: str, new_data: dict):
        """编辑岗位"""
        try:
            message = self.post_page.edit_post(
                post_name,
                new_data['postName'],
                new_data['postCode'],
                new_data['postSort']
            )
            self.logger.info(f"🔥编辑岗位消息: {message}")
            return message
        except Exception as e:
            self.logger.error(f"编辑岗位失败: {e}")
            return f"编辑失败: {str(e)}"

    def delete_post(self, post_name: str):
        """删除岗位"""
        try:
            message = self.post_page.delete_post(post_name)
            self.logger.info(f"🔥删除岗位消息: {message}")
            return message
        except Exception as e:
            self.logger.error(f"删除岗位失败: {e}")
            return f"删除失败: {str(e)}"

    def search_post(self, post_name: str):
        """搜索岗位"""
        try:
            self.post_page.search_post(post_name)
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            self.logger.error(f"搜索岗位失败: {e}")
            return False

    def get_post_info(self, post_name: str):
        """获取岗位信息"""
        try:
            self.post_page.search_post(post_name)
            self.page.wait_for_timeout(500)

            locator = self.post_page.get_locator(self.post_page.TABLE_LIST)
            rows = locator.locator("tr").all()
            print(f"找到 {len(rows)} 行数据")

            for row in rows:
                try:
                    name_cell = row.locator("td:nth-child(4)")
                    if name_cell.is_visible():
                        name_text = name_cell.text_content().strip()
                        print(f"检查行: postName={name_text}")  
                        if name_text == post_name:
                            return {
                                "postName": name_text,
                                "postCode": row.locator("td:nth-child(3)").text_content().strip(),
                                "postSort": row.locator("td:nth-child(5)").text_content().strip(),
                                "status": row.locator("td:nth-child(6)").text_content().strip()
                            }
                except Exception as e:
                    continue

            return None
        except Exception as e:
            self.logger.error(f"获取岗位信息失败: {e}")
            return None

    def validate_post_exists(self, post_name: str):
        """验证岗位是否存在"""
        try:
            self.post_page.search_post(post_name)
            self.page.wait_for_timeout(500)

            locator = self.post_page.get_locator(self.post_page.TABLE_LIST)
            rows = locator.locator("tr").all()

            for row in rows:
                try:
                    name_cell = row.locator("td:nth-child(3)")
                    if name_cell.is_visible():
                        name_text = name_cell.text_content().strip()
                        print(f"岗位名称: {name_text},post_name: {post_name}")
                        if name_text == post_name:
                            return True
                except:
                    continue

            return False
        except Exception as e:
            self.logger.error(f"验证岗位存在失败: {e}")
            return False

    def toggle_post_status(self, post_name: str):
        """切换岗位状态"""
        try:
            self.post_page.search_post(post_name)
            self.page.wait_for_timeout(500)

            locator = self.post_page.get_locator(self.post_page.TABLE_LIST)
            rows = locator.locator("tr").all()

            for row in rows:
                try:
                    name_cell = row.locator("td:nth-child(3)")
                    if name_cell.is_visible() and name_cell.text_content().strip() == post_name:
                        status_locator = row.locator('[role="switch"]').first
                        status_locator.click()
                        self.common.wait_for_dialog()
                        message = self.common.get_operate_message()
                        return message
                except:
                    continue

            return "未找到岗位"
        except Exception as e:
            self.logger.error(f"切换岗位状态失败: {e}")
            return f"切换失败: {str(e)}"

    def batch_delete_posts(self, post_name: str):
        """批量删除岗位"""
        try:
            # self.post_page.search_post(post_name)
            self.post_page.fill_search_input(post_name)
            self.post_page.click_search_button()
            
            self.post_page.checked_row()
            self.page.wait_for_timeout(200)
            self.post_page.click_batch_delete_button()
            self.common.confirm_dialog()
            message = self.common.get_operate_message()
            print(f"批量删除岗位消息: {message}")
            return message
        except Exception as e:
            self.logger.error(f"批量删除岗位失败: {e}")
            return f"批量删除失败: {str(e)}"
