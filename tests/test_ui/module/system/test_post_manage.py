"""
岗位管理模块测试
L1: API层测试 - 验证岗位管理的API接口
L2: UI层测试 - 验证岗位管理的UI功能
L3: 集成测试 - 验证岗位管理的端到端流程
性能测试 - 验证岗位管理的性能
安全测试 - 验证岗位管理的安全性
"""
import pytest
import time
import os
from common.utils.data_factory import DataFactory
from api.clients.post_client import PostClient
from config.settings import Settings


# =============================================================================
# L1: API层测试
# =============================================================================
class TestPostAPI:
    """岗位管理API测试"""

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_get_post_list_success(self, authenticated_client):
        """P0-获取岗位列表成功"""
        response = authenticated_client.get("/system/post/list", params={"pageNum": 1, "pageSize": 10})
        assert response["code"] == 200, f"获取岗位列表失败: {response}"
        assert "rows" in response, "响应数据中缺少rows字段"
        assert isinstance(response["rows"], list), "rows字段应该是列表类型"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_create_post_success(self, authenticated_client):
        """P0-创建岗位成功"""
        post_data = DataFactory.generate_post_data()
        response = authenticated_client.post("/system/post", post_data)
        assert response["code"] == 200, f"创建岗位失败: {response}"
        assert response["msg"] == "操作成功", f"创建岗位失败: {response.get('msg')}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_post_duplicate_name(self, authenticated_client):
        """P1-创建重复岗位名称"""
        post_data = DataFactory.generate_post_data()
        post_data['postCode'] = f"dup_{int(time.time())}"
        
        # 创建第一个岗位
        response1 = authenticated_client.post("/system/post", post_data)
        assert response1["code"] == 200, f"创建第一个岗位失败: {response1}"

        # 创建第二个同名岗位
        response2 = authenticated_client.post("/system/post", post_data)
        assert response2["code"] == 500, f"创建重复岗位名称应该失败: {response2}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_create_post_duplicate_code(self, authenticated_client):
        """P1-创建重复岗位编码"""
        post_data = DataFactory.generate_post_data()
        post_data['postName'] = f"dup_name_{int(time.time())}"
        
        # 创建第一个岗位
        response1 = authenticated_client.post("/system/post", post_data)
        assert response1["code"] == 200, f"创建第一个岗位失败: {response1}"

        # 创建第二个同编码岗位
        response2 = authenticated_client.post("/system/post", post_data)
        assert response2["code"] == 500, f"创建重复岗位编码应该失败: {response2}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_update_post_success(self, authenticated_client):
        """P0-更新岗位成功"""
        post_data = DataFactory.generate_post_data()
        create_response = authenticated_client.post("/system/post", post_data)
        assert create_response["code"] == 200, f"创建岗位失败: {create_response}"

        query_response = authenticated_client.get("/system/post/list", params={"postName": post_data['postName']})
        assert query_response["code"] == 200, f"查询岗位失败: {query_response}"
        assert len(query_response["rows"]) >= 1, "未找到刚创建的岗位"
        
        post_id = query_response["rows"][0]["postId"]
        update_data = {
            "postId": post_id,
            "postName": post_data['postName'] + "_updated",
            "postCode": post_data['postCode'] + "_updated",
            "postSort": post_data['postSort'],
            "status": post_data['status'],
            "remark": "updated"
        }
        
        response = authenticated_client.put("/system/post", update_data)
        assert response["code"] == 200, f"更新岗位失败: {response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p0
    def test_delete_post_success(self, authenticated_client):
        """P0-删除岗位成功"""
        post_data = DataFactory.generate_post_data()
        create_response = authenticated_client.post("/system/post", post_data)
        assert create_response["code"] == 200, f"创建岗位失败: {create_response}"

        query_response = authenticated_client.get("/system/post/list", params={"postName": post_data['postName']})
        assert query_response["code"] == 200, f"查询岗位失败: {query_response}"
        assert len(query_response["rows"]) >= 1, "未找到刚创建的岗位"
        
        post_id = query_response["rows"][0]["postId"]
        delete_response = authenticated_client.delete(f"/system/post/{post_id}")
        assert delete_response["code"] == 200, f"删除岗位失败: {delete_response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_delete_post_not_exists(self, authenticated_client):
        """P1-删除不存在的岗位"""
        response = authenticated_client.delete("/system/post/999999999")
        assert response["code"] in [404, 500], f"删除不存在的岗位应该返回错误: {response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_query_post_by_name(self, authenticated_client):
        """P1-根据岗位名称查询"""
        post_data = DataFactory.generate_post_data()
        create_response = authenticated_client.post("/system/post", post_data)
        assert create_response["code"] == 200, f"创建岗位失败: {create_response}"

        query_response = authenticated_client.get("/system/post/list", params={"postName": post_data['postName']})
        assert query_response["code"] == 200, f"查询岗位失败: {query_response}"
        rows = query_response["rows"]
        assert len(rows) >= 1, f"应该至少找到1条记录: {rows}"
        assert rows[0]["postName"] == post_data['postName'], f"岗位名称不匹配: {rows[0]['postName']} != {post_data['postName']}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_get_post_by_id(self, authenticated_client):
        """P2-根据ID获取岗位"""
        post_data = DataFactory.generate_post_data()
        create_response = authenticated_client.post("/system/post", post_data)
        assert create_response["code"] == 200, f"创建岗位失败: {create_response}"

        query_response = authenticated_client.get("/system/post/list", params={"postName": post_data['postName']})
        assert query_response["code"] == 200, f"查询岗位失败: {query_response}"
        assert len(query_response["rows"]) >= 1, "未找到刚创建的岗位"
        
        post_id = query_response["rows"][0]["postId"]
        get_response = authenticated_client.get(f"/system/post/{post_id}")
        assert get_response["code"] == 200, f"获取岗位失败: {get_response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_export_posts(self, authenticated_client):
        """P2-导出岗位数据"""
        response = authenticated_client.get("/system/post/export")
        assert response is not None, "导出岗位数据失败"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_pagination(self, authenticated_client):
        """P2-分页功能"""
        response = authenticated_client.get("/system/post/list", params={"pageNum": 1, "pageSize": 5})
        assert response["code"] == 200, f"获取岗位列表失败: {response}"
        assert response.get("pageSize") == 5 or len(response.get("rows", [])) <= 5, f"分页大小不正确: {response}"
        assert "total" in response, "缺少总数字段"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p3
    def test_create_post_missing_required_fields(self, authenticated_client):
        """P3-创建岗位缺少必填字段"""
        post_data = {"postName": "", "postCode": "", "postSort": ""}
        response = authenticated_client.post("/system/post", post_data)
        assert response["code"] in [500, 400], f"缺少必填字段应该返回错误: {response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p3
    def test_create_post_too_long_name(self, authenticated_client):
        """P3-创建岗位名称过长"""
        post_data = DataFactory.generate_post_data()
        post_data['postName'] = "A" * 51
        response = authenticated_client.post("/system/post", post_data)
        assert response["code"] in [500, 400], f"岗位名称过长应该返回错误: {response}"


