import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).parent.parent


load_dotenv(override=False)


ENVIRONMENT_FILE = PROJECT_ROOT / "config" / "environments.yaml"


class Settings(BaseSettings):
    TEST_ENV: str = os.getenv("TEST_ENV", "development")
    
    BASE_URL: str = "http://localhost:8081"
    API_BASE_URL: str = "http://localhost:8080"
    
    TEST_USERNAME: str = "admin"
    TEST_PASSWORD: str = "admin123"
    
    BROWSER: str = "chromium"
    HEADLESS: bool = False
    SLOW_MO: int = 0
    
    PAGE_LOAD_TIMEOUT: int = 30
    ELEMENT_TIMEOUT: int = 10
    UI_TIMEOUT: int = 60000
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "ry-vue"
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "123456"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    LOCUST_HOST: str = "http://localhost:8080"
    LOCUST_USERS: int = 100
    LOCUST_SPAWN_RATE: int = 10
    
    SECURITY_SCAN_ENABLED: bool = True
    SECURITY_SCAN_DEPTH: int = 2
    
    REPORT_DIR: str = "reports"
    DATA_DIR: str = "data"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._convert_ui_timeout()
        self._apply_environment_config()

    def _convert_ui_timeout(self):
        env_ui_timeout = os.getenv("UI_TIMEOUT")
        if env_ui_timeout is not None:
            try:
                self.UI_TIMEOUT = int(env_ui_timeout) * 1000
            except ValueError:
                pass

    def _apply_environment_config(self):
        if not ENVIRONMENT_FILE.exists():
            print(f"⚠️ 环境配置文件不存在: {ENVIRONMENT_FILE}")
            return

        try:
            with open(ENVIRONMENT_FILE, "r", encoding="utf-8") as f:
                env_config = yaml.safe_load(f)

            environments = env_config.get("environments", {})
            if self.TEST_ENV not in environments:
                print(f"⚠️ 环境 '{self.TEST_ENV}' 配置不存在，使用默认配置")
                return

            env_settings = environments[self.TEST_ENV]
            print(f"📋 加载环境配置: {self.TEST_ENV}")

            config_mapping = {
                "base_url": "BASE_URL",
                "api_base_url": "API_BASE_URL",
                "username": "TEST_USERNAME",
                "password": "TEST_PASSWORD",
                "browser": "BROWSER",
                "headless": "HEADLESS",
                "db_host": "DB_HOST",
                "db_port": "DB_PORT",
                "db_name": "DB_NAME",
                "db_username": "DB_USERNAME",
                "db_password": "DB_PASSWORD",
                "redis_host": "REDIS_HOST",
                "redis_port": "REDIS_PORT",
            }

            for yaml_key, attr_key in config_mapping.items():
                if yaml_key in env_settings:
                    env_var_name = attr_key
                    if os.getenv(env_var_name) is None:
                        setattr(self, attr_key, env_settings[yaml_key])

        except Exception as e:
            print(f"⚠️ 加载环境配置失败: {e}")

    @property
    def base_url(self):
        return self.BASE_URL

    @property
    def api_base_url(self):
        return self.API_BASE_URL

    @property
    def USERNAME(self):
        return self.TEST_USERNAME

    @property
    def PASSWORD(self):
        return self.TEST_PASSWORD

    @property
    def ALLURE_DIR(self):
        return os.path.join(self.REPORT_DIR, "allure")

    @property
    def HTML_DIR(self):
        return os.path.join(self.REPORT_DIR, "html")

    def print_config(self):
        print("\n" + "="*60)
        print(f"当前环境: {self.TEST_ENV}")
        print("="*60)
        print(f"服务配置:")
        print(f"  BASE_URL: {self.BASE_URL}")
        print(f"  API_BASE_URL: {self.API_BASE_URL}")
        print(f"\n认证配置:")
        print(f"  USERNAME: {self.TEST_USERNAME}")
        print(f"  PASSWORD: {'*' * len(self.TEST_PASSWORD)}")
        print(f"\n浏览器配置:")
        print(f"  BROWSER: {self.BROWSER}")
        print(f"  HEADLESS: {self.HEADLESS}")
        print(f"\n数据库配置:")
        print(f"  DB_HOST: {self.DB_HOST}")
        print(f"  DB_PORT: {self.DB_PORT}")
        print(f"  DB_NAME: {self.DB_NAME}")
        print(f"\n超时配置:")
        print(f"  UI_TIMEOUT: {self.UI_TIMEOUT}ms")
        print("="*60 + "\n")


settings = Settings()

Config = Settings