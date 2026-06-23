"""登录场景压力测试"""
from locust import HttpUser, task, between
from config.settings import Settings
import pytest
from pytest_loadflow import loadflow

class LoginUser(HttpUser):
    """登录用户类"""
    wait_time = between(1, 3)
    settings = Settings()
    
    @task
    def login(self):
        """登录任务"""
        self.client.post("/login", json={
            "username": self.settings.USERNAME,
            "password": self.settings.PASSWORD
        })
    
    @task
    def logout(self):
        """登出任务"""
        self.client.post("/logout")
class TestLoginStress:
    """登录压力测试"""
    
    @pytest.mark.performance
    @pytest.mark.stress
    def test_login_concurrent_100(self):
        """100 并发登录测试"""
        # 使用 pytest-loadflow 或集成 Locust
        pass
    
    @pytest.mark.performance
    @pytest.mark.stress
    def test_login_concurrent_500(self):
        """500 并发登录测试"""
        pass
    
    @pytest.mark.performance
    @pytest.mark.stress
    def test_login_concurrent_1000(self):
        """1000 并发登录测试"""
        pass