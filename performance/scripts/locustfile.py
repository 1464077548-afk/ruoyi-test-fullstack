"""Locust 性能测试脚本"""
from locust import HttpUser, task, between, events, run_single_user
from performance.scenarios.login_stress import LoginUser
from performance.scenarios.user_crud_load import UserCrudUser
from performance.scenarios.concurrent_api import ConcurrentApiUser
from performance.scenarios.endurance_test import EnduranceUser
from faker import Faker
import json

fake = Faker('zh_CN')
# 如果直接运行此文件，则运行单个用户进行测试

class RuoYiUser(HttpUser):
    """RuoYi 系统用户行为模拟"""
    
    wait_time = between(1, 3)  # 用户操作间隔
    host = "http://localhost:8080"
    
    def on_start(self):
        """用户开始时的初始化"""
        # 登录获取 token
        response = self.client.post("/prod-api/login", json={
            "username": "admin",
            "password": "admin123",
            "code": "",
            "uuid": ""
        })
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            self.client.headers["Authorization"] = f"Bearer {self.token}"
    
    @task(5)
    def get_user_list(self):
        """获取用户列表 - 高频操作"""
        self.client.get("/prod-api/system/user/list", 
                       params={"pageNum": 1, "pageSize": 10})
    
    @task(3)
    def get_role_list(self):
        """获取角色列表"""
        self.client.get("/prod-api/system/role/list")
    
    @task(2)
    def get_menu_list(self):
        """获取菜单列表"""
        self.client.get("/prod-api/system/menu/list")
    
    @task(1)
    def create_user(self):
        """创建用户 - 低频操作"""
        user_data = {
            "username": fake.user_name()[:20],
            "nickName": fake.name(),
            "phone": fake.phone_number()[:11],
            "email": fake.email(),
            "sex": "0",
            "status": "0"
        }
        self.client.post("/prod-api/system/user", json=user_data)
    
    @task(1)
    def search_user(self):
        """搜索用户"""
        keyword = fake.first_name()
        self.client.get("/prod-api/system/user/list",
                       params={"username": keyword})


class LoginStressUser(HttpUser):
    """登录压力测试专用用户"""
    
    wait_time = between(0.5, 1)
    host = "http://localhost:8080"
    
    @task
    def login(self):
        """持续登录请求"""
        self.client.post("/prod-api/login", json={
            "username": "admin",
            "password": "admin123",
            "code": "1234",
            "uuid": ""
        })

if __name__ == "__main__":
    run_single_user(LoginUser)
