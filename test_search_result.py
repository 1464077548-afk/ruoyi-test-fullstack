#!/usr/bin/env python3
"""测试搜索结果数量计算"""
from ui.biz.common_biz import CommonBiz
from ui.pages.modules.user_page import UserPage
from playwright.sync_api import sync_playwright


def test_search_result_count():
    """测试搜索结果数量计算"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # 登录
            page.goto("http://localhost:8081/login")
            page.fill("input[placeholder='账号']", "admin")
            page.fill("input[placeholder='密码']", "admin123")
            page.fill("input[placeholder='验证码']", "skip_captcha")
            page.click("button:has-text('登 录')")
            page.wait_for_load_state("domcontentloaded")
            
            # 导航到用户管理页面
            common_biz = CommonBiz(page)
            common_biz.switch_menu("系统管理/用户管理")
            
            # 测试正常搜索
            user_page = UserPage(page)
            print("\n=== 测试正常搜索 'admin' ===")
            result_count = common_biz.common_search(user_page, "admin")
            print(f"正常搜索 'admin' 结果数量: {result_count}")
            
            # 测试 SQL 注入 payload
            print("\n=== 测试 SQL 注入 payload ===")
            sql_payload = "' OR '1'='1"
            result_count = common_biz.common_search(user_page, sql_payload)
            print(f"SQL 注入 payload 结果数量: {result_count}")
            
            # 测试不存在的用户
            print("\n=== 测试不存在的用户 ===")
            result_count = common_biz.common_search(user_page, "nonexistent_user_123456")
            print(f"不存在用户搜索结果数量: {result_count}")
            
            # 检查页面内容，看看是否有用户数据
            print("\n=== 检查页面内容 ===")
            page_content = page.content()
            print(f"页面中是否包含 'admin': {'admin' in page_content}")
            print(f"页面中是否包含 '暂无数据': {'暂无数据' in page_content}")
            print(f"页面中是否包含 'el-table__empty-text': {'el-table__empty-text' in page_content}")
            
        finally:
            browser.close()


if __name__ == "__main__":
    test_search_result_count()
