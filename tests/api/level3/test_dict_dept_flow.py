"""L3: 字典和部门业务流测试"""
import pytest
from api.clients.dict_client import DictClient
from api.clients.dept_client import DeptClient
from api.clients.user_client import UserClient
from common.utils.data_factory import DataFactory


class TestDictDeptFlow:
    """字典和部门业务流测试类"""
    
    @pytest.mark.api
    @pytest.mark.l3
    @pytest.mark.e2e
    @pytest.mark.p0
    def test_dict_dept_user_integration(self, dict_client, dept_client, user_client):
        """P0-字典、部门、用户集成流程"""
        # 1. 创建字典类型
        dict_type_data = {
            "dictName": "部门状态",
            "dictType": f"dept_status_{DataFactory.random_string(6).lower()}",
            "status": "0",
            "remark": "部门状态字典"
        }
        create_dict_type_response = dict_client.create_dict_type(dict_type_data)
        assert create_dict_type_response.get("code") == 200
        
        # 2. 查询字典类型列表获取dictId
        dict_type_list = dict_client.get_dict_type_list(dictType=dict_type_data.get("dictType"))
        assert dict_type_list.get("code") == 200
        assert len(dict_type_list.get("rows", [])) > 0
        dict_id = dict_type_list.get("rows")[0].get("dictId")
        assert dict_id
        
        # 3. 创建字典数据
        dict_data = {
            "dictType": dict_type_data["dictType"],
            "dictLabel": "正常",
            "dictValue": "0",
            "status": "0",
            "remark": "正常状态"
        }
        create_dict_data_response = dict_client.create_dict_data(dict_data)
        assert create_dict_data_response.get("code") == 200
        
        # 4. 获取部门列表，选择父部门
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        parent_dept_id = depts[0].get("deptId")
        assert parent_dept_id
        
        # 5. 创建部门
        dept_data = {
            "deptName": f"测试部门_{DataFactory.random_string(6)}",
            "parentId": parent_dept_id,
            "orderNum": 100,
            "status": "0",
            "leader": "测试负责人",
            "phone": "13800138000",
            "email": "test@example.com",
            "remark": "测试部门"
        }
        create_dept_response = dept_client.create_dept(dept_data)
        assert create_dept_response.get("code") == 200
        
        # 6. 获取部门列表，找到创建的部门
        dept_list_after_create = dept_client.get_dept_list()
        assert dept_list_after_create.get("code") == 200
        created_dept = None
        for dept in dept_list_after_create.get("data", []):
            if dept.get("deptName") == dept_data["deptName"]:
                created_dept = dept
                break
        assert created_dept is not None
        dept_id = created_dept.get("deptId")
        assert dept_id
        
        # 7. 创建用户并分配到该部门
        user_data = DataFactory.generate_user_data()
        user_data["deptId"] = dept_id
        create_user_response = user_client.create_user(user_data)
        assert create_user_response.get("code") == 200
        
        # 8. 查询用户列表获取userId
        user_list_response = user_client.get_user_list(userName=user_data.get("userName"))
        assert user_list_response.get("code") == 200
        assert len(user_list_response.get("rows", [])) > 0
        user_id = user_list_response.get("rows")[0].get("userId")
        assert user_id
        
        try:
            # 9. 验证用户信息
            user_detail = user_client.get_user_by_id(user_id)
            assert user_detail.get("code") == 200
            assert user_detail.get("data", {}).get("deptId") == dept_id
            
            # 10. 验证部门信息
            dept_detail = dept_client.get_dept(dept_id)
            assert dept_detail.get("code") == 200
            assert dept_detail.get("data", {}).get("deptName") == dept_data["deptName"]
            
            # 11. 验证字典数据
            dict_by_type = dict_client.get_dicts_by_type(dict_type_data["dictType"])
            assert dict_by_type.get("code") == 200
            assert isinstance(dict_by_type.get("data"), list)
            
        finally:
            # 12. 清理：删除用户
            if user_id:
                user_client.delete_user(user_id)
            
            # 13. 清理：删除部门
            if dept_id:
                dept_client.delete_dept(dept_id)
            
            # 14. 清理：删除字典数据
            dict_data_list = dict_client.get_dict_data_list(dictType=dict_type_data["dictType"])
            if dict_data_list.get("code") == 200:
                for item in dict_data_list.get("rows", []):
                    dict_client.delete_dict_data(item.get("dictCode"))
            
            # 15. 清理：删除字典类型
            if dict_id:
                dict_client.delete_dict_type(dict_id)
    
    @pytest.mark.api
    @pytest.mark.l3
    @pytest.mark.e2e
    @pytest.mark.p1
    def test_dept_hierarchy_flow(self, dept_client):
        """P1-部门层次结构流程测试"""
        # 1. 获取根部门列表
        dept_list = dept_client.get_dept_list()
        assert dept_list.get("code") == 200
        depts = dept_list.get("data", [])
        assert len(depts) > 0
        root_dept = depts[0]
        root_dept_id = root_dept.get("deptId")
        assert root_dept_id
        
        # 2. 创建一级子部门
        level1_dept_data = {
            "deptName": f"一级部门_{DataFactory.random_string(6)}",
            "parentId": root_dept_id,
            "orderNum": 100,
            "status": "0",
            "leader": "一级部门负责人",
            "phone": "13800138001",
            "email": "level1@example.com",
            "remark": "一级部门"
        }
        create_level1_response = dept_client.create_dept(level1_dept_data)
        assert create_level1_response.get("code") == 200
        
        # 3. 获取部门列表，找到创建的一级部门
        dept_list_after_level1 = dept_client.get_dept_list()
        assert dept_list_after_level1.get("code") == 200
        level1_dept = None
        for dept in dept_list_after_level1.get("data", []):
            if dept.get("deptName") == level1_dept_data["deptName"]:
                level1_dept = dept
                break
        assert level1_dept is not None
        level1_dept_id = level1_dept.get("deptId")
        assert level1_dept_id
        
        # 4. 创建二级子部门
        level2_dept_data = {
            "deptName": f"二级部门_{DataFactory.random_string(6)}",
            "parentId": level1_dept_id,
            "orderNum": 200,
            "status": "0",
            "leader": "二级部门负责人",
            "phone": "13800138002",
            "email": "level2@example.com",
            "remark": "二级部门"
        }
        create_level2_response = dept_client.create_dept(level2_dept_data)
        assert create_level2_response.get("code") == 200
        
        # 5. 获取部门列表，找到创建的二级部门
        dept_list_after_level2 = dept_client.get_dept_list()
        assert dept_list_after_level2.get("code") == 200
        level2_dept = None
        for dept in dept_list_after_level2.get("data", []):
            if dept.get("deptName") == level2_dept_data["deptName"]:
                level2_dept = dept
                break
        assert level2_dept is not None
        level2_dept_id = level2_dept.get("deptId")
        assert level2_dept_id
        
        try:
            # 6. 验证部门层次结构
            dept_hierarchy = dept_client.get_dept_list()
            assert dept_hierarchy.get("code") == 200
            
            # 7. 验证一级部门的父部门是根部门
            assert level1_dept.get("parentId") == root_dept_id
            
            # 8. 验证二级部门的父部门是一级部门
            assert level2_dept.get("parentId") == level1_dept_id
            
        finally:
            # 9. 清理：删除二级部门
            if level2_dept_id:
                dept_client.delete_dept(level2_dept_id)
            
            # 10. 清理：删除一级部门
            if level1_dept_id:
                dept_client.delete_dept(level1_dept_id)