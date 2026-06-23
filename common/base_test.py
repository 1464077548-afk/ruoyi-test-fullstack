import pytest
from config.settings import settings

class BaseTest:
    """测试基类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前的设置"""
        print(f"=============== BaseTest setup 方法调用=================")
        self.base_url = settings.BASE_URL
        self.username = settings.TEST_USERNAME
        self.password = settings.TEST_PASSWORD
        self.browser = settings.BROWSER
        self.headless = settings.HEADLESS
    
    def get_base_url(self):
        """获取基础URL"""
        return self.base_url
    
    def get_timeout(self, timeout_type='page'):
        """获取配置的page或element超时时间"""
        if timeout_type == 'page':
            return settings.PAGE_LOAD_TIMEOUT
        elif timeout_type == 'element':
            return settings.ELEMENT_TIMEOUT
        return 30