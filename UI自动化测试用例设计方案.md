RuoYi 后台管理系统 UI 自动化测试用例设计方案

### **一、概述**

本方案基于 RuoYi 前后端分离版（Vue + Element UI + Spring Boot）设计，旨在通过 UI 自动化测试保障核心业务功能的稳定性和回归效率。设计遵循**测试金字塔**原则，将 UI 自动化聚焦于核心业务流程和频繁回归的场景，结合 **Page Object 模式**、**数据驱动**和**分层设计**，确保用例的可维护性、稳定性和可读性。

### **二、测试范围**

RuoYi 后台管理系统功能模块众多，UI 自动化测试覆盖以下核心模块（优先级由高到低）：

**模块**

**覆盖功能**

**优先级**

登录/注销

正常登录、密码错误、验证码错误、退出登录

P0

系统监控

在线用户、操作日志、登录日志的列表查看和搜索

P1

系统管理

**用户管理**：增删改查、重置密码、分配角色\
**角色管理**：增删改查、分配菜单权限\
**菜单管理**：增删改查、调整菜单树\
**部门管理**：增删改查、树形结构

P0/P1

系统工具

代码生成、表单构建等（视项目需求可选）

P2

> **说明**：P0 为冒烟测试级别，每次构建必须执行；P1 为高频回归，每日或每次迭代执行；P2 为低频回归，可按需执行。

### **三、自动化测试架构设计**

#### **1. 分层结构**

采用经典的四层架构：

- **用例层（TestCase）**：存放测试脚本，每个脚本对应一个业务场景，使用自然语言描述步骤，调用业务流程层方法。
- **业务流程层（BusinessFlow）**：组合多个页面操作完成一个业务流（如“创建用户并分配角色”），提高用例复用。
- **页面对象层（PageObject）**：每个页面一个类，封装页面元素定位和原子操作（点击、输入、获取文本等）。
- **基础层（Base）**：封装驱动初始化、等待工具、截图、报告、数据库连接等通用功能。

### 2.技术选型建议&#xA;测试框架：Pytest（Python）

- UI 自动化库：playwright
- 数据驱动：Pytest 的参数化或 Excel/CSV/YAML 数据文件
- 报告：Allure
- CI 集成：Jenkins / GitLab CI

**3.元素定位策略**

Playwright 推荐使用用户可见的属性定位，而非 XPath 或 CSS（虽然也支持）：

- **首选**：`get_by_role()`、`get_by_text()`、`get_by_label()`、`get_by_placeholder()`、`get_by_test_id()`（需开发添加 `data-testid`）。
- **次选**：`get_by_selector()` 使用稳定 CSS 选择器（如 `[name="username"]`、`#id`）。
- **避免**：依赖动态 class 或索引的 XPath。
  若项目未添加 `data-testid`，可约定使用 Playwright 的选择器组合

```Python
# 定位新增按钮：包含文本“新增”的按钮
page.get_by_role("button", name="新增")

# 定位用户名输入框：placeholder 为“请输入用户名称”
page.get_by_placeholder("请输入用户名称")

# 定位表格中的某行
page.get_by_role("row", name="测试用户").get_by_role("button", name="编辑")
```

#### **4. 测试夹具（conftest.py）**

利用 Pytest 的 fixture 管理浏览器和页面：

**5.测试数据管理**

- **静态配置**：`config.py` 存放 URL、管理员账号、浏览器设置。
- **动态数据生成**：`utils/data_generator.py` 提供唯一用户名、手机号等。
- **数据清理**：用例执行后通过 API 删除测试数据，或使用数据库回滚。

### 6.异常与稳定性处理

- 页面加载，可以使用 `page.wait_for_load_state("networkidle")` 或等待特定元素出现
- 失败重试：针对网络波动等非业务原因导致的失败，用例层支持重试机制（如 Pytest 的 @flaky）。
- 原子用例：每个用例独立，不依赖其他用例的执行结果。

**7.并发执行与浏览器矩阵**

- 使用 Pytest 的 `pytest-xdist` 插件并行运行用例（需注意测试隔离，每个 worker 独立浏览器上下文）。
- 在 conftest.py 中根据环境变量切换浏览器类型（`browser_type`）。