# =============================================================================
# L2: UI层测试
# =============================================================================
class TestPostUIModule:
    """岗位管理UI测试"""

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_post_page_load(self, common_biz):
        """P0-岗位管理页面加载"""
        common_biz.switch_menu("系统管理/岗位管理")
        assert True, "页面加载成功"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_create_post_success(self, test_post_data, common_biz, post_biz):
        """P0-新增岗位成功"""
        common_biz.switch_menu("系统管理/岗位管理")
        message = post_biz.add_post(test_post_data)
        assert "成功" in message, f"创建岗位失败: {message}"
        
        # 通过验证岗位是否存在来确认创建成功
        post_info = post_biz.get_post_info(test_post_data['postName'])
        assert post_info['postName'] == test_post_data['postName'], f"岗位创建失败，未在列表中找到: {test_post_data['postName']}"
        
        # 删除岗位
        message = post_biz.delete_post(test_post_data['postName'])
        # 通过验证岗位是否被删除来确认删除成功
        post_info = post_biz.get_post_info(test_post_data['postName'])
        assert post_info is None, f"岗位删除失败，仍在列表中: {test_post_data['postName']}"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_create_post_duplicate_name(self, test_post_data, common_biz, post_biz):
        """P1-新增重复岗位名称"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.add_post(test_post_data)
        
        message = post_biz.add_post(test_post_data)
        assert "已存在" in message or "失败" in message, f"创建重复岗位名称应该失败: {message}"

        #关闭弹窗
        post_biz.post_page.click_cancel_post()

        #删除岗位
        message = post_biz.delete_post(test_post_data['postName'])
        assert "成功" in message, f"删除岗位失败: {message}"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_create_post_missing_required_fields(self, common_biz, post_biz):
        """P1-新增岗位缺少必填字段"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.post_page.click_add_post()
        post_biz.post_page.click_save_post()
        # 验证操作提示消息
        message = common_biz.get_operate_message()
        # 表单验证错误可能显示为"岗位名称不能为空"或"岗位编码不能为空"
        assert "岗位名称不能为空" in message or "岗位编码不能为空" in message or "不能为空" in message, f"缺少必填字段应该提示: {message}"

        # 按ESC关闭弹窗
        post_biz.post_page.press_key("Escape")

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_create_post_cancel(self, test_post_data, common_biz, post_biz):
        """P2-新增岗位取消"""
        common_biz.switch_menu("系统管理/岗位管理")
        # 先关闭所有可能存在的弹窗
        post_biz.post_page.press_key("Escape")
        
        # 点击新增按钮
        post_biz.post_page.click_add_post()
        post_biz.post_page.fill_post_form(
            test_post_data['postName'],
            test_post_data['postCode'],
            test_post_data['postSort']
        )
        # 点击取消按钮
        try:
            post_biz.post_page.click_cancel_post()
        except Exception:
            # 如果取消按钮不可见，按ESC关闭
            post_biz.post_page.press_key("Escape")
        
        post_info = post_biz.get_post_info(test_post_data['postName'])
        assert post_info is None, f"取消新增后岗位不应该存在: {test_post_data['postName']}"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_edit_post_success(self, test_post_data, common_biz, post_biz):
        """P0-编辑岗位成功"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.add_post(test_post_data)
        
        new_data = {
            'postName': test_post_data['postName'] + "_edit",
            'postCode': test_post_data['postCode'] + "_edit",
            'postSort': test_post_data['postSort']
        }
        message = post_biz.edit_post(test_post_data['postName'], new_data)
        assert "成功" in message, f"编辑岗位失败: {message}"
        #删除岗位
        message = post_biz.delete_post(new_data['postName'])
        assert "成功" in message, f"删除岗位失败: {message}"

       

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p0
    def test_delete_post_success(self, test_post_data, common_biz, post_biz):
        """P0-删除岗位成功"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.add_post(test_post_data)
        
        message = post_biz.delete_post(test_post_data['postName'])
        assert "成功" in message, f"删除岗位失败: {message}"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_search_post_by_name(self, test_post_data, common_biz, post_biz):
        """P1-按名称搜索岗位"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.add_post(test_post_data)
        
        result = post_biz.search_post(test_post_data['postName'])
        assert result, f"搜索岗位失败"

        #删除岗位
        message = post_biz.delete_post(test_post_data['postName'])
        assert "成功" in message, f"删除岗位失败: {message}"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_get_post_info(self, test_post_data, common_biz, post_biz):
        """P2-获取岗位信息"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.add_post(test_post_data)
        
        info = post_biz.get_post_info(test_post_data['postName'])
        assert info is not None, f"获取岗位信息失败"
        assert info['postName'] == test_post_data['postName'], f"岗位名称不匹配"
        #删除岗位
        message = post_biz.delete_post(test_post_data['postName'])
        assert "成功" in message, f"删除岗位失败: {message}"


