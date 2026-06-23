import random
import string
from datetime import datetime, timedelta
import time
import os


class DataFactory:
    """数据工厂类，用于生成测试数据"""
    
    @staticmethod
    def random_string(length=8):
        """生成随机字符串"""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def random_email():
        """生成随机邮箱"""
        prefix = DataFactory.random_string(6)
        domain = random.choice(['test.com', 'example.com', 'demo.com'])
        return f"{prefix}@{domain}"
    
    @staticmethod
    def random_phone():
        """生成随机手机号（带时间戳确保唯一性）"""
        prefix = random.choice(['130', '131', '132', '133', '134', '135', '136', '137', '138', '139'])
        # 使用时间戳的最后6位确保唯一性
        timestamp_suffix = str(int(time.time() * 1000))[-4:]
        random_suffix = ''.join(random.choice(string.digits) for _ in range(4))
        return f"{prefix}{timestamp_suffix}{random_suffix}"
    
    @staticmethod
    def random_int(min_value=1, max_value=1000):
        """生成随机整数"""
        return random.randint(min_value, max_value)
    
    @staticmethod
    def random_float(min_value=0.0, max_value=1000.0, decimal_places=2):
        """生成随机浮点数"""
        value = random.uniform(min_value, max_value)
        return round(value, decimal_places)
    
    @staticmethod
    def random_date(start_date=None, end_date=None):
        """生成随机日期"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)
    
    @staticmethod
    def random_boolean():
        """生成随机布尔值"""
        return random.choice([True, False])
    
    @staticmethod
    def random_list(items, length=3):
        """从给定列表中随机选择指定长度的子列表"""
        if len(items) <= length:
            return items.copy()
        return random.sample(items, length)
    
    @staticmethod
    def random_dict(keys, values):
        """生成随机字典"""
        if len(keys) != len(values):
            raise ValueError("Keys and values must have the same length")
        
        items = list(zip(keys, values))
        random.shuffle(items)
        return dict(items)
    
    @staticmethod
    def _get_worker_id():
        """获取当前工作器ID（用于并行执行时区分不同工作器）"""
        return os.environ.get('PYTEST_XDIST_WORKER', 'gw0')
    
    @staticmethod
    def generate_user_data(start_with="test_"):
        """生成用户测试数据（并行执行安全）"""
        worker_id = DataFactory._get_worker_id()  # 保留完整的工作器ID如gw0, gw1
        timestamp = str(int(time.time() * 1000000))[-6:]
        rand_str = DataFactory.random_string(3)
        return {
            'userName': f"{worker_id}_{start_with}{timestamp}_{rand_str}",
            'password': DataFactory.random_string(10),
            'email': f"{worker_id}_{timestamp}_{DataFactory.random_email()}",
            'phonenumber': DataFactory.random_phone(),
            'nickName': f"{worker_id}_测试用户_{timestamp}_{rand_str}",
            'status': random.choice(['0', '1'])
        }
    @staticmethod
    def generate_user_data_batch(num=2):
        """生成批量用户测试数据"""
        return [DataFactory.generate_user_data("batch_") for _ in range(num)]

    @staticmethod
    def generate_role_data():
        """生成角色测试数据（并行执行安全）"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-8:]
        return {
            'roleName': f"{worker_id}_测试角色_{timestamp}_{DataFactory.random_string(4)}",
            'roleKey': f"{worker_id}_test_{timestamp}_{DataFactory.random_string(4)}",
            'roleSort': DataFactory.random_int(1, 100),
            'status': random.choice(['0', '1']),
            'remark': f"测试角色备注_{DataFactory.random_string(10)}"
        }
    @staticmethod
    def generate_role_menu_data():
        """生成角色菜单测试数据"""
        worker_id = DataFactory._get_worker_id()
        unique_id = str(int(time.time() * 1000))
        return {
            'roleName': f"{worker_id}_权限测试角色_{unique_id}",
            'roleKey': f"{worker_id}_perm_role_{unique_id}",
            'roleSort': DataFactory.random_int(1, 100),
            'menuNames': ["用户管理", "角色管理"]  # 分配用户管理、角色管理
        }
    
    @staticmethod
    def generate_menu_data():
        """生成菜单测试数据"""
        worker_id = DataFactory._get_worker_id()
        return {
            'menuName': f"{worker_id}_测试菜单_{DataFactory.random_string(6)}",
            'parentId': '0',
            'orderNum': DataFactory.random_int(1, 100),
            'path': f"/test/{DataFactory.random_string(6)}",
            'component': f"views/test/{DataFactory.random_string(6)}/index.vue",
            'query': '',
            'visible': random.choice(['0', '1']),
            'type': random.choice(['目录', '菜单', '按钮']),
            'perms': f"test:{DataFactory.random_string(6)}",
            'icon': f"icon-{DataFactory.random_string(4)}",
            'remark': f"测试菜单备注_{DataFactory.random_string(10)}"
        }
    @staticmethod
    def generate_menu_api_data():
        """生成菜单API测试数据"""
        worker_id = DataFactory._get_worker_id()
        return {
            'menuName': f"{worker_id}_测试菜单_{DataFactory.random_string(6)}",
            'parentId': '0',
            'orderNum': DataFactory.random_int(1, 100),
            'path': f"/test/{DataFactory.random_string(6)}",
            'component': f"views/test/{DataFactory.random_string(6)}/index.vue",
            'query': '',
            'visible': random.choice(['0', '1']),
            'menuType': random.choice(['M', 'C', 'F']),
            'perms': f"test:{DataFactory.random_string(6)}",
            'icon': f"icon-{DataFactory.random_string(4)}",
            'remark': f"测试菜单备注_{DataFactory.random_string(10)}"
        }
    @staticmethod
    def generate_dept_data():
        """生成部门测试数据"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-10:]
        return {
            'deptName': f"{worker_id}_测试部门_{timestamp}_{DataFactory.random_string(6)}",
            'orderNum': DataFactory.random_int(1, 100),
            'leader': f"测试负责人_{DataFactory.random_string(4)}",
            'phone': DataFactory.random_phone(),
            'email': f"e_{timestamp}_{DataFactory.random_string(6)}@test.com",
            'status': random.choice(['0', '1']),
            'parent':"若依科技",
        }
    @staticmethod
    def generate_child_dept_data():
        """生成子部门测试数据"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-10:]
        return {
            'deptName': f"{worker_id}_测试子部门_{timestamp}_{DataFactory.random_string(6)}",
            'orderNum': DataFactory.random_int(1, 100),
            'leader': f"测试负责人_{DataFactory.random_string(4)}",
            'phone': DataFactory.random_phone(),
            'email': f"child_{timestamp}_{DataFactory.random_string(6)}@test.com",
            'status': random.choice(['0', '1']),
            'parent':"若依科技",
        }  
    @staticmethod
    def generate_job_data():
        """生成定时任务测试数据"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-8:]
        return {
            'jobName': f"{worker_id}_测试任务_{timestamp}_{DataFactory.random_string(6)}",
            'jobGroup': 'DEFAULT',
            'invokeTarget': f"ryTask.ryParams('{DataFactory.random_string(6)}')",
            'cronExpression': '0/5 * * * * ?',
            'misfirePolicy': '3',
            'concurrent': '1',
            'status': '0',
        }
    
    @staticmethod
    def generate_config_data():
        """生成配置测试数据"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-8:]
        return {
            'configName': f"{worker_id}_测试配置_{timestamp}_{DataFactory.random_string(6)}",
            'configKey': f"{worker_id}_test_{DataFactory.random_string(6)}",
            'configValue': f"{worker_id}_test_value_{DataFactory.random_string(8)}",
            'configType': random.choice(['Y', 'N']),
            'remark': f"测试配置备注_{DataFactory.random_string(10)}"
        }
    
    @staticmethod
    def generate_unique_username():
        """生成唯一的用户名"""
        return f"test_{DataFactory.random_string(6)}"
    
    @staticmethod
    def generate_dict_type_data():
        """生成字典类型测试数据"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-8:]
        return {
            'dictName': f"{worker_id}_测试字典_{timestamp}_{DataFactory.random_string(4)}",
            'dictType': f"{worker_id}_test_{timestamp}_{DataFactory.random_string(4).lower()}",
            'status': random.choice(['0', '1']),
            'remark': f"测试字典类型备注_{DataFactory.random_string(10)}"
        }
    
    @staticmethod
    def generate_dict_data():
        """生成字典数据测试数据"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-8:]
        return {
            'dictLabel': f"{worker_id}_测试标签_{timestamp}_{DataFactory.random_string(4)}",
            'dictValue': f"{worker_id}_test_{timestamp}_{DataFactory.random_string(4)}",
            'dictSort': DataFactory.random_int(1, 100),
            'status': random.choice(['0', '1']),
            'remark': f"测试字典数据备注_{DataFactory.random_string(10)}"
        }
    
    @staticmethod
    def generate_post_data(start_with="test_"):
        """生成岗位测试数据（并行执行安全）"""
        worker_id = DataFactory._get_worker_id()
        timestamp = str(int(time.time() * 1000000))[-8:]
        rand_str = DataFactory.random_string(4)
        return {
            'postName': f"{worker_id}_{start_with}_{timestamp}_{rand_str}",
            'postCode': f"{worker_id}_post_{timestamp}_{rand_str}",
            'postSort': str(DataFactory.random_int(1, 100)),
            'status': random.choice(['0', '1']),
            'remark': f"测试岗位备注_{DataFactory.random_string(10)}"
        }
    @staticmethod
    def generate_post_data_batch(num=2):
        """生成批量岗位测试数据"""
        return [DataFactory.generate_post_data(start_with="batch_") for _ in range(num)]
        
