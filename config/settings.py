import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 打印环境变量以调试
import os
print(f"DEBUG: TEST_USERNAME from env: {os.getenv('TEST_USERNAME')}")
print(f"DEBUG: TEST_PASSWORD from env: {os.getenv('TEST_PASSWORD')}")
print(f"DEBUG: API_BASE_URL from env: {os.getenv('API_BASE_URL')}")

class Settings:
    # 基础配置
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8081')
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
    
    # 为了兼容性，添加小写属性
    @property
    def base_url(self):
        return self.BASE_URL
    
    @property
    def api_base_url(self):
        return self.API_BASE_URL

    # 认证信息
    USERNAME = os.getenv('TEST_USERNAME', 'admin')
    PASSWORD = os.getenv('TEST_PASSWORD', 'admin123')
    
    # 浏览器配置
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'false'
    SLOW_MO = int(os.getenv('SLOW_MO', '0'))
    
    # 超时设置
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    ELEMENT_TIMEOUT = int(os.getenv('ELEMENT_TIMEOUT', '10'))
    # UI_TIMEOUT 转换为毫秒
    UI_TIMEOUT = int(os.getenv('UI_TIMEOUT', '60')) * 1000
    
    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_NAME = os.getenv('DB_NAME', 'ry-vue')
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
    
    # 性能测试配置
    LOCUST_HOST = os.getenv('LOCUST_HOST', 'http://localhost:8080')
    LOCUST_USERS = int(os.getenv('LOCUST_USERS', '100'))
    LOCUST_SPAWN_RATE = int(os.getenv('LOCUST_SPAWN_RATE', '10'))
    
    # 安全测试配置
    SECURITY_SCAN_ENABLED = os.getenv('SECURITY_SCAN_ENABLED', 'True').lower() == 'true'
    SECURITY_SCAN_DEPTH = int(os.getenv('SECURITY_SCAN_DEPTH', '2'))
    
    # 报告配置
    REPORT_DIR = os.getenv('REPORT_DIR', 'reports')
    ALLURE_DIR = os.path.join(REPORT_DIR, 'allure')
    HTML_DIR = os.path.join(REPORT_DIR, 'html')
    
    # 测试数据配置
    DATA_DIR = os.getenv('DATA_DIR', 'data')

# 全局设置实例
settings = Settings()

# 为了兼容性，添加 Config 别名
Config = Settings