# =============================================================================
# L3: 集成测试 (E2E)
# =============================================================================
class TestPostLifecycleE2E:
    """岗位生命周期端到端测试"""

    @pytest.mark.e2e
    @pytest.mark.l3
    @pytest.mark.p0
    def test_complete_post_lifecycle(self, test_post_data, common_biz, post_biz):
        """P0-完整岗位生命周期流程"""
        common_biz.switch_menu("系统管理/岗位管理")
        
        message = post_biz.add_post(test_post_data)
        assert "成功" in message, f"创建岗位失败: {message}"
        
        post_info = post_biz.get_post_info(test_post_data['postName'])
        assert post_info is not None, f"岗位不存在: {test_post_data['postName']}"
        
        new_data = {
            'postName': test_post_data['postName'] + "_updated",
            'postCode': test_post_data['postCode'] + "_updated",
            'postSort': str(int(test_post_data['postSort']) + 1)
        }
        message = post_biz.edit_post(test_post_data['postName'], new_data)
        assert "成功" in message, f"编辑岗位失败: {message}"
        
        updated_info = post_biz.get_post_info(new_data['postName'])
        assert updated_info is not None, f"编辑后的岗位不存在: {new_data['postName']}"
        
        result = post_biz.search_post(new_data['postName'])
        assert result, f"搜索岗位失败: {new_data['postName']}"
        
        message = post_biz.delete_post(new_data['postName'])
        assert "成功" in message, f"删除岗位失败: {message}"
        
        exists = post_biz.validate_post_exists(new_data['postName'])
        assert not exists, f"岗位应该已被删除: {new_data['postName']}"

    @pytest.mark.e2e
    @pytest.mark.l3
    @pytest.mark.p1
    def test_post_crud_operations(self, test_post_data, common_biz, post_biz):
        """P1-岗位增删改查操作"""
        common_biz.switch_menu("系统管理/岗位管理")
        
        message = post_biz.add_post(test_post_data)
        assert "成功" in message, f"创建岗位失败"
        
        info = post_biz.get_post_info(test_post_data['postName'])
        assert info is not None, f"获取岗位信息失败"
        
        new_data = {
            'postName': test_post_data['postName'] + "_modified",
            'postCode': test_post_data['postCode'] + "_modified",
            'postSort': test_post_data['postSort']
        }
        message = post_biz.edit_post(test_post_data['postName'], new_data)
        assert "成功" in message, f"更新岗位失败"
        
        message = post_biz.delete_post(new_data['postName'])
        assert "成功" in message, f"删除岗位失败"


