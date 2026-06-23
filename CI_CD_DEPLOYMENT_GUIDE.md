# RuoYi 全栈测试 CI/CD 部署指南

## 概述

本指南说明如何将 `ruoyi_fullstack_test` 自动化测试代码和 RuoYi-Vue 测试环境通过 Docker 技术集成到 Jenkins 或 GitLab CI 中，实现代码变更触发和每日凌晨定时构建、部署、测试和报告归档。

---

## 环境要求

### 基础环境
- Docker 20.10+
- Docker Compose 2.0+
- JDK 17+（后端构建）
- Maven 3.8+（后端构建）
- Node.js 18+（前端构建）
- Python 3.9+（测试运行器）

### Jenkins 环境（可选）
- Jenkins 2.300+
- 插件：Pipeline、HTML Publisher、JUnit、Docker、Email Extension

### GitLab CI 环境（可选）
- GitLab 15.0+
- GitLab Runner（支持 Docker-in-Docker）

---

## 项目结构

```
ruoyi-ui/
├── RuoYi-Vue/                    # RuoYi-Vue 源码
│   ├── ruoyi-admin/              # 后端应用
│   ├── ruoyi-ui/                 # 前端应用
│   └── sql/                      # 数据库初始化脚本
└── ruoyi_fullstack_test/         # 自动化测试项目
    ├── Dockerfile                # 测试运行器镜像
    ├── docker-compose.yml        # Docker 编排配置
    ├── .env                      # 环境变量配置
    ├── Jenkinsfile               # Jenkins Pipeline 配置
    ├── ci/gitlab-ci/.gitlab-ci.yml # GitLab CI 配置
    ├── config/nginx.conf         # Nginx 配置
    ├── start-services.sh/bat     # 服务启动脚本
    ├── run-tests.sh/bat          # 测试执行脚本
    └── stop-services.sh/bat      # 服务停止脚本
```

---

## Docker 环境配置

### 1. 环境变量配置

编辑 `.env` 文件配置环境变量：

```env
DB_HOST=mysql
DB_PORT=3306
DB_NAME=ry-vue
DB_USERNAME=root
DB_PASSWORD=123456

REDIS_HOST=redis
REDIS_PORT=6379

ADMIN_PORT=8080
UI_PORT=80

BASE_URL=http://ruoyi-ui:80
API_BASE_URL=http://ruoyi-admin:8080

TEST_USERNAME=admin
TEST_PASSWORD=admin123

BROWSER=chromium
HEADLESS=true
```

### 2. 启动测试环境

**Linux/Mac：**
```bash
./start-services.sh
```

**Windows：**
```cmd
start-services.bat
```

### 3. 执行自动化测试

**Linux/Mac：**
```bash
./run-tests.sh
```

**Windows：**
```cmd
run-tests.bat
```

### 4. 停止测试环境

**Linux/Mac：**
```bash
./stop-services.sh
```

**Windows：**
```cmd
stop-services.bat
```

---

## Jenkins 配置

### 安装插件

1. 登录 Jenkins → 管理 Jenkins → 插件管理
2. 安装以下插件：
   - Pipeline
   - HTML Publisher
   - JUnit
   - Docker
   - Email Extension
   - Timestamper
   - AnsiColor

### 创建 Pipeline 任务

1. 点击「新建任务」
2. 输入任务名称：`ruoyi-fullstack-test`
3. 选择「流水线」→ 点击「确定」

### 配置任务

#### 基本配置
- **描述**: RuoYi 全栈自动化测试

#### 构建触发器
- 勾选「GitHub hook trigger for GITScm polling」（代码变更触发）
- 勾选「Build periodically」
- **日程表**: `0 0 * * *` （每天凌晨 0:00 执行）

#### 流水线定义
- 选择「Pipeline script from SCM」
- **SCM**: Git
- **Repository URL**: `你的代码仓库地址`
- **Credentials**: 配置 Git 凭证
- **Branch Specifier**: `*/main`
- **Script Path**: `Jenkinsfile`

#### 环境变量（可选）
添加以下环境变量：
- `DOCKER_HOST`: `tcp://localhost:2376`
- `TEST_USERNAME`: `admin`
- `TEST_PASSWORD`: `admin123`

### Jenkins Pipeline 阶段说明

| 阶段 | 说明 |
|------|------|
| Checkout | 代码检出 |
| Build Backend | 构建后端 Maven 应用 |
| Build Frontend | 构建前端 Vue 应用 |
| Build Docker Images | 构建 Docker 镜像 |
| Start Services | 启动测试环境服务 |
| Health Check | 服务健康检查 |
| Smoke Test | 冒烟测试 |
| API Test | API 接口测试 |
| UI Test | UI 自动化测试 |
| Integration Test | 集成测试 |
| Performance Test | 性能测试 |
| Security Test | 安全测试 |
| Stop Services | 停止服务 |

---

## GitLab CI 配置

### Runner 配置

确保 GitLab Runner 支持 Docker-in-Docker：

```toml
[[runners]]
  name = "docker-runner"
  url = "https://gitlab.example.com/"
  token = "your-runner-token"
  executor = "docker"
  [runners.docker]
    tls_verify = false
    image = "docker:latest"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
```

### 定时任务配置

在 GitLab 项目中配置定时任务：
1. 进入项目 → Settings → CI/CD → Schedules
2. 添加新的 Schedule
   - **Description**: 每日凌晨测试
   - **Cron**: `0 0 * * *`
   - **Target branch**: `main`
   - **Active**: 勾选

---

## 测试报告

### 报告位置

| 报告类型 | 路径 |
|----------|------|
| 冒烟测试 | `reports/html/smoke_report.html` |
| API 测试 | `reports/html/api_report.html` |
| UI 测试 | `reports/html/ui_report.html` |
| 集成测试 | `reports/html/integration_report.html` |
| 性能测试 | `reports/html/performance_report.html` |
| 安全测试 | `reports/html/security_report.html` |

### Jenkins 报告查看

1. 进入 Jenkins 任务 → 构建历史
2. 点击具体构建 → HTML Report（HTML 报告）
3. 点击具体构建 → Test Result（JUnit 报告）

---

## 故障排除

### 常见问题

1. **Docker 构建失败**
   - 检查 Docker 是否运行
   - 检查 Dockerfile 语法
   - 检查网络连接

2. **服务启动超时**
   - 增加 `docker-compose up` 后的等待时间
   - 检查 MySQL/Redis 服务是否正常启动
   - 检查后端应用日志

3. **测试执行失败**
   - 检查测试运行器容器是否正常运行
   - 检查环境变量配置
   - 检查测试代码依赖

4. **报告无法显示**
   - 确保 HTML Publisher 插件已安装
   - 检查报告路径配置
   - 检查 Jenkins 用户权限

5. **Jenkins Docker 权限问题**
   - 将 Jenkins 用户添加到 docker 组
   - 重启 Jenkins 服务

---

## 配置文件清单

| 文件 | 说明 |
|------|------|
| `Dockerfile` | 测试运行器 Docker 镜像配置 |
| `docker-compose.yml` | Docker Compose 编排配置 |
| `.env` | 环境变量配置 |
| `Jenkinsfile` | Jenkins Pipeline 配置 |
| `ci/gitlab-ci/.gitlab-ci.yml` | GitLab CI 配置 |
| `config/nginx.conf` | Nginx 反向代理配置 |
| `start-services.sh/bat` | 服务启动脚本 |
| `run-tests.sh/bat` | 测试执行脚本 |
| `stop-services.sh/bat` | 服务停止脚本 |