"""用户CRUD负载测试"""
from locust import HttpUser, task, between, tag
from config.settings import Settings
from common.utils.data_factory import DataFactory


class UserCrudUser(HttpUser):
    """用户CRUD用户类"""
    wait_time = between(2, 5)
    settings = Settings()
    token = None
    user_id = None
    
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
    
    @tag("user_list")
    @task(3)
    def get_user_list(self):
        """获取用户列表"""
        self.client.get("/system/user/list?pageNum=1&pageSize=10")
    
    @tag("user_create")
    @task(2)
    def create_user(self):
        """创建用户"""
        user_data = DataFactory.generate_user_data()
        response = self.client.post("/system/user", json=user_data)
        if response.status_code == 200:
            self.user_id = response.json().get("data", {}).get("userId")
    
    @tag("user_update")
    @task(2)
    def update_user(self):
        """更新用户"""
        if self.user_id:
            update_data = {
                "nickname": f"updated_{DataFactory.random_string(6)}",
                "email": DataFactory.random_email()
            }
            self.client.put(f"/system/user/{self.user_id}", json=update_data)
    
    @tag("user_delete")
    @task(1)
    def delete_user(self):
        """删除用户"""
        if self.user_id:
            self.client.delete(f"/system/user/{self.user_id}")
            self.user_id = None
