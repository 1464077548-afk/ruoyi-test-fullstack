"""并发API测试"""
from locust import HttpUser, task, between, tag
from config.settings import Settings


class ConcurrentApiUser(HttpUser):
    """并发API用户类"""
    wait_time = between(1, 2)
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
    
    @tag("api_concurrent")
    @task(5)
    def concurrent_requests(self):
        """并发请求"""
        # 同时发送多个API请求
        endpoints = [
            "/system/user/list?pageNum=1&pageSize=10",
            "/system/role/list?pageNum=1&pageSize=10",
            "/system/menu/list",
            "/monitor/server",
            "/monitor/jvm"
        ]
        
        for endpoint in endpoints:
            self.client.get(endpoint)
    
    @tag("api_mixed")
    @task(3)
    def mixed_requests(self):
        """混合请求"""
        # 混合发送GET和POST请求
        self.client.get("/system/user/list?pageNum=1&pageSize=10")
        self.client.get("/system/role/list?pageNum=1&pageSize=10")