## **四、测试用例设计（金字塔原则）**

遵循**测试金字塔**理论，UI自动化应处于最顶端，数量最少。

1. **单模块用例**：单个页面内的交互验证（如输入框校验、滑块拖动）。
2. **流程用例**：跨模块的业务串联（核心商业价值流，如“搜索商品->加入购物车->支付成功”）。
3. **探索式用例**：随机路径、异常中断（如支付中途断网重连）。

### **三类用例的定义与设计要点**

**类型--/定义---/设计目标---/示例（RuoYi）**

**单模块用例**

针对单个页面或单个功能的独立验证，不依赖其他模块。

快速定位模块内缺陷，覆盖边界和异常。

示例：用户管理页面的新增、编辑、删除、搜索、表单校验。

**端到端业务流**

跨越多个模块或页面的完整业务流程，模拟真实用户操作路径。

验证核心业务逻辑的完整性和数据一致性。

示例：从登录到创建用户并分配角色，再到该用户登录验证权限。

**探索式场景**

模拟真实用户的随机操作、异常操作或复杂组合，发现系统潜在问题。

发现自动化脚本难以覆盖的非预期场景和稳定性问题。

示例：频繁切换菜单、快速点击保存、输入超长字符、断网重连等。

### **单模块用例设计**

#### **2.1 设计原则**

- **独立**：不依赖其他用例的执行结果，每个用例可单独运行。
- **聚焦**：只测试一个页面或一个功能点，避免跨模块交互。
- **数据驱动**：使用参数化覆盖正常、边界和异常输入。
- **页面对象封装**：操作通过页面对象的方法完成，保持用例可读性。

#### **2.2 代码组织**

在 `tests/ui/level1` 下按模块分文件，如 `test_user_module.py`、`test_role_module.py`。

#### **2.3 示例：用户管理单模块用例**

```Python
# test_cases/test_user_module.py
import pytest
from business_flows.user_flow import UserFlow
from utils.data_generator import generate_unique_username

@pytest.mark.module
class TestUserModule:
    """用户管理模块单模块测试"""

    def test_add_user_success(self, user_flow):
        """正常新增用户"""
        username = generate_unique_username()
        user_flow.create_user(username=username)
        user_flow.user_page.search(username)
        expect(user_flow.page.get_by_role("row", name=username)).to_be_visible()

    @pytest.mark.parametrize("phone, expected_tip", [
        ("123", "手机号码格式错误"),
        ("13800138000", ""),
        ("abcdefg", "手机号码格式错误"),
    ])
    def test_phone_validation(self, user_flow, phone, expected_tip):
        """手机号格式校验"""
        user_flow.user_page.navigate().click_add().fill_user_form(phone=phone).click_save()
        if expected_tip:
            expect(user_flow.page.get_by_text(expected_tip)).to_be_visible()
        else:
            expect(user_flow.page.get_by_text("新增成功")).to_be_visible()

    def test_delete_user(self, user_flow):
        """删除用户"""
        # 先创建用户
        username = generate_unique_username()
        user_flow.create_user(username=username)
        # 删除
        user_flow.user_page.search(username)
        user_flow.page.get_by_role("row", name=username).get_by_role("button", name="删除").click()
        user_flow.page.get_by_role("button", name="确 定").click()
        expect(user_flow.page.get_by_text("删除成功")).to_be_visible()
        user_flow.user_page.search(username)
        expect(user_flow.page.get_by_text("暂无数据")).to_be_visible()
```

#### **2.4 断言策略**

- **UI 断言**：验证页面元素是否出现、文本是否正确、提示是否显示。
- **可选**：通过数据库验证数据落库（适合重要操作，但会增加复杂度）。

### **端到端业务流用例设计**

#### **3.1 设计原则**

- **完整业务价值**：模拟一个完整的用户故事，如“管理员创建新用户并分配角色，新用户登录验证权限”。
- **跨模块协作**：依赖多个页面对象和业务流程层，复用已有业务流。
- **数据清理**：测试前准备数据，测试后清理数据（通过 API 或数据库），保证可重复执行。
- **稳定性优先**：使用显式等待和重试机制，但 Playwright 的自动等待已足够。

