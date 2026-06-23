# Ruoyi 全栈测试框架

## 项目简介

Ruoyi 全栈测试框架是一个基于 Python + Pytest + Playwright 的综合测试框架，用于对 Ruoyi 管理系统进行全面的测试，包括接口测试、UI 测试、性能测试和安全测试。

## 项目结构

```
ruoyi_fullstack_test/
 ├── README.md
 ├── requirements.txt
 ├── pytest.ini
 ├── .env
 ├── docker-compose.yml                  # 测试环境编排
 │
 ├── config/                             # 配置中心
 │   ├── __init__.py
 │   ├── settings.py                     # 全局配置
 │   ├── environments.yaml               # 多环境配置
 │   ├── locator_map.yaml                # UI 元素定位
 │   ├── api_spec.yaml                   # API 规范定义
 │   └── test_levels.py                  # 测试级别定义
 │
 ├── common/                             # 公共模块
 │   ├── __init__.py
 │   ├── base_test.py                    # 测试基类
 │   ├── assertions.py                   # 断言封装
 │   ├── logger.py                       # 日志工具
 │   ├── report.py                       # 报告生成
 │   └── utils/
 │       ├── db_helper.py                # 数据库辅助
 │       ├── data_factory.py             # 数据工厂
 │       ├── crypto.py                   # 加密工具
 │       └── file_helper.py              # 文件处理
 │
 ├── api/                                # 接口测试层
 │   ├── __init__.py
 │   ├── clients/                        # API 客户端
 │   │   ├── __init__.py
 │   │   ├── base_client.py              # 基础客户端
 │   │   ├── auth_client.py              # 认证接口
 │   │   ├── user_client.py              # 用户接口
 │   │   ├── role_client.py              # 角色接口
 │   │   ├── menu_client.py              # 菜单接口
 │   │   └── monitor_client.py           # 监控接口
 │   ├── models/                         # 数据模型
 │   │   ├── user.py
 │   │   ├── role.py
 │   │   └── response.py
 │   ├── schemas/                        # 请求/响应 schema
 │   │   ├── user_schema.py
 │   │   └── role_schema.py
 │   └── fixtures/                       # 接口测试夹具
 │       ├── auth_fixtures.py
 │       └── data_fixtures.py
 │
 ├── ui/                                 # UI 测试层
 │   ├── __init__.py
 │   ├── pages/                          # Page Object
 │   │   ├── base_page.py
 │   │   ├── components/                 # 组件层
 │   │   ├── modules/                    # 模块层
 │   │   └── flows/                      # 业务流层
 │   └── fixtures/                       # UI 测试夹具
 │       ├── browser_fixtures.py
 │       └── page_fixtures.py
 │
 ├── performance/                        # 性能测试层
 │   ├── __init__.py
 │   ├── scenarios/                      # 性能场景
 │   │   ├── login_stress.py             # 登录压力测试
 │   │   ├── user_crud_load.py           # 用户 CRUD 负载测试
 │   │   ├── concurrent_api.py           # 并发接口测试
 │   │   └── endurance_test.py           # 稳定性测试
 │   ├── config/                         # 性能测试配置
 │   │   ├── load_profiles.yaml          # 负载配置
 │   │   └── thresholds.yaml             # 性能阈值
 │   ├── scripts/                        # Locust/JMeter 脚本
 │   │   ├── locustfile.py
 │   │   └── jmeter/
 │   └── reports/                        # 性能报告
 │
 ├── security/                           # 安全测试层
 │   ├── __init__.py
 │   ├── scanners/                       # 安全扫描器
 │   │   ├── owasp_scanner.py            # OWASP 扫描
 │   │   ├── sql_injection.py            # SQL 注入检测
 │   │   ├── xss_scanner.py              # XSS 检测
 │   │   ├── auth_scanner.py             # 认证安全检测
 │   │   └── api_security.py             # API 安全检测
 │   ├── scenarios/                      # 安全测试场景
 │   │   ├── auth_security.py            # 认证安全
 │   │   ├── data_security.py            # 数据安全
 │   │   ├── session_security.py         # 会话安全
 │   │   └── input_validation.py         # 输入验证
 │   └── reports/                        # 安全报告
 │
 ├── tests/                              # 测试用例层
 │   ├── __init__.py
 │   ├── conftest.py                     # pytest 配置
 │   │
 │   ├── api/                            # 接口测试用例
 │   │   ├── level1/                     # L1: 单接口测试
 │   │   ├── level2/                     # L2: 接口模块测试
 │   │   └── level3/                     # L3: 接口业务流测试
 │   │
 │   ├── ui/                             # UI 测试用例
 │   │   ├── level1/                     # L1: 组件测试
 │   │   ├── level2/                     # L2: 单模块测试
 │   │   └── level3/                     # L3: 业务流测试
 │   │
 │   ├── integration/                    # 集成测试 (UI+API)
 │   │   ├── test_ui_api_sync.py         # UI 与 API 数据一致性
 │   │   ├── test_cross_module.py        # 跨模块集成
 │   │   └── test_end_to_end.py          # 端到端集成
 │   │
 │   ├── performance/                    # 性能测试用例
 │   │   ├── test_api_performance.py
 │   │   ├── test_ui_performance.py
 │   │   └── test_system_stability.py
 │   │
 │   └── security/                       # 安全测试用例
 │       ├── test_auth_security.py
 │       ├── test_input_security.py
 │       ├── test_api_security.py
 │       └── test_data_security.py
 │
 ├── suites/                             # 测试套件
 │   ├── smoke_suite.py                  # 冒烟测试
 │   ├── regression_suite.py             # 回归测试
 │   ├── api_suite.py                    # 接口测试套件
 │   ├── ui_suite.py                     # UI 测试套件
 │   ├── performance_suite.py            # 性能测试套件
 │   ├── security_suite.py               # 安全测试套件
 │   └── nightly_suite.py                # 夜间全量套件
 │
 ├── data/                               # 测试数据
 │   ├── api/
 │   │   ├── requests/
 │   │   └── responses/
 │   ├── ui/
 │   └── performance/
 │
 ├── reports/                            # 测试报告
 │   ├── html/
 │   ├── allure/
 │   ├── performance/
 │   └── security/
 │
 └── ci/                                 # CI/CD 配置
     ├── jenkins/
     ├── github-actions/
     └── gitlab-ci/
```