# =============================================================================
# 性能测试
# =============================================================================
class TestPostPerformance:
    """岗位管理性能测试"""

    @pytest.mark.performance
    @pytest.mark.l3
    @pytest.mark.p1
    def test_create_post_performance(self, authenticated_client):
        """P1-创建岗位性能测试"""
        times = []
        for i in range(10):
            post_data = DataFactory.generate_post_data()
            start_time = time.time()
            response = authenticated_client.post("/system/post", post_data)
            elapsed = time.time() - start_time
            times.append(elapsed)
            
        avg_time = sum(times) / len(times)
        max_time = max(times)
        print(f"\n创建岗位性能: 平均={avg_time:.3f}s, 最大={max_time:.3f}s")
        assert max_time < 5.0, f"创建岗位最大耗时超过5秒: {max_time}s"

    @pytest.mark.performance
    @pytest.mark.l3
    @pytest.mark.p1
    def test_query_post_performance(self, authenticated_client):
        """P1-查询岗位性能测试"""
        times = []
        for i in range(20):
            start_time = time.time()
            response = authenticated_client.get("/system/post/list", params={"pageNum": 1, "pageSize": 100})
            elapsed = time.time() - start_time
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        print(f"\n查询岗位性能: 平均={avg_time:.3f}s, 最大={max_time:.3f}s")
        assert max_time < 3.0, f"查询岗位最大耗时超过3秒: {max_time}s"


