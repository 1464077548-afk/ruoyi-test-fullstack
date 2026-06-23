"""稳定性测试"""
from locust import HttpUser, task, between, tag
from config.settings import Settings


class EnduranceUser(HttpUser):
    """稳定性测试用户类"""
    wait_time = between(3, 5)
    settings = Settings()
    token = None
    
    def on_start(self):
        """初始化"""
        # 登录获取token
        response = self.client.post("/login", json={
            "username": self.settings.TEST_USERNAME,
            "password": self.settings.TEST_PASSWORD
        })
        if response.status_code == 200:
            self.token = response.json().get("data", {}).get("token")
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
    
    @tag("endurance")
    @task(10)
    def endurance_test(self):
        """稳定性测试"""
        # 模拟用户日常操作
        operations = [
            "/system/user/list?pageNum=1&pageSize=10",
            "/system/role/list?pageNum=1&pageSize=10",
            "/system/menu/list",
            "/monitor/server",
            "/monitor/jvm",
            "/monitor/cache"
        ]
        
        for operation in operations:
            self.client.get(operation)
    
    @tag("login_logout")
    @task(2)
    def login_logout_cycle(self):
        """登录登出循环"""
        # 登出
        self.client.post("/logout")
        # 重新登录
        response = self.client.post("/login", json={
            "username": self.settings.USERNAME,
            "password": self.settings.PASSWORD
        })
        if response.status_code == 200:
            self.token = response.json().get("data", {}).get("token")
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