## 环境要求

- Python 3.8+
- Pytest 7.0+
- Playwright 1.30+
- Requests 2.28+
- Pydantic 2.0+
- PyYAML 6.0+
- Allure Report (可选)

## 安装依赖

```bash
pip install -r requirements.txt
playwright install
```

## 配置环境变量

复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置：

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑环境变量
# 填写正确的 BASE_URL、USERNAME、PASSWORD 等配置
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行指定测试套件

```bash
# 运行冒烟测试
pytest -m smoke

# 运行接口测试
pytest tests/api/

# 运行UI测试
pytest tests/ui/

# 运行性能测试
pytest tests/performance/

# 运行安全测试
pytest tests/security/
```

### 生成测试报告

```bash
# 生成HTML报告
pytest --html=reports/html/report.html

# 生成Allure报告
pytest --alluredir=reports/allure
allure serve reports/allure
```

## 测试套件

- **smoke_suite.py**: 冒烟测试，验证系统核心功能
- **regression_suite.py**: 回归测试，验证系统稳定性
- **api_suite.py**: 接口测试套件，测试所有API接口
- **ui_suite.py**: UI测试套件，测试所有UI功能
- **performance_suite.py**: 性能测试套件，测试系统性能
- **security_suite.py**: 安全测试套件，测试系统安全性
- **nightly_suite.py**: 夜间全量测试，包含所有测试用例

## 测试级别

- **L1**: 单接口/组件测试，测试单个功能点
- **L2**: 模块测试，测试完整的功能模块
- **L3**: 业务流测试，测试完整的业务流程

## 贡献指南

1. Fork 本项目
2. 创建功能分支
3. 提交代码
4. 运行测试确保代码质量
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。