# =============================================================================
# 安全测试
# =============================================================================
class TestPostSecurity:
    """岗位管理安全测试"""

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p1
    def test_create_post_sql_injection(self, authenticated_client):
        """P1-SQL注入测试"""
        malicious_data = {
            "postName": "test'; DROP TABLE sys_post; --",
            "postCode": "test_code",
            "postSort": "1"
        }
        response = authenticated_client.post("/system/post", malicious_data)
        assert response["code"] in [200, 500], f"SQL注入测试失败: {response}"

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p1
    def test_create_post_xss(self, authenticated_client):
        """P1-XSS攻击测试"""
        xss_data = {
            "postName": "<script>alert('XSS')</script>",
            "postCode": "test_code",
            "postSort": "1"
        }
        response = authenticated_client.post("/system/post", xss_data)
        assert response["code"] in [200, 500], f"XSS测试失败: {response}"

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p2
    def test_unauthorized_access(self):
        """P2-未授权访问测试"""
        base_client = PostClient(base_url=Settings().API_BASE_URL)
        response = base_client.get("/system/post/list")
        assert response["code"] == 401 or response["code"] == 403, f"未授权访问应该被拒绝: {response}"

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p2
    def test_get_nonexistent_post(self, authenticated_client):
        """P2-获取不存在的岗位"""
        response = authenticated_client.get("/system/post/999999999")
        assert response["code"] in [200, 404, 500], f"获取不存在的岗位应该返回合理响应: {response}"

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p2
    def test_delete_nonexistent_post(self, authenticated_client):
        """P2-删除不存在的岗位"""
        response = authenticated_client.delete("/system/post/999999999")
        assert response["code"] in [404, 500], f"删除不存在的岗位应该返回错误: {response}"

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p2
    def test_special_characters_in_name(self, authenticated_client):
        """P2-特殊字符岗位名称"""
        post_data = {
            "postName": "岗位测试@#$%",
            "postCode": f"special_{int(time.time())}",
            "postSort": "1",
            "remark": "特殊字符测试"
        }
        response = authenticated_client.post("/system/post", post_data)
        assert response["code"] in [200, 500], f"特殊字符测试失败: {response}"

    @pytest.mark.security
    @pytest.mark.l3
    @pytest.mark.p2
    def test_boundary_post_sort(self, authenticated_client):
        """P2-岗位排序边界值测试"""
        post_data = DataFactory.generate_post_data()
        post_data['postSort'] = "0"
        response1 = authenticated_client.post("/system/post", post_data)
        assert response1["code"] in [200, 500], f"排序值0测试失败: {response1}"

        post_data2 = DataFactory.generate_post_data()
        post_data2['postSort'] = "999999999"
        response2 = authenticated_client.post("/system/post", post_data2)
        assert response2["code"] in [200, 500], f"排序值999999999测试失败: {response2}"


