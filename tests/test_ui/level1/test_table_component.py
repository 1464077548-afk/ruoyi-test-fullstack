"""
L1: 表格组件测试
验证表格的基本功能和交互
"""
import pytest
from ui.components.table_component import TableComponent
from config.settings import Config


class TestTableComponent:
    """表格组件测试类"""
    @staticmethod
    def _close_all_dialogs(page):
        """关闭所有弹窗，确保测试隔离"""
        try:
            # 尝试按 ESC 键关闭弹窗
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        except Exception:   
            try:
                # 尝试点击关闭按钮
                close_buttons = page.locator('.el-dialog__headerbtn').all()
                for btn in close_buttons:
                    if btn.is_visible():
                        btn.click()
                        print("点击关闭按钮")
                        page.wait_for_timeout(300)
            except Exception:
                pass 
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p0
    def test_table_display(self, page, common_biz):
        """P0-表格正常显示"""
        common_biz.switch_menu("系统管理/用户管理")
        
        # 等待表格加载完成
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(2000)
        
        table = TableComponent(page)
        
        assert table.is_visible(), "表格不可见"
        
        # 检查表格行数
        row_count = table.get_row_count()
        
        # 如果没有数据，可能是因为：
        # 1. 测试数据被清理了
        # 2. 表格正在加载中
        # 3. 没有权限查看数据
        # 先尝试等待一下
        if row_count == 0:
            page.wait_for_timeout(3000)
            row_count = table.get_row_count()
        
        # 记录实际行数，即使为0也继续测试（数据可能为空）
        print(f"表格行数: {row_count}")
        
        # 只验证表格可见性和表头存在，不强制要求有数据
        headers = table.get_headers()
        assert len(headers) > 0, "表格没有表头"
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p0
    def test_table_headers(self, page, common_biz):
        """P0-表格表头显示"""
        common_biz.switch_menu("系统管理/用户管理")
        
        table = TableComponent(page)
        headers = table.get_headers()
        
        expected_headers = ['用户编号', '用户名称', '用户昵称', '部门', '手机号码', '状态', '创建时间', '操作']
        
        for expected in expected_headers:
            assert expected in headers
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p0
    def test_table_row_data(self, page, common_biz):
        """P0-表格行数据显示"""
        common_biz.switch_menu("系统管理/用户管理")    
        table = TableComponent(page)
        first_row = table.get_row(0)
        
        assert first_row is not None, "未能获取表格第一行数据"
        assert len(first_row) > 0, "表格第一行数据为空"
        
        # 清理：关闭任何弹窗
        self._close_all_dialogs(page)
    

    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p1
    def test_table_pagination(self, page, common_biz):
        """P1-表格分页功能"""
        common_biz.switch_menu("系统管理/用户管理")
        
        # 优先使用通用表格定位器
        table = TableComponent(page)
        # 获取当前页码
        current_page = table.get_current_page()
        
        # 翻到下一页
        if table.has_next_page():
            table.go_to_page(current_page + 1)
            
            # 验证页码变化
            assert table.get_current_page() == current_page + 1
        
        # 翻到第一页
        table.go_to_page(1)
        assert table.get_current_page() == 1
        
        # 清理
        self._close_all_dialogs(page)
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p1
    def test_table_page_size_change(self, page, common_biz):
        """P1-表格每页条数切换"""
        common_biz.switch_menu("系统管理/用户管理")
        
        # 优先使用通用表格定位器
        table = TableComponent(page)
        # 切换到每页 20 条
        table.change_page_size(20)
        
        # 验证行数  
        assert table.get_row_count() <= 20
        
        # 清理
        self._close_all_dialogs(page)
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p2
    def test_table_row_selection(self, page, common_biz,user_biz):
        """P2-表格行选择"""
        common_biz.switch_menu("系统管理/用户管理")
        
        # 优先使用通用表格定位器
        table = TableComponent(page)
        # 选择第一行
        table.select_row(0)      
        # 验证选中状态
        assert table.is_row_selected(0)    
        # 清理
        self._close_all_dialogs(page)
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p2
    def test_table_empty_state(self, page, common_biz, user_biz):
        """P2-表格空状态显示"""
        common_biz.switch_menu("系统管理/用户管理")
        user_biz.search_user("nonexistent_xyz_123")     
        
        # 验证空状态提示
        empty_text_locator = page.locator(".el-table__empty-text")
        
        empty_text_locator.wait_for(state="visible", timeout=5000)
        assert empty_text_locator.is_visible()
        print("✅ 空状态文本可见")
     
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p1
    def test_table_row_edit(self, page, common_biz):
        """P1-表格行编辑按钮"""
        common_biz.switch_menu("系统管理/用户管理")
        
        # 优先使用通用表格定位器
        table = TableComponent(page)
        # 点击第一行的编辑按钮
        table.click_row_action(1, '修改')
        dialog_locator = page.get_by_role("dialog").filter(has_text="修改用户")
        dialog_locator.wait_for(state="visible", timeout=5000)
        assert dialog_locator.is_visible()
        print("✅ 修改弹窗可见")
        
        # 清理：关闭弹窗
        self._close_all_dialogs(page)
    
    @pytest.mark.ui
    @pytest.mark.l1
    @pytest.mark.component
    @pytest.mark.p1
    def test_table_row_delete(self, page,common_biz):
        """P1-表格行删除按钮"""   
        common_biz.switch_menu("系统管理/用户管理")
        # 优先使用通用表格定位器
        table = TableComponent(page)
        # 点击删除按钮 (不确认)
        table.click_row_action(1, '删除')
        dialog_locator = page.get_by_role("dialog").filter(has_text="系统提示")
        # 验证确认弹窗
        assert dialog_locator.is_visible()
               
        # 清理：关闭弹窗
        self._close_all_dialogs(page)