from ui.pages.base_page import BasePage


class UploadComponent(BasePage):
    """上传组件"""

    def upload_file(self, upload_locator: str, file_path: str):
        """上传文件"""
        # 获取上传元素
        upload_element = self.get_locator(upload_locator)
        # 设置文件路径
        upload_element.set_input_files(file_path)

    def upload_files(self, upload_locator: str, file_paths: list):
        """上传多个文件"""
        # 获取上传元素
        upload_element = self.get_locator(upload_locator)
        # 设置文件路径列表
        upload_element.set_input_files(file_paths)

    def clear_upload(self, upload_locator: str):
        """清除上传"""
        # 获取上传元素
        upload_element = self.get_locator(upload_locator)
        # 清除上传
        upload_element.set_input_files([])