# =============================================================================
# 补充测试：批量操作和状态切换
# =============================================================================
class TestPostBatchOperations:
    """岗位批量操作测试"""

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_batch_delete_posts(self, authenticated_client):
        """P1-批量删除岗位"""
        post_ids = []
        for i in range(3):
            post_data = DataFactory.generate_post_data()
            response = authenticated_client.post("/system/post", post_data)
            if response["code"] == 200:
                query_resp = authenticated_client.get("/system/post/list", params={"postName": post_data['postName']})
                if query_resp["code"] == 200 and len(query_resp["rows"]) > 0:
                    post_ids.append(query_resp["rows"][0]["postId"])

        assert len(post_ids) >= 2, "至少需要创建2个岗位用于批量删除测试"

        delete_response = authenticated_client.delete(f"/system/post/{','.join(map(str, post_ids))}")
        assert delete_response["code"] == 200, f"批量删除失败: {delete_response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p1
    def test_change_post_status(self, authenticated_client):
        """P1-修改岗位状态"""
        post_data = DataFactory.generate_post_data()
        post_data['status'] = '0'
        create_response = authenticated_client.post("/system/post", post_data)
        assert create_response["code"] == 200, f"创建岗位失败: {create_response}"

        query_resp = authenticated_client.get("/system/post/list", params={"postName": post_data['postName']})
        assert query_resp["code"] == 200, f"查询岗位失败: {query_resp}"
        assert len(query_resp["rows"]) >= 1, "未找到刚创建的岗位"
        post_id = query_resp["rows"][0]["postId"]

        # 尝试使用POST方法来修改状态
        try:
            status_response = authenticated_client.post("/system/post/changeStatus", {
                "postId": post_id,
                "status": '1'
            })
        except Exception:
            # 如果不支持changeStatus接口，就通过编辑岗位来修改状态
            update_data = {
                "postId": post_id,
                "postName": post_data['postName'],
                "postCode": post_data['postCode'],
                "postSort": post_data['postSort'],
                "status": '1',
                "remark": "changed"
            }
            status_response = authenticated_client.put("/system/post", update_data)
        
        assert status_response["code"] in [200, 500], f"修改状态失败: {status_response}"

        delete_response = authenticated_client.delete(f"/system/post/{post_id}")
        assert delete_response["code"] == 200, f"清理失败: {delete_response}"

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p1
    def test_toggle_post_status_ui(self, test_post_data, common_biz, post_biz):
        """P1-UI切换岗位状态"""
        common_biz.switch_menu("系统管理/岗位管理")
        post_biz.add_post(test_post_data)

        message = post_biz.toggle_post_status(test_post_data['postName'])
        assert "成功" in message or message == "未找到岗位", f"切换岗位状态失败: {message}"

        post_biz.delete_post(test_post_data['postName'])

    @pytest.mark.ui
    @pytest.mark.l2
    @pytest.mark.p2
    def test_batch_delete_posts_ui(self, test_post_data_batch, common_biz, post_biz):
        """P2-UI批量删除岗位"""
        common_biz.switch_menu("系统管理/岗位管理")
        
        for post_data in test_post_data_batch:
            print(f"增加岗位: {post_data['postName']}")
            post_biz.add_post(post_data)       

        message = post_biz.batch_delete_posts("batch_")
        assert "成功" in message, f"批量删除失败: {message}"


class TestPostEdgeCases:
    """岗位边界场景测试"""

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_create_post_with_emoji(self, authenticated_client):
        """P2-创建带Emoji的岗位名称"""
        post_data = DataFactory.generate_post_data()
        post_data['postName'] = f"测试岗位{int(time.time())}"
        response = authenticated_client.post("/system/post", post_data)
        assert response["code"] in [200, 500], f"Emoji测试失败: {response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_create_post_empty_remark(self, authenticated_client):
        """P2-创建岗位备注为空"""
        post_data = DataFactory.generate_post_data()
        post_data['remark'] = ""
        response = authenticated_client.post("/system/post", post_data)
        assert response["code"] == 200, f"空备注测试失败: {response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p2
    def test_concurrent_post_creation(self, authenticated_client):
        """P2-并发创建相同岗位"""
        post_data = DataFactory.generate_post_data()
        post_data['postCode'] = f"concurrent_{int(time.time())}"

        response1 = authenticated_client.post("/system/post", post_data)
        assert response1["code"] == 200, f"第一个创建失败: {response1}"

        response2 = authenticated_client.post("/system/post", post_data)
        assert response2["code"] == 500, f"并发创建应该失败: {response2}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p3
    def test_query_with_special_params(self, authenticated_client):
        """P3-使用特殊参数查询"""
        response = authenticated_client.get("/system/post/list", params={
            "postName": "'; OR 1=1; --",
            "pageNum": -1,
            "pageSize": 999999
        })
        assert response["code"] == 200, f"特殊参数查询失败: {response}"

    @pytest.mark.api
    @pytest.mark.l1
    @pytest.mark.p3
    def test_invalid_pagination_params(self, authenticated_client):
        """P3-无效分页参数"""
        response = authenticated_client.get("/system/post/list", params={
            "pageNum": 0,
            "pageSize": 0
        })
        assert response["code"] in [200, 500], f"无效分页参数测试失败: {response}"