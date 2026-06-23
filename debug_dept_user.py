"""调试部门和用户问题"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright
from config.settings import Settings

def debug_issues():
    settings = Settings()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. 调试用户添加重复用户名
            print("=" * 50)
            print("1. 调试用户添加重复用户名")
            print("=" * 50)
            
            page.goto(f"{settings.BASE_URL}/login")
            page.wait_for_load_state('domcontentloaded')
            
            page.locator(".login-form input[type='text']").first.fill(settings.USERNAME)
            page.locator(".login-form input[type='password']").fill(settings.PASSWORD)
            page.locator(".login-form input[type='text']").nth(1).fill("skip_captcha")
            page.locator(".login-form .el-button").first.click()
            page.wait_for_url("**/index**", timeout=10000)
            
            page.goto(f"{settings.BASE_URL}/system/user")
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_timeout(2000)
            
            # 点击新增按钮
            add_btn = page.get_by_role("button", name="新增")
            add_btn.first.click()
            page.wait_for_timeout(2000)
            
            # 填写表单
            dialog = page.locator(".el-dialog[aria-label='添加用户']")
            dialog.locator("input[placeholder*='用户']").first.fill("admin")
            dialog.locator("input[placeholder*='昵称']").fill("测试昵称")
            dialog.locator("input[placeholder*='密码']").fill("admin123")
            
            # 检查是否有表单错误
            form_errors = dialog.locator(".el-form-item__error")
            if form_errors.count() > 0:
                error_text = form_errors.first.text_content()
                print(f"表单错误: {error_text}")
            else:
                print("没有表单错误")
            
            # 点击保存
            save_btn = dialog.locator("button.el-button--primary")
            save_btn.click()
            page.wait_for_timeout(3000)
            
            # 检查消息
            messages = page.locator(".el-message, .el-alert, [role='alert']")
            print(f"找到 {messages.count()} 个消息元素")
            for i in range(messages.count()):
                msg_text = messages.nth(i).text_content()
                print(f"  消息{i}: {msg_text}")
            
            # 关闭对话框
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            
            # 2. 调试部门编辑
            print("\n" + "=" * 50)
            print("2. 调试部门编辑")
            print("=" * 50)
            
            page.goto(f"{settings.BASE_URL}/system/dept")
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_timeout(2000)
            
            # 点击新增部门
            add_dept_btn = page.get_by_role("button", name="新增")
            add_dept_btn.first.click()
            page.wait_for_timeout(2000)
            
            # 填写部门信息
            dept_dialog = page.locator(".el-dialog[aria-label='添加部门']")
            if dept_dialog.count() > 0:
                dept_dialog = dept_dialog.first
            else:
                dept_dialog = page.locator(".el-dialog:visible").first
            
            dept_dialog.locator("input[placeholder*='部门']").first.fill("测试部门_debug")
            dept_dialog.locator("button.el-button--primary").click()
            page.wait_for_timeout(3000)
            
            # 检查消息
            dept_messages = page.locator("[role='alert']")
            if dept_messages.count() > 0:
                msg = dept_messages.first.text_content()
                print(f"部门创建消息: {msg}")
            else:
                print("没有部门创建消息")
            
            # 搜索部门
            search_inputs = page.locator("input")
            print(f"找到 {search_inputs.count()} 个输入框")
            for i in range(search_inputs.count()):
                inp = search_inputs.nth(i)
                placeholder = inp.get_attribute("placeholder")
                inp_type = inp.get_attribute("type")
                print(f"  输入框{i}: placeholder='{placeholder}', type='{inp_type}'")
            
            # 查找搜索按钮
            all_buttons = page.get_by_role("button")
            print(f"找到 {all_buttons.count()} 个按钮")
            for i in range(all_buttons.count()):
                btn = all_buttons.nth(i)
                btn_text = btn.text_content().strip()
                if "查询" in btn_text or "搜索" in btn_text:
                    print(f"  搜索按钮: {btn_text}")
            
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    debug_issues()