#### **3.2 代码组织**

在 `tests/ui/level2` 下按业务域划分，如 `test_user_e2e.py`，并使用 `@pytest.mark.e2e` 标记。

#### **3.3 示例：用户创建与角色分配端到端流程**

#### **3.4 断言策略**

- **业务结果验证**：最终状态是否符合预期（如页面跳转、数据变化）。
- **数据一致性**：可结合数据库断言，确保多个表的数据正确。
- **跨系统验证**：如果涉及外部系统，可模拟或验证接口调用。

### **探索式测试场景设计**

**4.1 设计原则**

- **随机性与组合**：使用随机数据、随机操作序列，模拟真实用户行为。
- **异常与恢复**：注入异常（如网络中断、服务器错误）并验证系统行为。
- **状态验证**：关注系统是否崩溃、数据是否错乱、是否给出合理提示。
- **自动化可行性**：探索式测试通常以手工为主，但可自动化部分场景，如“随机点击菜单+随机表单填写”持续运行一段时间。

#### **4.2 代码组织**

建议单独放在 `tests/ui/level3` 目录下，使用 `@pytest.mark.exploratory` 标记，并设置较长的超时时间。

#### **4.3 示例：随机操作与异常注入**

```Python
# test_cases/exploratory/test_random_ops.py
import pytest
import random
from playwright.sync_api import expect

@pytest.mark.exploratory
@pytest.mark.flaky(reruns=0)  # 不重试，真实记录失败
def test_random_menu_click_and_form_submit(user_flow):
    """随机点击菜单并在表单中输入随机内容"""
    page = user_flow.page
    user_flow.login_as_admin()
    # 获取所有菜单项（模拟用户随意点击）
    menus = page.locator(".el-menu .el-menu-item").all()
    for _ in range(10):  # 随机点击10次
        menu = random.choice(menus)
        menu.click()
        page.wait_for_timeout(1000)  # 等待页面加载
        # 如果当前页面有表单，随机填写并提交
        if page.locator("form").count() > 0:
            # 随机填写输入框
            inputs = page.locator("input:not([type='hidden'])").all()
            for inp in inputs:
                if inp.is_visible():
                    inp.fill(str(random.randint(1, 1000)) + "测试")
            # 随机点击按钮
            buttons = page.locator("button:has-text('提交'), button:has-text('保存'), button:has-text('查询')").all()
            if buttons:
                random.choice(buttons).click()
                page.wait_for_timeout(2000)
        # 验证页面没有崩溃（无JS错误）
        assert not page.evaluate("window.jsErrors && window.jsErrors.length > 0")
```

#### **4.4 示例：异常注入（网络中断）**

#### **4.5 断言策略**

- **系统健壮性**：页面不崩溃，给出合理错误提示。
- **数据一致性**：异常后数据未发生错误变更。
- **日志与监控**：可结合前端错误监控，断言无 JavaScript 异常。

### **五、断言策略**

- **UI 断言**：优先验证页面上出现的提示信息、数据变化（如表格出现新行）、元素状态（按钮禁用/启用）。
- **数据库断言**（可选）：对于重要数据变更（如新增用户），可通过数据库直连验证数据是否落库，提高可靠性。
- **避免模糊断言**：如截图对比、位置坐标等，除非必要。

### **六、执行策略与 CI 集成**

1. **触发时机**：
   - 每次代码合并到主分支时执行 P0 冒烟用例。
   - 每日夜间构建执行全部 P0+P1 用例。
   - 版本发布前执行全量用例（含 P2）。
2. **并发执行**：使用 Selenium Grid 或多线程（如 pytest-xdist）在多个浏览器（Chrome、Firefox）上并行执行，缩短执行时间。
3. **失败处理**：用例失败自动截图并附加到 Allure 报告，同时发送飞书/钉钉通知。支持失败用例自动重跑 1 次（仅限网络或偶发因素）。
4. **持续集成与报告**
   - 集成 Allure 生成美观报告，包含截图、视频、Trace

